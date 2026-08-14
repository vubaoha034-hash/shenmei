# VPD V2 — Photography + Graphic Design Distillation

Status: `DESIGN_SPEC_DRAFT`
Date: 2026-08-14

## 1. Objective

Distill a high-quality visual work into a reusable executable visual program that preserves the causal image-making logic rather than merely imitating surface appearance.

The program must support:

- `RECONSTRUCT`: recover the source family's image-making logic;
- `VARIATE`: produce new work in the same family without literal copying;
- `TRANSFER`: apply higher-level logic to new content or a new domain;
- `ONBOARD_NEW_STYLE`: distill a genuinely different style using the same compiler architecture.

The visual model remains the creative renderer. The distillation system acts as photographer/art director/designer/retoucher guidance, not as a manual drawing engine.

## 2. Three-engine representation

### 2.1 PHOTOGRAPHY_ENGINE

Used whenever photography, photorealism, rendered-material realism, or image treatment materially affects quality.

#### A. Capture geometry

Record visible/inferable cues:

- camera elevation / view angle;
- azimuth / subject orientation;
- perspective strength;
- camera-subject distance feel;
- focal-length feel (`wide / normal / short-tele / tele`) unless exact EXIF exists;
- horizon/vanishing behavior;
- frame orientation and crop;
- subject occupancy ratio;
- subject centroid / dominant mass;
- foreground / midground / background separation;
- occlusion structure.

Never invent an exact focal length or aperture from pixels when EXIF is absent. Use perceptual ranges and confidence.

#### B. Focus and optics

- focus target / focus plane;
- depth-of-field amount;
- near-to-far blur gradient;
- bokeh size/shape/edge character where visible;
- motion blur / directional blur;
- lens softness vs clinical sharpness;
- distortion cues;
- vignetting if present;
- optical imperfections if stylistically relevant.

#### C. Lighting architecture

- key-light direction;
- key-light elevation;
- key apparent size / softness;
- fill level and direction;
- negative fill;
- rim/back/accent light;
- source count / dominance;
- light falloff;
- shadow direction;
- shadow density;
- shadow-edge hardness;
- specular width/intensity;
- highlight rolloff;
- reflective-material behavior;
- translucency / subsurface cues where relevant;
- practical/environmental light contribution;
- atmospheric haze/steam interaction with light.

#### D. Exposure and tonal architecture

- highlight placement;
- midtone placement;
- black floor;
- dynamic-range feeling;
- contrast ratio;
- highlight shoulder / clipping behavior;
- shadow toe / crush behavior;
- local contrast distribution;
- luminance hierarchy by region;
- subject/background luminance separation.

#### E. Color science and grading

- white-balance feel;
- global temperature;
- warm/cool split by region;
- dominant hue families;
- hue relationships (analogous/complementary/etc.);
- saturation distribution, not merely average saturation;
- luminance-by-hue behavior;
- food/skin/material color plausibility;
- selective color suppression or emphasis;
- black/neutral tint;
- highlight tint / shadow tint;
- color contrast hierarchy;
- palette role map.

#### F. Texture, sharpness, and microcontrast

- edge acuity;
- microcontrast;
- local clarity;
- sharpening feel;
- detail preservation;
- surface roughness rendering;
- pores/fibers/grain/crumbs/condensation/oil texture where relevant;
- film/digital grain;
- halation;
- bloom;
- scan softness;
- compression artifacts if intentionally part of style.

#### G. Subject styling and scene construction

For food/product/portrait/interior work, include:

- plating/arrangement;
- prop family;
- surface/background material;
- environmental authenticity;
- controlled imperfection;
- ingredient/feature distribution;
- moisture/oil/steam behavior;
- cleanliness vs lived-in character;
- scale cues;
- styling density;
- temporal/action cues.

#### H. Post-processing / retouch behavior

- global grade;
- local dodge/burn;
- local saturation;
- highlight cleanup;
- shadow shaping;
- background suppression;
- subject separation;
- selective sharpening;
- selective blur;
- texture preservation;
- artifact cleanup;
- compositing evidence where relevant.

### 2.2 GRAPHIC_DESIGN_ENGINE

