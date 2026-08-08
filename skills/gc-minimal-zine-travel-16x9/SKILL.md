---
name: gc-minimal-zine-travel-16x9
description: >
  Convert a travel photo or video frame into a minimal zine-style editorial image by following
  the supplied visual reference first: aspect ratio, orientation, composition density, paper
  treatment, typography behavior, color logic, and image-to-negative-space relationship.
  Do not force 16:9. Use 16:9 only when the user explicitly requests it or when preserving an
  already-16:9 source/reference. Supports torn-photo sticker, color-block collage, contour map,
  scenic print, architectural deconstruction, and symbolic silhouette treatments.
---

# GC Minimal Zine Travel — Reference-First

This is a repository-specific derivative of `gc-minimal-zine-poster-v0-1` for travel photos and video frames.

The governing principle is **reference first, not template first**.

The goal is not to force every source into one horizontal poster. The goal is to study the supplied reference image, preserve the important scene evidence from the user's source, and rebuild the image using the same visual grammar: paper, scale, negative space, collage behavior, print texture, typography, color rhythm, and overall proportion.

## Trigger

Use this Skill when the user provides or references:

- a travel video frame;
- a landscape or destination photo;
- a person-in-landscape travel image;
- architecture, desert, lake, coast, mountain, plateau, grassland, canyon, street, village or similar destination imagery;
- one or more reference images showing the desired zine treatment;
- a request for the `gc-minimal-zine-poster` look adapted to a travel image;
- a request to transform a batch of travel frames into a coherent editorial sequence;
- an explicit request for 16:9, 3:2, 4:5, 9:16, square, or another ratio.

Do not use this Skill for restaurant posters, ten-page restaurant branding, commercial product ads, UI layouts, or unrelated generic poster tasks.

## Aspect-ratio policy — reference first

**16:9 is not a default and is not a hard rule.**

Resolve canvas ratio in this priority order:

1. **Explicit user instruction wins.**
   - If the user says `16:9`, `9:16`, `3:2`, `4:5`, square, or gives exact pixel dimensions, use that target.
2. **Otherwise follow the supplied reference artwork.**
   - Match its orientation and approximate aspect ratio.
   - Match the designed image/poster area, not the phone screenshot shell.
3. **If the reference is a social-media screenshot or before/after comparison, isolate the actual reference artwork visually.**
   - Ignore app chrome, black bars, account UI, playback controls and surrounding screenshot space when determining ratio.
4. **If several references use different ratios and the user has not singled one out, preserve the source photo/video frame ratio rather than inventing a new one.**
5. **If no usable reference ratio exists, preserve the source image/frame ratio.**

Rules:

- Never force a source into 16:9 merely because this Skill was originally created from 16:9 travel examples.
- Never force the upstream 3:5 ratio either.
- Do not crop or stretch solely to satisfy a template ratio.
- A source or reference that is already 16:9 may naturally remain 16:9; that is preservation, not a forced conversion.
- Only convert to 16:9 when the user explicitly asks for 16:9 or provides exact dimensions equivalent to it.

## Reference decomposition

Before generating, inspect the reference and resolve these fields:

```text
reference_ratio:
reference_orientation:
negative_space_level:
main_visual_scale:
main_visual_position:
paper_family:
image_treatment:
typography_scale:
typography_position:
accent_color_logic:
texture_family:
composition_family:
```

Do not copy a reference mechanically. Reuse its **visual mechanism**, not its exact artwork.

### What should be learned from the reference

- ratio and orientation;
- proportion of image to empty paper;
- whether the image is a small clipping, broad scenic strip, silhouette, map field, or architectural fragment;
- where the visual cluster sits;
- how much paper remains empty;
- whether edges are torn, brushed, cut, photocopied, or geometrically masked;
- how typography uses the empty area;
- whether color comes from the source image, a tape strip, a flat field, a garment, water, sky or another meaningful element;
- print language: xerox, halftone, risograph, letterpress, dry brush, faded offset, scan noise;
- degree of realism versus abstraction.

