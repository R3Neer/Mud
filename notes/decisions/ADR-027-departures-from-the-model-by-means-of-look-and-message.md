---
id: D-027
title: "Departures from the model by means of `look` and `message`"
status: superseded
date: 2026-07-27
supersedes: []
superseded-by:
  - "D-096"
questions:
  - "Q-051"
  - "Q-052"
affects:
  - "future `22-looks-and-messages.md`, future `42-public-api.md`"
---
# ADR-027 — Departures from the model by means of `look` and `message`

- Amended by: [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]]
- Subsequently amended by: [[notes/decisions/ADR-083-unitless-base-quantities|D-083]]
- Open questions: Q-051, Q-052
- Documents affected: future `22-looks-and-messages.md`, future `42-public-api.md`

## Context

Actions allow requests to be submitted to a MUD model, but the model lacked a symmetrical, typed surface for extracting information. Reading directly from storage or implementation artefacts would break the separation between semantics and materialisation.

MUD includes two output entities:

- `look`, to observe the stable state currently available on demand.
- `message`, to report that an incident took place during the resolution of a action.

## Decision

### `look`

A `look` declares explicit participants with `for`, does not support `given` and publishes calculated properties:

```mud
look RealmSummary for kingdom: Kingdom {
    name := kingdom.name
    population: Nat := kingdom.cities.population.sum
}
```

Conceptual form:

```text
look name for participants {
    public-property [ : type ] := expression
    ...
}
```

Each expression may be a property reading or any well-typed pure expression, including those equivalent to derived properties. A `look` does not alter the world. Its fields are evaluated over a single stable state.

### `message`

A `message` declares automatic links with `on`, a condition `when`, a guard `if` Optional and calculated public properties:

```mud
message KingChanged on kingdom: Kingdom {
    when kingdom.king changes
    if kingdom.visible

    kingdomName := kingdom.name
    kingName: Text := kingdom.king.name
}
```

Conceptual form:

```text
message name on participants {
    when boolean-expression
    [if boolean-expression]
    public-property [ : type ] := expression
    ...
}
```

The detection of the message forms part of the sequence of waves caused by a action. Its public properties are not calculated using the values at the time of detection. They are evaluated over the stable state the target achieved upon completion of the entire sequence of waves of that action.

This separation requires the runtime to maintain a occurrence pending the necessary links between participants, and the assessment of public statements is deferred.

### Border semantics

`action`, `look` and `message` form the explicit boundary of the model:

- `action`: a post that could change the world.
- `look`: extract taken from the stable state.
- `message`: a temporary departure caused by a change.

None of these organisations authorises the examination of details relating to architecture, frameworks, databases or materialisation.

## Initial static rules

- The names of public properties are unique within their entity.
- All public property has a type static, either declared explicitly or inferred from its expression.
- The assigned expression must be pure. If the type If it is declared, it must be compatible with it; if it is omitted, its type it must be possible to infer it unambiguously.
- A `look` does not support `on`, `given`, `when`, `if`, `then` nor `after`.
- A `message` does not support `for`, `given`, `then` nor `after`.
- A `message` requires exactly one `when` and no more than one `if`.
- Public statements by a `message` must continue to be assessable in the stable state end date for retained links.
- A field audience whose value direct is a magnitude you can choose one presentation available via `in`. If units are supported and this is omitted, the output uses the canonical projection and the compiler issues a warning. A magnitude 'Sin Unidades' publishes its issue without prior notice.
- One magnitude from point published directly is a numerical coordinate in the unit chosen; her `format` It is only published by explicitly constructing a field `Text`.

## Issues still to be resolved

### Q-051 — Identity and selection of a `look`

It remains to be defined how participants are selected, what result is obtained when they are not active, if a query It may return multiple rows, and explains how cardinalities, aliases and nested magnitudes are serialised. D-061 already sets the presentation of a magnitude used as value directly from a field public.

### Q-052 — Delivery from `message`

Still to be decided:

- If a single relationship can result in one or more occurrences during a action.
- How different messages and multiple occurrences are sorted.
- If duplicate detections are deduplicated.
- What happens to a detection if the action ends as `rejected` or `failed`.
- What happens if a participant becomes inactive before the stable state.
- If you keep it `if` It is assessed upon detection, upon stabilisation, or at both stages.

Until further notice Q-052, the standard merely stipulates that the published fields are evaluated after the stabilisation; the protocol for delivery.

## Consequences

- The AST incorporates `LookDecl`, `MessageDecl` and `PublicFieldDecl`.
- The runtime requires a queue transactional record of pending incidents, separate from any specific bus or transport service.
- The graph Semantic incorporates reading dependencies from public expressions.
- Messages must not manifest as external effects before the resolution can be verified.
- Materialisations can convert looks and messages into endpoints, queries, events or callbacks, but these mechanisms are not part of MUD.

## Future verification

1. `look` cigar with properties of type explicit and implicit, and with a compound expression.
2. Rejection of `given` in `look`.
3. `message` with and without `if`.
4. Rejection of headings and incompatible clauses.
5. A case where the value when detecting, it differs from the value published stable version.
6. Rollback without premature external output.
7. Notice regarding a magnitude public with unit selectable but without `in`, no notification when there are no units available, and formatted display of a point by means of `Text`.

## State rear

This decision was **replaced in its entirety by [[ADR-096-modulos-callables-look-message-and-activation|D-096]]**. Its description of `look` without `given`, `message` as an output where fields are evaluated only at the end, and the ‘host-only’ boundary is retained here solely for historical purposes.

