---
id: D-044
title: "Alcanzabilidad `eventually`"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-026"
  - "Q-027"
  - "Q-028"
  - "Q-029"
  - "Q-030"
  - "Q-031"
affects:
  - "expresiones, alcanzabilidad, finitud, terminación"
---
# ADR-044 — Alcanzabilidad `eventually`

- Related questions: Q-026 a Q-031
- Documents affected: expressions, reachability, finiteness, termination

## Context

`eventually` expresses a question about reachability on the subject of model. In order to ensure a decidable response, it cannot be executed on an arbitrary space.

## Decisión

```mud
eventually game.Checkmate(White)
    through game.Move

eventually game.Checkmate(White)
    through game.Move, game.Pass

eventually game.Checkmate(White)
    through [game.Move, game.Pass]
```

The expression is true if there exists a finite sequence of accepted requests for the actions permitted by `through` which leads to a state where the target is true. The empty sequence is included: the state The current one can meet the objective.

Each edge explored is a transition MUD complete with validation from request, root, waves, rules `always` y `after`. Rejected requests do not form edges; a failure during a transition does not become a transition valid.

The participants and everyone `given` any that are to be generated must come from finite, countable domains with a canonical order. For a role `for` The ‘collective’ section lists complete collections that meet your contract, non-members holding positions of receiver separate. If the role has mutability exterior, there must also be a finite, countable and canonical set of candidate stored locations; it is not enough simply to list their current values.

The compiler only accepts the expression when it can be shown, conservatively, that:

- finiteness of the space of state relevant;
- enumerability of all applications;
- termination of each transition;
- comparability and standardisation of states;
- the absence of unbounded creation.

If chance exists, quantification is existential with regard to sequences of possible outcomes with positive probability:

$$
\exists \vec a,\vec r.\;
\Pr(\vec r)>0
\land
W \xRightarrow[\vec r]{\vec a} W'
\land
W'\models goal.
$$

`through` accepts one or more references to actions using the contextual syntax of collection, with optional square brackets. Its elements are references to actions, not calls with participants, and `given` already defined: the analysis lists the admissible requests based on their domains.

The order in which the references appear does not alter the truth of the query. The canonical order of enumeration and the specific search strategy are not yet part of the normative meaning, provided that the algorithm is complete for the permitted profile and terminates. General recursion is not introduced into the source language.

## Consequences

- The inability to demonstrate that the conditions are met categorically precludes the use of `eventually`; it does not return a false result.
- The canonical order of enumeration and the minimal definition of state The relevant issues remain unresolved.
- The initial implementation may use breadth-first search, but this choice will only be standard if it is decided that it affects diagnostics or test cases.

## Verification

1. True target via an empty sequence.
2. A finite path that exists and does not exist.
3. Rejection of a `given` infinite or uncountable.
4. Rejection of an unrestricted creation.
5. Random case with result with a positive probability.

