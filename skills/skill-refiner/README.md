# skill-refiner

Evidence-gated continual improvement for Agent Skills, agent operating rules, and repository/coding workflows.

The design deliberately separates **learning state** from **core instructions**:

- raw observations live in `.skill-evolution/<target>/state.json`;
- detailed knowledge should normally move to `references/` or executable `scripts/`;
- core `SKILL.md` changes are promotion-gated and size-budgeted;
- promotion requires regression evaluation and a reviewable Git change;
- stale unlinked evidence is archived, not loaded forever.

## Quick check

```bash
python skills/skill-refiner/tests/test_evolve.py
```

## Main CLI

```bash
python skills/skill-refiner/scripts/evolve.py --help
```

The Skill instructions in `SKILL.md` are authoritative.
