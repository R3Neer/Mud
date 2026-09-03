---
id: D-021
title: "Cycle logical lifespan and suspension by department"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-048"
  - "Q-049"
affects:
  - "[[especificacion/04-modelo-matematico]], futuros capítulos 11, 21 a 25 y 32"
---
# ADR-021 — Cycle logical lifespan and suspension by department

- Updated: 28 July 2026 to use the terminology of D-025
- Related to: [[notas/decisiones/ADR-031-aliases-nominales-e-inmutables|D-031]], [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]]
- Amended by: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- As further amended by: [[ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]]
- As further amended by: [[ADR-099-materializaciones-frescas-tras-destroy-create|D-099]]
- Example updated by: [[ADR-079-diagnostico-exterior-de-reglas-always|D-079]]
- Questions affected: [[notas/preguntas/Q-048-destruccion-con-descendientes-activos|Q-048]], [[notas/preguntas/Q-049-destruccion-y-colecciones-de-thing|Q-049]]
- Documents concerned: [[especificacion/04-modelo-matematico]], future chapters 11, 21 to 25 and 32

## Context

The cycle In life, one must distinguish between two phenomena that are reversible for different reasons:

- Explicitly destroy a `thing` or a rule withdraws its activation and ends the materialisation or the runtime memory associated with it.
- Make another one declaration It ceases to be interpretable because one of its dependencies is inactive; this merely suspends it; that suspension does not destroy the state which belongs to the declaration dependent.

The canonical definition and the identity of a declaration survive `destroy`. Therefore, if `King.kingdom` contains `Panama` and the type `Kingdom`, the ownership of `King` it can retain its charge in a latent state whilst the type is not effective. On the other hand, if the `Kingdom` If a particular one had its own runtime payload or structural modifications, these belonged to the materialisation destroyed and do not reappear when you recreate them.

This separation prevents both the destructive pruning of state foreign as an interpretation of `destroy` as a mere hibernation of the materialisation its own.

## Decisión

The model distinguishes:

1. A catalogue of **canonical definitions** of the programme, which preserves identities, descriptors and edges `as` static.
2. The state the runtime of materialisations and active declarations, together with the stored information on declarations that may simply be suspended due to dependencies.
3. A projection **effective**, which contains only the pieces currently in play.

Be $\mathcal D_P$ the set of statements recognised by the programme, and that it is $\mathcal L_P\subseteq\mathcal D_P$ the subset with cycle explicit way of life. A state $W$ maintains, as a minimum, information on activation:

$$
\operatorname{active}_W:
\mathcal L_P\to\mathbb B
$$

and the state runtime of the currently existing materialisations or memories. The effective projection:

$$
\operatorname{Effective}(W)
$$

is derived from those components and the dependencies between declarations.

`destroy d` change the activation from $d$ without altering its canonical definition:

