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
  - Q-063
  - Q-064
  - Q-065
  - Q-066
  - Q-067
  - Q-068
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
6. Classify `accepted`, `rejected` and `failed` in the same way.
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

The specification is organised into five parts. The separation is conceptual: some chapters depend on earlier definitions, but no part may contradict another.

```text
Part I    Foundations and notation
Part II   Static language
Part III  Dynamic semantics
Part IV   Advanced semantic analyses
Part V    Conformance and normative appendices
```

The compiler, conversational plugin, Git and materialisers have their own specifications. They rely on the language but do not define its meaning.

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

- MUD programme, module, file and path.
- Declaration, symbol, name and anchor.
- `thing`, identity and value.
- Field, relation and collection.
- Exact dictionary, functional dictionary, association, branch, selector and fallback.
- Participant, role, binding and `given`.
- Queryable, reactive and `always` rule.
- Action, request, root, wave and resolution.
- Test, assertion and diagnostic.
- State, snapshot, effect and conflict.
- Domain, constraint, condition and invariant.
- Acceptance, rejection and failure.

## 03. Mathematical notation and metalanguage

Chapter: [[03-notation]].

Fixes the notation used throughout the standard:

- Sets, sequences, multisets and finite maps.
- Relations, partial functions and transitive closures.
- Directed graphs.
- EBNF grammars.
- Typing judgements.
- Inference rules.
- Operational semantics.
- Labelled transition systems.
- Partial orders and fixed points.
- Probability and reproducible seeds.

Juicios previstos:

$$
\Gamma \vdash n \rightsquigarrow a
$$

“In environment $\Gamma$, name $n$ resolves to anchor $a$.”

$$
\Gamma;\Sigma \vdash e : \tau
$$

“In environments $\Gamma$ and $\Sigma$, expression $e$ has type $\tau$.”

$$
\Gamma;\Sigma \vdash e\ \mathsf{reads}\ R
$$

“Expression $e$ may read the set of anchors $R$.”

$$
\langle W, q \rangle \Downarrow \langle W', r, T \rangle
$$

“Request $q$ on world $W$ terminates in world $W'$, with result $r$ and causal trace $T$.”

## 04. Mathematical model of the world

Chapter: [[04-mathematical-model]].

Defines, before discussing syntax:

- Universes of anchors, `thing` and values.
- World state.
- Field and relation store.
- Identity versus structural equality.
- Well-formed states.
- Stable and tentative snapshots.
- Semantically visible observations.

---

# Part II — Static language

## 05. Source text and physical structure

Chapter: [[05-source-text]].

Defines:

- Encoding.
- Archivos `.mud`.
- Derivation of MUD paths from routes.
- Multiple declarations per file.
- Semantic independence from file ordering.
- Line terminators.

## 06. Lexical structure

Chapter: [[06-lexicon]].

Defines:

- Character categories.
- Identifiers and case sensitivity.
- Reserved words.
- Numeric, monetary and percentage literals.
- Ordinary and multiline `Text` templates, ordinary interpolations, escapes and typed `~anchor` access.
- `#`, `#...#` and `###...###` comments.
- Whitespace.
- Tokens, trivia, spans and lexical errors.
- Complete stream and significant view.

The executable lexical grammar lives in `grammar/mud-lexicon.ebnf`.

## 07. Concrete grammar

Chapter: [[07-concrete-grammar]].

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
- Canonical definitions of `thing` and rules, module-unified `start with` and activation through `create Name`.
- Isolated tests with local `start with`, `then`, `after` and `otherwise`.
- Optional `otherwise` diagnostic after an `always` rule body; omitting it produces a warning and a default reason.
- Numeric formats within `Text` interpolations.
- Quantifiers and iterations.

The complete executable grammar lives in `grammar/mud.ebnf`. Parsing produces a lossless CST; this chapter explains ambiguities, precedence, contextual validation and the boundary with desugaring, but does not repeat the entire EBNF.

## 08. Surface abstract syntax

Chapter: [[08-abstract-syntax]].

Defines the semantically relevant forms after the CST and contextual syntactic validation:

