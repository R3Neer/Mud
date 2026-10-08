---
title: Fields mutability and capabilities
aliases:
  - Static authority and effects
tags:
  - mud/specification
status: proposed
normative: true
depends-on:
  - "[[11-type-system]]"
questions:
  - Q-023
decisions:
  - D-146
  - D-137
  - D-133
  - D-019
  - D-026
  - D-037
  - D-046
  - D-060
  - D-080
  - D-098
  - D-100
  - D-101
  - D-103
  - D-105
  - D-109
  - D-111
  - D-112
  - D-114
  - D-117
  - D-118
  - D-119
  - D-120
  - D-121
  - D-123
  - D-066
  - D-126
  - D-128
---

# 15. Fields, mutability and capabilities

## Scope

This chapter defines stored/derived fields, writable places, capabilities, block effect admissibility and the minimum static obligations for effect compatibility. [[11-type-system]] supplies type inclusion and proof evidence; [[21-expressions]] supplies expression/block rules. [[28-effects]] supplies private execution and the root/wave batch boundary; acyclicity proofs for dynamically selected callables remain Q-023. Those uncertainties do not grant additional writes or alter the stored-field schema.

## 1. Places and authority

Let $\pi$ be a symbolic assignable path, $\lambda$ its final storage root, $\tau$ its leaf contract and $\kappa$ its available authority. Define

$$
\Gamma;\Sigma;\Phi\vdash\pi:\mathsf{Place}(\lambda,\tau,\kappa).
$$

A root may be a world stored field, an effect-local stored variable or private storage belonging to a value computation. Its owner and materialisation generation are part of its identity. A path extension may access a stored alias component or exact dictionary association. A calculated field, metadata, literal, computed local or functional-dictionary result is not a replacement destination.

There are two independent permissions: replacing a stored place and editing the state of immediately contained thing identities. The latter is represented by inner mut. Neither implies the other, and neither traverses an alias or nested container without the permission required at that level.

> [!rule] MUD-EFFECT-001 — Writable root
> An assignment/update must have an authorised stored root and a reconstructible path. Access through an immutable alias reconstructs a new alias and writes it back to that root. It does not mutate the original alias value. Ordinary field visibility and all nested permissions remain required.

Exact dictionary indexing at an intermediate path step may yield no association. A partial update then remains a no-op and cannot invent an association or default alias. Direct complete association replacement may insert when the dictionary contract admits it. A functional dictionary has no assignable runtime branch/result path.

Given values and ordinary on roles do not receive outer replacement authority. Only a signature's permitted outer mut slot accepts a caller's writable place. A literal, computed binding or immutable stored binding cannot satisfy it. Inner mut remains legal but inoperative for member types with no editable thing state; tooling may warn and must not manufacture a write.

Alias-overloaded compound updates use an admitted binary signature with the destination as its left operand and a result admissible at that destination. Resolve the place once and evaluate the RHS once; a failed calculation supplies no write. Preserve ordinary reconstructible-path write-back and authority. Such updates contribute absolute replacements; the numeric/set consolidation laws are not inferred from the token. [[28-effects]] defines replacement agreement/conflict.

## 2. Invariance and authority propagation

A supplied place of contract $\tau_s$ satisfies a requested read/write place of contract $\tau_t$ only if both $\tau_s\preceq\tau_t$ and $\tau_t\preceq\tau_s$ are proved. Domains, cardinality and collection guarantees participate, not just nominal names. This prevents a callee from writing a value valid for its parameter but invalid for the caller's storage.

Read-only use may forget stronger guarantees, including authority. Identity-preserving selection, filtering, indexing, slicing, deduplication, reordering and nominal views may retain inner authority already supplied. Creating a different value does not retain the source thing's authority by resemblance.

> [!rule] MUD-EFFECT-002 — No authority amplification
> A derived annotation, conversion, static narrowing, Error handler or foreign wrapper cannot grant authority absent from its inputs. Inner authority reaches immediate thing members only. Pure blocks cannot spend authority to change outside state even when a captured value carries that authority.

For collection algebra, order and inner mut follow these separate propagation laws:

| Operation | Result guarantee from operands $A,B$ |
| --- | --- |
| $A\mathbin{|}B$ | Both operands supply it. |
| $A\mathbin{\&}B$ | Either operand supplies it. |
| $A\mathbin{--}B$ | The left operand supplies it. |
| $A\mathbin{\hat{}}B$ | Both operands supply it. |

Compatible order criteria are required whenever two retained orders meet. Whole-value/keyed uniqueness uses the operation-specific rules in [[21-expressions]] rather than this Boolean authority table. No algebraic result becomes an externally writable place.

## 3. Effect summaries and owner modes

