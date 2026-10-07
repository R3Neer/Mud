---
id: D-122
title: "Finite type graphs and proof obligations"
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - "Q-056"
affects:
  - "[[specification/11-type-system]]"
---

# ADR-122 — Finite type graphs and proof obligations

## Context

The author authorised development of the static formalisation from the accepted alias, inference and variance contracts. This integrates D-113 through D-116 without selecting an internal compiler schema.

## Decision

Chapter 11 defines finite normalised type graphs, least-fixed-point constructor productivity, separately witnessed domain inhabitation, finite canonical enumeration, read-only contract inclusion, nominal construction, representation equivalence, callable substitution and unambiguous synthesis/checking. A recursive pair alone proves nothing; representation comparison checks the complete finite relation and all local labels. A positive unique container requires enough distinct admissible witnesses, not merely an inhabited member constructor.

The mandatory proof basis consists of nominal ancestry, declared guarantees and established flow facts, normalised exact interval arithmetic, constructor rules and exhaustive finite witnessed cases. Arbitrary predicates need not be decidable. Unknown is not a discharged static obligation. Permitted runtime admission checks apply to a particular value, not universal callable substitution or canonical enumeration. This completes the remaining formal proof boundary of Q-056; it does not introduce universal domain-solving or termination algorithms.

The chapter remains proposed pending chapter publication. Its rules formalise accepted contracts; conceptual elaboration outputs do not prescribe ASDL, serialisation, nodes or storage strategy. D-097 continues to delimit nominal HIR and deferred semantic representation.

## Verification

MUD-TYPE-001 through MUD-TYPE-008 and finite inclusion, variance, recursive productivity and graph-equivalence witnesses in specification/types/typing-cases.yaml. The validator and its regressions check these finite witnesses and coverage, not MUD programme execution.

## Amendment provenance

[[ADR-134-static-generic-declarations-and-applications|D-134]] requires a finite generic application closure before graph normalization, and [[ADR-135-normalized-structural-type-equality|D-135]] adds exact normalized-contract equality without replacing conversion representation equivalence.
