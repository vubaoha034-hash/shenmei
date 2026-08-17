# V3 Shan Ye Ji Display Lettering Source Validation R1 Task

Status: `AUTHORIZED / HUMAN_REVIEW_BOUND`

This task begins only from a branch that contains:

- `207450b8f7a3d7550879e583e0751ed10f7e747c`
- `d588f92f79bca590f4b5f1f081d50526f4210dcc`

## Purpose

Test only the missing **Display Lettering Source Pipeline** for the Shan Ye Ji Typography-only family candidate.

This is not a full poster generation task.
This is not Typography Transfer validation.
This is not Figma final production.

The isolated question is:

> Can `SPECIALIZED_VISUAL_SYNTHESIS_TO_APPROVED_ASSET` create a genuinely new, exact, readable Chinese display-lettering asset for the locked copy `灶边味` while transferring the evidence-backed landscape/stone/block visual mechanism without copying the source `山野集` glyph geometry?

## Mandatory reads

Read:

1. `V3_TYPOGRAPHY_SHANYEJI_HUMAN_REVIEW_RESULT.md`
2. `V3_TYPOGRAPHY_EVIDENCE_SHANYEJI.json`
3. `V3_TYPOGRAPHY_HYPOTHESIS_SHANYEJI.json`
4. `V3_DISPLAY_LETTERING_SOURCE_PIPELINE_CONTRACT.json`
5. `schemas/display-lettering-source-pipeline.v3.schema.json`
6. `V3_TYPOGRAPHY_FIGMA_PRODUCIBILITY_SHANYEJI.json`
7. official OpenAI imagegen Skill instructions used by this repository/workflow

Do not reinterpret the historical failed Figma-first path as permission to draw new Chinese lettering manually in Figma.

## Preflight

Resolve and SHA-verify the canonical Shan Ye Ji source:

- asset: `ast_d9e80019-544f-4c0c-9b8d-cc04541ff0ed`
- SHA-256: `9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414`

If exact pixels cannot be resolved, STOP:

`SHANYEJI_DISPLAY_SOURCE_VALIDATION_CANONICAL_REFERENCE_UNAVAILABLE`

Run private store integrity/doctor checks. Raw evidence and Discovery must remain unchanged.

## Locked source route

Use exactly:

`SPECIALIZED_VISUAL_SYNTHESIS_TO_APPROVED_ASSET`

Do not execute the other two source routes in R1.

## Locked copy

The only display text to generate is:

`灶边味`

No other Chinese or Latin copy may appear inside the candidate assets.

This string is a validation string only. It is not a brand naming decision.

## Renderer

Use the official OpenAI imagegen Skill and built-in `image_gen` route.

- CLI fallback: forbidden.
- Figma zero-to-one title construction: forbidden.
- Manual Codex vector tracing: forbidden.

Attach the canonical Shan Ye Ji reference only as visual-mechanism grounding.
Do not attach Reference 05, Reference 13, older V2/V3 generated outputs, or other typography references.

## What to transfer

Target these behavior-level mechanisms:

- one combined landscape-like display silhouette;
- unequal but controlled glyph mass;
- carved/constructed negative-space cuts;
- block / stone / mountain-like structural deformation;
- selective erosion or missing-stroke geometry;
- strong white/light display mass suitable for later placement over a dark photographic field;
- character identity must remain legible.

## What must NOT transfer

Do not copy:

- exact `山野集` glyph outlines;
- exact missing-stroke locations;
- exact central coordinates;
- orange path;
- orange badge;
- top English claims;
- handwritten slogan;
- WANCE footer/brand lockup;
- exact forest crop or full-page composition.

The candidate must be an isolated lettering asset, not a miniature reconstruction of the source poster.

## Candidate count

Create exactly **3 formal visible candidates**:

- `V3-SYJ_DISPLAY_SOURCE_R1_A.png`
- `V3-SYJ_DISPLAY_SOURCE_R1_B.png`
- `V3-SYJ_DISPLAY_SOURCE_R1_C.png`

No hidden variants.
No private best-of-N selection.
All three outputs must be preserved for human review.

Each formal candidate requires its own generation/provenance receipt.

Technical retry is allowed only if a call returns no valid image bytes or is otherwise technically invalid. A technically valid but aesthetically weak or text-incorrect candidate is preserved as failure evidence and is not silently replaced.

## Canvas / asset presentation

Prefer an isolated asset presentation:

- transparent background if the built-in route reliably supports it;
- otherwise use a simple flat neutral dark background with no decorative scene;
- generous margin around the lettering;
- no extra text;
- no poster mockup;
- no badge / line / logo / footer.

The goal is to judge the lettering source itself.

## Hard correctness gate

For every candidate record:

- exact requested copy: `灶边味`
- visually observed character correctness: PASS / FAIL
- if uncertain: FAIL

A candidate with incorrect Chinese characters cannot become an approved display asset even if visually attractive.

Do not use OCR as the primary validator. Human-readable pixel review remains required.

## Technical receipts

For each candidate record at least:

- source route
- canonical reference asset/sample ID and SHA
- exact locked copy
- renderer mode
- tool / model provenance available from runtime
- output filename
- output SHA-256
- dimensions
- formal call count
- technical retries
- hidden variants = 0
- copy correctness status
- `approved_asset_status = HUMAN_REVIEW_PENDING`

## Drive review package

Create one review folder containing:

- canonical Shan Ye Ji reference image;
- candidate A;
- candidate B;
- candidate C;
- all three receipts;
- a small manifest with filenames + SHA-256.

Do not include unrelated historical outputs.

## Human review only

Codex must not assign aesthetic PASS, family PASS, Typography Transfer PASS, or approved asset status.

After all valid formal outputs and receipts are uploaded, STOP.

## Forbidden in this task

- full poster generation;
- Figma final composition;
- typography transfer execution;
- content swap;
- composition/aspect transfer;
- Scale Gate;
- durable promotion;
- Discovery mutation;
- raw evidence mutation;
- promoting orange thread / English claims / badge / slogan based on this source test;
- copying exact source glyphs.

## Final response format

Return only:

# V3 SHANYEJI DISPLAY LETTERING SOURCE R1 READY FOR HUMAN PIXEL REVIEW

Branch:
HEAD:
Starting review commit verified:
Canonical Shan Ye Ji asset verified:
Source route:
Locked test copy:
Candidate A:
Candidate B:
Candidate C:
Imagegen skill used:
Renderer mode:
CLI fallback used:
Total formal outputs:
Hidden variants:
Technical retries:
Drive folder:
Candidate A receipt:
Candidate B receipt:
Candidate C receipt:
Typography Transfer validated: NO
Figma final composition executed: NO
Scale Gate executed: NO
Durable promotion executed: NO
Discovery modified: NO
Raw evidence modified: NO
Git working tree:

## 已完成什么

## 未完成什么

## 需要人工验收什么

Then STOP.
