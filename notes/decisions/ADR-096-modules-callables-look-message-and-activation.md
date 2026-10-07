---
id: D-096
title: "Parts, callables, `look`, `message` and activation"
status: current
date: 2026-08-28
supersedes:
  - "D-027"
superseded-by: []
questions:
  - "Q-051"
  - "Q-052"
  - "Q-062"
  - "Q-063"
  - "Q-064"
  - "Q-065"
  - "Q-066"
  - "Q-067"
  - "Q-068"
affects:
  - "parts, visibility and reflection"
  - "actions, subactions and `then`"
  - "`look`, `message` and triggers"
  - "domains, `all` and selection"
  - "initial activation and tests"
  - "grammar, CST, AST, IR, typing, resolution and host boundary"
---

# ADR-096 — Parts, callables, `look`, `message` and activation

- Amended by: [[ADR-119-invocation-owned-completion-and-imagine|D-119]].

- Amended by: [[ADR-118-action-replies-refusals-and-errors|D-118]].

- Amended by: [[ADR-116-contract-visible-cross-module-specialisation|D-116]].

- Amended by: [[ADR-115-static-produced-types-and-union-joins|D-115]].

- Amended by: [[ADR-114-callable-variance-and-static-named-binding|D-114]].

- Modified by: [[ADR-101-value-blocks-stored-local-variables-and-witness-extrema|D-101]].

- Supersedes: [[ADR-027-departures-from-the-model-by-means-of-look-and-message|D-027]].
- Modifies: [[ADR-036-participants-recipients-and-calls|D-036]], [[ADR-041-contracts-under-the-three-types-of-rules|D-041]], [[ADR-042-shares-root-and-results|D-042]], [[ADR-045-causal-resolution-connections-and-queue|D-045]], [[ADR-058-temporal-triggers-changes-and-reactive-old|D-058]], [[ADR-063-signatures-given-and-joint-on-bindings|D-063]], [[ADR-075-enumerable-domains-all-and-derived-value-form|D-075]], [[ADR-081-collection-filtering-take-and-indexing|D-081]], [[ADR-085-functional-dictionaries-metadata-and-structured-activation|D-085]], [[ADR-087-reflective-metadata-stable-descriptors-and-external-visibility|D-087]] and [[ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]].
- Amendments: [[ADR-131-parts-file-privacy-and-sub-operations|D-131]], [[ADR-132-minimal-part-manifests-and-direct-uses|D-132]].

- Modified by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].

- Amended by: [[ADR-109-foreign-language-blocks-and-value-exports|D-109]].

## Context

MUD's evolution had left several artificially separate boundaries: elementary versus compound actions, `look` as an essentially external query, `message` as output deferred to the host, separate activation in `things` and `rules`, and implicit domain consumption in operations producing collections. These separations interact poorly when the language is organised into parts, permits callable values and uses wave-based causal resolution.

The local manifest grammar is specified by D-132; external messages are specified by the causal delivery contract.

- Amended by: [[ADR-133-provisional-messages-and-scope-aware-tickets|D-133]].

## Decision

### A single `then` model

The semantic separation between elementary and compound actions is removed. A `then` is an ordered sequence of consequences and may mix calculated locals, immutable or `mut` stored locals, direct effects, calls to `action` or `subaction`, and `for each` traversals. Shared behaviour preambles contain pure calculated `:=` bindings or externally pure `from` blocks.

An internal call executes at its textual position within the resolution's private delta: it observes earlier effects visible at that point, contributes its effects to the same resolution, and later statements observe those effects. It does not open an independent transaction.

Each invocation checks after once its owned work stabilizes, before its caller continues. Shared consequences belong to the nearest common enclosing invocation; nested completion remains tentative. An ordered `for each` retains sequential semantics between iterations; in an unordered one, sibling-iteration deltas are consolidated under the ordinary concurrency rules.

