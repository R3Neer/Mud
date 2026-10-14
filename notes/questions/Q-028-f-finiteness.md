---
id: Q-028
title: Finiteness
priority: P2
opened: 2026-07-29
resolved: true
closed: 2026-10-14
decisions:
  - D-168
  - D-155
  - D-151
  - D-044
  - D-047
  - D-081
  - D-088
affects:
  - specification/11-type-system.md
  - specification/types
superseded-by: []
---

# Q-028 — Finiteness

## Resolution

D-168 completes the fixed-target source/application procedure: normalization,
finite source construction/search, exact proof decisions, nonexpansive generic
closure and explicit no-growth/variable-elimination completion. Violation,
completed-unproved and tool interruption remain distinct. Finite source values
need no uniform constant bound; no infinite lazy collections are introduced.
Deeper future-state/reachability profile work remains Q-027/Q-030 rather than
being inferred from a finite snapshot. The accepted procedure deliberately
rejects unsupported proofs conservatively; it does not promise a complete
mathematical solver for all source predicates.

## Closure criterion

- C1: The mandatory finite basis and source/generic proof premises are covered.
- C2: Specify exact normalization/search/completion and outcome distinctions.
- C3: Evidence sound accepted/rejected/unsupported and resource boundaries.

## Closure evidence

- C1: MUD-TYPE-033/MUD-TYPE-045 and finite-static-certification sections 3–4, with source/interval/generic witnesses.
- C2: D-168, MUD-CERT-001/MUD-CERT-002 and sections 1–5; the exact mixed affine, finite Rum and fixed-point procedures.
- C3: test_static_certification_witnesses.py, existing finite proof witnesses and corpus cases; explicit advanced-profile and tool-interruption exclusions.
