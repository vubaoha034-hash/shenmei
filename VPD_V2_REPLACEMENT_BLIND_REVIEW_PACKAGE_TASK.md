# VPD V2 — Replacement Blind Review Package Task

Status: `FROZEN_RECOVERY_TASK`

## Objective

Repair the invalid human-review binding without regenerating any benchmark image.

Use exactly the eight original frozen VPD V2 benchmark primary outputs and prepare a review package whose blind identities cannot be confused with chat attachment display order.

## Required branch

`visual-program-distillation-v2-photography-design-20260814`

## Mandatory first read

Read completely:

- `VPD_V2_EVALUATION_INVALIDATION.md`
- original benchmark machine-integrity report and generation receipts
- original private blind mapping only as needed to verify that benchmark artifacts are the original frozen outputs; never expose mapping in the review package

## Hard constraints

- Generate ZERO new benchmark images.
- Modify ZERO original benchmark images except for non-destructive review packaging outside the actual image canvas.
- Do not change V2 compiler, capsules, prompts, output bytes, Discovery, or Scale Gate state.
- Do not use or reproduce invalid human scores.
- Do not expose condition mapping.

## Canonical blind files

Resolve exactly these existing files from Drive:

- `VPD2-R01.png`
- `VPD2-R02.png`
- `VPD2-R03.png`
- `VPD2-R04.png`
- `VPD2-R05.png`
- `VPD2-R06.png`
- `VPD2-R07.png`
- `VPD2-R08.png`

For each:

1. download/read canonical bytes;
2. verify against the original benchmark output hash ledger;
3. record SHA-256, width, height, MIME;
4. do not alter the canonical output.

## Review package

Create a new Drive folder:

`VPD_V2_REPLACEMENT_BLIND_REVIEW`

Place exactly:

1. the eight original PNGs copied with filenames preserved exactly as `VPD2-R01.png` ... `VPD2-R08.png`;
2. one contact sheet `VPD2_BLIND_CONTACT_SHEET.png`.

Contact sheet rules:

- deterministic grid;
- each tile labeled only with its blind ID (`R01`...`R08`) outside the image region;
- no style/condition/direct/V2/content-role information;
- image aspect ratios preserved without cropping;
- neutral background;
- no aesthetic modifications;
- no reordering ambiguity: row-major ascending R01 -> R08.

## Review manifest

Create private/non-mapping manifest:

`VPD_V2_REPLACEMENT_BLIND_REVIEW_MANIFEST.json`

Fields:

- package_status
- source_benchmark_id
- invalidation_commit
- image_count = 8
- for each blind_id: filename, sha256, width, height, mime, drive_file_id
- contact_sheet filename, sha256, width, height
- condition_mapping_exposed = false
- original_output_bytes_preserved = true
- new_benchmark_images_generated = false

Do not include private condition names.

## Fresh evaluator requirement

The replacement human review must occur in a fresh independent ChatGPT context that has NOT seen the condition mapping.

The fresh evaluator receives only:

- the eight correctly named blind files and/or the labeled contact sheet;
- the review rubric below.

Do not include any previous scores, verdict, diagnosis, Style A/B names, or condition mapping.

## Review rubric to hand to fresh evaluator

For every R01..R08, independently score 0-10:

- photography quality
- graphic-design quality
- photo/design integration
- food/material realism
- typography quality

Also classify:

- `USABLE` or `UNUSABLE`
- `TOP_TIER` true/false

Review at:

- thumbnail scale
- normal scale
- detail scale

The evaluator must state visible reasons, not infer hidden condition identity.

After reviewing all eight, freeze the review before unblinding.

## Stop state

After package creation, STOP.

Do NOT unblind.
Do NOT run another diagnosis.
Do NOT propose an ablation.
Do NOT enter Library Scale Gate.

Return:

# VPD V2 REPLACEMENT BLIND PACKAGE READY

Branch:
HEAD:
Canonical outputs verified: 8/8
New benchmark images generated: NO
Contact sheet:
Drive folder:
Manifest:
Condition mapping exposed: NO
Scale Gate allowed: NO

## 已完成什么

## 未完成什么

## Fresh-review instructions
