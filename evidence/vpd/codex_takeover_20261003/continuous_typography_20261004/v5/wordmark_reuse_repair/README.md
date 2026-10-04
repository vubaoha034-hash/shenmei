# V5 original wordmark technical reuse repair

The historical `wordmark/` directory and its manifest remain immutable evidence.
Its `build_wordmark.py` writes before its photo assertion, and its render script
overwrites the bound PNG/provenance. Neither is a safe reuse command.

Use the new default read-only entry point from the repository root:

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B 'scripts/vpd_verify_original_wordmark.py'
```

It verifies the canonical photo/reference/V4 SHA bindings, the fixed manifest
itself and all eight entries, actual fontTools/Node/Sharp versions, and the bound
PNG metadata before replaying any geometry. It executes the pinned builder's
geometry with its imports replaced by a closed snapshot-only namespace. Every
mkdir/write request is captured in memory; there is no `open`, disk Path writer,
renderer call, or supported disk export. Four reconstructed outputs match the
historical bytes exactly. The Python-stage provenance is compared semantically
to the historical provenance before the old Node raster fields were added; its
original creator identity is reproduced only in memory.

All fifteen SVG paths are compared to the reconstructed contours, stroke origin
records and Figma path data. The shared main shafts, horizontal weight, corner
cuts, character components and spacing are also checked. This confirms technical
identity of the original asset, without creating a new design or judging taste.

`--photo-path`, `--reference-path` and `--v4-path` allow read-only negative-source
probes; both canonical and supplied sources must match the fixed SHA. All
`--output-dir` requests are rejected, including non-existent directories. Reuse
the already verified SVG bytes through a separate explicit copy when needed.
Do not rerun either historical writer against the bound directory.

`execution_01/EXECUTION_REPORT.json` records eleven actual subprocess controls:
three wrong sources, two existing bound-output targets, one new-output rejection,
and five valid controls with different caller thread IDs. Every scenario compared
all nine historical files byte-for-byte and by modification timestamp. Each valid
control captured five writes in memory and preserved the original creator identity.
No image was generated or rendered and no business-state file was written.

`run_controls.py` records into a newly created exclusive evidence directory and
refuses to overwrite an existing run. Its first execution is preserved here.
The entry point is bound to this exact V5 builder and exact inputs; it is not a
general sandbox for arbitrary scripts. Independent professional review is still
the reviewer's responsibility.
