---
id: D-055
title: "Declarative and diagnostic tests `otherwise`"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-059"
affects:
  - "[[notas/preguntas/README|Preguntas activas]], futuros capítulos 06 a 09, 25, 28, 30, 43, 46 y 49"
---
# ADR-055 — Declarative and diagnostic tests `otherwise`

- Related to: [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|D-025]], [[notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas|D-035]], [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]]
- Open: [[notas/preguntas/Q-059-observacion-de-resultados-de-accion-en-tests|Q-059]]
- Expanded by: [[notas/decisiones/ADR-071-vinculaciones-locales-en-bloques-booleanos|D-071]]
- Further expanded by: [[ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]]
- Documents concerned: [[notas/preguntas/README|Active questions]], future episodes 06 to 09, 25, 28, 30, 43, 46 and 49

## Context

MUD needs tests that can be read and written by those who model the world, without forcing them to abandon the language they use to describe the anticipated scenario. A test shares this with a action the use of effects, stabilisation and postconditions, but it is not part of the API of the world:

- It does not have an external applicant.
- It does not change a world persistent.
- It does not represent an operation available to characters or systems.
- His result inform the test administrator.

Treat it as a variant of `action` It would blur the distinction between the two and make it natural, albeit incorrect, to assign it a anchor `action::*`.

## Decisión

### Declaration own

`test` is a reserved word which introduces a category of declaration own:

```mud
test CounterIncreases {
    start with Counter

    then Counter.value += 1

    after {
        Counter.value == 1 otherwise "The counter did not increase"
        old Counter.value == 0 otherwise "The counter did not start at zero"
    }
}
```

A test:

- It has a nominal name in `PascalCase`.
- No statement `for`, `given`, `if`, `when` nor participants.
- It states exactly one `start with`, a `then` and a `after`.
- It cannot be invoked as `action` nor can it be queried as a rule; in a testing context, it can be invoked as an operation `test` from the `then` from another test visible in accordance with D-096.
- It cannot be the aim of `create` o `destroy`.
- It cannot appear in a set `start with`.

In brief:

```ebnf
test-declaration
    ::= "test" nominal-name "{"
        test-start-with
        then-clause
        test-after-clause
        "}"

test-start-with
    ::= start-with-declaration

test-after-clause
    ::= "after" test-assertion
      | "after" "{" test-assertion { terminator test-assertion } "}"

test-assertion
    ::= boolean-expression [ "otherwise" text-expression ]
```

`test` is not a contextual modifier of `action`. The AST contains its own form:

```text
TestDecl(anchor, initialActivationSet, thenBody, assertions)
TestAssertion(condition, optionalDiagnostic)
```

### World isolated and `start with`

Each execution of a test begins with a world empty, cool and isolated. The `start with` of a test is an original contribution by activation and does not itself incorporate the `start with` standard modules.

Area is the standardised term for D-096: a direct contribution or a block of expressions that provide zero, one or more activatable statements `thing | rule`. The order is not observable and duplicate identities are deduplicated. It contains no instructions `create`, assignments or other effects, and a collection The nested one is invalid.

Before running the test root The transitive closure of tests that it may call is calculated statically, whilst respecting `uses`, and the contributions are combined `start with` of all of them. One call following a test once included, it does not materialise again activation; a executable cycle between tests is invalid. The resulting declarations are instantiated together with their canonical initialisers and the world stabilises before the `then` root.

Be $C(t)$ the static transitive closure of tests reachable from the test root $t$, whether $I_u$ the contribution of activation of each test $u$ and let it be $I_t^*=\bigcup_{u\in C(t)} I_u$. The state The value prior to the scenario is obtained as follows:

$$
W_t^0
=
\operatorname{stabilize}
\bigl(
\operatorname{materialize}(P,I_t^*)
\bigr)
$$

The initial activation The ordinary form of the modules does not feature in this construction.

### `then` y state from the stage

`then` use the semantics ordinary in terms of consequences and form, the transition tested. You can combine effects, local variables and permitted calls, including operations `test` visible in the context of tests. The assignments and other modifications written at the beginning of `then` do not belong to the state Initial: these are effects of the spell. Cast a test whose `start with` if they have already taken part in the initial closing, they do not make that contribution again.

