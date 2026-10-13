---
title: Static formalisation phase integration review
status: current
tags:
  - mud/analysis
---

# Static formalisation phase integration review

## Completed scope

Chapters 11, 15 and 21 develop the accepted static contracts: finite type graphs, recursive productivity, nominal/representation compatibility, variance, checking and inference, schema initialization, root and inner permissions, block modes, effect/cardinality obligations, expression families, recovery and abstract foreign contracts. D-122 through D-124 record integration. Q-056, Q-006 and Q-021 close their remaining formal proof/minimum-analysis boundaries with rules and contrasting evidence.

The nominal HIR was reviewed with chapter 10. It retains only names, scopes, symbols, candidate sets and nominal relations; no type or effect fields were added. Existing grammar and AST forms are reused.

## Validation limits

The finite witness checker verifies its declared evidence language and constructor/rule coverage. It is not a parser, complete typechecker or execution engine. The static safety statement is conditional on admitted runtime predicates, valid operational semantics and checked/trusted foreign contracts. No whole-engine preservation/progress theorem is claimed.

All three chapters remain proposed, pending the separate publication lifecycle. Remaining numeric/operator, TypeKind catalogue, general termination, native ABI and complete causal-engine questions keep their active scope. They are not silently answered by this phase. Semantic IR encoding, Rust compiler/backend, adapters and REPL implementation remain subsequent work.

## Repository review

After integration, repository-wide semantic/editorial reviews use ordinary temporary lists outside the repository. Corrections are committed as coherent units; review continues until the next list is empty. Temporary lists are removed and never staged.

## Static chapter blocker audit — 2026-10-13

### Scope and result

This audit concerns chapters 12–26, including chapter 20 and the static contracts of reactive/always rules and public operations. Chapters 01–02 are supporting scope/glossary work. Chapter 28 supplies existing effect premises. Chapter 06 descriptor/dependency design, pending chapter 27 interoperability protocols, causal chapters 29–34, textual patches and host protocols are excluded.

There is no unresolved question that must be answered as a blanket prerequisite to drafting this static chapter set. The next work should draft coherent independent units, formalize already selected policies and ask only when a concrete unselected case prevents a rule. This does not certify that every full chapter can already be published: local uncertain features and exact certification procedures retain their active questions. Conditional judgements over explicit evidence may describe established static contracts, but do not constitute the completed normative analysis algorithm.

### Decisions integrated in this update

- D-152: ordered prefix demand under pruning, original-operand equality/inequality/xor demand, value-consuming domain/collection boundaries and transparent identical shapes. Q-050 is closed with normative/corpus evidence and removed from active indexes/exports.
- D-153: ordered operand descriptors expose names and types; operator metadata uses the two established descriptor attachment forms; complete textual canonical anchor policy. Q-075 remains partial for exact encoding and reflective schema, not for those choices.
- D-154: stored field/local interval endpoints must be transitively stable; derived fields/locals retain dynamic domains in each read's coherent view. Immutable scalar capture differs from an immutable handle to mutable state.
- D-155: the same normative analysis procedure per language version, with a reusable reference analyzer; distinguish proved violation, completed-but-unproved obligation and interrupted tool verification. Q-028/Q-029 remain partial for procedures/classes not yet specified. No lexicographic-descent rule was accepted.

### Chapter-by-chapter dependencies

| Unit | Work that can proceed | Local boundary before claiming complete publication |
| --- | --- | --- |
| 01–02 | Static scope/conformance distinctions and accepted terminology | Full project version declaration/migration is Q-038 with descriptor/IR work; do not invent it for the supporting static scope. |
| 12 | Thing identity, static ancestry/schema, visibility and reflection | Runtime identity registry encoding/lifecycle execution remains separate Q-016/Q-072 work. |
| 13 | Alias construction, specialization, equality, generics and operator contracts | Q-075 exact operator encoding/schema; generic closure obligations do not themselves complete the uniform proof procedure. |
| 14 | Closed families, generic applications, member/data contracts and ordering | No identified new semantic-choice blocker in the accepted core. |
| 15 | Stored/derived fields, stable interval bounds, capabilities and write admission | Q-023 dynamic-call proof/impact method; do not turn signature compatibility into acyclicity evidence. |
| 16 | Finite collections, cardinalities, nested empty, algebra and access | Q-032 stochastic caching/retries are runtime boundaries, not permission to change static cardinality or purity rules. |
| 17 | Exact/functional dictionary typing, associations, modes and queries | Q-029 full recursion certification; retain established well-founded-measure obligations without accepting the unchosen lexicographic proposal. |
| 18 | Domain/interval contracts, stable versus live bounds, exact normalization | Q-028 full uniform certification procedure; deeper reachable-state proofs stay with advanced reachability analysis. |
| 19 | Exact dimensional composition, units, prefixes and established numeric signatures | Q-034 dimensional-normalization algorithm/diagnostics must be specified; Q-058 explicitly retains Rum-derived representation inference and portable literal/constant evaluation choices. |
| 20 | Block categories, Normal/Fault separation, Error-only recovery and handler typing | Q-007 exhaustive external/adapter error codes, cancellation and runtime defects are not preconditions for the established Error/Refusal type and recovery contracts. Q-059 test execution observation is separate. |
| 21 | Syntax-directed expression typing and the integrated pruning/operator/raise rules | Local Q-075/Q-058 and certification methods above; do not claim all operational expression behavior is complete. |
| 22 | Source enumeration premises, quantifier results, binding patterns and finite traversal contracts | Q-028/Q-029 exact certification procedure; iteration admission can be specified over evidence while this method remains explicit and incomplete. |
| 23 | Pure signatures, argument/result contracts, dependencies and inactive-rule pruning | General recursive body certification is Q-029; no need to design causal scheduling or global caching to draft these contracts. |
| 24–25 | Reactive/always signatures, binding/trigger categories, pure conditions and effect permissions | Q-072 causal observation/readiness/checkpoint algorithm and Q-020 oscillation detection remain excluded operational dependencies. |
| 26 | Public type closure, uses/part-only/sub-operation boundary, callable binding and produced types | Q-069/Q-070 native protocols, Q-073 patches and Q-074 host protocols remain excluded; static signatures do not invent these protocols. |

