# R1C — ART DIRECTION LOCK

Status: `NO_GENERATION / REFERENCE_MECHANISM_AUDIT`
Date: `2026-08-14`

## Purpose

R1B proved that editable Figma layers alone do not create strong design. The failure was art direction: the page reduced to a generic food photo, headline, and arbitrary orange L-shaped graphic.

R1C therefore does **not** create another design. It first derives a concrete design mechanism from the user's actual approved visual references.

## Hard rule

No new image generation. No new Figma layout. No variant. No retry.

## Inputs

Use the frozen restaurant Discovery set only:

- approved = 18
- rejected = 12
- no new evidence

For R1C, expose the **18 approved canonical image assets individually** for independent visual inspection.

## Drive transport

Create/use:

`LIU_VISUAL_REVIEW/R1C/approved_refs/`

Copy/upload all 18 approved canonical images individually.

Requirements:

- no contact sheet;
- no montage;
- no resize unless format transport strictly requires it;
- no crop;
- no AI modification;
- preserve original aspect ratio;
- preserve canonical SHA where raw format is transportable; otherwise preserve source->derivative lineage and both hashes.

User-visible names should be neutral:

`R1C-APPROVED-01.*` ... `R1C-APPROVED-18.*`

Private manifest maps each neutral file to sample_id / asset_id / canonical SHA.

## Independent reviewer task

ChatGPT must inspect the actual pixels, not summaries.

From the 18 approved references, choose at most **3** that are most relevant to the current task:

> turning the frozen real-food asset into a premium restaurant hero visual with strong design structure.

Do not choose by filename or previous model summary.

## Art-direction extraction

From those selected references, lock only 5–8 high-leverage visible variables, such as:

- attention geometry;
- image-to-canvas proportion;
- crop behavior;
- negative-space behavior;
- typography scale/placement behavior;
- grid/alignment logic;
- accent-color logic;
- one graphic mechanism;
- texture/reproduction behavior.

Every variable must be traceable to visible pixels in one or more selected approved references.

Do not write generic words such as `premium`, `clean`, `young`, `high-end` unless translated into concrete visible behavior.

## Anti-generic test

Before lock, ask:

1. Could this mechanism belong to any restaurant?
2. Is it merely `photo + headline + colored bar`?
3. Is the accent shape arbitrary rather than derived from image/crop/brand behavior?
4. Does it rely on generic Chinese motifs?
5. Can the mechanism extend into menu, packaging, storefront, and social media without copying the same layout?

If answers show genericity, do not lock; revise the mechanism description only. Do not generate a design.

## Exit artifact

Create a private/public-safe `R1C_ART_DIRECTION_LOCK.md` containing:

- selected neutral reference IDs (max 3);
- why each is relevant;
- 5–8 locked visible variables;
- one concise art-direction statement;
- hard avoids;
- explicit statement that no new image/layout was generated.

## Exit gate

R1C passes only when:

- all 18 approved references were individually available for pixel review;
- independent reviewer selected max 3 anchors from actual pixels;
- the locked mechanism is concrete and imageable;
- it is not a generic restaurant-template recipe;
- no new design output was generated.

Only after R1C PASS may a single new Figma design proof be attempted.