Used whenever type, layout, graphics, branding, or page/image composition materially affects quality.

#### A. Semantic / communication intent

- what the work is trying to make the viewer feel/do/understand;
- primary proposition;
- secondary proposition;
- visual metaphor;
- cultural/semantic references actually visible or supported by context;
- what must remain literal vs what may become symbolic.

Do not invent a brand strategy unsupported by the work.

#### B. Attention hierarchy

- first read;
- second read;
- third read;
- dominant/subordinate masses;
- visual entry point;
- scan path;
- focal competition;
- thumbnail-scale read.

#### C. Grid and geometry

- underlying grid family;
- alignment axes;
- margins / safe zones;
- column logic;
- baseline rhythm;
- modular relationships;
- symmetry/asymmetry;
- image box geometry;
- crop-edge relationships;
- intentional misalignment;
- optical offsets.

#### D. Typography and lettering

Separate typography into:

1. `TYPE_SELECTION`
   - serif/sans/display/script/mono/etc.;
   - contrast class;
   - width;
   - weight;
   - stroke modulation;
   - historical/functional category when inferable.

2. `TYPE_SCALE_SYSTEM`
   - title/body/caption ratios;
   - line length;
   - line height;
   - tracking;
   - case behavior;
   - punctuation behavior.

3. `LETTERING_BEHAVIOR`
   - stock font vs modified font vs custom lettering;
   - glyph width variation;
   - baseline irregularity;
   - rotation/skew;
   - terminal/cut behavior;
   - overlap/ligature behavior;
   - outline/fill/stroke treatment;
   - distortion/roughness/print deformation;
   - word silhouette;
   - optical spacing.

4. `TYPE_IMAGE_INTERACTION`
   - overlap;
   - occlusion;
   - edge collision;
   - text inside/around object;
   - text using negative space;
   - text as object vs text as information.

#### E. Copy meaning and verbal tone

- exact visible copy where readable;
- copy role;
- brevity/verbosity;
- literal vs poetic;
- informational vs emotional;
- syntax rhythm;
- relationship between wording and image.

This layer matters because changing text meaning can require changing typography/layout.

#### F. Whitespace / density

- whitespace map by region;
- active vs passive whitespace;
- density gradient;
- breathing zones;
- compression zones;
- content-to-empty ratio;
- whether empty space functions as hierarchy, tension, luxury, silence, or simply unused area.

#### G. Color system

- background role;
- text role;
- accent role;
- image color relation;
- brand color dominance;
- proportion of each role;
- local contrast requirements;
- whether palette comes from subject or imposes on subject.

#### H. Graphic language

- geometric marks;
- illustration;
- iconography;
- lines/borders;
- blocks/fields;
- masks/cutouts;
- collage;
- diagrams;
- repeated motifs;
- motif source/semantics;
- scale and repetition rhythm;
- whether graphics are structural or decorative.

#### I. Layering / crop / edge behavior

- z-order;
- occlusion;
- image overflow;
- elements crossing frame edge;
- clipping/masking;
- bleed;
- border behavior;
- negative-space cuts;
- foreground/background integration.

#### J. Material / print / surface behavior

- paper/substrate feel;
- ink behavior;
- risograph/letterpress/offset/xerox/halftone cues;
- emboss/deboss/foil/metallic cues if visible;
- matte/gloss contrast;
- edge wear;
- scan/print defects;
- tactile hierarchy.

#### K. Sequence / system behavior

For multi-page or campaign systems:

- what repeats;
- what varies;
- continuity assets;
- rhythm between pages;
- variation budget;
- transition logic;
- repeated mistakes to avoid.

### 2.3 INTEGRATION_ENGINE

This is mandatory for hybrid photo/design work.

It models how the two engines interact:

- photograph vs type dominance;
- shared color logic;
- whether the photograph provides negative space for type;
- whether type overlaps or avoids subject;
- how crop supports copy placement;
- how light direction supports graphic hierarchy;
- whether graphic marks are derived from image semantics;
- how material realism is protected from graphic treatment;
- whether post-processing anticipates layout;
- how typography scale is conditioned by image mass;
- what must remain legible at thumbnail size;
- what visual surprise appears only on second read.

