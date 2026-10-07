---
title: Expression and block typing
aliases:
  - Static expression rules
tags:
  - mud/specification
status: proposed
normative: true
depends-on:
  - "[[10-type-system]]"
  - "[[14-fields-and-mutability]]"
questions:
  - Q-073
  - Q-007
  - Q-023
  - Q-029
  - Q-050
  - Q-058
decisions:
  - D-140
  - D-137
  - D-136
  - D-135
  - D-134
  - D-133
  - D-132
  - D-131
  - D-028
  - D-030
  - D-032
  - D-034
  - D-039
  - D-040
  - D-047
  - D-048
  - D-049
  - D-056
  - D-058
  - D-061
  - D-074
  - D-075
  - D-080
  - D-081
  - D-086
  - D-088
  - D-092
  - D-095
  - D-101
  - D-103
  - D-114
  - D-115
  - D-118
  - D-119
  - D-120
  - D-121
  - D-124
  - D-037
  - D-066
  - D-085
  - D-126
  - D-127
  - D-129
  - D-130
---

# 19. Expression and block typing

Normal and sub operations retain distinct declaration identity: `subaction <: action`, `sublook <: look` and `submessage <: message` in the descriptor hierarchy. Widening does not confer host capability. Only normal operations from shared files are host endpoints; any possible sub or part-only alternative requires narrowing/proof before host admission. Mud calls across parts use direct uses permission. Sublook is pure in every ordinary reading context, including a look body; submessage is a causal source with the ordinary on/when contracts but no external endpoint. Each look/sublook/message/submessage declaration has its own static produced type.

## Scope and notation

The environments and synthesis/checking judgements are defined in [[10-type-system]]. Block modes, effect summaries and stored-cardinality obligations are defined in [[14-fields-and-mutability]]. This chapter supplies syntax-directed contracts for every expression family in the Surface AST, without defining the physical representation of an elaborated expression or the full evaluator.

Dynamic callable acyclicity proofs remain Q-023 and general termination methods beyond the established decreasing measures remain Q-029. Boolean pruning beyond the specified core remains Q-050; portable binary64 evaluation parameters remain Q-058. These uncertainties cannot justify an undocumented operator overload, a real effect in a pure owner or a different numeric representation.

Let $\epsilon_e$ be an expression's effect/dependency summary and $O_e$ its obligations. Composition preserves evaluation order and actual short-circuiting; it does not force evaluation of skipped operands. Element operator contracts below are lifted only where expressly permitted.

## Judgement composition

Write $\mathcal C=(\Sigma,\Gamma,\Phi,\delta)$ and $\mathcal C\vdash e\Rightarrow\tau\triangleright(\epsilon,O)$ for synthesis. Checking does not change a value's identity or the permitted owner mode:

$$
\frac{\mathcal C\vdash e\Rightarrow\tau\triangleright(\epsilon,O)\quad
\Sigma;\Phi\vdash\tau\preceq\sigma}
{\mathcal C\vdash e\Leftarrow\sigma\triangleright(\epsilon,O)}
\;\mathsf{E\text{-}Subsumption}.
$$

Contextual literal construction and explicit conversions use their own rules rather than this subsumption rule. When only domain/cardinality admission of an otherwise compatible value is unknown, E-Admission adds that exact predicate to $O$ if and only if its context admits a runtime check. It cannot be used for writable invariance, enumeration, universal callable substitution or post-effect stored cardinality.

$$
\frac{\Gamma(x)=\tau\quad x\ \mathsf{visible}\quad
 B_{\mathcal C}(x)=(\epsilon_x,O_x)}
{\mathcal C\vdash x\Rightarrow\tau\triangleright(\epsilon_x,O_x)}
\;\mathsf{E\text{-}Binding}.
$$

Here $B_{\mathcal C}(x)$ is the binding-read summary and obligations in context $\mathcal C$. For a stored or iteration binding it is the ordinary captured-slot/value read summary. For a derived binding it checks the registered RHS under the read's semantic view and includes that derivation's dependencies, computing faults, temporal/random requirements and permitted confined private computation in the read summary and obligations. Its resolved lexical environment is the one preceding its declaration; no self/forward reference or later name rebinding is possible. All potential reads must satisfy their contexts even when a declaration itself performs no eager RHS evaluation.

