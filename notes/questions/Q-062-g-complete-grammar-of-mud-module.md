---
id: Q-062
title: Complete grammar of `mud.module`
priority: P1
opened: 2026-08-28
resolved: false
closed:
decisions:
  - D-096
  - D-109
affects:
  - module grammar, source text, tooling
superseded-by: []
---

# Q-062 — Complete grammar of `mud.module`

## Content

Define the complete syntax of `mud.module` without reopening what D-096 has already decided: the file is named `mud.module`, delimits the module by its nearest ancestor and `uses` is the construct that declares contract dependencies. The repetition and grouping of `uses` entries, their separators/terminators, the complete file structure and any additional properties remain to be fixed, without duplicating the directory-derived MudPath.

Foreign source/library/adapter dependencies also require explicit reproducible declarations. Their integration with `uses`, version pinning and adapter configuration remains to be specified with Q-069; `from` does not invent a second module grammar.
