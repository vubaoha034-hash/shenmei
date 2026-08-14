# R1E — DIRECT REFERENCE TYPOGRAPHY PROOF

Status: `FROZEN_PROTOCOL`
Date: `2026-08-14`
Parent finding: `R1D = UNUSABLE / ABSOLUTE_REFERENCE_DISTANCE_FAILURE`

## 1. Purpose

R1E isolates the weakest part of R1D: display-lettering quality.

The only question is:

> Can the system design the four Chinese characters `今日现烧` at a quality level that is materially closer to the user's approved Mother Reference than the R1D title, before any food, poster composition, packaging, or other brand application is attempted?

This is not a full poster task.
This is not a new art-direction exploration.
This is not a benchmark one-shot.
It is a controlled production proof with a bounded sequential revision loop on one target design.

## 2. Absolute-quality rule

R1E MUST NOT be judged relative to R1D.

The only meaningful comparison is:

`R1E target lettering ↔ Mother Reference 05`

If R1E is merely better than R1D but still obviously amateur, generic, font-default, or far from the Mother Reference in visual authority, it fails.

Relative improvement cannot authorize progression.

## 3. Single Mother Reference

The only active Mother Reference is:

`R1C-APPROVED-05.jpg`

Google Drive file ID:
`1M2sI6Q1TfPszHpORj29eY9sr-JDO3Co9`

R1C-APPROVED-13 and R1C-APPROVED-16 are excluded from generation and design decisions in R1E.

Reason:
- Reference 05 is the closest approved reference to the current category and energy: pan, chili, stove, fire, culinary action, commercial restaurant communication.
- Multi-reference averaging was identified as a failure mode in R1D.

## 4. Direct pixel binding — mandatory

The Mother Reference must be present as actual pixels in the same Figma file used for R1E.

The execution agent MUST NOT rely on:
- a prose summary of the reference;
- prior memory of the reference;
- extracted adjectives;
- a contact sheet;
- a style label such as `bold`, `premium`, `editorial`, `Chinese`, `handmade`.

Required Figma structure:

- `R1E_REFERENCE_LOCK` — contains the exact Mother Reference image, visible at useful inspection size;
- `R1E_TYPOGRAPHY_PROOF` — contains the only target lettering design;
- the reference remains visible during all design passes;
- the reference is not part of the final exported proof.

If direct reference pixels are not successfully placed and readable in Figma, status is:

`R1E_BLOCKED_REFERENCE_NOT_BOUND`

and execution stops.

## 5. What may be inherited from Mother Reference 05

Inherit visual mechanisms, not brand identity.

Allowed to study and translate:
- visual authority of the main Chinese display lettering;
- stroke-energy contrast;
- non-uniform character scale;
- non-uniform character width/height;
- asymmetrical optical balance;
- compressed and expanded internal spacing;
- controlled irregularity;
- relationship between heavy and thin areas;
- custom endpoints, cuts, terminals and protrusions;
- sense of heat / force / cooking action expressed through lettering;
- title behaving as a designed visual object rather than normal typesetting.

Do NOT copy or trace:
- the source brand name;
- exact source glyph outlines;
- logo geometry;
- source wording;
- trademark-specific symbol;
- exact composition of the original page.

The target must remain original lettering for `今日现烧`.

## 6. Target content

Only:

`今日现烧`

No food image.
No subtitle.
No English.
No price.
No logo.
No icons.
No pan arcs.
No heat trails.
No chili points.
No decorative background graphics.

The purpose is to isolate lettering ability.

## 7. Functional text vs display lettering

Previous rule was incorrect: the main visual title must not be forced to remain ordinary editable text.

R1E uses two layers:

1. `SOURCE_TEXT_LIVE`
   - contains live editable Chinese text `今日现烧`;
   - preserved outside the final export frame for provenance and future editing;
   - may use a real installed Chinese font as a starting skeleton.

2. `LETTERING_VECTOR`
   - the actual visible title in the proof;
   - converted to vector outlines and manually reconstructed;
   - may change stroke proportions, character width, height, optical center, terminals, negative spaces, cuts, overlaps and relative positioning;
   - must not remain recognizably equivalent to simply typing a stock font and changing size.

This distinction is mandatory.

