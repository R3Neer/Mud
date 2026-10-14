---
id: D-171
title: Explicit structural alias construction and readability suggestions
status: current
date: 2026-10-14
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/10-names-and-anchors.md
  - specification/11-type-system.md
  - specification/13-aliases.md
  - specification/21-expressions.md
  - specification/names
  - specification/syntax
  - specification/types
---

# ADR-171 — Explicit structural alias construction and readability suggestions

## Accepted policy

The author accepts Alias(components) for an unambiguously statically identified
concrete structural alias. Positional form supplies all stored components;
named form preserves declaration-relative order and may omit only effective
defaults. Mixed/duplicate/unknown/derived arguments are invalid. A() requires
defaults for every component; A(x) supplies one component without tuple unpacking.
Representation aliases retain contextual construction/to; abstract aliases,
other categories and runtime Type values are not constructors. No overload or
expected-result target selection is introduced. Fully resolved explicit static
generic applications use existing grouped application/call syntax; constructor
argument inference is not introduced in this scope.

Construction inherits component/default admission, source demand and permissions;
it produces the exact target nominal identity. Source CallExpr and current
nominal references suffice, with no new public anchor, callable category or IR.
This extends D-032/D-113/D-114 construction without replacing explicit casting.

Tooling suggests explicit naming when expected type context is not locally clear,
and named arguments from three positional components, especially repeated types.
Short conventional forms remain appropriate. Suggestions are configurable and
not warnings; source distance is secondary and never changes admission.

## Evidence

MUD-ALIAS-005/MUD-TYPE-046, ordinary grammar/CST/AST coverage, nominal reference
review and finite supplied constructor/default/type witnesses plus declarative
counterexamples define the boundary. No source compiler/runtime is implemented.
