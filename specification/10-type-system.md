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
  - "[[09-names-and-anchors]]"
questions:
  - Q-060
decisions:
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
---

# 10. Type system

## Scope and dependencies

This chapter defines well-formed types, value identity, representation compatibility, subtyping, contextual checking and inference. [[14-fields-and-mutability]] defines place authority and effect obligations; [[19-expressions]] assigns these contracts to expressions and blocks. These three chapters describe a static language contract, not a compiler data layout or a causal evaluator.

Numeric signatures and dimensional admission follow [[19-expressions#4. Numeric, dimensional and Boolean operators]]. A combination lacking a defined signature cannot be accepted by inventing a promotion. The reflective TypeKind member catalogue remains Q-060; the descriptor typing rules here do not introduce members of that catalogue.

## 1. Environments and judgements

Let $P$ be a linked, nominally resolved programme. Its finite nominal catalogue is $\Sigma$. It records declaration identity, category, ancestry, schema origins, callable signatures, module visibility and declared type expressions. $\Gamma$ maps visible local names to value contracts and place information. $\Phi$ is the finite set of facts established at the programme point by contracts and control-flow narrowing. $W$ is a well-formed world projection used only to interpret state-dependent domains.

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
> Type, cardinality, domain, capability and effect information is elaborated after nominal resolution. It is not inserted into nominal HIR. A pending receiver call retains its complete candidate set until the receiver-selection rule selects one target.

## 2. Type graph

The following constructors are metalanguage, not new source syntax. $\mathsf{Many}$ wraps a member form with cardinality interval $[\ell,u]$, uniqueness guarantee $q$, order guarantee $o$ and immediate-member capability $c$.

| Form | Information retained |
| --- | --- |
| $\mathsf{Basic}(b)$ | Text, Char, Bool, Nat, Int, Num, Rum, Money and Any. |
| $\mathsf{Nom}(a,k)$ | Nominal declaration identity $a$ and category $k$: thing, alias or family. |
| $\mathsf{Product}((n_i,\tau_i)_{i=1}^m)$ | Ordered named/positional structural components and their complete contracts. |
| $\mathsf{Produced}(a,S)$ | A look/message producer identity and its statically elaborated public schema $S$. |
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

Create one graph node for each resolved nominal declaration and normalised constructor specification. Representation/component edges may return to an existing node. Transparent alias edges must terminate at a constructor and cannot form a strongly connected component containing only transparent edges. This worklist terminates because the source graph and effective schemas are finite.

Union normalisation flattens nested unions, removes duplicate identical alternatives and gives them a stable canonical order for comparison. It preserves distinct nominal identities and does not discard an alternative merely because its domain is included in another. Cardinalities, nominal factors, stable paths and capabilities remain part of the contract.

> [!rule] MUD-TYPE-003 — Value type identity
> Each alias/family/thing declaration introduces a nominal identity. Each look or message declaration introduces one static produced type, independent of receiver and runtime state. Context-free literal products have structural identity from their normalised names, order and component contracts. Runtime evaluation creates values, not types or public anchors.

Specialisation views retain a value's exact effective nominal identity. Equality, hashing and caches cannot erase that identity merely because a value is held under a more general static annotation. A structural match grants neither nominal members nor an implicit alias identity. A calculated binding preserves its inferred producer identity.

## 4. Finite recursive values and productivity

Let $N$ be the finite set of constructor nodes. Define the monotone operator $F$ on subsets of $N$: add a nonrecursive inhabited leaf; a concrete product whose required components already have finite witnesses; a union with a witnessed alternative; or a zero-minimum container whose empty value meets its complete contract. A positive-minimum container additionally requires enough valid members or associations: uniqueness, key uniqueness, order and domains cannot be ignored. An abstract alias receives witnesses only from admissible concrete specialisations.

Starting with $X_0=\varnothing$, compute $X_{i+1}=X_i\cup F(X_i)$ until equality. At most $|N|$ strict additions are possible. The fixed point identifies constructor paths admitting finite witnesses. Defaults count only after their own finite value and contract have been checked.

> [!rule] MUD-TYPE-004 — Productive recursion
> A mandatory recursive constructor cycle without a finite exit is invalid. A recursive type edge does not create a cyclic value reference. Every constructed alias value is a finite immutable tree. An abstract alias cannot be constructed or be the exact target of a nominal cast.

Domain obligations are separate from constructor reachability. An empty or state-dependent domain does not acquire a witness from a basic type's unrefined inhabitation. A supplied/default value can witness inhabitation only after its domain check. Without such evidence the analysis must not claim unconditional inhabitation. A well-formed contract may denote no values in a projection; no automatic value is selected to repair it.

**Finite-witness lemma.** Every node admitted at iteration $i$ has a finite constructor witness whose children were admitted earlier. Proof is by induction on $i$. Conversely, any valid finite witness is admitted by induction on its tree height, provided its leaf/domain obligations are witnessed. This does not prove that all state-dependent domains are decidable.

## 5. Proof obligations and enumeration

A proof is a finite derivation from declared guarantees, established flow facts, normalised exact arithmetic/interval relations, or exhaustive evaluation of a proven finite canonical enumeration. Each use names its premises; a solver's unsupported assertion, a recursive call to the same unproved fact, or an observation of one runtime sample is not a proof.

The mandatory elementary rules include reflexivity, transitivity, intersection elimination, inclusion of normalised finite interval unions, interval arithmetic, declared nominal ancestry, constructor rules in this chapter, and checking all members of a finite explicit enumeration. Unbounded/symbolic predicates may remain unknown. Unknown differs from false; mandatory static obligations cannot be discharged by unknown.

For a domain $D$, canonical enumeration requires a finite sequence with no duplicates whose set equals $D$, with the order required by the domain. Evidence may be a finite explicit set; a bounded integral/scale-two progression; an exact stepped rational progression with a compatible nonzero signed step; a finite family; a finite linked-world population snapshot; or finite products/unions/filterings of already witnessed domains. A filtering predicate must terminate and satisfy its owner's purity/determinism requirements. Unstepped general Num intervals, Rum intervals and Any are not enumerable.

A static stepped domain uses the established signed progression to define membership: positive differences anchor at the lower bound, negative differences at the upper bound, and open starting bounds advance before the first candidate. Canonical materialisation orders the resulting members according to the domain, rather than copying descending traversal order. Finite bounds and nonzero compatible advance establish a finite number of candidates; zero advance cannot establish termination.

A recursive domain needs an explicit finite rank bound and finite branching evidence; induction on the bound reduces enumeration to finite constructor products. Finite individual trees alone supply no bound on the set of trees.

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

All premises are proved under $\Sigma;\Phi$. Guarantee strength $\succeq$ means the source supplies every target guarantee: keyed uniqueness implies whole-value uniqueness, which implies none; equal keyed criteria are compatible; order preserves the required criterion; authority may be forgotten but not created. No deep mutability is inferred. Outer writable-place invariance is defined in [[14-fields-and-mutability]].

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

Receiver-based nominal selection obeys [[09-names-and-anchors#Receiver-call selection]]. Only statically established incompatibility eliminates candidates; an unresolved domain/cardinality obligation does not select another declaration. Given arguments, return expectations and guards validate the selected declaration and never resolve nominal ambiguity.

## 9. Checking, inference and narrowing

Synthesis is bottom-up; checking passes an expected contract down into untyped literals and callable arguments. Each stored binding/declaration has its required annotation and explicit initialiser. Calculated bindings preserve their synthesised type unless an explicit shape requires checking or a declared derived transformation.

For a type-correct value whose domain/cardinality may fail, checking records a site-specific predicate obligation only where runtime admission is authorised. A known invalid static initialiser is rejected. Call admission reports the appropriate refusal; an ordinary value computation uses its Error channel. Mandatory post-effect stored cardinality proof is not replaced by such an obligation.

When an expression produces alternatives, consider their common supertype candidates under the proven inclusion relation. A unique most-specific informative candidate may be used. Any alone is not informative and cannot erase the original alternatives during synthesis. Several incomparable minima retain the normalised original union, as does absence of a more informative common candidate. Expected types may check each alternative but cannot force a nominal cast or resolve a nominal call target.

For a successful is test, $\Phi$ retains the compatible nominal alternatives; its false branch excludes only alternatives established impossible. Iis tests exact effective nominal identity; its negative case may still contain descendants. Narrowing on a mutable read is invalidated when an intervening effect may change that place or dependency. It never creates authority.

> [!rule] MUD-TYPE-008 — Unique inference
> An omitted type is inferred only when synthesis and the available context determine a unique contract, or a defined union join. Otherwise an annotation/narrowing is required. Context-free empty has cardinality zero and no chosen nominal member type; it can be checked against a zero-admitting expected collection, but cannot select a family member, world identity or type default.

## 10. Schemas, visibility and descriptor types

Every new stored thing field has an explicit initialiser. Alias components are all present in a value, from supplied values or explicit defaults. Family data are supplied by the schema or by every member. User-defined metadata needs an explicit effective value; intrinsic defaults retain their individual contracts.

Inherited writable stored contracts remain invariant. Immutable alias contracts may refine all inherited guarantees, with a valid effective initialiser/default where one is required. Diamonds deduplicate origins and incomparable independent members need a common explicit refinement. No runtime effect changes the set of field declarations.

Thing value admission preserves strict membership: a field whose member type is the thing declaration $T$ does not admit $T$ itself as a population member; compatible concrete descendants are admissible. A declaration descriptor for $T$ is a distinct reflective use.

Cross-module thing/alias specialisation requires uses authorisation and membership of the visible public contract's transitive type closure. Importing a path supplies no authority. Inherited initialisation is compiled under the declaring owner's access rights. Private ordinary thing fields do not become public through specialisation.

Descriptor reflection is checked against every possible static receiver category. A supported optional property may return empty; an unsupported property is a static error, never a dynamic empty fallback. A type expression obtained through type reflection must be statically established as Type; runtime-dependent type generation is invalid. Source spans and AST values are not MUD values merely because the compiler holds them.

## 11. Results and errors as types

Success is a zero-component nominal alias supplied by successful action evaluation. Refusal and Error are abstract structural aliases. IfRefusal, AfterRefusal and AlwaysRefusal are ConditionRefusal specialisations; ArgumentRefusal identifies the argument role. Refusal/Error require reason and Declaration origin. Error has an optional finite cause; ConditionRefusal has the BoolCheck trace of the actually evaluated final Boolean expression.

Errors is a nominal alias of a nonempty Error collection; ActionReply is the union Success | Refusal | Errors. Producing an Error or obtaining an ActionReply containing Errors is ordinary value production. Entering a block error channel is a separate evaluation outcome. Every block has an Error collection channel allowing zero occurrences; its normal result is available only when that channel is empty.

Otherwise roles bind only Error specialisations, conjunctively and by occurrences. A then recovery checks against the protected block's normal contract and permissions; raise checks one Error or a nonempty compatible Errors collection. Refusal is never an Error binding. [[19-expressions]] defines the block typing rules.

## 12. Static acceptance and elaboration output

An accepted programme has well-formed visible schemas, finite normalised type graphs, checked declarations/expressions, all mandatory static proofs and explicitly located permitted runtime obligations. Unproven writable substitution, unsupported reflection, ambiguous inference and missing initialisation are static diagnostics.

Elaboration preserves source origins and records the selected nominal targets, effective schemas/types, literal contextualisation, operation overloads, conversions, flow facts, permission checks, effect footprints, finite-enumeration/termination evidence and runtime predicate checks. No particular semantic IR serialisation or node catalogue is required.

**Conditional safety statement.** If the stated static premises hold, trusted foreign contracts hold, and each admitted runtime predicate succeeds, a normal result satisfies its declared contract and every write uses authorised storage. A computing error or refusal does not assert that a normal result exists. This is a compositional static obligation, not a proof of termination or atomic correctness of a complete causal engine.

The machine-readable instances in [[types/typing-cases.yaml]] distinguish static acceptance/rejection from permitted runtime checks. Their validator checks evidence structure and finite contract witnesses; it does not parse or execute MUD programmes.