Let $L$ be the private storage region of the current value computation. An effect summary
$\epsilon=(R,P,A,B,T)$ consists of read dependencies $R$, private writes $P$, authorised world effects $A$, external delivery obligations $B$ (including provisional notification and later Ticket confirmation/disposal) and temporal/random/termination requirements $T$. Entries are symbolic paths/operations with provenance, not a prescribed IR schema. Sequential composition retains statement order; concurrent composition retains common-view provenance. Combining summaries does not itself authorise their entries.

Let $\delta$ specify Expression, Value($L$) or Effect together with the owner's static-evaluation requirement where applicable. Static qualifies an existing expression/value computation; it is not a fourth block construction. The judgement
$\Gamma;\Sigma;\Phi;\delta\vdash b:\tau\triangleright(\epsilon,O)$ checks a block and its obligations $O$.

| Owner mode | Admitted computation |
| --- | --- |
| Expression | Externally pure calculation; no storage mutation or real action execution. |
| Value($L$) | Pure calculation plus mutation of storage created within $L$; no captured-place/world writes. |
| Effect | Authorised world and local effects, real action calls, lifecycle operations and tentative causal outputs. |
| Static requirement on Expression/Value($L$) | Closed statically evaluable, externally pure deterministic calculation; permitted private local computation remains private. No runtime-world dependency or real randomness. |

Error production is possible in every mode. Error is not a mutation permission. Randomness, old, changes, imagine and eventually additionally require their contextual contracts; being free of ordinary writes alone does not prove static eligibility or deterministic enumeration predicates.

> [!rule] MUD-EFFECT-003 — Context is inherited
> Initialisers, nested blocks, called operations, recoveries and foreign code inherit the owner's restrictions. Hiding a real action call in a local initialiser cannot make it pure. A value block may mutate a mutable enclosing private local belonging to the same computation, but cannot escape to captured external storage.

An effect block may capture a child's ActionReply as a normal value. A bare child effect call propagates its non-success outcome under the invocation contract. Imagine uses a disposable projection, returns ActionReply and contributes no confirmed writes/delivery; native calls inside it must satisfy isolation as well.

Explicit raise is an observable error-channel effect under the owner permissions, not a world-write footprint. Its Fault prevents normal completion; it does not excuse static checking of source continuations.

## 4. Schemas and initialisation

> [!rule] MUD-EFFECT-004 — Static field schema
> Thing field declarations come exclusively from the canonical schema and admissible specialisation. Every newly declared stored field has an explicit initialiser. Runtime add/remove modify collections or associations and never add/remove field declarations.

Stored thing schema initialisers must be closed and statically evaluable, including every subordinate ValueBlock and native contract they use. Private temporary storage is permitted, but captured runtime-world dependencies and observable effects are not. Stored locals inside a runtime value/effect computation instead inherit that owner's mode and are not schema initialisers.

Initialisation inherits declaration origins and existing override precedence. It does not inherit another thing's mutable state. A refinement keeps or replaces an initialiser that meets every inherited contract. Destroy/create uses a fresh materialisation generation; writes to the destroyed generation do not become writes to the new one.

Stored fields require outer authority for replacement. Calculated fields and `:=` locals are recomputed derivations without assignable storage. A live local reads the semantic view at its use, not an earlier captured value; `=` captures at slot creation. Derived ValueBlock computation may mutate only its fresh private storage. Type holes in stored annotations must be uniquely solved before execution and do not alter capability or cardinality proof obligations. Their declared domain, cardinality, uniqueness and order apply the specified derived transformations/checks; inner mut is an authority requirement. Stored collections do not automatically recompute or prune their membership to mimic derived views.

Explicit alias defaults are closed pure static values. Every family member supplies each required datum or uses its explicit schema default. Intrinsic metadata defaults have their own contracts; user-declared metadata needs an explicit effective value and all runtime metadata access is read-only.

## 5. Complete effect-block contract

A then sequence reads its own preceding private delta. A collection may temporarily fall outside its declared cardinality during that sequence, provided its completed projection preserves the contract. Different blocks cannot rely on a later wave to repair their completed projections.

Let $t$ be a complete effect block, $p$ an affected stored collection with bounds $[\ell_p,u_p]$, and $W$ an admitted entry state. Define $C(t,p,W)$ as the size after its private sequence completes. The mandatory proof is

$$
\forall W\text{ admitted by types and guards}.\quad
\ell_p\leq C(t,p,W)\leq u_p.
$$

> [!rule] MUD-EFFECT-005 — Static stored cardinality preservation
> Every complete then and every possible consolidation must prove stored cardinality preservation or establish that the relevant blocks cannot coexist. Unknown is insufficient. Runtime validation remains a safeguard, not permission to defer an unproved cardinality obligation.

This obligation differs from a readonly query producing empty, a value conversion requiring a runtime domain check or an argument rejected at admission. A protected block's computing error may be recovered, but a handler does not legalise an otherwise statically invalid stored-cardinality programme.

