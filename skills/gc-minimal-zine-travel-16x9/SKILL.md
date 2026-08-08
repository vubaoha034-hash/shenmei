---
name: gc-minimal-zine-travel-16x9
description: >
  Convert a travel photo or video frame into a 16:9 minimal zine-style editorial image
  with aged paper, large negative space, restrained archival typography, one strong
  source-derived color anchor, and rotating treatments such as torn-photo sticker,
  color-block collage, contour map, scenic print, architectural deconstruction, or
  symbolic silhouette. Use for travel-video frame redesigns, location diaries, and
  horizontal editorial inserts. Preserve the source scene while changing its visual grammar.
---

# GC Minimal Zine Travel 16:9

This is a repository-specific derivative of `gc-minimal-zine-poster-v0-1`, adapted for horizontal travel-video frames.

The goal is not to make a generic poster. The goal is to take a real travel frame and turn it into a quiet, tactile, editorial zine image that still clearly belongs to that exact place and moment.

## Trigger

Use this Skill when the user provides or references:

- a travel video frame;
- a landscape or destination photo;
- a person-in-landscape travel image;
- architecture, desert, lake, coast, mountain, plateau, grassland, canyon, street, village or similar destination imagery;
- a request for the `gc-minimal-zine-poster` look in horizontal `16:9` form;
- a request to transform a batch of travel frames into a coherent editorial sequence.

Do not use this Skill for restaurant posters, ten-page restaurant branding, commercial product ads, UI layouts, or unrelated vertical zine posters.

## Non-negotiable output frame

- Default aspect ratio: **16:9 horizontal**.
- Default working target: `1920 × 1080 px` or the image generator's closest native 16:9 size.
- Never silently fall back to the upstream 3:5 vertical canvas.
- No black bars, phone mockup, app UI, split-screen player controls, or screenshot chrome.
- Generate the redesigned zine frame itself, not the top/bottom comparison layout seen in social-media screenshots unless the user explicitly asks for a comparison layout.

## Source fidelity

The transformed result must still be recognizably derived from the input frame.

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

Every result should combine these stable characteristics:

- tactile aged or archival paper base;
- matte, flat scanned-paper appearance;
- xerox, halftone, risograph, letterpress or weathered-print texture;
- substantial negative space;
- one dominant visual idea rather than a dense scrapbook;
- restrained small typography;
- one clearly visible chromatic anchor;
- quiet field-note, travel-archive, independent-zine mood;
- no glossy advertising finish.

### Negative-space range

Because the target is 16:9 and some travel scenes need spatial continuity, use a wider range than the upstream vertical poster:

- sticker / specimen modes: roughly **65%–85%** empty paper;
- collage / contour / architecture modes: roughly **45%–70%** empty paper;
- scenic-print mode: roughly **35%–60%** empty paper, with the image concentrated in one band or region rather than full-bleed photographic coverage.

The page must still feel sparse. Empty paper is an active compositional element.

## Location typography rule

When a place is known, include the location in English in a quiet area of the composition.

Preferred structure:

```text
PLACE NAME
REGION / PROVINCE, COUNTRY
```

Examples of placement:

- upper-left;
- upper-right;
- far lower-left;
- narrow vertical edge text when the layout supports it.

Rules:

- use small serif, typewriter or monospaced typography;
- do not turn the location into a commercial headline;
- location text should support the image, not dominate it;
- if the user gives Chinese place names, translate or romanize them carefully;
- if the exact location is unknown, do not invent one;
- do not invent coordinates, dates, weather, archive numbers, awards, phone numbers, addresses or other fake precision;
- coordinates may appear only if supplied or reliably available from the user's source information.

Optional micro-labels may include short neutral terms such as `FIELD NOTES`, `ARCHIVE`, `RIDGE STUDY`, `DUSK OBSERVATION`, `EROSION NOTES`, or `LAKE CONTOUR`, but use at most one or two and keep them secondary.

## Variation engine

For every new frame, select one **visual family**. For a sequence, do not repeat the same family on consecutive frames unless the user explicitly requests consistency over variety.

### Family A — Torn Photo Sticker

Use when the source has a strong view that works as a small preserved memory fragment.

- shrink the source into a torn or irregular photo clipping;
- occupy about 12%–28% of the canvas;
- place it off-center with large paper space around it;
- allow one piece of tape, color paper, stamp-like block or rough registration mark;
- preserve source colors inside the clipping more than in the surrounding paper.

### Family B — Color-Block Collage

Use when a source frame contains a clear color relationship such as blue water, orange sand, red clothing, green grass or a saturated sky.

- reduce the scene to 2–4 large flat printed shapes;
- use one source-derived high-chroma hue as the main anchor;
- allow one geometric paper block, irregular sticker or printed panel;
- keep secondary colors muted or paper-toned;
- do not become a bright commercial collage.

### Family C — Scenic Print

Use when the scene itself is the identity: mountain ridge, dune line, canyon, coast, plateau, lake or sunset silhouette.

- preserve the source's broad landscape geometry;
- translate it into halftone, risograph, photocopy, dry-brush or faded field-print language;
- concentrate the scene in the lower half, lower third, side band or one broad strip;
- keep a substantial paper/sky area untouched;
- preserve a small human figure if it carries scale or story.

### Family D — Contour / Field Map

Use when water, roads, terrain or topographic boundaries are visually distinctive.

- convert a dominant shape into simplified contour lines or a flat map-like field;
- preserve one source-derived shape as the primary evidence of place;
- use one saturated fill such as lake blue, rust orange, field green or tomato red;
- combine with sparse archival labels and tiny geographic notes;
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
- use the most negative space of all full-scene modes.

