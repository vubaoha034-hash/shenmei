# VPD TYPOGRAPHY CREATION METHODS — RESEARCH SANDBOX

Date: 2026-09-16
Status: RESEARCH_ONLY_NOT_RULE
Project: visual-aesthetic-vpd

## 0. Admission boundary

This document is research evidence only. It does **not** modify the VPD typography rules, Style Capsule, prompt compiler, quality gate, or production workflow.

User authority for this sandbox: store the researched methods first, test them, and **do not admit a method into project rules unless the test succeeds and the user explicitly accepts the result**.

Promotion policy:

- Research source found -> `CANDIDATE_METHOD_ONLY`.
- Controlled sandbox test executed -> still not a rule.
- Technical correctness alone -> never enough.
- Human visual acceptance on actual pixels -> required.
- Failure / no visible benefit / lower design quality -> archive as negative evidence; **must not enter rules**.
- Passing one local test may justify a second validation, but does not prove universal applicability.

## 1. Method map found in professional practice

### M01 — Mature typeface -> surgical wordmark customization
Start from a structurally strong typeface and change only high-leverage features: width, spacing, terminals, selected counters, joins, and a few identity-bearing strokes. Do not redesign every stroke merely to make it “custom”.

Use when: the brand needs a clean contemporary wordmark and the base skeleton is already strong.

Risk: if the base font has the wrong DNA, local edits create a decorated font rather than an authored wordmark.

Evidence examples: Figma/brand-type development and professional custom type work emphasize iterative proportion/spacing changes rather than gratuitous deformation.

### M02 — Hand-drawn / generative lettering mother -> faithful vectorization -> local refinement
Treat a visually strong raster/sketch as the visual authority. Vectorization should preserve the character of the mother rather than reinterpret the design. Refine individual letters/strokes after conversion.

Use when: the mother image already has stronger design character than a font-derived construction.

Current project relevance: `茶作 D` is closest to this route.

### M03 — Centerline skeleton -> variable-width stroke -> outline
Build a stroke as a directional center path first; use variable-width profiles for thickness, taper, start/end pressure, then outline only after the stroke rhythm works. This separates “stroke trajectory” from “edge noise”.

Use when: expressive direction, taper, and controlled organic movement matter.

Current project relevance: high-value candidate for the major strokes of `茶`, especially where prior closed-contour tracing created hundreds of noisy points.

### M04 — Geometric / modular construction
Construct glyph identity from circles, rectangles, arcs, planar cuts, and controlled joins; use shape-building/boolean operations to create a disciplined system.

Use when: object/process semantics are naturally structural or modular.

Current project relevance: potentially better suited to `豆坊` than to `茶作` because tofu/press/block semantics can support geometric mass and compression.

### M05 — Typeface outline -> selective structural rewrite
Choose a base with suitable skeleton, convert to outlines, then edit only the parts needed for proprietary identity. Preserve correct proportions/character recognition instead of rebuilding the entire glyph from scratch.

Use when: correctness and legibility need a strong starting scaffold.

### M06 — CJK component / stroke-system construction
Treat a Chinese glyph as a hierarchy: character -> component -> main stroke -> secondary stroke -> counter/negative space. Control visual center of gravity, stroke relationships, component scale and internal spacing as a system.

Use when: Chinese characters are being custom-built rather than simply typeset.

Project lesson: converting `茶作` into one dense compound EVENODD outline is production-hostile; component/stroke-level structure should be preserved where possible.

### M07 — Semantic DNA embedded in strokes, not pasted as iconography
Translate brand/process/material semantics into the shape behavior of strokes: compression, opening, rhythm, terminal logic, counter topology, etc. A leaf, bean, press, tray, or tool should not be added merely as decoration if it does not participate in the glyph system.

Project lesson: the rejected three-leaf overlay and rejected internal green patch are direct negative evidence for post-hoc decoration.

### M08 — Historical / material / vernacular lettering as source DNA
Use real signs, packaging, carvings, printing, handwriting, workshop marks, or archival lettering to derive a visual language; redraw rather than copy assets mechanically.

Use when: brand character depends on place, craft, period, or material culture.

### M09 — Wordmark and supporting type are separate systems
A display wordmark should not be forced to perform like body copy. Conversely, supporting text should not inherit every distortion of the logo. Build the wordmark first; create a compatible supporting hierarchy later.

Project relevance: T2 stays blocked until the title itself is visually accepted.

### M10 — Surface texture as a separate layer after the skeleton passes
Real grain, ink, brush, paper, print or material texture should be treated as a separate layer/asset. Texture must not rescue a weak skeleton. Black/white structure must work before surface treatment is admitted.

