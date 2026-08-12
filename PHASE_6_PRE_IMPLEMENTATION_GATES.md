# LIU VISUAL SYSTEM — PHASE 6 PRE-IMPLEMENTATION GATES

Status: `REQUIRED_AFTER_FREEZE`
Date: `2026-08-12`
Applies to: first Scaffold and first real personal Pilot after `ARCHITECTURE_V0.1_FROZEN.md`

Purpose: prevent a technically correct architecture from becoming an unsafe or misleading Pilot implementation.

These are implementation entry gates, not new raw record families or infrastructure mandates.

---

# Gate A — Scaffold boundary

The first implementation phase may create only the minimum infrastructure required to prove the frozen contract.

Allowed initial scope:

```text
record serialization/schema
stable ID generation
SHA-256 exact hash
private-root path/config boundary
basic asset resolution
append-oriented EvidenceEvent write
record read/replay
correction/retraction replay
tombstone exclusion
minimal generation logging
basic integrity checks
small synthetic fixtures/tests
```

Do not introduce during minimal Scaffold unless a measured blocker appears:

```text
vector DB
embedding service
object store vendor
perceptual duplicate service
microservices
queue/workflow engine
trained preference model
multi-user support
multi-writer protocol
new top-level visual Skill
new critic
new Skill-promotion engine
```

---

# Gate B — Public repository privacy

Before any real personal data is written:

```text
[ ] canonical raw store resolves outside public Git
[ ] asset-vault location resolves outside public Git by default
[ ] test fixtures in Git are synthetic/non-sensitive
[ ] no private source paths or user feedback are committed accidentally
[ ] public calibration file is not used as a sink for private personal anchors
```

If these fail, real personal Pilot ingestion is blocked.

---

# Gate C — Raw persistence integrity

Before real Pilot:

```text
[ ] stable IDs survive file move/rename
[ ] SampleRecord and AssetRecord identity are separate
[ ] SHA-256 is validated as exact-blob hash only
[ ] EvidenceEvent original raw_text survives round trip
[ ] correction/supersede/retract replay produces correct effective state
[ ] a failed raw write is detected and not reported as learned
```

---

# Gate D — Backup / recovery

Before accumulating non-disposable personal evidence:

```text
[ ] raw structured store can be backed up/exported
[ ] required Asset Vault bytes can be backed up/exported
[ ] recovery test restores stable IDs and cross-record references
[ ] restore does not require user relabeling
```

A backup policy that has never been restored once is not considered verified.

Exact backup technology is not prescribed.

---

# Gate E — Deletion / purge

Before real private Pilot data scales beyond disposable test records:

```text
[ ] tombstoned records disappear from runtime retrieval
[ ] tombstoned records disappear from derived-profile building
[ ] tombstoned records disappear from eval selection
[ ] a documented physical-purge path exists for requested sensitive raw data/assets
[ ] derived outputs that include purged IDs can be deleted/rebuilt
```

No complex deletion service is required initially; deterministic/manual tooling is acceptable if reliable and documented.

---

# Gate F — Imported historical evidence fidelity

Historical chat/project memories are not automatically raw preference evidence.

Before importing any historical evidence:

```text
[ ] original user wording or original explicit structured action is available
[ ] origin is traceable enough to distinguish imported evidence from new current evidence
[ ] assistant summary/paraphrase is not substituted for missing original evidence
[ ] uncertain scope remains unspecified
```

If original evidence is unavailable, store only a derived note if useful.

---

# Gate G — Blind evaluation isolation

Before running any architecture/profile comparison:

```text
[ ] reserved samples are marked before discovery/tuning sees them
[ ] blind-case generated outputs are quarantined from discovery
[ ] EvidenceEvents generated from blind-case judgments are quarantined from discovery
[ ] blind-case IDs cannot be bridged to skill-refiner
[ ] production regression cases are labeled separately from blind cases
```

Any contamination invalidates that blind evaluation result.

---

# Gate H — Asset-resolution truthfulness

For every selected exemplar at runtime, the implementation can state:

```text
known?
selected?
resolvable?
actually inspected?
```

No visual claim may rely on a sample that was not actually resolved/inspected in that runtime.

An unavailable sample is not automatically removed from preference history.

---

# Gate I — Calibration privacy compatibility

Before enabling formal private `personal_fit`:

```text
[ ] anchors are projected from eligible raw explicit user evidence
[ ] anchor asset bytes are inspectable in the critic runtime
[ ] critic-category mapping is derived, not written into raw evidence
[ ] private calibration material does not enter public Git by default
[ ] unsupported domain mapping returns null/unavailable rather than forced category
```

Until this passes:

```text
personal_fit = null
```

is the required safe behavior.

---

# Gate J — Runtime context precedence

Test cases must verify:

```text
historical preference cannot override current explicit user request
one domain preference cannot silently leak into unrelated domain
current task still works when derived profiles are absent
current task still works when selected exemplars are unavailable
```

VisualContextPack must remain small enough that it does not recreate an alternate visual Skill grammar.

No exact token count is frozen; inspectability and boundedness matter more than an arbitrary number.

---

# Gate K — Existing-system authority

Before Pilot:

```text
[ ] existing START_HERE / AGENTS routing still owns route selection
[ ] personal context does not create a competing Router authority
[ ] critic output cannot write raw preference events
[ ] raw feedback cannot modify production Skills directly
[ ] durable Skill changes still require existing skill-refiner + eval + Git review
```

---

# Gate L — Rebuild proof

Before declaring Scaffold complete, perform one destructive derived-layer test:

```text
1. create synthetic raw Samples/Assets/Evidence/Generation records
2. build any initial derived compatibility/profile output
3. delete the derived output
4. rebuild it from raw
5. verify no user labeling/input was needed for rebuild
```

If derived state cannot be deleted and rebuilt, implementation violates the frozen architecture.

---

# Gate M — Minimal synthetic verification before personal Pilot

Do not begin with hundreds of real references.

First use a tiny synthetic/non-sensitive fixture set to verify:

```text
ID stability
hash behavior
record links
correction/retraction
pairwise event
revision event
generation lineage
tombstone
blind-eval isolation
asset-resolution failure
rebuild
backup/restore
```

Only after these pass should real personal Pilot data be added.

---

# Gate N — First personal Pilot size

Architecture Freeze does not prescribe an exact training dataset size, but the first real Pilot must remain deliberately small.

Recommended order of magnitude:

```text
~20–50 useful reference/positive samples
~10–20 rejected/negative samples
naturally occurring A/B and Before→After evidence
small separate blind-eval reserve
```

These are operating guidance, not frozen schema requirements.

Do not bulk-ingest the full library before the small Pilot proves that capture, retrieval, correction, privacy, and rebuild behavior are correct.

---

# Gate O — Pilot success questions

Before scaling, the Pilot must answer with evidence:

```text
1. Does relevant personal context improve blind/user preference vs baseline?
2. Does it reduce revision rounds?
3. Does retrieval select references the user recognizes as relevant?
4. Does the system avoid repeating known rejected mechanisms?
5. Can incorrect derived interpretation be deleted/rebuilt without raw damage?
6. Can current explicit instructions override history cleanly?
7. Can data be backed up/restored/deleted without relabeling?
```

If not, debug the smallest failing layer rather than adding more Skills/rules/infrastructure.

---

# Final gate

The next implementation phase may start minimal Scaffold work because Architecture V0.1 is frozen.

Real personal Pilot ingestion remains blocked until the relevant gates above pass.