### Remaining questions: decisions versus specification work

- Q-075: the selection, identity policy, operand information and metadata syntax choices are accepted. Draft the exact canonical encoding and reflection schema; ask only if a concrete case requires another semantic choice. It still blocks complete publication of those operator identity/reflection surfaces until specified and evidenced.
- Q-060: audit every builtin/descriptor projection against the fixed catalogue and complete its conformance table. No return to extensible TypeKind is needed. Cross-version migration/compatibility remains coordinated with Q-038 and does not block the fixed-version core inventory. Unknown descriptor categories cannot be invented during that audit.
- Q-034: formalize dimensional normalization and check Money interactions against established numeric signatures. Do not ask again about numeric-only magnitude representations. An unsupported concrete interaction must be exposed rather than guessed.
- Q-028/Q-029/Q-023: exact uniform certification and dynamic-call impact/acyclicity methods remain incomplete. They block a claim to a complete static admission procedure, not drafting independent construct contracts. Whether lexicographic descent becomes mandatory is not an urgent prerequisite; the author did not accept that proposal.
- Q-058: a genuine known unselected semantic surface, including representation inference for derived magnitudes involving Rum. Resolve its static inference/literal/constant-evaluation subset before claiming those cases complete; general backend execution/IR details need not stop exact-numeric units.

No other currently active question was identified as a blanket static drafting blocker. In particular Q-008/Q-014/Q-015/Q-036–Q-040 concern tooling, migration or product operation; Q-009 concerns a later semantic IR schema. Q-026/Q-027/Q-030/Q-031 and the deeper portions of Q-028/Q-029 concern reachability/advanced profiles. Q-033 calendar/localization design must not be invented as part of the accepted numeric magnitude core. Q-035 speculative budgets/cache isolation, Q-059 test execution traces and Q-069–Q-074 operational/foreign/world/host work retain their own scopes. Their exclusion does not close them or waive independent static contracts.

### Next drafting order and editorial status

Start with 12/14 and the independent alias contracts in 13; formalize Q-075/Q-060 surfaces alongside that work. Continue with stored/derived fields and collections/dictionaries/domains (15–18), exact magnitudes (19), shared blocks/recovery (20) and the focused 21–23 integration. Draft 24–26 static interfaces using explicit operational boundaries. Ask about Rum inference when reaching its affected unit, or any other indispensable concrete case discovered during drafting.

Chapters 08–11, 15 and 21 remain proposed; 01–02 remain skeletons. Planned 12–14, 16–20 and 22–26 have not been created or declared complete in this update. Publication remains a separate chapter-by-chapter lifecycle with conformance evidence and an empty final consistency review.

## Follow-up closure — 2026-10-13

Q-075, Q-060 and Q-034 are now closed with complete scoped specifications and evidence: D-156 operator identities/reflection, D-157 fixed TypeKind inventory and D-158 dimensions/representation boundaries. The author accepted DeclarationKind.Operator and auxiliary alias/Prefix classifications. Exact source/operator/typed phase boundaries remain intact.

D-159 formalizes the independent static part of Q-038 in chapter 01, now draft. Project descriptor/default/discovery and source/IR/persisted-world migration remain outside scope, so Q-038 remains partial. Chapter 02 is still a skeleton; the other developed chapters remain proposed. This does not publish them or create the pending 12–26 chapters.

The next author discussion is the static subset of Q-058: Rum literal/constant conversion and any remaining derived representation inference. Exact numeric signatures, rejection of implicit exact/Rum mixing and dimensional normalization must not be reopened. After those indispensable choices, continue the chapter drafting order above; ask only for a concrete unselected case, not an advanced-analysis proposal as a blanket prerequisite.

## Numeric closure — 2026-10-13

D-160 closes Q-058 with portable nearest-even binary64 conversion and arithmetic, gradual underflow, canonical positive zero, truncating-quotient remainder and explicit source rounding sites. Mud retains finite-only values and zero-divisor faults. Derived Rum representations follow existing signatures; no implicit exact/Rum mixing is introduced. Six finite rational certificates and seven declarative cases cover the boundary. Physical IR and foreign protocols remain excluded. Independent chapter drafting can now proceed without this numeric blocker.
