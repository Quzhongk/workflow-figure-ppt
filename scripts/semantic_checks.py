"""Optional declared-role checks. No scientific topology is inferred here."""
from __future__ import annotations

import math
from xml.etree import ElementTree as ET

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
EMU_PER_PX = 9525


def check_keys(value, allowed, context):
    if not isinstance(value, dict):
        raise ValueError(f'{context} must be an object')
    extra = set(value) - set(allowed)
    if extra:
        raise ValueError(f'{context}: unknown fields {sorted(extra)}')


def validate_spec(spec):
    check_keys(spec, {'version', 'allowed_fonts', 'top_headings', 'top_heading_font',
                      'typography_groups', 'geometry_groups', 'connections'}, 'spec')
    if spec.get('version') != 1:
        raise ValueError('spec.version must be 1')
    for key in ('top_headings', 'typography_groups', 'geometry_groups', 'connections'):
        if key in spec and not isinstance(spec[key], list):
            raise ValueError(f'spec.{key} must be an array')
    if 'allowed_fonts' in spec:
        fonts = spec['allowed_fonts']
        if not isinstance(fonts, list) or not fonts or not all(isinstance(f, str) and f.strip() for f in fonts):
            raise ValueError('allowed_fonts must be a nonempty array of font names')
    if 'top_heading_font' in spec and not isinstance(spec['top_heading_font'], str):
        raise ValueError('top_heading_font must be a font name')


class FigureIndex:
    def __init__(self, root):
        self.parents = {child: parent for parent in root.iter() for child in parent}
        self.items = []
        for tag, nv in [('sp', 'nvSpPr'), ('cxnSp', 'nvCxnSpPr'), ('grpSp', 'nvGrpSpPr')]:
            for el in root.findall(f'.//p:{tag}', NS):
                prop = el.find(f'p:{nv}/p:cNvPr', NS)
                if prop is not None:
                    self.items.append((el, tag, prop.get('id'), prop.get('name', '')))

    def select(self, selector):
        check_keys(selector, {'id', 'name', 'kind'}, 'selector')
        if ('id' in selector) == ('name' in selector):
            raise ValueError('selector needs exactly one of id or name')
        kind = selector.get('kind')
        if kind not in (None, 'shape', 'box', 'text', 'connector', 'group'):
            raise ValueError(f'Unknown selector kind: {kind}')
        matches = []
        for el, tag, ident, name in self.items:
            if 'id' in selector and ident != str(selector['id']):
                continue
            if 'name' in selector and name != selector['name']:
                continue
            has_text = bool(el.findall('p:txBody//a:t', NS))
            if kind == 'text' and not (tag == 'sp' and has_text): continue
            if kind == 'box' and not (tag == 'sp' and not has_text): continue
            if kind == 'shape' and tag != 'sp': continue
            if kind == 'connector' and tag != 'cxnSp': continue
            if kind == 'group' and tag != 'grpSp': continue
            matches.append(el)
        if len(matches) != 1:
            raise ValueError(f'Selector {selector} matched {len(matches)} objects; use a unique name/id')
        return matches[0]

    def identity(self, el):
        return next(ident for obj, _, ident, _ in self.items if obj is el)

    def bounds(self, el):
        xf = el.find('p:spPr/a:xfrm', NS)
        if xf is None: xf = el.find('p:grpSpPr/a:xfrm', NS)
        if xf is None: raise ValueError('No explicit geometry for selected object')
        if int(xf.get('rot', '0')) % 21600000:
            raise ValueError('Rotated geometry requires visual validation; not supported by this check')
        off, ext = xf.find('a:off', NS), xf.find('a:ext', NS)
        if off is None or ext is None: raise ValueError('Incomplete geometry')
        x, y, w, h = (float(off.get('x')), float(off.get('y')),
                       float(ext.get('cx')), float(ext.get('cy')))
        parent = self.parents.get(el)
        while parent is not None:
            if parent.tag == '{' + NS['p'] + '}grpSp':
                gx = parent.find('p:grpSpPr/a:xfrm', NS)
                if gx is None: raise ValueError('Group lacks explicit geometry')
                if int(gx.get('rot', '0')) % 21600000 or gx.get('flipH') in ('1', 'true') or gx.get('flipV') in ('1', 'true'):
                    raise ValueError('Rotated/flipped groups need visual validation; not supported by this check')
                go, ge, co, ce = [gx.find('a:' + key, NS) for key in ('off', 'ext', 'chOff', 'chExt')]
                if any(v is None for v in (go, ge, co, ce)): raise ValueError('Incomplete group transform')
                sx, sy = float(ge.get('cx')) / float(ce.get('cx')), float(ge.get('cy')) / float(ce.get('cy'))
                x = float(go.get('x')) + (x - float(co.get('x'))) * sx
                y = float(go.get('y')) + (y - float(co.get('y'))) * sy
                w, h = w * sx, h * sy
            parent = self.parents.get(parent)
        return {key: val / EMU_PER_PX for key, val in
                {'left': x, 'top': y, 'width': w, 'height': h,
                 'center_x': x + w / 2, 'center_y': y + h / 2}.items()}


