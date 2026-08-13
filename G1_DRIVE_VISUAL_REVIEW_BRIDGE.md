# G1 — GOOGLE DRIVE VISUAL REVIEW BRIDGE

Status: `PROVEN_FOR_SINGLE_IMAGE_REVIEW / NOT_A_G1_PASS`
Date: `2026-08-13`

## Purpose

Provide a reliable external review path so Codex-generated images can be inspected by a separate visual reviewer that actually sees the image pixels, rather than relying on Codex self-evaluation, logs, filenames, prompts, or validator output alone.

This bridge is part of the value-first control path. It does not itself prove renderer reference binding, routing correctness, prompt quality, or production quality.

---

## Proven single-image path

The following path has been exercised successfully:

```text
local Codex / Windows host
→ Google Drive sync/upload
→ private Drive folder LIU_VISUAL_REVIEW/G1/
→ ChatGPT Drive search/folder enumeration
→ raw image download
→ actual pixel-level visual inspection
```

Probe asset:

```text
LIU_G1_DRIVE_PROBE_001.png
```

Observed Drive file ID:

```text
1qK2WSPiwYwBL9WRA4rvT7Wi6T0sOE3oq
```

The file remained private/not shared during the probe.

The reviewer was able to identify actual image content from pixels, proving this was not metadata-only access.

---

## Important format finding

The probe filename ended in `.png`, but Google Drive reported the actual MIME type as:

```text
image/heif
```

Downloaded file identity was effectively:

```text
LIU_G1_DRIVE_PROBE_001.png.heif
```

Therefore future review assets must preserve extension/MIME consistency.

Required rule:

```text
actual PNG bytes  → .png
actual JPEG bytes → .jpg/.jpeg
actual HEIF bytes → .heif/.heic
```

Do not rename HEIF bytes to `.png` merely for convenience.

---

## Review authority boundary

For any future claim about final visual quality:

```text
Generation completed
≠
Quality reviewed
≠
USABLE
```

A final visual-quality PASS requires at least one reviewer that actually inspected the rendered pixels.

Codex self-evaluation alone cannot establish:

- product realism;
- material realism;
- composition quality;
- visual taste;
- template collapse;
- production usability.

Logs, prompts, validators, and metadata may support the review but cannot substitute for pixel inspection.

---

## Proposed review folder structure

```text
LIU_VISUAL_REVIEW/
├─ G1/
├─ G3/
├─ G4/
├─ G5/
└─ archive/
```

The folder is a review transport surface, not a second Raw Evidence truth store.

Canonical personal evidence remains in the private visual-memory store.

---

## Naming rules

For non-blind diagnostic work:

```text
<GATE>_<TASK_ID>_<VARIANT>.<ext>
```

For blind work, never expose semantic condition labels such as:

```text
baseline
personalized
expert
```

Use opaque presentation names only, for example:

```text
P10A2-01-A.png
P10A2-01-B.png
```

The true condition mapping stays in the private blind ledger.

---

## What this probe proved

`PROVEN`:

- Drive folder can be located from the connected ChatGPT environment;
- private image files can be identified;
- raw image can be downloaded;
- actual pixels can be inspected by the reviewer;
- public sharing is not required.

`NOT PROVEN`:

- multi-image batch reliability;
- automatic upload from Codex without human supervision;
- renderer reference binding;
- renderer/model identity;
- prompt/compiler correctness;
- visual quality of generated assets;
- blind-review package safety at scale.

---

## G1 relationship

This bridge solves only the `external pixel review availability` subproblem.

G1 still requires proof of:

```text
Task
→ Router
→ Skill
→ Compiler output
→ ContextPack
→ selected reference assets
→ actual renderer attachments
→ final renderer prompt
→ renderer/model/parameters
→ output
→ quality-gate execution
```

Therefore:

```text
DRIVE REVIEW BRIDGE = PASS
G1 END-TO-END GENERATION TRACE = NOT YET PASS
```

---

## Permanent rule

Any stage that claims final visual quality must make the actual image pixels available to an independent visual reviewer.

No stage may claim visual-quality PASS from Codex self-report alone.