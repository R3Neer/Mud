---
title: Obsidian Explorer Command
tags:
  - mud/gobierno
  - mud/obsidian
status: vigente
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
  especificacion
  notas
  gobierno
  referencias
  tooling
  AGENTS
  sortspec
  ...
   < a-z

  target-folder: gobierno
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

# Obsidian Scout Order

This note configures `Custom File Explorer sorting` with one general rule and two
specific editorial instructions:

-  in any folder, `README.md` appears first and the `.base` files
  immediately afterwards, listed in alphabetical order if there is more than one;

-  in the root, first the documentary aspects and then the technical support;
-  in `gobierno/`, first the policies that govern decisions and queries.

The folders for specification, the ADRs and the questions remain in the same order
natural by identifier. Their prefixes form part of portable navigation
and they should not be removed simply to improve the presentation in Obsidian.

## Local settings

The plugin is installed and activated as follows:

```powershell
obsidian plugin:install id=custom-sort enable
```

The configuration of `.obsidian/` is not versioned. To prevent dependencies and
To prevent generated outputs from skewing search results, the local vault excludes at least the following:

```text
exports/
/node_modules/
/__pycache__/
tooling/.deps/
/coverage/
/.wrangler/
```

