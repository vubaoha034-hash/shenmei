# R1E-2 — FAILURE AND TYPOGRAPHY CAPABILITY BOUNDARY

Status: `FAIL_HARD / TYPOGRAPHY_CAPABILITY_MISMATCH`
Date: `2026-08-14`

## User absolute judgment

The user judged the final R1E-2 lettering result as:

> 非常丑非常丑。毫无设计感。

This is authoritative direct user evidence for the project quality gate.

## Independent review correction

R1E-2 must not be treated as a near-pass or a refinement candidate. The result remains far below the Mother Reference 05 in overall lettering quality, coherence, authority, and commercial finish.

## What improved technically

- Mother Reference 05 remained directly bound as actual pixels.
- The design stayed on one target vector direction.
- Two controlled refinement passes were used.
- The title remained editable vector geometry.
- No food, poster layout, ImageGen, alternate design, or Discovery mutation was introduced.

These technical successes do not imply aesthetic capability.

## What failed visually

### 1. System coherence
The four glyphs still do not read as one authored lettering system. Their terminals, stroke behavior, mass, and silhouette remain inconsistent.

### 2. Glyph construction
`今` remains an unstable stylized construction; `日` remains rigid and box-like; `现` carries more weight but still shows transformed-font residue; `烧` remains visually congested and over-authored.

### 3. Semantic over-literalization
Attempts to encode heat/fire through droplets, hooks, spikes, cuts, and dynamic gestures produced symbolic decoration rather than convincing stroke logic.

### 4. Capability mismatch
The current workflow asks Codex/Figma to perform expert Chinese display-lettering design through low-level vector point editing. The tooling can execute geometry but does not reliably provide the visual calligraphic/glyph-design judgment needed for reference-level lettering.

### 5. Refinement-on-bad-skeleton problem
Restricting all work to the same initial Noto Serif-derived skeleton prevented recovery after the starting structure proved unsuitable. Refinement polished the wrong foundation rather than creating a strong authored glyph system.

## Falsified assumption

The following assumption is now rejected:

> With direct pixel reference binding, a suitable starting font, and constrained sequential vector refinement, Codex + Figma can reach Mother-Reference-level Chinese display lettering.

Current evidence does not support this.

## Stop rule

Do not run R1E-3 as another vector-refinement pass.
Do not add more micro-rules to the same path.
Do not continue changing the same glyph nodes.
Do not enter Composition Proof or poster design.

## Architecture change required

Typography must become a specialized asset pipeline instead of a Figma-construction task.

Recommended next capability class:

`VISUAL SYNTHESIS LETTERING -> PIXEL QUALITY GATE -> VECTOR TRACE / CLEANUP -> FIGMA PRODUCTION`

Meaning:

1. Mother Reference pixels remain directly bound.
2. A visual-synthesis model generates only the exact lettering asset, not a poster.
3. Exact Chinese character correctness and absolute visual quality are reviewed from pixels.
4. Only a passing lettering image is vectorized/traced and cleaned.
5. Figma is used after visual quality exists, for production and layout—not as the primary glyph-design engine.

## Why this is not rule-bloat

This change does not add more style rules. It changes the capability route because the current route has been empirically falsified.

## Exit status

`R1E-2 = FAIL_HARD / TYPOGRAPHY_CAPABILITY_MISMATCH`

Next allowed step: a narrowly scoped typography recovery experiment using a different capability class. No poster, no food, no packaging, no Discovery changes.