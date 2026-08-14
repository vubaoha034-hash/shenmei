# VPD V1 — Controlled Execution Runner

Execute this runner on branch:

`visual-program-distillation-v1-20260814`

Do not modify production routes.

## 1. Mandatory reads

Read completely:

1. `VISUAL_PROGRAM_DISTILLATION_V1.md`
2. `VISUAL_DISTILLATION_COMPILER_CONTRACT_V1.md`
3. `schemas/visual-program.v1.schema.json`
4. `VPD_V1_ACCEPTANCE_PROTOCOL.md`
5. `VPD_V1_FIRST_RUN_PLAN.md`
6. `VPD_V1_STATIC_ACCEPTANCE.md`
7. `AESTHETIC_SKILL_DESIGN_CHARTER.md`

Do not substitute older R1D/R1E art-direction rules for this runner.

## 2. Freeze state

Verify:

- Discovery approved = 18;
- Discovery rejected = 12;
- no new evidence admission;
- no global taste-rule promotion;
- no production Skill rewrite;
- doctor() == [] before execution.

If these do not hold, stop and report the actual blocker.

## 3. Resolve style sources

### Capsule A

Reference:

`R1C-APPROVED-05.jpg`

Expected SHA-256:

`eedd32a428f7483fefc53b1f5107dc9a790b76db2e408b29917607c3fb030e38`

### Capsule B

Reference:

`R1C-APPROVED-13.jpg`

Resolve canonical bytes and record SHA-256.

Both must be actual raw visual inputs to distillation and later renderer conditioning.

## 4. Resolve transfer content assets

Need three materially different real content identities.

### CONTENT-1

May use the existing real R1 dish source:

`R1_SOURCE_REAL_DISH_6720x4480.jpg`

Known source lineage exists from the R1 real-photo-first test.

### CONTENT-2

Select a different real food/product content asset from the private Asset Vault.

Requirements:

- not generated solely for this benchmark;
- not the same dish/crop as CONTENT-1;
- not a Style A/B reference used as a positive visual anchor;
- resolvable raw bytes and SHA.

### CONTENT-3

Select a third materially different real food/product content asset.

Same requirements.

If CONTENT-2 and CONTENT-3 cannot be honestly resolved, STOP:

`BLOCKED_NEEDS_TRANSFER_CONTENT_ASSETS`

Do not create fake transfer content.

## 5. Distill Capsule A

Use `visual-distillation-compiler-v1` exactly.

Create:

`private-data/.../vpd-v1/capsules/VPD-A-RESTAURANT-FIRE-V1/visual_program.json`

Requirements:

- schema-valid;
- source absolute quality = USABLE;
- full raw visual anchor;
- observed evidence separated from inference;
- fixed invariants;
- degrees of freedom;
- source-specific do-not-transfer decisions;
- at least required transform operators;
- concrete failure boundaries;
- compact renderer contract.

Do not reduce Style A to color/object keywords.

## 6. Distill Capsule B

Without changing compiler code or global personal priors, create:

`private-data/.../vpd-v1/capsules/VPD-B-EDITORIAL-V1/visual_program.json`

Use the same schema and compiler version.

If Style B requires a new global exception or compiler edit, STOP:

`NEW_STYLE_REQUIRES_COMPILER_CHANGE`

That is a failed generalization test.

## 7. Capsule validation

Validate both capsules against:

`schemas/visual-program.v1.schema.json`

Also execute the compiler self-check in `VISUAL_DISTILLATION_COMPILER_CONTRACT_V1.md`.

Any failure -> `DISTILLATION_NOT_READY`.

## 8. Compile eight render tasks

Exactly:

- A0 Direct baseline
- A1 Capsule A + anchors
- A2 Capsule A FAMILY with different content
- A3 Capsule A TRANSFER
- B0 Direct baseline
- B1 Capsule B + anchors
- B2 Capsule B FAMILY
- B3 Capsule B TRANSFER

Follow `VPD_V1_FIRST_RUN_PLAN.md` for content identity assignment.

## 9. Renderer policy

Use the strongest available visual generation/editing model already available to this environment.

The creative renderer receives actual visual anchor pixels.

Do NOT use Figma or manual SVG/path construction as the zero-to-one creative renderer.

For each capsule condition:

- <= 8 high-leverage variables;
- <= 6 hard avoids;
- explicit freedom statement;
- no long system manifesto in the image prompt.

For direct baseline:

- raw reference pixels;
- content asset;
- short human-style instruction;
- same underlying renderer.

## 10. One render per condition

Exactly 8 primary images.

No best-of-N.
No retries for aesthetic weakness.
No alternate prompts after seeing results.

Technical invalidity such as missing attachment, corrupt output, or wrong renderer receipt must be marked separately and does not become aesthetic evidence.

## 11. Drive review package

Create/use:

`LIU_VISUAL_REVIEW/VPD_V1/`

Upload the eight primary images with neutral condition-obscuring filenames for blind review if practical.

Store private mapping separately.

Also save:

- capsule validation receipts;
- compiled renderer payloads;
- attachment/reference receipts;
- output hashes;
- condition mapping;
- machine integrity report.

Do not place private mapping in the user-visible review folder.

## 12. Codex review boundary

Codex may report:

- machine integrity;
- schema validity;
- exact reference binding;
- text/attachment facts;
- provenance.

Codex must NOT declare aesthetic PASS or choose a winner.

Independent ChatGPT/user pixel review is required.

## 13. Final response

Return exactly:

# VPD V1 BENCHMARK READY

Branch:
HEAD:
Discovery approved:
Discovery rejected:
Compiler version:
Capsule A schema:
Capsule B schema:
Style B required compiler change:
CONTENT-1:
CONTENT-2:
CONTENT-3:
Primary outputs created:
Additional outputs created:
Direct baselines:
Capsule conditions:
Raw visual anchors bound:
Figma used as creative renderer:
Drive folder:
Machine integrity:
Independent pixel review:
VPD status:

## 已完成什么

## 未完成什么

## 是否证明了换风格无需重写系统

Hard requirements if ready:

- Primary outputs created = 8
- Additional outputs created = 0
- Direct baselines = 2
- Capsule conditions = 6
- Raw visual anchors bound = YES
- Figma used as creative renderer = NO
- Independent pixel review = PENDING

If transfer assets are insufficient, return instead:

# VPD V1 BLOCKED

exact_blocker: BLOCKED_NEEDS_TRANSFER_CONTENT_ASSETS

and list which content identities are available/missing.

STOP after the report.
