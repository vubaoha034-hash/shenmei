# VPD V1 — First Real Run Plan

Status: `READY_FOR_CONTROLLED_EXECUTION`

## 1. Goal

Prove the user's actual requirement:

> After an excellent work is distilled, the system knows how to make new works using the same design logic without simply cloning the original. When given a different style later, the same system can distill that new style without forgetting how to work.

This run is not a retrieval benchmark and not a single-reference imitation contest.

## 2. Freeze global state

During this run:

- Discovery remains frozen at approved 18 / rejected 12;
- no new global taste rules;
- no Skill promotion;
- no production router switch;
- no R2 / packaging expansion;
- no Figma zero-to-one creative construction;
- rejected images remain evaluator/failure anchors, not positive renderer attachments.

## 3. Capsule A

### Source style

`R1C-APPROVED-05.jpg`

Known Drive file id:

`1M2sI6Q1TfPszHpORj29eY9sr-JDO3Co9`

Known SHA-256:

`eedd32a428f7483fefc53b1f5107dc9a790b76db2e408b29917607c3fb030e38`

### Why A

It represents a high-impact commercial restaurant family with strong culinary-action energy, food/heat/chili relationships, and assertive title behavior.

### Required capsule output

`VPD-A-RESTAURANT-FIRE-V1`

The capsule must include raw-pixel anchors plus design grammar, degrees of freedom, transformation operators, and failure boundaries.

It must not reduce to:

`black + red + chili + fire`.

That would be surface imitation, not program distillation.

## 4. Capsule B

### Source style

`R1C-APPROVED-13.jpg`

Known R1C Drive file id:

`1vF1pKZHnMUJzEDdlh77jngM9Wc5Z4x4H`

### Why B

It is materially different from Capsule A in visual density, breathing room, display-type relationship, vessel/image placement, palette behavior, and editorial tone.

### Required capsule output

`VPD-B-EDITORIAL-V1`

The compiler version and global personal priors must be exactly the same as for Capsule A.

No Style-B-specific compiler change is allowed.

## 5. Visual anchor rule

For both capsules:

- canonical full reference is preserved as a raw-pixel anchor;
- up to three diagnostic crop anchors may be created only if they isolate genuinely distinct design evidence such as typography behavior, composition, or material texture;
- crops must preserve provenance to the source SHA;
- no contact sheet is used as renderer conditioning;
- visual anchors are first-class inputs, not merely documentation.

## 6. Distillation step

For each capsule, generate one schema-valid `visual_program.json`.

Distillation must explicitly answer:

### Observed evidence

What is directly visible?

### Design grammar

What relationships create the visual effect?

### Fixed invariants

What must remain for a new work to stay in the family?

### Degrees of freedom

What should change from work to work?

### Transformation operators

How do subject, aspect ratio, palette, density, motif, typography, and material change without collapsing the family?

### Failure boundaries

What would turn the result into a generic template or literal copy?

## 7. Renderer role

Use the strongest available visual generation/editing model as the creative renderer.

Do not use Figma/Codex path editing as the primary visual synthesis method.

Figma may be used only after an output is independently judged worth producing.

## 8. Prompt compiler constraint

For every generated output, compile the capsule into a compact instruction containing:

- task/content facts;
- actual visual anchors;
- mode;
- no more than 8 high-leverage visual variables;
- no more than 6 task-relevant hard avoids.

Do not serialize the full capsule into a long prose manifesto.

## 9. First benchmark conditions

### A0 — Direct baseline

Reference 05 raw pixels + content asset + short instruction -> visual renderer.

No capsule.

### A1 — Distilled reconstruction/family entry

Capsule A + raw visual anchors + same content asset -> renderer.

Goal: prove the capsule does not degrade the direct path.

### A2 — Family reuse

Capsule A + a different real food/content asset -> renderer in `FAMILY` mode.

Goal: same design family, new content, not same composition.

### A3 — Transfer

Capsule A + materially different restaurant product/content -> renderer in `TRANSFER` mode.

Goal: preserve hierarchy/tension/semantic derivation while allowing surface changes.

### B0 — Direct baseline

Reference 13 raw pixels + content asset + short instruction -> renderer.

### B1 — Distilled reconstruction/family entry

Capsule B + raw visual anchors + same content asset -> renderer.

### B2 — Family reuse

Capsule B + different content -> `FAMILY`.

### B3 — Transfer

Capsule B + materially different product/content -> `TRANSFER`.

## 10. Content asset requirement

Do not fake transfer with tiny crop/color changes of the same source image.

The run requires at least three content identities:

- `CONTENT-1`: may use the existing real R1 dish source;
- `CONTENT-2`: must be a different real food/product source;
- `CONTENT-3`: must be materially different from CONTENT-1 and CONTENT-2.

If the private Asset Vault does not contain CONTENT-2/3, stop with:

`BLOCKED_NEEDS_TRANSFER_CONTENT_ASSETS`

Do not substitute generated fake food merely to complete the benchmark.

## 11. Output count

Exactly 8 primary benchmark outputs.

One render per condition for the first run.

No best-of-N and no retry after seeing visual quality.

If renderer produces a technical corruption or wrong attachment, mark technical invalid separately; do not count it as aesthetic evidence.

## 12. Independent review

Each output is reviewed on actual pixels for:

- `USABLE / UNUSABLE`;
- fidelity to design grammar;
- non-copy behavior;
- transfer success;
- AI/material defects;
- distance from direct baseline.

The user may override any positive machine/assistant aesthetic assessment.

## 13. What proves success

Success is not `A1 looks like Reference 05`.

Success is:

1. A1 retains the high-quality direct path;
2. A2 feels like another legitimate member of A's family without copying A's exact page;
3. A3 still carries higher-order design logic after a major content change;
4. the same compiler creates B, which remains distinctly B rather than converging toward A;
5. B2/B3 work without changing global rules.

## 14. What proves failure

Immediate architectural failure if:

- capsule-only text dominates and raw visual evidence is no longer used;
- A and B converge to one generic house style;
- direct baseline beats capsule condition badly in both styles;
- family mode merely replays the source composition;
- transfer mode loses all recognizable design logic;
- Style B requires compiler rule changes;
- a relative-only/rejected output becomes a positive anchor.

## 15. Exit states

### `VPD_V1_PROMOTION_CANDIDATE`

All acceptance gates in `VPD_V1_ACCEPTANCE_PROTOCOL.md` pass.

### `VPD_V1_NOT_PROMOTED`

Architecture or quality gate fails.

### `BLOCKED_NEEDS_TRANSFER_CONTENT_ASSETS`

Insufficient real content assets to test reuse/transfer honestly.

## 16. After PASS only

Only after promotion candidate status may the project consider:

- compiling more approved styles into capsules;
- task-aware capsule selection;
- capsule composition/fusion research;
- automating capsule creation;
- integrating capsule use into normal visual Skill routing.

Do not bulk-distill 18 approved references before this benchmark passes.
