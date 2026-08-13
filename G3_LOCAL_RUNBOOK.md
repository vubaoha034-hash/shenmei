# G3 — LOCAL 3×3 CAPABILITY DIAGNOSTIC RUNBOOK

Status: `READY_AFTER_PRESTART_CHECKS`

## 1. Checkout and base verification

Use branch:

`g3-3x3-capability-diagnostic-20260813`

Requirements:

- working tree clean;
- base commit `d2ecc48c4d0fd3fa80b57f9ae7309123a751a3b8` is an ancestor;
- G2 is recorded as `G2_PASS` in private operations state;
- `doctor() == []`;
- Discovery still approved 18 / rejected 12;
- PHASE 10 Attempt 2 remains paused.

Do not modify `main`.

## 2. Run tests before generation

Run the full visual-memory verification suite.

Requirements:

- all G2 generation-bridge tests pass;
- reference-binding direct-attachment tests pass;
- prompt-preservation blocker tests pass;
- quality-gate fail-closed tests pass;
- compile checks pass.

Any failure blocks G3 before image generation.

## 3. Lock the public task set

Read exactly:

`G3_DIAGNOSTIC_TASKS.json`

Record the file SHA-256 in the private G3 pre-registration receipt.

Do not edit task wording after any request is rendered.

## 4. Build all nine requests before seeing outputs

For all three tasks, prepare all three conditions before rendering the first image.

### Baseline

Use the current G2-corrected normal chain with no historical Personal Context.

### Personalized

Use the same chain plus the frozen restaurant ContextPack.

Requirements:

- positive references are direct independent attachments;
- attachment identity matches canonical assets;
- rejected references are not ordinary image attachments;
- reference binding classifies `MULTIMODAL_BOUND` before render.

### Expert Direct

Bypass the current restaurant Prompt Compiler.

Before rendering, create and lock one concise prompt per task using only 5–8 high-leverage imageable variables plus mandatory correctness/realism constraints.

Do not use Personal Context.

Do not default to generic Chinese-restaurant style tokens.

Save prompt text and SHA privately before any G3 output exists.

## 5. Prompt preservation and renderer receipts

Before each Baseline or Personalized render, mandatory G2 prompt invariants must pass.

For every request save:

- task ID;
- opaque condition token;
- prompt SHA;
- route;
- Skill blob SHA where applicable;
- reference attachment identity/hashes;
- renderer/tool exposed identity;
- exposed request parameters;
- provider-unavailable fields explicitly marked `UNAVAILABLE_BY_PROVIDER`.

Do not guess hidden provider fields.

## 6. Hidden mapping and render order

Before rendering:

- randomly map the three real conditions to `X`, `Y`, `Z` independently for each task;
- store mapping only in the private G3 blind ledger;
- generate a private randomized render order across the nine locked requests.

User-visible filenames must contain only task ID and X/Y/Z.

Do not expose Baseline/Personalized/Expert Direct labels before all user judgments lock.

## 7. One-shot generation

Exactly one render per task-condition request.

No:

- visual-quality retry;
- best-of-N;
- retouch;
- prompt repair after seeing an image;
- extra references;
- selective regeneration.

If image bytes are returned, the render counts even when ugly.

A genuine provider/tool failure with no image bytes is recorded as technical failure and not confused with bad quality.

## 8. Machine Integrity Gate

Every returned image must pass file checks:

- readable bytes;
- true MIME/extension consistency;
- dimensions;
- aspect ratio;
- output hash;
- no corruption.

A machine-integrity failure is not repaired silently.

## 9. Google Drive review package

Create/use:

`LIU_VISUAL_REVIEW/G3/`

Upload only anonymous review images:

- `G3-D01-X.*`
- `G3-D01-Y.*`
- `G3-D01-Z.*`
- ... through `G3-D03-Z.*`

Do not upload prompts, mappings, condition labels, private IDs or receipts into the user-visible review folder.

Actual extension must match actual bytes.

## 10. Independent Pixel Gate

After all nine images are uploaded, stop generation.

An independent ChatGPT reviewer retrieves the actual Drive files and inspects real pixels.

For each output the reviewer records, while keeping the result hidden from the user's ranking until voting locks:

- food/material realism where applicable;
- structural plausibility;
- natural irregularity;
- specular/oil behavior;
- contact/shadow;
- heat/steam coherence where applicable;
- generic-template collapse;
- obvious AI material;
- task compliance;
- design-system coherence.

Reviewer result:

- `PASS_FOR_USER_REVIEW`
- `REJECTED_BELOW_FLOOR`

A rejected image is not regenerated.

## 11. User blind judgment

Only after all nine files are ready and mapping remains hidden, present task trios X/Y/Z.

For each image the user must mark:

- `USABLE`
- `UNUSABLE`

Then rank X/Y/Z as 1st / 2nd / 3rd.

Do not show independent reviewer verdicts or interim condition totals until all user judgments are locked.

## 12. Unblind and diagnose

After all user judgments lock:

- reveal X/Y/Z condition mapping;
- combine user absolute labels, rank results and independent Pixel Gate outcomes;
- report usable count per condition;
- report rank wins per condition;
- report failures by diagnostic axis.

Use only the decision vocabulary in `G3_CAPABILITY_DIAGNOSTIC_PROTOCOL.md`.

## 13. Stop

After G3 result is locked:

- stop;
- do not start G4 automatically;
- do not modify Skills automatically;
- do not add images to Discovery;
- do not resume PHASE 10 Attempt 2;
- return the G3 result for independent review.
