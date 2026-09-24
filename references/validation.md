# Optional semantic validation

Run the baseline native-object audit for every deliverable:

```text
python scripts/audit_pptx.py figure.pptx
```

For repeated roles or important geometry/edges, also create a task-specific JSON specification in the build directory, then run:

```text
python scripts/audit_pptx.py figure.pptx --spec figure-spec.json --json
```

The spec describes intended invariants, not a fixed scientific architecture. Do not change intended assertions merely to fit a faulty output. Use unique native shape names during authoring. Selectors accept exactly one of `name` or `id`, plus an optional `kind`: `text`, `box` (text-free shape), `shape`, `connector`, or `group`. Duplicate/missing matches fail rather than choosing an arbitrary object.

Example (names are illustrative, not built-in roles):

```json
{
  "version": 1,
  "allowed_fonts": ["Arial", "Arial Black"],
  "top_heading_font": "Arial Black",
  "top_headings": [
    {"name": "heading:input", "kind": "text"},
    {"name": "heading:method", "kind": "text"}
  ],
  "typography_groups": [{
    "members": [{"name": "label:a"}, {"name": "label:b"}],
    "font": "Arial", "size_pt": 15, "bold": true
  }],
  "geometry_groups": [{
    "members": [{"name": "node:a"}, {"name": "node:b"}],
    "equal": ["width", "height"], "aligned": "center_x", "tolerance_px": 1
  }],
  "connections": [{
    "connector": {"name": "edge:a-b"},
    "from": {"name": "node:a"}, "to": {"name": "node:b"},
    "axis": "vertical", "straight": true, "direction": "forward"
  }]
}
```

All top-level fields except `version` are optional. `allowed_fonts` overrides the default Arial/Arial Black policy only to reflect an actual user/reference font choice.

- `top_headings`: all selected labels must share font, size, and boldness, and use `top_heading_font` (default Arial Black). A global title is not required.
- `typography_groups`: nonempty peer selections must share font/size/boldness. Optional `font`, `size_pt`, and `bold` assert expected values. Italic scientific terms are allowed; italic is not compared.
- `geometry_groups`: at least two members; `equal` can contain `width`/`height`; `aligned` can be `left`, `top`, `center_x`, or `center_y`. Omit alignment for triangular peers. Default tolerance is 1 CSS pixel at 96 dpi.
- `connections`: selects an actual native connector. Optional `from`/`to` assert bound start/end object identities; omit them for intentionally gapped, unbound endpoints rather than attaching a line solely to satisfy the audit. `axis` is `vertical` or `horizontal`; omit it for deliberate diagonals. `straight: true` rejects bent/custom geometry. `direction` is `forward` (end arrow only), `bidirectional` (both arrows), or `none`. Omit assertions that do not apply. Check intended endpoint gaps and object crossings in the rendered slide.

Typography checks require explicit run or paragraph-default font and size. Unresolved theme/master inheritance is reported, not guessed. Geometry supports translation/scaling of nested groups; selected rotated geometry or rotated/flipped ancestor groups is rejected as unsupported and needs visual review or a supported authoring structure. Missing properties and malformed specs fail closed.

The audit does not prove scientific correctness, aesthetics, paper-size legibility, contrast, or absence of overlaps. Render and inspect the final slide and run the environment's overflow checks. Do not misreport a baseline-only pass as validation of the relationship graph.
