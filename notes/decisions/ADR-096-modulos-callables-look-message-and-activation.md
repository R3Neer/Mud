---
id: D-096
title: "Modules, callables, `look`, `message` and activation"
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
  - "modules, visibility and reflection"
  - "actions, subactions and `then`"
  - "`look`, `message` and triggers"
  - "domains, `all` and selection"
  - "initial activation and tests"
  - "grammar, CST, AST, IR, typing, resolution and host boundary"
---

# ADR-096 — Modules, callables, `look`, `message` and activation

- Modified by: [[ADR-101-bloques-de-valor-variables-locales-almacenadas-and-extremos-por-testigos|D-101]].

- Supersedes: [[ADR-027-departures-from-the-model-by-means-of-look-and-message|D-027]].
- Modifies: [[ADR-036-participants-recipients-and-calls|D-036]], [[ADR-041-contracts-under-the-three-types-of-rules|D-041]], [[ADR-042-shares-root-and-results|D-042]], [[ADR-045-causal-resolution-connections-and-queue|D-045]], [[ADR-058-temporal-triggers-changes-and-reactive-old|D-058]], [[ADR-063-signatures-given-and-joint-on-bindings|D-063]], [[ADR-075-enumerable-domains-all-and-derived-value-form|D-075]], [[ADR-081-filtering-take-and-indexing-de-collectiones|D-081]], [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]], [[ADR-087-metadatos-reflectivos-descriptores-estables-and-visibilidad-exterior|D-087]] and [[ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]].
- Associated open questions: Q-062 to Q-068.

- Modified by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].

## Context

MUD's evolution had left several artificially separate boundaries: elementary versus compound actions, `look` as an essentially external query, `message` as output deferred to the host, separate activation in `things` and `rules`, and implicit domain consumption in operations producing collections. These separations interact poorly when the language is organised into modules, permits callable values and uses wave-based causal resolution.

This decision unifies these pieces without closing the still-open questions of callable typing, anonymous-type identity or the complete `mud.module` grammar.

## Decision

### A single `then` model

The semantic separation between elementary and compound actions is removed. A `then` is an ordered sequence of consequences and may mix calculated locals, immutable or `mut` stored locals, direct effects, calls to `action` or `subaction`, and `for each` traversals. Shared locals written before behaviour clauses remain exclusively pure calculated `:=` bindings.

An internal call executes at its textual position within the resolution's private delta: it observes earlier effects visible at that point, contributes its effects to the same resolution, and later statements observe those effects. It does not open an independent transaction.

The `after` clauses of all actions/subactions executed during resolution are checked against the complete resolution's tentative final stable state. An ordered `for each` retains sequential semantics between iterations; in an unordered one, sibling-iteration deltas are consolidated under the ordinary concurrency rules.

An `action` or `subaction` may be invoked from any semantic `then` context, including a reactive rule's `then`. `action` also retains outer-root capability; `subaction` does not. A nested `failed` propagates and reverts the entire resolution. An internal `rejected` also aborts and reverts, while retaining the `rejected` category.

### Modules and visibility

Visibility derives from the semantic category, owning module, inter-module contracts and the type closure required by those contracts.

A module is a semantic encapsulation unit. Between modules, the visible operational boundary consists of `action`, `look`, `message` and, only in a test context, `test`. The application boundary towards the host includes `action`, `look` and `message`, not `test`.

Internal implementation declarations do not become visible by default. A module may use its own operations with the same semantic capabilities it grants to other modules in the relevant context.

Module membership is not part of the nominal anchor. Anchors such as `thing::infrastructure.economy.Bank` or `action::infrastructure.economy.Transfer` retain their form; the module is an additional dimension of visibility and dependency.

The physical root of a module is marked by a visible `mud.module` file. Each `.mud` belongs to the module of the nearest ancestor `mud.module`; a `.mud` without a modular ancestor is invalid, and a nested `mud.module` opens a new boundary. The module's logical name derives from the directory's MudPath.

`mud.module` declares external dependencies through `uses`. `uses` authorises a module to know another module's contract; `using` retains its name-resolution/import role inside a `.mud` and does not by itself grant modular permission. Modular dependencies may form cycles: the compiler must warn about cyclic coupling, not invent an initialisation order.

The complete grammar of the `mud.module` file remains open in Q-062; this decision fixes its semantic role, physical name and the responsibility of `uses`, but introduces no additional surface.

### Type closure and cross-module reflection

A visible contract must be closed with respect to the types needed to understand and use it. The closure includes, where applicable, `for` and `given` types, `on` participants, `look` results, `message` payloads and transitively required types inside aliases, families, magnitudes, collections, dictionaries and exposed products.