An `action` or `subaction` may be invoked from any semantic `then` context, including a reactive rule's `then`. `action` also retains outer-root capability; `subaction` does not. A bare invocation effect propagates Errors or Refusal; explicit reply-value capture permits observation after rolling back the unsuccessful child attempt.

### Parts and visibility

A part is an encapsulation unit within a Mud world project. Each `.mud` belongs to the part of its nearest ancestor `mud.part`; no such ancestor is a static error. A nested manifest opens a new part. The part path is derived from its directory relative to the world root, without a repeated name declaration.

A `mud.part` is a minimal manifest: only whitespace, comments and zero or more `uses exact.part.path` statements. Empty manifests are valid. Statements use ordinary newline or `;` separation. Paths are exact MudPaths from the world root and must identify directories containing a `mud.part`. Relative paths, wildcard paths, grouped lists, metadata, source declarations and backend settings are invalid. A repeated `uses` is redundant and produces a warning.

```mud
uses world.people
uses world.weather; uses world.time
```

`uses` authorises direct access to another part's visible contract; it does not import short names. `using` imports names inside an `.mud` and does not grant permission. Operational access is not transitive: if A uses B and B uses C, A cannot call C without its own uses C. The transitive type closure needed to represent B's visible contract remains available, without exporting all of C's operations. Fully qualified references obey the same checks.

The optional header `part only` applies to its entire `.mud` file. It must be the first content after an optional BOM and whitespace; comments, metadata, `using` and declarations cannot precede it. It is followed by ordinary statement separation. Declarations remain available throughout their owning part but cannot cross to another part or the host. The header does not affect other files or nested parts, and is not accepted in `mud.part`. No declaration-level visibility modifiers or export-selection list exist.

```mud
part only
using world.people

sublook Detail { score := 0 }
```

Normal `action`, `look` and `message` form host operations. Their sub forms `subaction`, `sublook` and `submessage` are visible to authorised Mud parts by default but are not direct host endpoints. A subaction has no outer-root capability; sublook is a pure query with no action-only calling restriction; submessage supplies internal causal occurrences without host delivery. A `part only` file restricts normal and sub forms alike. Tests retain test-context visibility.

A visible signature, produced value, nested alias/type component or reflective result cannot expose a `part only` declaration. Contract closure cannot lift this restriction. A visible ordinary value projection may be computed using private implementation state without exposing its private type. Ordinary thing fields remain private; imports, specialisation and descriptor widening grant no additional authority.

Contract-visible thing and alias types may be specialised under direct uses authorisation and public type closure. Inherited initialisation keeps the declaring owner's rights. Part dependency cycles are valid with a cyclic-coupling warning; they imply no startup order and do not permit cycles of domain evaluation. Part start contributions are materialised jointly.

Part membership remains an additional visibility dimension, not part of an anchor. Existing thing/action anchors retain their form; new sub declarations use their own sub category. Headers and manifest dependencies introduce no nominal symbols or anchors.

### Type closure and cross-part reflection

A visible contract must be closed with respect to the types needed to understand and use it. The closure includes, where applicable, `for` and `given` types, `on` participants, `look` results, `message` payloads and transitively required types inside aliases, families, magnitudes, collections, dictionaries and exposed products.

A `thing` visible by contract exposes the nominal identity/type needed to bind values, not its ordinary fields. Public state reading is expressed through `look`. A visible `alias`, `family` or `magnitude` exposes the structure needed to represent its values.

Reflection within the part itself may observe the model under the general descriptor system. Across a boundary, a reflective operation is valid only when its contract guarantees that it cannot return invisible entities. Results from `~fields`, `~children`, `~descendants` or similar properties are not silently filtered to simulate security.

Things and aliases may specialize contract-visible types across an authorized part boundary. Inherited contracts remain substitutable; private state and activation permissions are not exported by ancestry. Tooling exposes the generated visible type frontier.

### Part activation

Each part may contribute at most one `start with`. It is not `main`, does not call parts and does not establish an initialisation order. Contributions from all parts are combined and materialised together before initial stabilisation.

