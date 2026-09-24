# Color roles and native scientific symbols

## Defaults, not immutable templates

The user's preferred direction is a white canvas with softly colored layer fields and closely related module fills. Flat printed-diagram character is preferred over glossy corporate presentation styling. Current task instructions or a supplied reference may override this.

Color hierarchy should follow semantic grouping before route identity. If two routes belong to one layer, neighboring hues can distinguish them without making them look like unrelated layers. Conversely, distinct layers may use clearly different hue families.

Define colors by role:

- `canvas`: underlying page, white by default.
- `layerFill`: light scope/background field.
- `moduleFill`: related, slightly deeper fill for contained components.
- `subgroupFill`: optional nearby hue for a real subgroup.
- `stroke` / `edge`: readable same-family ink, not a second unrelated palette.
- `text`: dark enough to read independently of the background tint.

Increasing saturation alone does not fix a figure that feels bland. Check whether grouping, color distribution, and the difference between fields and modules are clear. Conversely, making the canvas white does not require whitening every field.

## Approved light-layer example

This is a reusable palette example, not a required four-layer structure or fixed assignment to scientific concepts.

| Family | Layer field | Module | Optional subgroup/header | Stroke |
| --- | --- | --- | --- | --- |
| Sky blue | `#EBF4FD` | `#D4E7F7` | `#C5DDF2` | `#6988A6` |
| Leaf green | `#ECF6EE` | `#D9EBD9` | `#CBE0D0` | `#597966` |
| Apricot/gold | `#FFF7E7` | `#F6E7C3` | `#F8E3CA` / `#EBD6A6` | `#8A7045` |
| Warm rose | `#FAEFEC` | `#F2DDD7` | `#EACBC4` | `#AE847E` |

Canvas `#FFFFFF`; body ink `#293B48`; highest-level heading ink `#354F69`. Keep peer headings typographically consistent even when fields differ in color. Use labels and position as well as hue; never rely on color alone to distinguish meaning.

For more assertive alternatives, useful families include indigo/mustard, petrol/apricot, ink-blue/olive, and pine/terracotta. Map the families to semantic roles first. Do not mechanically color every other node differently. When comparing alternatives, freeze topology, spacing, fonts, and icons. Render actual figures, not just swatches.

When the user asks for a historical/artistic reference, inspect the source and explain which relationships were adapted. Do not claim exact pigment extraction or scientific suitability without evidence. Notebook references inform plain ink blocks, limited color families, and practical typography; they do not require noise, scratches, or crooked geometry.

## Build symbols from editable primitives

Choose a symbol by the concept it clarifies. Keep primitives and text native, then group the symbol for convenient movement. In the absence of a suitable symbol, construct a small scientific schematic rather than forcing a generic icon.

| Concept | Native-shape recipe | Semantic caution |
| --- | --- | --- |
| Cell/state | Membrane ellipse, nucleus, a few internal marks | Do not imply a particular cell type without evidence |
| Multimodal data | Distinct schematic modalities next to a matrix | Show only modalities supported by the description |
| Integration/completion | Small input matrices, convergence arrows, completed matrix | Do not invent an extra processing stage |
| Representation | Biological entity with context marks and an abstract vector/matrix | Generic grid alone often fails to convey biological context |
| Biological relationships | Labeled/typed entity nodes and connecting edges | Avoid causal arrowheads if only association is known |
| Experiment | Plate wells, pipette, microscope, or monitor plus biological sample | Distinguish wet-lab from in-silico work |
| Feature comparison | Two compact matrices or profiles and a marked difference | Schematic values must not appear to be measured results |
| Retrieval | Documents/database and a magnifying lens | Magnifier belongs to search, not every analytical method |
| Hypothesis | Small proposed relationship or biological question | A lightbulb alone can be too generic |

Use consistent stroke weight, visual size, and level of detail. Keep icons adjacent to labels, with smaller within-group gaps than between groups. Native-shape assembly is a means of clarity, not a reason to add more ornament. Do not reuse an ambiguous symbol across unrelated concepts.

## Style failure checks

- Tiny decorative top borders or accent tabs with no semantic role.
- A dark header band disconnected from an otherwise washed-out figure.
- Identical pale colors for all semantic levels, making containers and modules indistinguishable.
- Unrelated saturated colors within a peer group.
- Excessive empty padding, or arbitrary icons added to fill it.
- Simulated texture that competes with labels or compromises editability.
