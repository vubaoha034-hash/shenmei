# VPD V2 Static Acceptance

Status: `PASS_STATIC_SPEC / IMPLEMENTATION_SCHEMA_PENDING`
Date: 2026-08-14

## Scope

This acceptance checks whether the VPD V2 design spec addresses the architectural weaknesses identified in `VPD_V1_PROFESSIONAL_SELF_AUDIT.md`.

It does not claim that generated images are already good.

## Checks

### A. Photography decomposition depth
PASS.

V2 explicitly covers:
- capture geometry;
- optics/focus;
- lighting architecture;
- exposure/tonality;
- color science/grade;
- texture/sharpness/microcontrast;
- subject styling/scene construction;
- post-processing/retouch.

### B. Graphic-design decomposition depth
PASS.

V2 explicitly covers:
- semantic intent;
- attention hierarchy;
- grid/geometry;
- typography and lettering;
- copy meaning;
- whitespace/density;
- color system;
- graphic language;
- layering/crop/edge;
- print/material treatment;
- sequence/system behavior.

### C. Photo/design integration
PASS.

V2 includes a mandatory integration engine so a hybrid poster cannot be represented as independent `photo` plus `text` layers with no interaction model.

### D. Observation vs inference
PASS.

V2 requires evidence type, confidence, source region, and uncertainty. Exact hidden camera settings may not be invented from pixels.

### E. Causal priority / prompt selection
PASS.

V2 requires critical/important/secondary/free classification plus variable interactions. Thin prompt compilation must select high-impact variables, not arbitrary easy-to-describe fields.

### F. Style/content separation
PASS.

V2 separates transferable style signature from content-bound, brand-bound, production-bound and optional variables.

### G. Strong visual model preserved
PASS.

The renderer remains responsible for zero-to-one creative synthesis. V2 does not reintroduce Figma/Codex node construction as the primary creative engine.

### H. Multi-scale quality review
PASS.

V2 requires thumbnail, normal-view and detail-view checks, with explicit photography and graphic-design criteria.

### I. Transfer/non-copy tests
PASS.

V2 requires source reconstruction, content swap, composition variation, aspect transfer, style-distance, direct-baseline and second-style compiler tests.

## Remaining gaps before any visual benchmark

1. machine-readable V2 schema is not yet implemented;
2. compiler implementation/runner is not yet frozen;
3. no capsule has been authored with the V2 structure;
4. no direct baseline vs V2 output has been generated;
5. no independent human visual acceptance has been performed.

Therefore:

`VPD_V2 = STATIC_SPEC_PASS / NOT_READY_FOR_RENDER`

Next action:

Implement machine-readable V2 schema and compiler/runner, validate them, then run a deliberately small visual benchmark. Do not bulk-distill the existing library yet.
