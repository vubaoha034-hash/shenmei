# V3 Semantic Identity and Transfer Contract

The core semantic identity record is domain-neutral: it identifies the subject,
aliases, primary entity, process, visible identity cues, forbidden
substitutions, source suitability, evidence authority, and confidence. Domain
adapters may add fields but may not weaken core identity or provenance.

The restaurant adapter maps `primary_entity` to primary ingredient/protein and
adds cooking-method semantics. It is not part of the V3 aesthetic core.

Each transfer plan must declare preconditions, grammar expected to survive,
allowed variation, semantic identity requirements, content compatibility,
actual reference attachments, the expected anchor-dependence test, failure
criteria, and complete renderer provenance requirements.

Minimum operators are `RECONSTRUCT`, `CONTENT_SWAP`, and
`COMPOSITION_OR_ASPECT_TRANSFER`. A missing semantic identity contract may be a
hard precondition failure for product-legibility work even when the visual
family contract is otherwise valid.
