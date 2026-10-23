---
id: D-183
title: Functional families, currification and input syntax
status: current
date: 2026-10-23
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/07-lexicon.md
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/10-names-and-anchors.md
  - specification/11-type-system.md
  - specification/13-aliases.md
  - specification/17-dictionaries.md
  - specification/21-expressions.md
  - specification/types/
  - specification/grammar/
  - specification/syntax/
  - specification/names/
  - notes/examples/duelo-spellcasting
---

# ADR-183 — Functional families, currification and input syntax

## Decision

The author accepts first-class correlated functional families, partial
application and cumulative/named/inferred arguments. Unknown free lowerCamel
references in eligible immutable definitions become inputs in first-occurrence
order; resolved outer references remain captures. value is reserved, with explicit
member-name exceptions for existing value components. Neither those exceptions
nor ordered by value permits local/argument shadowing. Literal partial inputs
retain contextual numeric possibilities until a static use requires selection.

Functional --> now gives type-adjacent input/output cardinalities; -> retains
association counts. Both associate right and grouping preserves residual policy
collections. first/all constructors select branches independently of result order;
unmarked branches use AllMatches. A plain body can omit its unconditional branch.
AllMatches aggregates exterior result occurrences from matching branches,
preserving repetitions unless explicit uniqueness removes them. It does not
wrap each contribution or flatten nested members: [1,2] plus [3,4] contributes
four members; [[1,2]] plus [[3,4]] contributes two collection members. Cardinality
is checked on the aggregate, not as a separate minimum on each contribution.
Compact f[a,b] checks product and curried interpretations; multiple valid paths
require explicit grouping. No distribution, Any guessing, implicit inverse,
runtime nominal type generation or real action effect is introduced.

= stores a policy/residual value; := reconstructs a live value from dependencies.
Capturing a thing identity does not freeze its fields. A residual captures applied
arguments; subsequent live body reads occur in its application snapshot.

Partially amends D-085/D-086/D-169/D-172/D-173/D-178/D-180. The canonical static
contracts are in specification/types/functional-families.md; the causal algorithm
and foreign-host callback protocols remain independently scoped.

## Verification

Integrate current normative surfaces, nominal HIR/Surface AST contracts and
bounded positive/negative corpus witnesses. Repository checks do not implement
a compiler/runtime or certify unresolved host/causal protocols.
