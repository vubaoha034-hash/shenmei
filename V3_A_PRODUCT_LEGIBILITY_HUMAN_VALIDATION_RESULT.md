# V3 A Product Legibility Recovery R1 — Human Validation Result

Status: `BUILTIN_IMAGEGEN_EFFECTIVE / HERO_IDENTITY_STILL_FAIL`

## Evidence inspected

- `V3-A_PRODUCT_LEGIBILITY_RECOVERY_R1.png`
- `V3-A_FOOD_APPETITE_CORRECTED_R1.png`
- exact real food source `ast_63aa377b-5287-400d-b0a3-a6282313b38c.jpg`

## Human judgment

The built-in OpenAI `image_gen` edit materially improved the selected artifact:

- ambiguous secondary bowls were removed/suppressed;
- the hero food gained clearer piece separation;
- the plate reads more cleanly;
- the image is easier to parse commercially than the previous version;
- Route A family identity and macro composition were retained.

However, the hero-food identity gate still fails under the user's real standard.

A viewer can understand that the plate contains a dark glazed / sauced cooked meat dish, but the exact dish identity and primary ingredient are not reliably legible from the hero image alone. The real source asset itself has the same ambiguity: it is visually dark, irregular, and not self-identifying enough to support a named hero-product claim without semantic metadata.

Therefore:

- `hero_shape_separation`: PASS
- `food_appetite_vs_previous`: PASS
- `secondary_food_clarity`: PASS
- `family_identity_retained`: PASS
- `specific_dish_identity`: FAIL
- `final_commercial_hero_usability`: FAIL
- `golden_exemplar`: NO

## Root cause update

This run confirms that renderer choice was a real factor: the official built-in `image_gen` performed the targeted cleanup/edit effectively with one call.

But renderer quality alone cannot solve an upstream semantic-data failure.

The system currently allows a food asset to become a hero visual without a verified semantic contract stating what the dish actually is. When the source pixels are ambiguous, the renderer can only create a more attractive ambiguous dish, not a reliably identifiable named dish.

## New required gate

Before any food asset is promoted to hero-KV generation, it must carry a verified `FOOD_SEMANTIC_IDENTITY_CONTRACT` containing at minimum:

- canonical dish name;
- primary ingredient / protein;
- cooking method;
- 2–5 visible identity cues that must remain recognizable;
- forbidden substitutions / hallucinated ingredients;
- whether the source asset itself is visually adequate for hero use;
- evidence source and confidence.

If those fields cannot be recovered from existing private provenance / source metadata, the system must fail closed and request the missing dish identity from the human rather than infer it from ambiguous pixels.

## Production implication

Do not resume Production Layer Separation yet for this artifact.

Correct dependency order:

1. resolve semantic dish identity;
2. decide whether the current source is hero-adequate;
3. if adequate, perform one semantic-identity-aware built-in `image_gen` recovery;
4. human validate product identity and appetite;
5. only then resume typography / production-layer refinement.

Route B remains `SOURCE_MISMATCH_FOR_ROUTE_B`.
Library Scale Gate remains blocked.
