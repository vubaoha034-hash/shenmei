# Upstream source

Canonical local wrapper: `gc-travel-zine-poster-v1`

Upstream:

- Project: `LiamGvchi/gc-minimal-zine-poster`
- Skill: `gc-minimal-zine-poster-v0-1`
- Upstream `SKILL.md` blob SHA: `7b6cbbdfcd660e979ea8db6fed57816584170103`
- License: MIT
- Author: LiamGvchi

## Vendored mirror

`UPSTREAM_SKILL.md` is a verbatim local mirror of the upstream `SKILL.md` at the blob SHA above.

The purpose of the mirror is to prevent future local rewrites from silently replacing the upstream prompt compiler and visual grammar.

## Local delta

The wrapper is intentionally thin. It may only adapt:

1. output aspect ratio when the user, reference artwork, or real source image requires a different canvas;
2. recognizable source-photo content as the upstream Image Anchor material;
3. factual place text explicitly supplied by the user;
4. one-source-one-output delivery for batches when requested.

It does **not** define a replacement art direction, visual-family taxonomy, percentage thresholds, structural-translation framework, or aesthetic validator.

If a future change needs to alter upstream composition, color, typography, texture, variation, prompt shape, or quality gate, it should be treated as a new experimental Skill rather than silently added to this wrapper.