- `MudFile` and `MudProject` roots.
- AST of declarations, types, domains, expressions and effects.
- Normalisation of cardinalities, intervals, blocks and contextual literals.
- Structural distinction among the three rule classes.
- Surface `ActionDecl` with `PublicAction` or `Subaction` class; candidate calls are resolved later without introducing an elementary/compound classification.
- Dedicated `TestDecl` node and assertions with optional diagnostics.
- Dedicated nodes for `look`, `message` and public properties.
- Provenance through `SourceOrigin`.
- Ambiguities retained until resolution.

Mechanical and transformation artefacts: `syntax/`.

## 09. Paths, `using`, names and anchors

Chapter: [[09-names-and-anchors]].

Defines:

- Scopes.
- Local and qualified resolution.
- Exact and recursive `using` declarations.
- Mandatory placement of all `using` declarations in the file header.
- Ambiguity.
- Formation and uniqueness of public anchors; functional-dictionary branches use local keys and receive no public anchor.
- Categories `thing::*`, `alias::*`, `family::*`, `magnitude::*`, `unit::*`, `rule::*`, `action::*`, `look::*`, `message::*`, `test::*` and `type::*`.
- Identity under file moves.
- Path and anchor migration.

Juicio principal:

$$
\Gamma \vdash n \rightsquigarrow a
$$

## 10. Type system

Planned file: `10-type-system.md`

Planned scope:

- Built-in, nominal, structural, collection, dictionary, interval, magnitude and union types.
- `Any`, first-class descriptors, callable types and types obtained statically through `~type`.
- Subtyping, compatibility, narrowing, equality, ordering, conversions and inference.
- Typing of anonymous `look` results and `message` payloads, including the join of dynamic calls.
- Interaction between a callable descriptor's static type and the nominal identity needed to bind its signature.

Questions of callable variance, inter-module alias specialisation, joins with incomparable common minima, binding after deletion and anonymous-type identity remain delimited respectively by Q-063, Q-064, Q-065, Q-066 and Q-068.

Juicio principal:

$$
\Gamma;\Sigma \vdash e : \tau
$$

## 11. `Thing`, specialisation and identity

Planned file: `11-things.md`

Planned scope:

- Identity, activity, destruction of a materialisation's own load, rematerialisation from the canonical definition and independent state of concrete and abstract `thing`s.
- Single and multiple specialisation, inheritable schema, defaults and initialisers.
- Integration of `Thing` as the built-in root and of nominal identity/equality rules.
- Modular boundary of `thing`s: visible identity/type versus ordinary state projected through public operations and inter-module specialisation limits.
- `thing` metadata and reflection without confusing them with state fields.

## 12. Nominal aliases and structural values

Planned file: `12-aliases.md`

Planned scope:

- Nominal and structural representation aliases, contextual construction and nominal casting.
- Single and multiple nominal specialisation, inheritance of representation or members, provenance-based deduplication and conflicts between independent members.
- Inherited defaults, immutable values, equality, ordering and enumerability where applicable.
- Reconstruction of immutable aliases through write-back from assignable paths, without introducing mutability into their values.
- Boundary between structural compatibility and explicit acquisition of nominality.
- Alias-specialisation rules across modules, whose exact scope remains open in Q-064.

## 13. Closed value families

Planned file: `13-closed-families.md`

Planned scope:

- Declaration, members, nominality, ordering and enumeration of `family`.
- Uniform schema for associated data, defaults and per-member calculations.
- Equality, ordering, reflection and absence of runtime lifecycle for its values.

## 14. Fields, mutability and capabilities

Planned file: `14-fields-and-mutability.md`

Planned scope:

- Stored and calculated fields, defaults, initialisers and derived views.
- External mutability, inner `[mut]` capability and its composition without implicit deep mutability.
- Participant capability and write accessibility.
- Postfix metadata as information separate from ordinary state and read-only during execution.

## 15. Cardinalities and collections

Planned file: `15-collections.md`

Planned scope:

- Cardinalities, `empty`, multiplicity, uniqueness and ordering.
- Membership, collection algebra, indexing, selection and `take`.
- Inference and preservation of cardinality, domain, ordering and capabilities.
- Snapshots and observable semantics of collection iteration.

## 16. Dictionaries

Planned file: `16-dictionaries.md`

Planned scope:

