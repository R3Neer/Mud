# Risks and restrictions

## Conceptual risks

### To confuse semantic representation completely architecture-independent

All semantics An executable implies decisions: identity, atomicity, concurrency, error, time and chance. MUD can do without React or a database, but it cannot be neutral with regard to its own model operational.

Mitigation: treat those decisions as semantics explicitly define them and test them using different implementations.

### Promising regeneration without specifying the boundaries

The generated code may require manual integration. If that integration contains rules for domain, `.mud` is no longer the source of truth.

Mitigation: clear contracts, generated zones, explicit adaptors and tests that compare behaviour.

### Natural language as an incidental source

If the AI ‘remembers’ an intention that was not recorded in `.mud` or in versioned metadata, the system retrieves semantics invisible.

Mitigation: after each operation, any lasting effect must remain in the source or decision revised.

### Early overextension

The specification It combines compilation, reactive runtime, state tracking, generation, AI integration and Git. Implementing it horizontally can produce many components without a contract verifiable.

Mitigation: first complete the formalisation of MUD 1.0 in accordance with [[notes/decisions/ADR-013-formalizacion-completa-antes-de-implementar|D-013]] and then validate the implementation using vertical sections and scenarios of conformance.

## Semantic risks

### No determinism accidental

You can browse by map, explore the collections, resolution statements `using`, coincidence or chance.

Mitigation: canonical order, explicit seeds, repeated tests and byte-by-byte comparison of IR and traces.

### No termination

Reactive rules can fluctuate or simulate unbounded computation.

Mitigation: cycle detection, restricted profiles and diagnostics that distinguish between technical limitations and contradictions semantics.

### Invalid intermediate states

Validating at different times can affect which rules are triggered and which actions are accepted.

Mitigation: semantics Small-scale operational testing in stages and comprehensive trace testing.

### Combinatorial explosion

Multiple links, calculated fields, `allowed` y `eventually` can grow exponentially.

Mitigation: metrics, conservative analysis, transparent technical specifications and advanced features outside the core.

### Identity unstable

Renaming or moving MUD paths changes anchors and may break history, references and persisted states.

Mitigation: Migrate first-class anchors before allowing automatic refactoring.

## Tooling risks

### Desynchronised derivatives

Graph, tax reference number, code or documentation may not correspond to the same one model.

Mitigation: source content and compiler version are recorded in each derivative; full reconstruction is available.

### Corrupted commits

An automation may include previous changes made by the user or unrelated artefacts.

Mitigation: index An isolated worktree, a file allowlist and a comparison of the diff against the plan.

### Incomplete rollback

Editing source code, generating files and running formatters leaves several areas that need to be restored.

Mitigation: transactional staging in a temporary area and publication only after validation, rather than ‘undoing’ partial changes.

### Inadequate diagnostics

A `failed` without a chain causal The MUD’s main promise is once again in doubt.

Mitigation: codes for error stables, anchors, ranges, waves, readings/escrituras and suggestions for corrections.

## Risks associated with future developments

### IR has become an accidental API

Materialisers and plug-ins can be linked to placeholder details.

Mitigation: outline version, compatibility declared and migration evidence.

### Syntax frozen too soon

Optimise for readability before stabilising the semantics leads to costly migration.

Mitigation: addressing the grammar established by [[notes/decisions/ADR-057-gramatica-concreta-y-continuacion|D-057]] as a regulatory proposal subject to document lifecycle; validate real-world examples and record any changes through standardisation, decision y conformance.

### Silent decisions during implementation

A developer will fix any inevitable gaps if the tests require it.

Mitigation: the implementation must be able to select ‘not specified’ and link to the open-ended question, rather than choosing an arbitrary behaviour.

## Non-negotiable restrictions

- `.mud` is the sole source of behaviour for domain.
- Interim results are not published.
- An invalid change does not result in a commit.
- Derivatives can be reconstructed.
- Boolean rules are pure.
- External writing is expressed through actions.
- Participants and `given` remain apart.
- The result It does not depend on random order.
- Unresolved issues are not resolved without provenance.
- The implementation cannot silently extend the language.

## Warning signs during development

Stop and check whether any of the following situations occur:

- “For the time being, the order will be as given in the dictionary.”
- “The generator can add this validation”.
- “This case returns a false result because it’s easier.”
- “We’ll only keep this rule in the prompt.”
- “We’ll migrate the anchors later.”
- “The boundary of waves defines meaning.”
- “The parser will make a decision based on context, even if the grammar is ambiguous.”
- “The commit also includes these changes, but they appear to be related.”

