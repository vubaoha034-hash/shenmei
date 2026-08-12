# ADR-008 — Only Explicit User Evidence Enters the Raw Preference Ledger

Status: `ACCEPTED_FOR_V0.1`
Date: `2026-08-12`

## Context

The long-term value of LIU VISUAL SYSTEM depends more on evidence quality than on model sophistication. The highest-risk failure is silently treating weak signals—uploading an image, lack of complaint, AI critic scores, assistant summaries, or renderer behavior—as if they were confirmed personal taste.

Once contaminated evidence influences future generations, it can create a self-reinforcing loop.

## Decision

The raw `EvidenceEvent` preference ledger accepts only:

```text
direct current user evidence
or
faithfully imported historical user evidence with traceable origin
```

Qualifying examples:

```text
“这张喜欢。”
“这张不喜欢。”
“A比B好。”
“这个太脏。”
“把这个范围缩小。”
“这版好多了。”
“刚刚那句话我说错了。”
```

Hard rules:

1. uploading or supplying a reference image alone is **not** approval;
2. silence is **not** approval;
3. task completion is **not** approval;
4. an AI critic score is not user preference evidence;
5. LLM interpretation/summary is not raw preference evidence;
6. prompt text is not raw preference evidence;
7. professional aesthetic rules are not user preference evidence;
8. assistant-generated revisions without direct user instruction do not create raw user `revision` events;
9. corrections/retractions are appended as new user events rather than overwriting old wording;
10. when explicit intent is ambiguous, preserve raw text and leave structured verdict/scope unknown instead of inventing certainty;
11. routine successful turns do not need learning events unless the user expresses evidence-worthy preference.

The human interaction budget remains minimal: natural reactions are sufficient; no mandatory labeling form is introduced.

## Alternatives Considered

### A. Treat all uploaded references as positive anchors

Rejected. A user may provide an image for criticism, comparison, or partial mechanism reference without liking the whole work.

### B. Infer approval from no further revision request

Rejected. Silence is ambiguous and would create large amounts of false-positive data.

### C. Let the critic write preference labels automatically

Rejected. Professional quality and personal taste are different authorities.

### D. Require explicit structured labeling forms

Rejected. Human burden would likely kill the learning loop.

## Consequences

Positive:

- raw evidence stays high precision;
- personal memory remains auditable;
- derived models can be rebuilt without inheriting silent labels;
- user corrections have a clean semantics.

Negative:

- the dataset grows slower;
- some useful weak signals are intentionally ignored as raw truth;
- derived analytics may later use weak signals separately, but they cannot silently promote them to personal truth.

## Migration Impact

This ADR reduces future cleanup cost. Relaxing the rule later is possible because weak signals can be added as a separate derived/telemetry layer. Cleaning contaminated raw evidence later would be much more expensive.

## Revisit Trigger

Revisit only if a later system can demonstrate a clearly separated, auditable weak-signal layer whose labels never masquerade as direct user preference evidence.
