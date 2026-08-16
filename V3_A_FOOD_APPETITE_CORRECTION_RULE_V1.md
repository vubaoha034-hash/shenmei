# V3 A Food Appetite Correction Rule V1

Status: ACTIVE HUMAN-CORRECTION EVIDENCE

This rule exists because the current selected V3-A artifact was judged by the human reviewer to make the dish look over-browned / burnt / visually blackened ("炒糊了，乌漆麻黑"). This is a higher-priority defect than production typography polish.

## Core distinction

Do not equate wok heat / caramelization / sear with blackened food.

Desired visual target:
- red-brown / sauce-red / amber-brown body color;
- glossy sauce wrap and moist surface;
- selective browned edges only;
- visible internal tonal separation and ingredient texture;
- appetizing heat and freshness;
- green garnish remains fresh, not neon;
- food reads as freshly cooked, not burnt, dry, charred, or soot-dark.

Forbidden failure modes:
- whole-dish dark-brown/black dominance;
- large-area carbonized/charred surfaces;
- black glossy crust that hides ingredient texture;
- crushed shadow detail in food;
- burnt / over-fried / scorched appearance;
- using global contrast or black background to make the dish darker;
- replacing appetizing sauce gloss with hard specular black shine.

## Priority order for this dish family

1. appetizing red-brown color separation
2. moist sauce gloss
3. believable meat/ingredient texture
4. selective seared edges
5. wok-heat cues
6. fire intensity

If 5 or 6 damages 1-4, reduce the heat/fire cue instead of darkening the food.

## Gate

A selected artifact cannot enter Production Layer Separation / Golden Exemplar validation while the primary food subject visually reads as burnt, blackened, dry, or unappetizing.

Food appetite correction must pass human visual review first.

## Architecture rule

This is a thin correction gate, not a new large prompt block. The runtime should translate it into only the minimum high-leverage food-specific direction needed for the current artifact.
