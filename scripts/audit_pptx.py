#!/usr/bin/env python3
"""Audit a scientific workflow PPTX for the skill's structural constraints.

This is a package-level check. It complements, rather than replaces, rendering
and visual inspection.
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from semantic_checks import check_semantics, validate_spec


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}

ALLOWED_FONTS = {"arial", "arial black"}


def parse_xml(archive: zipfile.ZipFile, name: str) -> ET.Element:
    try:
        return ET.fromstring(archive.read(name))
    except KeyError as exc:
        raise ValueError(f"Missing required PPTX part: {name}") from exc
    except ET.ParseError as exc:
        raise ValueError(f"Invalid XML in {name}: {exc}") from exc


def audit(path: Path, spec: dict | None = None) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    report: dict[str, object] = {
        "file": str(path.resolve()),
        "errors": errors,
        "warnings": warnings,
        "ok": False,
    }

    if spec is not None:
        try:
            validate_spec(spec)
        except ValueError as exc:
            errors.append(str(exc))
            return report
    allowed_fonts = {f.casefold() for f in (spec or {}).get('allowed_fonts', ALLOWED_FONTS)}

    if path.suffix.lower() != ".pptx":
        errors.append("Output must use the .pptx extension.")
        return report
    if not path.is_file():
        errors.append("PPTX file does not exist.")
        return report
    if not zipfile.is_zipfile(path):
        errors.append("File is not a valid zipped PPTX package.")
        return report

    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            slides = sorted(
                name
                for name in names
                if name.startswith("ppt/slides/slide")
                and name.endswith(".xml")
                and "/_rels/" not in name
            )
            report["slide_count"] = len(slides)
            if len(slides) != 1:
                errors.append(f"Expected exactly one slide; found {len(slides)}.")

            media = sorted(name for name in names if name.startswith("ppt/media/"))
            embeddings = sorted(
                name
                for name in names
                if name.startswith("ppt/embeddings/")
                or name.startswith("ppt/oleObjects/")
            )
            report["media_parts"] = media
            report["embedded_parts"] = embeddings
            if media:
                errors.append(
                    "Found embedded media. This skill requires native PowerPoint "
                    "shapes and text, with no raster images or monolithic SVG artwork."
                )
            if embeddings:
                errors.append("Found embedded or OLE objects; use native editable shapes instead.")

            shape_count = 0
            connector_count = 0
            group_count = 0
            picture_count = 0
            graphic_frame_count = 0
            text_items = 0
            explicit_fonts: set[str] = set()
            title_fonts: set[str] = set()
            title_shapes = 0

            for slide_name in slides:
                root = parse_xml(archive, slide_name)
                if spec is not None and len(slides) == 1:
                    errors.extend(check_semantics(root, spec))
                shape_count += len(root.findall(".//p:sp", NS))
                connector_count += len(root.findall(".//p:cxnSp", NS))
                group_count += len(root.findall(".//p:grpSp", NS))
                picture_count += len(root.findall(".//p:pic", NS))
                graphic_frame_count += len(root.findall(".//p:graphicFrame", NS))
                text_items += len(root.findall(".//a:t", NS))

                for latin in root.findall(".//a:latin", NS):
                    typeface = (latin.get("typeface") or "").strip()
                    if typeface and not typeface.startswith("+"):
                        explicit_fonts.add(typeface)

                for shape in root.findall(".//p:sp", NS):
                    placeholders = shape.findall(".//p:nvPr/p:ph", NS)
                    is_title = any(
                        ph.get("type") in {"title", "ctrTitle"}
                        for ph in placeholders
                    )
                    if not is_title:
                        c_nv_pr = shape.find("./p:nvSpPr/p:cNvPr", NS)
                        shape_name = (c_nv_pr.get("name") if c_nv_pr is not None else "") or ""
                        is_title = shape_name.lower().startswith("heading:")
                    if is_title:
                        title_shapes += 1
                        for latin in shape.findall(".//a:latin", NS):
                            typeface = (latin.get("typeface") or "").strip()
                            if typeface and not typeface.startswith("+"):
                                title_fonts.add(typeface)

            report.update(
                {
                    "shape_count": shape_count,
                    "connector_count": connector_count,
                    "group_count": group_count,
                    "picture_count": picture_count,
                    "graphic_frame_count": graphic_frame_count,
                    "text_item_count": text_items,
                    "explicit_fonts": sorted(explicit_fonts),
                    "title_fonts": sorted(title_fonts),
                }
            )

            if picture_count:
                errors.append(f"Found {picture_count} picture object(s); use native shapes instead.")
            if graphic_frame_count:
                warnings.append(
                    f"Found {graphic_frame_count} graphic frame object(s). Confirm each is editable "
                    "and necessary for the scientific workflow."
                )
            if shape_count == 0:
                errors.append("No native PowerPoint shapes were found.")
            if text_items == 0:
                warnings.append("No editable text was found on the slide.")
            if connector_count == 0:
                warnings.append("No native connectors were found; verify that process relationships are editable.")

            disallowed = sorted(
                font for font in explicit_fonts if font.casefold() not in allowed_fonts
            )
            if disallowed:
                errors.append("Found fonts outside the declared font policy: " + ", ".join(disallowed))
            if not explicit_fonts:
                warnings.append(
                    "No explicit slide fonts were detected. Verify that the effective fonts are "
                    "consistent by semantic role, with Arial Black for top-level headings by default."
                )
            # A diagram need not have a global title. Explicit role assertions
            # check every heading, rather than accepting one Arial Black run
            # somewhere in the deck or guessing from a substring like 'subtitle'.
            if spec is None:
                report['semantic_checks'] = 'not requested; visually review hierarchy and relationships'
            else:
                report['semantic_checks'] = 'declared assertions checked'

    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        errors.append(str(exc))

    report["ok"] = not errors
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit a one-slide editable scientific workflow PPTX."
    )
    parser.add_argument("pptx", type=Path, help="Path to the PPTX file")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--spec", type=Path, help="Optional JSON role/geometry/connection assertions")
    args = parser.parse_args()

    try:
        spec = json.loads(args.spec.read_text(encoding='utf-8-sig')) if args.spec else None
        result = audit(args.pptx, spec)
    except (OSError, ValueError) as exc:
        result = {'ok': False, 'errors': [str(exc)], 'warnings': []}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"PPTX audit: {'PASS' if result['ok'] else 'FAIL'}")
        for key in (
            "slide_count",
            "shape_count",
            "connector_count",
            "group_count",
            "picture_count",
            "graphic_frame_count",
            "text_item_count",
        ):
            if key in result:
                print(f"  {key}: {result[key]}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
        for error in result["errors"]:
            print(f"ERROR: {error}")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