The state observed by `old e` inside `after` is $W_t^0$, prior to the `then` Complete. There is no implicit boundary between preparation and exercise instructions based on their position in the text.

The resolution from the `then` includes its root, its causal waves, the rules `always` and the stabilisation. The world The resulting figure is never published and is discarded at the end of the test.

### Statements and `otherwise`

The `after` of a test contains one or more ordered assertions. Each assertion consists of:

1. A pure expression of type `Bool`.
2. A diagnostic optional feature introduced by the reserved word `otherwise`.

The diagnostic it must be a pure expression of type `Text` and is only evaluated when the associated condition is false. If omitted, the compiler offers a suggestion and the runtime produces a diagnostic default value based on the condition and its provenance.

```mud
after condition

after condition
    otherwise "Explanation"

after {
    firstCondition
    secondCondition otherwise "Second condition failed"
}
```

All conditions are assessed on the same basis state stable and in textual order. The executor may report all false conditions together. An assertion has no effect.

`after` does not return the union `Bool | Text`: the condition remains type `Bool` and the diagnostic preserves type `Text`.

### Result and discard

The execution of a test produces exactly one of these results for the executor:

| Result | Reason |
| --- | --- |
| `passed` | The initial world and the `then` they stabilise and all the assertions are true |
| `failed` | At least one statement is false and no phase produces a error |
| `error` | The initial world, the resolution from the `then` or the evaluation of an assertion fails, or diagnostic |

`passed`, `failed` y `error` are not ordinary shares in the world nor do they replace `accepted`, `rejected` y `failed` of the shares.

The state in isolation, the messages and any other output produced during the test are always discarded. The executor may retain only the result, the diagnostics and the trace required to explain them.

### Words and anchors

`test` y `otherwise` These are reserved words.

`abstract` remains contextual in the context of `thing` y `always` is contextual before `rule`. Modifiers and variants do not change the category of the anchor:

```text
thing::world.Vegetation
rule::world.ValidWorld
test::world.CounterIncreases
```

One `abstract thing` use `thing::*`. A ruler `always` use `rule::*`. A test use `test::*` because it constitutes a distinct declarative category.

## Consequences

- The tests form part of the source code, but not of the world neither the executable nor its public API.
- The compiler may exclude `TestDecl` from a compilation of production after validating it.
- The test runner reuses the transactional engine and causal without publishing the results.
- Selection by anchors `test::*` allows you to run a test, a path from MUD or a filtered set.
- No preparatory phase can be inferred from the initial instructions in `then`.
- The explicit verification of the result `accepted`, `rejected` o `failed` of a action The appeal remains pending in Q-059.

## Options ruled out

### `test action`

It is ruled out because it presents the test as a variant of the write API, and it would be inconsistent to assign it a category of anchor different.

### `if` as a precondition for the test

This is ruled out because it would allow a test to be silently skipped when the world does not meet the condition. The test deliberately builds his world by means of `start with`.

### State changeable within `start with`

It is ruled out because it would lead to a mix-up initial activation and effects. The specific values for the scenario are set out in `then`.

### `after` from type `Bool | Text`

It is ruled out because it combines verification and diagnostic. `otherwise` It keeps the two types separate and allows different messages for various conditions.

## Future verification

1. Recognition of `test` y `otherwise` as reserved words.
2. Anchor `test::*` regardless of `action::*`.
3. Rejection of `for`, `given`, `if` y `when` in a test.
4. Union from `start with` of the static transitive closure of reachable tests, without applying the activation standard configuration of the modules.
5. Rejection of instructions and assignments within a contribution `start with` from test.
6. Materialisation y stabilisation before the `then` root, call subsequent without reactivation and rejection of executable cycles between tests.
7. Reading from `old` on the state prior to the `then` complete.
8. A single assertion and multiple assertions with optional diagnostics.
9. A cursory assessment of the diagnostic `otherwise`.
10. Distinction between `passed`, `failed` y `error`.
11. Unconditional rejection of the world and their outings.
12. Anclas `thing::*` for abstracts and `rule::*` for rules `always`.

## Amendment current by D-096

The `start with` from test use the unified interface of D-096. For a test root The transitive closure of tests that it can call is calculated statically, and their contributions are combined activation before executing the body. Tests may cross modules only within a test context, by means of test visible elements and dependencies `uses`; a call the latter does not run the `start with` from the test achieved.


