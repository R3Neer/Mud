---
id: D-042
title: "Shares, root and results"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-002"
  - "Q-003"
  - "Q-004"
  - "Q-022"
  - "Q-023"
  - "Q-046"
  - "Q-059"
affects:
  - "frontera pública, efectos, solicitud de acciones, semántica de la raíz"
---
# ADR-042 — Shares, root and results

- Amended by: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Related to: [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]]
- Amended by: [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]], [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Further amended by: [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]] y [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]]
- Related questions: Q-002, Q-003, Q-004, Q-022, Q-023, Q-046, Q-059
- Documents concerned: public boundary, effects, request shares, semantics of the root

## Context

One action is the MUD’s writing boundary. Its contract one must distinguish between expected inadmissibility and that of a request the errors that prevent one from obtaining a state valid.

## Decisión

```mud
action Recruit for kingdom: Kingdom [mut]
given
    amount: Nat in 1..100
{
    if kingdom.treasury >= amount * kingdom.recruitmentCost
    otherwise "The kingdom cannot afford {amount} recruits"
    then {
        kingdom.treasury -= amount * kingdom.recruitmentCost
        kingdom.soldiers += amount
    }
    after kingdom.soldiers >= old kingdom.soldiers
    otherwise "Recruitment did not increase the army"
}
```

One action:

- declares participants via `for`;
- can declare values `given` and its domains;
- may state `if` y `after`;
- must state `then`;
- does not state `when` nor does it activate automatically;
- one `action` It can be applied for from abroad and, in that case, the causal resolution root;
- one `action` o `subaction` invoked from a `then` joins the causal resolution is already active and does not open a root independent;
- the resolution It is atomic in its entirety, together with all its waves.

The participants are recipients and the `given` these are arguments in accordance with D-036 y D-063. When starting the action the roles are linked by identity, value or place, depending on its contract, their types, cardinalities and capacities are checked, and the `given` If they are omitted and their static defaults are used, they are all evaluated and validated, and then the following is evaluated `if`. A role with `mut` The exterior retains its original appearance receiver as the destination for effects and requires it to be storable and externally mutable. A `given` outside domain or a `if` False ones have no effect.

Within a block `then`, D-066 allows for calculated local links. They are resolved in textual order, reading the delta previous private provision, remain unchanged and do not form part of the state from the world.

### Unified sequence of `then`

There is no classification semantics between elementary and compound actions. A `then` is an ordered sequence of consequences and may combine local links, direct effects and calls to `action` o `subaction` and routes `for each`.

Each sentence reads: delta private, visible in its textual position. A call The internal function is validated and executed in that point, takes into account the previous private effects and adds its own effects to them resolution It has atomicity and preserves these effects for subsequent statements. It does not open a separate transaction.

The `after` of all the shares/subactions The executed commands are checked against the stable state final attempt at the resolution complete. Call analysis must prevent executable cycles; Q-023 The proof of acyclicity and impact remains open when the selection of the descriptor 'callable' is a dynamic property, not the ability to call it.

### `after` y `old`

`if` y `after` can be attached via `otherwise` one reason `Text` because it is false. Its omission is lawful and implies a suggestion, not a warning, because rejection is a normal response; in that case, this results in a reason based on the condition and its provenance. The diagnostic He is pure and lazy.

`after` is evaluated after all the waves on the stable state attempt. Its falsity results in `rejected`; a error during its assessment, it produces `failed`. A error when assessing `if` o `after` is not captured by `otherwise`, which only accounts for a condition that has been correctly evaluated as false.

In the context of actions and tests, `old e` read `e` in the stable state immediately prior to the action complete exterior and is only permitted within `after`. D-058 adds a different context for `old` within reactive rules, where it compares snapshots of wave.

### Results

| Result | Reason |
| --- | --- |
| `accepted` | Request valid, root compatible, stabilisation, invariants and `after` satisfied |
| `rejected` | `given` outside domain, `if` false or `after` false |
| `failed` | Conflict, cycle u oscillation, invalid operation, domain or invalid references, `always` unfulfilled or failure propagated semantic |

The request returns to the external caller an object whose field `state` contains one of those three results. When it contains `rejected` o `failed`, the item also includes a field compulsory `reason: Text` with the explanation human. Any regulatory case other than `accepted` must provide that reason in accordance with D-061; it may be accompanied by codes and structured reasons.

Everything result other than `accepted` restores exactly the stable state previous and does not publish messages or have any other external effects.

The normalisation of a linear interval with inverted endpoints to `empty` is a valid assessment in accordance with D-059 and does not produce `failed` in its own right. A `given` to be excluded from domain or a `if` o `after` which turns out to be false because of that gap, result in `rejected`; a domain that leaves a value invalid storage or a rule `always` unfulfilled lead to `failed` by the tentative state resulting.

## Consequences

- `rejected` is an answer semantics normal; `failed` indicates that a transition valid.
- Atomicity includes root, waves, `always`, `after` and upcoming events.
- Q-004 is now closed: one `after` 'false' reverses the entire resolution.
- The values of domain returned by a action, if they were to be admitted, they remain open in Q-022.

## Verification

1. Acceptance, rejection of domain from `given`, rejection due to `if` and rejection of `after`.
2. Full rollback of a action rejected in the end.
3. `then` a mixture of effects, local elements and calls in textual order.
4. Spread of the delta private via internal calls and the rejection of a executable cycle calls.
5. `old` note the action outer layer, not an intermediate layer.
6. Linking a receiver-a changeable place and the rejection of a receiver let it just be a value.
7. Normalised inverse interval to `empty` without failure intrinsic.
8. Distinguishing between rejection on the grounds of a false custody order regarding `empty` y failure by state outside domain.
9. Compulsory attendance by `reason: Text` in `rejected` y `failed`, and absence from `accepted`.
10. Diagnostics `otherwise` explicit and generated for `if` y `after`, including lazy evaluation.

## Amendment current by D-096

The classification is withdrawn semantics between action elementary and compound. All `then` is an ordered sequence that can combine effects, locations, calls and `for each`. A call Internal observes the delta deprived of the point verbatim and contributes to its effects resolution. `action` retains the ability to root outdoor; `subaction` can be reused from any `then` but that can’t be right root exterior. The `after` Nested ones are evaluated against the stable state final attempt at the resolution complete.

