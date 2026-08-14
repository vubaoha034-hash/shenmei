# VPD V2 Status

Current status: `PROFESSIONAL_SPEC_COMPLETE / MACHINE_CAPSULE_VALIDATION_PENDING / VISUAL_BENCHMARK_NOT_STARTED`

Canonical next branch to create from this commit:

`visual-program-distillation-v2-photography-design-20260814`

The previous VPD V1 runner must not be executed as the next experiment.

Next required work:

1. create V2 branch from this exact commit;
2. author one concrete V2 capsule from an absolutely usable reference;
3. validate the capsule against `schemas/visual-program.v2.schema.json`;
4. inspect compiled renderer payload for evidence loss / prompt bloat;
5. only then run the controlled visual benchmark in `VPD_V2_ACCEPTANCE_PROTOCOL.md`.
