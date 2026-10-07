---
title: MUD formal specification
aliases:
  - MUD specification index
  - MUD 1.0
tags:
  - mud/specification
  - mud/moc
status: in-preparation
normative: true
questions:
  - Q-009
  - Q-059
  - Q-069
  - Q-070
  - Q-071
  - Q-072
  - Q-073
  - Q-074
decisions:
  - D-013
  - D-107
  - D-108
  - D-109
  - D-120
  - D-121
  - D-140
  - D-139
  - D-138
  - D-137
  - D-134
  - D-135
  - D-136
  - D-133
  - D-132
  - D-131
  - D-112
  - D-113
  - D-114
  - D-115
  - D-116
  - D-118
  - D-119
  - D-122
  - D-123
  - D-124
---

# MUD formal specification

## Document status

- Overall status: **in preparation**
- Initial target version: **MUD 1.0**
- Current authority: chapters with `status: current` and their linked current decisions. A file with `normative: true` belongs to the normative surface, but its `status` determines whether the complete chapter has consolidated authority. Non-current chapters may incorporate rules backed by current decisions, but do not replace them or close open questions. Git history retains withdrawn provenance but has no subsidiary authority.
- Scope: the complete MUD language, its execution semantics and conformance criteria.

This directory contains the normative MUD specification. Its objective is that two independent implementations can:

1. Recognise the same programmes.
2. Resolve the same names and anchors.
3. Assign the same types.
4. Reject the same programmes statically.
5. Produce the same observable semantic transitions.
6. Classify Success, Refusal and nonempty Errors in ActionReply in the same way.
7. Agree on admissibility and reachability analyses when they are decidable for the programme.

The specification presupposes no compiler architecture, implementation language, database, graphics engine or framework.

Drafting conventions: [[00-editorial-conventions]].

## Normative character

Surface and publication status are distinct axes. `normative: true` indicates that the file is intended to contain conformance rules; it does not by itself amount to approval. The `skeleton → draft → proposed → in-review → current` cycle determines the chapter's authority as a unit.

- **Current chapter**: its normative text is consolidated authority.
- **Non-current chapter**: it may transcribe or explain contracts already fixed by current decisions and coherent mechanical artefacts, but the complete chapter remains in preparation and cannot introduce new authority above those sources.
- **Informative content**: explains a rule without extending it.
- **Open question**: has no definitive semantics until the decision process closes it or explicitly excludes it from the applicable profile.

Contradiction between a non-current chapter and a current decision is a documentary defect, not a new semantic choice. Contradiction between normative prose and a normative mechanical artefact is likewise a defect and must be corrected in accordance with MUD-EDIT-001.

The words are used with these meanings:

- **must**: conformance requirement.
- **must not**: conformance prohibition.
- **may**: permitted behaviour.
- **should**: non-normative recommendation.

An implementation must not silently choose behaviour for a question marked open and continue to claim conformance for that feature.

## Specification architecture

The specification is organised into five parts and 53 numbered chapters, with a separate planned standard-library contract volume. The separation is conceptual: chapters depend on definitions elsewhere, and all normative surfaces must agree.

```text
Part I    Foundations and notation
Part II   Language constructs and static contracts
Part III  Dynamic semantics
Part IV   Advanced semantic analyses
Part V    Conformance and normative appendices
```

The compiler, conversational plugin, Git and materialisers have their own specifications. They rely on the language but do not define its meaning.

Planned chapters and library documents gain no developed authority merely by appearing in this plan. Current rules remain governed by their developed surfaces and linked current decisions until publication under the document lifecycle. Cross-cutting responsibilities are allocated as follows.

