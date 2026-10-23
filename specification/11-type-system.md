---
title: Type system
aliases:
  - Static types of MUD
tags:
  - mud/specification
status: current
normative: true
depends-on:
  - "[[03-notation]]"
  - "[[10-names-and-anchors]]"
questions:
  - Q-073
decisions:
  - D-186
  - D-183
  - D-184
  - D-185
  - D-181
  - D-180
  - D-176
  - D-178
  - D-177
  - D-171
  - D-170
  - D-169
  - D-167
  - D-168
  - D-166
  - D-165
  - D-163
  - D-162
  - D-161
  - D-160
  - D-159
  - D-158
  - D-157
  - D-156
  - D-155
  - D-154
  - D-151
  - D-149
  - D-148
  - D-147
  - D-146
  - D-145
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

## Stored declaration inference

Ordinary stored field/local types may be omitted when initialiser and domain evidence determine a unique contract. Explicit recursive holes retain MUD-TYPE-021; a bare hole is valid with a semantics-preserving simplification suggestion. Written constraints remain admission checks. Declaration markers, omitted-cardinality policy and domain-only shapes follow [[15-fields-and-mutability#Value declarations and stored inference]]. No inferred input type is invented for an uncontextualised functional policy.

## Scope and dependencies

This chapter defines well-formed types, value identity, representation compatibility, subtyping, contextual checking and inference. [[15-fields-and-mutability]] defines place authority and effect obligations; [[21-expressions]] assigns these contracts to expressions and blocks. These three chapters describe a static language contract, not a compiler data layout or a causal evaluator.

```mud
alias Position { let x: Int; let y: Int }
look Example {
    let origin: Position := (0, 0)
    let coordinates: Int [2] := [origin.x, origin.y]
}
```

Position supplies the unique nominal construction context; coordinates checks
its own member and cardinality contract.

Numeric signatures and dimensional admission follow [[21-expressions#4. Numeric, dimensional and Boolean operators]]. A combination lacking a defined signature cannot be accepted by inventing a promotion. Alias operator declarations and their local result-inference preference follow [[21-expressions#Alias-owned operator signatures]]; selection and lifting follow the same section; complete signature identity and the reflective schema follow [[names/operator-contract-identity]]. The complete fixed TypeKind catalogue, supporting inventory and normalized projection are specified below.

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
| $\mathsf{Basic}(b)$ | String, Char, Bool, Nat, Int, Num, Rum, Money and Any. |
| $\mathsf{App}(a,(\tau_i),k)$ | Static application of constructor declaration $a$ to type arguments, retaining category $k$. |
| $\mathsf{Nom}(a,k)$ | Nominal declaration identity $a$ and category $k$: thing, alias or family. |
| $\mathsf{Product}((n_i,\tau_i)_{i=1}^m)$ | Ordered named/positional structural components and their complete contracts. |
| $\mathsf{Produced}(a,(\tau_i),S)$ | A producer declaration $a$, its static generic arguments where applicable, and public schema $S$. |
| $\mathsf{Union}(\tau_1,\ldots,\tau_m)$ | Finite nonempty alternatives without an invented intersection type. |
| $\mathsf{Exact}(K,V,s)$ | Exact dictionary key/value contracts and association specification $s$. |
| $\mathsf{Functional}(K,V)$ | Functional input/output contracts; body mode is a value property. |
| $\mathsf{Scheme}(Q,C,S)$ | Correlated quantified functional constraints and signature. |
| $\mathsf{Trait}(R)$ | Normalized minimum structural requirements. |
| $\mathsf{Interval}(\tau)$ | An interval/domain value over an ordered member type. |
| $\mathsf{Magnitude}(a,r,d,p)$ | Nominal dimensional factors $d$, representation $r$, and linear/point kind $p$. |
| $\mathsf{Descriptor}(k)$ | A first-class declaration, participant, type, domain or metadata descriptor contract. |
| $\mathsf{Callable}(k,I,R,A)$ | Callable category $k$, ordered input slots $I$, output $R$ and authority/effect guarantees $A$. |
| $\mathsf{Many}(f,D,[\ell,u],q,o,c)$ | Members of form $f$ in domain $D$ and the specified collection guarantees. |

An ordinary omitted collection specification means $[1,1]$; the omission remains source provenance. In an immutable stored field with an initialiser, omitted outer cardinality instead inherits the exact external shape of that initial value. A dictionary remains one outer value independently of its association count. An outwardly mutable field keeps $[1,1]$ when omitted. A bare star is resolved against the applicable effective limits, not against a guessed finite runtime population. All actual collections are finite even when their static upper bound is unbounded. Nested collections occupy members without implicit flattening.

For exact dictionaries the bracketed specification immediately following -> constrains associations, not a collection of independent dictionaries. For functional dictionaries type-adjacent specifications constrain complete input/output values, independently of residual-policy population and selection mode. Each arrow-owned omitted cardinality follows the owner matrix in [[17-dictionaries#Omitted cardinality and owner contracts]]: infer immutable initializers and derived bodies, retain [1] for mutable stored exact dictionaries and type-only contracts. Inference is static over admitted inputs/views, not the first invocation. Written bounds are checked before an inferred policy can satisfy a positive-minimum receiving contract. The value contract may itself contain a collection or another dictionary. String is a positional sequence as one basic value, not Char with a collection-order modifier.

> [!rule] MUD-TYPE-002 — Well-formed type constructors
> Every referenced declaration must be visible and have the required category. Cardinalities have nonnegative integral lower bounds and upper bounds no smaller than their lower bounds. Keyed paths and order paths must be statically meaningful and satisfy their stability contracts. Dictionary arrows must be the complete outer form, including after resolving representation aliases. A collection specification after a complete union qualifies that union; it does not qualify only its last alternative.

Action/subaction callable output is fixed to the single ActionReply contract; it cannot be specialised into an additional domain-result output. The nominal collection alias Errors is one union alternative in ActionReply. Resolving it as an alias does not create anonymous per-alternative collection syntax. No empty structural literal or general intersection syntax is introduced.

> [!rule] MUD-TYPE-027 — Independent nested collection layers
> Repeated specifications wrap the preceding complete member contract from left to right. Every layer independently satisfies its cardinality, domain, uniqueness, order and authority obligations. Neither nested values nor singleton-empty members are flattened. Empty and [] have zero outer members; [empty] and [[]] have one empty collection member and compare equal under compatible context, but unequal to empty.

Int [0] [1] admits one empty inner collection; Int [0] [0] admits no outer member. Int [3] [*] fixes each inner length at three; Int [*] [*] does not imply rectangularity. Empty still requires a zero-admitting outer context and cannot choose an ambiguous nominal member type.

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

Arguments likewise have no direct outer domain, cardinality or modifiers. A named representation alias may wrap a complete shape: `alias CatQueue := Cat [* ordered]` admits `Box with CatQueue`; `Box with (Cat [*])` is invalid. A suffix after the complete application, as in `(Box with Cat) [*]`, shapes the outer Box collection, not its Cat argument. Grouped member unions such as `Box with (Nat | String)` are also admitted without per-alternative collection/domain syntax. An ungrouped `|` combines the surrounding complete type, not generic arguments. Product arguments are admitted, with each component retaining its ordinary complete contract. Substitution replaces the member form at a parameter occurrence; the occurrence supplies its own outer domain/collection contract. It neither flattens a collection-valued argument nor fuses its inner shape with the occurrence's outer shape. Keyed order/uniqueness requires bounds proving the relevant paths and contracts.

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

Recursion at the same application, mutual recursion and permutations of a finite argument tuple may close a finite graph. A constructor that recursively demands itself with `List with T`, then List of List and so on, does not. A finite closure certificate enumerates application identities, roots and all substituted outgoing applications, with every edge inside that set and all bounds discharged; it is not a depth cutoff or a visited-pair assumption. Generic body checking additionally establishes this obligation parametrically for admitted inputs. The applicable normative finite-analysis procedure governs conservative closure certification; implementations cannot independently choose a stronger admission procedure. A completed analysis without a closure proof requires a static diagnostic, not truncation or runtime type creation. Closure finiteness does not establish productivity or enumerable value populations.

## 4. Finite recursive values and productivity

Let $N$ be the finite set of constructor nodes. Define the monotone operator $F$ on subsets of $N$: add a nonrecursive inhabited leaf; a concrete product whose required components already have finite witnesses; a union with a witnessed alternative; or a zero-minimum container whose empty value meets its complete contract. A positive-minimum container additionally requires enough valid members or associations: uniqueness, key uniqueness, order and domains cannot be ignored. An abstract alias receives witnesses only from admissible concrete specialisations.

Starting with $X_0=\varnothing$, compute $X_{i+1}=X_i\cup F(X_i)$ until equality. At most $|N|$ strict additions are possible. The fixed point identifies constructor paths admitting finite witnesses. Defaults count only after their own finite value and contract have been checked.

> [!rule] MUD-TYPE-004 — Productive recursion
> A mandatory recursive constructor cycle without a finite exit is invalid. A recursive type edge does not create a cyclic value reference. Every constructed alias value is a finite immutable tree. An abstract alias cannot be constructed or be the exact target of a nominal cast.

> [!rule] MUD-TYPE-016 — Acyclic domain evaluation
> A computed domain cannot depend directly or transitively on its own evaluation. Static admission must establish acyclicity across the calculations/callable dependencies needed to obtain it; a potential unresolved circular dependency is not a proof. No least/greatest fixed-point semantics is admitted for recursive computed domains.

> [!rule] MUD-TYPE-034 — Stable stored interval bounds
> Interval bounds restricting stored fields or stored locals must be stable for the binding's lifetime. Their evaluation cannot depend directly or transitively on mutable state. A pure acyclic expression is insufficient if it reads mutable data. An immutable captured scalar can supply a bound; an immutable handle does not freeze mutable fields reached through it. No endpoint snapshot is implicit.

Derived fields and locals defined by := may retain dynamic interval bounds and domains. On each demanded read, compute the derivation and domain in the same applicable semantic view, retain their transitive dependencies, apply the specified transformations and then check cardinality. An already captured collection retains its ordinary value. This rule does not freeze domain members, restrict every named state-dependent set or change participant-domain admission.

Reading an already stored value from the inherited coherent view does not evaluate that value's domain again. Several candidate-field contracts may read already available stored values without a circular domain calculation, but stored interval endpoint reads must independently satisfy stability. This does not permit circular initialisers or remove ordinary field/write/checkpoint validation. Cyclic point-domain normalisation, nominal type recursion and dependency cycles of computed domains are distinct.

Domain obligations are separate from constructor reachability. An empty or state-dependent domain does not acquire a witness from a basic type's unrefined inhabitation. A supplied/default value can witness inhabitation only after its domain check. Without such evidence the analysis must not claim unconditional inhabitation. A well-formed contract may denote no values in a projection; no automatic value is selected to repair it.

**Finite-witness lemma.** Every node admitted at iteration $i$ has a finite constructor witness whose children were admitted earlier. Proof is by induction on $i$. Conversely, any valid finite witness is admitted by induction on its tree height, provided its leaf/domain obligations are witnessed. This does not prove that all state-dependent domains are decidable.

## 5. Proof obligations and enumeration

A proof is a finite derivation from declared guarantees, established flow facts, normalised exact arithmetic/interval relations, or exhaustive evaluation of a proven finite canonical enumeration. Each use names its premises; a solver's unsupported assertion, a recursive call to the same unproved fact, or an observation of one runtime sample is not a proof.

The mandatory elementary rules include reflexivity, transitivity, intersection elimination, inclusion of normalised finite interval unions, interval arithmetic, declared nominal ancestry, constructor rules in this chapter, and checking all members of a finite explicit enumeration. Unbounded/symbolic predicates may remain unknown. Unknown differs from false; mandatory static obligations cannot be discharged by unknown.

For a domain $D$, canonical enumeration requires a finite sequence with no duplicates whose set equals $D$, with the order required by the domain. Evidence may be a finite explicit set; a bounded integral/scale-two progression; an exact stepped rational progression with a compatible nonzero signed step; a finite family; a finite linked-world population snapshot; or finite products/unions/filterings of already witnessed domains. A filtering predicate must terminate and satisfy its owner's purity/determinism requirements. Unstepped general Num intervals, Rum intervals and Any have no admitted finite canonical domain enumeration. Rum binary64 values are mathematically finite/countable; the restriction on its numeric domain/interval enumeration is a language contract. Explicit finite Rum collections/sets obtain enumeration from their supplied members. Num's exact rational domain is countably infinite; bounded rational endpoints alone do not supply a finite enumeration.

A static stepped domain uses the established signed progression to define membership: positive differences anchor at the lower bound, negative differences at the upper bound, and open starting bounds advance before the first candidate. Canonical materialisation orders the resulting members according to the domain, rather than copying descending traversal order. Finite bounds and nonzero compatible advance establish a finite number of candidates; zero advance cannot establish termination.

Enumeration of a recursive constructor type needs an explicit finite rank bound and finite branching evidence; induction on the bound reduces enumeration to finite constructor products whose domain contracts are already established. Finite individual trees alone supply no bound on the set of trees. A finite rank does not license circular evaluation of computed domain definitions.

> [!rule] MUD-TYPE-005 — No guessed proof
> Mandatory static inclusion, writable invariance, termination and finite enumeration require evidence. Runtime admission checks may validate a particular value only where that context permits them; they cannot justify universal callable substitution or an unproven enumeration.

> [!rule] MUD-TYPE-033 — Mandatory finite enumeration basis
> Implementations must support the specified elementary proof rules and established finite source constructions. A finite collection snapshot needs no uniform finite static size bound. Enumerating a domain requires a complete finite canonical enumeration certificate; producing the source and evaluating each body retain their independent termination obligations. Unknown mandatory proof obligations are rejected statically, without trial truncation or a negative runtime answer.

The minimum basis comprises finite explicit sets/collection snapshots, closed finite families, bounded integral or Money progressions, exact stepped rational progressions, finite linked-world population snapshots, and justified finite products/unions/filterings of enumerated domains. Use the premises and elementary inclusion/arithmetic rules above. A filter does not make an unenumerated infinite source enumerable; take does not turn all Int into a lazy prefix operation. Exact normalization, proof search and completion follow [[types/finite-static-certification]]; body termination follows [[types/termination-certification]]. A finite container value supplies no finite bound on all future worlds or recursively generated values.

> [!rule] MUD-TYPE-035 — Uniform normative analysis and diagnostic outcomes
> All conforming implementations of one language version must reproduce its normative certification procedure. A reusable reference analyzer may supply it; stronger optional analysis cannot independently expand admission. A proved violation and a completed analysis leaving an obligation unproved require distinct static diagnostic reasons. Resource-interrupted analysis reports incomplete tool verification, not a judgement that the program is invalid. These outcomes introduce no source-language values or runtime error types.

The procedure includes its normalization, search and completion conditions, not merely a collection of inference rules. An implementation's memory/time/depth limit cannot silently constrain a mathematical domain or replace obligatory elementary evidence. Finite source admissibility, body termination and finite reachable-state analysis remain distinct obligations. Source/application and body proofs follow the fixed procedures above; advanced reachable-state profiles require their separate evidence and do not permit implementation-dependent admission.

### Dimensional normalization

> [!rule] MUD-TYPE-037 — Dimension and representation checks are independent
> Normalize admitted linear dimensions by original base magnitude anchors and integer exponents. Check every original numeric signature and representation obligation before using factor equality. Cancellation does not authorize unsupported arithmetic, erase nominal identity, remove point/cycle kind or move rounding across source operations.

For each independent linear base magnitude $a$, including a unitless one, define $d(a)=\{a\mapsto1\}$. For a derived product/quotient, add/subtract exponent maps pointwise, remove zeros and order remaining anchors lexicographically. The neutral map is empty; no new nominal base or dimensionless cast is synthesized. Integer powers here are metalanguage generated by products/quotients, not additional source syntax.

Check declarations and equivalences as a finite dependency graph. Compute strongly connected components; reject a nontrivial component or self-edge. Process remaining nodes in topological order, using canonical anchor order to break independent-node ties. Root units have scale 1. A checked positive equivalence to an already normalized compatible quantity supplies the alternative unit's canonical scale; reduce its canonical coordinate to a positive numerator/denominator pair. Multiplication/division of unit expressions multiply/divide these ratios; an enabled SI prefix multiplies by its exact decimal power. Reject zero/negative equivalences, incompatible dimensions, undeclared/disabled prefixes, missing/multiple forbidden roots and dependency cycles under their existing declaration contracts. No arbitrary predicate solving or invented fallback units are needed.

A derived magnitude's canonical unit is the normalized structural product/quotient of component roots; it may declare compatible alternative units but no new root. Identity remains the declared magnitude identity. Two independent unitless magnitudes have different base anchors, even though neither has a printed unit. Equal normalized factor maps justify dimensional compatibility only; nominal construction/conversion still follows the relevant context's rules. Point coordinates use their established linear difference and point/cycle contracts, not an implicit linearization.

For example, Length/Time and Length*Time/Time/Time have the same factor map. Length*Length normalizes to exponent 2; it does not become a new anonymous nominal base. The scales of km/h and m/s are 5/18 and 1 relative to meter/second, so 90 km/h has canonical coordinate 25 in exact compatible representations. This scale relation does not permit transforming arbitrary runtime arithmetic across representation-rounding sites.

Select representations recursively in original source grouping using [[21-expressions#4. Numeric, dimensional and Boolean operators]]. Nat/Int/Num products follow their widening rules and division yields Num. Money*Num and Money/Num yield Money; Num*Money yields Money; Money/Money yields Num; Money*Money and scalar/Money remain invalid. Money result sites round to hundredths ties-to-even and then check domains. An explicit representation annotation requires the existing representability evidence and introduces no rounding or implicit conversion. Thus a dimensionally canceling expression can still be rejected for an unsupported intermediate representation signature.

The dimension/scale procedure takes checked canonical equivalence values as input. Rum literal/constant evaluation and derived representation follow MUD-TYPE-038 below. Factor normalization never rewrites floating-point computation across its rounding sites.

### Portable Rum values and static evaluation

> [!rule] MUD-TYPE-038 — Portable binary64 sites and canonical values
> Rum literals and admitted arithmetic use round-to-nearest, ties-to-even binary64, with subnormals and gradual underflow. Each source arithmetic site rounds independently. Preserve observable errors/dependencies and actual demand during constant evaluation. No implicit exact/Rum or Money/Rum signature is created. Nonfinite values and division by zero remain faults; all zero results normalize to positive zero.

Define RN(t) for a nonnegative exact rational t as its nearest integer, choosing the even integer on a tie. For exact rational x, let a=abs(x). If a=0, return canonical positive zero. If 0<a<2^-1022, compute k=RN(a*2^1074). Return the signed subnormal k*2^-1074, except k=0 returns positive zero and k=2^52 is the minimum normal. Otherwise choose the unique integer e with 2^e<=a<2^(e+1), and k=RN(a/2^(e-52)). If k=2^53, replace k by 2^52 and increment e. If e>1023, the rounded result is outside finite binary64 and supplies a fault. Otherwise return sign(x)*k*2^(e-52). Comparisons/rounding use exact integer/rational relations, not a host decimal approximation. The overflow midpoint is handled by this same carry rule, never by clamping to the largest finite value.

The finite canonical word has the IEEE binary64 sign, exponent and fraction fields. For a nonzero normal result, exponent=e+1023 and fraction=k-2^52. A subnormal has exponent=0 and fraction=k. Canonical zero is the all-zero word. Use exactly 16 lowercase hexadecimal digits when a textual semantic bit-pattern label is required. This fixes value identity for normalized constants and signature-domain labels; it does not prescribe physical IR fields, file encoding or foreign ABI.

Decode a decimal literal's digits and exponent into an exact rational first, then apply this procedure once. A pure Rum literal requires r; the established Rum-magnitude unit context may omit r. Unary signs are separate operators. A nonfinite/unrepresentable literal is statically invalid. Subnormal literals are valid and tiny literals may become zero; their contextual domain/cardinality admission remains required. Num to Rum uses the same procedure; Rum to Num recovers the exact rational of the canonical finite value. Subsequent explicit integer conversion retains the existing quantitative ties-to-even contract.

For Rum operands, +, -, * and / compute the mathematical operation on their represented finite dyadic values and round once at that source site. A zero divisor faults. Unary minus changes the sign of a nonzero value and leaves canonical zero. Comparisons use the represented numerical values. For a%b with b nonzero, let q be truncation toward zero of the exact mathematical a/b; compute a-q*b and round to Rum. Do not calculate q through a rounded Rum division. Thus (-r5.5)%r2 is -r1.5; r5%r3 is r2. A zero remainder normalizes to positive zero.

Every expression site has binary64 intermediate precision; wider host registers cannot change results. a*b+c has a multiplication rounding followed by addition rounding. Automatic FMA contraction, reassociation or constant folding is permitted only when it preserves the complete observable value/fault/demand contract. No implicit fast-math mode or source FMA operation is established. Required static owners must produce a normal admitted result after applicable recovery; executable computing faults retain the ordinary error channel. Staged effect consolidation retains its specified algebra/rounding stages in [[28-effects]] rather than acquiring an accidental host evaluation order.

Unit construction consumes its checked numeric value, converts its coordinate using the symbolic exact canonical unit factor and rounds the resulting Rum coordinate. The exact factor belongs to unit elaboration, not a new implicit source arithmetic signature. Domain validation follows canonical result construction. All operands of a derived magnitude's representation expression must admit their original operation signatures: Rum-only product/quotient results are Rum; mixed exact/Rum or Money/Rum is rejected. Annotation cannot silently convert components. Dimensional equality does not rescue an unsupported numeric signature.

### Exact remainder

> [!rule] MUD-TYPE-039 — Exact truncating remainder
> Nat%Nat yields Nat, Int%Int yields Int and Num%Num yields Num. Mixed operands use the exact Nat-to-Int-to-Num widening chain. With nonzero divisor b, let q=trunc(a/b), where trunc is mathematical integer truncation toward zero; the exact result is a-q*b. A zero divisor supplies Fault under ordinary demand and recovery rules. Money has no remainder signature and %= is not introduced.

For a nonzero remainder its sign is the dividend's sign and its absolute value is below abs(b). Thus (-5)%3=-2, 5%(-3)=2 and (5/2)%1=1/2. This internal quotient is not a source integer conversion and does not use its ties-to-even rule. Existing arithmetic member lifting retains its static cardinality/signature premises; no member computation occurs for empty inputs.

### Unitless point coordinates

> [!rule] MUD-TYPE-041 — Contextual coordinates without units
> A point with no ~format over a magnitude without admitted unit presentation accepts a bare numeric literal only under one unique expected point type. A typed numeric expression must use explicit to Point, applying its quantitative representation/domain checks. Absent unit text neither removes nominal factors nor grants conversion between unrelated nominal magnitudes/points.

A source literal must satisfy the point domain before cyclic normalization; coordinate materialization through to cannot silently repair an invalid value. Ordinary runtime point arithmetic retains the declared cycle contract. Unit presentation/extraction requires actual compatible units and is unavailable in this case; no synthetic unit or new format hole exists. Rum numeric literals keep their r prefix without a unit context. Existing point formats retain their separate invertibility and canonical-rendering requirements.

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

Read-only exact dictionary values may widen covariantly. Their key contract must preserve all lookups admitted by the target: every target key must be admitted by the source key contract. Association/domain/modifier guarantees must also hold. This is query substitution, not permission to replace keys or values. Any writable dictionary destination is checked invariantly at its stored root. Functional substitution checks complete input contravariance, output covariance and the termination/effect contract. It does not change the supplied policy's branch-selection behaviour; selection mode is a property of that value, not a type dimension.

## 7. Representation equivalence and explicit construction

Representation equivalence compares complete constructor labels after nominal representation wrappers are exposed. Product arity, component names/order, underlying component forms, collection cardinalities/modifiers and dictionary nesting must match. Defaults are not components and do not change shape. Domain refinements are separately validated at the target; they are not silently satisfied by shape equivalence.

For recursion, initialise the finite set of candidate node pairs with matching local constructor labels. Repeatedly remove a pair if a required child pair is absent; compare all ordered product children and all required alternatives, not one sample. The greatest fixed point is a finite labelled bisimulation. Every surviving pair must satisfy all its local conditions. Revisiting a pair alone is not proof. This relation establishes representational compatibility for conversion, not nominal subtyping or inhabitation.

> [!rule] MUD-TYPE-006 — Contextual nominal construction
> An untyped basic or structural literal may acquire a unique concrete expected alias type while constructing all its components. Positional construction supplies every component. Named construction retains declaration order and may omit only components with explicit effective defaults. Already typed values keep their nominal identity and require an admitted explicit conversion to acquire another.

An explicit nominal cast requires representation equivalence and validates destination domains and guarantees without rounding or changing the underlying contents. Quantitative conversion is a different family: it checks numerical/dimensional compatibility, applies the specified rounding where required, then validates the destination. Casting never creates world identity or grants a capability.

Two context-free structural literals do not supply each other with a nominal comparison context. An already typed alias operand may supply its type to the opposite untyped compatible literal.

Normal and sub operations retain distinct declaration identity: `subaction <: action`, `sublook <: look` and `submessage <: message` in the descriptor hierarchy. Widening does not confer host capability. Only normal operations from shared files are host endpoints; any possible sub or part-only alternative requires narrowing/proof before host admission. Mud calls across parts use direct uses permission. Sublook is pure in every ordinary reading context, including a look body; submessage is a causal source with the ordinary on/when contracts but no external endpoint. Each look/sublook/message/submessage declaration has its own static produced type.

### Value equality support

> [!rule] MUD-TYPE-040 — Functional values have no equality
> FunctionalDictionary does not admit value == or !=. A comparison of aliases, tuples, collections or exact dictionaries is likewise inadmissible when comparing their stored contents requires functional value equality. Nominal wrapping cannot grant that operation. All remaining possible compared static alternatives must support equality; missing proof cannot be replaced by inspecting current runtime contents.

Apply this exclusion through equality's stored representation/component/key/value edges in the finite normalized type graph. Derived fields, family associated data and metadata are not stored equality payload and do not create such edges. A container with proven maximum zero has no compared-member edge; comparing its empty content does not compare a functional value. Productive finite recursive values do not become unequal merely because their type graph is recursive; the exclusion applies when a compared reachable form is functional. This is a restriction on existing equality contracts, not a new source trait or public TypeKind.

Exact dictionary keys, ordinary unique, whole-value membership/algebra and order comparisons cannot use an unsupported required equality. A stable unique by path can use a supported projected key without comparing the complete functional payload; it does not make ordinary whole-value equality or collection algebra available. Any claim of whole-value uniqueness is conditional on the member type having that equality. Automatic on binding sets and temporal changes also require equality for the values they actually compare; unsupported functional participant values cannot gain an internal equality implementation from binding syntax. Thing identity and family member equality do not compare ordinary fields or associated data. Functional FirstMatch is branch selection, independent of output order and a value comparator. Application and noncomparing filtering/traversal retain their established contracts. Type ===/!== below compares normalized contracts, not functional behavior, branch bodies or runtime captures.

### 7.1. Exact structural type equality

> [!rule] MUD-TYPE-020 — Structural equality of normalized contracts
> `===` compares two Type operands by their entire normalized effective contracts, erasing only alias nominal identity. `!==` is its exact negation. Things and families, including their applications, are nominally opaque: distinct exact identities never become equal by matching fields or members. Ordinary value equality, nominal `is`/`iis` and representation compatibility for `to` retain their separate contracts.

Compare member names and declaration order, stored/component versus calculated kind, complete member types, domains, cardinality, multiplicity, uniqueness and its key criterion, order and its criterion, inner authority, product composition, nested collection layers, dictionary grouping and normalized union alternatives. Callable contracts retain inputs, outputs and authority guarantees. Alias representations and effective inherited schemas participate after substitution. Metadata, presentation names, documentation, defaults and calculated bodies do not participate; a default or body that changes an inferred effective type/shape affects comparison through that resulting contract. Hence calculated `let x: Nat := 1` and `let x: Nat := 2` match, while stored and calculated x do not.

Domain equality uses normalized symbolic contracts, including resolved provenance, binders and generic substitution, plus the defined exact arithmetic/interval normalization. It does not evaluate current populations or arbitrary predicates to prove semantic equivalence. Different symbolic predicates do not become equal because they currently yield equal sets. Union order/duplicate syntax is normalized; match the complete normalized alternatives without source-order dependence. Nominally distinct alternatives retained by ordinary union normalization are not silently removed by representational matching or semantic inclusion. No general program-equivalence oracle is required.

For recursive admitted type graphs, compare a closed finite relation of node pairs: all local structural labels must match and every required child pair must belong to the relation. Alias identity is omitted from these labels; opaque thing/family labels retain constructor and exact argument identities. Greatest-fixed-point labelled bisimulation handles recursion without comparing sample values. Merely visiting a pair is not evidence. The relation is exact equality of this normalized contract representation, not the weaker conversion representation relation $\cong_R$.

```mud
alias A { let x: Nat; let y: String [0..1] }
alias B { let x: Nat; let y: String [0..1] }
rule SameStructure { A === B }
rule DifferentOrder { String [*] !== String [* ordered] }
```

Both types may be exposed as Type descriptors without adding application anchors. Descriptors retain source constructor and argument information; member `~anchor` denotes the source declaration and `~type` the effective applied type. Their public categories follow the complete fixed TypeKind catalogue below; structural comparison introduces no additional intrinsic metadata spellings.

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

Synthesis is bottom-up; checking passes an expected contract down into untyped literals and callable arguments. Each stored binding/declaration has its required initialiser/default under its owner contract. Ordinary field/local annotations may be omitted; written annotations may contain inference holes only when the declaration has its own initial value. Calculated bindings preserve their synthesised type unless an explicit shape requires checking or a declared derived transformation.

For a type-correct value whose domain/cardinality may fail, checking records a site-specific predicate obligation only where runtime admission is authorised. A known invalid static initialiser is rejected. Call admission reports the appropriate refusal; an ordinary value computation uses its Error channel. Mandatory post-effect stored cardinality proof is not replaced by such an obligation.

When an expression produces alternatives, consider their common supertype candidates under the proven inclusion relation. A unique most-specific informative candidate may be used. Any alone is not informative and cannot erase the original alternatives during synthesis. Several incomparable minima retain the normalised original union, as does absence of a more informative common candidate. Expected types may check each alternative but cannot force a nominal cast or resolve a nominal call target.

For a successful is test, $\Phi$ retains the compatible nominal alternatives; its false branch excludes only alternatives established impossible. Iis tests exact effective nominal identity; its negative case may still contain descendants. Narrowing on a mutable read is invalidated when an intervening effect may change that place or dependency. It never creates authority.

> [!rule] MUD-TYPE-008 — Unique inference
> An omitted type is inferred only when synthesis and the available context determine a unique contract, or a defined union join. Otherwise an annotation/narrowing is required. Context-free empty has cardinality zero and no chosen nominal member type; it can be checked against a zero-admitting expected collection, but cannot select a family member, world identity or type default.

### 9.1. Stored type-inference holes

> [!rule] MUD-TYPE-021 — Unique stored-hole solution
> In a stored annotation with an initial value, each `_` stands for one omitted static member type. Holes may occur recursively in otherwise admitted product, generic-argument, callable and dictionary type positions. Solve the complete annotation and initialiser jointly, using written structure and established domain/type evidence. Every hole must have one uniquely determined normalized type. Unsolved, inconsistent or ambiguous holes are compile-time errors, with tooling marking the hole's source span. No unresolved hole reaches runtime. A hole is not Any, a wildcard, dynamic typing or a fresh nominal type, and insufficient evidence never falls back to Any.

Each written hole is an independent inference occurrence; two underscores do not implicitly equate their solutions. An already established Any source contract may itself be the uniquely synthesized type, but Any cannot be guessed to repair missing evidence. Propagate the written expected structure into components of the initialiser and synthesize missing component contracts where unique. Several source spellings for the same normalized exact type are one solution; structurally equal but nominally distinct aliases are different possible solutions. Do not enumerate nominal aliases to invent a contextual construction. Defined union synthesis retains its ordinary rule; a union of possible guesses is not a solution for an ambiguous hole. A generic application is checked only after its arguments are resolved, with ordinary bounds, variance and finite-closure obligations.

`let pair: (_, String) = source` succeeds when source and written constraints determine the first component uniquely and the second meets String. `let pair: (_, String) = (empty, "hello")` fails without additional evidence for the first member type. `let values: _ = empty` fails; `let values: _ in Cats [*] = empty` succeeds only if the domain contract supplies unique type evidence. Mutable stored annotations admit holes with the same rule; subsequent assignments obey the inferred fixed contract and ordinary writable invariance.

Written domains, cardinalities, uniqueness, order and authority remain stored admission constraints, never coercive derived transforms. Omitted shape retains the owner policy, including initializer-shape capture for immutable stored fields, body-result inference for functional definitions, and the singleton default for mutable fields and type-only contracts. Dictionary arrow-owned counts and exterior cardinality are resolved independently under [[17-dictionaries#Omitted cardinality and owner contracts]]. No hole infers missing bounds or creates authority. Schema/default/metadata initialisers retain their closed-static requirements. Hole syntax is unavailable in participant/given signatures, generic parameter bounds, alias representation definitions, derived annotations, ordinary casts or standalone Type expressions.

### 9.2. Pattern typing

> [!rule] MUD-TYPE-022 — Exact positional binding
> Check a binding pattern against its complete source contract. Names capture the corresponding component; `_` checks the same position but binds nothing. A positional node requires an admitted singleton positional product of exactly its arity and recursively checks its components. Named products cannot be opened. Every statically possible source alternative must admit the pattern and yield a unique contract for every named capture under the ordinary inference rules. Shape mismatch is a static error, not a filter or a runtime failed match.

Nested products may remain whole under a name or be opened recursively. An already nominal alias is not implicitly cast into an anonymous product to enable a pattern; its exposed positional representation, where available under the ordinary alias contract, supplies projections while the original source identity remains intact. Exact-dictionary traversal admits a two-position association pattern with key/value contracts; this exception does not make associations ordinary products. Nested positions inside that pattern follow ordinary positional-product rules. Iteration, selection and quantifiers bind one admitted source item/association at a time; a collection-valued component is not implicitly flattened.

Exact dictionaries retain key traversal for a single name or discard. A positional root of exactly two positions selects association projection, even when the key itself has a positional representation; open that key within the first position if needed. The pattern only changes available predicate/body bindings. Selection retains accepted associations, and dictionary min/max retain their original accepted key witness rather than constructing an ordinary product from key/value bindings. Step, finiteness and usable-order requirements remain those of the original traversal.

Stored local patterns evaluate the RHS once, validate the complete pattern and establish all immutable captures atomically; a failed RHS exposes no partial bindings. Derived patterns register live component projections of their common RHS. They have no writable root, and pure expression positions retain their ExpressionBlock restrictions. A completely discarded stored pattern still evaluates its RHS and enforces admission/error obligations; tooling may suggest removal only when no observable obligation is lost. Derived patterns retain derivation checks even when every component is discarded, but do not introduce eager reads or new effects solely to discard them.

## Structural views and functional schemes

> [!rule] MUD-TYPE-052 — Trait satisfaction and identity
> Structural views require accessible complete-contract witnesses under
> [[types/structural-traits]]. Preserve concrete nominal identity and existing
> authority. Satisfies is not === or nominal Specializes; iis Trait is invalid.

> [!rule] MUD-TYPE-053 — Static functional family formation
> Immutable functional definitions may synthesize correlated schemes under
> [[types/functional-families]]. Captures bind before implicit parameters;
> copy/partial application preserves constraints and contextual literal evidence.
> A mandatory unresolved or ambiguous specialization is a static diagnostic,
> not arbitrary Any, independent unions or runtime overload dispatch.

## 10. Schemas, visibility and descriptor types

Every new concrete stored thing field has an explicit initialiser; an explicitly typed abstract field may defer initialization until a concrete effective schema resolves the obligation. Alias components are all present in a value, from supplied values or explicit defaults. Family data are supplied by the schema or by every member. User-defined metadata needs an explicit effective value; intrinsic defaults retain their individual contracts.

Inherited writable stored contracts remain invariant. Immutable alias contracts may refine all inherited guarantees, with a valid effective initialiser/default where one is required. Diamonds deduplicate origins and incomparable independent members need a common explicit refinement. No runtime effect changes the set of field declarations.

Thing value admission preserves strict membership: a field whose member type is the thing declaration $T$ does not admit $T$ itself as a population member; compatible concrete descendants are admissible. A declaration descriptor for $T$ is a distinct reflective use.

Cross-part thing/alias specialisation requires uses authorisation and membership of the visible public contract's transitive type closure. Importing a path supplies no authority. Inherited initialisation is compiled under the declaring owner's access rights. Private ordinary thing fields do not become public through specialisation.

Descriptor reflection is checked against every possible static receiver category. A supported optional property may return empty; an unsupported property is a static error, never a dynamic empty fallback. A type expression obtained through type reflection must be statically established as Type; runtime-dependent type generation is invalid. Source spans and AST values are not MUD values merely because the compiler holds them.

> [!rule] MUD-TYPE-036 — Operator declaration descriptors
> An operator descriptor is a non-callable declaration descriptor. Its category property is DeclarationKind.Operator and its own public type category is TypeKind.DeclarationDescriptor. Descriptor access is read-only and obeys ordinary static visibility for every returned contract. Reflection neither selects overloads nor creates inverse signatures.

Complete signature encoding and operator reflection schema: [[names/operator-contract-identity]].

### Public TypeKind categories

> [!rule] MUD-TYPE-026 — Public exterior classification
> TypeKind is a builtin closed family, fixed for each language version and not extensible by programmes or libraries. It classifies the normalized effective public type exterior, preserving nominal identities. An alias remains Alias regardless of its representation. Applied generics retain the constructor's category; internal compiler nodes have no public kind merely by existing.

| Public form | Category |
| --- | --- |
| Nat, Int, Num, Rum, Money, String, Char, Bool | Basic |
| Any | Any |
| Nominal thing, alias, family | Thing, Alias, Family respectively |
| Anonymous tuple, collection, union, interval | Tuple, Collection, Union, Interval respectively |
| Exact dictionary; functional dictionary/family | Dictionary; FunctionalDictionary |
| Structural trait contract | Trait |
| Linear magnitude; point magnitude (including cyclic points) | Magnitude; PointMagnitude |
| Produced look/sublook result; message/submessage payload | LookResult; MessagePayload |
| Action/subaction callable; look/sublook callable; Boolean-rule callable | ActionCallable; LookCallable; BooleanRuleCallable |
| Type, field, component, participant, metadata, domain descriptor | TypeDescriptor, FieldDescriptor, ComponentDescriptor, ParticipantDescriptor, MetadataDescriptor, DomainDescriptor respectively |
| Declaration descriptor without a more specific established category | DeclarationDescriptor |

Reactive/always rules do not acquire a BooleanRuleCallable category. Exact nominal identities and generic arguments remain available independently of kind. Public names do not change product notation or AST constructors. TypeKind itself is a family and has category Family. Its members follow ordinary closed-family identity, equality and finite enumeration. Future language versions may change the catalogue only through their specification. The table is the complete MUD 1.0 core constructor catalogue. Every public contract must project through one of its forms; compiler-private tags cannot add public categories. The supporting builtin inventory below covers the established reflective/error types. Fixed-target compatibility follows [[01-scope-and-conformance]]; project target declaration and persistent migration protocols remain separate version-scope work.

Normalize before classification: Int | Int has kind Basic, whereas a nominal alias represented by Int has kind Alias. Collection specifications [3], [*], [3 ordered] and [3 unique] all project to Collection; Int [*] [*] is also Collection because its exterior is a collection. Cardinality, guarantees and element types remain separate reflective contracts. DeclarationKind classifies a described declaration; TypeKind classifies the descriptor's own type. Field descriptors and component descriptors have different TypeKind members even though they share structural properties.

### Supporting builtin inventory and complete projection

| Established builtin forms | Projection |
| --- | --- |
| Name, Anchor, MudPath, MudFile, Cardinality, Order | Alias. Payload APIs are not determined by category. |
| Prefix, TypeKind, DeclarationKind, RuleKind, ActionKind, FieldKind, ClauseKind, ParticipantClause, MetadataKind | Family. Prefix has the fixed SI member catalogue. |
| Success, Refusal, ConditionRefusal, IfRefusal, AfterRefusal, AlwaysRefusal, ArgumentRefusal, BoolCheck, Error, Errors, ActionReply | Alias, including abstract aliases and aliases represented by a collection or union. |
| Type, Field, Component, Participant, Metadata, Domain descriptor contracts | Their specific TypeDescriptor, FieldDescriptor, ComponentDescriptor, ParticipantDescriptor, MetadataDescriptor, DomainDescriptor categories. |
| General Declaration/Rule, FamilyMember, Unit and operator declaration descriptor contracts | DeclarationDescriptor when no more specific established callable category applies. A unit descriptor is not a first-class unit expression or quantity. |
| Effective Action/Subaction, Look/Sublook and Boolean-rule callable contracts | ActionCallable, LookCallable and BooleanRuleCallable. A generic declaration descriptor view is not automatically callable. |
| Operator operand description record | Tuple; its containing ordered list is Collection. No new descriptor category or anchor. |

A simple unrestricted singleton specification, whether omitted or written, is a default wrapper and does not classify bare Int as Collection. A redundant unrestricted Int [1] confirms the same default singleton contract and is Basic. A nondefault collection form such as Int [0], Int [*], or an ordered/unique/nested collection layer is Collection. A nominal alias of any such form remains Alias; its schema does not leak through kind projection. Normalize duplicate unions before projection. A genuine remaining multi-alternative union is Union, even if all alternatives share one category. A generic application follows its constructor category, not GenericApplication. Cyclic points remain PointMagnitude. This recursion on the normalized public exterior terminates on the admitted finite type graph; nominal leaves do not require representation unfolding.

For a fixed language version, the TypeKind member set, its spellings and this projection are invariant across compiler releases. A later catalogue applies only to a different selected language version; it is never silently merged into this one. Rechecking source under a new version may require changes to exhaustive family use. No unknown-kind fallback or automatic migration is implied. DeclarationKind.Operator and DeclarationKind.Trait classify their declarations; their descriptors remain DeclarationDescriptor. TypeKind.Trait classifies a structural trait contract, not a user-extensible kind.

The catalogue has no members for host-only Ticket states, Normal/Fault block outcomes, the erased marker, AST/CST/HIR nodes, compiler proof objects, unit spellings, part/file syntax nodes or generic binders. A public immutable MudFile value still uses its nominal Alias category; that does not expose a file syntax tree. These exclusions do not prohibit explicitly supported reflection values.

## 11. Results and errors as types

Success is a nominal alias supplied by successful action evaluation. The interface for obtaining the incorporated textual patch, including any Success component, remains Q-073; no additional component/type is defined here. It remains part of the sole ActionReply result, not an action-specific domain return. Refusal and Error are abstract structural aliases. IfRefusal, AfterRefusal and AlwaysRefusal are ConditionRefusal specialisations; ArgumentRefusal identifies the argument role. Refusal/Error require reason and Declaration origin. Error has an optional finite cause; ConditionRefusal has the BoolCheck trace of the actually evaluated final Boolean expression.

Errors is a nominal alias of a nonempty Error collection; ActionReply is the nominal alias of the union Success | Refusal | Errors. Producing an Error or obtaining an ActionReply containing Errors is ordinary value production. Entering a block error channel is a separate evaluation outcome. Every block has an Error collection channel allowing zero occurrences; its normal result is available only when that channel is empty.

Otherwise roles bind only Error specialisations, conjunctively and by occurrences. A then recovery checks against the protected block's normal contract and permissions; raise checks one Error or a nonempty compatible Errors collection. Refusal is never an Error binding. Explicit raise in executable bodies has the same payload contract and no normal value; checking-only result contextualisation follows [[21-expressions#9. Blocks and error recovery]]. [[21-expressions]] defines the block typing rules.

### Diagnostic provenance and privacy

> [!rule] MUD-TYPE-042 — Private diagnostic references grant no authority
> The original Error.origin, Refusal.origin and ArgumentRefusal.argument components may retain private declaration/participant references across a public boundary as read-only diagnostic provenance. Recognition is by original inherited component identity, not field spelling. This exception does not export a private diagnostic subtype, arbitrary additional private payload or operational/schema authority.

The reference preserves canonical identity. Its supported intrinsic identifier/anchor/path/file/category information may be observed; ordinary property-category checks remain mandatory. Invocation, state access, private schema/participant/ancestry reflection and arbitrary configured metadata are not granted. Static ~type retains its existing contract and privacy obligations; no private signature/type frontier becomes visible from diagnostic receipt. Independent visibility rights are separate. Finite Error cause chains/diagnostic containers retain the same component-scoped exception when their value types are otherwise visible. Copying, widening or narrowing cannot launder it into an ordinary visible declaration or host endpoint; export elsewhere remains prohibited. No new source descriptor category or nominal identity is created.

## Contextual callable destinations

> [!rule] MUD-TYPE-043 — Contextual complete call analysis
> Compute destination contexts and transitive summaries by [[types/contextual-call-analysis]]. Preserve demonstrated nominal input contexts and use the compatible legally obtainable catalogue for unknown inputs. Every remaining alternative retains its signature, permission, dependency, effect and acyclicity/termination obligations. No runtime scan, expected-result selection or source execution supplies missing evidence.

> [!rule] MUD-TYPE-044 — Normative recursive body certification
> Functional dictionaries, Boolean rules, looks/sublooks and alias operator bodies may use recursion only with [[types/termination-certification]]'s strict continuing-edge certificate. Finite natural tuples, same-declaration phases, actual finite Rum order and exact affine scalar synthesis are supported. Independent action/test, domain and definition-cycle prohibitions remain mandatory.

> [!rule] MUD-TYPE-045 — Complete finite certification procedure
> Mandatory source/application finiteness and elementary proof decisions follow [[types/finite-static-certification]]. Its fixed normalization, supported abstraction, search and completion distinguish established violation, completed-unproved rejection and tool interruption. No implementation-specific stronger solver may expand admission under the same target.

> [!rule] MUD-TYPE-046 — Explicit structural alias construction
> A statically named concrete structural alias construction follows MUD-ALIAS-005
> in [[13-aliases]]. Check its exact applied schema, positional/named completeness,
> defaults, component contracts and permissions before producing that exact alias.
> No expected-result selection, runtime Type dispatch or implicit unpacking/cast
> supplies a missing argument or changes the constructed nominal identity.

## 12. Static acceptance and elaboration output

An accepted programme has well-formed visible schemas, finite normalised type graphs, checked declarations/expressions, all mandatory static proofs and explicitly located permitted runtime obligations. Unproven writable substitution, unsupported reflection, ambiguous inference and missing initialisation are static diagnostics.

Elaboration preserves source origins and records the selected nominal targets, effective schemas/types, literal contextualisation, operation overloads, conversions, flow facts, permission checks, effect footprints, finite-enumeration/termination evidence and runtime predicate checks. No particular semantic IR serialisation or node catalogue is required.

**Conditional safety statement.** Assume the static derivation's premises hold
in the applicable observation view, every primitive/subordinate operation meets
its established value/effect contract, trusted foreign contracts hold, and every
permitted runtime admission predicate succeeds. A completed normal result meets
its checked contract and every write uses authorised storage. Fault or Refusal
asserts no normal result. This is a local compositional statement over these
interfaces, not a theorem about the complete causal engine.

Declared storage bounds are not automatically facts at each private prefix.
The permission chapter admits temporary stored-cardinality deviations; proofs
must use the actual view and invalidate changed/dependent flow facts. A later
completion/checkpoint guarantee cannot establish an earlier predicate or erase
an earlier possible call. The finite certification procedure supplies the
conservative widening of unestablished proof bounds; it does not change the
field declaration, reflective schema or completed-storage obligation.

For finite nonrecursive derivations, composition follows induction on the
checked expression/block: admitted construction and conversion discharge their
component and destination checks; substitution preserves inputs/results and
permissions; alternatives and handlers retain the required normal-result
contract; actual-view reads use only established premises. Recursive body
composition additionally uses the certified well-founded call measure. Neither
argument assumes a missing runtime interface or proves global stabilization.

The machine-readable instances in [[types/typing-cases.yaml]] distinguish static acceptance/rejection from permitted runtime checks. Their validator checks evidence structure and finite contract witnesses; it does not parse or execute MUD programmes.

## Deferred abstract schema and tuple-input boundaries

> [!rule] MUD-TYPE-048 — Complete concrete initialization
> An abstract thing may defer an explicitly typed stored initializer. Every
> concrete descendant must resolve each required initializer under existing
> origin/conflict precedence before materialization. No uninitialized concrete
> field, implicit default or runtime inheritance of another thing's state exists.

Schema checking follows [[15-fields-and-mutability]]. Anonymous dictionary input
projection follows MUD-TYPE-047 in [[17-dictionaries]]; it ignores source component
names at that boundary only. === and explicit conversion keep their existing
name-sensitive contracts. Tuple components are not new nominal declarations.

> [!rule] MUD-TYPE-047 — Anonymous dictionary tuple input
> A structural alias may project its complete stored component sequence into
> an anonymous exact/functional input tuple with identical component contracts,
> ignoring source names and applying target names. No nominal component cast,
> extra member, hidden schema or added authority is admitted.

> [!rule] MUD-TYPE-050 — Zero-admitting policy coverage
> Functional application with a zero-admitting result cardinality may leave
> inputs uncovered and returns ordinary empty for no applicable branch. Positive
> minima require universal coverage and result proofs. Selected faults and
> omitted required results are not converted to empty.
