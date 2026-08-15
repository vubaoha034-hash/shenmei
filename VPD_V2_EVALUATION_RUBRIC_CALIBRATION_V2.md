# VPD V2 Evaluation Rubric Calibration V2

Status: `MANDATORY_FOR_FUTURE_HUMAN_REVIEW`

## 1. Why this correction exists

A replacement independent blind review rated the benchmark 8/8 USABLE and 2/8 TOP_TIER, largely rewarding legibility, cleanliness, material plausibility, recognizable hierarchy, and lack of catastrophic artifacts.

The user explicitly rejected that calibration: food/material realism was only around 6/10 in the user's own wording, while design/typography/layout/integration were around 1-2/10 and the batch was visually ugly.

The evaluation bug is a correctness/taste conflation.

## 2. Two-axis review is mandatory

### Axis A — Technical / Production Correctness

Evaluate separately:

- text legibility / character correctness;
- absence of catastrophic image artifacts;
- object integrity;
- material plausibility;
- crop/export integrity;
- basic hierarchy readability;
- file/production correctness.

A high Axis A score means the image is technically coherent. It does NOT mean the image is aesthetically good.

### Axis B — Aesthetic / Art-Direction Quality

Evaluate separately:

- absolute visual impact;
- authored composition;
- typography/lettering authorship;
- semantic graphic system;
- photo/type integration;
- controlled whitespace;
- color sophistication;
- non-genericity;
- reference-family mechanism fidelity without literal copying;
- campaign/brand authorship;
- second-read intelligence;
- distance to the approved canonical reference quality floor.

A visually generic, template-like output may score well on Axis A and very poorly on Axis B.

## 3. Reference-distance requirement

For benchmark work with canonical approved references, every aesthetic review must explicitly compare the output against the relevant reference at:

- thumbnail;
- normal view;
- detail view.

The reviewer must answer:

`If the approved reference is the target quality class, how far below it is this output in photography, design, typography, integration, and authorship?`

Do not score in isolation against ordinary commercial ads.

## 4. Absolute-quality floor

`USABLE` for LIU VISUAL SYSTEM means the user would realistically accept the image as a finished aesthetic output for the intended use, not merely that a generic restaurant could technically publish it.

`TOP_TIER` means competitive with strong professional reference work on the relevant dimensions. Clean execution alone is insufficient.

If an image is technically coherent but aesthetically generic/ugly, it is `UNUSABLE` for this project.

## 5. Relative gain cannot override absolute failure

If condition B is better than condition A but both are below the absolute aesthetic floor, record:

`RELATIVE_GAIN / ABSOLUTE_FAIL`

Do not convert relative preference into approval.

A benchmark may prove a causal improvement while the whole system still fails production quality.

## 6. Generic-template failure indicators

Examples requiring strong aesthetic penalties when present:

- oversized generic brush/calligraphy headline used as the main design mechanism;
- `big title + plate of food` with no authored secondary system;
- black/red/white Chinese-restaurant trope without reference-specific structural intelligence;
- beige/mineral background + centered plate + headline where whitespace is merely empty rather than actively composed;
- decorative red brush blocks, chili/star-anise line art, steam, or flames added as generic symbols rather than semantically integrated mechanisms;
- typography that is merely readable or expressive but not designed;
- distinct reference families collapsing into the same macro-template with only palette changes.

## 7. Future score reporting

Future human review should report at least:

### Technical scores
- material/object integrity
- text correctness
- artifact cleanliness

### Aesthetic scores
- photography_art_direction
- graphic_design_authorship
- photo_design_integration
- typography_lettering_quality
- reference_distance
- originality_non_genericity

Then report:

- `personal_target_usable: true/false`
- `top_tier: true/false`
- `relative_gain_vs_baseline` separately if applicable.

Do not average Axis A and Axis B into one flattering number.

## 8. Authority hierarchy

For the personal aesthetic system:

1. explicit user absolute judgment;
2. calibrated reference-distance evaluation;
3. independent expert review under this calibrated rubric;
4. generic commercial usability as a secondary technical diagnostic only.

## 9. Current benchmark consequence

The replacement independent blind review remains preserved as evidence of generic commercial-readability judgment, but its `8/8 USABLE` and `2/8 TOP_TIER` conclusions are not accepted as personal-target approval.

The current benchmark remains blocked from Library Scale Gate and production promotion until correct unblinding and calibrated diagnosis are complete.