### Minimum transfer evidence

The required analysis tracks initial size intervals, membership/multiplicity facts, uniqueness criteria, guards and the complete sequence. It preserves correlations necessary to prove a replacement, rather than independently widening each intermediate statement.

| Transfer | Required conservative fact |
| --- | --- |
| Assignment | The supplied completed value meets the target contract. |
| Add one member | Increase by at most one; exact change needs presence/multiplicity evidence. |
| Remove one occurrence | Decrease by at most one; exact change needs presence/multiplicity evidence. |
| Remove then add in a singleton | A known present removed member followed by one valid replacement ends at one. |
| Exact association replacement | Existing-key replacement preserves size; a proved absent key adds one. |
| Exact-key deletion | A proved present key removes one; a proved absent key changes none. |
| Selection/filtering | Output upper bound is the input upper bound; lower bound is zero without survivor evidence. |
| Guarded branches | Analyse each admitted branch under its established facts and combine their bounds. |
| Concurrent blocks | Compose their semantic destinations/updates, including deduplication, before checking joint bounds. |

If target membership, correlated keys or possible coexistence remain unknown, the bounds must include all possibilities. Syntactically different paths are not necessarily disjoint. Finite interval arithmetic and witnessed finite cases are required proof mechanisms; more elaborate sound proofs cannot remove runtime safeguards.

## 6. Conflict classification

Each symbolic destination contains its storage root, member/key/component path and generation. The analysis may establish equal, disjoint or potentially overlapping destinations. Equality cannot be inferred from spelling alone across different owners; disjointness cannot be inferred from different variable names.

> [!rule] MUD-EFFECT-006 — Static conflicts and residual overlaps
> A proved inevitable incompatible composition is a static error. A proved possible conflict is reported as a warning and checked during consolidation. If semantic destination overlap cannot be decided, the unresolved coincidence is also checked during consolidation, subject in both cases to the stronger mandatory stored-cardinality proof. Unknown overlap is neither proved disjointness nor a reason to impose source-order priority.

Inevitable means the conflict follows from the admitted entry/guard facts for the applicable contributions; possible means there is a witnessed admitted conflicting case without that universal conclusion. A runtime check handles actual co-occurrence and values, without turning a warning into permission to defer cardinality proof.

The minimum required cases are identical resolved roots with equal constant keys/component paths, distinct constant keys, known distinct components of one alias and known different generations. Apply the existing replacement-before-change algebra: equal replacements merge, different replacements conflict, replacement precedes compatible arithmetic/partial changes, disjoint components compose, same-key deletion wins, and whole-value/keyed uniqueness is checked jointly. Heterogeneous collection updates without a specified algebra conflict.

Sequential normalisation precedes sibling composition: a later whole replacement erases earlier local updates to that replaced value. Exact-dictionary uniqueness may cause a proposal to become a no-op under the stable-provenance collision rules. Cardinality proof must include that outcome; an intended insertion is not guaranteed to increase size merely because its source contains add.

The minimum does not require a complete solver for arbitrary symbolic predicates. Statically safe but unproved cardinality cases may be rejected. Potential value/key conflicts with proved safe cardinalities retain their defined runtime error behaviour. [[28-effects]] defines the operational composition boundary without weakening these static conflict rules.

## 7. Foreign operations and recovery

Foreign contracts identify captures, converted types, read dependencies, write footprints, static/deterministic eligibility, Error translation and isolation/lifetime obligations. A read-only native parameter does not prove purity. A checked or explicitly trusted contract may supply these premises; tooling identifies trusted obligations in English. Unknown effects cannot be treated as pure.

Wrappers preserve authority, nominal identity, exact representations and collection contracts. They route authorised writes into the owning journal, publish no partial exports on failure and retain no writable handle after the evaluation. Irreversible delivery requires confirmed delivery or an explicit transactional contract. Native resource cleanup does not introduce a MUD finally.

Handlers run after the protected scope has rolled back. Their bindings are immutable Error values, not writable projections of failed locals. Recovery then obeys the protected block mode and result contract. Recovery effects compose tentatively; a remaining/new error discards them under the block recovery contract. A raised Error's optional cause is ordinary finite immutable data, not authority over the originating state.

## 8. Elaboration and conformance

Elaboration records storage roots, reconstructible paths, generation dependencies, authorised footprints, per-block proof obligations and permitted runtime overlap checks. It preserves incorporated operator update classes for consolidation; user-overloaded updates retain their computed replacement class rather than acquiring an inferred algebra. It does not add those fields to nominal HIR or prescribe a semantic IR layout.

Conformance instances in [[types/typing-cases.yaml]] cover writable invariance, nested capability boundaries, private-region mutation, cardinality-preserving replacement, rejected unknown cardinality and residual key overlap. Full operational wave correctness and dynamic lifetime/acyclicity proofs remain separately scoped.