For an admitted call with selected signature $I\to R$, every actual expression checks against its assigned input slot under the same owner mode; slot permission premises also hold. Its result is $R$, effects compose the actual summaries and the declared callee summary, and obligations are their union together with call-site admission predicates. This rule runs after nominal target selection; it has no premise that can pick another candidate using the result type.

For sequential local declarations, check each RHS in the preceding environment, then extend $\Gamma$ with its checked/inferred contract and, for stored bindings only, storage region. Pattern leaves are introduced together after the complete RHS and pattern have been checked; no leaf can resolve within that same RHS. Check the final result only in the completed environment. Effects compose in statement order. Expression/test preambles require expression mode. Shared behaviour preamble local RHSs may use confined Value computation; their foreign statement items remain externally pure. Value computations additionally permit their declared private region. Effect-block completion requires every stored-cardinality obligation before returning its normal result.

Block evaluation has the disjoint outcomes $\mathsf{Normal}(v)$ and $\mathsf{Fault}(E)$, where $E$ is a nonempty collection of Error occurrences. For an admitted block contract $\tau$, Normal requires $v\in\llbracket\tau\rrbracket_W$; Fault supplies no $v$. A stored Error value or an ActionReply containing Errors is not Fault by its shape alone. These outcome labels are metalanguage, not added MUD constructors.

## 1. Literals, names and constructors

> [!rule] MUD-TYPE-009 — Literal synthesis and checking
> A name obtains the contract of its resolved visible binding. An exact numeric literal remains contextual until its compatible representation is uniquely established. No Nat/Int/Num/Money priority is applied to an ambiguous literal; an insufficiently constrained calculated binding requires an annotation. Signs are operators. A basic/alias/magnitude expected context may contextualise a compatible untyped literal. A Rum literal requires its lexical r prefix even in a Rum context.

Text literals synthesise Text, including one-scalar text. A Char context admits one decoded Unicode scalar, with no interpolation. Text is not implicitly a canonically ordered Char collection; its specified textual-list construction in a Char-collection context must satisfy that collection's order/shape. Bool literals have singleton Bool.

Empty has cardinality zero and no chosen nominal member type. An expected zero-admitting collection can check it; a positive-minimum context fails the ordinary admission/contract check. All and fallback are contextual forms: all requires a finite enumerable expected domain, and fallback exists only in a functional branch position.

Component declarations/checking provide the ordered schema of a structural literal. Named and positional forms use the construction rules in chapter 10. A comma-separated value expression produces one outer member for each element expression and does not flatten nested collections. The outer cardinality counts supplied element expressions.

A declaration-category expression denotes its defined descriptor category. Interval, quantity and point literals retain their own elaborated domain/dimensional forms; they are not guessed from their visual similarity to products or numbers.

## 2. Access, reflection and indexing

For field access, every possible static receiver alternative must expose one compatible member contract under the part's access rights. The result joins those contracts without inventing nominal identity. A thing's private ordinary fields remain inaccessible across parts even when its type is visible. A multi-receiver collection does not implicitly project each member's fields.

Metadata access applies the static owner-category matrix. Type reflection returns Type for the statically known contract at that programme point, including valid narrowing. Unsupported metadata is rejected; supported absent optional metadata returns its declared optional result. No runtime lookup repairs invalid reflection.

Positional indexing requires observable order, uses one-based indices and returns the optional member form when absence is permitted. Slices preserve the source members' contracts and retained guarantees with conservative cardinality. Text indexing produces Char and text slicing produces Text; positional text order is distinct from a canonical ordered-collection modifier.

An exact dictionary query checks the key contract and yields its value contract with possible absence; composite keys contextualise one product key. A functional query applies all relevant branch-selector/result contracts and the dictionary's selection mode. The static result preserves the documented FirstMatch or AllMatches collection shape. Missing exact keys and unmatched functional branches yield empty, not an invented type default or a special aggregation error.

## Static generic expressions

`TypeApplicationExpr` denotes an admitted static type application, never a runtime constructor chosen by a Type value. `GenericFamilyMemberExpr` denotes the source member at that applied family type; expected applied-family context may provide its qualification. `GenericCallSpecializationExpr` supplies static arguments to its retained CallExpr before checking or executing the call. It does not execute an unspecialised call first, alter action result/error propagation or add host/root capability. Generic look results retain producer-and-argument identity independently of participant values. Ambiguous generic inference requires explicit `with`, not a guessed type.