A `thing` visible by contract exposes the nominal identity/type needed to bind values, not its ordinary fields. Public state reading is expressed through `look`. A visible `alias`, `family` or `magnitude` exposes the structure needed to represent its values.

Reflection within the module itself may observe the model under the general descriptor system. Across a boundary, a reflective operation is valid only when its contract guarantees that it cannot return invisible entities. Results from `~fields`, `~children`, `~descendants` or similar properties are not silently filtered to simulate security.

`thing` specialisation/inheritance cannot cross a module boundary.

### Module activation

Each module may contribute at most one `start with`. It is not `main`, does not call modules and does not establish an initialisation order. Contributions from all modules are combined and materialised together before initial stabilisation.

A module's `start with` may activate only declarations with a lifecycle in the same module. The mandatory separation between `things` and `rules` sections is removed: the conceptual set contains activatable `thing | rule` declarations, is unordered and deduplicated, and is not interpreted as `for each create`.

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

Tests respect the module boundary. In a test context they may call public tests from other modules authorised by `uses` from `then`. Before the root test runs, the static transitive closure of reachable tests is computed and their `start with` contributions are joined; a later call to a test already included does not execute its initial activation again. An executable cycle of calls between tests is invalid.

### Domains, `all` and selection

In addition to contextual literal `all`, `all D` is accepted to materialise the complete canonical enumeration of an enumerable domain `D`. `all` without an operand retains its contextual domain.

`all D` requires valid finite enumeration when the context requires exhaustive materialisation. It also applies to visible reflective domains, for example `all action`, `all rule`, `all look` or `all A.action(B)`. `all thing` enumerates visible `thing` descriptors; `all Thing` retains the domain meaning of the built-in `Thing` type.

Constructs that traverse or quantify a domain without producing a collection may consume it directly. When an operation produces a collection from a domain, materialisation must be explicit through `all D`. This includes selection and `take`, for example `take n from all D`.

Current uses of `in` remain separate: `x in D` locally restricts a value to domain `D`; `a: A in D` is a declarative domain restriction; `x in source : predicate` is selection and produces a collection. Boolean membership is expressed through `D has x` or `D has not x`. No implicit conversion from a filtered collection to `Domain`, nor a predicate-refined domain, is introduced.

### Descriptors, `Any`, `is` and `~type`

Descriptors are first-class values and may form part of `Any`. `Any` is a genuine top type of MUD values, not a textual union of every program type.

`is` may narrow a general value to a compatible descriptor, including nominal types and callable types such as `Dragon.look(Detail)`. `e~type` returns the current static type of `e` at the program point, after narrowing demonstrated by flow analysis. The result is determinable during elaboration and may be used in a type position.

An expression that already denotes a `Type`, such as `Dragon.look(Detail)`, does not need `~type` to become a type.


The callable surface forms fixed by this decision are `A.action(B...)`, `(A, C).action(B...)`, `A.rule(B...)` and `A.look(B...)`: the left side describes receiver/participant types and the parentheses describe the signature's `given` part. `subaction <: action` remains a semantic descriptor relation and does not by itself introduce a type spelling `A.subaction(...)`. Q-063 keeps variance and formal compatibility between callable types open.
The reflective relation `subaction <: action <: Declaration` is accepted, but outer-root capability is independent of subtyping. A value widened to `action` cannot cross the outer boundary if any possible runtime alternative remains `subaction`; narrowing may prove that outer capability is safe. Callable variance and formal compatibility remain open in Q-063.

### Dynamic invocation of callable values

A stored callable descriptor is invoked using the same receiver form as a nominal declaration, without special `.(op)` syntax:

```mud
op := someAction
then dragon.op(volume)
```

```mud
predicate := someRule
allowed := dragon.predicate(limit)
```

With several participants, `(attacker, defender).op(amount)` may be written. Storing the descriptor does not pre-bind receivers or `given`; invocation performs those bindings at the call site.

The exact rule for nominal binding when invoking a sufficiently erased descriptor remains open in Q-066.

### `look` as a pure callable

`look` is a pure callable query from the host, another module that can see its contract, its own module and pure runtime contexts compatible with state reading. It admits `for` and `given`.

`look`'s `given` parameters follow the general `given` rules. A dynamic domain violation from the host is a query error; inside a resolution, if it invalidates evaluation, it produces `failed`. `given` parameters must not introduce concerns purely about host transport or presentation.

`look` fields are evaluated over a single coherent read view inherited from the caller. From the host this is the queryable stable state; from a rule it is that rule's snapshot; from a `then` it includes the private delta visible at the call's textual point. A `look` can therefore observe earlier private effects of the same `then` while remaining pure.