## Choosing the family

Selection should feel random across a batch, but not arbitrary.

Use this priority:

1. identify what makes the source frame unique;
2. exclude families that would destroy that evidence;
3. among the remaining valid families, rotate away from the previous 1–2 outputs;
4. choose a family that produces a visibly different composition, not only a different object position.

For batches, aim for a healthy spread across sticker, collage, scenic, contour, architecture and symbolic treatments when the source material supports them.

## Color logic

Prefer a color anchor derived from the source frame rather than a fixed house color.

Examples:

- blue lake → cobalt / ultramarine / mineral blue;
- red jacket → tomato red / vermilion;
- orange desert or earth → ochre / burnt orange;
- green valley → field green / moss green;
- cold sky → cyan / dusty teal.

Rules:

- use **one main chromatic family** per image;
- preserve the anchor strongly enough to survive thumbnail viewing;
- let paper, grayscale photo fragments and microtext remain subdued;
- a tiny secondary hue is permitted only when it directly comes from the source and improves scene recognition;
- do not automatically force blue into every image;
- do not wash the accent into pastel unless the source or user requests it.

## Typography system

Preferred typography:

- small serif;
- typewriter;
- monospaced archive text;
- lightly distressed letterpress text.

Default hierarchy:

1. English location label;
2. optional field-note phrase;
3. optional tiny date or factual metadata only when supplied.

Avoid:

- oversized promotional headlines;
- dense explanatory paragraphs;
- fake editorial copy;
- meaningless English used as decoration;
- too many numbers;
- large Chinese text unless the user explicitly requests it.

If a source screenshot contains social-media overlay text, player controls, account names, likes, comments or UI elements, treat them as non-source content and exclude them from the generated zine frame.

## Prompt compiler

Write the final image-generation prompt as four compact blocks.

### Block 1 — Frame and paper

State:

- exact `16:9` horizontal format;
- paper tone and flat scanned texture;
- intended negative-space range;
- main visual region and placement.

### Block 2 — Source evidence and transformation

State:

- the scene elements that must remain recognizable;
- selected variation family;
- how those elements are simplified, clipped, printed, mapped or abstracted.

### Block 3 — Typography and color

State:

- English place text and exact placement;
- optional single field-note phrase;
- main source-derived chromatic hue;
- its physical form: ink block, tape, silhouette, water field, printed panel, clothing accent, etc.;
- print defects and micro-registration behavior.

### Block 4 — Mood and hard avoids

State:

- quiet archival travel-zine mood;
- matte, scanned, non-glossy finish;
- hard avoids: commercial ad, cinematic grading, 3D, neon, glossy poster, UI screenshot, black bars, dense scrapbook, fake technical data, unrelated invented scenery.

## Sequence mode

When transforming multiple frames from one trip or one video:

- keep a consistent paper family and typographic family;
- preserve a coherent print texture across the sequence;
- rotate layout families and accent colors according to each source frame;
- do not use the same sticker placement repeatedly;
- do not place the location label in the exact same corner every time;
- keep location naming format consistent;
- prefer scene-to-scene continuity over template repetition;
- maintain a visual rhythm: dense → sparse → contour → sticker → scenic, rather than ten near-identical pages.

## Negative constraints

Always reject or regenerate if the output becomes:

- vertical 3:5;
- full-bleed glossy travel photography;
- cinematic movie-still grading with depth-of-field drama;
- tourism advertising;
- a generic poster unrelated to the source frame;
- dense scrapbook with many stickers;
- neon, cyberpunk, kawaii, cartoon or 3D;
- UI screenshot or phone frame;
- fake map with invented data;
- unreadable gibberish dominating the page;
- overdecorated with many colors;
- a direct copy of the original photo with only a paper filter.

## Workflow

1. Inspect the source image or video frame.
2. Identify the scene's non-negotiable evidence of place.
3. Resolve the known location text; do not fabricate it.
4. Select one visual family using the variation rules.
5. Select one source-derived accent family.
6. Compile the four-block prompt.
7. Generate the 16:9 image.
8. Inspect the output at thumbnail scale and at normal scale.
9. Regenerate once if source fidelity, aspect ratio, location text, negative space or color anchor clearly fails.
10. Return the image, final prompt, selected family, location label and one-sentence interpretation note.

## Quality gate

Before marking the result complete, verify:

```text
[ ] output is 16:9 horizontal
[ ] no black bars, UI or screenshot chrome
[ ] source scene is still recognizably the same place/moment
[ ] at least three important source features were preserved when available
[ ] one visual family was selected and applied decisively
[ ] composition is meaningfully different from recent batch outputs
[ ] aged paper / archival print materiality is visible
[ ] negative space fits the selected family
[ ] one main source-derived chromatic family is visible
[ ] location appears in English when known
[ ] location text sits in negative space and is not a headline
[ ] no fake coordinates or invented factual metadata
[ ] typography is sparse and editorial
[ ] result is not a commercial travel ad
[ ] result is not merely the original photo plus a texture filter
[ ] sequence mode avoids repetitive template placement
```

If any critical item fails, the result is `DRAFT`, not complete.

## Output format

```markdown
**生成图**
[rendered 16:9 image]

**最终 Prompt**
```text
[final image-generation prompt]
```

**执行记录**
- Family: [A–F + name]
- Location: [English location or UNKNOWN]
- Accent: [source-derived chromatic family]
- Source evidence preserved: [short list]
- Status: READY | DRAFT
```