## 3. Calls

> [!rule] MUD-TYPE-010 — Call contract
> Select the nominal operation using static receivers and actually written given arguments, without using the expected result. Bind every required receiver/argument, validate positional/named form, check types and permissions, and insert only explicitly declared defaults. Unproved domain admission cannot be used to prefer another candidate.

For a callable value, check every static alternative against the admitted signature. Named calls require the static common-name contract. The supplied callable must preserve required purity, determinism and root permission as well as input/output variance.

> [!rule] MUD-TYPE-014 — Sole action result
> Every action/subaction returns exactly one ActionReply. No additional domain return type, success payload or second output value is admitted. Authorised state changes and message occurrences are effects, not additional return values. Imagine returns the same ActionReply contract.

Boolean rules yield Bool, looks yield their static produced type, and real actions/subactions yield ActionReply only in an effect-capable context. Reactive/always/message declarations are trigger sources under their contracts, not interchangeable Boolean callables. A message payload type is distinct from occurrence identity.

An outer request additionally requires action root capability. A subaction or a value that might denote one is not rescued by an action-shaped annotation. Call cycles must meet the relevant prohibition/proof contract; a type-correct signature does not prove acyclicity.

Computed domains used by expression contracts obey [[10-type-system]]: their evaluation dependencies must be statically acyclic. Reading stored candidate values does not recursively revalidate their contracts. Runtime membership admission cannot legalise an invalid domain-evaluation cycle.

## 4. Numeric, dimensional and Boolean operators

Let $n_A,n_B$ be member numeric representations. Exact addition/subtraction/multiplication use the least common member of Nat, Int, Num. Exact division produces Num; implicit truncation is not introduced. Rum combines only with Rum in its supported signatures, without implicit exact/Rum or Money/Rum mixing.

> [!rule] MUD-TYPE-015 — Numeric representation signatures
> Nat/Int/Num use their exact widening chain. Money is outside that chain. Its only cross-representation arithmetic signatures are exact scaling by Num, admitting Nat/Int factors through ordinary widening. Select the table's result representation before applying nominal dimensions and destination contracts; an unsupported signature is statically invalid.

| Member operands | Operators and result |
| --- | --- |
| Money, Money | + and - yield Money; / yields Num |
| Money, Num | * and / yield Money |
| Num, Money | * yields Money |
| Money, Nat/Int or Nat/Int, Money | Only the corresponding Num scaling signatures via exact widening |
| Money, Money | * and % are unsupported |
| Money and a non-Money scalar | + and - are unsupported; a scalar / Money is unsupported |
| Money, Rum or Rum, Money | All mixed arithmetic is unsupported |

Money-producing scaling computes the exact rational result, rounds to hundredths with round-to-nearest, ties-to-even, then checks the result domain. Money / Money yields an exact rational without monetary rounding. Sequential operators normalise at their textual sites; concurrent numeric stages use [[25-effects]] and its canonical stage normalisation. An update additionally needs a result admissible at its stored destination: Money /= Money cannot implicitly narrow its Num result back to Money.

A supported operation with zero divisor, invalid domain/conversion or prohibited nonfinite Rum result supplies Error occurrences rather than a normal value, empty or sentinel. Resource exhaustion is a technical Error, not numerical overflow/wraparound. A statically invalid closed computation is diagnosed statically. Detailed Error subtype names remain Q-007; binary64 portability remains Q-058. No new arithmetic saturation is inferred.

Pure Nat subtraction saturates before a declared domain check; signed additive effect deltas instead consolidate before one Nat normalisation. Explicit to conversions round and then validate without corrective saturation. Numeric % requires its specified compatible member operation; an absent overload is a static error, not an implicit cast.

Magnitude arithmetic composes nominal dimensional factors and selects the representation allowed by the operation. Addition/subtraction require the specified dimension and linear/point compatibility. Different unitless nominal magnitudes retain different factors. Unit presentation in changes presentation, not dimension or nominal magnitude. Point extraction requires compatible ordered units and produces Nat.