Each `look` induces an anonymous result object formed from its public fields. A call returns exactly one value of that type; multiplicity is expressed through ordinary fields. The anonymous type receives no anchor merely by existing. It can be obtained with `~type` and used to define an ordinary alias.

A call `MyDragon.Stats()` is a value and cannot directly occupy a type position; `MyDragon.Stats()~type` does denote its static type. By contrast, `Dragon.look(Detail)` is already a callable type.

If a dynamic call may select several `look` declarations with distinct results, the result type must be the most specific common type covering all alternatives. When no more informative common supertype exists that explicitly retains those alternatives, the result is their union. The formal choice when several incomparable common minima exist remains open in Q-065; anonymous-type identity/equality remains open in Q-068.

### `message` as a causal occurrence

A `message` is not called to produce a value. It occurs as a consequence of its `when` during causal resolution. Each occurrence retains the declaration, its `on` bindings, the causal view/wave and a technical identity preserving multiplicity. The payload is an anonymous type formed from the public fields.

The `when` of a reactive rule and that of a `message` share the same trigger language. In addition to temporal triggers, occurrences/firings of compatible visible declarations may be observed: an occurred `message`, a reactive rule that has fired and an `always` rule evaluated for a binding. Actions, subactions, looks, Boolean rules and tests are not trigger sources.

Declarations governed by `on` do not admit `given`; when referenced as a trigger they have no `()`. `when Damaged`, `when Dragon.Damaged` or a prior local such as `damage := Dragon.Damaged` followed by `when damage` are valid forms. The receivers of a reference constrain `on` bindings; they do not turn the trigger into an ordinary call.

A reactive rule used as a trigger pulses when it has actually fired. An `always` used as a trigger pulses on every wave in which it is evaluated for the corresponding binding; observing it does not invert its meaning or turn it into a failure trigger. Tooling must warn about the risk of useless causality or lack of stabilisation.

A trigger produces zero or more matches, not necessarily a `Bool`. Each match retains bindings/witnesses and the identity of causal occurrences. `and` performs a natural join of compatible matches, or a Cartesian product when they share no bindings; `or` performs a union. Causally distinct occurrences are not deduplicated merely because they have the same payload, and no implicit inequality exists between bindings.

An occurrence born on wave `n` becomes available as a causal consequence on the next wave; it does not execute consumers immediately by physical order. Stabilisation requires a wave with no effects or pending new consequences/occurrences. A purely causal cycle of messages or firings may prevent stabilisation even when world state does not change.

The `when` and `if` of a `message` are resolved in the causal view producing the occurrence. If `if` is false, the occurrence is not born. Within MUD, the observed payload is projected onto the occurrence's causal view. Towards the host, if resolution confirms, it is projected onto the final stable state. Both projections belong to the same occurrence; if resolution reverts, there is no external delivery.

External treatment of participants that cease to exist before the final state remains open in Q-067.


The external wrapper of a confirmed occurrence keeps `on` bindings and the public payload separate; they are not flattened into one object where participant names compete with payload names. Delivery preserves causal order between waves. Within one wave, a stable reproducible technical order is used without attributing semantic priority between occurrences to that order.
### Locals preceding behaviour clauses

A `action`, reactive rule or `message` may declare pure locals using `:=` between metadata and its main clauses. They are immutable and sequential, visible to later locals and clauses, and follow the ordinary rules against forward references, cycles and shadowing.

A local may name a trigger before `when`; it does not select a concrete occurrence until `when` produces a match. Payload fields are accessible only where flow analysis guarantees that the binding exists.

### Operation-centred host boundary

The canonical host API is organised around the identity of public operations, not around a participant chosen as owner. The production boundary comprises `action`, `look` and `message`. Tests may be public between modules in a test context, but are not thereby part of the external production API.

## Additional constraints

- The module boundary is not controlled through explicit visibility modifiers.
- Cross-module reflection must be contract-safe; results are not silently censored.
- A `thing` cannot specialise a `thing` from another module.
- An internal action/subaction call never opens a new root resolution.
- A `look` remains pure even when it reads the caller's visible private delta.
- A `message` is not emitted through `emit` or modelled as a `Bool` value.
- `message` occurrences do not become `on` participants; causality belongs to `when`.
- Actions, subactions, looks, Boolean rules and tests are not declarative trigger sources.
- Selection producing a collection from a domain must use a source explicitly materialised with `all D`.

## Open questions

- Q-062: complete `mud.module` grammar.
- Q-063: formal compatibility and variance of callable types.
- Q-064: aliases and nominal specialisation across modules.
- Q-065: joining `look` result types with multiple common minima.
- Q-066: nominal binding when invoking an erased descriptor.
- Q-067: `message` participants absent from the final state.
- Q-068: structural identity and equality of anonymous types.

These questions do not authorise silently choosing a variant during implementation.
