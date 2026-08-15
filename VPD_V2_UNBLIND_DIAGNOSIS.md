# VPD V2 Unblind Diagnosis

## Freeze integrity

- The human review was frozen before unblinding: `true`.
- Frozen review SHA-256: `36ee9c1dfc24a2d0a9745f0d59ff5bcf0c538c0392c9e86040859f58d8922ff1`.
- Frozen totals remain exactly `0 top-tier / 4 USABLE / 4 UNUSABLE`.
- Scale status remains `NOT_READY_FOR_SCALE`; `allow_library_scale_gate = false`.
- Mapping, attachment, prompt, output, and machine-integrity receipts agree by hash. All eight outputs were valid one-attempt primaries with no hidden batch, best-of-N selection, or cosmetic retry.

## Frozen mapping

Human scores below are copied without alteration from the frozen blind review.

| Blind ID | Frozen condition | Style | Content role | Photography | Graphic design | Integration | Material realism | Typography | Absolute |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| VPD2-R01 | A0_DIRECT | A | reconstruction source | 6 | 4 | 4 | 7 | 3 | UNUSABLE |
| VPD2-R02 | B0_DIRECT | B | reconstruction source | 5 | 4 | 3 | 7 | 3 | UNUSABLE |
| VPD2-R03 | B1_V2_RECONSTRUCT | B | reconstruction source | 8 | 7 | 7 | 8 | 6 | USABLE |
| VPD2-R04 | B3_V2_COMPOSITION_OR_ASPECT_VARIATION | B | composition/aspect source | 7 | 5 | 5 | 8 | 4 | UNUSABLE |
| VPD2-R05 | B2_V2_CONTENT_SWAP | B | genuinely different content source | 8 | 7 | 8 | 8 | 6 | USABLE |
| VPD2-R06 | A2_V2_CONTENT_SWAP | A | genuinely different content source | 7 | 4 | 4 | 8 | 4 | UNUSABLE |
| VPD2-R07 | A3_V2_COMPOSITION_OR_ASPECT_VARIATION | A | composition/aspect source | 8 | 7 | 7 | 8 | 6 | USABLE |
| VPD2-R08 | A1_V2_RECONSTRUCT | A | reconstruction source | 7 | 7 | 7 | 7 | 6 | USABLE |

## Style A comparison

### DIRECT baseline

`A0_DIRECT` is `UNUSABLE`. Its material realism was adequate (`7`), but graphic design and integration were both `4`, and typography was `3`. The short raw-reference instruction produced a credible food image with a conventional poster layer rather than an authored photo-design system.

### RECONSTRUCT value

`A1_V2_RECONSTRUCT` versus `A0_DIRECT` is a `CLEAR_GAIN`:

| Dimension | A0 | A1 | Delta |
|---|---:|---:|---:|
| Photography | 6 | 7 | +1 |
| Graphic design | 4 | 7 | +3 |
| Integration | 4 | 7 | +3 |
| Material realism | 7 | 7 | 0 |
| Typography | 3 | 6 | +3 |

The gain is not explainable by a reference-binding difference: both conditions received the same raw style anchor and reconstruction content, and the receipt hashes match. The V2 payload converted an unusable direct result into a usable result while preserving the realism floor.

### CONTENT_SWAP robustness

`A2_V2_CONTENT_SWAP` is `UNUSABLE`. The source dish remained materially credible (`photography 7`, `material realism 8`), so this is not a material-realism collapse or a missing-reference failure. Family quality did not survive: graphic design and integration fell to `4`, typography to `4`, and the result reduced the distilled family to a generic black/red/brush-poster treatment. The payload forced a static plated egg/rice source to express a cooking-action heat bridge, a fermented-red structural zone, and rough motifs. That is evidence of style/content binding trouble, not evidence that content swap is robust.

There is no evidence of literal reference-brand or exact-glyph copying. The failure is genericization and photo/design separation.

### COMPOSITION / ASPECT robustness

`A3_V2_COMPOSITION_OR_ASPECT_VARIATION` is `USABLE` (`8/7/7/8/6`). It is a real 3:2 recomposition of an overhead multi-dish source: the meal cluster, title mass, red carrier, and supporting path were redistributed for landscape. It is not a center crop of the portrait source. Style A therefore demonstrated one successful composition/aspect transfer, though typography remained below top-tier.

## Style B comparison

### DIRECT baseline

`B0_DIRECT` is `UNUSABLE`. Material realism held at `7`, but photography was `5`, graphic design `4`, integration `3`, and typography `3`. The result was a generic styled food scene with a headline rather than the intended two-anchor editorial field.

### RECONSTRUCT value

`B1_V2_RECONSTRUCT` versus `B0_DIRECT` is a `CLEAR_GAIN`:

| Dimension | B0 | B1 | Delta |
|---|---:|---:|---:|
| Photography | 5 | 8 | +3 |
| Graphic design | 4 | 7 | +3 |
| Integration | 3 | 7 | +4 |
| Material realism | 7 | 8 | +1 |
| Typography | 3 | 6 | +3 |

The measured mass map, warm mineral field, two-anchor hierarchy, soft grounding, and sparse color rhythm were compactly represented in the capsule and renderer payload. With the same raw style and reconstruction content bindings, V2 produced a usable result and improved every frozen score dimension.

### CONTENT_SWAP robustness

`B2_V2_CONTENT_SWAP` is `USABLE` (`8/7/8/8/6`). The genuinely different egg/rice/plate/spoon source remained recognizable and materially credible, while the warm field, dark headline/dish anchors, active pause, and sparse natural color rhythm survived. It did not collapse into a photo card, literal reference copy, or material-realism loss. Style B therefore demonstrated one genuine content-transfer success.

