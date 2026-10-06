# System architecture

MUD is an executable declarative language. `.mud` explicitly defines its domain model and foreign-code boundaries; generated artefacts preserve those contracts. Reproduction includes declared foreign sources, dependency versions and adapter contracts. The reference compiler and runtime are written in Rust and initially generate Rust code. The formal language remains independent of that implementation choice.

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
                   Rust, docs, tests
```

The current regulatory chain runs through the Surface AST and Nominal HIR. Typing and elaboration are later architectural phases; no regulatory framework yet defines the semantic representation they will produce.

## Source and derivatives

Source semantics:

- `.mud` files, including explicit foreign-code boundaries.
- Declared foreign sources, library versions and adapter contracts required by those boundaries.

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

The current contract for this boundary is [[notes/decisions/ADR-097-current-nominal-hir-and-deferred-semantic-ir|D-097]], which amends and clarifies [[notes/decisions/ADR-051-graph-future-semantics-and-reconstructable-information|D-051]] and [[notes/decisions/ADR-093-surface-ast-nominal-hir-and-later-semantic-phase|D-093]].

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
- tentative journal with private sequential deltas, semantic consolidation and per-wave patches/snapshots;
- atomic confirmation of the complete resolution or discard;
- causal explanation registry;
- deterministic seed manager.

The runtime must consume a representation produced after resolution, typing and elaboration. It must not rely on parser-specific behaviour or use the Nominal HIR as a substitute for semantic information that it deliberately does not contain. The specific form of that representation remains deferred by D-097.

### Tentative journal

[[notes/decisions/ADR-110-tentative-wave-journal-and-atomic-confirmation|D-110]] adopts a tentative journal for the reference runtime. A `then` reads its own private sequential delta; concurrent siblings retain the common prior projection. Semantic consolidation creates tentative wave patches and coherent snapshots for the next wave. Recording a patch does not apply it to confirmed world storage.

Each invocation evaluates after once its owned causal work stabilises, before its caller resumes. Nested completion retains tentative work; only successful outer completion permits one atomic confirmation. Non-success scopes discard their attempted contributions and delivery under explicit reply-capture and block-recovery rules. For example, concurrent `+= 3` and `+= 4` from `10` consolidate to `17`; Git is an analogy for isolated change records, not the conflict algorithm.

`imagine` shares the semantic engine but always discards its speculative journal. It returns ActionReply unchanged (Success, Refusal or Errors), with no consumption of confirmed queues, random state or resolution identities. Tentative message occurrences can cause later waves; they reach the host only after a real commit. Diagnostic traces may be retained separately from confirmed logs. Foreign calls must respect the same boundary; patches cannot undo arbitrary native I/O.

Physical journal layout, persistence and compression remain implementation choices. Q-002 still requires complete operational effect semantics, and Q-035 retains admissibility costs, memoisation and resource diagnostics. No semantic IR format is prescribed.

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

- Rust code as the initial backend.
- C or TypeScript code as possible alternative backends, without near-term commitment.
- API contracts.
- Fixtures and tests.
- Documentation.
- Adapters for a motor.

It cannot:

- infer rules from a new domain;
- convert an Error or Refusal into an untyped false;
- collapse participants and `given`;
- change atomicity, causal ordering or identity.

## Hosting and language adapters

The production API remains operation-centred: `look` observes a coherent view, `action` requests a causal transaction and `message` delivers confirmed occurrences. MUD may be embedded in another language or coordinate foreign components itself. Rust, Python and C# are the initial planned adapters, respectively supporting the reference backend, Python libraries and the .NET/Unity ecosystem. Adapters preserve type conversions, capabilities, read dependencies, transaction isolation and error contracts. The Rust backend does not translate Python or C# source into Rust; the corresponding language environment executes those fragments.

`from Language` delegates native statements to a language-specific parser and bridges `mud name [: Type] <- nativeExpression` back to immutable MUD values, under [[notes/decisions/ADR-109-foreign-language-blocks-and-value-exports|D-109]]. MUD handles the language label and export name/type; native tooling handles statements and export RHSs. Editors use virtual documents, wrappers and source maps so native semantic colouring, completion and diagnostics refer to original source. Csharp may use Roslyn; Unity/AOT requires build-time native compilation rather than assuming runtime compilation.

Adapter wrappers retain MUD visibility, type, collection and capability contracts, track reads and route authorised writes into tentative deltas. Foreign errors must participate in MUD failure handling. Pure owners require explicit pure contracts; irreversible I/O needs deferred confirmed host delivery or a transactional adapter. Native representations require semantic equivalence, and exports cannot leak opaque objects or hidden mutable aliases. Exact hosting/effect contracts remain [[notes/questions/Q-069-foreign-adapter-contract-and-hosting|Q-069]], with conversions, lifetime and errors in [[notes/questions/Q-070-foreign-value-conversion-lifetime-and-errors|Q-070]].

Dependencies and adapter versions must be reproducible. A C-compatible ABI may support host integration without implying that MUD generates C source. The exact adapter protocol remains a separate design obligation.

## Considered interactive environment

An interactive environment similar in purpose to GHCi is a desirable expansion under [[notes/decisions/ADR-108-considered-interactive-model-environment|D-108]]. It would load models and let users interrogate them and evaluate expressions or operations under their ordinary contracts. Entering an expression or operation requests its evaluation or execution; there is no separate `:run` command. Command syntax, loading, sessions and persistence remain undesigned. This expansion is distinct from the illustrative CLI below and carries no initial delivery commitment.

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

