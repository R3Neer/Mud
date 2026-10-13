---
title: Closed value families
tags:
  - mud/specification
status: current
normative: true
depends-on:
  - "[[10-names-and-anchors]]"
  - "[[11-type-system]]"
  - "[[15-fields-and-mutability]]"
  - "[[21-expressions]]"
questions: []
decisions:
  - D-038
  - D-064
  - D-066
  - D-076
  - D-087
  - D-091
  - D-092
  - D-100
  - D-101
  - D-102
  - D-105
  - D-112
  - D-114
  - D-122
  - D-157
---

# 14. Closed value families

## Family identity and members

> [!definition] Closed family
> `family F { ... }` declares a finite nominal type with exactly its written
> members. A member is an immutable nominal value, not a thing identity or a
> runtime payload constructor. `ordered family` additionally supplies member
> comparison by declaration position.

```mud
ordered family Severity { Low, Medium, High }
level: Severity = Medium
```

Let F be a resolved family, A its exact static type arguments (empty for a
nongeneric family), and M(F)=(m1,...,mn) its member declaration sequence. Its
values are Member(F,A,mi). Equality requires the same constructor, exact
arguments and member identity. Associated data, presentation metadata and the
place holding the value do not affect that equality.

> [!rule] MUD-FAMILY-001 — Closed nominal membership
> A family value must name one declared member of the exact applied family.
> Families cannot specialise or inherit families. Members have no create/destroy
> lifecycle and cannot use thing ancestry queries to acquire membership.

Families remain opaque under structural type equality: identical member lists
in different families do not make their types equal. Expected family context
can resolve an unqualified member, but cannot choose between ambiguous contexts.
No type selects a default member.

The syntax is [[grammar/mud.ebnf]], with family/member/data nodes in
[[syntax/mud-surface-ast.asdl]]. There is no implicit open extension list or runtime
operation to add members. Model changes require a new elaboration under the
applicable version, not a world effect.

## Static generic applications

A family may declare `with` parameters under [[11-type-system]]. The complete
uniform data schema is checked using the bounds and then substituted for each
admitted application. Each application has exact nominal type identity,
including phantom arguments. Members retain source declaration anchors; applied
types differ even when their source anchors agree. For example `Cat Slot.Empty`
and `Dog Slot.Empty` are members of different applications of
`family Slot with T { Empty, Full }`.

Applications create no extra declaration, member anchor, metadata owner or
runtime payload slot. A member cannot be called with a runtime T payload as if
it were a variant constructor. Parameter variance must be proved from the full
contract; mixed, phantom or unproved positions remain invariant. Finite generic
application closure is an independent admission premise, not a consequence of
having finitely many members per application.

## Uniform associated data

Schema declarations appear before members in the family body. Each datum has
one name and one complete value contract shared by all members. Stored data is
immutable and may have an explicit schema default. A member body may assign a
different value to an existing stored datum; it cannot declare another datum,
change its type/domain/shape or assign computed data.

For member m and stored datum d, define Init(m,d) as its explicit member
assignment if present, otherwise the explicit schema default. If neither
exists, the member is invalid. Evaluate Init(m,d) statically and check the result
against d's complete contract. A type annotation supplies no fallback value.
Short expressions and full pure ValueBlocks use the same admission/recovery
contract as other static value owners.

> [!rule] MUD-FAMILY-002 — Complete immutable member data
> Every member must supply a valid value for each stored datum by explicit
> assignment or explicit schema default. All computed data must have a uniquely
> inferred or explicitly checked contract and an acyclic dependency graph.
> Member override bodies must not change the uniform schema.

Computed data uses `name [derived-form] := value-body`. The full derived form
may specify a type, domain, cardinality, uniqueness and order. It is pure,
unstored and nonassignable, and cannot manufacture `[mut]` or other authority.
Its local domain/shape transformations follow [[15-fields-and-mutability]].

Let C be the computed datum declarations and let E contain d-to-e when d's
computation depends on computed datum e. E must be acyclic; forward references
are resolved before ordering. Once stored values are admitted for a member,
evaluate computed data in dependency order, admitting every produced value
against its complete contract. Written declaration order is not a dependency
resolution algorithm. Mutable runtime-world reads are not static evaluation.

Write Family(F,A) admitted when the application is well formed, all member
identities resolve, every Init exists and succeeds, the computed dependency
graph is acyclic, and every computed result satisfies its contract. This
judgement describes required evidence; finite witnesses are not a universal
solver for arbitrary source predicates.

## Ordering and enumeration

Canonical enumeration is the finite declaration sequence M(F). This sequence
exists for both ordered and unordered families. Semantic `<`, `<=`, `>` and `>=`
between members require `ordered family` and compare their declaration positions;
enumeration order alone does not grant those operators to an unordered family.

A collection of members may carry `ordered by path` when the selected stable
associated value has total semantic order. The path starts at each member;
arbitrary inline key expressions must first be named as computed data. Key
ordering changes the collection's primary order and does not change the family's
member comparison. Equal keys preserve stable occurrence provenance. Repeated
members retain multiplicity unless the collection's uniqueness contract removes
it. Enumeration, `ordered by`, and member comparison are three separate contracts.

## Descriptors and presentation

Each family and member has its canonical descriptor/anchor under the family
category. Stored/computed associated data is a single schema `Field` descriptor
with `FieldKind.Stored` or `FieldKind.Calculated` and subordinate anchor
`family::<qualified-family>::<datum>`. `~fields` and `~declaredFields` expose
those declarations under the ordinary visibility rules.

Access `member.datum` produces a value, not a new descriptor per member.
A member assignment has no public anchor or metadata body. A datum's immediate
metadata-only body belongs to its schema descriptor. Execution cannot write
postfix `~` properties. Configured `~name` is presentation and does not change
member identity, equality or ordering; Text interpolation uses that presentation.
The projected type category is Family even for applied families and members.

## Examples and counterexamples

```mud
ordered family Terrain {
    movementCost: Nat = 1
    passable: Bool = true
    costly := movementCost >= 3

    Plain,
    Forest { movementCost = 2 },
    Mountain { movementCost = 4 },
    Water { movementCost = 0; passable = false }
}
```

Representative example: Mountain.costly is true and Plain.costly is false.
Their stored data follows the uniform schema; costly is evaluated statically
per member. Sorting a collection by movementCost does not redefine Terrain's
member order.

```mud
family Missing { code: Nat; One }       # invalid: no code value
family Override {
    score: Nat = 0
    doubled := score * 2
    One { doubled = 4 }                # invalid: computed datum assignment
}
family Cycle {
    first := second
    second := first
    One                                # invalid: computed dependency cycle
}
```

`create Terrain.Mountain` and adding an undeclared member datum are invalid.
Two different family declarations both containing `One` do not share a member.
An unordered family's enumeration does not permit `One < Two`.

## Conformance evidence

[[types/typing-cases.yaml]] includes applied-family phantom identity and
payload-constructor rejection; declaration cases cover missing values, computed
override rejection, ordering and schema descriptor identity.
[[types/test_declaration_witnesses.py]] checks finite supplied member/data
certificates, order distinction and declaration-origin sharing. No parser,
compiler, runtime member construction or general static evaluator is implemented.
