# ADR-005 — Runtime Personal Context Is Host-Level, Bounded, and Subordinate to Current Intent

Status: `ACCEPTED_FOR_V0.1`
Date: `2026-08-12`

## Context

PHASE 4 proposes a `VisualContextPack` assembled from current task intent, scoped preference projections, and a small set of relevant exemplars. The repository already has routing and mature visual Skills. Creating a new permanent top-level personal visual Skill solely to inject memory would add trigger collisions and prompt bloat.

## Decision

Personal visual context is integrated at the **host/runtime orchestration layer before the selected existing visual Skill executes**.

A dedicated new top-level Skill is not required for V0.1.

Runtime precedence is:

```text
current explicit user instruction
>
current task constraints
>
explicit scoped historical evidence
>
confirmed durable/global evidence
>
derived historical inference
```

The `VisualContextPack` is:

- ephemeral;
- bounded;
- evidence-cited;
- task-specific;
- not a new source of truth.

It may contain:

```text
small scoped preference summary
selected positive/reference exemplars
selected negative/rejected exemplars
known relevant anti-patterns
asset-resolution status
source evidence IDs
```

It must not contain a copy of the entire evidence ledger, entire visual Skill, or hundreds of accumulated taste rules.

If context assembly fails, generation may proceed using the current explicit request and any explicit references the user supplied in the current task.

## Alternatives Considered

### A. Create `$liu-visual-director` as mandatory front door

Rejected for V0.1. The missing capability is personal evidence/context, not another routing layer.

### B. Append all personal history into every visual Skill prompt

Rejected. It would recreate the repository's documented rule-bloat failure mode.

### C. Fully dynamic retrieval with no stable constraints

Rejected as the exclusive strategy. Confirmed critical cross-domain constraints may be included in a tiny derived core, but that core may remain empty.

## Consequences

Positive:

- existing visual Skills stay focused;
- current instructions cannot be overridden by old preference guesses;
- context strategy can change without changing Skill topology;
- prompt size remains controllable.

Negative:

- the host/runtime needs an integration point before Skill execution;
- environments without personal-memory access fall back to ordinary existing behavior.

## Migration Impact

A future plugin, tool, Skill, or host-native memory implementation may replace the context assembler without changing raw records or existing visual Skills, provided precedence and authority rules remain intact.

## Revisit Trigger

Revisit only if repeated measured routing/integration problems prove that a thin dedicated entry Skill materially improves reliability.
