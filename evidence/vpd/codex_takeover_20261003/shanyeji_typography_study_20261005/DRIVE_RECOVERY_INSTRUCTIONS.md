# Confirmed archive and byte-preserving recovery

Current delivery: DELIVERY_MANIFEST_DRIVE_ARCHIVED.json. The previous blocked manifest and rejected operations remain historical evidence. The human reply “是确认。” approved the specified folder and PNG/SVG only; it did not accept the design.

| Asset | Drive ID | MIME | Bytes | SHA256 |
|---|---|---|---|---|
| Complete S2 typography PNG | 1Yf5-usJV-dawGNP-uaPooxdRUVCm6NCj | image/png | 290066 | 200619e4ed960f0442b931532c5b595ceb7e5e77360e72e3c5e3b16ec4c31d26 |
| Clean editable contours SVG | 1vevAlJaGqJc3TwxN2bY8TTOjjTZn_J2q | image/svg+xml | 326634 | 59376f5da7fa880efa8c0e92adcb1e60845cfdf697c5a8cf04430abbd9ec4a6b |

Use Google Drive skill: read metadata first, then fetch the canonical file URL with download_raw_file=true and include_base64=false. Materialize the authenticated top-level file_uri into a new private path. Compare complete bytes and SHA256 before restoring the original local path recorded in DRIVE_PNG_READBACK_CONFIRMED.json / DRIVE_SVG_READBACK_CONFIRMED.json. Do not overwrite an existing mismatched file. Temporary bearer URLs stay private; never save them to Git or use them as lasting links.

Actual post-upload readbacks were HTTP200 and byte-for-byte equal for both files. PNG is 960×1280. Source photography, Figma nodes, original reviewer result, and the 29 Tea poster versions did not change.

The clean SVG stores the editable contour geometry; it does not reproduce the S2 raster soft ink exactly. S2 complete visual output is in the PNG and Figma416:2, with hidden curve group416:3 and visible ink416:271. Original font/alpha remain unknown. These two archives restore the delivered study assets, not every private mask and producer dependency needed for re-running production.

Next action is LIU_REVIEW_SHANYEJI_TYPOGRAPHY_REFERENCE_STUDY; human acceptance PENDING. Do not resume Tea poster production from this archive authorization.