### COMPOSITION / ASPECT robustness

`B3_V2_COMPOSITION_OR_ASPECT_VARIATION` is `UNUSABLE` (`7/5/5/8/4`). It is not merely a changed crop: the portrait multi-dish source was recomputed into a 3:2 landscape arrangement and the dish relationships were retained. However, true geometric recomposition did not preserve the family logic. The headline and meal ceased to behave as co-equal anchors; the mineral field became passive empty space, typography lost authority, and photo/type read as separated regions. The operation was a real variation, but the style transfer failed.

## DIRECT vs V2 conclusion

Both matched reconstruction comparisons favor V2 materially: `A0 -> A1` and `B0 -> B1` each move from `UNUSABLE` to `USABLE`, with large gains in graphic design, integration, and typography. DIRECT did not win either matched reconstruction comparison.

The overall verdict is `V2_PARTIAL_ADVANTAGE`, not `V2_CLEAR_ADVANTAGE`. V2 produced four usable outputs among its six conditions, including two reconstruction gains and two genuine but different transfer successes. It also produced two transfer failures, there is no matched DIRECT output for the content-swap or landscape sources, and no output reached top-tier quality. The benchmark therefore supports practical V2 value but not reliable transfer superiority.

## Transfer conclusions

- CONTENT_SWAP preserved family quality for `B2` but not `A2`. A single success cannot be generalized as robust transfer.
- COMPOSITION / ASPECT variation was genuinely recomputed in both `A3` and `B3`, rather than being a center crop. Only `A3` preserved usable style logic; `B3` did not.
- The split is not explained by a missing raw reference, invalid image, retry selection, or output corruption: all bindings and outputs were receipt-verified.

## Root-cause attribution

| Root cause | Evidence | Affected conditions | Confidence | Layer |
|---|---|---|---|---|
| `STYLE_CONTENT_BINDING_ERROR` | A2 preserved the new dish and material realism but forced a static plated source through cooking-action heat, fermented-red structure, and rough-motif invariants; design/integration fell to 4/4 while A1 and A3 were usable. | A2 | HIGH | architectural |
| `CAUSAL_PRIORITY_ERROR` | The capsules distinguish CRITICAL/IMPORTANT variables, but the renderer payloads flatten eight controls into a numbered list. In both failed transfers, content/material scores stayed high while the highest-value photo/type relationship failed. | A2, B3 | MEDIUM | compiler-level |
| `PROMPT_COMPILATION_INTERFERENCE` | A2 specifically compels yolk/sauce to become a fermented-red structural zone. The visible result overexpresses the black/red/brush shorthand named in the frozen review. Because A1 and A3 succeed with the same payload size, this is targeted interference, not a general complexity penalty. | A2 | MEDIUM | compiler-level |
| `TYPOGRAPHY_CAPABILITY_LIMIT` | Typography is the lowest or joint-lowest dimension throughout; it is 3 on both DIRECT outputs, 4 on both failed transfers, and never exceeds 6. Explicit original-lettering direction improved usability but did not reach top-tier authority. | A0, A1, A2, A3, B0, B1, B2, B3 | HIGH | renderer-level |
| `PHOTO_DESIGN_INTEGRATION_FAILURE` | A2 scores 7 photography/8 material versus 4 design/4 integration; B3 scores 7/8 versus 5/5. Credible food did not become one composition with type and field. | A2, B3 | HIGH | task-level |
| `RENDERER_CAPABILITY_LIMIT` | B3 received the raw reference, verified content, and an explicit two-anchor/active-field instruction but failed to realize that balance in a one-attempt landscape synthesis. One sample cannot separate a stable capability boundary from sampling variance. | B3 | MEDIUM | renderer-level |

`OBSERVATION_ERROR` is not supported: both reconstructions made large gains from the measured descriptions. `REFERENCE_BINDING_ERROR` is ruled out by matching attachment and output hashes. `STYLE_FAMILY_EASINESS_BIAS` is not established after unblinding: Style A and Style B each contain two usable and two unusable outputs, and each has two usable V2 conditions out of three. Dark high-contrast tropes can mask weakness, but this benchmark does not support treating family ease as the global cause.

## What V2 actually proved

- On the same reconstruction source, V2 clearly beat DIRECT for both Style A and Style B.
- Capsule-derived controls can preserve a high material-realism floor while improving design integration.
- Controlled transfer is possible: B2 survives a genuine content swap, and A3 survives a true landscape recomposition.
- The measured evidence and raw-pixel binding were operational, not merely documentary.

## What V2 did not prove

- It did not prove reliable transfer across content and aspect changes: A2 and B3 are counterexamples.
- It did not prove superiority to matched DIRECT baselines for the content-swap or landscape sources; those matched DIRECT conditions do not exist in this benchmark.
- It did not prove top-tier typography, top-tier authored distinctiveness, or a solved photo-design integration pipeline.
- It did not validate either single-reference capsule as a scalable Style Signature.

## Why Scale Gate remains blocked

The frozen review is still `0 top-tier / 4 USABLE / 4 UNUSABLE` and explicitly states `NOT_READY_FOR_SCALE`. Unblinding explains the split but does not supersede it. No Library Scale Gate was executed, and `allow_library_scale_gate` remains `false` until a later independent human review explicitly replaces this freeze.

## Minimum next experiment

Run exactly the single experiment specified in `VPD_V2_NEXT_EXPERIMENT.md`: `A2_FORCED_RED_CONTROL_ABLATION`. It tests one evidence-selected payload variable with a matched DIRECT baseline and three outputs total. No generation is performed in this diagnosis task.
