# Visual Distillation Compiler Contract V2

Status: `FROZEN_FOR_IMPLEMENTATION`
Compiler id: `visual-distillation-compiler-v2`

## 1. Principle

The compiler must behave like a coordinated photographer + retoucher + graphic designer + art director.

It does not merely describe a reference image. It extracts the image-making decisions that are both:

- perceptually responsible for the result;
- transferable enough to guide a strong visual model on new content.

The compiler must not replace the strong visual model with manual low-level drawing.

## 2. Input

Required:

- canonical reference pixels;
- provenance/hash;
- absolute quality status;
- task/domain context.

Optional:

- coherent supporting references;
- EXIF/metadata;
- user feedback tied to the reference;
- rejected failure anchors;
- source/content image for a target transfer test.

Reject if:

- positive reference is only `RELATIVE_ONLY`;
- unrelated styles are silently mixed;
- raw pixels are unavailable;
- the source quality is not sufficient to serve as an anchor.

## 3. Stage A — Reference type classification

Before detailed decomposition, classify the work as one or more of:

- `PHOTO_LED`
- `TYPE_LED`
- `ILLUSTRATION_LED`
- `MATERIAL_PRINT_LED`
- `HYBRID_PHOTO_DESIGN`
- `SEQUENCE_SYSTEM`

This controls which engines receive the most attention.

A photo-led work still gets design analysis if design matters. A type-led poster still gets photography analysis if photography materially contributes.

## 4. Stage B — Photography Engine decomposition

For every relevant field, record:

- value;
- evidence type;
- confidence;
- source region;
- uncertainty.

### B1 Capture geometry

Analyze:

- view angle/elevation;
- perspective strength;
- focal-length feel, never unsupported exact focal length;
- subject-camera distance feel;
- horizon/vanishing behavior;
- framing/crop;
- subject occupancy;
- dominant mass centroid;
- foreground/midground/background structure;
- occlusion.

### B2 Focus / optics

Analyze:

- focus target;
- focus plane;
- DOF amount and gradient;
- bokeh character;
- motion/subject blur;
- optical softness/sharpness;
- distortion/vignette/aberration cues if stylistically meaningful.

### B3 Lighting

Analyze:

- key direction/elevation;
- apparent source size and softness;
- fill/negative fill;
- back/rim/accent light;
- falloff;
- shadow direction/density/edge hardness;
- specular width/intensity;
- highlight rolloff;
- practical/environment contribution;
- atmospheric interaction.

Do not reduce this to `soft light` or `cinematic light`.

### B4 Exposure / tone

Analyze:

- highlight placement;
- midtone placement;
- black floor;
- dynamic range;
- contrast ratio;
- shoulder/toe behavior;
- local contrast;
- luminance hierarchy;
- subject/background separation.

### B5 Color science / grade

Analyze:

- WB feel;
- global temperature;
- local warm/cool split;
- hue families;
- hue relationships;
- saturation distribution;
- luminance by hue;
- material/food/skin color plausibility;
- selective suppression/emphasis;
- neutral/black tint;
- highlight/shadow tint;
- role-based color map.

### B6 Texture / sharpness

Analyze:

- edge acuity;
- microcontrast;
- clarity;
- sharpening feel;
- detail retention;
- roughness/surface texture;
- grain;
- halation;
- bloom;
- scan softness;
- deliberate degradation.

### B7 Subject styling

Analyze subject-dependent styling:

- arrangement/plating;
- props;
- background/surface materials;
- imperfection;
- density;
- moisture/oil/steam;
- contact behavior;
- temporal/action cues;
- authenticity cues.

### B8 Post-processing

Analyze:

- global grade;
- local dodge/burn;
- selective saturation;
- subject separation;
- selective sharpening/blur;
- background suppression;
- highlight cleanup;
- texture protection;
- compositing evidence.

## 5. Stage C — Graphic Design Engine decomposition

### C1 Semantic intent

Record what is supported by visible content/context:

- primary message;
- secondary message;
- emotional/functional job;
- literal vs symbolic relationship;
- visual metaphor.

Do not invent marketing strategy not evidenced by the work.

### C2 Attention hierarchy

Record:

- first/second/third read;
- visual entry point;
- scan path;
- dominant/subordinate masses;
- competition points;
- thumbnail read.

### C3 Grid / geometry

Record:

- grid family;
- alignment axes;
- margins;
- columns;
- baseline rhythm;
- symmetry/asymmetry;
- optical offsets;
- image box geometry;
- intentional misalignment;
- edge/crop relationships.

### C4 Typography / lettering

Separate:

- type selection category;
- scale ratios;
- weight/width ratios;
- line height;
- tracking;
- alignment;
- stock vs modified vs custom lettering;
- glyph irregularity;
- terminal/cut behavior;
- baseline variation;
- overlap/ligature;
- outline/fill/stroke;
- deformation/roughness;
- word silhouette;
- optical spacing;
- type-image interaction.

`big bold type` is not an acceptable distilled description.

### C5 Copy meaning

Record:

