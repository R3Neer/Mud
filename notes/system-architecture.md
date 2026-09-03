# System architecture

Architecture must make a boundary visible: `.mud` contains semantics; everything else interprets, verifies, query or brings that about semantics.

## View by component

```text
Natural language / CLI / editor
              │
              ▼
      Semantic operator
   intent, impact, operations
              │
              ▼
       Model service
 .mud files + agenda + transaction
              │
              ▼
          Compiler
 scanner → CST → Surface AST
              │
              ▼
      nominal resolution
              │
              ▼
          nominal HIR
              │
              ▼
      typing + elaboration
              │
              ▼
 future semantic representation
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
 queries  runtime  materialisers
                   TypeScript, docs, tests
```

The current regulatory chain runs through the Surface AST and Nominal HIR. Typing and elaboration are later architectural phases; no regulatory framework yet defines the semantic representation they will produce.

## Source and derivatives

Source semantics:

- `.mud` files.

Metadata for governance, no semantics from the world:

- Specification roadmap.
- Decision record.
- Project settings.

Reconstructible derivatives already defined:

- Tokens and lossless CST.
- Surface AST.
- Table of symbols, scopes and bindings.
- Anchor index.
- Nominal HIR and its nominal graph ownership, specialisation and reference.

Derivatives or subsequent representations not yet established by a complete contractual regulatory mechanism:

- Types and effective contracts resulting from classification and elaboration.
- Semantic representation after typing and elaboration.
- Subsequent semantic graphs and indices, such as reads, writes, effects or elaborated dependencies.
- Materialised code.
- Generated tests and documentation.
- Editor support that depends on later stages.

The roadmap and decisions should not conceal world behaviour; their function is to govern the evolution of the specification.

## Compiler

Current or planned separation:

1. **Scanner and contextual classification**: tokens, trivia, comments, verbatim quotations and context-dependent lexical classification where applicable.
2. **Parser**: Lossless CST, syntactic structure and error correction.
3. **Surface AST**: a semantically relevant form of the syntax, retaining provenance enough.
4. **Nominal resolution**: MUD paths, `using`, names, scopes, symbols, bindings and anchors.
5. **Nominal HIR**: current regulatory framework for resolution, limited to nominal information.
6. **Classification and elaboration**: types, cardinalities, domains, conversions, mutability and other contracts that require information in addition to names.
7. **Subsequent semantic analyses**: purity, effects, cycles, finiteness, stochasticity and other advanced properties.
8. **Later semantic representation**: this may come into effect once the preceding stages have been sufficiently formalised; its specific details have not yet been finalised.
9. **Consumers**: runtime, queries, diagnostics, materialisers and editor support.

The parser should not directly generate an elaborated semantic representation. This separation makes it possible to trace errors, resolve names before typing and prevent premature IR decisions from influencing language aspects not yet formalised.

## Surface AST and Nominal HIR

The Surface AST primarily answers: ‘Which semantically relevant construction was written, and where does it come from?’ The Nominal HIR asks: ‘Which symbols, scopes, owners, bindings, anchors and nominal relations result after name resolution?’

The Nominal HIR current:

- uses symbols and explicit references when nominal resolution can determine them;
- represents scopes and owners;
- represents local bindings;
- retains public anchors where appropriate;
- can record nominal relationships `Owns`, `Specializes` and `RefersTo`;
- preserves provenance enough for diagnostics and navigation.

It does not belong to the Nominal HIR set:

- effective types;
- effective domains;
- inferred cardinalities;
- complex conversions;
- effects or read/write sets;
- post-typing semantic dependencies;
- evidence of termination.

The current contract for this boundary is [[notes/decisions/ADR-097-hir-nominal-vigente-and-ir-semantico-diferido|D-097]], which amends and clarifies [[notes/decisions/ADR-051-graph-future-semantics-and-reconstructable-information|D-051]] and [[notes/decisions/ADR-093-ast-superficial-hir-nominal-and-fase-semantica-posterior|D-093]].

