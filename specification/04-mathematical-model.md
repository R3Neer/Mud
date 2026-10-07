---
title: Mathematical foundations of the MUD world
aliases:
  - Mathematical model of the MUD world
tags:
  - mud/specification
  - mud/normativa
status: draft
normative: true
depends-on:
  - "[[02-terminology]]"
  - "[[03-notation]]"
questions: []
decisions:
  - D-134
  - D-133
  - D-111
  - D-110
  - D-014
  - D-015
  - D-054
  - D-025
  - D-019
  - D-026
  - D-021
  - D-055
  - D-068
  - D-077
  - D-085
  - D-086
  - D-087
  - D-096
  - D-099
  - D-103
  - D-112
  - D-113
  - D-117
  - D-118
  - D-119
  - D-120
  - D-122
  - D-123
  - D-124
  - D-125
  - D-126
---

# 04. Mathematical foundations of the MUD world

## Scope

This chapter defines the semantic objects and invariants shared by the static language and the world model. It distinguishes the programme's canonical definitions, activation, owned storage and effective projection. It records the established boundaries of execution without supplying a complete transition system.

The chapter remains a draft. The operational chapters must define complete judgments and conformance traces for the accepted lifecycle and observation contracts without changing the invariants below.

## Canonical programme and identity

Let $P$ be a programme, $\mathcal D_P$ its catalogue of declaration identities, and $\operatorname{Def}_P(d)$ the canonical definition of $d\in\mathcal D_P$. The catalogue includes definitions that are currently inactive. Name resolution and anchors identifying these declarations are defined in [[09-names-and-anchors]]; presentation metadata does not supply identity.

Every `thing` has one top-level canonical definition, including its abstract/concrete category, direct predecessors and body. A concrete `thing` denotes one particular thing with its own state and may also be an ancestor. An abstract `thing` belongs to the same nominal domain but has no own concrete payload. MUD does not turn these declarations into classes with separately created instances.

Let $\mathcal T_P\subseteq\mathcal D_P$ be the `thing` identities, including the built-in abstract `Thing`. Let $R_P\subseteq\mathcal T_P\times\mathcal T_P$ contain direct specialisation edges, oriented from descendant to predecessor. A root other than `Thing` with no declared `as` predecessors has an implicit semantic edge to `Thing`; that edge is not a declared predecessor. The graph is acyclic and its reflexive-transitive closure defines canonical `is`:

$$
\operatorname{is}_P:=R_P^*.
$$

Consequently `is` is a partial order. `as` specifies direct specialisation, while `iis` and `iis not` require or exclude exact effective nominal type. They are not identity comparisons. Specialisation inherits declarations, constraints, domains and effective defaults, never an ancestor's active mutable state.

`Thing` is always effective, has no own concrete state, cannot be created or destroyed, and is excluded from `start with` and `all Thing`. A typed collection of `thing`s requires strict membership: for member $c$ and nominal type $T$, $c\ne T\land c\,\operatorname{is}_P\,T$. There is no `reflexive` modifier.

## Values and nominal aliases

Let $\mathcal V_P$ denote the semantic values admitted by the programme's type contracts. This symbol does not imply that all such values can be enumerated. `thing` values compare by identity; alias values are finite immutable structural values. The equality and collection contracts are defined in [[10-type-system]].

Aliases form a separate nominal partial order whose nodes are value types, not activatable identities. Abstract aliases are inhabited through concrete descendants. Statically admitted generic applications have a proven finite closure. Productive recursion describes that finite type graph with finite individual values; it does not introduce cyclic value identity or imply finite enumeration.

A descendant of several nominal aliases must satisfy every predecessor: its admitted values are contained in their intersection, not their union. Effective structural members are aggregated by declaration origin. Reaching one member by several inheritance paths does not duplicate it; independent origins with the same name conflict. Part visibility and permission to specialise follow [[09-names-and-anchors]].

## Activation and materialisation

Let $\mathcal L_P\subseteq\mathcal D_P$ contain the declarations with explicit lifecycle: concrete and abstract `thing`s, Boolean rules, reactive rules and `always` rules, excluding `Thing`. For a world $W$ of $P$, activation is a total predicate:

$$
\operatorname{active}_W:\mathcal L_P\to\{\bot,\top\}.
$$

Activation does not change $\operatorname{Def}_P$. `create d` and `destroy d` refer to an already-defined `thing` or rule; they do not introduce a category, body, predecessors or implicit captures from their caller. Aliases, actions and the static dimensional system are not lifecycle targets.

