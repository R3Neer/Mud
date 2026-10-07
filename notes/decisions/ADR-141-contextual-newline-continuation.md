---
id: D-141
title: Contextual newline continuation
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions:
  - Q-001
affects:
  - specification/07-lexicon.md
  - specification/08-concrete-grammar.md
  - specification/grammar/
  - specification/syntax/
---

# ADR-141 — Contextual newline continuation

## Context

The author accepts next-fragment grammatical lookahead after a complete line, including separate instructions whose beginnings are valid but incomplete on their first physical line. This amends the newline portions of D-050 and D-057, without replacing their other scopes or reopening resolved Q-001.

## Decision

Open constructions retain grammatical newline continuation. After a complete unit, inspect the next significant fragment in the enclosing grammatical context. If it starts a separate unit, the newline separates them; that start may be incomplete, such as `other =`. This interpretation wins over possible continuation. Otherwise, if it can continue the current unit, treat the newline as whitespace. If neither interpretation is valid, diagnose a syntax error rather than forcing concatenation. A recognised next-unit start is not undone to rescue later invalid content.

Skip comments and blank lines when inspecting the next fragment. Do not cross explicit semicolons, EOF or the enclosing closing delimiter. An explicit semicolon remains a separator and cannot repair an unfinished instruction. Required attachments, native regions and literal/comment modes retain their own grammar contracts. Indentation, resolution and typing play no part in the choice.

Continuation newlines retain exact bytes/spans as ContinuationNewlineTrivia in the lossless CST catalogue. Separating newlines supply TERMINATOR. No production, node/token kind, AST or nominal HIR constructor changes are needed. Source that is syntactically admitted remains subject to ordinary names, types and capabilities.

## Alternatives and consequences

Reject the prefix-only rule because it forbids a leading operator that cannot start another instruction. Reject unconditional concatenation because it would join valid separate instructions. A next unit need not be complete on its first physical line. This expands accepted wrapping, while explicit semicolons retain intentional separation.

## Verification

MUD-SYN-015 and the lexical/CST/projection contracts agree. Reviewed sources and finite supplied-premise certificates cover leading operators, incomplete next assignments, start/continuation priority, blank lines/comments, semicolons, enclosing boundaries and invalid continuations. The checker does not parse Mud, infer grammatical premises or implement a compiler. Existing EBNF/CST/ASDL checks and syntax regressions must pass. Chapter publication states remain unchanged.
