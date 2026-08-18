# V3-A R3A — Narrow Codex Render Bridge Task

Status: `ADMISSIBLE_NEXT_TECHNICAL_TASK / AESTHETIC_AUTHORITY_FORBIDDEN`

Repository: `vubaoha034-hash/shenmei`
Working branch: `vpd-v3-cinema-dna-integration-audit-20260818`
Production branch to protect: `visual-program-distillation-v2-photography-design-20260814`
Production branch frozen HEAD at experiment start: `40bf943d1e9b3f2e1d514a2d0b1d5c3b5d402368`

## Why Codex is now admissible

Direct visual routes have been exhausted or technically invalid:

1. Adobe instruct-edit route: blocked by account connection/auth failure.
2. Native ImageGen selective edit attempt: technically invalid because the renderer regenerated a new landscape scene, changed geometry/identity, and returned `1536x1024` instead of the required `1024x1536`.
3. Figma Weave route: unavailable because Figma is not linked to Weave.

Therefore Codex may now be used only for a transport/execution bridge that can prove exact source binding and output verification.

This does **not** authorize Codex to perform aesthetic judgment, redesign the poster, change VPD architecture, or promote R3A.

## Inputs

Canonical visual source location:

- Figma file key: `XZPhanfxH1JWUPsOoxt0zp`
- node: `3:8`
- expected dimensions: `1024x1536`
- role: `V3-A R3A clean base`

Previous external handoff identity recorded in production evidence:

`V3-A_R3A_CLEAN_BASE_LOCAL.png`

SHA-256:

`15ecb2901de7588771905663a8eedbe48979819b87b952cb418f075f97a54612`

Do not assume a fresh Figma export is byte-identical to this earlier handoff. Compute and record the exact SHA-256 of the bytes actually used for the bridge run.

Experimental renderer instruction:

`V3_A_R3A_CINEMA_DNA_BOUNDED_PATCH_V1.md`

Invalid native attempt evidence:

`V3_A_R3A_NATIVE_IMAGEGEN_ATTEMPT1_INVALID_20260819.md`

## Objective

Implement the thinnest possible technical path:

`exact input PNG -> actual image-edit operation -> exact output PNG -> deterministic verification`

The bridge is successful only if it can demonstrate that the edit runtime received the intended source image as an edit input, not merely as text/context/reference for full regeneration.

## Allowed work

Codex may:

1. export/materialize the exact Figma node if a supported authenticated route exists;
2. compute SHA-256, MIME, dimensions and decoded-image metadata;
3. discover whether the current runtime/environment exposes a genuine image-edit endpoint/tool capable of source-image editing;
4. create a minimal one-shot script/wrapper for that edit endpoint if credentials and API access already exist;
5. submit exactly one edit request using the bounded patch text;
6. save exactly one returned output candidate if the operation is genuinely source-bound;
7. compute output SHA-256, MIME and dimensions;
8. run deterministic structural sanity checks that do **not** pretend to judge taste, such as:
   - exact orientation/dimensions;
   - global registration feasibility;
   - coarse edge/layout preservation outside intended focal edit regions when technically possible;
   - left-rail occupancy and large structural silhouette stability when measurable without semantic invention;
9. write a technical result/manifest into this audit branch.

## Forbidden work

Codex must not:

- change the active production branch;
- rewrite the VPD V3 architecture or six-control patch;
- generate multiple aesthetic variants;
- choose the “best-looking” output;
- change `现烧`, composition, typography, brand language or layout;
- declare `R3A PASS`;
- declare `COMMERCIAL_QUALITY_PASS`;
- promote Golden Exemplar;
- run Scale Gate;
- hide failed attempts;
- use a text-to-image fallback and call it an edit;
- crop/resize a landscape regeneration into portrait merely to satisfy dimensions;
- fabricate tool/API availability or credentials.

## Runtime discovery rule

Before writing integration code, inspect the actual environment for an edit-capable runtime.

Acceptable examples include a genuine image-edit API/tool with source-image input semantics.

If no such runtime/credential exists, STOP with:

`V3_A_R3A_CODEX_BRIDGE_BLOCKED_NO_EDIT_RUNTIME`

and record what was checked.

Do not build an elaborate framework around a missing renderer.

## One-shot execution budget

- formal image candidates: exactly `1` maximum
- hidden variants: `0`
- aesthetic retries: `0`
- technical retries: at most `1` for transport/auth/transient failure only

If the first returned image is clearly a whole-image regeneration or wrong orientation, mark it technical invalid and stop. Do not retry aesthetically.

## Required output names

If a valid source-bound edit is returned:

`V3-A_R3A_ART_REALISM_CANDIDATE_01.png`

Technical manifest:

`V3_A_R3A_CODEX_RENDER_BRIDGE_RESULT.md`

Optional machine-readable manifest:

`V3_A_R3A_CODEX_RENDER_BRIDGE_MANIFEST.json`

## Required technical manifest fields

Record:

- exact repository branch and HEAD before execution;
- Codex/runtime version where observable;
- edit runtime/tool actually used;
- whether source image bytes were explicitly supplied to the runtime;
- exact input filename;
- input SHA-256;
- input MIME;
- input dimensions;
- prompt source file and prompt hash if convenient;
- number of API/tool calls;
- technical retry count;
- output filename if any;
- output SHA-256 if any;
- output MIME if any;
- output dimensions if any;
- source-bound edit confirmed: `YES/NO`;
- whole-image regeneration detected: `YES/NO`;
- technical verdict.

## Technical verdicts

Use exactly one:

- `R3A_CODEX_BRIDGE_VALID_CANDIDATE_READY_FOR_HUMAN_REVIEW`
- `R3A_CODEX_BRIDGE_TECHNICAL_INVALID`
- `V3_A_R3A_CODEX_BRIDGE_BLOCKED_NO_EDIT_RUNTIME`
- `V3_A_R3A_CODEX_BRIDGE_BLOCKED_AUTH`

## Human authority boundary

Even if the bridge produces a technically valid source-bound candidate, Codex must stop before aesthetic promotion.

The main project/human review must decide:

- food realism improvement;
- appetite preservation;
- garnish/particle restraint;
- photographic coherence;
- identity/composition preservation;
- R3A PASS or FAIL.

## 已完成什么

- direct renderer failures have been isolated and recorded;
- Codex admission condition is now satisfied for a narrow engineering bridge only;
- exact source location, patch, invalid attempt and output budget are frozen;
- technical/human authority boundaries are explicit.

## 未完成什么

- Codex bridge has not yet been executed;
- no valid source-bound R3A candidate exists;
- no R3A human review exists;
- R3B, Commercial Quality, Golden and Scale remain blocked.