> [!rule] MUD-TYPE-011 — Restricted arithmetic lifting
> Binary numeric +, -, *, / and % admit collection lifting only when at least one static upper cardinality is at most one. Every pair of possible member alternatives must support the operator. The result preserves one occurrence per evaluated pair and has conservative bounds $[\ell_A\ell_B,u_Au_B]$ before explicit normalisation.

If an operand is empty, no member operation is evaluated. Order is preserved from the sole potentially multiple operand where observable. Uniqueness is retained only with non-collision evidence; key uniqueness additionally requires a meaningful stable key path. No implicit zip, reduction or unrestricted Cartesian product is selected.

Logical not, and, or, xor, implication and equivalence require singleton Bool results, with their specified short-circuit/desugaring contract. Temporal is a metalanguage qualification of triggers, not a newly introduced first-class MUD type. A temporal trigger expression is not a Bool that may participate in arbitrary operators: only its defined trigger-combination forms are admitted.

## 5. Equality, comparisons, membership and narrowing

Equality requires compatible effective member types and uses their defined equality: thing identity, exact nominal alias/produced identity with payload equality, family identity, normalised intervals, multisets or ordered sequences, and extensional dictionaries as applicable. Any equality first checks effective types. A representation match alone does not compare two nominal aliases as one type.