An active concrete `thing` has its own materialisation. Abstract `thing`s have activation without concrete payload; active rules have the memory applicable to their category. A materialisation generation distinguishes successive activations of one concrete identity. Generation tokens are semantic distinctions, not programmer-visible names or a required integer encoding.

Destroying a concrete owner ends its materialisation and discards its own stored data. A subsequent creation uses the same canonical identity with a fresh generation and schema initialisation; it does not restore the destroyed payload. Stored writes target the generation observed by their branch and cannot migrate to a later generation.

> [!rule] MUD-LIFE-001 — Instruction-local lifecycle admission
> `create d` on an explicitly active declaration and `destroy d` on an explicitly inactive declaration are successful no-ops. Each instruction tests the current private view, including preceding effects and internal calls. A redundant instruction neither skips its enclosing rule/block/action nor prevents later instructions. Suspension is distinct from explicit inactivity.

No-op instructions change no generation, initialised payload or temporal memory and produce no refusal/error merely for redundancy. An otherwise successful action returns Success. Multiple lifecycle operations have no joint all-absent/all-present precondition. Effective operations retain validation, tentative composition and rollback; parallel branch consolidation retains its existing rules.

> [!rule] MUD-TIME-001 — Binding identity and observation continuity
> A persistent reactive binding is identified by the canonical rule and the mapping of named roles to participant identities, independently of field values or enumeration order. Its temporal memory belongs to an observation episode under the same rule activation and concrete participant materialisations. Causal occurrences retain their separate identity and multiplicity.

Absence or dependency suspension in a wave snapshot ends the observation episode. Reappearance establishes a new baseline without firing merely because observation resumes. Explicit destruction/recreation of a rule or concrete participant also starts a new episode, even when the generation changes between snapshots without an observable absence. Suspension does not discard independently owned world storage. A false `if` suppresses consequences, not continued observation. No-op lifecycle instructions do not reset the episode.

> [!rule] MUD-TIME-002 — Observation baseline
> Initial `start with` bindings retain virtual previous false for Boolean rising branches, while `changes` does not pulse and `old` reads the initial snapshot. Later or resumed episodes use their first observable wave as baseline without a memory-based temporal pulse; comparison begins in the next wave. A genuinely observed value changing from `empty` to a member is a change; missing observation history is not an empty value.

Baseline rules govern the memory-based Boolean/changes/old branches, not the identity or availability of direct message/firing occurrences. Those sources retain their causal-match contracts. Bindings remain fixed at the beginning of each wave. Memory changes are tentative and obey rollback and `imagine` isolation.

## Owned storage and static schema

For a concrete owner $d$, let $\operatorname{Fields}_P(d)$ be its canonical stored field declarations, including inherited declarations identified by origin. Runtime cannot add or delete these declarations. Each newly declared stored field has an explicit initialiser; descendants inherit schema initialisation. Required alias components and family data receive explicit values or explicit effective defaults. A type never supplies a default value.

For an existing materialisation generation $g$ of $d$, write $\operatorname{store}_W(d,g,f)$ for the stored value at field origin $f\in\operatorname{Fields}_P(d)$. This is a partial selector over owned storage, not a declaration of a physical memory layout. A field can have stored data while it is unavailable in the effective projection.

Every field denotes a collection. Outer membership mutability and immediate-member capability are independent, including at cardinality `[1]`. Runtime changes values, writable membership, relations and activity within their permissions. [[14-fields-and-mutability]] defines schema, initialisation and capability contracts.

Stored collection membership persists until an authorised change or an applicable lifecycle operation. Derived fields are recalculated from the current evaluation snapshot; they have no independently writable membership. An inner `[mut]` contract requires authority from the source and preserves it through identity-preserving transformations. It affects immediate members, not nested membership or unrestricted external mutation.

## Effective projection and suspension

$\operatorname{Effective}(W)$ is the projection of definitions and stored data currently usable in $W$. It differs from both the canonical catalogue and the activation predicate. A declaration with an inactive hard dependency is suspended as a whole: its signature, participants and fields are not partially rewritten. Suspension does not end its own materialisation or discard its independently owned payload.

Hard dependencies include the owner, declared type and declarations required to interpret a field's domain and shape. A dependent action can become unavailable even though actions are not explicitly destroyable. A suspended reactive rule produces no bindings; a suspended `always` rule imposes no current check; a suspended Boolean rule is unavailable for evaluation.

Canonical specialisation edges survive destruction. Specialisation alone is not a hard dependency that suspends every descendant: an active descendant may remain effective with its own applicable fields while inherited fields requiring the inactive predecessor are unavailable. The effective graph may bridge inactive intermediate ancestors, without altering canonical `is` or rewriting the schema. Restoring a dependency restores the applicable projection and retained foreign-owned storage, not the destroyed dependency's former own payload.

