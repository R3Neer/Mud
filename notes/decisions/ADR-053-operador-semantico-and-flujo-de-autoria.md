---
id: D-053
title: "Operador semántico y flujo de autoría"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-008"
  - "Q-015"
  - "Q-036"
  - "Q-039"
  - "Q-040"
affects:
  - "cambios semánticos, Git, tooling del operador"
---
# ADR-053 — Operador semántico y flujo de autoría

- Expanded by: [[ADR-085-diccionarios-funcionales-metadatos-and-activacion-estructurada|D-085]]
- Related questions: Q-008, Q-015, Q-036, Q-039, Q-040
- Documents affected: semantic changes, Git, operator tooling

## Context

Natural language interaction must transform the model through verifiable operations. You cannot hide new rules within the AI or edit `.mud` without considering the consequences.

## Decisión

Before making any changes, the operator classifies the request according to at least the following criteria:

- query or change;
- `CREATE`, `UPDATE`, `RETIRE` or migration;
- structural change, API change, causal, liaison, domain, type, chance, invariant, admissibility o reachability;
- ambiguous, incomplete, out of scope or an attempt to circumvent restrictions.

It can only apply mechanical inferences that have already been defined by the language, such as cardinality `[1]`, absence of `given` when no values are required, `empty`, canonical orders and finiteness derivable. It does not invent participants, `given`, domains, rules, actions, `after`, `always` nor the meaning of `allowed` o `eventually`.

The flowchart for a mutation is:

1. capture state Git and versions;
2. resolve intent, names and anchors;
3. to discuss decisions, queries and graph;
4. assess the impact and ambiguities;
5. draw up an operational plan;
6. prepare an isolated restoration;
7. edit authorised source and metadata;
8. format, compile and validate;
9. rebuild graph and IR;
10. to plan and carry out tests;
11. compare the expected and observed impact;
12. check diffs, paths and changes made by others;
13. create a atomic commit.

A failure prior to the commit restores the state Initial. A dirty worktree does not authorise you to modify or discard someone else’s work.

Pure enquiries `READ` do not create a commit. If a query resolves an issue or amends documentation; that amendment is `UPDATE`, no `READ`.

## Consequences

- A Codex plugin is a possible interface to services provided by query, rule management and action management.
- The diary retains state, provenance and asks questions, but doesn’t add semantics to the world.
- `RETIRE`, approval permits and the contract from explanation are still open.

## Verification

1. Multi-label classification of representative queries.
2. Rejection of a inference from domain unauthorised.
3. Restoration following failure at any stage.
4. Commits limited to the plan and no commits for `READ`.
5. Detection of unexpected impact before confirmation.