A part's `start with` may activate only declarations with a lifecycle in the same part. The mandatory separation between `things` and `rules` sections is removed: the conceptual set contains activatable `thing | rule` declarations, is unordered and deduplicated, and is not interpreted as `for each create`.

One direct contribution and one contribution block are admitted:

```mud
start with Kingdom
```

```mud
start with {
    Kingdom,
    Place,
    CanEnter
}
```

Each expression may contribute zero, one or several activatable declarations. Repeated identities are deduplicated and order has no semantic meaning.

Tests respect the part boundary. In a test context they may call public tests from other parts authorised by `uses` from `then`. Before the root test runs, the static transitive closure of reachable tests is computed and their `start with` contributions are joined; a later call to a test already included does not execute its initial activation again. An executable cycle of calls between tests is invalid.

### Domains, `all` and selection

In addition to contextual literal `all`, `all D` is accepted to materialise the complete canonical enumeration of an enumerable domain `D`. `all` without an operand retains its contextual domain.

`all D` requires valid finite enumeration when the context requires exhaustive materialisation. It also applies to visible reflective domains, for example `all action`, `all rule`, `all look` or `all A.action(B)`. `all thing` enumerates visible `thing` descriptors; `all Thing` retains the domain meaning of the built-in `Thing` type.

Constructs that traverse or quantify a domain without producing a collection may consume it directly. When an operation produces a collection from a domain, materialisation must be explicit through `all D`. This includes selection and `take`, for example `take n from all D`.

Current uses of `in` remain separate: `x in D` locally restricts a value to domain `D`; `a: A in D` is a declarative domain restriction; `x in source : predicate` is selection and produces a collection. Boolean membership is expressed through `D has x` or `D has not x`. No implicit conversion from a filtered collection to `Domain`, nor a predicate-refined domain, is introduced.

### Descriptors, `Any`, `is` and `~type`

Descriptors are first-class values and may form part of `Any`. `Any` is a genuine top type of MUD values, not a textual union of every program type.

`is` may narrow a general value to a compatible descriptor, including nominal types and callable types such as `Dragon.look(Detail)`. `e~type` returns the current static type of `e` at the program point, after narrowing demonstrated by flow analysis. The result is determinable during elaboration and may be used in a type position.

An expression that already denotes a `Type`, such as `Dragon.look(Detail)`, does not need `~type` to become a type.


The callable surface forms fixed by this decision are `A.action(B...)`, `(A, C).action(B...)`, `A.rule(B...)` and `A.look(B...)`: the left side describes receiver/participant types and the parentheses describe the signature's `given` part. `subaction <: action` remains a semantic descriptor relation and does not by itself introduce a type spelling `A.subaction(...)`. Callable compatibility is contravariant for read-only inputs, covariant for outputs and invariant for read/write places, with independent capability obligations.
The reflective relation `subaction <: action <: Declaration` is accepted, but outer-root capability is independent of subtyping. A value widened to `action` cannot cross the outer boundary if any possible runtime alternative remains `subaction`; narrowing may prove that outer capability is safe. Callable substitution does not weaken purity or grant additional caller authority.

### Dynamic invocation of callable values

A stored callable descriptor is invoked using the same receiver form as a nominal declaration, without special `.(op)` syntax:

```mud
op := someAction
then dragon.op(volume)
```

```mud
predicate := someRule
permitted := dragon.predicate(limit)
```

With several participants, `(attacker, defender).op(amount)` may be written. Storing the descriptor does not pre-bind receivers or `given`; invocation performs those bindings at the call site.

Named binding requires an unequivocal static role contract shared by every possible alternative. Positional binding may use an erased compatible contract; named binding requires preserved names or prior static narrowing.

### `look` as a pure callable

`look` is a pure callable query from the host, another part that can see its contract, its own part and pure runtime contexts compatible with state reading. It admits `for` and `given`.

