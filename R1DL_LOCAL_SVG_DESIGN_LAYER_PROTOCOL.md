# R1D-L — LOCAL SVG DESIGN LAYER PROTOCOL

Status: `ACTIVE_FALLBACK / NO_FIGMA_DEPENDENCY`
Date: `2026-08-14`

## Purpose

Continue the already locked `STOVE-RIM EDITORIAL` Art Direction without relying on Figma MCP. This stage changes only the execution surface, not the design direction, food asset, typography content, color logic, or quality criteria.

## Frozen source

Use only the frozen food asset:

`R1_SINGLE_DISH_HERO_CANDIDATE.png`

Google Drive file ID:

`1ptSMiN7b88DEvbmWdQ7l4Td_BTo-PWh8`

The food raster is frozen. No ImageGen, inpaint, redraw, repaint, or generative modification is allowed.

## Locked Art Direction

Read and execute `R1C_ART_DIRECTION_LOCK_RESULT.md` exactly.

Working direction:

`STOVE-RIM EDITORIAL`

Primary mechanism:

`PAN RIM ARC + HEAT TRAIL + CHILI POINT RHYTHM`

Selected anchors remain:
- R1C-APPROVED-13: composition / typography / negative space;
- R1C-APPROVED-16: proprietary product-derived graphic language;
- R1C-APPROVED-05: culinary action / supporting graphic system.

No new reference selection or style exploration is permitted.

## Output technology

Create exactly one editable SVG document plus one raster export.

Required files:
- `R1DL_STOVE_RIM_EDITORIAL.svg`
- `R1DL_STOVE_RIM_EDITORIAL.png`

Canvas:
- 4:5
- preferred 1080 x 1350 or 1200 x 1500.

SVG must contain:
- embedded or explicitly linked frozen raster asset with lineage recorded;
- editable `<text>` nodes using a real installed Chinese font;
- editable vector paths for pan-rim arc, heat-trail, and chili-point rhythm;
- real mask/clip paths for image crop where needed;
- no flattened text-as-image workaround.

## Typography

Use only:
- title: `今日现烧`
- supporting copy: `锅气刚好，趁热吃`

Title must not be one uniform heavy sans line. It must have internal hierarchy with one phrase dominant and the other subordinate.

Prefer a real Chinese display/serif/humanist face with some hand-made energy. `Noto Serif SC` is an acceptable fallback.

No fake English, price, date, QR, address, microcopy, or invented brand story.

## Attention geometry

- Food remains the primary visual anchor.
- Use a strong asymmetrical crop.
- Pan should occupy roughly 55–65% of the canvas and be partially cropped by the frame.
- Visual mass biases lower-right or lower-center.
- Upper-left / upper field remains a real breathing zone for title and tension.
- Title cluster, image edge, and pan-rim arc must interlock as one composition.

Automatic failure patterns:
- rectangular food image under headline;
- headline + arbitrary geometric block;
- centered generic poster;
- large L-shape or border frame;
- empty whitespace with no compositional role.

## Product-derived vector mechanism

Use exactly these three semantic families:

1. `PAN RIM ARC`
   - one or two partial arcs derived from actual pan geometry;
   - no arbitrary circle decorations.

2. `HEAT TRAIL`
   - restrained line/path behavior that links food and title;
   - no fake smoke bitmap or CGI steam.

3. `CHILI POINT RHYTHM`
   - sparse deep-chili-red dots or short marks;
   - small quantity only;
   - must feel derived from pepper / heat / sparks.

Maximum supporting graphic groups: 3.

## Color

Only:
- warm mineral off-white;
- charcoal / near-black;
- deep fermented-chili red;
- natural colors from frozen food image.

No bright orange, black-gold, extra brand blue/green, large red block, or generic premium gradient.

## Image treatment

Allowed:
- crop;
- scale;
- position;
- clip/mask;
- non-destructive tonal matching if done outside the frozen food pixels or recorded as display-level treatment.

Forbidden:
- ImageGen;
- repaint;
- inpaint;
- generative fill;
- fake smoke;
- artificial vignette used to simulate premium mood.

## Execution discipline

Exactly one design execution.

Forbidden:
- second concept;
- variant;
- duplicate layout;
- best-of-N;
- redesign after viewing output;
- alternate colorway.

If the output is weak, keep it as the diagnostic result and stop.

## Technical gate

Before review confirm:
- source asset SHA recorded;
- SVG is valid and opens;
- text remains editable text in SVG;
- vector mechanism remains vector;
- frozen raster asset is not regenerated;
- PNG export succeeds;
- PNG MIME / dimensions are correct;
- exactly one SVG and one PNG were produced.

## Review transport

Upload only the final PNG to:

`LIU_VISUAL_REVIEW/R1DL/`

The SVG can remain in private runtime or be uploaded separately outside the user review folder if needed.

Final aesthetic judgment must be performed by ChatGPT from actual PNG pixels and then by the user as `USABLE / UNUSABLE`.

Codex must not declare aesthetic PASS.

## Exit

Allowed outcomes:
- `R1DL_DESIGN_READY / WAITING_FOR_INDEPENDENT_PIXEL_REVIEW`
- `R1DL_TECHNICAL_FAILURE`

Do not enter R2, packaging, evidence expansion, or Discovery changes after completion.
