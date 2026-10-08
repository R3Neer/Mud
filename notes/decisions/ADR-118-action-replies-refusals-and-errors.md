---
id: D-118
title: Action replies refusals and errors
status: current
date: 2026-10-06
supersedes:
  - D-008
  - D-079
superseded-by: []
questions:
  - Q-073
  - Q-003
  - Q-007
  - Q-022
  - Q-059
affects:
  - Language contracts and their developed normative surfaces
---

# ADR-118 — Action replies refusals and errors

- Amended by: [[ADR-121-typed-foreign-adapter-contracts|D-121]].

- Amended by: [[ADR-120-element-wise-block-error-recovery|D-120]].

- Formalised by: [[ADR-124-expression-and-block-typing-coverage|D-124]].

## Context

The author chooses first-class Success, Refusal and Errors values and Error-only block recovery. This replaces D-008 and D-079; it amends D-041, D-042, D-055, D-061 and D-077. All tooling and generated diagnostics are in English.

- Amended by: [[ADR-140-readable-patches-and-host-only-confirmation-tickets|D-140]].

## Decision

The following reply catalogue specifies no patch component; Q-073 retains that access interface.

```mud
alias Success {}
abstract alias Refusal { reason: Text; origin: Declaration }
abstract alias ConditionRefusal as Refusal { condition: BoolCheck }
alias IfRefusal as ConditionRefusal
alias AfterRefusal as ConditionRefusal
alias AlwaysRefusal as ConditionRefusal
alias ArgumentRefusal as Refusal { argument: Participant }
alias BoolCheck {
    expression: Text
    value: Bool [0..1]
    parts: BoolCheck [* ordered] = empty
}
abstract alias Error {
    reason: Text
    origin: Declaration
    cause: Error [0..1] = empty
}
alias Errors := Error [1..*]
alias ActionReply := Success | Refusal | Errors
```

These are language-defined nominal aliases; user aliases can specialize abstract bases with their own required fields and static conceptual metadata. Success denotes successful relative confirmation; access to the incorporated textual patch remains Q-073. The catalogue above does not select a patch component or resolve that interface. Error and Refusal have mandatory nonempty origin descriptors and human-readable reason. Origin is not a new general-purpose type: Declaration retains its existing nominal/reflection contract. An always refusal identifies the always rule declaration itself, whose identifier/path/anchor are available through existing metadata. ArgumentRefusal identifies the supplied role descriptor; the declaration origin is the invoked operation. Native exception origins identify the owning MUD declaration and source-mapped call site in diagnostics, not a fabricated native Declaration.

Error's optional cause enables wrapping another finite immutable error value. Conceptual description belongs to static metadata (for example ~description); specific reason, origin, cause and subtype-specific data are ordinary components. No field named message is introduced: message remains reserved for its language declaration.

Errors is a nominal collection alias used as one union alternative. Its representation has positive minimum cardinality. This does not allow an anonymous per-alternative collection specifier such as Success | Error [1..*] to mean a scalar-or-list union: the trailing shape applies to the complete union. The normal union restrictions are retained. Error occurrences preserve multiplicity even when values compare equal. Canonical error traversal/diagnostics respect causal order and use existing stable provenance for concurrent occurrences; no ordered modifier or deduplication is silently added to the user-visible Errors alias.

A successfully evaluated false action if yields IfRefusal; false after yields AfterRefusal; false always invariant yields AlwaysRefusal. Invalid supplied argument domains yield ArgumentRefusal. An ordinary Boolean expression returning false is a normal value, not intrinsically a Refusal. The owning constraint decides whether false refuses an operation. A computing error inside any block, including an expression block, produces Error occurrences instead of a Boolean result. Domain-invalid stored writes, incompatible effect consolidation and invalid runtime operations are errors, not false conditions. Static typing/name errors are compile-time diagnostics, not runtime Error values.