`look`'s `given` parameters follow the general `given` rules. A dynamic domain violation from the host is a query error; inside a resolution, if it invalidates evaluation, it produces `Errors`. `given` parameters must not introduce concerns purely about host transport or presentation.

`look` fields are evaluated over a single coherent read view inherited from the caller. From the host this is the queryable stable state; from a rule it is that rule's snapshot; from a `then` it includes the private delta visible at the call's textual point. A `look` can therefore observe earlier private effects of the same `then` while remaining pure.

Each look/sublook declaration and static generic application induces one produced nominal result type formed from its public fields and exact generic arguments. Different declarations retain distinct result types even when their fields match; calls to the same declaration with the same exact generic arguments share its type, independently of receiver identity or runtime state. A call returns exactly one value of that type; multiplicity is expressed through ordinary fields. The anonymous type receives no anchor merely by existing. It can be obtained with `~type` and used to define an ordinary alias.

A call `MyDragon.Stats()` is a value and cannot directly occupy a type position; `MyDragon.Stats()~type` does denote its static type. By contrast, `Dragon.look(Detail)` is already a callable type.

If a dynamic call may select several `look` declarations with distinct results, the result type must be the most specific common type covering all alternatives. When no more informative common supertype exists that explicitly retains those alternatives, the result is their union. If several incomparable common minima exist, retain the union of the original result alternatives. Literal products use normalized structural identity; := preserves inferred producer identity.

### `message` as a causal occurrence

A `message` is not called to produce a value. It occurs as a consequence of its `when` during causal resolution. Each occurrence retains the declaration, its `on` bindings, the causal view/wave and a technical identity preserving multiplicity. The payload has a static produced nominal type determined by its message declaration, independently of occurrence identity.

The `when` of a reactive rule and that of a `message` share the same trigger language. In addition to temporal triggers, occurrences/firings of compatible visible declarations may be observed: an occurred `message`, a reactive rule that has fired and an `always` rule evaluated for a binding. Actions, subactions, looks, sublooks, Boolean rules and tests are not trigger sources.

Declarations governed by `on` do not admit `given`; when referenced as a trigger they have no `()`. `when Damaged`, `when Dragon.Damaged` or a prior local such as `damage := Dragon.Damaged` followed by `when damage` are valid forms. The receivers of a reference constrain `on` bindings; they do not turn the trigger into an ordinary call.

A reactive rule used as a trigger pulses when it has actually fired. An `always` used as a trigger pulses on every wave in which it is evaluated for the corresponding binding; observing it does not invert its meaning or turn it into a failure trigger. Tooling must warn about the risk of useless causality or lack of stabilisation.

A trigger produces zero or more matches, not necessarily a `Bool`. Each match retains bindings/witnesses and the identity of causal occurrences. `and` performs a natural join of compatible matches, or a Cartesian product when they share no bindings; `or` performs a union. Causally distinct occurrences are not deduplicated merely because they have the same payload, and no implicit inequality exists between bindings.

An occurrence born on wave `n` becomes available as a causal consequence on the next wave; it does not execute consumers immediately by physical order. Stabilisation requires a wave with no effects or pending new consequences/occurrences. A purely causal cycle of messages or firings may prevent stabilisation even when world state does not change.

A message/submessage occurrence is born when its `when` matches and its `if`, if present, is true. Its public fields are evaluated and frozen as one immutable payload in that causal view. The internal and external observations share that payload and occurrence identity. Later field changes, participant destruction or recreation neither reproject the payload nor suppress it by final-state equality. Participants in `on` remain canonical identity descriptors; their later inactivity does not invalidate the event or grant a host mutable world handle.

A shared normal `message` is provisionally delivered after the producing wave is consolidated and its mandatory always/domain/cardinality checkpoints succeed. No sibling private prefix or failed checkpoint is published. Internal causal consumers still see the occurrence in the next wave. A `submessage`, a declaration in a `part only` file, an isolated test or `imagine` has no external delivery. A root-produced occurrence passes the analogous root consolidation/checkpoint barrier. Publication does not confirm tentative world state, and host `look` continues to read confirmed state.

