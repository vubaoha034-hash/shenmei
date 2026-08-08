# Upstream and locking notes

Canonical local Skill: `gc-travel-zine-poster-v1`

Derived from:

- Project: `LiamGvchi/gc-minimal-zine-poster`
- Upstream Skill: `gc-minimal-zine-poster-v0-1`
- License: MIT
- Upstream author: LiamGvchi

## Why this locked derivative exists

The upstream Skill establishes the core minimal-zine grammar: large negative space, restrained type, a small or controlled image anchor, one high-chroma color family, scanned paper, old-print defects, and rejection of commercial poster / dense scrapbook behavior.

This local derivative adds strict behavior required for transforming real travel and life-memory photos:

1. reference-first decomposition;
2. explicit source-image fidelity;
3. one source image per output;
4. user/reference/source aspect-ratio priority;
5. only one dominant transformation family per image;
6. source-derived accent color;
7. no invented in-image headlines or factual metadata;
8. prompt serialization so the image generator receives concrete rules rather than only a Skill name;
9. a hard anti-template / anti-scrapbook / anti-tourism-ad quality gate;
10. compatibility redirects from older local travel-zine Skill names.

The intent is to transfer visual mechanisms, not copy creator watermarks, account identifiers, exact microtext, or complete proprietary artwork.
