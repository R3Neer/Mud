---
id: Q-008
title: Git and READ protocol
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-053
affects: []
superseded-by: []
---

# Q-008 — Git and `READ` protocol

## Content

Which operations produce a commit? Proposal: `READ` queries do not; `CREATE`, `UPDATE`, `RETIRE` and migrations do.

Status: **partially decided** by [[notas/decisiones/ADR-053-operador-semantico-y-flujo-de-autoria|D-053]].

Pure `READ` queries produce no commit, and every confirmed change is limited to the plan without discarding other work. The stable message format, technical isolation and which derived artefacts are versioned remain to be fixed.