### What must not be copied

- creator name or account handle;
- watermark;
- exact decorative microtext;
- fake archive numbers;
- coordinates not supplied by the user;
- exact proprietary layout if it would amount to direct duplication;
- social-media UI.

## Source fidelity

The transformed result must still be recognizably derived from the user's source frame.

Preserve at least three of the following when they are visually important:

- terrain silhouette;
- shoreline or river/lake geometry;
- mountain ridge direction;
- architectural massing;
- the person's pose, scale or location in the frame;
- horizon height;
- dominant movement direction;
- one signature object, tree, wall, road, dune, rock or mirror;
- the source frame's most important color cue.

Do not replace the place with an unrelated invented scene just to satisfy the style.

## Core visual system

Every result should combine these stable characteristics unless the reference clearly indicates otherwise:

- tactile aged, archival, matte or fibrous paper;
- flat scanned-paper appearance;
- xerox, halftone, risograph, letterpress, dry-brush or weathered-print texture;
- deliberate negative space;
- one dominant visual idea rather than a dense scrapbook;
- restrained editorial typography;
- one clearly visible chromatic anchor when the reference uses one;
- quiet field-note, travel-archive, independent-zine mood;
- no glossy advertising finish.

## Negative-space policy

Negative space must follow the reference, not a fixed percentage.

Use these only as fallback guides when the reference is ambiguous:

- sticker / specimen modes: roughly **65%–85%** empty paper;
- collage / contour / architecture modes: roughly **45%–70%** empty paper;
- scenic-print mode: roughly **35%–60%** empty paper.

For portrait or square references, reinterpret these proportions spatially rather than converting them into a horizontal layout.

## Location typography rule

When a place is known, include the location in English in an available quiet area **if the reference composition supports this behavior**.

Preferred structure:

```text
PLACE NAME
REGION / PROVINCE, COUNTRY
```

Possible placements:

- upper-left;
- upper-right;
- far lower-left;
- far lower-right;
- narrow vertical edge text;
- another quiet zone that mirrors the reference hierarchy.

Rules:

- use small serif, typewriter or monospaced typography unless the reference clearly uses another restrained editorial family;
- do not turn the location into a commercial headline;
- location text should support the image, not dominate it;
- if the user gives Chinese place names, translate or romanize them carefully;
- if the exact location is unknown, do not invent one;
- do not invent coordinates, dates, weather, archive numbers, awards, phone numbers, addresses or other fake precision;
- coordinates may appear only if supplied or reliably available from the user's source information.

Optional micro-labels may include short neutral terms such as `FIELD NOTES`, `ARCHIVE`, `RIDGE STUDY`, `DUSK OBSERVATION`, `EROSION NOTES`, or `LAKE CONTOUR`, but use at most one or two and only when the reference uses comparable editorial notation.

## Variation engine

For every new frame, select one primary **visual family** that is compatible with both source and reference.

For a sequence, do not repeat the same family on consecutive frames unless the reference sequence itself is intentionally repetitive.

### Family A — Torn Photo Sticker

Use when the reference shows a small preserved memory fragment or the source has a strong view that survives reduction.

- shrink the source into a torn or irregular photo clipping;
- scale and placement should follow the reference;
- allow one piece of tape, color paper, stamp-like block or rough registration mark if reference-compatible;
- preserve source colors inside the clipping more than in the surrounding paper.

### Family B — Color-Block Collage

Use when the source frame contains a clear color relationship such as blue water, orange sand, red clothing, green grass or a saturated sky.

- reduce the scene to 2–4 large flat printed shapes;
- use one source-derived high-chroma hue as the main anchor;
- allow one geometric paper block, irregular sticker or printed panel;
- keep secondary colors muted or paper-toned;
- do not become a bright commercial collage.

### Family C — Scenic Print

Use when the scene itself is the identity: mountain ridge, dune line, canyon, coast, plateau, lake or sunset silhouette.

