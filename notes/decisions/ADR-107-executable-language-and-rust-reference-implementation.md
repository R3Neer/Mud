---
id: D-107
title: "Executable language and Rust reference implementation"
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions: []
affects:
  - "README, vision and scope, system architecture, source authority, compiler and materialiser direction"
---

# ADR-107 — Executable language and Rust reference implementation

- Modifies: [[ADR-001-mud-as-a-source-semantics-really|D-001]], [[ADR-002-mud-describes-domain-not-application-architecture|D-002]] and [[ADR-052-pipelines-renderers-and-conformance|D-052]].
- Preserves: [[ADR-003-mud-is-a-formal-declarative-language|D-003]], [[ADR-011-derivatives-do-not-add-behaviour-of-domain|D-011]] and the host boundary of [[ADR-096-modules-callables-look-message-and-activation|D-096]].

## Context

The author wants an executable language and toolchain, rather than treating the specification as the sole product. Formal precision remains necessary, and the implementation must not silently decide open language questions.

## Decision

The reference compiler and runtime will be written in Rust. Initial MUD code generation targets Rust. C and TypeScript remain possible alternatives without a near-term implementation commitment. This project choice does not constrain the implementation technology of another conforming MUD implementation.

MUD supports two hosting directions: an application may embed a MUD model through `look`, `action` and `message`, or a MUD programme may coordinate foreign-language components through explicit adapters. Rust, Python and C# are the initial planned adapters. Adapters execute or link foreign code in its own environment; they are not MUD code-generation backends for those languages.

MUD sources explicitly identify domain behaviour and foreign contributions. Reproduction includes declared foreign sources, library and adapter versions and boundary contracts. Generated artefacts cannot introduce undeclared domain rules. Guarantees involving foreign code are conditional on its declared contracts; they are not proofs of arbitrary external libraries.

The feature inventory is intended to be complete after the foreign construction is integrated. Completing the formal specification, outstanding contracts and conformance cases remains the immediate work; no compiler or adapter implementation is claimed by this decision.

## Verification

1. README, vision and architecture agree on Rust implementation and initial Rust generation.
2. C and TypeScript are possibilities, not scheduled deliverables.
3. Host integration retains the operation-centred boundary.
4. Source-authority descriptions include explicit foreign dependencies while keeping generated artefacts reconstructible.
5. Current ADR bodies and reciprocal links reflect the accepted direction; no normative chapter is promoted or future semantic IR schema created.
