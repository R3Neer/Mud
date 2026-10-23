---
title: Structural trait requirements and views
status: current
normative: true
depends-on:
  - "[[../10-names-and-anchors]]"
  - "[[../11-type-system]]"
  - "[[../15-fields-and-mutability]]"
  - "[[functional-families]]"
questions: []
decisions:
  - D-184
  - D-183
---

# Structural trait requirements and views

A trait declares minimum capabilities without constructing a nominal value or
requiring an implements declaration. It can type values, collection members and
generic bounds. Its own declaration has a canonical trait::path.Name anchor;
satisfaction adds no as/Specializes edge to the nominal graph.

```mud
trait Named { name: String }
trait Addable { + }
trait IntAddition { +: Int --> Int --> Int }
```

> [!rule] MUD-TRAIT-001 — Structural satisfaction
> Gamma |- T satisfies R holds when every requirement in R has an accessible,
> compatible effective witness in T and all required guarantees are proved.
> Stored, calculated and inherited fields may witness a read requirement. Extra
> fields are allowed. No sampled current field value, private-member leak,
> nominal conversion or new write permission can establish satisfaction.

## Fields, bounds and capabilities

A field requirement name: U requires a singular named readable field whose
complete result contract is included in U. U's omitted cardinality uses the
ordinary type-only [1] default; it is not a wildcard. A typed numeric domain is
a declared guarantee, not a predicate tested against the current payload.
Witness inclusion must hold throughout every admitted view/lifetime of the
structural view; a transient mutable-state coincidence cannot establish it.
Ordinary subtype inclusion and the fixed normative proof procedure apply.

An omitted domain/uniqueness/order/inner-mut requirement introduces no additional
restriction on that dimension beyond the written type/shape. Stronger candidates
are allowed. No order requirement grants ordered use; no authority requirement
grants mutable use. Bare ordered requires an observable sequence, not a particular
sort criterion. ordered by p requires the corresponding proved criterion;
an unrelated q is insufficient. unique by p implies whole-value unique only
under the existing supported equality premises. Distinct projected keys are not
interchangeable. Equality support remains necessary for any claimed uniqueness.

mut name: U additionally requires an accessible stored writable place with the
ordinary invariant writable contract and supplied replacement authority. A
calculated field or immutable alias component cannot witness that requirement.
Inner [mut] separately requires immediate-thing capability and cannot be invented
by trait satisfaction, narrowing or view construction. Read-only views of
mutable fields do not grant replacement. Operator-valued fields remain pure.

Trait parameters reuse ordinary finite static generic declarations/application
contracts. Substitution precedes requirement inclusion; generic use does not
introduce dynamic type construction. There is no additional intersection,
exclusion or descriptor-driven union construction syntax. Ordinary | keeps its
established union meaning. A trait body cannot supply default implementations
or a new lifecycle/activation mechanism.

## Operator requirements

The name of an operator field is its symbol, without parentheses. A bare +
requires at least one accessible admitted + signature involving the candidate
owner/type. It does not imply T+T->T, binary instead of unary, commutativity or
compatibility between two different Addable values. A typed requirement demands
the specified family/signature contract. Multiple overloads form one constrained
operator field family; one arbitrary overload is not chosen to witness all uses.
Every actual operation still needs a valid uniquely determined static signature. Builtin pure capabilities can witness a requirement without an alias declaration; this does not make equality, comparisons or composition alias-overloadable. A === capability compares Type contracts, never ordinary numeric/string payloads.

Ordinary field requirements have unique names. Operator requirements group by
symbol into a family: every distinct typed signature requirement must be met;
they are not alternatives from which a witness may choose only one. A bare
symbol adds only its capability-existence requirement and contributes no
additional signature when a typed requirement already ensures that existence.
Repeated identical normalized operator requirements are redundant set entries, not new
overloads or new nominal members. Normalization sorts requirement names and
signature contracts; declaration order does not affect trait equality.

An operator family can be projected using Type.+ or an accessible value.+;
projection is not implicit partial application of that value. Operator-reference
(+) denotes the visible family, independently of this bare field-name syntax.
Trait witnesses retain the ordinary owner, purity, domain, visibility and
termination requirements. They do not synthesize an inverse signature.

## Value views, tests and identity

A value of a trait contract retains its actual nominal alias/thing/family
identity. The visible static contract exposes required capabilities; additional
fields require ordinary narrowing. A heterogeneous collection can retain a trait
member contract without erasing its actual identities. No implicit alias
construction occurs. A view does not manufacture value equality or total order;
all admitted alternatives must support a requested comparison under the ordinary
functional-value and thing-identity rules. Projection lifetime/authority and public-boundary checks
remain in force; trait views cannot launder hidden schema or private types.
A private field is a witness only where its access is independently authorized.
Reflection cannot recover inaccessible concrete schema from an exported view.

value is Trait checks structural satisfaction. If all known static alternatives
satisfy it, the test is true; if all refute it, false. A finite closed set of
known nominal alternatives may be tested at execution and narrowed by its
checked schema cases. This is not operator overload dispatch based on runtime
type. Unproved contract inclusion is not repaired by testing a field's current
value. Use a supported proof/constraint; missing mandatory evidence is a static
diagnostic. iis Trait is invalid because a trait is not an exact nominal identity.

> [!rule] MUD-TRAIT-002 — Requirement contract equality
> R === S compares normalized requirement contracts, independent of trait names
> and requirement declaration order. Retain member names, complete types,
> domains, cardinalities, by criteria, read/write/inner authority and operator
> signature relations. Alpha-normalize bound variables; do not prove arbitrary
> semantic equivalence of predicates. Satisfaction is not equality.

A read requirement does not encode whether its witness is stored or calculated;
that implementation distinction does not enter equality of such requirements.
A writable requirement is distinct. Bare + and a particular typed + requirement
are distinct contracts. A trait and a nominal alias do not become === merely
because that alias satisfies it. Existing normalized finite graph equality
handles admitted recursive requirement graphs; no proof follows from samples.

The fixed language catalogue includes TypeKind.Trait for a public structural
trait contract and DeclarationKind.Trait for its declaration descriptor. The
descriptor itself remains DeclarationDescriptor. Applied traits normalize their
requirements structurally; nominal aliases wrapping a view retain Alias. These
are fixed catalogue entries, not user-extensible type kinds.
