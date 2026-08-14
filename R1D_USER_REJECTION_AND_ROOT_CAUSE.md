# R1D — USER REJECTION AND ROOT CAUSE

Status: `UNUSABLE / ABSOLUTE_REFERENCE_DISTANCE_FAILURE`
Date: `2026-08-14`

## User verdict

The R1D output is rejected on absolute quality. The user explicitly judged the result to be dramatically below the supplied references, described the reference-quality gap as approximately `100 vs 5`, judged the typography/design as very poor, and judged food realism as only minimally sufficient.

This overrides the previous provisional `PASS_WITH_CAVEATS / PROVISIONAL_USABLE` interpretation.

## Evaluator correction

The previous independent review made a methodological error: it gave too much weight to relative improvement versus R1B. That is not the project gate. The correct gate is absolute distance to the selected approved references and real-project usability.

Therefore:

`R1D = UNUSABLE / ABSOLUTE_REFERENCE_DISTANCE_FAILURE`

No R2, packaging expansion, Discovery expansion, or quality-pass claim is allowed.

## Root causes

### 1. Reference-binding regression at the design layer

R1C selected anchors from actual pixels, but R1D downstream execution received mainly textual abstraction of those anchors (composition role, typography role, product-derived graphic role) rather than a guaranteed direct pixel-bound visual reference inside the design execution context.

This reintroduced the same class of failure previously seen in generation: image evidence was compressed into prose before execution, losing high-dimensional visual information such as exact proportion, stroke energy, optical spacing, texture behavior, density, edge treatment, rhythm, and micro-hierarchy.

### 2. Three stylistically different anchors were blended into a generic hybrid

R1C-13, R1C-16, and R1C-05 each have strong but different authored visual languages. Combining them as abstract mechanisms diluted their authorship and produced generic derived graphics instead of a coherent mother style.

For the next proof, one reference must be the primary mother style. Additional references may only act as guardrails, not equal-weight ingredients.

### 3. Typography architecture was fundamentally underpowered

The reference designs rely on custom lettering / calligraphic or highly authored display typography. R1D used a standard editable Chinese serif treatment. Font selection is not typography design.

The previous requirement that all title typography remain ordinary live editable text over-constrained the design. For expressive display titles, custom vector lettering / outlined-and-edited glyph construction must be allowed, while functional supporting copy remains live editable text.

### 4. Figma scripting was treated as an art-direction engine

Figma is a construction environment. Programmatically placing text, arcs, dots, and an image can correctly implement geometry, but it does not itself supply expert visual judgment, optical correction, lettering craft, or authored composition.

The design process needs an explicit visual-reconstruction / design-judgment stage before final Figma construction.

### 5. One-shot diagnostic discipline was incorrectly carried into production-quality work

`one output / no retry / no variant` is useful for controlled experiments and capability diagnosis, but it is not a production craftsmanship workflow. High-end graphic design normally requires controlled revisions.

Future work may allow sequential, traceable revisions against a frozen failure list. This is not the same as generating random alternatives or best-of-N sampling.

### 6. Missing brand-specific source material

R1D was asked to achieve reference-level brand design using one dish image and two generic lines (`今日现烧` / `锅气刚好，趁热吃`) without a sufficiently rich brand identity, proprietary lettering system, or brand asset set. The reference images derive quality partly from coherent brand systems, not layout alone.

### 7. Food asset is only minimum-acceptable

The real-photo-first route successfully moved food from obvious AI/fake territory to plausible/usable realism, but the current food asset is not top-tier editorial food photography. It is acceptable as an input for design diagnosis, not yet a premium final hero asset.

## Next allowed step

Do not produce another final poster immediately.

First run a direct-pixel single-anchor reconstruction stage:

1. choose one primary mother reference whose actual pixels are bound directly into the design context;
2. reproduce its visual grammar with different content, without copying brand identity;
3. isolate typography as a separate proof before full layout;
4. allow custom vector display lettering;
5. compare against the mother reference directly on typography, composition, spacing, texture, image treatment, graphic-system coherence, and finish;
6. only after that passes, re-integrate the frozen dish asset;
7. no R2 / packaging / Discovery changes until absolute quality passes.
