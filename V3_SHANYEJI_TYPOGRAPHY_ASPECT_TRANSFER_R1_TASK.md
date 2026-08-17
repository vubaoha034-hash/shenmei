# V3 Shan Ye Ji Typography Aspect + Hierarchy Transfer R1

## Required starting state

Branch:
`v3-distillation-first-long-term-system-20260817`

Required human-review commit:
`97dfb2d036d12b6538e0e1d85ec6ddb468e0d9b1`

Before execution verify the branch contains that commit.

## Goal

Validate whether the Shan Ye Ji typography family can survive a major aspect-ratio and hierarchy change while keeping the approved provisional display-lettering asset fixed.

This is a controlled typography transfer. It is not a new lettering-generation experiment.

## Locked asset

Use the exact refined transparent `灶边味` display asset from R2.

Requirements:
- identity resolved from the prior receipt/SHA;
- alpha valid;
- no redraw;
- no vector tracing;
- no image generation;
- no glyph modification.

If the unique official asset cannot be resolved, return:
`TYPOGRAPHY_ASPECT_TRANSFER_SOURCE_UNRESOLVED`
and STOP.

## Single-variable transfer

Change only the production geometry / hierarchy:

- previous proof: 1080×1350
- new proof: 1080×1920 (9:16)

Do NOT scale the old 4:5 proof proportionally. Recompose from the approved typography mechanisms.

## Required hierarchy

First read:
- approved provisional `灶边味` display asset

Second read — live Chinese:
- `山野风味`
- `灶火现炒 · 趁热上桌`

Third read — optional live English, maximum two groups:
- `WOK HEI`
- `MOUNTAIN KITCHEN`

English may be omitted if its inclusion weakens the hierarchy. Omission must be recorded rather than treated as failure.

## Composition requirements

- maintain active whitespace, not empty leftover space;
- display title must dominate without being mechanically centered;
- subordinate text must visibly belong to the same composition rather than read like specification labels;
- no duplicate small live-text `灶边味` under the display asset;
- no semantic orange thread by default;
- no badge;
- no handwritten slogan;
- no brand/footer lockup;
- no photography;
- no food;
- no decorative illustration.

Background may remain a restrained dark neutral/deep-green field. Exact color is production-bound.

## Figma responsibilities

- place the locked display asset unchanged;
- create all functional copy as editable live text;
- establish grid, spacing, alignment, optical balance, and export;
- preserve exact copy correctness;
- do not author complex Chinese display lettering from zero.

## Output discipline

Exactly ONE formal proof:
`V3-SYJ_TYPOGRAPHY_ASPECT_TRANSFER_R1.png`

- 1080×1920
- hidden variants = 0
- no best-of-N
- no image generation
- no alternative formal layouts

A technically valid but aesthetically weak proof must be retained for human review. Do not silently replace it.

## Required receipt

Record:
- branch / HEAD;
- source display asset identity and SHA-256;
- Figma file key / page / frame;
- display asset node ID;
- live-text node IDs and exact copy;
- whether English was included or omitted;
- export dimensions / SHA-256;
- readback result;
- formal outputs count;
- hidden variants;
- image generation executed = NO;
- Figma redraw of display asset = NO;
- Scale Gate = NO;
- durable promotion = NO.

Upload the existing exported proof to an explicitly searchable `LIU_VISUAL_REVIEW` Drive folder and return both folder ID and output file ID.

## Human-review boundary

After export, STOP.

Do not claim aesthetic PASS, Typography Transfer validation, Golden status, or durable promotion.

Final state must be:
`TYPOGRAPHY_ASPECT_TRANSFER_R1_READY_FOR_HUMAN_PIXEL_REVIEW`
