---
name: gc-minimal-zine-travel-poster-v1
description: Turn a travel photo, landscape, architecture scene, person-in-place photo, or location brief into a 16:9 minimal zine / archival editorial poster. Derived from LiamGvchi/gc-minimal-zine-poster. Use for cinematic travel-to-zine transformations with aged paper, restrained print texture, randomized collage/block/imagery treatments, and accurate English place labels in negative space.
---

# GC Minimal Zine Travel Poster v1

This skill is a 16:9 travel-photo adaptation of `gc-minimal-zine-poster-v0-1`.

It should preserve the identity of the supplied place/photo while translating it into a quiet, tactile, editorial ZINE image rather than merely applying a filter.

## Core output

For each request, produce:

1. one generated 16:9 poster image;
2. the exact final image-generation prompt;
3. the selected visual recipe;
4. a short note explaining the transformation.

Generate the image by default. Only stop at prompt-only output when the user explicitly asks for prompt only.

## 1. Canvas and composition

- Default aspect ratio: **16:9 horizontal**.
- The final deliverable is a single poster frame, not a phone screenshot and not a stacked before/after composite unless the user explicitly asks for that.
- Use warm or neutral aged paper, scanned paper, uncoated stock, or quiet off-white as the dominant base.
- Keep meaningful negative space, normally about 35%-70% of the frame. Do not force the original upstream 70%-90% rule when it would destroy the location identity.
- The main subject or transformed scene should normally occupy about 20%-55% of the frame.
- Preserve a clear first visual center.
- Avoid perfectly centered commercial-ad symmetry unless the source scene truly calls for it.

## 2. Photo fidelity rule

When a reference photo is supplied:

- preserve the recognizable terrain, building silhouette, shoreline, mountain profile, tree, person pose, or other defining geometry;
- keep the subject's orientation and key spatial relationship recognizable;
- do not invent famous landmarks, architecture, weather, props, clothing, or geography not present in the source;
- do not turn a real place into a generic stock-travel scene;
- stylize through paper, print, crop, silhouette, contour, halftone, risograph, xerox, ink, and collage logic rather than by replacing the scene.

If no photo is supplied, build one clear visual metaphor from the brief.

## 3. Randomized visual grammar

Before writing the final prompt, choose one primary treatment and optionally one supporting treatment. Do not repeat the same treatment in consecutive outputs when alternatives fit.

### Primary treatment families

1. **paper-sticker-photo**
   - a torn or deckled photo fragment sits on aged paper;
   - may include one small tape/ink/tab accent;
   - the photo remains recognizable.

2. **color-block-field**
   - translate part of the terrain, sky, architecture, or path into one flat high-chroma printed block;
   - allow imperfect risograph edges and slight registration shift;
   - the block should belong to the scene rather than float as decoration.

3. **imagery-map**
   - convert the landscape into contour, topographic, erosion-band, architectural elevation, or field-note imagery;
   - retain the original silhouette/profile;
   - combine with one restrained photo or color anchor.

4. **vertical-slice-memory**
   - preserve one narrow vertical photo slice containing a person, tree, tower, doorway, or other key motif;
   - surround it with paper, abstract landscape fields, or sparse type.

5. **archival-specimen**
   - isolate one architectural form, tree, rock, sign, or person as a specimen-like anchor;
   - use old-print softness, halftone, paper fibers, or xerox wear.

6. **layered-terrain-bands**
   - simplify mountains, desert, water, or stratified rock into 2-4 horizontal printed bands;
   - use subdued black/gray plus one accent hue;
   - keep a small real-photo or person anchor when useful.

7. **type-led-field-note**
   - typography and small archive marks become the main compositional scaffold;
   - image remains secondary and sparse;
   - only use when the source has enough negative space.

### Supporting elements

Choose sparingly from:

- one torn paper edge;
- one small opaque color sticker/tab;
- one irregular ink field;
- one topographic line;
- one crop mark or registration cross;
- one short archival rule line;
- one small coordinate/date block only when factual data is known.

Do not use all of them at once.

## 4. Color engine

- Use paper tone + black/gray + **one dominant accent hue**.
- Preferred accent families: cobalt/ultramarine, cyan, mineral blue, tomato red, burnt orange, ochre, moss/pear green.
- The accent may be a terrain field, clothing retained from the photo, a tree/subject, a block, an irregular cutout, or type.
- Prefer an accent area large enough to read at thumbnail scale, normally about 2%-12% of the frame depending on the recipe.
- Do not automatically desaturate an important source-color cue such as a red jacket, orange shirt, or blue lake if it is the visual anchor.
- Avoid multicolor scrapbook aesthetics.

## 5. Typography and location labels

Typography should feel like an archival field note, independent travel zine, museum study sheet, or small-run editorial print.

Use:

- small serif, typewriter, or monospaced text;
- restrained uppercase labels;
- sparse microtext;
- occasional vertical type or a short poetic phrase;
- imperfect print registration when useful.