| Cross-cutting scope | Read with | Responsibility |
| --- | --- | --- |
| [[#20. Blocks and error recovery]] | 11, 21, 28–33 | Shared block outcomes, protection and recovery; category-specific expression/effect evaluation stays in its chapter. |
| [[#27. Foreign interoperability]] | 08–11, 15, 26–34 | `from` boundaries, conversions, adapter guarantees and native hosting contracts. |
| [[#06. World descriptors and dependencies]] | 05, 10, 26 | World/distribution configuration and resolution, distinct from local part access and name imports. |
| [[#37. Textual patches and reproduction]] | 28–34, 36, 52 | Readable incorporated changes, validated reproduction and patch compatibility. |
| [[#Standard-library contracts]] | Relevant type, effect, interoperability and dependency chapters | Included-base and extension API contracts, distinct from their implementations. |

---

# Part I — Foundations and notation

## 01. Scope, conformance and versions

Chapter: [[01-scope-and-conformance]].

Defines:

- Purpose of the specification.
- What it means to implement MUD.
- Conformance profiles.
- Extensions and experimental features.
- Compatibility between versions.
- Authority of examples, notes and appendices.
- Normative treatment of open questions.

## 02. Terminology

Chapter: [[02-terminology]].

Normative glossary of:

- MUD world/programme, part, source file, descriptor, distribution and path.
- Declaration, symbol, name and anchor.
- `thing`, identity and value.
- Field, relation and collection.
- Exact dictionary, functional dictionary, association, branch, selector and fallback.
- Participant, role, binding and `given`.
- Queryable, reactive and `always` rule.
- Action declaration, invocation identity, causal owner, request, root, wave and resolution.
- Test, assertion and diagnostic.
- State, snapshot, effect, conflict, reality level, alternative branch and relative confirmation.
- Domain, constraint, condition and invariant.
- ActionReply, Success, Refusal, Error occurrence, Errors and block error channel.
- Textual patch, reproduction and host-only Ticket confirmation, with pending interfaces explicitly delimited.

## 03. Mathematical notation and metalanguage

Chapter: [[03-notation]].

Defines the shared metalanguage: symbols and logic, sets and collection shapes, functions and relations, graphs, judgments, operational notation, EBNF and ASDL-MUD. Mathematical notation is distinct from MUD source and does not prescribe implementation layout. Each semantic chapter defines the objects and judgments it uses; the notation alone does not define an execution protocol.

## 04. Mathematical foundations of the MUD world

Chapter: [[04-mathematical-model]].

Defines canonical programme identities, specialisation, values, activation and materialisation generations, owned storage and effective projection. It distinguishes confirmed from tentative state and records the established lifecycle, checkpoint, recovery and initial-world invariants. It remains a foundation for the operational formalisation, including instruction-local lifecycle no-ops and reactive binding observation episodes.

---

# Part II — Language constructs and static contracts

## 05. Source text and physical structure

Chapter: [[05-source-text]].

Defines:

- Encoding.
- `.mud` source files and minimal `mud.part` manifests.
- World/part/file boundaries, direct non-transitive `uses` and initial `part only` placement.
- Derivation of MUD paths from routes.
- Multiple declarations per file.
- Semantic independence from file ordering.
- Line terminators.

The world descriptor is planned as `mud.world.toml`; its schema and external distribution resolution are not part of the current source grammar. [[#06. World descriptors and dependencies]] owns that scope, pending Q-071 and coordinated with adapter configuration in Q-069.

## 06. World descriptors and dependencies

Planned file: `06-world-and-dependencies.md`

Planned scope:

- `mud.world.toml` discovery, descriptor schema and validation under Q-071.
- Included library base and installable official extensions; distribution identity, sources, versions, locking and namespace collisions.
- Distribution-to-part mapping under direct `uses`, file privacy and contract-type closure; `using` imports names rather than installing dependencies.
- Adapter declarations, label lookup, dependency-local environments and delegated native manifests coordinated with Q-069.
- Configuration boundaries for runtime and recording once the causal, patch and host-observation contracts support them.

Required tables, defaults, schema-version notation, build settings, adapter aliases, quick fixes and runtime/recording options remain unselected. Descriptor examples are design material, not an accepted manifest schema.

## 07. Lexical structure

Chapter: [[07-lexicon]].

Defines:

- Character categories.
- Identifiers and case sensitivity.
- Reserved words.
- Numeric, monetary and percentage literals.
- Ordinary and multiline `Text` templates, ordinary interpolations, escapes and typed `~anchor` access.
- `#`, `#...#` and `###...###` comments.
- Whitespace.
- Tokens, trivia, spans and lexical errors.
- Complete stream and significant view, including contextual generic-header and native-region token boundaries.

The normative lexical grammar lives in `grammar/mud-lexico.ebnf`.

## 08. Concrete grammar

Chapter: [[08-concrete-grammar]].

Defines the complete syntax of:

- `using` declaration header, placed before any top-level declaration.
- Declarations.
- Types.
- Fields.
- Participants.
- `given` values.
- Expressions.
- Effects.
- Blocks.
- Calls.
- Canonical definitions of `thing` and rules, part-unified `start with` and activation through `create Name`.
- Isolated tests with local `start with`, `then`, `after` and `otherwise`.
- Error-only otherwise handlers on expression, value and effect blocks, with joint on bindings and then/raise branches.
- Numeric formats within `Text` interpolations.
- Quantifiers and iterations.

Foreign `from Language` bodies delegate native parsing and preserve `mud name [: Type] <- nativeExpression` bridges, with braces determined by instruction count. All existing block capabilities remain in force; pure preambles and value/effect statement slots admit compatible foreign blocks.

The complete concrete grammar lives in `grammar/mud.ebnf`. Parsing produces a lossless CST; this chapter explains ambiguities, precedence, contextual validation and the boundary with desugaring, but does not repeat the entire EBNF.

## 09. Surface abstract syntax

Chapter: [[09-abstract-syntax]].

Defines the semantically relevant forms after the CST and contextual syntactic validation:

- `MudFile` and `MudProject` roots.
- AST of declarations, types, domains, expressions and effects.
- Normalisation of cardinalities, intervals, blocks and contextual literals.
- Structural distinction among the three rule classes.
- Surface `ActionDecl` with `PublicAction` or `Subaction` class; candidate calls are resolved later without introducing an elementary/compound classification.
- Dedicated TestDecl and assertions with protected expression blocks.
- Dedicated nodes for `look`, `message` and public properties.
- Foreign regions, source origins and immutable exports, with distinct ordered expression/test and shared behaviour preambles.
- Recursive positional binding patterns, explicit discards and stored annotation type holes with preserved source spans.
- Provenance through `SourceOrigin`.
- Ambiguities retained until resolution.

Mechanical and transformation artefacts: `syntax/`.

## 10. Paths, `using`, names and anchors

Chapter: [[10-names-and-anchors]].

Defines:

- Scopes.
- Local and qualified resolution.
- Exact and recursive `using` declarations.
- Mandatory placement of all `using` declarations in the file header.
- Ambiguity and candidate-local static selection of homonymous imported callables by supplied `for` participants and written `given` arguments, without expected-result tie-breaking or changes to anchors and lookup priorities.
- Foreign exports as ordinary local symbols and native captures as source-mapped nominal references; adapter labels/private native locals receive no MUD declaration identity.
- One ordinary LocalSymbol per named pattern leaf; discards and type holes introduce no symbol or anchor.
- Formation and uniqueness of public anchors; functional-dictionary branches use local keys and receive no public anchor.
- Categories `thing::*`, `alias::*`, `family::*`, `magnitude::*`, `unit::*`, `rule::*`, `action::*`, `look::*`, `message::*`, `test::*` and `type::*`.
- Identity under file moves.
- Path and anchor migration.

Juicio principal:

$$
\Gamma \vdash n \rightsquigarrow a
$$

## 11. Type system

Chapter: [[11-type-system]].

Defines:

- Built-in, nominal, structural, collection, dictionary, interval, magnitude and union types.
- `Any`, first-class descriptors, callable types and types obtained statically through `~type`.
- Static generic parameters/applications, nominal bounds, conservative inferred variance and proven finite application closure.
- Subtyping, compatibility, narrowing, exact normalized structural type equality, ordering, conversions and unambiguous inference.
- Whole and partial stored type holes requiring a unique compile-time solution, and exact positional pattern typing.
- Typing of anonymous `look` results and `message` payloads, including the join of dynamic calls.
- Interaction between a callable descriptor's static type and the nominal identity needed to bind its signature.

Callable contracts use contravariant read-only inputs, covariant outputs and invariant read/write places. Named invocation requires an unequivocal static signature, with no runtime scan. Produced look/sublook types are static and nominal per declaration and exact generic arguments; message/submessage types are static per declaration; anonymous literal types are structural. Multiple incomparable common result minima retain the original union. Things and aliases share contract-visible specialization across authorized parts.

Juicio principal:

$$
\Gamma;\Sigma \vdash e : \tau
$$

## 12. `Thing`, specialisation and identity

Planned file: `12-things.md`

Planned scope:

- Identity, activity, destruction of a materialisation's own load, rematerialisation from the canonical definition and independent state of concrete and abstract `thing`s.
- Single and multiple specialisation, including applied generic abstract ancestors, inheritable schema, defaults and initialisers; concrete things are not generic.
- Integration of `Thing` as the built-in root and of nominal identity/equality rules.
- Part-level boundary of `thing`s: visible identity/type versus ordinary state projected through public operations and inter-part specialisation limits.
- `thing` metadata and reflection without confusing them with state fields.

## 13. Nominal aliases and structural values

Planned file: `13-aliases.md`

Planned scope:

- Nominal and structural representation aliases, generic applications, contextual construction and nominal casting; exact structural type equality remains distinct from nominal value equality.
- Single and multiple nominal specialisation, inheritance of representation or members, provenance-based deduplication and conflicts between independent members.
- Inherited defaults, immutable values, equality, ordering and enumerability where applicable.
- Reconstruction of immutable aliases through write-back from assignable paths, without introducing mutability into their values.
- Boundary between structural compatibility and explicit acquisition of nominality.
- Contract-visible alias specialization across parts under uses authorization and inherited substitutability.

## 14. Closed value families

Planned file: `14-closed-families.md`

Planned scope:

- Declaration, generic applications, members, nominality, ordering and enumeration of `family`; applied members retain source anchors and exact applied types.
- Uniform schema for associated data, defaults and per-member calculations.
- Equality, ordering, reflection and absence of runtime lifecycle for its values.

## 15. Fields, mutability and capabilities

Chapter: [[15-fields-and-mutability]].

Defines:

- Stored and calculated fields, defaults, initialisers and derived views.
- External mutability, inner `[mut]` capability and its composition without implicit deep mutability.
- Participant capability and write accessibility.
- Postfix metadata as information separate from ordinary state and read-only during execution.

## 16. Cardinalities and collections

Planned file: `16-collections.md`

Planned scope:

- Cardinalities, `empty`, multiplicity, uniqueness and ordering.
- Membership, collection algebra, indexing, selection and `take`.
- Inference and preservation of cardinality, domain, ordering and capabilities.
- Snapshots and observable semantics of collection iteration.

## 17. Dictionaries

Planned file: `17-dictionaries.md`

Planned scope:

- Exact and functional dictionaries, their types, cardinalities and queries.
- Associations, keys, iteration, ordering and algebraic operations.
- Indexing within assignable paths, partial write-back on associated values and treatment of missing keys without confusing partial update with complete insertion.
- Branch-selection modes, fallback, dependencies, recursion and termination of functional dictionaries.

## 18. Domains and intervals

Planned file: `18-domains-and-intervals.md`

Planned scope:

- Declared and calculated domains, membership, normalisation, finiteness and enumerability.
- Acyclic computed-domain evaluation dependencies, distinct from stored-value reads, recursive constructor enumeration and periodic point-domain normalisation.
- Linear, discontinuous, cyclic and magnitude-dependent intervals.
- Explicit materialisation of enumerable domains through `all D` when an operation must produce a collection.
- Difference between consuming a domain, materialising its enumeration and producing a filtered collection, without implicit conversion of the latter to `Domain`.

## 19. Magnitudes, units and points

Planned file: `19-magnitudes.md`

Planned scope:

- Base, derived and point magnitudes, their representations and domains.
- Units, prefixes, equivalences, normalisation and dimensional arithmetic.
- Coordinates, cycles, presentation, formats and component extraction.
- Temporal magnitudes and calendar/localisation constructs that ultimately belong to the MUD 1.0 profile.

## 20. Blocks and error recovery

Planned file: `20-blocks-and-recovery.md`

Planned scope:

- Common outcomes of expression, value and effect blocks; an empty Error occurrence channel permits the normal result, while a nonempty channel is distinct from an ordinary Error or ActionReply value.
- Protected scopes, rollback before recovery, propagation and observation boundaries.
- Error-only `otherwise`, joint element-wise `on` bindings, optional filters and exclusive `then`/`raise` branches; occurrence identity and unhandled errors.
- Refusal versus computing failure, wrapping through finite causes, and block-category-specific fallback/result obligations.
- Interfaces with chapter 11's reply/error types, chapters 21/28's evaluation and chapters 29–33's completion; unresolved test observation belongs to Q-059.

## 21. Expressions

Chapter: [[21-expressions]].

Defines:

- Literals, operators, calls, access, comparison, conversion and contextual construction.
- Resolution and elaboration of receivers, arguments and callable values.
- `old`, `imagine`, `eventually`, selection, `take` and `all D` materialisation in expression contexts.
- Purity, narrowing, expected-type propagation and evaluation failures.
- Local declarations, ordered/shared preambles and positional binding patterns; stored annotation holes use the static inference contract in chapter 11.

[[#20. Blocks and error recovery]] owns the common block/error protocol; this chapter supplies expression-specific admission, normal results and evaluation obligations.

## 22. Quantifiers, aggregations and iteration

Planned file: `22-quantifiers-and-iteration.md`

Planned scope:

- Quantifiers and aggregators over finite enumerable sources.
- `for each`, iteration bindings, ordering, filters, steps and membership snapshots.
- Direct consumption of finite domains when no collection is produced and termination requirements for every traversal.

## 23. Boolean rules

Planned file: `23-boolean-rules.md`

Planned scope:

- Pure signatures with explicitly named `for` participants and read-only `given` values.
- Binding of receivers and arguments, domains, defaults and capabilities admitted by a pure query.
- Boolean evaluation, dependencies, memoisation and treatment of non-effective declarations.
- Integration with callable values of Boolean-rule type.

## 24. Reactive rules

Planned file: `24-reactive-rules.md`

Planned scope:

- Set-valued `on` bindings, including finite enumerable related sources and nominal refinements.
- `when`, `changes` and `old` triggers, `if` guards, reactive memory and `then` consequences.
- Appearance, disappearance and temporal identity of bindings.
- Use of a triggered reactive rule as a causal source for other triggers.

## 25. `always` rules

Planned file: `25-always-rules.md`

Planned scope:

- `on` bindings, pure condition, checkpoints and diagnostics.
- Dependencies, suspension and the effect of a violation on resolution.
- Use of `always` evaluation as a causal trigger source, separately from whether its condition is true or false.

## 26. Public boundary: `action`, `look` and `message`

Planned file: `26-public-boundary.md`

Planned scope:

- Contracts visible between parts and to the host for `action`, `look` and `message`; `test` crosses parts only in a test context.
- Normal/sub operation availability across authorised parts, host entry capability and the whole-file `part only` boundary.
- Part-level authorisation through `uses`, transitive closure of the types needed to understand a contract and safe cross-part reflection without silent filtering.
- Host API centred on the identity of public operations, not on a participant chosen as owner.
- Generic callable signatures and static receiver/written-given selection, with no expected-result tie-break.
- `for`/`given` signatures, external capability of `action` versus `subaction`, callable values and binding at the invocation point.
- `look` as a pure query with a coherent caller view and one value of its static produced result type.
- Message/submessage causal occurrences with frozen birth-view payloads; shared normal messages publish host-only provisional Ticket handles after validated wave consolidation, with Waiting/Kept/Dropped scope-aware lifetime. Generalised observation objects and exterior execution results remain to be specified.
- Separation of bindings and payload, multiplicity and delivery ordering, and rollback of external outputs.

Canonical participant descriptors and frozen historical payloads survive later inactivity; host looks read confirmed state and tickets report eventual commitment or rollback.

Generalised host observation objects and exterior execution-result contracts remain Q-074. Native adapter boundaries are coordinated with [[#27. Foreign interoperability]], rather than inferred from a public operation's signature alone.

## 27. Foreign interoperability

Planned file: `27-foreign-interoperability.md`

Planned scope:

- Embedding Mud through `look`/`action`/`message` and coordinating native fragments through `from`, under the same language contracts.
- Native parsing and immutable value exports, captures, source maps and semantic tooling boundaries.
- Conversion, wrappers, nominal identity, domains, collection shapes, capabilities and read/dependency reporting.
- Checked/trusted purity, declared effects, private work, Error translation and exterior intentions relative to stable-root confirmation.
- Adapter configuration and hosting/ABI negotiation under Q-069; conversion, borrowing, retained-reference and lifetime protocols under Q-070.
- Transactional adapter guarantees and exterior execution results coordinated with Q-072/Q-074; no implicit reversibility or asynchronous source syntax.

Rust, Python and Csharp are the initial planned adapters. SQL is a persistence-adapter candidate; no dialect, connection protocol, adapter alias scheme or implementation order is selected here.

---

# Part III — Dynamic semantics

## 28. Effects

Chapter: [[28-effects]]. Status: proposed.

Defines private effect/statement judgments, semantic destinations and branch normalisation, staged numeric composition, collection/dictionary/lifecycle operations, finite traversal and call/native interfaces, recovery and the root/wave batch boundary. [[effects/README]] supplies Surface AST coverage, declarative traces and bounded executable witnesses. The chapter does not claim a complete scheduler or native ABI.

Scope:

- Assignments, updates, collection operations and `create`/`destroy`; field declarations come exclusively from the canonical static schema, including specialisation.
- Effectful calls and traversals within a unified `then`.
- Reads, writes, deltas, conflicts and effect composition.
- Elaboration of reconstructible assignable paths and propagation of write-back through immutable values to their root storage.
- Interaction between direct effects and internal calls sharing one causal resolution.

[[#20. Blocks and error recovery]] owns the common protected-block protocol; this chapter supplies effect sequencing, rollback/recovery integration and batch-specific obligations.

## 29. State and expression evaluation

Planned file: `29-evaluation.md`

Planned scope:

- Environments, stable/provisional read views, store and deterministic expression evaluation.
- Reality levels as relative confirmation frontiers and isolated alternative branches.
- Abstract evaluation configurations and transitions, with observation views and pending native work coordinated by Q-072 and Q-069/Q-070.
- Evaluation of calculated fields, partial queries, expected types and failures.
- Coherent views inherited by `look`, including the private delta visible at the call site.
- Evaluation of callables and effective binding once their signature is resolved.

## 30. Action requests and results

Planned file: `30-action-requests.md`

Planned scope:

- External request, binding and initial validation of a root `action`.
- Sole action/subaction result ActionReply = Success | Refusal | Errors, with no additional domain result; patch-access interface pending, mandatory origins and final-condition BoolCheck traces.
- Relationship among signature validation, guards, stabilisation, final constraints and external publication.
- Explicit reply capture versus bare effect-call propagation, distinct from a block's error channel; test observation/aggregation remains Q-059.

## 31. Root semantics

Planned file: `31-root.md`

Planned scope:

- Root causal resolution, private deltas and textual sequencing within each `then`.
- Automatic relative incorporation of nested invocation contributions without independent stable-root transactions.
- Consolidation, normalisation and conflicts among concurrent contributions.
- State observed by each phase of a resolution, with consolidated tentative projections kept separate from confirmed storage.

## 32. Wave-based causal semantics

Planned file: `32-waves.md`

Planned scope:

- Snapshots, active bindings, triggers and progression between waves.
- Causal matches with witnesses, multiplicity and conjunction/disjunction composition.
- `message` occurrences and rule firings as consequences available to later waves.
- Effect combination, causal work registration/discovery, readiness and stabilisation; invocation ownership distinct from shared physical waves.
- Distinction between causal ordering and any reproducible technical ordering within a wave.
- Causal attribution, discovery barriers, readiness and completion pseudocode with reviewed traces; the complete algorithm remains Q-072.

## 33. Constraints, `after` and `old`

Planned file: `33-final-constraints.md`

Planned scope:

- Checks of domains, cardinalities, `always` rules and other invariants over tentative states.
- Invocation-owned causal completion and after before returning, without rechecking completed children.
- Contextual semantics of `old`, including the difference between actions, tests and reactive rules.
- Relative inner confirmation and automatic incorporation; one atomic stable-root confirmation after owned completion, root/wave checkpoints and after; containing-level and protected-scope rollback.

## 34. Conflicts, cycles and stabilisation

Planned file: `34-conflicts-and-stabilisation.md`

Planned scope:

- Compatibility and conflict of effects, activations and other concurrent consequences.
- Executable cycles, oscillations and detection of non-stabilisation.
- Purely causal message/firing cycles that may keep consequences pending even without state change.
- Semantic stabilisation condition and separation from technical implementation limits.

## 35. Runtime creation, destruction and identity

Planned file: `35-runtime-lifecycle.md`

Planned scope:

- Activity, materialisation, destruction of a materialisation's own load and rematerialisation from the canonical definition.
- Part `start with` contributions, joint materialisation and first-activation initialisation.
- Latent storage of suspended foreign state, effective projection, dependency suspension and restoration.
- Appearance and disappearance of activity-dependent bindings.

## 36. Randomness

Planned file: `36-randomness.md`

Planned scope:

- Random values and points, seeds, sub-seeds and reproducibility.
- Snapshot caches, randomness in expressions/effects and its relationship to rollback.
- Conditions under which an apparently random operation simplifies to a deterministic choice.

## 37. Textual patches and reproduction

Planned file: `37-patches-and-reproduction.md`

Planned scope:

- Readable serialisable records of successfully incorporated changes, with automatic relative incorporation and no duplicate application caused by observation.
- Semantic contents, originating identities, dependencies/preconditions, generations, joint contributions and destination compatibility.
- ActionReply/Success access, textual grammar, format compatibility and round-trip cases under Q-073; no source Patch type, Success component or mandatory disk file is assumed.
- Validated transition reconstruction versus programme re-execution, including exterior inputs, randomness, failed attempts and irreversible-operation limits.
- Provisional host observations and prepared exterior intentions coordinated with Q-074; ticket confirmation is distinct from successful exterior execution.

Derive the patch contract from the completed causal algorithm in Q-072. Physical journals and the later semantic representation do not determine its schema. Recording defaults and retention remain pending.

---

# Part IV — Advanced semantic analyses

## 38. Semantic graph

Planned file: `38-semantic-graph.md`

Planned scope:

- Semantic relations after nominal resolution that depend on types, domains, effects or elaboration.
- Reads, writes, dependencies, binding patterns and stochastic dependencies.
- Reconstruction criteria from the programme and relation to the Nominal HIR, without turning the latter into a prematurely semantic graph.

## 39. Speculative query `imagine`

Planned file: `39-imagine.md`

Planned scope:

- Construction and unconditional disposal of an isolated alternative reality branch, distinct from a nested invocation's confirmation level.
- ActionReply results, isolation and unconditional discard, without implicit Bool conversion.
- Relative Success inside the branch, without incorporation into the stable root or speculative host publication.
- Acyclicity/admissibility conditions and reproducibility of randomness.

## 40. Reachability `eventually`

Planned file: `40-eventually.md`

Planned scope:

- Explored transition system, target state and permitted action sequences.
- Randomness semantics and state equivalence/canonicalisation criteria.
- Search strategies only insofar as they form part of normative meaning.

## 41. Finiteness, enumerability and relevant state

Planned file: `41-finiteness-and-enumerability.md`

Planned scope:

- Finiteness and canonical enumeration of domains and sources.
- Finite-world profiles, relevant state and state canonicalisation.
- Sufficient conditions for exhaustive analysis and constructs requiring enumerability.

## 42. Termination and decidability

Planned file: `42-termination.md`

Planned scope:

- Termination of iterations, resolutions and recursive components.
- Conservative analyses and the boundary between static rejection, runtime failure and undecidability.
- Decidable or semi-decidable properties of advanced constructs.

## 43. Metatheoretic properties

Planned file: `43-properties.md`

Planned scope:

- Hypotheses and proofs about resolution, types, progress, determinism, reproducibility and atomicity.
- Independence from orderings without semantic meaning and correctness of speculative analyses.
- Counterexamples and explicit limits where a property is not valid for all MUD.

---

# Part V — Conformance and appendices

## 44. Diagnostics

Planned file: `44-diagnostics.md`

Planned scope:

- Categories, codes, locations and related anchors.
- Mandatory diagnostics versus drafting freedom.
- Parser/tooling recovery and the relationship between static and dynamic diagnostics; language-level block recovery belongs to [[#20. Blocks and error recovery]].

## 45. Later semantic representation

Planned file: `45-ir.md`

Planned scope:

- Contract between typing/elaboration phases and later consumers once those phases are sufficiently developed.
- Semantic information that must be preserved or may be reconstructed, provenance and versioning criteria if a serialisable representation is adopted.
- Relationship with Surface AST and Nominal HIR without duplicating or degrading their responsibilities.

No ASDL/JSON schema, concrete node or edge names, schema version or storage-versus-reconstruction policy is currently assumed. These details will be fixed only when typing and elaboration surfaces make them justifiable.

The representation question remains Q-009. A textual patch records incorporated changes under [[#37. Textual patches and reproduction]]; it does not define this compiler representation.

## 46. Implementation conformance

Planned file: `46-conformance.md`

Planned scope:

- Implementation profiles and each one's requirements.
- Determinism, version declaration, optional features and conforming materialisation.
- Relationship between frontend, runtime, analysis and normative tooling conformance.
- Applicable host, adapter, package and library contract obligations, without requiring every implementation to use the reference backend.

## 47. Declarative tests

Planned file: `47-declarative-tests.md`

Planned scope:

- `test` declarations, fresh isolated world, execution and disposal.
- Static transitive closure of reachable tests and union of **their own** `start with` contributions; ordinary part activation is not part of a test's initial world.
- Prior materialisation/stabilisation, `then`, `after`, `old`, diagnostics and executor results.
- Test visibility between parts exclusively in a test context.
- ActionReply observation, assertion/aggregation and protected-scope observation lifetime, pending Q-059.

## 48. Conformance suite

Planned file: `48-conformance-suite.md`

Planned scope:

- Valid and invalid cases, diagnostics and normative regressions.
- Current normative mechanical outputs to compare at each phase.
- Transitions, traces and observable properties needed to contrast implementations.
- Nested relative confirmation, parent rollback, isolated branches, host ticket transitions, adapter failures and patch round-trips under their applicable specified contracts.

The corpus will live in:

```text
conformance/
├── valid/
├── invalid/
├── execution/
├── diagnostics/
└── properties/
```

Declarative tests written by a user are part of MUD, but do not replace this suite: the conformance suite checks complete language implementations.

## 49. Consolidated grammar

Planned file: `49-consolidated-grammar.md`

Normative appendix generated or verified against `grammar/mud.ebnf`.

## 50. Reserved-word catalogue

Planned file: `50-reserved-words.md`

Normative list and classification as reserved or contextual words, derived from the current lexical grammar.

## 51. End-to-end examples

Planned file: `51-end-to-end-examples.md`

Informative examples built only from rules already specified. They introduce no new behaviour.

## 52. Compatibility and migrations

Planned file: `52-compatibility.md`

Planned scope:

- Compatible and incompatible language changes.
- Anchor evolution and programme migration.
- Compatibility of serialised normative artefacts where an applicable serialisation contract exists.
- Separate language, descriptor/distribution, adapter-protocol and patch-format compatibility obligations; their concrete version schemes are specified only by the corresponding contracts.
- Deprecation of syntax and version declarations.

## 53. Normative-rule index

Planned file: `53-normative-index.md`

Generated index of requirements with stable identifiers, for example:

```text
MUD-LEX-001
MUD-SYN-014
MUD-NAME-008
MUD-TYPE-023
MUD-ACTION-011
MUD-WAVE-006
MUD-REACH-004
MUD-TEST-003
```

---

# Standard-library contracts

Planned location: `libraries/`

Plan an included base and installable official extensions. Inventory broad capability contracts and representative Mud uses before detailed implementations, using [[../notes/standard-library-design|the library design catalogue]] as non-normative design material.

For each selected API, specify types/generic parameters, cardinalities, capabilities, purity/read dependencies, effects, errors, determinism and applicable confirmation/reproduction guarantees. Library wrappers reuse the language's collection, numeric, callable and effect contracts. Candidate themes do not become mandatory APIs merely by appearing in the catalogue.

Native implementations and runtime integration follow the completed language/adapter contracts. Asynchronous I/O APIs depend on causal execution and exterior protocols; library wrappers cannot implicitly select scheduling syntax or transaction guarantees.

# Related but separate specifications

Planned tooling documents are separate from the language and library contracts:

```text
tooling/
├── compiler.md
├── cli.md
├── editor-support.md
├── semantic-operator.md
├── git-protocol.md
├── rust-backend.md
├── interactive-environment.md
└── plugin-codex.md
```

This separation prevents an architectural decision from accidentally becoming a MUD rule.

The reference compiler and runtime use Rust and initially generate Rust. C and TypeScript are possible alternative destinations without near-term implementation commitment. Backend architecture does not impose an implementation language on conformance.

An interactive model environment is a considered expansion. Entering an expression or operation requests evaluation/execution; no separate `:run` command is planned. Loading, sessions, persistence and command syntax are not designed here. Compiler, runtime and library implementation follow the complete-formalisation gate.

## Verifiable syntax artefacts

The `syntax/` subdirectory contains the CST contract, Surface ASDL, transformation, production-by-production coverage and editorial validator.

```text
syntax/
├── cst-lossless.md
├── mud-syntax-kinds.yaml
├── mud-surface-ast.asdl
├── cst-to-surface-ast.md
├── syntax-coverage.yaml
├── validate_syntax_model.py
└── cases/
```

## Verifiable static artefacts

The [[types/README|static contract corpus]] maps expression constructors and rule obligations to declarative fragments and finite derivation witnesses. Its validator does not parse or execute MUD programmes.

## Main dependencies

```text
notation
   │
   ├──► mathematical model
   │       │
   │       ├──► types and values
   │       └──► state and effects
   │
lexicon ─► lossless CST ─► Surface AST
                         │
               ┌──────────┴──────────┐
              ▼                     ▼
       static semantics       dynamic semantics
              │                     │
              └──────────┬──────────┘
               ▼
               advanced analyses
                         │
                         ▼
                    conformance
```

## Drafting order

Numerical order is the final reading order, not the strict writing order. Work proceeds in vertical cycles:

1. Define minimal notation.
2. Choose a MUD construct.
3. Formalise its concrete and abstract syntax.
4. Formalise its static rules.
5. Formalise its dynamic behaviour.
6. Write examples and counterexamples.
7. Add conformance tests.
8. Review dependencies and open questions.

## Current drafting priorities

1. Formalise the causal runtime across chapters 29–34: abstract state, reality levels/branches, invocation identities, observation views, causal attribution/discovery, readiness, wave advancement, completion and incorporation/disposal. Close Q-072 through pseudocode and contrasting traces, not diagrams alone. Existing effect algebra and relative-confirmation rules constrain this work; asynchronous source syntax and concurrent exterior roots are not selected implicitly.
2. In parallel, complete independent static construct chapters among 12–26, including things, aliases, families, collections, dictionaries, quantifiers and Boolean rules. Resolve each chapter's actual pending questions before publication. Reactive/always rules and host publication must coordinate their final execution contracts with the causal algorithm.
3. After the causal algorithm, specify textual patches/reproduction under Q-073 and additional host observation/exterior execution contracts under Q-074. Coordinate native hosting, conversion and lifetime work with Q-069/Q-070.
4. Develop world/dependency configuration under Q-071 with the adapter boundary. Its descriptor/distribution work may advance independently where possible; runtime/recording settings wait for the contracts they expose. Inventory library contracts broadly, while asynchronous and effectful APIs wait for their required runtime/exterior guarantees.
5. Complete lifecycle, randomness, advanced analyses, diagnostics, applicable library/adapter contracts and end-to-end conformance evidence. Justify the later semantic representation from developed typing/elaboration under Q-009. Publish chapters through the document lifecycle and finish the complete specification before compiler/runtime/library implementation.

Shared block/recovery formalisation accompanies the affected expression, effect and completion units rather than waiting until diagnostics. Mathematical chapters 03/04 supply common foundations; each operational chapter defines its own state and transitions without duplicating the world model. Examples, mechanical witnesses and iterative dependency reviews accompany every unit.

## “Complete specification” criterion

MUD 1.0 will be formally specified when:

1. No grammar production remains without semantics.
2. Every construct has static rules.
3. Every statically valid programme has defined behaviour or an explicitly defined failure.
4. Every interaction between features is covered or prohibited.
5. All open MUD 1.0 questions are resolved.
6. The grammar, CST/AST coverage, Nominal HIR and every other current normative mechanical representation are automatically verifiable.
7. A representative conformance suite exists.
8. Promised properties are proved or delimited by explicit hypotheses.
9. End-to-end examples do not depend on implicit behaviour.
10. An implementation can objectively declare its degree of conformance.
11. Every world/package, adapter, library and patch feature included in the target profile has an explicit applicable contract and conformance evidence; deferred features and unselected protocols are identified without presenting design examples as accepted schemas.
