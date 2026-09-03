---
title: Obsidian Explorer ordering
tags:
  - mud/governance
  - mud/obsidian
status: current
sorting-spec: |
  target-folder: /*
  README
  /:files. ....base
   < a-z
  sorting: standard

  target-folder: /
  README
  /:files. ....base
   < a-z
  specification
  notes
  governance
  references
  tooling
  AGENTS
  sortspec
  ...
   < a-z

  target-folder: governance
  README
  /:files. ....base
   < a-z
  POLITICA-DE-DECISIONES
  POLITICA-DE-PREGUNTAS
  CICLO-DOCUMENTAL
  POLITICA-DE-COMMITS
  ...
   < a-z
---

# Obsidian Explorer ordering

This note configures `Custom File Explorer sorting` with one general rule and
two specific editorial orderings:

- in any folder, `README.md` appears first and `.base` files immediately
  afterwards, in alphabetical order when there is more than one;
- at the root, documentation surfaces come first, followed by technical support;
- in `governance/`, the policies governing decisions and questions come first.

Specification folders, ADRs and questions retain their natural identifier
order. Their prefixes are part of portable navigation and must not be removed
solely to improve their presentation in Obsidian.

## Local configuration

Install and enable the plugin with:

```powershell
obsidian plugin:install id=custom-sort enable
```

The `.obsidian/` configuration is not versioned. To keep dependencies and
generated output out of searches, the local vault excludes at least:

```text
exports/
/node_modules/
/__pycache__/
tooling/.deps/
/coverage/
/.wrangler/
```
