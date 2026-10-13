---
id: D-153
title: Operator descriptors metadata and textual anchor policy
status: current
date: 2026-10-13
supersedes: []
superseded-by: []
questions:
  - Q-075
affects:
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/10-names-and-anchors.md
  - specification/21-expressions.md
  - specification/grammar/mud.ebnf
  - specification/syntax
  - specification/names/mud-nominal-hir.asdl
---

# ADR-153 — Operator descriptors metadata and textual anchor policy

## Decision

Operator reflection exposes ordered operand descriptors containing each source operand's name and effective type contract. Names are descriptive, not signature identity. They do not become alias fields or for/given participant descriptors. Existing access/visibility and source-owner rules apply.

Operator metadata follows the established descriptor-value-body convention: a short result expression may have an immediate metadata-only body; an expanded value body may begin with the operator descriptor's metadata preamble. The two attachment forms cannot be combined. Metadata describes the original whole declaration and is elaborated under ordinary metadata-owner rules, not on every invocation. Operand runtime bindings are unavailable in the metadata preamble. Configured properties have no algebraic, selection or automatic-inverse privileges.

Canonical operator anchors use complete collision-free textual encodings of normalized operand contracts. They are self-contained; a digest or registry lookup is not their identity. The established simple form remains alias::path.Vector2::operator::*(path.Vector2, Num). Formatting and normalized equivalent sugar do not change identity; nominal labels, symbolic domain provenance and ordered contracts remain significant. A display may abbreviate an anchor without changing it.

## Formalization boundary

Q-075 retains the exact canonical grammar/escaping for complex normalized contract graphs, generic binders and applications, and the complete reflective property/type schema. These are required specification work under the accepted policy, not permission to choose hash identities or erase operand names. No new policy for generic application anchors is introduced.

## Verification and provenance

Extends [[ADR-149-alias-operator-selection-inheritance-and-reflection|D-149]]. EBNF, CST catalogue, coverage, Surface AST metadata lists, projection, source fixtures and token-level grammar tests integrate both attachment forms. Chapter 10 and nominal HIR preserve typed/nominal phase separation.