- Exact and functional dictionaries, their types, cardinalities and queries.
- Associations, keys, iteration, ordering and algebraic operations.
- Indexing within assignable paths, partial write-back on associated values and treatment of missing keys without confusing partial update with complete insertion.
- Branch-selection modes, fallback, dependencies, recursion and termination of functional dictionaries.

## 17. Domains and intervals

Planned file: `17-domains-and-intervals.md`

Planned scope:

- Declared and calculated domains, membership, normalisation, finiteness and enumerability.
- Linear, discontinuous, cyclic and magnitude-dependent intervals.
- Explicit materialisation of enumerable domains through `all D` when an operation must produce a collection.
- Difference between consuming a domain, materialising its enumeration and producing a filtered collection, without implicit conversion of the latter to `Domain`.

## 18. Magnitudes, units and points

Planned file: `18-magnitudes.md`

Planned scope:

- Base, derived and point magnitudes, their representations and domains.
- Units, prefixes, equivalences, normalisation and dimensional arithmetic.
- Coordinates, cycles, presentation, formats and component extraction.
- Temporal magnitudes and calendar/localisation constructs that ultimately belong to the MUD 1.0 profile.

## 19. Expressions

Planned file: `19-expressions.md`

Planned scope:

- Literals, operators, calls, access, comparison, conversion and contextual construction.
- Resolution and elaboration of receivers, arguments and callable values.
- `old`, `allowed`, `eventually`, selection, `take` and `all D` materialisation in expression contexts.
- Purity, narrowing, expected-type propagation and evaluation failures.

## 20. Quantifiers, aggregations and iteration

Planned file: `20-quantifiers-and-iteration.md`

Planned scope:

- Quantifiers and aggregators over finite enumerable sources.
- `for each`, iteration bindings, ordering, filters, steps and membership snapshots.
- Direct consumption of finite domains when no collection is produced and termination requirements for every traversal.

## 21. Boolean rules

Planned file: `21-boolean-rules.md`

Planned scope:

- Pure signatures with explicitly named `for` participants and read-only `given` values.
- Binding of receivers and arguments, domains, defaults and capabilities admitted by a pure query.
- Boolean evaluation, dependencies, memoisation and treatment of non-effective declarations.
- Integration with callable values of Boolean-rule type.

## 22. Reactive rules

Planned file: `22-reactive-rules.md`

Planned scope:

- Set-valued `on` bindings, including finite enumerable related sources and nominal refinements.
- `when`, `changes` and `old` triggers, `if` guards, reactive memory and `then` consequences.
- Appearance, disappearance and temporal identity of bindings.
- Use of a triggered reactive rule as a causal source for other triggers.

## 23. `always` rules

Planned file: `23-always-rules.md`

Planned scope:

- `on` bindings, pure condition, checkpoints and diagnostics.
- Dependencies, suspension and the effect of a violation on resolution.
- Use of `always` evaluation as a causal trigger source, separately from whether its condition is true or false.

## 24. Public boundary: `action`, `look` and `message`

Planned file: `24-public-boundary.md`

Planned scope:

- Contracts visible between modules and to the host for `action`, `look` and `message`; `test` crosses modules only in a test context.
- Modular authorisation through `uses`, transitive closure of the types needed to understand a contract and safe cross-module reflection without silent filtering.
- Host API centred on the identity of public operations, not on a participant chosen as owner.
- `for`/`given` signatures, external capability of `action` versus `subaction`, callable values and binding at the invocation point.
- `look` as a pure query with a coherent caller view and one anonymous result.
- `message` as a causal occurrence, `on` bindings, public payload and internal causal and external stable projections.
- Separation of bindings and payload, multiplicity and delivery ordering, and rollback of external outputs.

Nominal binding of sufficiently erased callable descriptors and external projection of a `message` whose participants cease to exist remain open in Q-066 and Q-067.

## 25. Effects

Planned file: `25-effects.md`

Planned scope:

- Assignments, updates, collection operations, `create`, `destroy` and permitted structural modifications.
- Effectful calls and traversals within a unified `then`.
- Reads, writes, deltas, conflicts and effect composition.
- Elaboration of reconstructible assignable paths and propagation of write-back through immutable values to their root storage.
- Interaction between direct effects and internal calls sharing one causal resolution.

