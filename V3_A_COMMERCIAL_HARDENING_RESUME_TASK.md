# V3-A — Commercial Hardening Resume Task

Status: `FROZEN_NEXT_TASK`

Repository: `vubaoha034-hash/shenmei`
Required branch: `visual-program-distillation-v2-photography-design-20260814`

## Corrected state

The prior `V3_FOOD_SEMANTIC_IDENTITY_NEEDS_HUMAN_INPUT` blocker is INVALIDATED.

Reason:

The food visual under evaluation is system-generated and is not currently tied to a user-specified named menu item or real-world product claim. Requiring the user to invent/recover a canonical dish name, protein, and cooking method was a category error.

Do not fabricate a named dish identity.
Do not ask the user for dish identity unless a later real brief explicitly requires a named product claim.

## Frozen results retained

- Family Transfer: PASS
- Macro-layout break: PASS
- Family identity: PASS
- Generic template collapse: not dominant, but commercial-template risk remains
- Food appetite correction: PASS
- Golden Exemplar: NOT YET
- Commercial Readiness: NOT YET
- Route B: SOURCE_MISMATCH_FOR_ROUTE_B
- Library Scale Gate: BLOCKED

## Objective

Raise the selected V3-A direction from an improved AI-generated design artifact toward a real commercial-production standard without changing the validated macro visual program.

This phase is capability hardening, not scaling.

## Commercial hardening priorities

1. Functional typography ownership and precision
   - exact hierarchy
   - optical alignment
   - tracking
   - line spacing
   - baseline rhythm
   - left identity-rail balance
   - removal of stock-template English-label feel

2. Production-layer separation
   - preserve art pixels
   - replace only functional typography and micro-alignment where technically safe
   - no overlay-on-top-of-baked-text shortcut
   - fail closed if clean local separation is impossible

3. Food/material realism preservation
   - retain appetite correction
   - no return to black/burnt food
   - avoid synthetic orange saturation
   - preserve believable sauce, texture, selective sear, and dimensional separation

4. Brand authorship
   - reduce generic premium-restaurant template cues
   - preserve the large `现烧` raster identity as the visual leader
   - do not replace it with a stock font or redraw it using low-quality vectors

5. Commercial information discipline
   - no filler English
   - no invented product claims
   - no fake menu-item identity
   - retain only semantically useful supporting labels

## Immediate execution target

Resume the already-defined production-layer pilot using:

`V3_A_PRODUCTION_LAYER_SEPARATION_PILOT_R2_TASK.md`

The selected before-state remains:

`V3-A_FOOD_APPETITE_CORRECTED_R1.png`

Expected SHA-256:
`64c9a1370519f0cc3bc7a16046f4042712353b08b2729f10051a58ffc3c6803c`

Expected dimensions:
`1024x1536`

## Important correction to the production pilot

Do not interpret generic food imagery as a named menu item.

The commercial review should judge:

- appetite;
- plausibility;
- category-level food readability;
- material realism;
- typography precision;
- brand authorship;
- production readiness;

It must NOT require a fabricated canonical dish name unless the later brief introduces one.

## Stop conditions

Do not:

- run Library Scale Gate;
- generate Route B;
- modify Discovery;
- modify the global compiler;
- create a new macro concept;
- invent a dish name;
- ask the user for a dish name for this generic generated visual.

After one production-layer formal output or a fail-closed retrofit blocker, STOP for human validation.