## Later semantic representation

Classification and elaboration will need a representation suitable for execution, analysis and materialisation. For now, it exists only as an architectural necessity and set of requirements, not as a current regulatory framework.

When designing, a decision must be made, taking into account the typefaces and elaboration already developed:

- which nodes and relationships it requires;
- what information should be stored and what can be reconstructed;
- how it preserves provenance;
- what searchable projections it offers;
- whether serialisation is required and, if so, its versioning.

There is currently no `schemaVersion` contract for that representation, nor a normative ASDL for subsequent semantic processing that consumers must perform.

## Searchable graphs

The Nominal HIR now makes it possible to reconstruct a nominal graph for navigation, ownership, specialisation and references. Richer semantic graphs may be projected from the later representation once typing and elaboration provide sufficient information.

Any derived graph is used for:

- impact before making a change;
- anchor navigation;
- direct and transitive dependencies within the available information;
- detection of cycles when defined by the relevant phase;
- identification of readers and writers once these have been produced;
- explanation of a resolution.

It must not become a second source of truth. If there is a discrepancy with the normative representation of the phase that gave rise to it, it is discarded and reconstructed.

## Causal runtime

The runtime requires at least:

- state store with snapshots;
- pure expression evaluator;
- effect applicator and normaliser;
- trigger engine;
- wave planner;
- conflict and cycle detector;
- transaction with confirmation or rollback;
- causal explanation registry;
- deterministic seed manager.

The runtime must consume a representation produced after resolution, typing and elaboration. It must not rely on parser-specific behaviour or use the Nominal HIR as a substitute for semantic information that it deliberately does not contain. The specific form of that representation remains deferred by D-097.

## Semantic operator

The natural language processing layer should not edit text arbitrarily. It should produce a structured plan:

```text
intent
→ classification
→ target anchors
→ preconditions
→ semantic operations
→ expected impact
→ derived text patch
```

Minimal operations:

- `CREATE anchor`
- `UPDATE anchor`
- `RETIRE anchor`
- `MOVE anchor` or explicit migration

`READ` is a query operation and does not produce a commit by itself. This separation between queries and versionable changes is determined by [[notes/decisions/ADR-012-validation-and-atomic-versioning-of-semantic-changes|D-012]], developed by [[notes/decisions/ADR-053-semantic-operator-and-authoring-flow|D-053]] and implemented by [[governance/COMMITS-POLICY|the commits policy]].

## Materialisers

Each materialiser receives a validated representation sufficient for its task, together with technical configuration. A consumer requiring types, effects or advanced semantics cannot obtain them by inventing them from the Nominal HIR.

It can produce:

- TypeScript code.
- API contracts.
- Fixtures and tests.
- Documentation.
- Adapters for a motor.

It cannot:

- infer rules from a new domain;
- convert `failed` to `false`;
- collapse participants and `given`;
- change atomicity, causal ordering or identity.

## Early interfaces

A first executable could be a CLI with commands equivalent to:

```text
mud check
mud format
mud graph
mud explain <anchor>
mud run <action> --state <file>
mud impact <operation-plan>
```

Conversational integration and the plugin should be developed once these operations have stable contracts. This ensures that AI uses verifiable capabilities rather than containing special-case semantics.

The current policy for operator classification, permitted inferences and atomic flow belongs to [[notes/decisions/ADR-053-semantic-operator-and-authoring-flow|D-053]].

## Runtime-state persistence

The specification rules out persistence of MUD semantics, but a materialisation will need to save states. A distinction must be made between:

- The `.mud` model, which states what the world may be.
- A runtime-state instance.
- The technology used to keep that instance running.

Declarative tests written in MUD conform to the language as defined by D-055 and should not be confused with tests generated by a materialiser. The technical format of additional snapshots or fixtures may be defined within tooling without imposing a database on the language.

