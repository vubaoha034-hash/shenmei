S5 single bounded local repair — pending independent cold review

Formal vector: S5_WORDMARK.svg (SHA256 e5e3e540f1a296935e44aaa74053c6855907eb5563557e939d30386f8ebde5a1; 29052 bytes; 5 paths; no bitmap/font embeds).
Transparent technical raster: S5_WORDMARK_TRANSPARENT_RENDER.png. Green and 480px derivatives are visibility aids, not final posters.

Implementation: exact S4 traces reused; no new VTracer calls. Fixed VTracer0.6.15/skia-pathops0.9.2 unchanged. Seam FROZEN_SPEC changes only two XIAN_UPPER_BAR_END left x coordinates to 658, window remains x660. 36 final straight faces match the 21 explicit polygon edits. Their endpoints receive <=1.5px transitions; faces receive deterministic 0.65px shallow quadratic bows. No randomness or new grain. Original cut direction, body mapping, source geometry outside incident shoulders, all four orange paths and 2.8px width retained. Original S4 files untouched; SOURCE_S4_* are exact preserved copies.

Actual seam evidence: XIAN_SEAM_BEFORE_10X.png and AFTER. At y461/467/473, x548–556 alpha now all255; original seam pixels x551/x552 had alpha100/163,100/110,100/57. Outer top/bottom contours remain sloped, so endpoints are not asserted to be solid rectangular fills. Both orange groups are byte-identical. Cream raster bounds remain [224,431,792,601].

Pixel diff: 1082 samples changed.16 lie outside polygon4px envelopes; maximum absolute alpha difference12/255, all boundary antialias samples. Trimming and rounding incident source Bézier controls introduces small serialization differences along their original curve. Exact pixel identity outside edit masks is NOT claimed. See LOCAL_PIXEL_CHECK.json for every such sample.

Technical attempts: first Windows GBK adapter failure preserved; copied unadapted S4 builder recomputed exact S4, then -X utf8 resolved runtime only. One S5 geometry implementation, zero parameter retries. No native imports, Drive, generation, state changes or taste PASS. Root must assemble native full poster and commission independent actual-pixel cold review; photography and supporting text remain outside worker scope. Source lower-left Xian channel and two-leg opening intentionally preserved.

Rebuild uses --root explicit checkout and --output-dir restored directory, --reuse-traces. Input SVGs/PNGs are included with bindings in TRACE_GENERATION.json/SOURCE.json. prepare-inputs.cjs is preserved historical extraction source; it need not rerun for S5. Do not use its fresh extraction without original source/reference binding.