## 3. Observation vs inference

Every extracted field must carry:

- `evidence_type`: `DIRECT_VISIBLE | METADATA | INFERENCE`;
- `confidence`: `0.0–1.0`;
- `source_region` or source asset reference;
- optional `uncertainty_note`.

Examples:

- soft shadow edge: direct visible;
- likely large soft source: inference;
- exact 90cm softbox: unsupported unless metadata exists;
- 85mm lens: unsupported unless EXIF/metadata exists.

Unsupported precision is a distillation bug.

## 4. Causal priority map

Every capsule must identify:

- `critical`: if changed, family/quality collapses;
- `important`: materially affects quality;
- `secondary`: visible but tolerant;
- `free`: can vary without damage.

Also record interactions, e.g.:

- `subject scale × title scale`;
- `shadow softness × surface texture`;
- `background luminance × text weight`;
- `crop × negative-space placement`;
- `depth of field × sharpening`;
- `accent saturation × image saturation`.

The thin renderer prompt must be selected from the highest-impact variables for the current task, not from whichever fields are easiest to verbalize.

## 5. Style signature vs content binding

Each extracted property must be classified as:

- `STYLE_SIGNATURE`: transferable style mechanism;
- `CONTENT_BOUND`: caused by the specific subject/content;
- `BRAND_BOUND`: belongs to source identity and must not be copied;
- `PRODUCTION_BOUND`: output-medium constraint;
- `OPTIONAL_VARIATION`: can vary.

This is required to avoid both literal cloning and over-generalization.

## 6. Renderer contract

The creative visual model receives:

- actual source/content images;
- actual visual anchors/crops;
- target use case;
- mode;
- a compact set of high-impact image-making controls;
- explicit freedoms;
- a short task-specific avoid list.

It must not receive the full schema dump.

The renderer is expected to create the image, not manually reproduce field values as vector geometry.

## 7. Professional quality gates

### Photography gate

Review at three scales:

1. thumbnail: overall mass/color/read;
2. normal view: light, color, focus, composition, realism;
3. detail view: texture, edge behavior, artifacts, sharpening, material response.

For food/product realism, independently judge:

- material authenticity;
- moisture/oil/specular behavior;
- ingredient/feature variation;
- contact shadows;
- depth;
- repeated/cloned detail;
- fake steam/smoke;
- unnatural microtexture.

### Graphic-design gate

Review:

- semantic clarity;
- hierarchy;
- grid/optical alignment;
- typography quality;
- type-image relationship;
- whitespace function;
- color role discipline;
- graphic-language coherence;
- non-genericity;
- production plausibility.

### Integration gate

Review whether photography and design form one system rather than two stacked layers.

## 8. Required tests before promotion

A Style Capsule is not promoted after one attractive output.

Minimum tests:

1. `SOURCE_RECONSTRUCTION_TEST`
   - can the model reproduce the style family without copying identity?

2. `CONTENT_SWAP_TEST`
   - new subject, same family.

3. `COMPOSITION_VARIATION_TEST`
   - different crop/layout while retaining family logic.

4. `ASPECT_TRANSFER_TEST`
   - different aspect ratio without stretching the original layout.

5. `STYLE_DISTANCE_TEST`
   - remains recognizably related but not near-copy.

6. `DIRECT_BASELINE_TEST`
   - compare against raw reference + short prompt using the same visual model.

7. `NEW_STYLE_COMPILER_TEST`
   - distill a second materially different style with unchanged compiler architecture.

Any complex system that cannot beat or at least match the direct baseline on usable quality is not promoted.

## 9. Non-goals

V2 does not promise to recover exact hidden camera settings from pixels.
It does not train model weights.
It does not claim one global aesthetic formula.
It does not replace human aesthetic judgment.
It does not require Figma for zero-to-one image creation.

## 10. Success definition

The system succeeds only if it can answer both:

1. `Why does this image look this way at a photography/design-production level?`
2. `How do I make a new image of different content that preserves the same quality logic without literal copying?`

and then demonstrate both claims with generated outputs that survive independent human review.