### Place Label Engine

If the user provides a location, add a concise English/romanized location label in a negative-space area.

Recommended hierarchy:

`PLACE / REGION, COUNTRY`

Examples of form only:

- `YUSHAN ISLAND / FUJIAN, CHINA`
- `ZHADA EARTH FOREST / TIBET, CHINA`

Accuracy rules:

- Never invent a specific place name from visual guesswork alone.
- Never invent coordinates, dates, altitude, weather, archive numbers, telephone numbers, awards, or institutions.
- If location is unknown, omit the location label or use a neutral label such as `FIELD NOTES / LOCATION UNSPECIFIED`.
- If the user supplies Chinese place text, romanize/translate conservatively and keep the original meaning.

Location text is a supporting element, never the main headline unless requested.

## 6. Print and material texture

Use tactile reproduction cues such as:

- aged uncoated paper fibers;
- xerox softness;
- risograph grain;
- halftone degradation;
- faded offset ink;
- letterpress bleed;
- scan noise;
- subtle edge wear;
- slight misregistration;
- deckled/torn photo edges.

The overall image should still read as a flat scanned print, not as a 3D mockup sitting on a desk.

## 7. Mood

Default emotional direction:

- quiet;
- solitary;
- cinematic without cinematic lighting tricks;
- memory-like;
- distant;
- field-recording / travel-journal / archival;
- Japanese/Korean indie-zine restraint;
- tactile and human rather than polished-commercial.

## 8. Hard avoids

Avoid:

- glossy travel advertising;
- tourism-bureau campaign layouts;
- giant commercial headlines;
- logo/CTA lockups;
- generic poster templates;
- dense scrapbook collage;
- excessive stickers;
- more than two strong accent colors;
- neon, cyberpunk, chrome, glassmorphism;
- glossy 3D paper mockups;
- cinematic lens flare or dramatic studio lighting;
- full replacement of the real landscape with fantasy scenery;
- fake landmarks or fake metadata;
- long clean body-copy blocks;
- random meaningless English used only to look professional.

## 9. Prompt compiler

Write the final image-generation prompt as four compact paragraphs in this order:

1. **frame + paper + negative-space geometry + subject scale/location**;
2. **source-photo fidelity + chosen primary treatment + any supporting treatment**;
3. **typography + accurate place label + exact accent hue/form + print defects**;
4. **flat scanned-paper mood + hard avoid list**.

The prompt must be concrete and imageable. Do not dump the whole SKILL.md into the prompt.

## 10. Workflow

1. Parse the source image or brief.
2. Identify the one defining visual feature: terrain silhouette, architecture, person-in-place, tree, lake, ridge, dune, coastline, etc.
3. Extract factual location text only if provided or otherwise verified from user context.
4. Choose one primary treatment family at random from the eligible set, avoiding recent repetition.
5. Choose one dominant accent hue based on the source image when possible.
6. Compile the four-paragraph prompt.
7. Generate a **16:9** image.
8. Inspect at thumbnail scale and at normal size.
9. Regenerate once if any of these fail:
   - source identity is lost;
   - place label is wrong or fabricated;
   - the result becomes commercial/generic;
   - the paper/print materiality is weak;
   - the accent feels pasted on rather than integrated;
   - the layout repeats the immediately previous recipe without reason.
10. Return image, prompt, recipe, and one short interpretation note.

## 11. Quality gate

Before finalizing, confirm:

- [ ] Output is 16:9 horizontal unless user requested another ratio.
- [ ] The source place/subject is still recognizable.
- [ ] The composition contains meaningful negative space.
- [ ] One primary treatment family is clearly dominant.
- [ ] Color/sticker/imagery treatment is integrated into the scene rather than decorative clutter.
- [ ] There is at most one dominant accent hue.
- [ ] Paper/print/scanning texture is visible but not dirty for its own sake.
- [ ] English location text is accurate, small, and placed in negative space when factual location is known.
- [ ] No fake coordinates, dates, archive codes, or filler English were invented.
- [ ] No tourism-ad, glossy mockup, 3D, neon, cyberpunk, or dense scrapbook aesthetic appears.
- [ ] The image was actually generated unless prompt-only was explicitly requested.

## Output format

```markdown
**生成图**

[rendered 16:9 image]

**最终 Prompt**

```text
[exact prompt used]
```

**视觉配方**

- Treatment: [primary treatment + optional supporting treatment]
- Accent: [hue + form]
- Place label: [exact text or omitted]
- Texture: [print/scanning treatment]

**说明**

[one concise sentence]
```

## Upstream attribution

Derived from `LiamGvchi/gc-minimal-zine-poster` (`gc-minimal-zine-poster-v0-1`), MIT License, Copyright (c) 2026 LiamGvchi.

See `UPSTREAM_LICENSE.txt` in this skill directory.