Project relevance: the human-rejected Figma vector-only “high-fidelity” surface test showed that gradients/outlines/shadows do not create premium craft when the underlying construction route is weak.

## 2. Curve and glyph construction principles worth testing

These are candidate principles, **not rules yet**:

- Fewer meaningful Bézier nodes are preferable to dense trace topology when the same silhouette can be preserved.
- Place nodes at meaningful extrema and structural corners; remove intermediate points that do not change the shape.
- Handle continuity and balanced curvature matter more than “smoothing” a noisy trace.
- Curved forms often need optical overshoot relative to straight boundaries.
- Spacing and negative space are part of the glyph design, not a final cosmetic adjustment.
- For variable-width construction, build the stroke trajectory first and thickness second.
- Texture should be independently controllable and clipped/masked to an already-approved form.

## 3. Tool facts confirmed by current documentation

### Figma
- Vector edit mode includes Variable width, Shape builder, Cut, Bend, Eraser, Lasso and Paint.
- Figma Vectorize can turn raster drawings/hand-drawn lettering into editable vectors and is explicitly presented for modifiable logo/lettering workflows.
- Figma Vectorize is also presented for captured grain/noise/brush textures as reusable overlays.
- Plugin API update 123 (2026-01-26) exposes `variableWidthStrokeProperties`, including preset and custom width profiles.
- Current ChatGPT Figma connector does not expose a dedicated one-click Vectorize action; Plugin API vector/stroke manipulation is available, so sandbox tests must distinguish editor-only features from connector-callable features.

### Illustrator
- Width Tool supports variable-width strokes and pointed/tapered ends; width profiles can be saved and reused.
- Outlining a suitable base typeface and editing its vector shapes is a standard custom-lettering route.

### Glyphs / FontLab
- Professional contour guidance emphasizes extrema, balanced handles and removal of superfluous points.
- FontLab’s current construction guidance explicitly treats point-clean contours and overshoot as fundamental rather than cosmetic cleanup.

## 4. External source index

Primary / official sources used for this research snapshot:

1. Figma — “For the love of craft: Vectorize images in Figma” (2026-02-04): https://www.figma.com/blog/introducing-vectorize/
2. Figma Help — “Edit vector layers”: https://help.figma.com/hc/en-us/articles/360039957634-Edit-vector-layers
3. Figma Developer Docs — Version 1, Update 123 (variable width strokes / Draw API): https://developers.figma.com/docs/plugins/updates/2026/01/26/version-1-update-123/
4. Figma Developer Docs — VariableWidthStrokeProperties: https://developers.figma.com/docs/plugins/api/VariableWidthStrokeProperties/
5. Adobe Illustrator — Width Tool: https://helpx.adobe.com/illustrator/using/tool-techniques/width-tool.html
6. Adobe Learn — Hand lettering / outlining and editing type: https://www.adobe.com/learn/illustrator/web/use-sketches-to-make-hand-lettering
7. Glyphs — Drawing good paths: https://glyphsapp.com/learn/drawing-good-paths/
8. FontLab — Glyph construction from scratch (2026): https://blog.fontlab.com/2026/02/10/fontlab-tv-glyph-construction/
9. TypeTogether — Geely custom typeface / “a font is not a logo”: https://www.type-together.com/2021-geely-custom-font
10. Pentagram — Cooper Hewitt identity/custom typeface: https://www.pentagram.com/work/cooper-hewitt-smithsonian-design-museum-1

Additional case-study families to consult only if a later test needs them: Monotype custom type/brand systems; Adobe CJK type development; Pentagram wordmark/type projects.

## 5. Negative evidence already earned in this project

Do not erase these failures when testing new methods:

- Dense auto-traced closed contours + global/local smoothing did not produce acceptable edge quality.
- Automatic point reduction damaged glyph structure.
- Post-hoc green leaf overlays read as unrelated dirty spots.
- Coloring a small internal segment green did not create semantic integration.
- Figma-only gradients/outlines/shadows improved visibility slightly but remained visibly low/flat compared with the mother concept.
- Repeated effect/rule stacking is now considered a failed taste route, not a reason to add more rules.

## 6. Rule-admission firewall

Nothing in this document is allowed to become `VPD_PROJECT_ROADMAP`, Style Capsule, Typography rules, Prompt Compiler, Quality Gate, or any production default merely because it appears in professional documentation.

A method may be promoted only after:

1. a bounded test on actual project material;
2. preserved baseline comparison;
3. no hidden polish/retry advantage;
4. actual-pixel human review;
5. explicit user acceptance that the method produces a visible improvement worth keeping;
6. a separate promotion step that names exactly what is being admitted and where.

Until then: **RESEARCH ONLY.**