## 26. State and expression evaluation

Planned file: `26-evaluation.md`

Planned scope:

- Environments, read views, store and deterministic expression evaluation.
- Evaluation of calculated fields, partial queries, expected types and failures.
- Coherent views inherited by `look`, including the private delta visible at the call site.
- Evaluation of callables and effective binding once their signature is resolved.

## 27. Action requests and results

Planned file: `27-action-requests.md`

Planned scope:

- External request, binding and initial validation of a root `action`.
- `accepted`, `rejected` and `failed` results, diagnostics, visible state and rollback.
- Relationship among signature validation, guards, stabilisation, final constraints and external publication.

## 28. Root semantics

Planned file: `28-root.md`

Planned scope:

- Root causal resolution, private deltas and textual sequencing within each `then`.
- Integration of internal calls without opening independent transactions.
- Consolidation, normalisation and conflicts among concurrent contributions.
- State observed by each phase of a resolution.

## 29. Wave-based causal semantics

Planned file: `29-waves.md`

Planned scope:

- Snapshots, active bindings, triggers and progression between waves.
- Causal matches with witnesses, multiplicity and conjunction/disjunction composition.
- `message` occurrences and rule firings as consequences available to later waves.
- Effect combination, stabilisation and causal trace.
- Distinction between causal ordering and any reproducible technical ordering within a wave.

## 30. Constraints, `after` and `old`

Planned file: `30-final-constraints.md`

Planned scope:

- Checks of domains, cardinalities, `always` rules and other invariants over tentative states.
- `after` for actions/subactions executed within a resolution and its evaluation over the final tentative stable state.
- Contextual semantics of `old`, including the difference between actions, tests and reactive rules.
- Final rejection/failure and restoration of the previous state where applicable.

## 31. Conflicts, cycles and stabilisation

Planned file: `31-conflicts-and-stabilisation.md`

Planned scope:

- Compatibility and conflict of effects, activations and other concurrent consequences.
- Executable cycles, oscillations and detection of non-stabilisation.
- Purely causal message/firing cycles that may keep consequences pending even without state change.
- Semantic stabilisation condition and separation from technical implementation limits.

## 32. Runtime creation, destruction and identity

Planned file: `32-runtime-lifecycle.md`

Planned scope:

- Activity, materialisation, destruction of a materialisation's own load and rematerialisation from the canonical definition.
- Module `start with` contributions, joint materialisation and first-activation initialisation.
- Latent storage of suspended foreign state, effective projection, dependency suspension and restoration.
- Appearance and disappearance of activity-dependent bindings.

## 33. Randomness

Planned file: `33-randomness.md`

Planned scope:

- Random values and points, seeds, sub-seeds and reproducibility.
- Snapshot caches, randomness in expressions/effects and its relationship to rollback.
- Conditions under which an apparently random operation simplifies to a deterministic choice.

---

# Part IV — Advanced semantic analyses

## 34. Semantic graph

Planned file: `34-semantic-graph.md`

Planned scope:

- Semantic relations after nominal resolution that depend on types, domains, effects or elaboration.
- Reads, writes, dependencies, binding patterns and stochastic dependencies.
- Reconstruction criteria from the programme and relation to the Nominal HIR, without turning the latter into a prematurely semantic graph.

## 35. Speculative query `allowed`

Planned file: `35-allowed.md`

Planned scope:

- Construction and disposal of the speculative world.
- Conversion of results to `Bool`, failure propagation and dependence on queried actions.
- Acyclicity/admissibility conditions and reproducibility of randomness.

## 36. Reachability `eventually`

Planned file: `36-eventually.md`

Planned scope:

- Explored transition system, target state and permitted action sequences.
- Randomness semantics and state equivalence/canonicalisation criteria.
- Search strategies only insofar as they form part of normative meaning.

## 37. Finiteness, enumerability and relevant state

Planned file: `37-finiteness-and-enumerability.md`

Planned scope:

- Finiteness and canonical enumeration of domains and sources.
- Finite-world profiles, relevant state and state canonicalisation.
- Sufficient conditions for exhaustive analysis and constructs requiring enumerability.

