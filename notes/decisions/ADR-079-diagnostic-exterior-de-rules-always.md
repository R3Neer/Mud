---
id: D-079
title: "External diagnostics for `always` rules"
status: current
date: 2026-08-04
supersedes: []
superseded-by: []
questions: []
affects:
  - "always rules, grammar, CST, AST, examples and diagnostics"
---
# ADR-079 — External diagnostics for `always` rules

## Context

The `otherwise` diagnostic of an `always` rule was written inside the braces containing its locals and final expression. That position made the diagnostic appear to be another element of the Boolean block and broke the form shared by `if`, `after` and `then` diagnostics.

## Decision

The braced body of an `always` rule contains only zero or more local bindings followed by a single final Boolean expression. Its optional `otherwise` is written after the closing brace:

```mud
always rule ValidPopulation on kingdom: Kingdom {
    population := kingdom.population
    population >= 0 people
}
otherwise "Population cannot be negative: {population}"
```

The diagnostic remains part of the complete rule, is evaluated lazily only when the invariant is false, and may resolve the body's local bindings. An `otherwise` placed inside the braces is invalid.

## Consequences

- `InvariantBodySyntax` no longer contains the diagnostic.
- `AlwaysRuleDeclarationSyntax` retains the optional `DiagnosticTailSyntax` after the body.
- `AlwaysRuleDecl` is unchanged: it continues to store the Boolean block and optional diagnostic separately.
- Terminator rules remain uniform; braces do not turn several complete expressions into one.

## Verification

1. A rule with an external diagnostic on the same line and on the following line.
2. A rule without a diagnostic and the corresponding warning.
3. Rejection of `otherwise` inside the body.
4. Visibility of body locals from the external diagnostic.
