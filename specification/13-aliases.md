---
title: Nominal aliases and structural values
tags:
  - mud/specification
status: proposed
normative: true
depends-on:
  - "[[10-names-and-anchors]]"
  - "[[11-type-system]]"
  - "[[15-fields-and-mutability]]"
  - "[[21-expressions]]"
questions: []
decisions:
  - D-167
  - D-168
  - D-162
  - D-031
  - D-032
  - D-033
  - D-074
  - D-084
  - D-086
  - D-087
  - D-098
  - D-103
  - D-112
  - D-113
  - D-114
  - D-115
  - D-116
  - D-117
  - D-122
  - D-135
  - D-146
  - D-149
  - D-153
  - D-155
  - D-156
  - D-157
---

# 13. Nominal aliases and structural values

## Scope and forms

Aliases introduce nominal immutable value contracts, independently of thing
identity and activity. Their declared type form may represent a basic type,
collection, dictionary, union or an ordered structural tuple. A representation
definition `alias A := Type` is static type definition, not runtime calculation.
An ordered structural body declares stored components and optional pure derived
fields. Component defaults do not remove components from the representation.

```mud
alias PlayerName := Text
alias Vector2 { x: Num; y: Num }
position: Vector2 = (1, 2)
```

> [!rule] MUD-ALIAS-001 — Nominal immutable values
> An alias introduces its own nominal type even when its normalized
> representation equals another type's representation. Its values are finite
> immutable structural values. They have no activatable world identity, own
> mutable payload or create/destroy lifecycle.

An abstract alias may be structural or have a structural effective inherited
representation. It types concrete descendant values but cannot be directly
constructed or cast into as a new exact value. A root without representation or
structural definition is invalid. A descendant may omit its local definition
only when the inherited effective representation is uniquely compatible.
Grammar and source constructors are [[grammar/mud.ebnf]] and
[[syntax/mud-surface-ast.asdl]].

## Components, defaults and derived fields

Let S(A)=((n1,t1),...,(nk,tk)) be the effective stored component sequence of
structural alias A. Every value contains those k components in that order.
Each component has a complete type/domain/collection contract and optionally
an explicit statically evaluable default. Outer `mut` is not permitted on an
alias component. Inner `[mut]` is an immediate-thing capability governed by
[[15-fields-and-mutability]], not mutable alias storage or implicit deep authority.

A derived field uses the ordinary complete derived form and a pure value body.
It has no stored component position, cannot be assigned, and does not enter
stored-content equality as a separately cached value. Domain/shape coercion
follows the field rules; authority can be preserved where identity permits it
but cannot be manufactured. Dependences are checked under the applicable pure
body and acyclicity/termination contracts.

## Contextual construction and explicit conversion

> [!rule] MUD-ALIAS-002 — Construction does not convert typed values
> An untyped literal may construct a concrete alias when its expected alias
> contract is unique. An already typed expression retains its nominal identity
> and requires an admitted explicit `to` conversion to change it.

A positional structural construction supplies all k stored components.
A named construction may omit only components with explicit effective defaults.
Named components retain declaration-relative order; unknown, duplicate or
reordered names and mixed positional/named forms are static errors. Missing
defaults are not inferred from types. Every supplied/default value must be
admitted against its complete component contract before producing the alias.

Using the checking judgement of [[11-type-system]], define Construct(A,L)
when A is concrete, literal L matches S(A) by the positional/named rules,
all missing components have defaults, and every resulting component check
succeeds with its required obligations. Its result has exact nominal type A.
An abstract A fails the first premise. A unique context is necessary even when
several nominal aliases have matching component arity.

Nominal `to` requires normalized representation compatibility, preserves the
underlying content and changes its exact nominal type, validating the destination
restrictions. It does not perform quantitative rounding or arbitrary conversion
between things, text and numbers. Representation compatibility checks component
names/order, underlying forms, cardinality, dictionary/nesting and structural
modifiers; destination domains are separately validated. This conversion relation
is distinct from exact alias-erasing Type equality `===`, which compares full
normalized effective contracts including domains and authority.

## Ancestry, origins and refinements

Alias `as` edges form their own acyclic nominal graph; the closure used by `is`
is reflexive and transitive. Written predecessor order supplies no priority.
A descendant must refine all predecessor representations simultaneously, not
choose an alternative from their union. Cross-part ancestry requires direct
`uses` and contract-visible type closure, preserving ordinary substitutability.

> [!rule] MUD-ALIAS-003 — All-ancestor refinement and origin sharing
> Gather inherited members by original declaration identity. A diamond counts
> one origin once. Equivalent independent contributions may merge; distinct
> compatible contracts require an explicit common refinement. Incompatible
> categories cannot be repaired by ancestor ordering.

The effective stored component/default refinement must satisfy every inherited
contract. A descendant may replace an inherited explicit default with a valid
more specific one. A derived field from one origin retains its defining expression
while an allowed refinement strengthens its contract. Independent same-name
derived fields with different expressions require a new explicit derived
definition satisfying all inherited contracts. Bare structural matching cannot
grant these nominal members; acquisition through context or `to` is required.

## Recursive and generic types

Representation recursion uses finite normalized graph references, not infinite
unfolding or cyclic value identity. Transparent cycles without a productive
constructor are invalid, as are mandatory component cycles with no finite exit.
An empty-admitting recursive collection may supply a finite terminating value.
Abstract alias inhabitation uses productive concrete descendants. Explicit
defaults must themselves be finite valid values. Productivity and compatibility
are separate judgements; visiting a recursive graph pair proves neither.

