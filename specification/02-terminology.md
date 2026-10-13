---
title: Terminology
aliases:
  - MUD Regulatory Glossary
tags:
  - mud/specification
status: proposed
normative: true
depends-on:
  - "[[01-scope-and-conformance]]"
  - "[[04-mathematical-model]]"
  - "[[10-names-and-anchors]]"
  - "[[11-type-system]]"
questions: []
decisions:
  - D-025
  - D-055
  - D-085
  - D-086
  - D-096
  - D-110
  - D-118
  - D-119
  - D-123
  - D-126
  - D-131
  - D-133
  - D-140
  - D-157
  - D-159
  - D-162
  - D-165
---

# 02. Terminology

## Use of terms

This glossary fixes the vocabulary shared by the chapters. The linked construct
chapters define the corresponding judgements and admission requirements. A
semantic object named here does not introduce a source keyword, public type,
serialization layout or protocol.

> [!definition] Declaration and occurrence
> A declaration is a canonical programme definition. An occurrence is a
> particular use, evaluation or event associated with a definition. Equal
> results do not identify distinct occurrences.

## Programme, source and identity

| Term | Meaning |
| --- | --- |
| Programme | The resolved collection of canonical definitions and their static contracts under one effective language target. |
| World | The state of a programme, including activation, owned storage and its effective projection. A programme definition and its changing world are distinct. |
| Part | The source/access unit assigned by the nearest ancestor mud.part manifest. A nested manifest opens another part. |
| Source file | A .mud text containing source declarations, with its own nominal file identity and optional whole-file part-only restriction. |
| Manifest | A configuration document describing a source or dependency boundary. The minimal part manifest and the planned world descriptor have different responsibilities. |
| World descriptor | The planned mud.world.toml configuration boundary; this term specifies no descriptor schema or dependency-resolution algorithm. |
| Distribution | A dependency/distribution unit to be mapped to parts by the world/dependency contract; it is not a using import. |
| Path | A qualified nominal location derived under source/name rules, distinct from an operating-system path value. |
| Name | A source identifier or qualified name used by lookup. |
| Symbol | A resolved nominal entity associated with a declaration or local binding in a scope. |
| Anchor | A canonical category-qualified public declaration identifier, formed by the nominal rules. A display label does not determine it. |
| Visibility | Whether the declaration/type contract can be referenced from an access context. Visibility alone does not grant write or host-endpoint authority. |
| Contract type frontier | The finite transitive type graph required to represent and use a visible public contract, subject to privacy. |

Canonical contracts: [[05-source-text]], [[10-names-and-anchors]] and
[[26-public-boundary]]. Descriptor and dependency design belongs to chapter 06;
the preceding terms do not settle that design.

## Things, lifecycle and state

| Term | Meaning |
| --- | --- |
| Thing | A canonical nominal identity, rather than a class with separately created instances. Builtin Thing is the abstract nominal root. |
| Concrete thing | One particular thing with independently owned materialised state when active. It may also be an ancestor. |
| Abstract thing | An identity contributing ancestry/schema without its own concrete stored payload. |
| Specialisation | The acyclic nominal descendant-to-predecessor relation introduced by as and its closure. It inherits contracts, not an ancestor's mutable state. |
| Canonical identity | The identity of the resolved definition, retained across inactivity, destruction and reactivation. |
| Activity | Explicit lifecycle availability of a thing or rule definition. |
| Materialisation | An active concrete owner's own stored payload. |
| Generation | The semantic distinction between successive materialisations of one canonical identity. It is not a new source name. |
| Owned storage | Stored values belonging to a concrete owner and materialisation generation. |
| Effective projection | Definitions and data currently usable after activity and hard-dependency restrictions. |
| Suspension | Unavailability caused by an inactive hard dependency, distinct from explicit inactivity or destruction of independently owned storage. |
| Field | A declared stored or calculated collection-valued component of its owner. Singleton is a collection shape. |
| Relation | A field/source relating values or identities; it introduces no implicit extra ownership or write capability. |
| State view | The coherent confirmed, snapshot or private-delta projection supplied to one computation. |
| Snapshot | A fixed semantic view for an applicable observation/evaluation step, without a required physical copy. |

Canonical contracts: [[04-mathematical-model]], [[12-things]] and
[[15-fields-and-mutability]].

## Values, types and domains

