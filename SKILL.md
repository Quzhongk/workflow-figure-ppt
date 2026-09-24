---
name: workflow-figure-ppt
description: Create or revise a clear scientific workflow, pipeline, framework, or model-architecture figure as a single-slide editable PPTX from prose, a sketch, or a reference image. Use for explicit research workflow or scientific process diagram requests and follow-up revisions; do not use for ordinary multi-slide decks, decorative illustrations, or raster-only figures.
---

# Scientific Workflow Figure in PowerPoint

Make the scientific relationships understandable without presenter narration. Preserve the user's current directions over the default style below.

## Deliverable contract

- Deliver one slide per PPTX, without an added cover. Normally deliver one PPTX; when the user asks for alternatives, deliver one single-slide PPTX per alternative.
- Keep diagram text, symbols, containers, and connectors native and individually editable. Group logical symbols/modules without flattening them. Native DrawingML shapes satisfy the crisp editable-vector requirement; do not describe them as standalone SVG files.
- Do not insert rasterized text, stock artwork, external icons, generated images, or a monolithic SVG. Supplied images are references unless the user explicitly asks to embed them.
- Preserve content and scientific meaning. Do not invent mechanisms, causal edges, feedback paths, or performance claims for visual balance.
- Save revisions under new filenames unless overwrite is explicitly requested. Preserve prior deliverables.
- Use the environment's required presentation-authoring toolchain. Use the editable-diagram exception for semantic shapes, not decorative artwork.

## Work in semantic order

1. **Infer the architecture.** Identify entities, peer groups, containment, inputs/outputs, annotations, and directed or reciprocal relations. For a rotated sketch, first read it in the orientation the user specifies; do not infer order from the photo's page orientation. Separate facts supplied by the user from assumptions. Infer routine layout details; ask one focused question when an unresolved relation would change scientific meaning.
2. **Check scientific notation.** Transcribe mathematical labels and relations before drawing. Check symbols, subscripts, superscripts, operators, and, where relevant, vector/matrix dimensions and orientation. Re-check dependent notation after changing the visual arrangement. Read [figure-design-guide.md](references/figure-design-guide.md) for notation guidance when the figure contains formulas or a rotated sketch.
3. **Set the hierarchy.** Assign text roles and visual scope before positioning boxes. Source/infrastructure notes are not automatically process stages. Peers need equal visual weight, not necessarily a single row.
4. **Compose and route.** Fit the actual relationship graph to the canvas. Align one-to-one mappings on a common axis. Reserve bends for branches, merging, feedback, or obstacle avoidance. Triangular peer cooperation may use straight diagonal edges when the relationships justify them. For directional connectors, normally leave a small visible gap at the objects while keeping the intended target unambiguous.
5. **Apply typography.** Define shared font, size, and weight per semantic role; do not style equivalent labels independently. By default use Arial Black for the highest-level headings (including multiple Layer headings) and Arial for other text. Do not add an overall title merely to satisfy a template.
6. **Apply color and symbols.** Use color to explain grouping and hierarchy. Build subject-specific symbols from PPT primitives and keep them close to their labels.
7. **Render and review.** Verify semantics as well as geometry and editability. Automated checks cannot decide whether the scientific interpretation or visual design is good.

For a new composition, a structural revision, or ambiguous grouping, read [figure-design-guide.md](references/figure-design-guide.md). For palette selection, reference-style translation, or icon construction, read [visual-system.md](references/visual-system.md).

## User's default visual preference

These are overridable preferences, not universal scientific-figure rules:

- White underlying canvas; light colored layer containers; related, slightly deeper module fills within each layer. Different layers may use more distinct hue families. Similar semantic roles within a layer stay close in color.
- Compact, visually full composition with useful separation for grouping and routing. Avoid large accidental blank regions, but do not fill space with decoration.
- Flat, plain printed-diagram character: simple corners, coherent ink colors, clear lines. Avoid dashboard-like accents, gratuitous badges, gradients, shadows, or simulated dirt and deliberately crooked lines.
- Meaningful editable micro-diagrams, not generic icons chosen merely to fill a slot. Use native shapes to construct a suitable symbol when no appropriate one exists.
- Prefer 16:9 when no canvas is specified. Fit dimensions and type sizes to the reference, content, and target publication size; no fixed four-layer architecture or fixed palette is required.

## Revision discipline

- Translate feedback into the affected design variable. A color-only change must preserve approved content, geometry, typography, and edge topology.
- For palette comparisons, keep everything except color constant. Each alternative should differ meaningfully, not merely shuffle nearly identical tints.
- Interpret "white background" separately for canvas, layer containers, and modules. Do not silently turn every container white or desaturate the whole drawing.
- Preserve approved choices across revisions. Do not convert an example-specific triangle, ten-column grid, color sequence, or exact point size into a universal template.
- Provide the final PPTX. Include a rendered preview/comparison when requested or useful during an ongoing visual iteration. Do not deliver scratch builds.

## Build and validate

Use stable unique names for semantic shapes, labels, and connectors. Use endpoint binding or stable anchors when helpful, but do not force visible contact with an object merely to bind a connector; preserve the intended small gap unless exact contact carries meaning. Prefer shared style definitions and palette roles to scattered literal settings.

Before delivery:

1. Render at full size and inspect at the intended viewing scale. Check content coverage, hierarchy, icon meaning/proximity, density, text fit, contrast, arrow routes, endpoint gaps, and whether connectors cross objects or labels.
2. Check that peers have coherent visual weight; a genuine central contribution may be emphasized, but do not impose a single dominant node on a peer architecture.
3. Run the presentation workflow's overflow/package checks and `python scripts/audit_pptx.py <deck.pptx>`.
4. For figures with repeated styles, aligned mappings, or important reciprocal edges, also supply a task-specific `--spec figure-spec.json`. Read [validation.md](references/validation.md) for its schema. Derive assertions from approved semantics, not from whatever the output happens to contain.
5. Resolve errors and inspect warnings. Review the rendered final file; do not claim desktop PowerPoint verification unless it was actually performed.
