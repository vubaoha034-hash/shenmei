# VPD Photo / Figma Pipeline Hardening V1 — Implementation and Migration Note

Status: `IMPLEMENTED_FORWARD_ONLY / FIRST_VALIDATION_NOT_RUN`

## Architecture

Future VPD controlled or formal commercial photo-design runs may opt into, and
future `FORMAL_COMMERCIAL_OUTPUT` classifications must use, this staged route:

`PHOTO_ONLY_RENDER -> FIGMA_COMPOSITION -> FINAL_EXPORT`

The image generator produces photographic source material. It does not produce
final Chinese or English titles, support copy, badges, footer copy, fake labels,
logo lockups, pseudo-copy, or placeholder gibberish. Figma is the approved
structured design surface for editable typography, spacing, hierarchy, grid,
photo/type integration, and export lineage.

This task does not perform the first run of that route.

## Machine-readable authority

- `contracts/vpd/PHOTO_ONLY_RENDER_CONTRACT_V1.json` defines the photo payload
  separation, `CHATGPT_ONLY` route boundary, prohibited raster text fields, and
  prohibited panel/banner/shadow shortcuts.
- `contracts/vpd/FIGMA_COMPOSITION_CONTRACT_V1.json` defines the editable title,
  support-copy, grid, integration, distinctiveness, and node-evidence contract.
- `contracts/vpd/COMMERCIAL_DESIGN_GATE_POLICY_V1.json` defines six independent
  gates and the non-compensating conditions for formal commercial classification.
- `schemas/commercial-design-provenance-receipt.v1.schema.json` defines the
  photo-render, Figma-composition, and final-export receipt bundle.
- `visual_memory/vpd_commercial_pipeline.py` performs deterministic structural
  and hash-chain validation without renderer, network, Figma, or export actions.

## Forward migration

1. Compile a dedicated `PHOTO_ONLY_RENDER` payload containing photographic
   controls and scene-derived type-safe-space requirements.
2. Validate it before rendering. A final typography field or
   `final_typography_in_render = true` fails closed.
3. Render only through the declared ChatGPT product-UI route and capture the
   source photo identity, hash, and dimensions.
4. Compose exact copy in Figma using editable text or editable vector nodes.
   Record the actual Figma file key, frame/node IDs, node geometry, copy, and
   source-photo hash. Use `UNKNOWN` only while evidence is genuinely unavailable;
   an `UNKNOWN` critical identity cannot pass formal commercial provenance.
5. Export from the recorded frame and bind the final export to the source photo
   and Figma composition receipt.
6. Run all six gates. Machine checks prove structure and traceability only;
   human review remains authoritative for typography quality, integration,
   distinctiveness, photography quality, and final pixel quality.

## Backward compatibility

The policy is forward-only. It does not rewrite, invalidate, or reclassify
Attempt 1, Attempt 2, their payloads, pixels, hashes, or historical receipts.
Historical raster typography is not relabeled as editable Figma design.

The global Visual Distillation Compiler V2 and VisualProgram V2 schema remain
unchanged. This project-level contract also does not override the repository's
separate V4.2 daily-brand route. No renderer infrastructure has been added.

## Attempt-2 status

Attempt 2 remains:

`ATTEMPT2_FAMILY_VALIDATION_FAIL / FAIL_WITH_STRONG_POSITIVE_MECHANISM_EVIDENCE`

The current task preserves that settlement as diagnostic evidence. It does not
promote Style Capsule V1.1 Candidate and does not claim that prior Attempt-2
outputs used Figma. The repository contains no authoritative Figma file key or
node IDs for the file named `VPD Attempt2 Typography Rebuild`; those values
remain `UNKNOWN` until a later formal evidence-ingestion run.

## Validation entry point

Focused validation:

`python -m pytest tests/visual_memory/test_vpd_photo_figma_pipeline_hardening_v1.py -q`

The focused suite checks contract/schema syntax, photo-only text prohibition,
missing-Figma rejection, complete photo-to-Figma-to-export binding, six-gate
enforcement, historical hashes, and absence of renderer/network infrastructure.

## Next action

`RUN_FIRST_FORWARD_PHOTO_ONLY_PLUS_FIGMA_COMPOSITION_VALIDATION`

Do not execute that action as part of pipeline hardening.
