---
id: D-025
title: "Vocabulary from `thing`, headings and sections"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "[[specification/04-mathematical-model]], futuro `07-concrete-grammar.md`, futuro `11-things.md`, futuro `20-reglas.md`, futuro `21-acciones.md`"
---
# ADR-025 — Vocabulary from `thing`, headings and sections

- Related to: [[notes/decisions/ADR-018-as-declares-specialisation-in-is-the-query|D-018]], [[notes/decisions/ADR-030-explicit-quantitative-conversion-using-to|D-030]], [[notes/decisions/ADR-055-declarative-and-diagnostic-tests-otherwise|D-055]]
- Amended by: [[notes/decisions/ADR-096-modulos-callables-look-message-and-activacion|D-096]]
- Documents affected: [[specification/04-mathematical-model]], future `07-concrete-grammar.md`, future `11-things.md`, future `20-reglas.md`, future `21-acciones.md`

## Context

MUD terminology and headers must address three issues:

1. `construct` It sounded like a linguistic construct rather than something from the world.
2. `from` claimed to be a specialist, although natural reading for children is ‘`A` it’s like `B`».
3. `on` y `for` were assigned in a way that ran counter to the distinction one wishes to draw between observational statements and requested operations.

Furthermore, the documentation did not distinguish with sufficient clarity between instances where the keys are part of a clause and those where they are mandatory.

## Decisión

### `thing` y `as`

`thing` replaces `construct` such as reserved word:

```mud
thing Kingdom {}

abstract thing Place {}
```

`as` introduces the direct ancestors of a `thing`:

```mud
thing Egypt as Kingdom, Place {}

thing Alexandria as City {}
```

The list following `as` continues to denote a finite set of direct predecessors with no priority based on position. The Boolean operator `is` retains its semantics: query the reflective and transitive closure of that relation.

`as` it ceases to be an explicit conversion operator. D-030 subsequently sets the branch quantitative analysis of `to` y D-032 Add the nominal casting of compatible aliases.

### List of participants

The headings are arranged as follows:

| Organisation | Participants | `given` |
| --- | --- | --- |
| Exchange rate | `on` | No |
| Ruler `always` | `on` | No |
| `message` | `on` | No |
| `action` | `for` | Yes |
| Boolean rule | `for` | Yes |
| `look` | `for` | Yes |

`on` declares relationships that the engine automatically detects and constructs in order to identify events in the world. `for` declares the number of participants provided when requesting a transaction or query. `given` provides auxiliary values that are not participants and belongs to actions, Boolean rules and `look`; reactive rules, rules `always` y `message` They do not admit it.

### Key clauses

The clauses `when`, `if`, `after` y `then` They can take a ‘naked’ form when their body consists of a single element:

```mud
when door.open
if person is Citizen
then open gate
after gate.open
```

All these clauses always take brackets, even when they contain a single element:

```mud
when {
    door.open
}
```

A `then` Where there are several instructions, you must use brackets:

```mud
then {
    remove oldKing from kingdom.kings
    add newKing to kingdom.kings
}
```

In terms of actions and rules, `when`, `if` y `after` contain a single Boolean expression, even if that expression is compound. The `after` of a test, defined by D-055, contains one or more ordered assertions and requires curly brackets when it contains more than one. `then` It also requires curly brackets when it contains several statements.

## Consequences

- The lexer reserves `thing` y `as`; `abstract` is contextual before `thing`, in accordance with D-054; `construct` ceases to be reserved word.
- The AST uses `ThingDecl` and a list `directAncestors` introduced by `as`.
- `is` remains the only operator of query specialisation.
- The parser can select the header format based on the entity type.
- The analyser must reject `given` in `message`, exchange rules and rules `always`; `look` it accepts this in accordance with D-096.
- The future formatter may prefer the unindented form for short bodies and indents for long expressions, without changing the AST.

## Future verification

1. Declaration root, abstract and covering a wide range of specialisms, with `thing` y `as`.
2. Rejection of `construct` and from `from` as specialisation introducers; other grammatical uses of `from`, such as `remove x from c`, do not change.
3. Rejection of `as` as an explicit conversion.
4. One positive test and one negative test for each row of the matrix of participants.
5. Acceptance of each clause with and without curly brackets when it contains an element.
6. Rejection of a `then` naked, with various instructions.
7. Acceptance of a bare assertion and the requirement for keys for various assertions `after` of a test.
