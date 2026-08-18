# V3-A R4 — Drive Reference Calibration Result — 2026-08-19

Status: `R4_INITIAL_EXPLORATION_REFERENCE_CALIBRATION_FAIL / DRIVE_GROUNDED_RECOMPOSE_REQUIRED`

Repository: `vubaoha034-hash/shenmei`
Branch: `visual-program-distillation-v2-photography-design-20260814`

## Trigger

Human review judged the initial R4-A / R4-B / R4-C outputs materially better than the rejected prior poster, but still far from the user's preferred visual standard.

A post-generation audit then opened the user's Google Drive `R1C/approved_refs` set and inspected all 18 approved reference images directly.

Critical correction:

The initial R4-A/B/C generation did **not** have the actual Drive approved reference pixels bound as active visual context. It used project abstractions and the R4 conceptual split only. Therefore those three candidates are not valid evidence of Drive-calibrated personal taste fidelity.

## Drive-approved visual families observed

The 18 approved images form several related but distinct families rather than one averaged style.

### Family N — Nature / Regional Brand World

Representative references include 01, 02, 07, 09, 13, 14, 15, 16, 17, 18.

Recurring mechanisms:
- mountain / forest / village / field / ingredient environment as a brand world, not merely background decoration;
- dark forest green, sage green, off-white, soil/wood neutrals, restrained orange/red accents;
- custom or hand-drawn Chinese display lettering integrated with landscape/photography;
- primitive icons, stamps, line drawings and regional symbols;
- visible paper/print/material texture;
- food often acts as one proof layer rather than monopolizing the whole composition;
- strong brand-system/editorial behavior rather than a single glossy food advertisement.

### Family S — Spicy / Wok / Rustic Heat Brand System

Representative references include 03, 04, 05, 06, 08.

Recurring mechanisms:
- heat/process imagery exists, but is embedded inside a broader brand system;
- oxidized red, dark brown/near-black, parchment/cream and restrained white rather than luxury black+gold;
- large authored Chinese lettering, often rough/printed/brush-like but not generic calligraphy as decoration;
- hand-drawn food/ingredient symbols, stamps and vernacular graphic marks;
- multiple campaign/application modules, environmental/context imagery and brand storytelling;
- visual richness comes from a coherent graphic language, not from smoke, fire, bokeh and food gloss alone.

### Family G — Graphic / Editorial Natural System

Representative references include 10, 11, 12 and parts of 02/14/15.

Recurring mechanisms:
- large negative space and controlled grids;
- sage/olive/cream color systems;
- simplified illustration, packaging, icon and symbol systems;
- restrained photography;
- design authorship is carried by typography, shapes, illustration and material behavior, not only by a hero photo.

## Why initial R4-A/B/C are still far away

The three outputs improved local polish but converged on a different category:

`generic premium Chinese food advertisement / black-gold food photography`

instead of the dominant Drive preference:

`authored regional restaurant brand world + vernacular/custom typography + natural/editorial graphic system + restrained commercial photography`.

Main mismatches:

1. black + gold became the default premium shortcut;
2. generic generated calligraphy was used as the main design authorship layer;
3. hero food or chef/wok photography occupied too much semantic authority;
4. food remained glossy/saturated and advertisement-like;
5. environmental/regional brand-world evidence was weak or absent;
6. almost no primitive icon, illustration, stamp, print or material language was present;
7. the outputs behaved like single posters, while many approved references behave like coherent campaign/brand-system surfaces;
8. negative space and graphic composition did not match the Drive references' editorial restraint;
9. the three candidates differed in macro composition but not enough in underlying design worldview.

## Decision

- R4-A: `DO_NOT_SELECT`
- R4-B: `DO_NOT_SELECT`
- R4-C: `DO_NOT_SELECT`

Reason: useful quality step, but wrong taste calibration.

Do not refine these three further.

## Next stage

`V3-A R4.1 — DRIVE-GROUNDED COMMERCIAL RECOMPOSE`

Generate exactly three new full-frame candidates using actual approved Drive references as visible grounding, but do not copy brand names, logos, proprietary symbols or exact layouts.

### R4.1-A — Rustic Heat Brand System

Ground primarily in the mechanisms visible in references 03/04/05/06/08.

Goal:
- `现烧` interpreted as a real restaurant brand/campaign system;
- oxidized red / parchment / near-black;
- real wok/process photography as one layer;
- authored vernacular lettering + primitive food/heat symbols;
- no luxury gold-calligraphy shortcut;
- no cinematic fire spectacle.

### R4.1-B — Nature / Regional Freshness

Ground primarily in references 01/07/09/13/14/15/16/17/18.

Goal:
- `现烧` tied to locality, ingredients, mountain/field/village/natural context;
- forest/sage/cream with one restrained warm accent;
- real food photography but not oversized hero-ad behavior;
- custom Chinese lettering integrated with environment;
- natural print/material texture and small vernacular marks.

### R4.1-C — Minimal Editorial Brand Campaign

Ground primarily in references 10/11/12/13/15.

Goal:
- large negative space;
- one restrained food/process image;
- sage/cream/ink or another reference-supported restrained palette;
- custom display lettering + graphic symbol/illustration system;
- quiet premium commercial finish without black-gold luxury coding.

## Runtime rule

Use Drive reference pixels directly as visual grounding for each candidate. Do not rely only on distilled prose.

Each candidate may extract mechanisms from a small coherent subset of references; do not average all 18 into one style.

Keep final prompt compact:
- 1 visual cause;
- 1 attention flow;
- 5–8 high-leverage decisions;
- <=3 hard avoids;
- exact required copy only.

## Current gate state

- Family Transfer: `PASS`
- initial R4-A/B/C: `REFERENCE_CALIBRATION_FAIL / DO_NOT_SELECT`
- R4.1 Drive-grounded recomposition: `NEXT`
- Commercial Quality Gate: `NOT YET`
- Golden Exemplar: `NO`
- Scale Gate: `BLOCKED`

## 已完成什么

- all 18 Drive `R1C/approved_refs` images were opened and visually inspected;
- the approved set was separated into coherent visual families instead of averaged;
- the initial R4-A/B/C mismatch was diagnosed as a taste/reference-calibration error, not merely insufficient polish;
- the three initial R4 candidates were removed from selection/refinement;
- R4.1 was defined as a Drive-grounded three-candidate recomposition.

## 未完成什么

- R4.1-A/B/C have not yet been generated;
- no Drive-grounded new candidate has passed human review;
- no R4 artifact is selected for production typography;
- Commercial Quality, Golden and Scale remain blocked.