The host envelope keeps declaration/occurrence identity, `on` bindings, immutable payload and `ticket` separate. A `Ticket` is a read-only host-facing occurrence handle whose `state` is `Waiting`, `Kept` or `Dropped`. It is not a Mud thing, a writable participant, a new keyword or a user-constructible source type. It has no new nominal anchor. Its occurrence identity is distinct even when another message has the same payload. Concrete ABI and native representation follow the adapter contracts.

Every published ticket starts Waiting. It transitions once to Kept when the real outer resolution commits and its producing rollback scope survives, or to Dropped when that scope or an enclosing scope is discarded. Both terminal states are permanent. Successful child completion leaves Waiting until outer confirmation. Later caller changes do not recheck the child's after or invalidate historical payload values. A child's refusal/error drops its attempted occurrences and causal descendants. Outer refusal/error drops all surviving pending tickets. For jointly caused work the owner is the nearest common enclosing invocation; an entire physical wave does not acquire a single owner.

Block rollback is part of ticket provenance. A failed protected block drops its occurrences even if `otherwise` recovers and the outer action succeeds. Handler occurrences belong to their new surviving scope and get new tickets. An occurrence discarded before its publication barrier emits no provisional host notification. Payload-evaluation errors enter the ordinary error channel; they do not create a successfully published occurrence with a partially calculated payload.

The host can read current ticket state and subscribe to terminal updates. Subscription registration and its initial current-state observation must be serialised with state transitions so that a host cannot miss completion between reading Waiting and registering. Local observation and remote occurrence-identity notifications obey this same contract; transport replay/reconnection protocols are adapter details. The host cannot set ticket state or cancel a Mud resolution through this handle. Kept is observable only after the confirmed state is available.

Waiting permits speculative host responses with cancellation/compensation; irreversible external effects require Kept or an explicit transactional adapter contract. Dropped does not undo arbitrary I/O, sound or already displayed frames. Ticket observation is not permission to read tentative storage. Published frozen payloads and terminal ticket state remain readable as historical evidence after rollback; private writable handles and failed foreign exports do not escape.

Publication preserves causal order across wave barriers. A reproducible technical order within a wave does not give semantic priority to equal-time occurrences. Tickets report validity of the recorded causal occurrence, not whether its payload still equals current state. Unbounded resolution duration or nontermination may leave Waiting pending; timeout/oscillation policy is separate from inventing Kept or Dropped.

### Locals preceding### Locals preceding behaviour clauses

A `action`, reactive rule or `message` may declare pure locals using `:=` between metadata and its main clauses. They are immutable and sequential, visible to later locals and clauses, and follow the ordinary rules against forward references, cycles and shadowing.

A local may name a trigger before `when`; it does not select a concrete occurrence until `when` produces a match. Payload fields are accessible only where flow analysis guarantees that the binding exists.

### Operation-centred host boundary

The canonical host API is organised around the identity of public operations, not around a participant chosen as owner. The production boundary comprises `action`, `look` and `message`. Tests may be public between parts in a test context, but are not thereby part of the external production API.

## Additional constraints

- There are no per-declaration visibility modifiers; part only restricts an entire file.
- Cross-part reflection must be contract-safe; results are not silently censored.
- Cross-part thing/alias specialization requires contract visibility and uses authorization, preserving encapsulation.
- An internal action/subaction call never opens a new root resolution.
- A `look` remains pure even when it reads the caller's visible private delta.
- A `message` is not emitted through `emit` or modelled as a `Bool` value.
- `message` occurrences do not become `on` participants; causality belongs to `when`.
- Actions, subactions, looks, sublooks, Boolean rules and tests are not declarative trigger sources.
- Selection producing a collection from a domain must use a source explicitly materialised with `all D`.

Generic produced-type identity is extended by [[ADR-134-static-generic-declarations-and-applications|D-134]]; host-boundary and activation contracts remain unchanged.