- exact readable text;
- copy role;
- literal/poetic/informational tone;
- sentence rhythm;
- image-copy relationship.

Typography is conditioned by meaning; changing copy can require a new lettering treatment.

### C6 Whitespace / density

Record:

- region map;
- active vs passive whitespace;
- density gradient;
- breathing/compression zones;
- empty-to-content ratio;
- function of emptiness.

### C7 Color system

Record role relationships:

- background;
- type;
- accent;
- image;
- proportions;
- local contrast;
- whether palette is subject-derived or imposed.

### C8 Graphic language

Record:

- marks;
- illustration;
- icons;
- rules/lines;
- fields/blocks;
- masks/cutouts;
- collage;
- diagrams;
- repeated motifs;
- semantic source of motifs;
- structural vs decorative role;
- repetition rhythm.

### C9 Layer / crop / edge

Record:

- z-order;
- overlap;
- occlusion;
- clipping;
- bleed;
- overflow;
- edge crossing;
- frame interaction.

### C10 Material / print

Record visible production language:

- paper/substrate;
- ink behavior;
- halftone;
- letterpress/risograph/xerox/offset cues;
- emboss/deboss/foil if visible;
- gloss/matte contrast;
- wear/scan defects.

### C11 Sequence/system

For campaigns/sets:

- fixed continuity assets;
- variation budget;
- page rhythm;
- transition logic;
- repeated layout constraints;
- what must not repeat.

## 6. Stage D — Integration Engine

Mandatory for hybrid work.

Extract how the image and design co-create the result:

- which dominates;
- where the image intentionally leaves type-safe tonal space;
- how crop anticipates type;
- whether type crosses subject/edge;
- how color grade supports type contrast;
- how lighting supports hierarchy;
- whether motifs derive from subject semantics;
- how realism is protected from graphic treatment;
- how type scale responds to image mass;
- thumbnail first read vs second-read detail.

If the compiler cannot explain the interaction, the work has not been distilled deeply enough.

## 7. Stage E — Causal priority map

Every meaningful variable receives:

- priority: `CRITICAL / IMPORTANT / SECONDARY / FREE`;
- classification: `STYLE_SIGNATURE / CONTENT_BOUND / BRAND_BOUND / PRODUCTION_BOUND / OPTIONAL_VARIATION`;
- confidence;
- tolerance;
- interactions.

The purpose is to identify what actually matters.

The renderer prompt is compiled from the highest-impact variables for the current target.

Do not simply include every field.

## 8. Stage F — Transfer logic

For every capsule, define:

- invariants;
- degrees of freedom;
- do-not-copy elements;
- transfer operators.

Required operators:

- `CONTENT_SWAP`
- `COMPOSITION_VARIATION`
- `ASPECT_ADAPT`
- `TYPOGRAPHY_REBIND`

Use as relevant:

- `PALETTE_SHIFT`
- `LIGHTING_REBIND`
- `OPTICS_REBIND`
- `MOTIF_REBIND`
- `MATERIAL_SHIFT`
- `DENSITY_SHIFT`

An operator must state:

- what changes;
- what stays;
- what breaks the family.

## 9. Stage G — Renderer compilation

The strong visual model receives:

- actual reference pixels/crops;
- source/content asset;
- use case;
- mode;
- no more than 10 high-impact controls;
- explicit freedoms;
- no more than 6 task-relevant hard avoids.

Do not send the full decomposition.

The prompt must use concrete image-making language.

For photography, prefer words about:

- camera/framing;
- light;
- tone;
- grade;
- focus;
- texture/material;
- styling.

For design, prefer words about:

- hierarchy;
- grid;
- type behavior;
- spacing;
- color roles;
- graphic language;
- image/type interaction.

## 10. Stage H — Quality review

Review at multiple scales.

### Thumbnail

- overall mass;
- palette;
- first read;
- hierarchy;
- family signature.

### Normal view

- composition;
- light;
- color;
- focus;
- type;
- spacing;
- image/type interaction;
- semantic clarity.

### Detail view

- material realism;
- edges;
- microtexture;
- sharpening;
- artifacts;
- glyph quality;
- print/texture behavior.

Machine checks do not replace human absolute quality judgment.

## 11. Stage I — Benchmark before promotion

Required conditions using the same underlying visual model:

1. Direct reference baseline;
2. V2 reconstructed family output;
3. V2 content-swap output;
4. V2 composition variation;
5. V2 aspect transfer;
6. style-distance/non-copy check;
7. second materially different reference distilled with unchanged compiler.

Promotion requires that the system not consistently degrade usable quality versus the direct baseline.

## 12. Self-audit questions

Before rendering, the compiler must answer:

- Have I separated direct visible evidence from inference?
- Have I analyzed the photographic image-making chain deeply enough?
- Have I analyzed typography beyond font category and size?
- Have I explained image/type interaction?
- Have I identified the actual high-impact variables?
- Have I preserved raw visual anchors?
- Have I made transfer instructions executable?
- Have I prevented brand/source copying?
- Is the renderer receiving art direction rather than governance prose?

Any NO -> `DISTILLATION_NOT_READY`.