def typography(el):
    """Explicit run properties, falling back to paragraph default run properties."""
    signatures = set()
    for para in el.findall('p:txBody/a:p', NS):
        default = para.find('a:pPr/a:defRPr', NS)
        for run in list(para.findall('a:r', NS)) + list(para.findall('a:fld', NS)):
            t = run.find('a:t', NS)
            if t is None or not (t.text or '').strip(): continue
            prop = run.find('a:rPr', NS)
            chain = [p for p in (prop, default) if p is not None]
            def attr(key):
                return next((p.get(key) for p in chain if p.get(key) is not None), None)
            font = next((p.find('a:latin', NS).get('typeface') for p in chain if p.find('a:latin', NS) is not None), None)
            size = attr('sz')
            if not font or font.startswith('+') or size is None:
                raise ValueError('Typography check needs explicit font and size; theme/master inheritance requires manual review')
            signatures.add((font.casefold(), float(size) / 100, attr('b') in ('1', 'true')))
    if len(signatures) != 1:
        raise ValueError(f'Expected one font/size/weight style, found {len(signatures)}')
    return next(iter(signatures))


def tolerance(item):
    value = item.get('tolerance_px', 1.0)
    if not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError('tolerance_px must be a finite nonnegative number')
    return value


def check_semantics(root, spec):
    validate_spec(spec)
    index, errors = FigureIndex(root), []

    def attempt(label, fn):
        try:
            fn()
        except (ValueError, TypeError, KeyError, AttributeError, ZeroDivisionError) as exc:
            errors.append(f'{label}: {exc}')

    def type_group(item):
        check_keys(item, {'members', 'font', 'size_pt', 'bold'}, 'typography group')
        if not isinstance(item.get('members'), list) or not item['members']:
            raise ValueError('members must be a nonempty array')
        styles = [typography(index.select(sel)) for sel in item['members']]
        if len(set(styles)) != 1: raise ValueError('Peer font, size, or weight differs')
        font, size, bold = styles[0]
        if 'font' in item and font != item['font'].casefold(): raise ValueError(f'Expected font {item["font"]}, found {font}')
        if 'size_pt' in item and abs(size - float(item['size_pt'])) > 0.02: raise ValueError(f'Expected {item["size_pt"]} pt, found {size}')
        if 'bold' in item:
            if not isinstance(item['bold'], bool): raise ValueError('bold must be boolean')
            if bold != item['bold']: raise ValueError('Unexpected text weight')

    if spec.get('top_headings'):
        attempt('Top-level headings', lambda: type_group({'members': spec['top_headings'], 'font': spec.get('top_heading_font', 'Arial Black')}))
    for i, item in enumerate(spec.get('typography_groups', [])):
        attempt(f'Typography group {i + 1}', lambda item=item: type_group(item))

    def geometry_group(item):
        check_keys(item, {'members', 'equal', 'aligned', 'tolerance_px'}, 'geometry group')
        if not isinstance(item.get('members'), list) or len(item['members']) < 2:
            raise ValueError('geometry members needs at least two selectors')
        equal = item.get('equal', [])
        if not isinstance(equal, list) or any(k not in ('width', 'height') for k in equal):
            raise ValueError('equal supports width and height')
        aligned = item.get('aligned')
        if aligned not in (None, 'left', 'top', 'center_x', 'center_y'):
            raise ValueError('Unknown alignment axis')
        keys = equal + ([aligned] if aligned else [])
        if not keys: raise ValueError('Declare equal or aligned geometry')
        boxes = [index.bounds(index.select(sel)) for sel in item['members']]
        for key in keys:
            values = [b[key] for b in boxes]
            if max(values) - min(values) > tolerance(item): raise ValueError(f'Peer {key} differs')

    for i, item in enumerate(spec.get('geometry_groups', [])):
        attempt(f'Geometry group {i + 1}', lambda item=item: geometry_group(item))

    def connection(item):
        check_keys(item, {'connector', 'from', 'to', 'axis', 'straight', 'direction', 'tolerance_px'}, 'connection')
        con = index.select(item['connector'])
        if con.tag != '{' + NS['p'] + '}cxnSp': raise ValueError('Expected native connector')
        ends = con.find('p:nvCxnSpPr/p:cNvCxnSpPr', NS)
        for spec_key, xml_key in (('from', 'stCxn'), ('to', 'endCxn')):
            if spec_key in item:
                endpoint = ends.find('a:' + xml_key, NS) if ends is not None else None
                expected = index.identity(index.select(item[spec_key]))
                if endpoint is None or endpoint.get('id') != expected:
                    raise ValueError(f'Incorrect or unbound {spec_key} endpoint')
        axis = item.get('axis')
        if axis not in (None, 'vertical', 'horizontal'): raise ValueError('axis must be vertical or horizontal')
        if axis:
            box = index.bounds(con)
            if box['width' if axis == 'vertical' else 'height'] > tolerance(item):
                raise ValueError(f'Connector is not {axis}')
        if 'straight' in item and not isinstance(item['straight'], bool): raise ValueError('straight must be boolean')
        if item.get('straight'):
            geom = con.find('p:spPr/a:prstGeom', NS)
            if geom is None or geom.get('prst') not in ('line', 'straightConnector1'):
                raise ValueError('Expected straight connector geometry')
        direction = item.get('direction')
        if direction not in (None, 'forward', 'bidirectional', 'none'): raise ValueError('Unknown direction')
        if direction:
            ln = con.find('p:spPr/a:ln', NS)
            def has_arrow(name):
                end = ln.find('a:' + name, NS) if ln is not None else None
                return end is not None and end.get('type', 'none') != 'none'
            actual = (has_arrow('headEnd'), has_arrow('tailEnd'))
            expected = {'forward': (False, True), 'bidirectional': (True, True), 'none': (False, False)}[direction]
            if actual != expected: raise ValueError(f'Arrowheads do not encode {direction}')

    for i, item in enumerate(spec.get('connections', [])):
        attempt(f'Connection {i + 1}', lambda item=item: connection(item))
    return errors
