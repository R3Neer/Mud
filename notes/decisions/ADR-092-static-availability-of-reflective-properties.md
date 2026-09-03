---
id: D-092
title: "Static availability of reflective properties"
status: current
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "reflection, metadata, participants, nominal resolution, typing, post-typing and elaboration semantic representation, diagnostics and tooling"
---

# ADR-092 — Static availability of reflective properties

- Clarifies: [[ADR-087-reflective-metadata-stable-descriptors-and-external-visibility|D-087]].
- Aligned with the phase boundary of [[ADR-093-surface-ast-nominal-hir-and-later-semantic-phase|D-093]].
- Clarifies `Metadata` terminality in accordance with [[ADR-094-terminal-anchors-for-configured-metadata|D-094]].
- Extends: [[ADR-074-nominal-unions-and-type-narrowing|D-074]] and [[ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]].

## Context

The postfix syntax `expression~property` must recognise names that are hard keywords, such as `for`, `on` and `given`. The concrete rule `metadata-name ::= identifier | "for" | "on" | "given"` permits this spelling, but cannot determine during parsing which category a receiver expression denotes.

D-087 also stated that an absent clause produces `empty`. Read without the owner restriction, that sentence could be misinterpreted to mean that every declaration always has `~for`, `~on` and `~given`. That would make, for example, `thing A; A~for` valid even though a `thing` has no `for` signature.

## Decision

The existence of a reflective property is checked statically after resolving and typing the receiver. Each property has a set of owning categories or descriptors. If the receiver's static category does not guarantee membership in that set, the access is a static error.

Syntactically recognising the name after `~` does not grant the property. There is no dynamic name lookup, fallback to `empty` or implicit user metadata for an unsupported property. Narrowing that makes the receiver's category sufficiently precise may make valid an access that was previously not guaranteed.

For participant properties, the matrix is:

| Resolved subcategory | `~for` | `~on` | `~given` |
| --- | --- | --- | --- |
| `RuleKind.Boolean` | yes | no | yes |
| `RuleKind.Reactive` | no | yes | no |
| `RuleKind.Always` | no | yes | no |
| `ActionKind.Action` | yes | no | yes |
| `ActionKind.Subaction` | yes | no | yes |
| `look` | yes | no | yes |
| `message` | no | yes | no |
| any other declaration | no | no | no |

The matrix describes subcategory capability, not the concrete presence of the clause. When a property is supported and the optional clause was omitted from that declaration, the access is valid and returns `empty` with type `Participant [* unique ordered]`. When the clause is present, it returns its descriptors in signature order.

Therefore, this program reaches the superficial AST but contains a static error in reflective access:

```mud
thing A

rule InvalidForReflection {
    A~for == empty
}
```

By contrast, a compatible category may omit the clause and produce `empty`:

```mud
thing A

action Ping {
    then create A
}

rule PingHasNoForParticipants {
    Ping~for == empty
}
```

The availability rule also applies to the remaining reflective properties according to their contract's set of owners. A property whose result permits absence or an empty collection still distinguishes that absence from the property's non-existence. In particular, `Metadata` admits its intrinsic contract, including `~anchor`, `~path` and `~file`, but does not admit `~metadata`: D-094 defines it as a terminal descriptor.

## Phase consequences

### Parser and CST

They do not change. They must accept the postfix form whenever the name is syntactically valid. In particular, `for`, `on` and `given` remain admitted after `~` because they are hard keywords.

### Superficial AST

It retains `MetadataAccessExpr(receiver, metadata)` even when the access will prove semantically invalid. It does not have enough information to apply the matrix.

### Resolution and typing

They determine the receiver's static category, apply narrowing where available and select the property contract. If no compatible property exists for every receiver case still possible, they emit a static error. Only valid accesses reach elaboration, which determines their result type; the later mechanical representation is not yet fixed.

### Execution

It performs no dynamic lookup to rescue an invalid access. `empty` appears only as the value of a valid contract that permits it.

## Boundary cases

- `thing A; A~for` is invalid.
- An `action` without `for` has `ActionName~for == empty`.
- A Boolean rule without `given` has `RuleName~given == empty`.
- A reactive rule without `on` has `RuleName~on == empty`.
- `ActionName~on` is invalid even if the action has no participants.
- An overly broad static receiver must be narrowed before accessing a property not guaranteed by all its possible alternatives.

## Rejected alternatives

### All signature properties exist and inapplicable ones return `empty`

Rejected because it erases the distinction between a category that admits an optional clause and one that lacks the concept entirely.

### Reject during parsing based on receiver text

Rejected because the receiver is a general expression and its category is known only after resolution; tying the grammar to the textual name would break aliases, qualified references and narrowing.

## Verification

1. The EBNF continues to accept `for`, `on` and `given` as `metadata-name`.
2. `thing A; A~for` produces a superficial AST and then a static unsupported-property error.
3. A compatible-category declaration without a concrete clause returns `empty`.
4. `AssignableExpr` contains no metadata suffix.
5. Typing and elaboration accept only metadata accesses compatible with the resolved static category and determine their result type.
