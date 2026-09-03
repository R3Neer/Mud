---
id: Q-061
title: Declarable form of computed `family` data
priority: P1
opened: 2026-08-16
resolved: true
closed: 2026-08-29
decisions:
  - D-037
  - D-038
  - D-085
  - D-091
  - D-102
affects:
  - specification/07-gramatica-concreta.md
  - specification/08-sintaxis-abstracta.md
  - specification/grammar/mud.ebnf
  - specification/syntax/mud-surface-ast.asdl
superseded-by: []
---

# Q-061 — Declarable form of computed `family` data

## Question

Which form may declare computed `family` data: only an optional type before `:=`, or the complete `derived-value-shape` of computed fields?

## Context

D-038 retained a narrow exception, while the EBNF and surface AST already represented `[ derived-value-shape ]`. D-102 expressly adopts the broad form and removes the divergence.

## Already decided

- Computed data is immutable and evaluated statically for each member.
- Its type may be inferred when the expression determines one uniquely.
- The data declaration has a `Field` descriptor, subordinate anchor and its own metadata in accordance with D-091.
- A member assignment may not target computed data.

## Closure criterion

- C1: One non-contradictory normative form exists for computed `family` data.
- C2: The complete form reuses the `derived-value-shape` contract of computed fields without granting outer mutability or storage.
- C3: EBNF, CST coverage, AST projection and surface AST retain exactly that form.

## Resolution

The complete `derived-value-shape` of computed fields is adopted. Computed `family` data may declare compatible type, domain and collection form as result constraints or coercions, but remains immutable, has no outer `mut` and has no own storage.

## Closure evidence

- C1: D-102 fixes `name [derived-form] := value-body`, and D-038 incorporates that rule literally.
- C2: D-102 refers to D-037 semantics and explicitly retains the absence of outer `mut`, stored default and own storage.
- C3: `specification/grammar/mud.ebnf` retains `[ derived-value-shape ]`; `cobertura-sintactica.yaml` and `cst-a-ast-superficial.md` project that form; `mud-surface-ast.asdl` retains `derived_value_shape? shape` in `CalculatedFamilyDataDecl`.