$$
\operatorname{active}_{W'}(d)=\bot
$$

When $d$ is a `thing` Specifically, confirmed destruction also brings an end to its materialisation current runtime. The stored values specific to that materialisation and runtime structural modifications whose owner be $d$. When $d$ is a rule, the runtime memory associated with that is discarded activation in accordance with D-099.

`create d` re-enable the same one identity declarative. For a `thing` specifically that it no longer owns materialisation active, create a materialisation fresh from the canonical definition: reconstructs its declared structure and reapplies defaults and initialisers. It does not restore the load or the structural modifications specific to the materialisation destroyed.

One `thing` abstracta does not have its own specific payload to reset; its cycle The building’s lifespan depends on appropriate maintenance and structural restoration. For rules, a activation The posterior region reconstructs temporal memory in accordance with D-099 and does not retrieve the memory of the activation destroyed.

The initiators of a `thing` Specific rules are applied whenever it needs to be recreated from its canonical definition, whether in the materialisation initially or following a `destroy` confirmed followed by `create`.

The conservation of canonical identity does not involve the preservation of materialisation its own.

## Categories with cycle of life

`create` y `destroy` can trade in:

- `thing` specific.
- `thing` abstract.
- Boolean rules.
- Reactive rules.
- Rules `always`.

They do not operate on:

- Aliases.
- Shares.
- Quantities.

The actions form the stable writing API. The quantities form part of the static dimensional system.

## Surface syntax

In accordance with D-054, all `thing` and the rule has only one canonical definition top-class:

```mud
thing Kingdom {}

abstract thing Place {}

rule CanEnter for person: Person {
    ...
}

rule OpenGate on gate: Gate [mut] {
    ...
}

always rule ValidKingdom on kingdom: Kingdom {
    kingdom.population >= 0
}
otherwise "Invalid population in {kingdom}"
```

Runtime activations omit the category and body:

```mud
create CanEnter
create OpenGate
create ValidKingdom
```

This form triggers a `thing` and, where appropriate, creates its new materialisation:

```mud
create Kingdom
create Place
```

The statements at the beginning are provided by means of the `start with` unified D-096:

```mud
start with {
    Kingdom,
    Place,
    CanEnter
}
```

Contributions may include statements that trigger action `thing | rule`; they are deduplicated and their order is not semantic.

`destroy` It just needs a reference that resolves unambiguously:

```mud
destroy Kingdom
destroy CanEnter
```

Declaration names share the space required for that resolution be unambiguous. An ambiguous reference must be identified; `destroy` It does not select a category based on priority.

The compiler can internally generate these forms as canonical definition, initial activation, materialisation runtime and deactivation. `activate` y `deactivate` are not entered as words in the MUD surface.

## Suspension by department

One declaration it may not be effective even though its own explicit brand remains active. For example:

$$
\operatorname{HardDep}_P(d)
$$

the set of dependencies the absence of which prevents the use of $d$. In brief:

$$
\operatorname{effective}_W(d)
\iff
\operatorname{active}_W(d)
\land
\forall e\in\operatorname{HardDep}_P(d).
\operatorname{effective}_W(e)
$$

For a stored property $p$, these are hard dependencies:

- His owner.
- His type stated.
- The statements required to interpret its domain and shape.

Therefore, if:

```mud
thing King {
    kingdom: Kingdom[1] = Panama
}
```

and is executed:

```mud
destroy Kingdom
```

the property `King.kingdom` ceases to belong to $\operatorname{Effective}(W)$, but it remains stored alongside `Panama` because that load belongs to `King`, not to the materialisation destroyed from `Kingdom`. When creating a new one `Kingdom`, the title may once again take effect subject to the same encumbrance, provided that the transition is complete and valid.

The structure of a `thing` destroyed, it disappears from the effective projection. His canonical definition remains in the programme, but the loading and runtime modifications specific to the materialisation Once destroyed, they are not stored for future reactivation. A new materialisation part of the canonical definition.

## Participants and dependent declarations

If the type of a participant When it ceases to be effective, it is not just that parameter that is removed from the signature. The declaration which requires a full signature:

- One reactive rule It does not produce bindings.
- A ruler `always` does not temporarily impose its invariant.
- One Boolean rule It is considered inactive for assessment purposes.
- One action The dependent temporarily ceases to be targetable, even though the cards cannot be destroyed directly.

This suspension retains arity, role names and internal references. Recreating the dependency restores the declaration without rewriting it.

## Specialisation and descendants

Edges declared using `as` remain in the canonical definition of the programme. In the effective projection, an active descendant is not necessarily suspended simply because one of its predecessors has been destroyed.

When a path is declared:

$$
c = n_0,\ldots,n_k = p
$$

has active endpoints and all its internal nodes are inactive; the effective projection can connect $c$ with the most recent active predecessor $p$. There is no intermediate ancestor that remains active.

Thus, by destroying `Kingdom`:

```text
Thing
└── Kingdom
    └── Panama
```

the effective projection It could be:

```text
Thing
└── Panama
```

The properties declared by `Kingdom` are no longer inherited whilst it is destroyed. The properties inherent in `Panama` remain in force if their provisions remain in force. Upon re-establishment `Kingdom`, the edges and properties derived from its canonical definition; runtime structural modifications belonging to the materialisation destroyed from `Kingdom`.

The specialisation unit declared with `as` it can be crossed at the effective projection and not just one hard dependency which will cause a chain reaction that destroys all the descendants.

## `add` y `remove` about properties

`add` y `remove` They also operate on properties. The word `property` is not necessary:

```mud
add kingdom: Kingdom[1] = Panama to King
remove kingdom from King
```

The colon indicates the addition of a declaration resulting from the addition of a member:

```mud
add Panama to King.kingdoms
remove Panama from King.kingdoms
```

`remove kingdom from King` Removes the property and its stored data. Re-adding a property with the same name does not automatically restore it `Panama`.

Therefore:

$$
\operatorname{remove}(p)
\implies
p\notin\operatorname{Stored}(W')
$$

whereas destroying one hard dependency It does not transfer ownership, but merely suspends it:

$$
\operatorname{destroy}(T)
\land
T\in\operatorname{HardDep}_P(p)
\land
\operatorname{owner}(p)\ne T
\implies
\begin{cases}
p\in\operatorname{Stored}(W')\\
p\notin\operatorname{Effective}(W')
\end{cases}
$$

This preservation does not apply to fields or structural modifications whose load belongs to the materialisation a specific one destroyed.

## Absence of implicit captures

One declaration introduced by `create` does not capture free variables from the `then`, action or a binding that performs the creation.

You may declare and use:

- Its own participants `on` o `for`.
- Their own values `given` when their rule class permits it.
- Resolvable global names and anchors.

It cannot implicitly retain a participant not even a `given` belonging to the creative context. If a law needs to refer to a piece of data, that data must be explicitly represented in the state from the world.

This rule prevents the same identity The global variable should have different closures depending on which binding activates it.

## Options ruled out

### Indiscriminate, destructive pruning

The option to automatically remove all members of collections in the same way is ruled out. D-077 adopts a conditional withdrawal: it must retain the cardinality Ultimately, unchanging relationships retain a latent sense of belonging, and relationships `mut` they delete the stored membership.

### Hibernation of the materialisation own

The option of retaining the payload and runtime structural modifications associated with a `thing` specifically after `destroy`. D-099 requires that a `create` subsequently build a materialisation fresh from the source canonical identity.

### Destructive waterfall

Automatic deletion of descendants and dependants is not permitted. The suspension derivative is sufficient to remove them from the projection when necessary and preserves the reversibility of the state which belongs to them.

### `activate` y `deactivate` on the surface

They are retained as potential internal terminology for aspects of the activity, but are excluded from the main terminology. `create`, `destroy`, `add` y `remove` describe the rules of a world.

### Catches subject to the uniqueness condition

These are ruled out. They would require defining when uniqueness is demonstrated, what happens if it changes, and how to resolve two different loads for the same identity.

## Issues still to be resolved

- Permitted transactions involving suspended properties.
- Serialisation and introspection of the stored representation and runtime instantiations.

## Future verification

The suite must cover:

1. Disposal of the own stored data of a `thing` the destruction of a specific instance and its rematerialisation based on predetermined settings and initialisers when recreating it.
2. Maintenance of another person’s property and the liability arising from its destruction hard dependency as his type stated.
3. Restoration of that property, subject to the same encumbrance, when the dependency arises again and the transition is valid.
4. Pressure drop downstream of `remove`.
5. Suspension a comprehensive list of rules and actions involving participants from type inactive.
6. Rejection of `create` y `destroy` applied to a alias, in accordance with D-031.
7. Compression and restoration of the graph cash.
8. Retention of property rights by descendants where their tenancies remain in force.
9. No implicit captures.
10. Resolution unequivocal indication of `destroy`.
11. Rejection of `create` o `destroy` on actions and quantities.