## 8. Starting-font policy

A real installed Chinese font may be used only as raw material.

Allowed:
- Noto Serif SC or another real Chinese display/serif/humanist face;
- converting to outlines;
- non-destructive source preservation in `SOURCE_TEXT_LIVE`;
- substantial vector reconstruction after outlining.

Not sufficient:
- choosing a different font;
- adding tracking;
- changing weight;
- scaling the whole word uniformly;
- splitting `今日` / `现烧` into two text boxes while leaving default glyphs intact.

If the visible result can be reproduced by ordinary text settings alone, R1E fails the construction requirement.

## 9. Composition constraints

Canvas: `1080 × 1350` (4:5).

Background:
- neutral warm off-white or near-white only;
- no texture needed for this proof.

The lettering should occupy enough area to judge character design clearly.

The four characters do not need equal size or a single baseline.

The design must deliberately control:
- dominant vs subordinate character mass;
- vertical and horizontal rhythm;
- optical centering;
- counters / internal negative spaces;
- stroke-density distribution;
- outer silhouette;
- reading order.

The goal is a coherent four-character lettering object, not four independently decorated glyphs.

## 10. Controlled sequential revision — production, not benchmark

R1E permits bounded refinement because production design is iterative.

Exactly one target design may exist.

Allowed process:
- Pass 0: construct the first target;
- Pass 1: revise the same vector lettering based on direct reference comparison;
- Pass 2: one final refinement pass if still needed.

Maximum: 3 total passes on the same target.

Forbidden:
- creating multiple candidate directions;
- creating A/B/C alternatives;
- keeping several target frames and choosing the best;
- changing Mother Reference;
- restarting from a different style;
- hiding failed alternatives.

Each pass may modify the same `LETTERING_VECTOR` only.

A private revision log must record, for each pass:
- what looked weak versus Mother Reference 05;
- exactly what was changed;
- which issue class was addressed: glyph construction / spacing / scale hierarchy / silhouette / stroke energy / optical balance.

The log is procedural evidence, not an aesthetic PASS claim.

## 11. No self-certification of beauty

Codex may verify technical facts only:
- reference pixels are directly bound;
- target content is exactly `今日现烧`;
- source live text exists;
- visible lettering is vector outlines;
- vector geometry differs substantially from stock source glyphs;
- only one target design exists;
- number of sequential passes ≤ 3;
- export integrity;
- Drive upload;
- Discovery unchanged.

Codex MUST NOT declare:
- `beautiful`;
- `premium`;
- `reference-level`;
- `USABLE`;
- `PASS` on visual quality.

## 12. Output

Figma file to use:
`https://www.figma.com/design/d3cXkpHHs3obW0TSeiJeHa/Untitled`

Required final target frame:
`R1E_TYPOGRAPHY_PROOF`

Export exactly one review PNG:
`R1E_TYPOGRAPHY_PROOF.png`

Upload to:
`LIU_VISUAL_REVIEW/R1E/`

The Mother Reference image is not included in the final proof PNG.

## 13. Independent review gate

After Drive upload:

1. ChatGPT fetches the actual PNG pixels;
2. ChatGPT compares them directly against actual pixels of `R1C-APPROVED-05.jpg`;
3. user gives absolute judgment.

Required review dimensions:
- custom-glyph evidence;
- stroke energy;
- hierarchy;
- optical spacing;
- outer silhouette;
- controlled irregularity;
- visual authority;
- reference distance;
- stock-font residue.

The gate is strict:

`R1E_TYPOGRAPHY_PASS`

only if the title itself is good enough to justify building a composition around it.

Otherwise:

`R1E_TYPOGRAPHY_FAIL`

and no poster/composition stage may start.

## 14. Frozen project boundaries

During R1E:
- no new Discovery evidence;
- approved/rejected remains 18 / 12;
- no ImageGen;
- no food edits;
- no packaging;
- no R2;
- no new Skill promotion;
- no new reference set;
- no 13/16 reference blending.

## 15. Exit status

Technical completion status:

`R1E_TYPOGRAPHY_READY / WAITING_FOR_INDEPENDENT_PIXEL_REVIEW`

Visual status remains pending until ChatGPT + user review actual pixels.