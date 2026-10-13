---
id: Q-034
title: Derived magnitudes
priority: P2
opened: 2026-07-29
resolved: true
closed: 2026-10-13
decisions:
  - D-158
  - D-028
affects: []
superseded-by: []
---

# Q-034 — Derived magnitudes

## Resolution

The dimensional factor/unit-scale algorithm, deterministic validation diagnostics and Money interactions are specified. Rum representation inference and numeric literal/evaluation portability remain separately active Q-058; no corresponding numeric behavior is inferred from dimensional compatibility.

## Closure criterion

- C1: Specify terminating dimensional and unit normalization with diagnostics.
- C2: Specify Money and nominal/point boundaries with contrasting evidence.

## Closure evidence

- C1: D-158 and MUD-TYPE-037 in specification/11-type-system.md: finite exponent maps, positive checked scales, graph cycle rejection and topological anchor order.
- C2: Chapter 21 numeric signature/rounding table, magnitude-normalization-* corpus cases and specification/types/test_dimension_witnesses.py.
