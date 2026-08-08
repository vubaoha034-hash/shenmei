# Upstream and adaptation notes

This Skill is a repository-specific derivative of:

- Project: `gc-minimal-zine-poster`
- Author: LiamGvchi
- Upstream callable Skill: `gc-minimal-zine-poster-v0-1`
- Upstream repository: `LiamGvchi/gc-minimal-zine-poster`
- License: MIT

The upstream MIT license is preserved in this directory.

## Main adaptations in this repository

1. Change the default canvas from vertical `3:5` to horizontal `16:9` for travel-video frames.
2. Preserve recognizable evidence from the supplied photo/video frame instead of treating the prompt as a free-standing theme.
3. Add a travel-specific variation engine that rotates among torn-photo sticker, color-block collage, scenic print, contour/field map, architectural deconstruction, and symbolic silhouette treatments.
4. Make the chromatic anchor source-derived when possible, e.g. lake blue, red clothing, orange sand or green valley.
5. Require an English location label in available negative space when the place is known.
6. Prohibit invented coordinates, dates, weather, archive numbers and other fake factual metadata.
7. Add sequence rules so multiple frames from one trip share a paper/typographic system while avoiding repetitive template placement.
8. Explicitly exclude app UI, social-media overlays, player controls and top/bottom comparison chrome from the generated frame.

## Reference intent

The local adaptation is designed to reproduce the visual mechanisms seen in the supplied travel-video examples: broad 16:9 editorial frames, aged paper, halftone/risograph treatment, preserved scene geometry, large negative space, quiet English place labels, and visibly different collage/imagery treatments from frame to frame.
