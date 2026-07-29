---
name: restaurant-brand-aesthetic-gate
description: >
  Use after the Figma three-page proof and before ten-page expansion, and again before final
  delivery. It orchestrates the personal aesthetic critic, reference/rejected anchor comparison,
  brand evidence, AI artifact and portfolio continuity gates.
---

# Restaurant Brand Aesthetic Gate

## Mandatory reads

1. `skills/personal-aesthetic-critic/SKILL.md`;
2. `config/rubric.v1.json`;
3. `config/penalties.v1.json`;
4. `calibration/README.md`;
5. `calibration/anchors.json`;
6. `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`;
7. current strategy, DNA, asset and Figma manifests.

## Mission

Stop weak work before it expands. Generation completion is never a pass condition.

## Inputs

For the three-page gate:

- three exported proof pages;
- brief and strategy;
- reference anchors;
- rejected anchors;
- Figma manifest;
- actual dimensions.

For the ten-page gate:

- ten exported pages;
- all project records;
- per-page brand evidence;
- Figma manifest and node IDs.

## Evaluation sequence

### 1. Blind formal evaluation

Anonymize page order when comparing alternatives. Use `poster_design` dimensions:

- information hierarchy;
- typography;
- layout grid;
- color system;
- imagery quality;
- brand consistency;
- communication;
- originality and restraint.

### 2. Reference-anchor comparison

State concrete pairwise findings:

- closer to which positive/reference anchor and why;
- closer to which rejected anchor and why;
- which visual decisions create the difference;
- whether the work depends on explanation to appear good.

Never infer private taste when anchors are insufficient. Set `personal_fit` to `null`, but still provide qualitative comparison.

### 3. Brand-evidence gate

For each page answer:

> Apart from the logo and color, what visible evidence makes this page belong only to this brand?

Answers based only on color, logo or generic food photography fail.

### 4. AI-artifact gate

Reject:

- fake text;
- malformed product or packaging;
- copied ingredients;
- plastic material;
- false steam;
- impossible space or perspective;
- repeated generic mockup;
- full-page image-generator composition imported as design.

### 5. Portfolio-continuity gate

Check:

- one book, not isolated ads;
- shared tokens and components;
- at least four layout archetypes for ten pages;
- no identical layout more than twice consecutively;
- visual rhythm across light/dark, image scale and density;
- one conclusion per page;
- no fake professional metadata.

## Three-page pass threshold

All conditions are mandatory:

- technical total ≥ 78;
- information hierarchy ≥ 70;
- typography ≥ 70;
- layout grid ≥ 70;
- imagery quality ≥ 70;
- brand consistency ≥ 70;
- no fatal penalty or cap below 78;
- positive/reference similarity evidence exceeds rejected-anchor similarity evidence;
- concept engine remains visible in all three pages;
- Figma manifest contains real file URL and three frame node IDs.

If any condition fails:

`THREE_PAGE_PROOF_REJECTED`

Do not average away a blocking failure.

## Ten-page pass threshold

- every page passes text and structure inspection;
- no page is `REJECTED`;
- set average ≥ 80;
- no key page (01, 02, 04, 05, 08, 10) below 75;
- all ten frame node IDs and exports recorded;
- at least four layout archetypes;
- brand-evidence gate passes on all pages;
- no full-page image-generator result.

Only then may status become `CONCEPT_SET`.

## Output

Write `AESTHETIC_EVALUATION.json` and user-facing summary containing:

- blind ranking;
- formal score and confidence;
- reference and rejected-anchor comparisons;
- strongest evidence;
- largest limiters;
- exact edit order;
- pass/fail status;
- whether ten-page expansion is allowed.

## Hard rule

Do not soften a failed gate because substantial work has already been generated.
