# VPD V2 Evaluation Invalidation

Status: `INVALID_HUMAN_REVIEW_BINDING`
Date: 2026-08-15

## What is invalidated

The following artifacts/results must not be used as evidence for VPD V2 quality or next-experiment selection:

- `VPD_V2_HUMAN_BLIND_REVIEW_FREEZE.json`
- `VPD_V2_HUMAN_REVIEW_RESULT.json`
- `VPD_V2_UNBLIND_DIAGNOSIS.md`
- `VPD_V2_NEXT_EXPERIMENT.md`
- verdict `V2_PARTIAL_ADVANTAGE`
- proposed next experiment `A2_FORCED_RED_CONTROL_ABLATION`

The benchmark image generation itself is NOT invalidated. The eight original primary outputs remain valid frozen artifacts.

## Root cause

The human evaluator received eight images in a chat attachment display sequence and treated display position 1..8 as blind IDs `VPD2-R01..VPD2-R08`.

That assumption was false.

A direct Drive fetch of the canonical file `VPD2-R01.png` proved that its real pixels do not match the image that had been scored as R01 in the frozen review. Therefore the human scores were bound to the wrong blind IDs before unblinding.

This is a review-package identity/binding defect, not an aesthetic disagreement.

## Consequence

Because the blind-ID -> human-score binding is invalid, all downstream condition comparisons and causal diagnoses derived from that binding are invalid even if the private condition mapping itself was correct.

No compiler conclusion, DIRECT-vs-V2 conclusion, transfer conclusion, Scale Gate decision, or next ablation may rely on the invalid review.

## Required recovery

Do not regenerate benchmark images.

Reuse exactly the original eight frozen benchmark outputs.

Create a new verified blind-review package in which:

1. each image is fetched from its canonical Drive file named `VPD2-R01.png` through `VPD2-R08.png`;
2. each displayed/reviewed image visibly carries only its blind ID outside the image area or is delivered as a file whose filename is the blind ID;
3. file SHA-256 is recorded before packaging and verified after packaging;
4. no condition name, Style A/B name, DIRECT/V2 identity, content role, capsule identity, prompt identity, or private mapping is exposed;
5. a contact sheet, if created, preserves a deterministic grid order explicitly labeled R01..R08;
6. a fresh independent evaluator that has not seen the condition mapping performs the review;
7. the fresh review is frozen before any unblinding;
8. only then may unblind diagnosis be repeated.

## Contamination boundary

The current evaluation context has already seen the private condition mapping and is not eligible to perform the replacement blind review.

A fresh independent review context is required.

## Scale Gate

`allow_library_scale_gate = false`

Scale Gate remains blocked until the replacement blind review and a subsequent valid unblind diagnosis are complete.
