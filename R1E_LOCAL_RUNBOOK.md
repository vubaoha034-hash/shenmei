# R1E — LOCAL RUNBOOK

Status: `EXECUTION_RUNBOOK`
Protocol: `R1E_DIRECT_REFERENCE_TYPOGRAPHY_PROOF_PROTOCOL.md`

## 0. Preflight

Verify:
- current branch is `r1e-direct-reference-typography-proof-20260814`;
- protocol exists and is unchanged;
- `doctor() == []`;
- Discovery remains `approved 18 / rejected 12`;
- Figma account is writable;
- target Figma file is accessible:
  `https://www.figma.com/design/d3cXkpHHs3obW0TSeiJeHa/Untitled`.

If any item fails, stop before design.

## 1. Bind Mother Reference 05 directly

Fetch exact Mother Reference:
- neutral name: `R1C-APPROVED-05.jpg`;
- Drive file ID: `1M2sI6Q1TfPszHpORj29eY9sr-JDO3Co9`.

Place the actual reference raster into the Figma file in a clearly named section/frame:

`R1E_REFERENCE_LOCK`

Rules:
- full image visible at useful size;
- no contact sheet;
- no crop that hides relevant lettering;
- no AI modification;
- no color treatment;
- no replacement with screenshot if original raster can be used;
- keep the reference visible throughout all design passes.

Record:
- reference node ID;
- source file ID;
- source SHA if available from local/private mapping.

If reference pixels cannot be bound, stop with:
`R1E_BLOCKED_REFERENCE_NOT_BOUND`.

## 2. Create one target proof frame

Create exactly one design frame:

`R1E_TYPOGRAPHY_PROOF`

Dimensions:
`1080 × 1350`.

Background:
- warm off-white / near-white;
- no decorative texture.

Do not place food or any other visual asset.

## 3. Preserve live source text

Create a live editable text layer outside the final export frame:

`SOURCE_TEXT_LIVE`

Content exactly:
`今日现烧`

Use one real installed Chinese font as the initial skeleton.

Record:
- font family;
- font style;
- text layer node ID.

This layer is provenance only and must not be the visible final title.

## 4. Construct visible vector lettering

Create:

`LETTERING_VECTOR`

The visible target title must be vector lettering.

Process:
1. duplicate the live text or otherwise create vector outlines from the real font skeleton;
2. convert to editable vector paths;
3. reconstruct the four characters as a single designed lettering object.

Required intervention classes:
- at least one character must have altered width/height proportion;
- at least one character must have altered stroke/terminal/cut geometry;
- relative positions of the four characters must not be a normal text baseline;
- at least one internal negative space/counter must be optically adjusted;
- global outer silhouette must be intentionally shaped rather than a normal four-character text box.

These are construction checks, not aesthetic PASS criteria.

Forbidden:
- leaving four stock-font glyphs unchanged;
- only changing font size/weight/tracking;
- only splitting into two text boxes;
- applying drop shadows, glow, bevel or effects to hide weak glyph design;
- using an AI-generated raster title.

## 5. Direct comparison loop

The reference must remain visible next to the target while editing.

Maximum 3 total passes on the same `LETTERING_VECTOR`:

### Pass 0 — First construction
Focus only on:
- character mass;
- hierarchy;
- silhouette;
- initial stroke energy.

### Pass 1 — Reference-distance correction
Compare actual pixels/shape directly against Mother Reference 05 and revise only the same lettering object.
Focus on:
- stock-font residue;
- over-regular spacing;
- weak character contrast;
- weak terminal behavior;
- timid asymmetry.

### Pass 2 — Final optical refinement (optional)
Use only if needed.
Focus on:
- optical spacing;
- counters;
- local stroke balance;
- outer silhouette;
- reading order.

No Pass 3.
No alternate target.
No new style.

## 6. Private revision log

Create a private runtime log, not a new public design artifact:

`R1E_TYPOGRAPHY_REVISION_LOG.json`

For each pass record:
- pass number;
- issue classes observed;
- exact modifications;
- node IDs modified;
- whether Mother Reference remained visible;
- whether any alternate design was created (`must be false`).

Do not use the log to declare visual quality.

## 7. Technical audit before export

Verify:
- one Mother Reference raster is directly bound;
- exactly one target proof frame exists;
- `SOURCE_TEXT_LIVE` exists and is editable text;
- `LETTERING_VECTOR` exists and is vector paths;
- target visible text content reads `今日现烧`;
- no food image in proof;
- no subtitle;
- no English;
- no icon system;
- no ImageGen use;
- no second design;
- revision count <= 3;
- Discovery unchanged.

## 8. Export

Export exactly one review PNG from `R1E_TYPOGRAPHY_PROOF`:

`R1E_TYPOGRAPHY_PROOF.png`

Target export:
`1080 × 1350` PNG.

Upload to:
`LIU_VISUAL_REVIEW/R1E/`

Drive folder should contain only the final review PNG for this stage.

Do not upload intermediate passes.
Do not upload the Mother Reference again unless needed for transport; it already exists in R1C.

## 9. Final report contract

Return only:

# R1E TYPOGRAPHY READY

Branch:
HEAD:
Figma account:
Figma writable:
Figma file:
Mother Reference:
Mother Reference bound as actual pixels:
Mother Reference node ID:
Target frame node ID:
SOURCE_TEXT_LIVE:
Starting font:
LETTERING_VECTOR:
Vector reconstruction performed:
Sequential passes used:
Alternate designs created:
Food used:
ImageGen used:
Export PNG:
Drive upload:
Independent pixel review:
Discovery changed:
R1E status:

## 已完成什么

## 未完成什么

## 是否始终直接绑定 Mother Reference 05

Hard required values:
- Mother Reference bound as actual pixels = YES
- Vector reconstruction performed = YES
- Sequential passes used <= 3
- Alternate designs created = 0
- Food used = NO
- ImageGen used = NO
- Independent pixel review = PENDING
- Discovery changed = NO
- R1E status = `TYPOGRAPHY_READY / WAITING_FOR_INDEPENDENT_PIXEL_REVIEW`

Then STOP.

Do not start poster composition.
Do not start R2.
Do not modify Discovery.