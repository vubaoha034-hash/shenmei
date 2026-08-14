# VPD V2 Measurement + Causal Spec

Status: `MANDATORY_ADDENDUM`

## 1. Why this addendum exists

A detailed taxonomy is still insufficient if the analyst can fill it with vague prose.

V2 therefore requires three parallel representations for important variables:

1. `MEASURED / DIRECTLY OBSERVED`
2. `INFERRED PRODUCTION HYPOTHESIS`
3. `CAUSAL QUALITY HYPOTHESIS`

These must not be collapsed.

## 2. Single-reference limitation

One reference image cannot prove which visible properties are true style invariants.

With one source, all proposed invariants are initially:

`INVARIANT_HYPOTHESIS`

They become `VALIDATED_STYLE_SIGNATURE` only after surviving one or more controlled changes such as:

- content swap;
- crop/composition variation;
- aspect-ratio change;
- copy change;
- palette change where appropriate.

If 2–5 coherent references from the same known visual family exist, cross-example recurrence may strengthen the hypothesis before generation, but it still does not replace output validation.

This prevents the system from treating every accidental detail in one picture as style law.

## 3. Required measured evidence — composition

Where material, record normalized estimates:

- canvas width/height ratio;
- primary subject bounding box `[x, y, w, h]` in 0–1 coordinates;
- primary subject occupancy ratio;
- dominant visual mass centroid `[x, y]`;
- key negative-space regions with normalized boxes/polygons;
- horizon / dominant perspective direction when visible;
- major alignment axes;
- crop/edge crossings;
- number and rough location of major visual clusters;
- image/type overlap or distance relationship.

These are estimates from pixels, not physical camera metadata.

## 4. Required measured evidence — tone / color

Where material, record:

- dominant palette samples (approximate RGB/HEX) with role and rough area proportion;
- relative luminance order of subject/background/type/accent;
- highlight, midtone and shadow occupancy tendency;
- saturation distribution by major region;
- warm/cool region map;
- black/neutral tint direction;
- local contrast hotspots;
- color separation between subject and background.

Do not invent exact colorimetry beyond what the source supports.

## 5. Required measured evidence — focus / sharpness

Where material, record:

- focus target region;
- sharpness hierarchy across regions;
- blur-gradient direction;
- approximate blur category (`NONE / LOW / MODERATE / STRONG`);
- microcontrast category by key region;
- edge character (`CRISP / NATURAL / SOFT / HALATED / OVER-SHARPENED`);
- visible grain/noise/scan character.

Avoid fake aperture/focal-length claims without metadata.

## 6. Required measured evidence — lighting

Where material, record observable cues:

- brightest directional side/region;
- shadow direction;
- shadow-edge category;
- highlight/specular region and width category;
- fill depth category;
- back/rim presence;
- falloff character;
- subject/background luminance relationship;
- atmosphere/steam interaction.

Then separately record inferred lighting hypotheses, with confidence.

## 7. Required measured evidence — typography/layout

Where text/design is material, record:

- text bounding boxes normalized to canvas;
- title height as fraction of canvas height;
- title width as fraction of canvas width;
- relative scale ratios among title/subtitle/body/caption;
- alignment axes;
- text-image overlap/interlock region;
- estimated line-height ratio;
- tracking category;
- baseline regularity;
- width/weight variation across glyphs/words;
- custom-lettering indicators;
- whitespace around title and copy;
- reading order.

The goal is not pseudo-precision. The goal is to prevent `big type / lots of whitespace` from passing as a complete analysis.

## 8. Required measured evidence — texture/material

Where material, record region-specific cues:

- rough/matte/gloss/translucent behavior;
- specular character;
- surface irregularity;
- fine-detail density;
- repeated/cloned detail risk;
- grain/halftone/ink bleed/paper fiber/scan noise;
- edge wear or print defects;
- moisture/oil/condensation cues for food/product work.

## 9. Causal quality hypotheses

For every `CRITICAL` or `IMPORTANT` variable, record:

- `hypothesis`: why this variable contributes to quality/family identity;
- `counterfactual`: what would happen if it changed materially;
- `interaction`: what other variable it depends on;
- `validation_test`: which benchmark output can test it.

Example:

Variable: `large warm neutral negative space around display title`

Hypothesis:
`The empty field increases title authority and lets the lower food mass feel deliberate rather than crowded.`

Counterfactual:
`If filled with decorative marks or additional copy, the design becomes generic promotional clutter.`

Interaction:
`depends on title scale and lower image mass.`

Validation test:
`COMPOSITION_VARIATION_TEST`.

## 10. Quality-causing vs merely present

Every observed property must be classified as one of:

- `QUALITY_CAUSAL_HYPOTHESIS`
- `FAMILY_SIGNATURE_HYPOTHESIS`
- `CONTENT_INCIDENTAL`
- `BRAND_SPECIFIC`
- `PRODUCTION_ARTIFACT`
- `UNKNOWN`

The compiler must not transfer a property merely because it is visible.

## 11. Evidence overlays

For high-value references, create non-destructive analytical overlays/annotations as private diagnostic artifacts when tooling permits:

- subject/mass boxes;
- negative-space map;
- light direction map;
- focus/sharpness map;
- palette-role swatches;
- typography boxes/alignment axes;
- reading-order arrows.

These overlays are for analysis and QA only. They are not renderer reference images unless explicitly required.

## 12. Renderer boundary

Measured evidence is not dumped into the renderer prompt.

It informs selection of the 4–10 highest-impact controls.

Example analysis may contain 60 fields, while renderer payload may contain only:

- large lower-right food mass, close crop;
- soft side/back light with controlled speculars;
- warm-neutral background held brighter than food shadows;
- moderate depth separation, food surface fully readable;
- high-authority custom display type occupying upper-left breathing field;
- restrained dark-red accent;
- preserve natural food irregularity and texture.

## 13. Acceptance

A capsule fails professional distillation if:

- critical areas have only adjectives and no observable evidence;
- exact hidden camera settings are fabricated;
- typography is reduced to font category/size;
- color is reduced to palette names without role/proportion;
- lighting is reduced to `soft / cinematic`;
- sharpness/blur/post-processing are omitted when they materially shape the image;
- one-reference incidental details are declared universal invariants without validation;
- all visible features are transferred without causal prioritization.