A relation without `mut` capability retains membership of a withdrawn identity latently and may restore it on creation of the same identity. A relation with that capability removes the stored affiliation; creation alone does not restore it. Authorised `remove` also removes latent membership. Destroying the referenced identity does not otherwise clear data belonging to independently owned declarations.

No confirmed state has an effective collection cardinality contrary to its declaration. Destruction commits only if resulting domains and cardinalities remain valid; an invalid transition produces Error occurrences and rolls back. Creation validates jointly the fresh own payload, restored latent memberships and external declarations becoming effective again. An invalid restoration produces Errors and complete rollback; no partial materialisation is confirmed. These requirements do not demand erasing suspended storage or define a complete algorithm for computing the effective projection.

## Confirmed world and tentative resolution

Let $W_c$ denote the confirmed world and $W_t$ a tentative projection in one resolution. Private branch deltas and consolidated wave projections remain tentative. Later waves can read consolidated tentative changes while $W_c$ remains unchanged. These distinctions impose no textual patch format, Git merge algorithm or physical journal layout.

Each invocation owns the causal work it starts. Jointly caused consequences belong to their common enclosing invocation. An invocation's `after` is evaluated when its owned waves have stabilised, before it returns; it is not deferred until the outer invocation completes or rechecked later. Successful outer completion confirms the tentative world atomically.

`always` invariants are checked after the consolidated root and after every consolidated wave. A false condition produces `AlwaysRefusal`; an unsuccessful evaluation produces Error occurrences. Later waves cannot repair a failed checkpoint. Hard-dependent rules are checked when effective again.

Message occurrence data consists of identity, declaration, canonical participant bindings, birth view/wave, frozen payload and rollback-scope provenance. For each externally published occurrence $o$, its host ticket has $s(o)\in\{\mathrm{Waiting},\mathrm{Kept},\mathrm{Dropped}\}$. The only transitions are Waiting to Kept after outer confirmation, or Waiting to Dropped after disposal of a containing scope. Kept and Dropped are terminal. A consolidated validated wave may publish Waiting without changing $W_c$; these observations and the confirmed world are distinct. [[07-concrete-grammar]] defines payload, publication and read-only subscription contracts.

`imagine` executes the same invocation protocol in isolation, returns its `ActionReply` and always discards tentative changes. It leaves the confirmed world, queues, logs, randomness and resolution identity unchanged.

Error occurrences belong to the resolution's error channel, not automatically to world storage. Block recovery rolls back its protected failed work before running handlers. Successful recovery remains tentative; unhandled or newly raised errors propagate. Refusal is not an Error occurrence and is not selected by `otherwise`. Selection, occurrence multiplicity, handler composition and ordinary observation of replies are defined in [[19-expressions]].

## Initial and test worlds

Each part contributes at most one `start with`: a static expression yielding an activatable declaration or a flat finite collection of `thing | rule`. It permits no instructions, effects or nested collections. An omitted contribution is empty. Contributions are unordered, deduplicated and materialised jointly before initial stabilisation, as defined in [[07-concrete-grammar]].

Every test constructs a fresh isolated world. The static transitive closure of reachable tests supplies the combined initial contributions before the test root. Tests are not world declarations or the host's public API; cross-part test visibility exists only in the test context. The test world and all its outputs are discarded at completion.

## Metadata and observations

Identity and effective nominal type are independent of presentation. `~name` has type `Name`; when supported, its default comes from the unqualified nominal identifier and may be configured in the declaration or model. Distinct identities may share a presentation name. Metadata is not inherited.

All postfix `~` access is read-only during execution. `~path`, `~anchor` and `~file` are intrinsic, nonconfigurable identity/provenance properties. Their supported categories and descriptor contracts are defined in [[09-names-and-anchors]] and [[19-expressions]].

## Boundary of the operational formalisation

The objects above are a shared foundation, not a complete state tuple, scheduler, transition relation or serialisation format. Operational definitions must account for activation, generations, retained storage, effective projection and tentative ownership. [[25-effects]] supplies private effect judgments, recovery boundaries and root/wave batch consolidation. The remaining operational chapters must complete scheduler/evaluation and invocation protocols without changing that effect boundary.

Lifecycle admission and reactive observation continuity are fixed by the contracts above. Complete lifecycle/observation and scheduler protocol judgments and their conformance traces remain to be formalised; a complete evaluator cannot be inferred from these invariants alone.