- preserve the source's broad landscape geometry;
- translate it into halftone, risograph, photocopy, dry-brush or faded field-print language;
- place and scale the scenic band according to the reference;
- preserve a small human figure if it carries scale or story.

### Family D — Contour / Field Map

Use when water, roads, terrain or topographic boundaries are visually distinctive.

- convert a dominant shape into simplified contour lines or a flat map-like field;
- preserve one source-derived shape as the primary evidence of place;
- use one saturated fill such as lake blue, rust orange, field green or tomato red;
- combine with sparse archival labels;
- avoid fake technical-map complexity.

### Family E — Architectural Deconstruction

Use for brutalist buildings, walls, mirrors, towers, gates, stairs, monuments or strong structural scenes.

- isolate 1–3 architectural masses;
- turn one plane, mirror, window or wall into the image anchor;
- abstract surrounding sand, sky, road or shadow into printed curves or flat bands;
- retain the source's dominant vertical/horizontal rhythm;
- do not turn it into 3D concept art.

### Family F — Symbolic Silhouette / Ink Ridge

Use when the original composition is simple and iconic.

- reduce the scene to one ridge, dune, rock, tree, person or shoreline silhouette;
- combine a rough ink, charcoal, brush or torn-paper edge with one controlled color field;
- allow extreme simplification while preserving the source pose or geography;
- use large negative space when reference-compatible.

## Choosing the family

Use this priority:

1. identify the reference's dominant visual mechanism;
2. identify what makes the source frame unique;
3. exclude families that would destroy source evidence or violate the reference;
4. among the remaining valid families, rotate away from the previous 1–2 outputs when working in a batch;
5. choose a family that produces a materially different composition, not only a different object position.

The word “random” means controlled variation among compatible families, not arbitrary styling.

## Color logic

Prefer a color anchor derived from the source frame when that matches the reference logic.

Examples:

- blue lake → cobalt / ultramarine / mineral blue;
- red jacket → tomato red / vermilion;
- orange desert or earth → ochre / burnt orange;
- green valley → field green / moss green;
- cold sky → cyan / dusty teal.

Rules:

- use one main chromatic family per image unless the reference clearly uses more;
- preserve the anchor strongly enough to survive thumbnail viewing;
- let paper, grayscale photo fragments and microtext remain subdued;
- a tiny secondary hue is permitted only when it directly comes from the source and improves scene recognition;
- do not automatically force blue into every image;
- do not wash the accent into pastel unless the reference or user requests it.

## Typography system

Typography should be derived from the reference hierarchy.

Preferred fallback families:

- small serif;
- typewriter;
- monospaced archive text;
- lightly distressed letterpress text.

Default hierarchy when the reference is ambiguous:

1. English location label;
2. optional field-note phrase;
3. optional tiny date or factual metadata only when supplied.

Avoid:

- oversized promotional headlines unless the reference explicitly uses them;
- dense explanatory paragraphs;
- fake editorial copy;
- meaningless English used as decoration;
- too many numbers;
- large Chinese text unless requested or clearly present in the reference style.

If a source screenshot contains social-media overlay text, player controls, account names, likes, comments or UI elements, treat them as non-source content and exclude them from the generated zine artwork.

## Prompt compiler

Write the final image-generation prompt as four compact blocks.

### Block 1 — Resolved frame and reference grammar

State:

- resolved aspect ratio and orientation;
- why that ratio was selected: explicit user request / reference artwork / preserved source ratio;
- paper tone and flat scanned texture;
- reference-derived negative-space level;
- main visual scale and placement.

### Block 2 — Source evidence and transformation

State:

- the scene elements that must remain recognizable;
- selected visual family;
- how those elements are simplified, clipped, printed, mapped or abstracted;
- which reference mechanisms are being followed without literal copying.

### Block 3 — Typography and color

State:

- English place text and placement when known and appropriate;
- optional single field-note phrase;
- main source-derived chromatic hue;
- its physical form: ink block, tape, silhouette, water field, printed panel, clothing accent, etc.;
- print defects and micro-registration behavior.