| Term | Meaning |
| --- | --- |
| Value | Data satisfying an admitted contract. Thing identity, immutable structural data and descriptors have distinct contracts. |
| Type | A static contract describing admitted values, with its normalized nominal/structural form and shape. A Type descriptor is its reflective value. |
| Nominal alias | An immutable value type with its own identity and an admitted representation or component schema. It is not an activatable thing. |
| Tuple | An anonymous positional or named structural value/type. Public TypeKind.Tuple does not rename the internal product notation. |
| Family | A closed nominal value family whose members have canonical member identities and uniform associated-data contracts. |
| Collection | A finite value with member contract, cardinality, multiplicity and applicable uniqueness/order guarantees. An unbounded admitted cardinality does not create an infinite value. |
| Cardinality | The admitted number of collection occurrences, including lower/upper bounds. |
| Occurrence multiplicity | How many occurrences a collection retains, independently of whether member values compare equal. |
| Uniqueness | The applicable guarantee that compared members or projected keys are distinct under supported equality. |
| Semantic order | An established order usable by source-level operations, distinct from an internal hash/storage enumeration. |
| Empty | The zero-occurrence collection value. A singleton containing an empty collection is not empty. |
| Dictionary | An exact finite key-to-value collection of associations. Public TypeKind.Dictionary refers to this form. |
| Association | One exact-dictionary key/value entry; traversal may project it as a pair without making it an ordinary tuple value. |
| Functional dictionary | A finite branch policy over its declared input contract, with an optional fallback and an established branch-selection mode. Its definition is finite even when the input domain is not enumerable. |
| Branch | A selector/result clause of a functional dictionary, with local branch identity rather than a public declaration anchor. |
| Selector | The exact-key or predicate input criterion of a functional branch. |
| Fallback | The functional result used when the selected mode finds no accepted branch. |
| Union | The normalized static alternatives admitted by a type contract, without implicit nominal conversion. |
| Equality | Supported value comparison. It is distinct from nominal membership, exact Type comparison and equality of definitions. Functional-policy values have no value equality. |
| Domain | An admitted set/constraint of values over a type; membership and enumeration are separate properties. |
| Interval | A bound-delimited domain with its endpoint openness and admitted numeric/ordered contract. |
| Finiteness | Having finitely many admitted occurrences/members in the relevant scope. It does not alone supply an enumeration procedure. |
| Enumerability | Having an admitted source traversal over the relevant domain/collection under its required finite evidence. |
| Magnitude | A nominal numeric quantity with an underlying representation and dimension/unit contracts. |
| Point magnitude | A coordinate over a linear magnitude, with its point/difference and optional cyclic-domain contracts. |
| Unit | A declared spelling and exact conversion relationship for an admitted magnitude. A reflected unit descriptor is not a first-class unit expression. |

Canonical contracts: [[11-type-system]], [[13-aliases]], [[14-closed-families]],
[[16-collections]], [[17-dictionaries]], [[18-domains-and-intervals]] and
[[19-magnitudes]].

## Binding, capabilities and computation

| Term | Meaning |
| --- | --- |
| Participant | A value bound to a declared role under its type/domain/shape contract. |
| Role | A named for/on signature slot with its independent capability contract. |
| Binding | A mapping of declared names to admitted values/identities. Automatic on bindings satisfy the entire joint header. |
| For | Caller-supplied participant signature. |
| On | Automatically related participant signature, including joint related sources and refinements. |
| Given | A read-only supplied argument with an optional explicit closed static default. |
| Place | An admitted assignable root/path with its destination contract and authority. |
| Outer mutability | Permission to replace or change a place's collection membership. |
| Inner capability | Permission over immediate members, as supplied by [mut]; it does not imply outer or arbitrary deep mutability. |
| Stored binding | A value captured at its admitted initialization/evaluation site. |
| Derived binding | A registered pure definition read in its applicable coherent view, without an independently writable root. |
| Expression block | A pure singleton-result computation under its expected contract. |
| Value block | A value-producing computation with the local capabilities supplied by its owning context. |
| Effect block | A computation allowed to perform world effects within its supplied authority. |
| Normal | The metalanguage outcome carrying a block's normal result. |
| Fault | The metalanguage outcome carrying nonempty Error occurrences, with no normal result. |
| Erasure | Structural omission of unavailable Boolean syntax under pruning, rather than a third Bool value. |
| Error channel | A block's error-occurrence channel; constructing an Error value does not enter it. |
| Recovery | Error-only otherwise handling after the protected failed work is rolled back. |
| Proof obligation | Evidence required by a static judgement, separate from a runtime check expressly admitted by that contract. |

Canonical contracts: [[15-fields-and-mutability]], [[20-blocks-and-recovery]],
[[21-expressions]] and [[22-quantifiers-and-iteration]].

## Rules and public operations

