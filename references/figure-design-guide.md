# Architecture, hierarchy, and layout

## Build a semantic model before drawing

For each item, identify its role (layer, module, method, input/output, or annotation), its parent if any, and its peers. For each edge, identify source, target, direction, and meaning. A compact internal table is sufficient; do not make the user supply a formal specification.

| Relationship | Visual expression |
| --- | --- |
| Contains / belongs to | Nested container, not an arrow by default |
| Same-level components | Comparable sizes, label styles, and visual weight |
| Data or information flow | Directed connector |
| Reciprocal cooperation | Two-headed connector only when supported |
| Source, storage, or explanatory metadata | Close icon/text group or plain association line |
| Repeated one-to-one correspondence | Shared centerlines and consistent straight connectors |

A repository beside a dataset does not automatically establish a three-stage pipeline. Likewise, two arrows pointing to a peer can describe information transfer rather than a part-of hierarchy. If that difference matters and evidence is insufficient, explain the uncertainty and ask; do not invent feedback to make a symmetric triangle.

## Read sketches and notation before layout

For a rotated or skewed reference, follow the user's stated viewing direction before reading sequence, labels, and grouping. Make a small item-to-item mapping from the sketch to the intended slide so that repositioning does not silently change a relation.

For mathematical content, record the exact labels and expressions, including case, indices, superscripts, transpose marks, and operators. Check that visual representations agree with the algebra: a row or column of cells implies a vector orientation, and matrix multiplication must have compatible dimensions and the intended output shape. When a vector is redrawn in the other orientation, revisit its transpose notation and adjacent equation. Use a native equation object when exact mathematical typography matters and the authoring tool supports it; otherwise keep correctly formatted notation editable in PowerPoint.

## Choose geometry from relationships

- Sequential transformations: a row or column along the dominant reading direction.
- Layered systems: scope bands with related modules inside; unequal content can justify unequal band heights.
- Parallel modalities/routes: aligned lanes; align corresponding outputs before routing.
- Shared-state or cooperative systems: a hub, triangle, or compact network where warranted. Same-level nodes need not share a y-coordinate.
- Feedback and iteration: clear return paths outside the main flow.
- Overview plus detail: use only when both levels add necessary information.

Do not force a fixed number of levels, layers, lanes, or nodes. Highlight a central contribution only when the story has one; otherwise preserve balanced peer emphasis.

## Route arrows deliberately

- For one-to-one mappings, first align endpoints along the intended axis, then use a straight connector. In a vertical layout, share x-centers; in a horizontal layout, share y-centers.
- Branches may use a shared horizontal/vertical bus and orthogonal bends. Bends are not a defect when they reveal the branching structure.
- A reciprocal triangle can use three straight edges, including diagonal edges. Do not apply a global ban on diagonal lines.
- Do not introduce tiny accidental diagonals due to misaligned centers. Do not add decorative curves or unnecessary elbows to a direct connection.
- Keep edges off labels and symbols. For a connector that chiefly indicates direction, aim clearly at the intended object but normally stop a small visible distance before its outline; use a similarly small gap at the source where appropriate. Choose the gap at the final viewing scale so the relation stays obvious and the layout does not feel cramped. Exact contact is appropriate when a specific port, junction, or continuous path carries scientific meaning. Use routing anchors only as implementation objects, not extra scientific nodes.
- Arrowheads, line weight, and dash patterns must have consistent meanings. A plain line denotes association only when that interpretation is clear; explain non-obvious encodings.

## Typography by role

Create a role table before rendering: highest-level headings, component labels, method captions, and annotations. Within each role, share font family, point size, and weight. Use Arial Black for highest-level headings and Arial elsewhere by default; italic scientific terms can remain italic within an otherwise shared style.

For a dense one-slide figure, starting ranges are 20–26 pt for top-level headings, 14–18 pt for component labels, and 10–14 pt for captions. These are starting points, not quotas. Keep a reference's scale when appropriate. Simplify labels or enlarge boxes before shrinking type; inspect at likely publication size.

No overall title is required if the layer headings already orient the reader. Match equivalent headings even if one is positioned at the bottom/right.

## Density and proximity

- Size containers around their content and routing needs, rather than expanding a generic template's padding.
- Keep icon-label distance smaller than distance to unrelated content. Align multiline captions with their own module, not a distant grid edge.
- Make semantic symbols large enough to recognize, but subordinate to the scientific label.
- Repeated items should have comparable dimensions. Give more space to genuinely longer content when necessary, without suggesting a false higher rank.
- Eliminate accidental holes by revising placement, scale, or internal padding, not by adding meaningless symbols.
- Preserve deliberate whitespace for reading, separation, and edge routing. Fullness is not a target occupancy percentage.

## Use references critically

The [Top-Conf Figure Gallery](https://github.com/qwdwqfwq/topconf-paper-figure-gallery) is an optional source for pipeline/framework/architecture examples. Inspect relevant examples when using them; it is not a source of scientific relations for the user's figure. Record what is borrowed (grouping, routing, density, or color relationships), not copied artwork. Do not claim a style has publication validation merely because it resembles a gallery image.

## Review questions

- Does each visual level match the intended scientific level?
- Could containment, spatial position, or arrow direction imply an unintended hierarchy?
- Can annotations be distinguished from processing steps?
- Are source/target relationships clear without narration?
- Do close labels and symbols form the correct groups?
- Is density useful, with no missing content or decorative filler?
- Does a local revision preserve the previously approved dimensions of the design?
- Are notation and the drawn orientation/dimensions consistent, including after a local revision?
- Do directional connectors point to the intended objects with a clean, small endpoint gap and avoid crossing their interiors or labels?