Aliases may declare static `with` parameters. Bounds, exact application identity,
inferred conservative variance and proven finite application closure are
[[11-type-system]] contracts. Application creates no new declaration or anchor.
An immutable output parameter can be covariant only with the required proof;
domain, callable-input and capability uses can force invariance. A phantom or
unproved parameter remains invariant. Recursive finite values do not establish
finite generic application closure or finite exhaustive enumeration.

Domain/source finiteness and application closure follow [[types/finite-static-certification]].
Pure operator bodies use [[types/termination-certification]], including certified
lexicographic/phase and synthesized affine measures. Required proofs remain
admission premises; implementation-specific admission is not permitted.

## Equality, order and enumeration

Alias equality requires exact effective nominal identity and equal stored
content. A value viewed through a predecessor retains its exact identity;
metadata, component defaults and derived caches cannot change equality. `!=`
negates equality. Different aliases sharing a representation require explicit
conversion before ordinary nominal comparison.

A representation alias inherits the representation's order when available.
A structural alias has lexicographic order by stored component sequence when
every component supplies the required semantic order. Equality needs no ordering but must be supported by all compared stored
contents under MUD-TYPE-040 in [[11-type-system]]; functional payload cannot
acquire equality from alias nominality. Comparison can provide expected nominal context to an untyped
literal on either side; it cannot silently convert a typed variable or select
between two bare untyped structural literals.

Exhaustive alias enumeration requires a proven finite canonical enumeration
of the complete admitted domain. A structural product enumerates component
domains lexicographically, with the last component varying fastest. With finite
component enumerations E1,...,Ek, its unfiltered product size is their size
product; further domain restrictions remain required. Finite individual values,
finite type graphs and orderability do not prove a finite enumerable value space.

## Stored reconstruction and write-back

> [!rule] MUD-ALIAS-004 — Reconstruction preserves immutability
> A partial write may traverse stored alias components and exact-dictionary
> indices only when it resolves unambiguously back to a writable root with the
> required authority. Reconstruct containing values with unchanged exact
> nominality and unchanged other stored components; do not reapply defaults.

Derived fields are recomputed from the reconstructed value and are not write-back
targets. An ordinary immutable local holding an alias read from storage has no
reverse link to that place. Inner `[mut]` cannot replace outer mutability.
At an intermediate missing exact dictionary key, partial write-back supplies
no change: it neither inserts a default alias nor produces an error merely for
absence. Direct whole-association assignment retains its ordinary insertion
contract. Leaf calculation or admission faults still use ordinary error handling.
Sequential/private and concurrent semantic-destination contracts are
[[28-effects]]; reconstruction does not reduce all component effects to conflicting
whole-root replacements.

Pure recursive bodies retain their ordinary static result contract. [[types/termination-certification]] supplies their ranking search and evidence; it does not infer an ambiguous result, introduce nominal types or bypass independent owner-specific acyclicity.

## Owned operators and reflection

Only the closed unary/binary symbol set in [[21-expressions#Alias-owned operator signatures]]
is overloadable. A declaration belongs to its alias and at least one operand
must be that applied alias type. Bare operands imply that type; annotated operands
are grouped. The form is `a * (factor: Num): Vector2 := value-body`, with optional
result annotation. Owner-first tuple-result inference is confined to this context;
other operand ambiguity requires an explicit result contract.

Each declaration supplies only its written ordered signature. No reverse
signature, equality or order overload, algebraic privilege from metadata, or
compiler-proved commutativity is introduced. Selection uses complete static
operand contracts and unique strict specificity; equal/incomparable declarations
are ambiguous. Inheritance retains original owner, body and result. Every remaining
union alternative pair must select; expected results and runtime subtypes do not
repair ambiguity. Direct signatures precede builtins and restricted arithmetic
lifting; errors never trigger signature fallback. Derived compound updates require
an assignable destination and storable result and produce absolute replacements
for user operators. `%=` is unavailable.

The complete canonical identity and reflective schema are
[[names/operator-contract-identity]]. Alias `~operators` and `~declaredOperators`
preserve origins and ordinary visibility. Component and derived-field metadata
describes their schema descriptors, not payload copies. TypeKind projects aliases
to Alias regardless of their representation. Nominal HIR retains source origins,
operand scopes and references; inferred signatures, typed graph encodings and
write-back destinations belong to later phases.

## Examples and counterexamples

```mud
alias Pagination { page: Nat = 1; size: Nat = 20 }
p: Pagination = (size = 30)       # constructs page=1, size=30
alias PlayerName := Text
name: PlayerName = "Ada"         # contextual literal construction
raw: Text = "Ada"
converted: PlayerName = raw to PlayerName
alias Tree { children: Tree [*] = empty }
```

```mud
bad: Pagination = (2)            # invalid: incomplete unnamed form
badName: PlayerName = raw        # invalid: typed Text does not become alias
alias Impossible { next: Impossible } # invalid: no finite value
alias A := B
alias B := A                     # invalid: transparent cycle
```

Inside an action with authority to update `Piece.square`, writing
`Piece.square.file = C` reconstructs its stored Square value. Writing
`square.file = C` after `square := Piece.square` is invalid because the binding
has no writable root. Two aliases both represented by Text do not compare as
the same nominal values.

## Conformance evidence

[[types/typing-cases.yaml]] and its finite derivation checker cover contextual
construction, required/default components, productive/transparent cycles,
exact graph equality, variance, alias/operator identity and signature selection.
[[types/test_operator_identity_witnesses.py]] checks canonical identity certificates;
[[types/test_declaration_witnesses.py]] distinguishes origins and ancestry.
Write-back and missing-key effect certificates are in [[effects/README]].
These are scoped evidence, not a complete source compiler or normative proof solver.