## 38. Termination and decidability

Planned file: `38-termination.md`

Planned scope:

- Termination of iterations, resolutions and recursive components.
- Conservative analyses and the boundary between static rejection, runtime failure and undecidability.
- Decidable or semi-decidable properties of advanced constructs.

## 39. Metatheoretic properties

Planned file: `39-properties.md`

Planned scope:

- Hypotheses and proofs about resolution, types, progress, determinism, reproducibility and atomicity.
- Independence from orderings without semantic meaning and correctness of speculative analyses.
- Counterexamples and explicit limits where a property is not valid for all MUD.

---

# Part V — Conformance and appendices

## 40. Diagnostics

Planned file: `40-diagnostics.md`

Planned scope:

- Categories, codes, locations and related anchors.
- Mandatory diagnostics versus drafting freedom.
- Error recovery and relationship between static and dynamic diagnostics.

## 41. Later semantic representation

Planned file: `41-ir.md`

Planned scope:

- Contract between typing/elaboration phases and later consumers once those phases are sufficiently developed.
- Semantic information that must be preserved or may be reconstructed, provenance and versioning criteria if a serialisable representation is adopted.
- Relationship with Surface AST and Nominal HIR without duplicating or degrading their responsibilities.

No ASDL/JSON schema, concrete node or edge names, schema version or storage-versus-reconstruction policy is currently assumed. These details will be fixed only when typing and elaboration surfaces make them justifiable.

## 42. Implementation conformance

Planned file: `42-conformance.md`

Planned scope:

- Implementation profiles and each one's requirements.
- Determinism, version declaration, optional features and conforming materialisation.
- Relationship between frontend, runtime, analysis and normative tooling conformance.

## 43. Declarative tests

Planned file: `43-declarative-tests.md`

Planned scope:

- `test` declarations, fresh isolated world, execution and disposal.
- Static transitive closure of reachable tests and union of **their own** `start with` contributions; ordinary module activation is not part of a test's initial world.
- Prior materialisation/stabilisation, `then`, `after`, `old`, diagnostics and executor results.
- Test visibility between modules exclusively in a test context.

## 44. Conformance suite

Planned file: `44-conformance-suite.md`

Planned scope:

- Valid and invalid cases, diagnostics and normative regressions.
- Current normative mechanical outputs to compare at each phase.
- Transitions, traces and observable properties needed to contrast implementations.

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

## 45. Consolidated grammar

Planned file: `45-consolidated-grammar.md`

Normative appendix generated or verified against `grammar/mud.ebnf`.

## 46. Reserved-word catalogue

Planned file: `46-reserved-words.md`

Normative list and classification as reserved or contextual words, derived from the current lexical grammar.

## 47. End-to-end examples

Planned file: `47-end-to-end-examples.md`

Informative examples built only from rules already specified. They introduce no new behaviour.

## 48. Compatibility and migrations

Planned file: `48-compatibility.md`

Planned scope:

- Compatible and incompatible language changes.
- Anchor evolution and programme migration.
- Compatibility of serialised normative artefacts where an applicable serialisation contract exists.
- Deprecation of syntax and version declarations.

## 49. Normative-rule index

Planned file: `49-normative-index.md`

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

# Related but separate specifications

These documents are not part of the language definition:

```text
tooling/
├── compiler.md
├── cli.md
├── editor-support.md
├── semantic-operator.md
├── git-protocol.md
├── typescript-materialisation.md
└── plugin-codex.md
```

This separation prevents an architectural decision from accidentally becoming a MUD rule.

## Verifiable syntax artefacts

The `syntax/` subdirectory contains the CST contract, Surface ASDL, transformation, production-by-production coverage and editorial validator.

```text
syntax/
├── lossless-cst.md
├── mud-syntax-kinds.yaml
├── mud-surface-ast.asdl
├── cst-to-surface-ast.md
├── syntax-coverage.yaml
├── validate_syntax_model.py
└── cases/
```

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

Recommended first cycle:

```text
thing
→ basic fields
→ Boolean rule
→ action
→ look
→ state
→ message
→ accepted/rejected/failed
```

This allows the complete language to be formalised progressively without starting implementation or postponing every check until the end.

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
