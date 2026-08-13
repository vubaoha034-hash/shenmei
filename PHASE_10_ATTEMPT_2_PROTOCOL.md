# LIU VISUAL SYSTEM — PHASE 10 ATTEMPT 2 BLIND-SAFE RESTART

Status: `PRE_REGISTERED / NOT_STARTED`
Date: `2026-08-13`
Base protocol: `PHASE_10_FROZEN_CONTEXT_REPLICATION_PROTOCOL.md`
Attempt 1 status: `INVALID_BLIND_CONTAMINATION`

## 1. Why Attempt 1 cannot continue

Attempt 1 is permanently invalid because the first P10-01 output was shown to the voting user together with the `baseline` condition label before voting.

The invalid run must not be repaired in place.

Do not:

- regenerate P10-01 inside Attempt 1;
- reuse the Attempt 1 A/B mapping;
- continue from P10-02;
- delete the contaminated output or incident history;
- use the user's reaction to the contaminated output as Discovery Evidence;
- use the contaminated output/evidence in ContextPack or skill-refiner.

The contaminated output and incident stay quarantined as `blind_eval_reserved` / evaluation-only history.

## 2. Attempt 2 is a fresh experimental run

Attempt 2 must have:

- a new run ID;
- a newly verified frozen private snapshot;
- a new private blind ledger;
- a new cryptographically random A/B mapping;
- 20 newly pre-registered restaurant tasks;
- 40 newly generated outputs;
- no reuse of Attempt 1 outputs;
- no user-visible generation receipts before the blind package is complete.

The Phase 9 locked prior remains `Personalized 6 / Baseline 4 / Tie 0` for the combined pre-registered statistic.

## 3. Frozen personal state still cannot change

Attempt 2 continues to use the same frozen restaurant Discovery system:

```text
Discovery approved = 18
Discovery rejected = 12
Domain = 餐饮
positive max = 4
negative max = 2
Retrieval logic = unchanged
Router / Skill / Critic = unchanged
```

Before generating Attempt 2 outputs, recompute a fresh private replication snapshot and verify the current state matches the Phase 9 frozen Discovery state.

The previous snapshot hash may be compared for audit, but Attempt 2 must write its own snapshot receipt.

## 4. Prior exposure limitation

The voting user has previously seen one invalid Attempt 1 output labelled `baseline`.

This fact must be retained in the Attempt 2 report as:

```text
prior_condition_exposure = true
prior_exposed_attempt = attempt_1
prior_exposed_pair = P10-01
```

It does not authorize changing the primary decision threshold.

Attempt 2 must not show any further condition labels before all votes are locked.

## 5. New task pre-registration

Attempt 2 uses exactly 20 new tasks from:

`PHASE_10_ATTEMPT_2_TASKS.json`

They must preserve the original category balance:

```text
brand_key_visual = 4
promotion_poster = 4
food_product_visual = 4
menu_packaging = 4
store_social_system = 4
```

No Attempt 2 task may be identical to a PHASE 9 blind task or PHASE 10 Attempt 1 task.

No task may be replaced after Attempt 2 generation begins.

## 6. Blind-safe generation boundary

This is the critical correction.

During generation of all 40 Attempt 2 images, the voting user must not receive or see:

- individual image-generation tool receipts;
- renderer messages containing `baseline` or `personalized`;
- condition-specific prompt text;
- ContextPack contents;
- approved/rejected exemplar IDs;
- private output filenames containing condition labels;
- intermediate images before the full blind package is assembled.

Generation must occur through a private/non-user-visible worker boundary that writes outputs to private files.

If the available renderer/tool necessarily exposes condition labels, prompts, or individual outputs directly to the voting user during generation, stop with:

```text
ATTEMPT_2_BLOCKED_NO_BLIND_RENDER_PATH
```

Do not proceed by hoping the user ignores the receipt.

## 7. Opaque internal condition IDs

Private generation orchestration should use opaque condition tokens at the renderer boundary, such as:

```text
cond_x
cond_y
```

The mapping from opaque token to Baseline/Personalized stays only in the private blind ledger.

User-visible review assets must use only:

```text
Task ID
Image A
Image B
```

## 8. Pre-presentation leak audit

Before the user sees any Attempt 2 image, scan the complete blind review package and user-visible metadata.

The following strings/information must not appear:

```text
baseline
personalized
condition mapping
ContextPack
approved / rejected source role
private sample IDs used for personalization
condition-specific prompt text
```

Also verify user-visible filenames and captions do not reveal the condition.

If any leak exists, Attempt 2 is invalid before voting.

## 9. Pair symmetry

Each task still follows the frozen primary protocol:

- same task text;
- same route/Skill;
- same renderer/model/ratio/parameters;
- one Baseline generation;
- one Personalized generation;
- Personalized only receives the frozen bounded restaurant ContextPack;
- no selective repair/regeneration;
- renderer technical failure may invalidate the task but not trigger creative retry.

All outputs remain `blind_eval_reserved`.

## 10. User presentation

Only after all valid Attempt 2 pairs are generated, locked, snapshot-reverified, and leak-audited may the blind review package be shown.

The user receives all pairs without condition labels and votes only:

```text
A
B
tie
```

All votes lock before unblinding.

## 11. Scoring

Use the existing `summarize_replication` pre-registered rule without changing thresholds after seeing results.

Possible primary decisions remain:

```text
REPLICATION_PASS
INCONCLUSIVE
NOT_REPLICATED
INVALID
```

The final report must additionally disclose `prior_condition_exposure = true` as a limitation.

## 12. Stop rule

After Attempt 2 scoring:

- stop;
- do not automatically expand the image library;
- do not train from Attempt 1 or Attempt 2 blind outputs;
- do not convert the contaminated P10-01 reaction into Discovery Evidence;
- return the result for independent review.
