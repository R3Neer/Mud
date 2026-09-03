---
id: Q-062
title: Complete grammar of `mud.module`
priority: P1
opened: 2026-08-28
resolved: false
closed:
decisions:
  - D-096
affects:
  - module grammar, source text, tooling
superseded-by: []
---

# Q-062 — Complete grammar of `mud.module`

## Content

Define the complete syntax of `mud.module` without reopening what D-096 has already decided: the file is named `mud.module`, delimits the module by its nearest ancestor and `uses` is the construct that declares contract dependencies. The repetition and grouping of `uses` entries, their separators/terminators, the complete file structure and any additional properties remain to be fixed, without duplicating the directory-derived MudPath.