`===` and `!==` require two operands denoting Type and produce singleton Bool. They compare normalized complete contracts under [[10-type-system#7.1. Exact structural type equality]]; collection-shaped source types are Type operands, not lifted value comparisons. They are nonchainable comparison-level operators. A family member value is invalid as an operand; `Cat Slot.Empty~type !== Dog Slot.Empty~type` is valid, while their `~anchor` values may compare equal with ordinary `==`. Computation of a Type-producing expression obeys normal purity/error/dependency rules; comparison does not evaluate symbolic domains or create runtime types.

Ordering requires a common defined order. Any has none. Ordered family members, Char scalar values, compatible numbers, normalised supported intervals and lexicographically ordered structural alias components use their specified order. A type without such a contract cannot obtain ordering through an arbitrary comparator.

Is and iis check a nominal type operand. Is uses specialisation; iis uses exact effective nominal identity. Positive/negative flow facts refine subsequent statically justified uses without changing value identity or authority. Has checks the right-hand candidate against the left-hand collection/domain contract; membership tests do not turn a domain into a collection.

Comparison chains type each adjacent comparison and evaluate intermediate expressions once under the concrete chain restrictions. Contextual comparison may type one bare literal from an already typed alias operand; two context-free structural literals do not supply a nominal comparison context.

## 6. Collection and dictionary algebra

Collection |, &, -- and ^ combine compatible member contracts and preserve whole-value multiplicities according to their specified algebra. ^ requires whole-value uniqueness from both operands. Text | is concatenation and does not provide Text overloads for &, -- or ^.

For finite upper bounds $u_A,u_B$, conservative size bounds are:

| Operation | Bounds without stronger overlap evidence |
| --- | --- |
| Union | $[\max(\ell_A,\ell_B),u_A+u_B]$ |
| Intersection | $[0,\min(u_A,u_B)]$ |
| Difference | $[\max(0,\ell_A-u_B),u_A]$ |
| Unique symmetric difference | $[0,u_A+u_B]$ |

Infinite upper bounds use extended nonnegative interval arithmetic. Domain/member result contracts account for both operand domains where needed; lower bounds may be strengthened only with evidence. Keyed uniqueness implies whole-value uniqueness but does not survive cross-operand collisions by declaration alone.

Union guarantees whole-value uniqueness only when both operands supply it. Intersection retains a sole/equal keyed criterion, but differing keyed criteria conservatively yield whole-value uniqueness; without keyed criteria either unique operand suffices. Difference retains the left criterion; symmetric difference conservatively yields whole-value uniqueness. Chapter 14 supplies the separate order/authority table.

An exact association checks one key and one complete value against its contextual dictionary contract and contributes one association. A functional branch checks its selector against the input contract, its result against the output contract and its fallback only in the permitted branch position; selection mode determines result multiplicity. These are value constructors, not assignable branch storage.

Exact dictionary operators operate on complete associations with their defined shared-key precedence; ordered equality and value-uniqueness requirements remain part of the contract. Functional operators are extensional combinations of result computations, not implicit edits or concatenation of branch lists. Their operand/result contracts and termination proofs must all remain valid.

## 7. Domains, selection and finite traversal

All D materialises a proved finite enumerable domain into a collection with its canonical enumeration guarantees. Any and unstepped general Num/Rum intervals do not acquire an enumeration. A stepped exact progression proves a compatible nonzero signed difference, finite bounds and its supported representation; Nat/Int and Money retain their default successor increments.

Selection binds source members only inside its predicate. It requires a captured finite enumerable source and a pure deterministic singleton-Bool predicate. It preserves surviving member identity, multiplicity, uniqueness, order and supplied inner authority; its conservative cardinality is $[0,u]$. An is predicate may narrow surviving alternatives. A bare domain is explicitly materialised when selection must return a collection. Dictionary pair selection retains complete associations.

Take checks a singleton Nat amount and a finite enumerable source. With constant amount $n$ its bounds are $[\min(\ell,n),\min(u,n)]$. It preserves the documented prefix/sample behaviour and retained members' guarantees; an unordered proper sample is a random point, not a proof of deterministic purity. Taking an entire provably small source or zero members need not consume randomness. Text take yields Text; container alias nominality is not reconstructed automatically.

| Quantifier | Source/body requirements | Result |
| --- | --- | --- |
| Exists, forall | Finite enumerable source; pure deterministic Bool predicate | Singleton Bool |
| Count | Same predicate contract | Singleton Nat, bounded by source size |
| Min, max | Finite enumerable source with the required order; pure deterministic Bool filter | Source member contract with cardinality $[0,1]$ |

Min/max return witnesses, not a value computed by a numeric body. No accepted witness yields ordinary empty. Direct quantification/traversal may consume a finite domain without first constructing a collection where its contract permits this. For each executes the appropriate effect/private-region block and preserves its source snapshot and decreasing/finite traversal evidence. Iteration, selection and quantifiers validate the complete recursive binding pattern before the predicate/body, introducing named leaves together and no symbol for a discard. Exact association patterns preserve dictionary witnesses; min/max still return the original accepted witness. Pattern mismatch is a static error and cannot filter the source.

Domain restriction and derived local collection transforms apply their specified filtering, cardinality, ordering and uniqueness normalisation. They do not introduce implicit flattening, a new nominal alias, a new domain from a filtered collection or new inner authority.

## 8. Temporal, random and speculative forms

Old checks the operand under the appropriate entry/snapshot contract; a derived local or pattern projection reinterprets its derivation in that temporal view, while a stored local remains its captured slot. Changes compares the same derivation in the relevant snapshots, not a frozen local result. A test/action entry view differs from reactive previous-wave state. Changes compares defined consecutive observations within one observation episode and has temporal-trigger form. A first or resumed observation supplies a baseline, not a change pulse; lifecycle no-ops preserve continuity. [[04-mathematical-model]] defines binding identity and episode boundaries. Combining/negating inactive Boolean-rule calls uses the specified canonical pruning core; undefined additional desugarings are not inferred from ordinary truth tables.

Rand checks a finite enumerable source and yields a member with the documented random-point identity/cache restrictions. Finiteness, admissibility and purity requirements of its owner still apply. A missing valid sample follows its ordinary error/admission contract, not an invented default.

Imagine checks a root-capable admissible action call, including isolation of its foreign work, and synthesises ActionReply. It is available in pure reading contexts but is not automatically static or deterministic evidence. All resulting world writes/outputs remain speculative and are discarded; an Errors alternative is returned as a value.

Eventually checks its Boolean goal and finite permitted action references, with the specified reachability finiteness/termination obligations. It does not accept arbitrary effect statements as through operands. Its accepted static shape does not prove that an unrestricted world search terminates.

## 9. Blocks and error recovery

> [!rule] MUD-TYPE-012 — Normal result and error channel
> Every expression/value/effect block checks its owner's result contract and effect permissions and carries an Error collection channel. Empty means the normal result is available. Nonempty means it is unavailable. Successfully evaluating false is a normal Bool; only the owning action/invariant interprets it as Refusal.

ExpressionBlock introduces sequential immutable pure preamble values and one final expression. A pure local or pure derived pattern has an ExpressionBlock RHS, not private mutable storage. ValueBlock introduces sequential private computed/stored locals, admitted local mutations/iterations and one final value. EffectBlock contains ordered effects/locals and its required observable effect contract. Declaration/schema braces and LocalStatementBlock grouping do not create another normal-result owner.

Handler on bindings are clause-local immutable Error specialisations. All roles must bind jointly; no on is catch-all. A handler's optional if is an externally pure singleton-Bool expression block. False leaves occurrences pending; errors produced while calculating the filter go outward.

> [!rule] MUD-TYPE-013 — Recovery alternatives
> Then recovery checks against the protected normal result and mode. Raise checks an Error or nonempty Errors-compatible collection and is confined to a handler branch. Then and raise cannot coexist in one handler. Text-only diagnostics, Refusal bindings and arbitrary in-body raise are static errors.

Distinct equal-valued error occurrences are not deduplicated. Clauses handle remaining occurrences in textual/stable causal order; ordinary role binding does not introduce implicit inequality. Protected-body locals and partial exports are unavailable after rollback. Valid enclosing locals and handler bindings remain available.

All successful recovery proposals compose tentatively. Equal compatible value results agree; incompatible result proposals produce a composition error. Remaining or newly raised errors discard the recovery scope and propagate outward without reentering the same chain. Nested recovery blocks retain their own handlers. No finally is introduced.

## 10. Declaration and programme acceptance

Check signatures and effective schemas before their bodies. Guards, after conditions and always invariants require pure singleton Bool; reactive activators additionally require their temporal context. Look/sublook/message/submessage public fields check their declared/inferred value contracts and part boundary. Message payload expressions are evaluated once in the causal birth view and yield immutable, validated values; an error enters the enclosing block error channel instead of publishing a partial occurrence. Ticket is exclusively part of the host observation contract, not a new expression/type constructor. Access to a successful invocation's textual patch remains Q-073 and introduces no guessed source-level field or expression form. Test assertions have expression blocks and a false assertion is distinct from an error in calculating it.

> [!rule] MUD-TYPE-023 — Live local derivations
> Every := local registers a non-assignable derivation with a fixed static contract. An actual read evaluates its definition against the applicable current or temporal view, including preceding effects of its own sequential branch. Derived RHSs and their handlers remain externally pure, including confined fresh ValueBlock computation. = locals instead evaluate once at slot creation and capture the resulting value. Neither form creates a world field or persistent memory between declaration instances.

A real action call may be captured by a stored initializer in an effect-capable context, for example `reply: ActionReply = actor.Move()`. A live derived initializer such as `reply := actor.Move()` is invalid: reading the local cannot replay world effects. Imagine remains an admitted pure speculative query under its ordinary isolation/random rules. Shared preambles, expressions and value-only owners never gain real-action authority from a stored initializer.

Derived positional captures project their common registered RHS, retaining its resolved origin and random-point identity. They do not manufacture independent copied RHS/random sites per leaf; caching/sharing must preserve the existing random and temporal contract. Faults arise on an actual derived read and enter that read's protected block unless handled by the derivation's own admissible RHS handler. Stored initialization faults arise at slot creation and expose no partial captures.

An immutable stored local requires an annotation and initial value; a mutable local additionally receives its private/effect-region place. A calculated binding synthesises or checks a unique static type, registers a live derivation and obtains no outer place authority. Every read uses the semantic view applicable there, including the current private sequential projection; the inferred type does not change when values change. Stored bindings capture once at slot creation. Explicit or partial `_` annotations obey unique stored-hole inference. Shared behaviour preambles admit immutable stored/derived bindings with value-body RHSs, while expression/test preambles retain pure derived expression RHSs. Stored schema initialisers, defaults and static metadata require closed static evaluation in the permitted expression/value mode.

For each syntax family, elaboration selects the already defined operation contract, contextual literal type, runtime admission check, effect summary and proof evidence. Unsupported combinations produce a static diagnostic. Successful static checking proves neither global causal termination nor bit-for-bit binary64 portability beyond the declared guarantees.

The coverage matrix in [[types/expression-coverage.yaml]] accounts for every Surface AST expression constructor. [[types/typing-cases.yaml]] supplies positive, negative and runtime-boundary examples. Their mechanical validation verifies coverage, evidence and finite type-contract witnesses rather than claiming a complete MUD parser/typechecker or executor.
