---
id: Q-060
title: Reflective `TypeKind` catalogue
priority: P1
opened: 2026-08-16
resolved: true
closed: 2026-10-13
decisions:
  - D-157
  - D-148
  - D-144
  - D-087
affects:
  - specification/09-abstract-syntax.md
superseded-by: []
---

# Q-060 — Reflective `TypeKind` catalogue

## Resolution

The complete fixed core constructor/support inventory and normalized projection are specified. Libraries cannot add kinds. Compiler releases preserve the selected target catalogue; project target declaration and persistent migrations remain Q-038, without changing this fixed-version contract.

## Closure criterion

- C1: Complete normative core catalogue and projection exist.
- C2: Fixed-family behavior and observable target-version compatibility are specified.
- C3: Internal forms project without incidental implementation nodes.

## Closure evidence

- C1: D-157 and the public/core-support tables in specification/11-type-system.md, including nominal support/error aliases, reflective families and descriptor boundaries.
- C2: MUD-TYPE-026 and the fixed-target compatibility paragraphs in chapter 11: no compiler-release catalogue changes or automatic merge/fallback.
- C3: Chapter 11 normalized-exterior algorithm and exclusions; typekind-support-inventory, typekind-nominal-reply-alias and typekind-default-versus-explicit-collection corpus cases.
