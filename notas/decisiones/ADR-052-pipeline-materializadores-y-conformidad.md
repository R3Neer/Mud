---
id: D-052
title: "Pipelines, renderers and conformance"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-007"
  - "Q-009"
  - "Q-037"
  - "Q-038"
affects:
  - "arquitectura, tooling, conformidad"
---
# ADR-052 — Pipelines, renderers and conformance

- Expanded by: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Expanded by: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]
- Related to: [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]]
- Related questions: Q-007, Q-009, Q-037, Q-038
- Documents affected: architecture, tooling, conformance

## Context

The example combined language requirements with a TypeScript implementation, a plugin and editor support. MUD needs to enforce conservation semantics without imposing those technologies.

## Decisión

The conceptual pipeline separates:

1. lexer;
2. parser;
3. Surface AST;
4. resolution MUD paths, statements `using`, names and anchors;
5. system of types, aliases, domains, cardinalities, mutability and quantities;
6. analysis of purity, effects, cycles, finiteness, termination and stochasticity;
7. Canonical IR;
8. graph, diagnostics, formatting and media creation.

The parser does not directly produce IR: it must be retained provenance sufficient for diagnosis, syntax and syntactic development.

A materialiser can use functions, parameters, tuples, maps, transactions, speculative copies or exhaustive exploration. It cannot:

- to make up rules for domain;
- change identity, nominality or specialisation;
- to confuse participants with `given`;
- change atomicity, order causal or results;
- convert `failed` false;
- use a floating decimal point for the semantics observable of `Num`;
- bring forward the publication of `message`.

The conformance It is tested using valid and invalid programmes, required diagnostics, expected IR, transitions, traces and properties. The editor must distinguish between participants `on`, roles `for` linked by identity, value or place, `given`, domains, rule variants and public signatures, but it does not constitute semantics.

The compiler validates the declarations `test`. A profile of production You can remove them after the analysis; a test runner retains their IR, constructs their isolated worlds and discards all their effects and outputs. Tests written in MUD do not replace the suite of conformance of an implementation.

## Consequences

- TypeScript is a possible destination, not part of MUD.
- The list of reserved words is generated or checked against the standard grammar; it is not maintained manually as a provisional list.

## Verification

1. Two different materialisers produce equivalent observations.
2. AST and IR have distinct functions.
3. Cases of conformance for participants, `given`, actions, rules and exits.
4. The editor displays the signature semantics resolved.
5. No derived artefact is required to reconstruct the model.
6. Separation between user tests, execution of production and suite of conformance.

