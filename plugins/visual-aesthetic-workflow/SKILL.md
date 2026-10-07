---
name: visual-aesthetic-workflow
description: Strict request-level typography production controller. Preserves native Shanyeji→Liu authority as read-only, while isolated typography requests must pass reference text extraction → local lettering asset → editable Figma rebuild → actual independent pixel review → isolated editable typography delivery. Full posters, structure-lock regressions and flattened Figma images cannot substitute.
---

Version 0.2.0 changes the request workflow contract without changing the native task lock or S7 state.

For an isolated typography request, do not treat a poster edit, structure-lock regression, transparent lettering image, Figma image upload, plan, or chat summary as the final delivery. The only completion path is:

1. REFERENCE_TEXT_EXTRACTION — actual reference pixels viewed and text/geometry evidence bound.
2. LOCAL_LETTERING_ASSET — isolated local lettering guide bound to the reference and requested copy.
3. FIGMA_EDITABLE_REBUILD — isolated Figma typography source with actual readback; at least one native text or editable vector node; zero image nodes in the final typography node set.
4. ACTUAL_INDEPENDENT_TYPOGRAPHY_REVIEW — actual reference/output pixels reviewed in an independent context. FAIL returns to Figma repair.
5. ISOLATED_TYPOGRAPHY_DELIVERY — reviewed editable Figma source delivered as isolated typography only.

Call get_current_workflow to read the authoritative native context. For a new typography production request, call start_typography_delivery with that current commit and a stable request_key. Persist and resume with get_typography_delivery. Record each real stage artifact with record_typography_stage using the exact current revision. The server rejects stage skipping and substitute artifacts.

Native state remains separate: the request task stores only a read-only native snapshot. It never writes CURRENT_TASK_LOCK, the S7 human state, native AI verdicts, or business acceptance. The historical compile_transfer_plan and validate_user_request_delivery tools remain available for legacy poster/structure-lock diagnostics, but they cannot complete a v0.2.0 isolated typography task.

External execution still requires the actual allocated image/Figma/reviewer tools. Tool receipts must describe real calls and readbacks; the controller does not manufacture pixels, Figma nodes, or independent review. If an external capability is unavailable, stop at that gate rather than claiming completion.

Human feedback intake remains append-only and non-authoritative. AI review never replaces Liu's acceptance.
