# Supplemental review: native historical human-feedback binding

Verdict: PASS for this narrowly scoped source adjustment. FINAL_SOURCE_REVIEW.md (independently executed 33-test baseline) and INITIAL_REVIEW.md (old published c6 FAIL) remain unchanged. Production OAuth, deployed corrected behavior and real D1 persistence remain INCONCLUSIVE.

New exact source hashes:

- core.mjs: 4c51a64df0a7da97058134683780759b62af21f6c1c56f8901f7f035113034a5
- core.test.mjs: 91f867394f8e0d6bfd11ed19efe1f1d2d69cb0e52aeda037cbce38b4b77dd087
- worker.mjs remains 8aeab739d994c0675e32f49e7ea279a9f21f0a050573dd82337dcbc4a6d33710.

I inspected the actual two-file diff against final-snapshot/. Core changes only the native schema-key compatibility, historical target binding and explicit output identity markers. Test changes provide the corresponding real schema field, grant target, mismatch negative case and newer-artwork scenario. No image, Figma, Drive, reviewer, native-write capability or mainline identity changes were introduced.

I read the actual native HUMAN_S4_LOCAL_REPAIR_ALLOCATION_20261006.json. Its field is schema_version, not schema; target_export is the original S4 SHA ddb621ebf7e230279a1358b1b93ab9fcd55705b7e6ca99af8649aa3295ab1ca4. The previous implementation therefore rejected the actual grant format. The corrected code prefers schema_version and keeps schema as a fallback.

Historical feedback is admitted only when its target SHA is valid, equals the hash-bound grant target and occurs in the existing native attempt history. The response now distinguishes applies_to_export_sha256 from current_artwork_assessed_by_this_feedback. The latter is false for a newer artwork; the historical comment cannot become its human assessment. This relaxes only the erroneous current-artwork-equals-historical-target assumption; it does not loosen the grant/feedback hash checks or authorize another work.

Actual reviewer executions:

1. Three affected tests ran with the bundled Node, all PASS: scoped feedback exposure and prompt exclusion; wrong hash/artwork/grant-target rejection; historical S4 feedback with a newer synthetic artwork. The last retains human PENDING, promotion_allowed:false and MISSING_OR_INVALID_NO_PASS for cold evidence. See native-feedback-targeted-tests.txt. I did not claim a new independent full 34-test run.
2. Reviewer-written native-feedback-replay.mjs loaded the actual grant and feedback bytes, verified their SHA binding, and inserted them only into an in-memory fixture layered over actual committed S4 state at 4d128f7b44dc43163f021b5717f5e003ca70a323. Result: HTTP-equivalent core status 200, correct S4 target, current_matches:true, human PENDING, promotion_allowed:false, independent_review_input:false. This is actual native-file compatibility evidence, not a production tool call or fresh S5/S6 state validation.

Native grant SHA256: da09f7773629b8ff80d80119057bef707d8ddca61c8f4b6aa7de4ce7dad7b597. Bound feedback SHA256: a8ce523dca16e2397c8c5943a88ab8d4526224b7b11e12d3c2f5f0357a723c25. The feedback text is not repeated in this report. See native-feedback-replay-results.txt and native-feedback-snapshot/.

No production writes, source edits, business-state edits or Site publication occurred in this review. I did not inspect this round's pixel-review content. The previous protocol/persistence fixes remain intact by exact diff and unchanged worker hash. Root may proceed with the already-authorized same-Site publication; it must bind its deployment/readback to these new source hashes and continue to report unconnected OAuth/D1 capability as unverified.