ConditionRefusal stores BoolCheck for the final returned Boolean expression only. Each Boolean subexpression has its source expression text, its evaluated truth value or empty if not evaluated, and ordered child checks. The root has value false. Preserve the actual short-circuit evaluation, including unevaluated branches, without reevaluating operands. A local used in the return is a leaf; its earlier defining expression and called rule/look internals are not expanded. The trace is captured before rollback and survives as immutable data. No automatic operand-value log or arbitrary execution trace is promised.

Built-in Error specializations classify arithmetic evaluation, domain/cardinality violations, incompatible effects and adapter failures; each retains the base components and relevant typed data. The exhaustive expression error catalogue and implementation resource-limit/defect boundary remain Q-007. A resource interruption or engine defect must not be silently presented as a modeled refusal or recoverable semantic error.

## Block error channel and recovery syntax

Every expression, value and effect block evaluates with a normal result and an Error [*] error channel. Empty means no error; nonempty means the normal result is unavailable. Sequential dependent evaluation stops at its first failed dependency; independent concurrent evaluations can contribute several occurrences. Action completion embeds a nonempty channel as Errors in ActionReply. Refusal is never an Error and is not selected by otherwise.

Otherwise clauses attach to blocks, including normalized short forms, not to declaration categories. They occur outside the protected body and use optional on bindings to Error-specialized aliases, an optional if filter, and exactly one then or raise branch. Multiple on roles are conjunctive; no on means catch any error. Then provides recovery subject to the protected block's normal-result/effect contract. Raise constructs a nonempty error value/collection and propagates it outward; executable-body raise is also admitted under D-147 and uses the same fault/recovery channel. Otherwise raise errorValue is catch-all short sugar. A clause with both then and raise, a Text-only diagnostic, or a Refusal binding is invalid. There is no finally. Detailed occurrence selection, rollback and propagation obligations belong to the block-recovery contract.

```mud
always rule Positive on counter: Counter { counter.value >= 0 }
# false produces AlwaysRefusal without an otherwise diagnostic
```

## Integration review

The result terminology also amends [[ADR-037-fields-and-declarative-domains|D-037]], [[ADR-039-collections-and-dictionaries|D-039]], [[ADR-045-causal-resolution-connections-and-queue|D-045]], [[ADR-046-algebra-and-conflicts-of-effects|D-046]], [[ADR-048-reproducible-randomness-and-errors|D-048]], [[ADR-052-pipelines-renderers-and-conformance|D-052]], [[ADR-059-magnitude-intervals-and-inverted-endpoints|D-059]], [[ADR-060-additive-deltas-and-nat-normalisation|D-060]], [[ADR-084-alias-specialisation-inherited-members-and-derived-views|D-084]], [[ADR-085-functional-dictionaries-metadata-and-structured-activation|D-085]], [[ADR-086-exact-nominal-identity-external-arrows-and-dictionary-algebra|D-086]], [[ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]], [[ADR-095-empty-extrema-as-ordinary-absence|D-095]], [[ADR-096-modules-callables-look-message-and-activation|D-096]], [[ADR-098-assignable-paths-and-write-back-of-immutable-aliases|D-098]], [[ADR-099-fresh-materialisations-after-destroy-and-create|D-099]], [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]], [[ADR-105-keyed-uniqueness-by-stable-path|D-105]], [[ADR-110-tentative-wave-journal-and-atomic-confirmation|D-110]].

The developed mathematical, grammar, lexical, CST and AST surfaces represent structured replies and block handlers. Chapters 11 and 21 develop static result/record and recovery typing; the complete dynamic action/error taxonomy remains separately scoped. Handler on names are local clause bindings, not new world participants or public anchors. Declaration descriptors retain their ordinary categories; no Origin type or typed-error graph is added to nominal HIR.

## Verification

Check each refusal subtype and mandatory origin, Error wrapping, finite BoolCheck trees with skipped branches, nominal Errors in a union, equal-valued occurrence multiplicity and Error-only handler selection. A false invariant is refused rather than a computing error. Errors from a Boolean computation remain distinguishable from false.
