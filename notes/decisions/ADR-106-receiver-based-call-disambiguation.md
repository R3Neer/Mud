---
id: D-106
title: "Receiver-based call disambiguation"
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions: []
affects:
  - "chapter 09, participant calls, chapter 07, Surface AST phase boundary, CST-to-AST explanation, Nominal HIR, validators and decision index"
---

# ADR-106 — Receiver-based call disambiguation

- Modifies: [[ADR-035-organisation-names-using-and-anchors|D-035]], [[ADR-036-participants-recipients-and-calls|D-036]], [[ADR-072-resolution-environments-and-explicit-anchor-migrations|D-072]], [[ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]], [[ADR-093-surface-ast-nominal-hir-and-later-semantic-phase|D-093]] and [[ADR-097-current-nominal-hir-and-deferred-semantic-ir|D-097]].
- Preserves the callable and part-level contracts of [[ADR-096-modules-callables-look-message-and-activation|D-096]].

## Context

Independent MUD paths may define operations with the same short name for unrelated participant types. Requiring qualification in every receiver call loses information already present in its `for` subjects. The author accepted static participant-based disambiguation while retaining distinct action anchors and rejecting overlapping compatible signatures.

## Decision

MUD-NAME-007 in [[specification/09-names-and-anchors#Receiver-call selection|chapter 09]] defines the complete contract. In a call with explicit receivers, all homonymous nominal callables governed by `for` at the first non-empty lookup level may be considered. They may be actions, subactions, Boolean rules, looks or sublooks. Exactly one must remain compatible with the static receivers, including role binding, collection shape, mutation capabilities and written given arguments. Candidate-local generic inference cannot use the expected result to choose a declaration.

Only statically established incompatibility excludes a candidate. Domain predicates and runtime values do not select an operation; ordinary unresolved obligations still apply after selection. Flow narrowing contributes static receiver information, but a union never triggers runtime dispatch between declarations. Written `given` names/types may select a target; omitted defaults as evidence, expected results and action conditions cannot. There is no most-specific preference, path-distance preference or import-order tie-break. Lookup never falls through because all candidates at an earlier level are incompatible.

Bare descriptor references, declarations governed by `on`, stored callable invocation and same-path name uniqueness retain their existing contracts. This decision does not resolve erased-descriptor binding or callable variance; it does not require changing those existing questions.

The two example declarations retain `action::a.stuff.Play` and `action::b.stuff.Play`. Their receivers neither own the actions nor contribute new anchor segments. Path overlap has no selection semantics. Qualification and `using` do not bypass part-level visibility.

The nominal HIR represents bindings using the sum `nominal_reference`: `ResolvedReference` or `PendingReceiverCall`. Pending calls retain at least two deduplicated nominal candidate symbols and the selected lookup level, with no type conclusion or chosen target. They introduce no symbols or anchors and no candidate `RefersTo` edges. Static selection belongs to later elaboration; the schema of that later result remains unfixed.

## Integration review

- Chapter 09 incorporates the exception, selection failures, examples, counterexamples, phase boundaries and graph invariants in their canonical locations.
- Chapters 07 and 08 and the CST-to-AST explanation preserve existing syntax while explaining deferred selection. EBNF, CST kinds, coverage and Surface AST constructors require no structural change.
- `names/mud-nominal-hir.asdl`, its README and the syntax validator incorporate the pending nominal lookup contract atomically.
- Amended current ADR bodies describe the resulting state and retain reciprocal provenance links. The decision index is regenerated.
- No chapter is promoted to `current`; their unrelated publication obligations and active questions remain in force. No temporary document or new open question is required.

## Rejected alternatives

- Changing anchors to make imported actions members of their receivers.
- Allowing two declarations named `Play` within the same MUD path.
- Choosing by result type, omitted defaults as argument evidence, runtime domains or conditions.
- Selecting the most specialised compatible candidate.
- Trying later lookup levels when an earlier non-empty level has no compatible receiver contract.
- Recording every candidate as a resolved nominal reference or placing receiver types in the nominal HIR.

## Verification

The following are semantic conformance requirements, not claims that a MUD compiler already executes them:

1. Two exact imports with unrelated `for A` and `for B` declarations select different anchors for `A.Play()` and `B.Play()`.
2. Repeated imports of the same anchor are deduplicated before selection; import order and shared path suffixes do not affect the result.
3. Multiple positional receivers and exhaustive named receivers are checked against each signature; one collective role is not expanded into multiple roles.
4. Missing roles, incompatible static types or collection contracts, and unavailable mutation capabilities exclude incompatible candidates.
5. `for A` and `for Thing`, or two unrelated bases satisfied by a common subtype, remain ambiguous for a compatible receiver.
6. A zero-candidate result fails at the original lookup level; exact imports retain priority over recursive imports and current-path or lexical symbols retain their precedence.
7. Different written `given` names/types may break a receiver tie; omitted defaults as evidence, expected results and runtime conditions never do. A uniquely selected target with invalid arguments fails ordinary validation.
8. Narrowing before the call may yield a unique target; a union cannot dispatch each alternative to a different target at runtime.
9. Bare `Play` descriptor references remain ambiguous, and stored callable values retain their existing invocation contract.
10. Fully qualified operation references avoid short-name selection but still require compatible participants and authorised part-level visibility.
11. Same-path duplicates remain invalid, and the selected action retains its path-derived anchor.
12. Pending HIR calls retain source provenance, lookup level and the complete candidate set, with neither a target nor candidate `RefersTo` edges. Resolved receiver roots retain their own edges.

Mechanical validation checks the HIR constructor contract, declared ASDL types, forbidden elaboration fields, grammar/CST/AST consistency, decision metadata, question metadata, editorial rules and temporary-document inventory. Regression tests reject malformed HIR declarations; they do not implement the receiver compatibility algorithm.

## Amendment provenance

The static written-given selection contract is amended by [[ADR-136-static-given-call-disambiguation|D-136]]; the first non-empty lookup level, nominal HIR boundary and absence of runtime dispatch remain in force.