| Term | Meaning |
| --- | --- |
| Boolean rule | A pure callable query with for/given inputs and singleton Bool result. |
| Reactive rule | An activatable declaration with automatic on bindings, when observation, optional if guard and authorised then consequences. |
| Always rule | An activatable pure invariant checked for its effective automatic bindings at mandatory consolidated checkpoints. |
| Condition | An ordinary pure Bool computation in its applicable context. |
| Constraint | A contract restricting admission of values, bindings or states. |
| Invariant | A condition required at the checkpoints prescribed by its owning contract. |
| Trigger | An internal temporal/causal match qualification in when, not a storable public type. |
| Observation episode | Continuing temporal observation under the same rule activation and concrete participant materialisations. |
| Action | A declared effect operation whose sole result is ActionReply. |
| Sub operation | An action/look/message category usable internally under its contract, without a production host endpoint. |
| Look | A pure query producing one immutable value of its declaration's statically determined nominal result type. |
| Message | A declarative causal source producing distinct occurrences with payload frozen in their birth views. It is not a source-level emit instruction. |
| Produced type | The static nominal result/payload type belonging to the producer declaration and, where admitted, its exact generic arguments. |
| Endpoint | A visible shared normal operation admitted at the production host boundary. Widening a sub descriptor does not create one. |
| Request | A supplied invocation intent at an admitted operation boundary, separate from the declaration and from actual invocation identity. |
| Invocation identity | The identity of one actual invocation instance, distinct from callable/declaration identity. |
| Causal owner | The invocation to which causal work is attributed; jointly caused work belongs to its common enclosing invocation. Wave membership does not itself choose that owner. |
| Root | The initial direct effect batch in an admitted resolution, distinct from its later reactive waves and from individual nested calls. |
| Wave | A consolidated reactive batch over the supplied snapshot/bindings; one wave may contain work owned by several invocations. |
| Resolution | The tentative evolution and validation of requested work through its applicable root/waves and completion boundaries. |
| Effect | An authorised change or operation in the current private execution view. |
| Conflict | Incompatible contributions under the established effect consolidation contract, rather than an arbitrary sequential last-writer policy. |
| Reality level | A relative confirmation/isolation boundary for tentative work. |
| Alternative branch | Isolated alternative evolution, including imagine, whose disposition is separate from ordinary nested-call incorporation. |
| Relative confirmation | Successful incorporation into the containing level; it need not imply stable exterior confirmation. |
| Confirmed world | The stable incorporated state available to ordinary host looks. |

Canonical contracts: [[23-boolean-rules]], [[24-reactive-rules]],
[[25-always-rules]], [[26-public-boundary]] and [[28-effects]]. These terms retain
the accepted interfaces; they supply no causal discovery/completion algorithm.

## Replies, tests and external evidence

| Term | Meaning |
| --- | --- |
| ActionReply | The nominal union of Success, Refusal and Errors, returned exactly once by every action/subaction. |
| Success | Successful action completion at its applicable level, distinct from an arbitrary domain result. |
| Refusal | An admitted request that fails an argument/condition/invariant contract, with its required reason, origin and applicable trace. It is not Error. |
| Error | An immutable diagnostic value with reason, origin and optional finite cause; an Error occurrence enters a computing-error channel. |
| Errors | A nominal nonempty Error collection, including the action reply alternative. |
| BoolCheck | Immutable evidence of the actually evaluated final condition, preserving short circuit and unevaluated branches without reevaluation. |
| Diagnostic provenance | Canonical origin/argument references in the established diagnostic components, with no additional invocation/state/private-schema permission. |
| Test | A declaration executed in a fresh isolated world and discarded on completion, outside production endpoints. |
| Assertion | A test check under its protected pure result/error contract. |
| Diagnostic | Evidence explaining an admission failure, refusal, computing error or test result; its required schema belongs to its owning contract. |
| Textual patch | Readable incorporated changes with a reproduction contract; this term defines no pending patch schema or reply access API. |
| Reproduction | Applying/checking an incorporated change description under its applicable compatibility contract. |
| Ticket | A host-only observation with Waiting, Kept or Dropped status. It is not a Mud source value/type. |
| Waiting | Published provisional evidence not yet incorporated into the stable root or disposed. |
| Kept | Terminal ticket state after surviving stable-root incorporation. |
| Dropped | Terminal ticket state after disposal of a containing scope. |

Canonical contracts: [[20-blocks-and-recovery]], [[26-public-boundary]],
[[28-effects]] and the foundation in [[04-mathematical-model]]. Patch, generalized
host-observation and foreign protocols retain their separately delimited scopes.
Naming these objects neither specifies those protocols nor claims their completion.
