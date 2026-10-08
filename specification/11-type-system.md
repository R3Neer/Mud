---
title: Type system
aliases:
  - Static types of MUD
tags:
  - mud/specification
status: proposed
normative: true
depends-on:
  - "[[03-notation]]"
  - "[[10-names-and-anchors]]"
questions:
  - Q-073
  - Q-060
decisions:
  - D-144
  - D-140
  - D-137
  - D-136
  - D-135
  - D-134
  - D-132
  - D-131
  - D-014
  - D-018
  - D-028
  - D-030
  - D-031
  - D-032
  - D-034
  - D-039
  - D-040
  - D-074
  - D-084
  - D-086
  - D-087
  - D-092
  - D-095
  - D-096
  - D-103
  - D-112
  - D-113
  - D-114
  - D-115
  - D-116
  - D-118
  - D-122
  - D-037
  - D-085
  - D-088
  - D-127
  - D-129
  - D-130
---

# 11. Type system

## Scope and dependencies

This chapter defines well-formed types, value identity, representation compatibility, subtyping, contextual checking and inference. [[15-fields-and-mutability]] defines place authority and effect obligations; [[21-expressions]] assigns these contracts to expressions and blocks. These three chapters describe a static language contract, not a compiler data layout or a causal evaluator.

Numeric signatures and dimensional admission follow [[21-expressions#4. Numeric, dimensional and Boolean operators]]. A combination lacking a defined signature cannot be accepted by inventing a promotion. The public TypeKind core categories are specified below; their complete extensibility and projection contract remains Q-060.

## 1. Environments and judgements

Let $P$ be a linked, nominally resolved programme. Its finite nominal catalogue is $\Sigma$. It records declaration identity, category, ancestry, schema origins, callable signatures, part visibility and declared type expressions. $\Gamma$ maps visible local names to value contracts and place information. $\Phi$ is the finite set of facts established at the programme point by contracts and control-flow narrowing. $W$ is a well-formed world projection used only to interpret state-dependent domains.

An elaborated value contract $\tau$ consists of an element form, its domain and its outer collection specification. A place's outer mutability is separate. Let $\mathcal V$ be the universe of finite MUD values and $\llbracket\tau\rrbracket_W\subseteq\mathcal V$ the values satisfying that complete contract in $W$. A normal result must belong to this set; a computing error supplies no normal result.

| Judgement | Meaning |
| --- | --- |
| $\Sigma\vdash\tau\ \mathsf{wf}$ | The type expression has a well-formed finite graph. |
| $\Sigma;\Phi\vdash\tau\preceq\sigma$ | Every source value/guarantee meets the target without a runtime test, nominal cast or manufactured authority. |
| $\Sigma\vdash\tau\cong_R\sigma$ | Representations have the same normalised shape for explicit nominal conversion. |
| $\Gamma;\Sigma;\Phi\vdash e\Rightarrow\tau$ | Synthesis obtains a type without an expected type. |
| $\Gamma;\Sigma;\Phi\vdash e\Leftarrow\sigma\triangleright O$ | Checking against the expected contract produces obligations $O$. |
| $\Phi\vdash p$ | The required proposition has a finite, valid proof from the available facts. |

The unadorned $\Gamma;\Sigma\vdash e:\tau$ abbreviates a successful synthesis judgement after discharging its mandatory static obligations. Checking is distinct: a permitted runtime admission obligation does not prove subtyping.

> [!rule] MUD-TYPE-001 — Separate nominal and typed phases
> Type, cardinality, domain, capability and effect information is elaborated after nominal resolution. It is not inserted into nominal HIR. A pending receiver call retains its complete candidate set until the static receiver/given selection rule selects one target.

## 2. Type graph

The following constructors are metalanguage, not new source syntax. $\mathsf{Many}$ wraps a member form with cardinality interval $[\ell,u]$, uniqueness guarantee $q$, order guarantee $o$ and immediate-member capability $c$.

| Form | Information retained |
| --- | --- |
| $\mathsf{Basic}(b)$ | Text, Char, Bool, Nat, Int, Num, Rum, Money and Any. |
| $\mathsf{App}(a,(\tau_i),k)$ | Static application of constructor declaration $a$ to type arguments, retaining category $k$. |
| $\mathsf{Nom}(a,k)$ | Nominal declaration identity $a$ and category $k$: thing, alias or family. |
| $\mathsf{Product}((n_i,\tau_i)_{i=1}^m)$ | Ordered named/positional structural components and their complete contracts. |
| $\mathsf{Produced}(a,(\tau_i),S)$ | A producer declaration $a$, its static generic arguments where applicable, and public schema $S$. |
| $\mathsf{Union}(\tau_1,\ldots,\tau_m)$ | Finite nonempty alternatives without an invented intersection type. |
| $\mathsf{Exact}(K,V,s)$ | Exact dictionary key/value contracts and association specification $s$. |
| $\mathsf{Functional}(K,V,m)$ | Functional dictionary selector/result contracts and branch-selection mode $m$. |
| $\mathsf{Interval}(\tau)$ | An interval/domain value over an ordered member type. |
| $\mathsf{Magnitude}(a,r,d,p)$ | Nominal dimensional factors $d$, representation $r$, and linear/point kind $p$. |
| $\mathsf{Descriptor}(k)$ | A first-class declaration, participant, type, domain or metadata descriptor contract. |
| $\mathsf{Callable}(k,I,R,A)$ | Callable category $k$, ordered input slots $I$, output $R$ and authority/effect guarantees $A$. |
| $\mathsf{Many}(f,D,[\ell,u],q,o,c)$ | Members of form $f$ in domain $D$ and the specified collection guarantees. |

An ordinary omitted collection specification means $[1,1]$; the omission remains source provenance. In an immutable stored field with an initialiser, omitted outer cardinality instead inherits the exact external shape of that initial value. A dictionary remains one outer value independently of its association count. An outwardly mutable field keeps $[1,1]$ when omitted. A bare star is resolved against the applicable effective limits, not against a guessed finite runtime population. All actual collections are finite even when their static upper bound is unbounded. Nested collections occupy members without implicit flattening.

For exact dictionaries the bracketed specification following the arrow constrains associations, not a collection of independent dictionaries. The value contract may itself contain a collection or another dictionary. Text is a positional sequence as one basic value, not Char with a collection-order modifier.

> [!rule] MUD-TYPE-002 — Well-formed type constructors
> Every referenced declaration must be visible and have the required category. Cardinalities have nonnegative integral lower bounds and upper bounds no smaller than their lower bounds. Keyed paths and order paths must be statically meaningful and satisfy their stability contracts. Dictionary arrows must be the complete outer form, including after resolving representation aliases. A collection specification after a complete union qualifies that union; it does not qualify only its last alternative.

Action/subaction callable output is fixed to the single ActionReply contract; it cannot be specialised into an additional domain-result output. The nominal collection alias Errors is one union alternative in ActionReply. Resolving it as an alias does not create anonymous per-alternative collection syntax. No empty structural literal or general intersection syntax is introduced.

## 3. Canonicalisation and identity

Normalisation first resolves identities and validates the specialisation DAG. It gathers inherited declarations by origin, deduplicates diamonds, intersects permitted refinements and requires explicit resolution of incompatible independent contributions. Source order of ancestors supplies no priority.

Create one graph node for each resolved nominal declaration and normalised constructor specification. Representation/component edges may return to an existing node. Transparent alias edges must terminate at a constructor and cannot form a strongly connected component containing only transparent edges. Before unfolding generic applications, establish a finite application closure under section 3.1. Within that admitted closure this worklist terminates; finite source text alone does not establish finite generic instantiation.

Union normalisation flattens nested unions, removes duplicate identical alternatives and gives them a stable canonical order for comparison. It preserves distinct nominal identities and does not discard an alternative merely because its domain is included in another. Cardinalities, nominal factors, stable paths and capabilities remain part of the contract.

> [!rule] MUD-TYPE-003 — Value type identity
> Each alias/family/thing declaration introduces a nominal identity. Each look/sublook declaration and static generic application introduces one produced type, independent of receiver identity and runtime state; each message/submessage declaration introduces one produced type. Context-free literal products have structural identity from their normalised names, order and component contracts. Runtime evaluation creates values, not types or public anchors.

Specialisation views retain a value's exact effective nominal identity. Equality, hashing and caches cannot erase that identity merely because a value is held under a more general static annotation. A structural match grants neither nominal members nor an implicit alias identity. A calculated binding preserves its inferred producer identity.

### 3.1. Generic declarations and applications

> [!rule] MUD-TYPE-017 — Static generic application
> Aliases, families, abstract things, actions/subactions, Boolean rules and looks/sublooks may declare type parameters with `with`. Concrete things, reactive/always rules, messages/submessages, magnitudes and tests do not. Each parameter has all its written nominal `as` bounds, or Any when omitted. The entire header and body share the parameter scope, including ancestors written before `with`. A generic body must typecheck using only those bounds.

`with T, U as A, B with V as C with W` gives T and U both bounds A and B, V bound C, and W bound Any. Bounds are nominal types, possibly statically applied, with no direct domain, cardinality or collection modifiers. Header lists may be bracketed: `with [T, U] as [A, B]` and `as [ParentA, ParentB]`; brackets are sugar, not runtime collections. Ancestor `as` precedes parameter groups; `as` inside a `with` group supplies bounds. In the declaration's ancestor/parameter portion, before any for/given clauses, a new ungrouped `with` starts the next parameter group. An explicit application inside an unbracketed ancestor/bound list is parenthesised, as in `as (Base with T) with T`; a postfix ancestor `as T Base with T` is concise. An explicit application inside a bracketed ancestor/bound list is already delimited by that list.

Arguments likewise have no direct outer domain, cardinality or modifiers. A named representation alias may wrap a complete shape: `alias CatQueue := Cat [* ordered]` admits `Box with CatQueue`; `Box with (Cat [*])` is invalid. A suffix after the complete application, as in `(Box with Cat) [*]`, shapes the outer Box collection, not its Cat argument. Grouped member unions such as `Box with (Nat | Text)` are also admitted without per-alternative collection/domain syntax. An ungrouped `|` combines the surrounding complete type, not generic arguments. Product arguments are admitted, with each component retaining its ordinary complete contract. Substitution replaces the member form at a parameter occurrence; the occurrence supplies its own outer domain/collection contract. It neither flattens a collection-valued argument nor fuses its inner shape with the occurrence's outer shape. Keyed order/uniqueness requires bounds proving the relevant paths and contracts.

`Constructor with A, B` is explicit application. `A Constructor` and `(A, B) Constructor` are postfix forms. After resolving constructor arity, a grouped postfix product supplies its components to an arity greater than one, or remains one product argument to an arity-one constructor. Thus `(Cat, Dog) Pair` supplies two arguments and `(Nat, Nat) Wrapper` supplies one product. Grouping does not bypass argument-shape restrictions, arity or bounds. There is no overloading one generic declaration by arity; an unapplied constructor does not denote a value type or implicit self-application. Its declared parameter type variables are available within its own parameterised scope.

An application is identified by constructor declaration and exact canonical argument identities, independent of source spelling or scope. It creates no declaration, global symbol, anchor, metadata owner or runtime world identity. Applied aliases retain nominal constructor-and-argument identity; a separately declared alias representing an application introduces a new alias identity. Applications of abstract things remain abstract and cannot be created or destroyed. A concrete thing specialising one provides its own canonical identity and statically substituted schema:

```mud
abstract thing Store with T {
    mut items: T [*] = empty
}
thing CatStore as Cat Store
```

Applied family types differ by exact argument identities, including phantom parameters. Members retain their source declaration anchors but have the applied family type. `Cat Slot.Empty` and `Dog Slot.Empty` may share `~anchor` while their `~type` differs. Expected applied-family context permits unqualified `Empty`. Parameters may appear in uniform associated data; members remain closed nominal values, not runtime payload constructors.

Interval is a builtin arity-one generic constructor: `Interval with Nat` and `Nat Interval` are one application. Its existing numeric endpoint/ordered-member admission, domain normalisation and interval operations remain builtin contracts; ordinary generics do not grant an order to a type lacking one.

For generic callables, explicit arguments follow the ordinary call: `(left, right).Equal() with Nat`. Candidate-local constraints come from static `for` and written `given` arguments, explicit type arguments and bounds. A unique declaration must be selected without the expected result; that result may refine inference only afterwards. Apply explicit arguments first and check their substituted inputs by ordinary compatibility. For parameters still requiring inference, a direct parameter input contributes an equation with its supplied static member type; nested contracts contribute corresponding structural equations after candidate-local literal checking. Solve consistent equations and discharge bounds/contract checks under the supported proof rules. Compatibility with arbitrary supertypes does not create extra inferred solutions or a most-specific priority. Conflicting, absent or otherwise ambiguous constraints require explicit `with`; an already selected declaration may use an expected result to supply missing equations. No most-specific guessed solution, runtime Type argument or runtime dispatch is introduced. All ordinary purity, capability, visibility and role-name contracts still apply.

> [!rule] MUD-TYPE-018 — Conservative generic variance
> Infer covariance for a parameter occurring solely in proven output/read positions, contravariance solely in input/consume positions, and invariance for mixed, writable, phantom or unproved positions. Inspect the full effective contract, including inherited/calculated members, domains and authority, rather than only a `mut` spelling. Variance licenses contract inclusion, never equality of applied nominal identities or extra mutation authority.

Start with positive polarity at a produced value contract. Read-only fields/components preserve polarity; callable inputs reverse it and outputs preserve it. Read/write positions require both polarities. An applied constructor composes polarities with its proven parameter variances; invariant positions require both. Dependencies through domain predicates, criteria or other contracts must preserve the inclusion universally; without proof they force invariance. On a finite template dependency graph, accumulate positive/negative requirements to a fixed point; unresolved circular variance claims remain invariant. A phantom parameter supplies no directional proof and remains invariant, in particular in families. Mutable-place substitution retains ordinary complete-contract invariance even when its contained generic constructor has covariant parameters.

For one constructor, proven covariance checks source argument inclusion in the target, contravariance reverses it, and invariance requires mutual complete-contract inclusion. These are compatibility checks, not erasure of exact argument identity. Specialisation ancestry of an application substitutes arguments into its written ancestor applications. Reaching different applications of the same ancestor must satisfy existing coherent-schema/diamond rules rather than merge merely by constructor name.

> [!rule] MUD-TYPE-019 — Finite application closure
> Before normalisation, prove that the static applications reachable through the programme's effective contracts form a finite closed graph. Reject unproved closure and indefinitely growing argument instantiation. Productive recursive values require the separate finite-witness checks below.

Recursion at the same application, mutual recursion and permutations of a finite argument tuple may close a finite graph. A constructor that recursively demands itself with `List with T`, then List of List and so on, does not. A finite closure certificate enumerates application identities, roots and all substituted outgoing applications, with every edge inside that set and all bounds discharged; it is not a depth cutoff or a visited-pair assumption. Generic body checking additionally establishes this obligation parametrically for admitted inputs. Implementations may use a conservative proof procedure; inability to prove closure requires a static diagnostic, not truncation or runtime type creation. Closure finiteness does not establish productivity or enumerable value populations.

## 4. Finite recursive values and productivity

Let $N$ be the finite set of constructor nodes. Define the monotone operator $F$ on subsets of $N$: add a nonrecursive inhabited leaf; a concrete product whose required components already have finite witnesses; a union with a witnessed alternative; or a zero-minimum container whose empty value meets its complete contract. A positive-minimum container additionally requires enough valid members or associations: uniqueness, key uniqueness, order and domains cannot be ignored. An abstract alias receives witnesses only from admissible concrete specialisations.

Starting with $X_0=\varnothing$, compute $X_{i+1}=X_i\cup F(X_i)$ until equality. At most $|N|$ strict additions are possible. The fixed point identifies constructor paths admitting finite witnesses. Defaults count only after their own finite value and contract have been checked.

> [!rule] MUD-TYPE-004 — Productive recursion
> A mandatory recursive constructor cycle without a finite exit is invalid. A recursive type edge does not create a cyclic value reference. Every constructed alias value is a finite immutable tree. An abstract alias cannot be constructed or be the exact target of a nominal cast.

> [!rule] MUD-TYPE-016 — Acyclic domain evaluation
> A computed domain cannot depend directly or transitively on its own evaluation. Static admission must establish acyclicity across the calculations/callable dependencies needed to obtain it; a potential unresolved circular dependency is not a proof. No least/greatest fixed-point semantics is admitted for recursive computed domains.

Reading an already stored value from the inherited coherent view does not evaluate that value's domain again. Several candidate-field contracts may read each other's already available stored values without a circular domain calculation. This does not permit circular initialisers or remove ordinary field/write/checkpoint validation. Cyclic point-domain normalisation, nominal type recursion and dependency cycles of computed domains are distinct.

Domain obligations are separate from constructor reachability. An empty or state-dependent domain does not acquire a witness from a basic type's unrefined inhabitation. A supplied/default value can witness inhabitation only after its domain check. Without such evidence the analysis must not claim unconditional inhabitation. A well-formed contract may denote no values in a projection; no automatic value is selected to repair it.

**Finite-witness lemma.** Every node admitted at iteration $i$ has a finite constructor witness whose children were admitted earlier. Proof is by induction on $i$. Conversely, any valid finite witness is admitted by induction on its tree height, provided its leaf/domain obligations are witnessed. This does not prove that all state-dependent domains are decidable.

## 5. Proof obligations and enumeration

A proof is a finite derivation from declared guarantees, established flow facts, normalised exact arithmetic/interval relations, or exhaustive evaluation of a proven finite canonical enumeration. Each use names its premises; a solver's unsupported assertion, a recursive call to the same unproved fact, or an observation of one runtime sample is not a proof.

The mandatory elementary rules include reflexivity, transitivity, intersection elimination, inclusion of normalised finite interval unions, interval arithmetic, declared nominal ancestry, constructor rules in this chapter, and checking all members of a finite explicit enumeration. Unbounded/symbolic predicates may remain unknown. Unknown differs from false; mandatory static obligations cannot be discharged by unknown.

For a domain $D$, canonical enumeration requires a finite sequence with no duplicates whose set equals $D$, with the order required by the domain. Evidence may be a finite explicit set; a bounded integral/scale-two progression; an exact stepped rational progression with a compatible nonzero signed step; a finite family; a finite linked-world population snapshot; or finite products/unions/filterings of already witnessed domains. A filtering predicate must terminate and satisfy its owner's purity/determinism requirements. Unstepped general Num intervals, Rum intervals and Any are not enumerable.

A static stepped domain uses the established signed progression to define membership: positive differences anchor at the lower bound, negative differences at the upper bound, and open starting bounds advance before the first candidate. Canonical materialisation orders the resulting members according to the domain, rather than copying descending traversal order. Finite bounds and nonzero compatible advance establish a finite number of candidates; zero advance cannot establish termination.

Enumeration of a recursive constructor type needs an explicit finite rank bound and finite branching evidence; induction on the bound reduces enumeration to finite constructor products whose domain contracts are already established. Finite individual trees alone supply no bound on the set of trees. A finite rank does not license circular evaluation of computed domain definitions.

> [!rule] MUD-TYPE-005 — No guessed proof
> Mandatory static inclusion, writable invariance, termination and finite enumeration require evidence. Runtime admission checks may validate a particular value only where that context permits them; they cannot justify universal callable substitution or an unproven enumeration.

## 6. Subtyping and guarantee inclusion

Nat and Int have arbitrary-precision nonnegative/signed integer values. Money has arbitrary-precision signed integer hundredths; Num retains exact rational values. None has a language-level native-integer bound. Implementations must promote before observable overflow; resource exhaustion uses the technical Error channel rather than wrapping or restricting the mathematical domain.

For basic numeric representations the only implicit widening chain is Nat $\preceq$ Int $\preceq$ Num. Rum and Money are not on that chain. Every MUD value contract can be forgotten to Any, but Any supplies no member operations, enumeration, ordering or writable authority.

Nominal subtyping follows declared admissible ancestry. A source concrete alias/thing may be viewed through its ancestor while retaining its exact identity. A representation alias is not implicitly assignable to its underlying representation merely because the representations match.

For read-only collection contracts, the following premises give the constructor rule:

$$
\frac{
f_A\preceq f_B\quad D_A\subseteq D_B\quad
[\ell_A,u_A]\subseteq[\ell_B,u_B]\quad
(q_A,o_A,c_A)\succeq(q_B,o_B,c_B)
}{
\mathsf{Many}(f_A,D_A,[\ell_A,u_A],q_A,o_A,c_A)
\preceq
\mathsf{Many}(f_B,D_B,[\ell_B,u_B],q_B,o_B,c_B)
}
\;\mathsf{T\text{-}ReadCollection}
$$

All premises are proved under $\Sigma;\Phi$. Guarantee strength $\succeq$ means the source supplies every target guarantee: keyed uniqueness implies whole-value uniqueness, which implies none; equal keyed criteria are compatible; order preserves the required criterion; authority may be forgotten but not created. No deep mutability is inferred. Outer writable-place invariance is defined in [[15-fields-and-mutability]].

A source union is usable as $\sigma$ only when every alternative satisfies $\sigma$. A source fits a target union if it satisfies a target alternative; composite derivations may prove coverage without arbitrarily selecting a target for an ambiguous literal. Read-only products require matching component names/order and componentwise inclusion. Nominal membership still needs ancestry or contextual construction.

Recursive read-only inclusion may use a finite relation of graph-node pairs. Every pair must satisfy its local nominal, constructor, domain and guarantee premises; every required child pair must belong to the relation. Contravariant input/key positions reverse the child pair. This is a closed finite certificate, not acceptance because a pair was visited before. Writable invariance requires certificates in both directions. Domain premises not discharged by the mandatory proof basis remain unknown.

Read-only exact dictionary values may widen covariantly. Their key contract must preserve all lookups admitted by the target: every target key must be admitted by the source key contract. Association/domain/modifier guarantees must also hold. This is query substitution, not permission to replace keys or values. Any writable dictionary destination is checked invariantly at its stored root. Functional dictionaries additionally preserve selector admission, output inclusion, selection mode and their termination/effect contract.

## 7. Representation equivalence and explicit construction

Representation equivalence compares complete constructor labels after nominal representation wrappers are exposed. Product arity, component names/order, underlying component forms, collection cardinalities/modifiers and dictionary nesting must match. Defaults are not components and do not change shape. Domain refinements are separately validated at the target; they are not silently satisfied by shape equivalence.

For recursion, initialise the finite set of candidate node pairs with matching local constructor labels. Repeatedly remove a pair if a required child pair is absent; compare all ordered product children and all required alternatives, not one sample. The greatest fixed point is a finite labelled bisimulation. Every surviving pair must satisfy all its local conditions. Revisiting a pair alone is not proof. This relation establishes representational compatibility for conversion, not nominal subtyping or inhabitation.

> [!rule] MUD-TYPE-006 — Contextual nominal construction
> An untyped basic or structural literal may acquire a unique concrete expected alias type while constructing all its components. Positional construction supplies every component. Named construction retains declaration order and may omit only components with explicit effective defaults. Already typed values keep their nominal identity and require an admitted explicit conversion to acquire another.

An explicit nominal cast requires representation equivalence and validates destination domains and guarantees without rounding or changing the underlying contents. Quantitative conversion is a different family: it checks numerical/dimensional compatibility, applies the specified rounding where required, then validates the destination. Casting never creates world identity or grants a capability.

Two context-free structural literals do not supply each other with a nominal comparison context. An already typed alias operand may supply its type to the opposite untyped compatible literal.

Normal and sub operations retain distinct declaration identity: `subaction <: action`, `sublook <: look` and `submessage <: message` in the descriptor hierarchy. Widening does not confer host capability. Only normal operations from shared files are host endpoints; any possible sub or part-only alternative requires narrowing/proof before host admission. Mud calls across parts use direct uses permission. Sublook is pure in every ordinary reading context, including a look body; submessage is a causal source with the ordinary on/when contracts but no external endpoint. Each look/sublook/message/submessage declaration has its own static produced type.

### 7.1. Exact structural type equality

> [!rule] MUD-TYPE-020 — Structural equality of normalized contracts
> `===` compares two Type operands by their entire normalized effective contracts, erasing only alias nominal identity. `!==` is its exact negation. Things and families, including their applications, are nominally opaque: distinct exact identities never become equal by matching fields or members. Ordinary value equality, nominal `is`/`iis` and representation compatibility for `to` retain their separate contracts.

Compare member names and declaration order, stored/component versus calculated kind, complete member types, domains, cardinality, multiplicity, uniqueness and its key criterion, order and its criterion, inner authority, product composition, nested collection layers, dictionary grouping and normalized union alternatives. Callable contracts retain inputs, outputs and authority guarantees. Alias representations and effective inherited schemas participate after substitution. Metadata, presentation names, documentation, defaults and calculated bodies do not participate; a default or body that changes an inferred effective type/shape affects comparison through that resulting contract. Hence calculated `x: Nat := 1` and `x: Nat := 2` match, while stored and calculated x do not.

Domain equality uses normalized symbolic contracts, including resolved provenance, binders and generic substitution, plus the defined exact arithmetic/interval normalization. It does not evaluate current populations or arbitrary predicates to prove semantic equivalence. Different symbolic predicates do not become equal because they currently yield equal sets. Union order/duplicate syntax is normalized; match the complete normalized alternatives without source-order dependence. Nominally distinct alternatives retained by ordinary union normalization are not silently removed by representational matching or semantic inclusion. No general program-equivalence oracle is required.

For recursive admitted type graphs, compare a closed finite relation of node pairs: all local structural labels must match and every required child pair must belong to the relation. Alias identity is omitted from these labels; opaque thing/family labels retain constructor and exact argument identities. Greatest-fixed-point labelled bisimulation handles recursion without comparing sample values. Merely visiting a pair is not evidence. The relation is exact equality of this normalized contract representation, not the weaker conversion representation relation $\cong_R$.

```mud
alias A { x: Nat; y: Text [0..1] }
alias B { x: Nat; y: Text [0..1] }
rule SameStructure { A === B }
rule DifferentOrder { Text [*] !== Text [* ordered] }
```

Both types may be exposed as Type descriptors without adding application anchors. Descriptors retain source constructor and argument information; member `~anchor` denotes the source declaration and `~type` the effective applied type. This does not introduce new intrinsic metadata spellings or settle the TypeKind member catalogue.

## 8. Callable substitution and call selection

Write a callable contract as $(I,R,A)$; $I$ is the ordered input-slot list and $A$ includes permissions, effects, determinism and outer-root capability. Let $s$ be supplied and $t$ requested.

$$
\frac{
\forall i\in I_t^{read}.\ I_{t,i}\preceq I_{s,i}\quad
\forall i\in I_t^{write}.\ I_{s,i}\equiv I_{t,i}\quad
R_s\preceq R_t\quad A_s\ \mathsf{meets}\ A_t
}{
(I_s,R_s,A_s)\preceq(I_t,R_t,A_t)
}
\;\mathsf{T\text{-}Callable}
$$

Here $\equiv$ means mutual complete-contract inclusion, not equality of source text. The supplied signature must admit every requested call, including optional/default arguments, and cannot introduce mandatory roles. Inner-member authority is checked by permission/footprint inclusion; mentioning mut does not automatically make every nested type invariant.

> [!rule] MUD-TYPE-007 — Static signature names
> Named receiver/argument binding requires identical unambiguous names at compatible static signature positions across all possible callable alternatives. Collections are not scanned at runtime to recover names. Positional binding or prior static narrowing may use an otherwise compatible erased contract. An action-shaped type containing a subaction does not obtain outer-root permission.

Receiver-based nominal selection obeys [[10-names-and-anchors#Receiver-call selection]]. Only statically established incompatibility eliminates candidates; an unresolved domain/cardinality obligation does not select another declaration. Written given names and static contracts participate in candidate-local selection. Expected results, omitted defaults as argument evidence and guards cannot resolve nominal ambiguity; ordinary remaining admission obligations validate the selected declaration.

## 9. Checking, inference and narrowing

Synthesis is bottom-up; checking passes an expected contract down into untyped literals and callable arguments. Each stored binding/declaration has its required annotation and initialiser/default under its owner contract; an annotation may contain inference holes only when the declaration has its own initial value. Calculated bindings preserve their synthesised type unless an explicit shape requires checking or a declared derived transformation.

For a type-correct value whose domain/cardinality may fail, checking records a site-specific predicate obligation only where runtime admission is authorised. A known invalid static initialiser is rejected. Call admission reports the appropriate refusal; an ordinary value computation uses its Error channel. Mandatory post-effect stored cardinality proof is not replaced by such an obligation.

When an expression produces alternatives, consider their common supertype candidates under the proven inclusion relation. A unique most-specific informative candidate may be used. Any alone is not informative and cannot erase the original alternatives during synthesis. Several incomparable minima retain the normalised original union, as does absence of a more informative common candidate. Expected types may check each alternative but cannot force a nominal cast or resolve a nominal call target.

For a successful is test, $\Phi$ retains the compatible nominal alternatives; its false branch excludes only alternatives established impossible. Iis tests exact effective nominal identity; its negative case may still contain descendants. Narrowing on a mutable read is invalidated when an intervening effect may change that place or dependency. It never creates authority.

> [!rule] MUD-TYPE-008 — Unique inference
> An omitted type is inferred only when synthesis and the available context determine a unique contract, or a defined union join. Otherwise an annotation/narrowing is required. Context-free empty has cardinality zero and no chosen nominal member type; it can be checked against a zero-admitting expected collection, but cannot select a family member, world identity or type default.

### 9.1. Stored type-inference holes

> [!rule] MUD-TYPE-021 — Unique stored-hole solution
> In a stored annotation with an initial value, each `_` stands for one omitted static member type. Holes may occur recursively in otherwise admitted product, generic-argument, callable and dictionary type positions. Solve the complete annotation and initialiser jointly, using written structure and established domain/type evidence. Every hole must have one uniquely determined normalized type. Unsolved, inconsistent or ambiguous holes are compile-time errors, with tooling marking the hole's source span. No unresolved hole reaches runtime. A hole is not Any, a wildcard, dynamic typing or a fresh nominal type, and insufficient evidence never falls back to Any.

Each written hole is an independent inference occurrence; two underscores do not implicitly equate their solutions. An already established Any source contract may itself be the uniquely synthesized type, but Any cannot be guessed to repair missing evidence. Propagate the written expected structure into components of the initialiser and synthesize missing component contracts where unique. Several source spellings for the same normalized exact type are one solution; structurally equal but nominally distinct aliases are different possible solutions. Do not enumerate nominal aliases to invent a contextual construction. Defined union synthesis retains its ordinary rule; a union of possible guesses is not a solution for an ambiguous hole. A generic application is checked only after its arguments are resolved, with ordinary bounds, variance and finite-closure obligations.

`pair: (_, Text) = source` succeeds when source and written constraints determine the first component uniquely and the second meets Text. `pair: (_, Text) = (empty, "hello")` fails without additional evidence for the first member type. `values: _ = empty` fails; `values: _ in Cats [*] = empty` succeeds only if the domain contract supplies unique type evidence. Mutable stored annotations admit holes with the same rule; subsequent assignments obey the inferred fixed contract and ordinary writable invariance.

Written domains, cardinalities, uniqueness, order and authority remain stored admission constraints, never coercive derived transforms. Omitted outer shape retains the owner's existing policy, including initializer-shape capture for immutable stored fields and the singleton default for mutable fields. No hole infers missing bounds or creates authority. Schema/default/metadata initialisers retain their closed-static requirements. Hole syntax is unavailable in participant/given signatures, generic parameter bounds, alias representation definitions, derived annotations, ordinary casts or standalone Type expressions.

### 9.2. Pattern typing

> [!rule] MUD-TYPE-022 — Exact positional binding
> Check a binding pattern against its complete source contract. Names capture the corresponding component; `_` checks the same position but binds nothing. A positional node requires an admitted singleton positional product of exactly its arity and recursively checks its components. Named products cannot be opened. Every statically possible source alternative must admit the pattern and yield a unique contract for every named capture under the ordinary inference rules. Shape mismatch is a static error, not a filter or a runtime failed match.

Nested products may remain whole under a name or be opened recursively. An already nominal alias is not implicitly cast into an anonymous product to enable a pattern; its exposed positional representation, where available under the ordinary alias contract, supplies projections while the original source identity remains intact. Exact-dictionary traversal admits a two-position association pattern with key/value contracts; this exception does not make associations ordinary products. Nested positions inside that pattern follow ordinary positional-product rules. Iteration, selection and quantifiers bind one admitted source item/association at a time; a collection-valued component is not implicitly flattened.

Exact dictionaries retain key traversal for a single name or discard. A positional root of exactly two positions selects association projection, even when the key itself has a positional representation; open that key within the first position if needed. The pattern only changes available predicate/body bindings. Selection retains accepted associations, and dictionary min/max retain their original accepted key witness rather than constructing an ordinary product from key/value bindings. Step, finiteness and usable-order requirements remain those of the original traversal.

Stored local patterns evaluate the RHS once, validate the complete pattern and establish all immutable captures atomically; a failed RHS exposes no partial bindings. Derived patterns register live component projections of their common RHS. They have no writable root, and pure expression positions retain their ExpressionBlock restrictions. A completely discarded stored pattern still evaluates its RHS and enforces admission/error obligations; tooling may suggest removal only when no observable obligation is lost. Derived patterns retain derivation checks even when every component is discarded, but do not introduce eager reads or new effects solely to discard them.

### Public TypeKind categories

> [!rule] MUD-TYPE-026 — Public exterior classification
> TypeKind classifies the public type exterior. An alias remains Alias regardless of its representation. Applied generics retain the constructor's public category; neither application nodes nor internal compiler constructors acquire a public kind merely by existing.

| Public form | Selected category |
| --- | --- |
| Nat, Int, Num, Rum, Money, Text, Char, Bool | Basic |
| Any | Any |
| Nominal thing, alias, family | Thing, Alias, Family respectively |
| Anonymous tuple, collection, union, interval | Tuple, Collection, Union, Interval respectively |
| Exact dictionary; functional dictionary | Dictionary; FunctionalDictionary |
| Linear magnitude; point magnitude (including cyclic points) | Magnitude; PointMagnitude |
| Produced look/sublook result; message/submessage payload | LookResult; MessagePayload |
| Action/subaction callable; look/sublook callable; Boolean-rule callable | ActionCallable; LookCallable; BooleanRuleCallable |
| Type, field, participant, metadata, domain descriptor | TypeDescriptor, FieldDescriptor, ParticipantDescriptor, MetadataDescriptor, DomainDescriptor respectively |

Reactive/always rules do not acquire a BooleanRuleCallable category. Exact nominal identities and generic arguments remain available independently of kind. Public names do not change product notation or AST constructors. The catalogue permits additions, so consumers must not assume the selected core exhausts future/extension categories. Standard forms retain their classification. Extension identities/registration, compatibility rules, complete descriptor inventory and remaining normalization/projection boundaries are [[../notes/questions/Q-060-c-reflective-typekind-catalogue|Q-060]]; this table does not claim a complete extensible-family schema.

## 10. Schemas, visibility and descriptor types

Every new stored thing field has an explicit initialiser. Alias components are all present in a value, from supplied values or explicit defaults. Family data are supplied by the schema or by every member. User-defined metadata needs an explicit effective value; intrinsic defaults retain their individual contracts.

Inherited writable stored contracts remain invariant. Immutable alias contracts may refine all inherited guarantees, with a valid effective initialiser/default where one is required. Diamonds deduplicate origins and incomparable independent members need a common explicit refinement. No runtime effect changes the set of field declarations.

Thing value admission preserves strict membership: a field whose member type is the thing declaration $T$ does not admit $T$ itself as a population member; compatible concrete descendants are admissible. A declaration descriptor for $T$ is a distinct reflective use.

Cross-part thing/alias specialisation requires uses authorisation and membership of the visible public contract's transitive type closure. Importing a path supplies no authority. Inherited initialisation is compiled under the declaring owner's access rights. Private ordinary thing fields do not become public through specialisation.

Descriptor reflection is checked against every possible static receiver category. A supported optional property may return empty; an unsupported property is a static error, never a dynamic empty fallback. A type expression obtained through type reflection must be statically established as Type; runtime-dependent type generation is invalid. Source spans and AST values are not MUD values merely because the compiler holds them.

## 11. Results and errors as types

Success is a nominal alias supplied by successful action evaluation. The interface for obtaining the incorporated textual patch, including any Success component, remains Q-073; no additional component/type is defined here. It remains part of the sole ActionReply result, not an action-specific domain return. Refusal and Error are abstract structural aliases. IfRefusal, AfterRefusal and AlwaysRefusal are ConditionRefusal specialisations; ArgumentRefusal identifies the argument role. Refusal/Error require reason and Declaration origin. Error has an optional finite cause; ConditionRefusal has the BoolCheck trace of the actually evaluated final Boolean expression.

Errors is a nominal alias of a nonempty Error collection; ActionReply is the union Success | Refusal | Errors. Producing an Error or obtaining an ActionReply containing Errors is ordinary value production. Entering a block error channel is a separate evaluation outcome. Every block has an Error collection channel allowing zero occurrences; its normal result is available only when that channel is empty.

Otherwise roles bind only Error specialisations, conjunctively and by occurrences. A then recovery checks against the protected block's normal contract and permissions; raise checks one Error or a nonempty compatible Errors collection. Refusal is never an Error binding. [[21-expressions]] defines the block typing rules.

## 12. Static acceptance and elaboration output

An accepted programme has well-formed visible schemas, finite normalised type graphs, checked declarations/expressions, all mandatory static proofs and explicitly located permitted runtime obligations. Unproven writable substitution, unsupported reflection, ambiguous inference and missing initialisation are static diagnostics.

Elaboration preserves source origins and records the selected nominal targets, effective schemas/types, literal contextualisation, operation overloads, conversions, flow facts, permission checks, effect footprints, finite-enumeration/termination evidence and runtime predicate checks. No particular semantic IR serialisation or node catalogue is required.

**Conditional safety statement.** If the stated static premises hold, trusted foreign contracts hold, and each admitted runtime predicate succeeds, a normal result satisfies its declared contract and every write uses authorised storage. A computing error or refusal does not assert that a normal result exists. This is a compositional static obligation, not a proof of termination or atomic correctness of a complete causal engine.

The machine-readable instances in [[types/typing-cases.yaml]] distinguish static acceptance/rejection from permitted runtime checks. Their validator checks evidence structure and finite contract witnesses; it does not parse or execute MUD programmes.
