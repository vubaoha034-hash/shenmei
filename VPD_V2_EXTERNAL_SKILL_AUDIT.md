# VPD V2 External Skill Audit

Status: `PASS_WITH_REQUIRED_BOUNDARIES`
Date: 2026-08-14

## Sources reviewed

- OpenAI `imagegen` skill;
- `gc-minimal-zine-poster`;
- `taste-skill` / `imagegen-frontend-web`.

## Patterns worth keeping

### 1. Strong visual model does the visual synthesis

Proven image-generation skills route zero-to-one raster creation to the image model rather than manually rebuilding art through deterministic layout primitives.

VPD V2 matches this.

### 2. Reference images remain first-class inputs

OpenAI image-generation guidance explicitly labels input-image roles and supports reference images for style/composition/mood. High-value references should remain attached/visible when the generation path supports them.

VPD V2 keeps raw-pixel anchors.

### 3. Prompt compilation is compact

The zine skill compiles a concrete small set of pixel-producing dimensions: canvas, composition, image anchor, typography, color, texture, lighting and mood. It does not send governance architecture to the renderer.

VPD V2 analysis may be deep, but renderer compilation must stay thin.

### 4. Design dials / variation controls are valuable

Taste-skill uses small global dials such as variance, density and art-direction intensity rather than hundreds of independent rules.

VPD V2 should derive similar task-level controls from the causal map when useful, but should not force frontend-specific dials onto unrelated photography/design work.

### 5. Inspect actual outputs and make targeted changes

OpenAI imagegen guidance validates subject, style, composition, text accuracy and invariants after rendering, then iterates with a single targeted change.

VPD V2 must preserve this production behavior after the benchmark stage. A fixed benchmark can prohibit hidden retries, but normal production should allow traceable targeted iteration.

### 6. Anti-patterns should be specific and limited

Taste-skill's anti-slop lists are useful when they target known model defaults. They become harmful if promoted into universal aesthetic law.

VPD V2 keeps hard avoids task-specific and capped.

## Important difference

Existing visual skills usually solve a deliberately narrow product:

- one zine family;
- frontend comps;
- brand-kit boards;
- generic image generation/editing.

VPD V2 has a different objective: distill an unfamiliar high-quality reference into a reusable program.

Therefore VPD V2 necessarily needs deeper analysis than those generation skills, but that depth must remain upstream. The image renderer should still receive a compact recipe similar in spirit to successful existing skills.

## Failure condition

If VPD V2's deep analysis causes longer prompts, weaker creativity, or worse output than direct reference + short prompt, the additional analysis has failed to create value and must be reduced or recompiled rather than defended because it is sophisticated.