### Block 4 — Mood and hard avoids

State:

- quiet archival travel-zine mood;
- matte, scanned, non-glossy finish;
- hard avoids: commercial ad, cinematic grading, 3D, neon, glossy poster, UI screenshot, black bars introduced by formatting, dense scrapbook, fake technical data, unrelated invented scenery, forced 16:9 when not requested.

## Sequence mode

When transforming multiple frames from one trip or one video:

- keep a consistent paper family and typographic family when the references form one system;
- preserve a coherent print texture across the sequence;
- keep the resolved aspect-ratio policy consistent with the references or explicit output requirement;
- rotate layout families and accent colors according to each source frame;
- do not use the same sticker placement repeatedly unless the reference sequence does;
- do not place the location label in the exact same corner every time unless that is a defining reference rule;
- keep location naming format consistent;
- prefer scene-to-scene continuity over template repetition.

## Negative constraints

Always reject or regenerate if the output becomes:

- a forced 16:9 conversion without an explicit 16:9 request or a 16:9 source/reference being preserved;
- a forced 3:5 conversion simply because the upstream Skill used 3:5;
- a layout whose ratio/orientation clearly disagrees with the supplied reference;
- full-bleed glossy travel photography when the reference is paper-zine based;
- cinematic movie-still grading with depth-of-field drama;
- tourism advertising;
- a generic poster unrelated to the source frame;
- dense scrapbook with many stickers when the reference is restrained;
- neon, cyberpunk, kawaii, cartoon or 3D unless explicitly requested;
- UI screenshot or phone frame;
- fake map with invented data;
- unreadable gibberish dominating the page;
- overdecorated with many colors;
- a direct copy of the original photo with only a paper filter.

## Workflow

1. Inspect the reference image(s).
2. Resolve the target aspect ratio using the priority policy.
3. Inspect the source image or video frame.
4. Identify the source's non-negotiable evidence of place.
5. Resolve known location text; do not fabricate it.
6. Select one visual family compatible with reference and source.
7. Select one source-derived accent family when appropriate.
8. Compile the four-block prompt.
9. Generate the image at the resolved ratio — **not automatically at 16:9**.
10. Inspect the output at thumbnail scale and normal scale.
11. Regenerate once if aspect ratio, reference fidelity, source fidelity, location text, negative space or color anchor clearly fails.
12. Return the image, final prompt, selected family, resolved ratio, location label and one-sentence interpretation note.

## Quality gate

Before marking the result complete, verify:

```text
[ ] resolved ratio follows explicit user instruction when one exists
[ ] otherwise resolved ratio follows the reference artwork
[ ] if no usable reference ratio exists, source ratio is preserved
[ ] 16:9 was not forced by default
[ ] screenshot chrome / app UI was excluded from ratio analysis
[ ] source scene is still recognizably the same place/moment
[ ] at least three important source features were preserved when available
[ ] one visual family was selected and applied decisively
[ ] reference visual grammar is recognizable without literal copying
[ ] aged paper / archival print materiality is visible when reference-compatible
[ ] negative space follows the reference or fallback family logic
[ ] one main source-derived chromatic family is visible when appropriate
[ ] location appears in English when known and compositionally appropriate
[ ] no fake coordinates or invented factual metadata
[ ] typography is sparse and editorial unless the reference clearly differs
[ ] result is not a commercial travel ad
[ ] result is not merely the original photo plus a texture filter
[ ] sequence mode avoids accidental template repetition
```

If any critical item fails, the result is `DRAFT`, not complete.

## Output format

```markdown
**生成图**
[rendered image at resolved aspect ratio]

**最终 Prompt**
```text
[final image-generation prompt]
```

**执行记录**
- Ratio: [resolved ratio + source of decision]
- Family: [A–F + name]
- Location: [English location or UNKNOWN]
- Accent: [source-derived chromatic family]
- Source evidence preserved: [short list]
- Reference mechanisms preserved: [short list]
- Status: READY | DRAFT
```
