# V3 Route A — Visual Validation Package Task

Status: `FROZEN_UPLOAD_ONLY`

Repository: `vubaoha034-hash/shenmei`
Required branch: `visual-program-distillation-v2-photography-design-20260814`

## Purpose

Expose the already-generated Route A artifact for independent pixel review. This task does not generate, edit, resize, crop, recompress, re-render, score, or reinterpret the artwork.

## Exact artifact

Existing output:
- `V3-A_STRUCTURE_LOCKED_BRAND_WORLD.png`
- expected dimensions: `1024x1536`
- expected SHA-256: `3344a127bc8a696cd83a53bc136873e0b7d6528048f30d8f9d0d87d8b6eb7c82`

## Required actions

1. Locate the exact existing PNG produced by the completed V3 Structure-Locked Reconstruction Route A run.
2. Verify its SHA-256 equals exactly:
   `3344a127bc8a696cd83a53bc136873e0b7d6528048f30d8f9d0d87d8b6eb7c82`
3. Verify PNG readability and `1024x1536` dimensions.
4. If SHA or dimensions do not match, return `V3_A_ARTIFACT_IDENTITY_FAILURE` and STOP.
5. Upload the exact bytes, unchanged, to Google Drive folder:
   `LIU_VISUAL_REVIEW/V3_STRUCTURE_LOCKED_VALIDATION`
6. Preserve filename exactly:
   `V3-A_STRUCTURE_LOCKED_BRAND_WORLD.png`
7. Upload the canonical Mother Reference 05 to the same folder only if not already directly available there, preserving its canonical bytes and filename:
   `R1C-APPROVED-05.jpg`
8. Create `V3_A_VISUAL_VALIDATION_MANIFEST.json` containing:
   - artifact filename
   - Drive file id
   - SHA-256
   - dimensions
   - Mother Reference filename / Drive id / SHA
   - `regenerated: false`
   - `edited: false`
   - `resized: false`
   - `aesthetic_score_by_codex: null`
9. Do not upload Route B fake/placeholder output. Route B remains `SOURCE_MISMATCH_FOR_ROUTE_B`.

## Prohibited

Do NOT:
- regenerate Route A;
- make a variant;
- fix typography;
- edit pixels;
- crop/resize/recompress;
- run best-of-N;
- score aesthetics;
- call Route A visually successful;
- change Route B gate;
- run Library Scale Gate;
- modify Discovery;
- modify the compiler.

## Final response

Return only:

# V3 A VISUAL VALIDATION PACKAGE READY

Branch:
HEAD:
Artifact SHA verified:
Artifact dimensions:
Drive folder:
Artifact Drive id:
Mother Reference 05 Drive id:
Regenerated: NO
Edited: NO
Route B status: SOURCE_MISMATCH_FOR_ROUTE_B
Scale Gate executed: NO

Then STOP.
