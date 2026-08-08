# Upstream and adaptation notes

This Skill is a repository-specific derivative of:

- Project: `gc-minimal-zine-poster`
- Author: LiamGvchi
- Upstream callable Skill: `gc-minimal-zine-poster-v0-1`
- Upstream repository: `LiamGvchi/gc-minimal-zine-poster`
- License: MIT

The upstream MIT license is preserved in this directory.

## Main adaptations in this repository

1. Replace the upstream fixed vertical `3:5` canvas with a **reference-first aspect-ratio policy**. Explicit user size wins; otherwise follow the supplied reference artwork; if no usable reference ratio exists, preserve the source photo/video ratio. `16:9` is used only when explicitly requested or naturally preserved from an already-16:9 source/reference.
2. Preserve recognizable evidence from the supplied photo/video frame instead of treating the prompt as a free-standing theme.
3. Add a travel-specific variation engine that rotates among torn-photo sticker, color-block collage, scenic print, contour/field map, architectural deconstruction, and symbolic silhouette treatments.
4. Make the chromatic anchor source-derived when possible, e.g. lake blue, red clothing, orange sand or green valley.
5. Add optional English location labeling in available negative space when the place is known and the reference composition supports it.
6. Prohibit invented coordinates, dates, weather, archive numbers and other fake factual metadata.
7. Add sequence rules so multiple frames from one trip share a paper/typographic system while avoiding repetitive template placement.
8. Explicitly exclude app UI, social-media overlays, player controls, black bars and top/bottom comparison chrome from both generated artwork and aspect-ratio analysis.
9. Add explicit reference decomposition: ratio, orientation, negative-space level, visual scale, paper family, image treatment, typography behavior, color logic and texture family are learned from the reference before generation.

## Reference intent

The local adaptation is designed to reproduce the **visual mechanisms** seen in supplied travel-zine references rather than force every image into the same layout. It studies the actual reference artwork area, then transfers its proportion, negative-space rhythm, paper/print treatment, restrained typography, source-derived color logic, and collage/imagery behavior to the user's own travel frame.

The directory and callable name still contain `16x9` for backward compatibility with the first installed version. This suffix no longer defines the default output ratio.
