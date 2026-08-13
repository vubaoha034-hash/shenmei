# PHASE 10A — GENERATION TRACE CONTRACT

Status: `REQUIRED_FOR_AUDIT`
Date: `2026-08-13`

Purpose: make the restaurant generation chain observable without turning trace metadata into preference truth.

All real traces are private runtime artifacts. Public Git may contain this contract and synthetic tests only.

## 1. One trace per generated condition

A trace represents one concrete renderer invocation, not a reusable preference record.

Minimum private trace:

```json
{
  "trace_version": "1",
  "trace_id": "trace_<opaque>",
  "task_id": "diag-01",
  "condition": "baseline|personalized|expert_direct",
  "task_text": "...",
  "route": {
    "route_id": "...",
    "evidence": "which START_HERE branch was selected and why"
  },
  "skills_read": [
    {"path": ".../SKILL.md", "git_blob_sha": "..."}
  ],
  "mandatory_files_read": [
    {"path": "...", "git_blob_sha": "..."}
  ],
  "compiler": {
    "name": "host/manual/skill compiler identifier",
    "output_text": "exact compiled prompt before renderer binding"
  },
  "context": {
    "domain": "餐饮",
    "positive_exemplars": [],
    "negative_exemplars": [],
    "source_event_ids": []
  },
  "reference_bindings": [],
  "renderer": {
    "tool": "...",
    "model": "...",
    "model_version": null,
    "ratio": "...",
    "parameters": {},
    "final_prompt": "exact text payload sent to renderer"
  },
  "output": {
    "sample_id": "...",
    "asset_id": "...",
    "sha256": "sha256:..."
  },
  "quality_gate": {
    "realism_status": "PASS|FAIL|NOT_RUN",
    "design_status": "PASS|FAIL|NOT_RUN",
    "absolute_quality": "USABLE|UNUSABLE|NOT_JUDGED",
    "reasons": []
  }
}
```

## 2. Reference binding proof

For every positive exemplar claimed to affect a Personalized renderer call, record:

```json
{
  "sample_id": "smp_...",
  "asset_id": "ast_...",
  "asset_sha256": "sha256:...",
  "resolved_path_or_private_ref": "...",
  "renderer_attachment_present": true,
  "renderer_attachment_sha256": "sha256:...",
  "renderer_attachment_index": 0
}
```

A positive exemplar is counted as **actually bound** only when:

1. the selected ContextPack contains that `asset_id`;
2. the canonical AssetRecord has an exact SHA-256;
3. the bytes/file reference resolved on the real host;
4. the renderer invocation explicitly includes that attachment/reference;
5. when bytes are inspectable locally, attachment SHA matches AssetRecord SHA.

If any step is missing, it is not proven multimodal personalization.

## 3. Bridge classifications

Allowed classifications:

```text
MULTIMODAL_BOUND
PARTIAL_MULTIMODAL_BOUND
TEXT_ONLY_PERSONALIZATION
UNPROVEN_BINDING
```

Definitions:

- `MULTIMODAL_BOUND`: every selected positive exemplar intended for the call is explicitly attached and hash/accounting agrees.
- `PARTIAL_MULTIMODAL_BOUND`: at least one but not all intended positive exemplars are attached.
- `TEXT_ONLY_PERSONALIZATION`: Context IDs/text are used but no selected positive image is attached.
- `UNPROVEN_BINDING`: host claims image use but does not expose enough invocation evidence to verify it.

`UNPROVEN_BINDING` is not treated as success.

## 4. Negative exemplar handling

Negative/rejected examples must have an explicit strategy in the trace:

```text
not_used
textual_avoid_summary
multimodal_negative_reference_if_renderer_supports_semantics
```

Do not silently attach rejected images as ordinary positive references. If the renderer has no reliable negative-reference semantics, prefer a small evidence-backed textual avoid statement.

## 5. Prompt provenance

Record three text layers separately:

```text
Task brief
→ compiler output
→ final renderer prompt
```

Do not store only the final prompt if it prevents identifying where a cliché or rule loss was introduced.

The audit must answer:

- Did the Skill compiler generate a concrete imageable direction?
- Were mandatory realism/anti-template constraints preserved or dropped?
- Was the prompt overloaded with explanation/checklists?
- Did the host inject generic words such as "Chinese", "oriental", "ink", "brush", "premium" that were not demanded by the task or Skill?

## 6. Route proof

For each diagnostic task, the trace must state which root route was selected:

```text
A — complete restaurant brand case
B — single poster / product visual
C — editable Figma brand system
```

and list the actual Skill(s) read.

A route label without file evidence is insufficient.

## 7. Quality-gate proof

The output must be judged before it is considered a valid generation result for an experiment.

Correctness/realism checks should apply existing mandatory rules. For the audit, at minimum flag:

```text
plastic/waxy/rubbery food
uniform mirror gloss
copied/repeated ingredients
impossible food/utensil/contact geometry
steam detached from heat source
background/food looking like separate layers
default ink/brush/seal cliché
template repetition
```

Absolute quality is independent:

```text
USABLE = user would plausibly use the image in a real project without redesigning the core visual concept
UNUSABLE = pairwise preference may exist, but the image is below production floor
```

## 8. Privacy

Real trace artifacts may contain:

- private paths;
- sample IDs;
- prompt history;
- renderer receipts;
- private reference filenames.

Therefore real traces live only under the private data root and are never committed to public Git by default.

## 9. Stop conditions

Stop before the 9-image diagnostic if any is true:

```text
route cannot be reconstructed
actual Skill files read are unknown
final renderer prompt is unavailable
reference binding cannot be inspected at all
renderer identity/settings cannot be captured
```

In that case, fix observability first. Do not continue generating more images to gather aesthetic evidence from an untraceable chain.
