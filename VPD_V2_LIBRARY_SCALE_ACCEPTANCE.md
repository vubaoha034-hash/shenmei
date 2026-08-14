# VPD V2 — Library Scale Acceptance Gate

Status: `REQUIRED_BEFORE_BULK_INGESTION_OR_PRODUCTION_PROMOTION`

## 1. Purpose

Prove that a large restaurant-reference library improves evidence quality without increasing active generation complexity or collapsing distinct styles into one average.

This gate is independent from the 8-output visual-quality benchmark.

## 2. Required test corpus structure

Use a representative staged corpus containing:
- multiple coherent restaurant visual families;
- exact duplicates;
- near-duplicates/crops/exports;
- repeated images from the same campaign/source;
- materially different styles;
- whole-image positive judgments;
- at least some component-specific positive/negative judgments;
- contradiction cases where two liked images use opposite mechanisms.

Do not bulk-import the full private library merely to run the gate.

## 3. Test A — Duplicate amplification resistance

Procedure:
1. Select one coherent family.
2. Record its routing weight, family signature, capsule size, exemplar set and renderer payload.
3. Add many duplicate/near-duplicate copies of the same evidence.
4. Recompute library state.

PASS only if:
- duplicates are grouped/quarantined as redundant evidence;
- no duplicate-derived new rules are added;
- renderer payload does not grow materially;
- unrelated task routing does not shift materially solely because of duplicate count.

## 4. Test B — New-family isolation

Procedure:
1. Start with an established visual family.
2. Add a clearly different high-quality restaurant style.

PASS only if:
- the system creates/suggests a new family or explicit controlled fusion;
- the established capsule is not silently averaged toward the new style;
- the new style does not modify unrelated fixed invariants.

## 5. Test C — Component approval integrity

Procedure:
Use examples where photography is strong but typography/layout is weak, and vice versa.

PASS only if:
- whole-image `LIKED` does not automatically promote all subsystems;
- component evidence remains scoped;
- weak typography is not learned as positive merely because the photograph was liked;
- weak photography is not learned as positive merely because the layout was liked.

## 6. Test D — Contradiction preservation

Procedure:
Add two absolutely liked examples whose visible mechanisms conflict, such as:
- dense vs sparse layout;
- warm vs cool palette;
- shallow vs deep focus;
- maximal vs restrained typography.

PASS only if:
- the system preserves both as style-local possibilities or separate families;
- it does not average them into a vague global rule;
- no cross-style personal prior is promoted without independent recurrence.

## 7. Test E — Active-context boundedness

Measure before and after staged library growth:
- number of renderer reference attachments;
- number of high-impact controls;
- number of hard avoids;
- active capsules per task;
- compiled prompt length/structure;
- global priors loaded.

PASS only if per-task active context remains bounded by policy and does not scale with raw image count.

## 8. Test F — Quality non-regression

Freeze a small benchmark task set and compare:
- pre-growth library snapshot;
- post-growth library snapshot.

Use the same renderer/model and same task inputs.

PASS only if additional library evidence does not systematically reduce absolute visual quality or increase family-confusion failures.

If quality regresses, investigate:
- duplicate overweighting;
- wrong family routing;
- family merge contamination;
- component-label contamination;
- cross-style prior contamination;
- prompt/context expansion.

Do not fix by adding generic rules first.

## 9. Test G — Coverage benefit

Large libraries must provide positive value, not merely avoid damage.

PASS requires at least one demonstrated benefit attributable to increased independent evidence, such as:
- more accurate family identification;
- better tolerance/variation envelope;
- stronger transfer to unseen content;
- better selection of family-level visual anchors;
- improved confidence calibration;
- reduced false global-prior promotion.

## 10. Promotion rule

Bulk ingestion or production promotion is BLOCKED unless all scale tests pass.

Valid states:
- `SCALE_GATE_PASS`
- `SCALE_GATE_FAIL_DUPLICATE_AMPLIFICATION`
- `SCALE_GATE_FAIL_FAMILY_COLLAPSE`
- `SCALE_GATE_FAIL_COMPONENT_CONTAMINATION`
- `SCALE_GATE_FAIL_CONTEXT_GROWTH`
- `SCALE_GATE_FAIL_QUALITY_REGRESSION`
- `SCALE_GATE_FAIL_NO_COVERAGE_BENEFIT`

## 11. Core invariant

The desired behavior is:

> More images increase evidence and coverage; they do not proportionally increase rules, prompt size, active references, or style averaging.

Raw-library growth and active-generation complexity are deliberately decoupled.
