---
title: Finite normative static certification procedure
status: current
normative: true
depends-on:
  - "[[../11-type-system]]"
  - "[[../18-domains-and-intervals]]"
  - "[[contextual-call-analysis]]"
questions:
  - Q-030
  - Q-027
decisions:
  - D-168
  - D-151
  - D-155
  - D-166
  - D-167
---

# Finite normative static certification procedure

## Scope and result

This procedure certifies finite source enumeration, finite application closure
and the elementary propositions used by termination certification. The language
target fixes the procedure and its supported abstraction. Unsupported predicates
remain unproved, even when another mathematical method could prove them.

```mud
items: Int [*] = all [1..20]
rule Positive for n: Nat { n > 0 }
```

A finite container may have an unbounded static size. Its enumeration certificate
is parametric in the captured finite value; it needs no uniform constant bound.
The procedure does not prove a finite future world/state space. Relevant-state
projection and the eventually profile remain Q-027/Q-030. Native contracts and
causal completion are supplied by their separately established interfaces.

> [!rule] MUD-CERT-001 — Completed normative outcomes
> Return Proven with checked evidence, Violation with an established contrary
> fact or missing language enumeration, or Unproved after completing the
> prescribed procedure. Violation and Unproved prevent mandatory admission.
> Resource interruption is Incomplete tool verification, not Unproved or a
> runtime Error value. Optimization must preserve the completed outcome.

## 1. Ordered stages and normalization

The logical stage order is: finite resolved templates and elementary proofs;
generic closure; contextual call/summary closure; ranked body certificates;
source enumeration and closed evaluations. Inside a ranked component, normal
finite result and subordinate termination premises are discharged together by
well-founded induction on strict calls, not by circular assumptions.

Process resolved identities and source origins in canonical order. Use the
normalization and finite graph identities of chapter 11; retain nominal leaves,
exact generic arguments, default wrappers and declared shape/capability labels.
Normalize exact constants, interval segments, signed progressions and dimensions
under their owning rules. Binary64 sites retain their prescribed rounding;
Nat saturation and Money rounding are not replaced by real arithmetic.

Expand acyclic nonrecursive pure definitions and immutable local definitions
under their bound inputs before abstraction; do not inline a recursive component
to assume its own result. Enumerate the finite Boolean-call availability profiles
and apply canonical pruning to each guard, retaining demanded prefix work. A
pruned guard supplies no numeric/nominal premise that was erased. Original source
resolution/type/permission checks remain mandatory in every profile.

Build finitely many source sites, input/value-origin variables, guard atoms and
contract obligations. Use the contextual procedure's finite destination/summary
fixed point. A captured value and a later mutable/live read have different origins
when an intervening effect can change them. Pure repeated reads may share only
when their inputs, dependencies and coherent view are established equal.

Use full signature/value admission premises established at the actual body
entry. For global stored reads, a declared domain/cardinality is usable only to
the extent it is validated in the current view or proved preserved at that point.
A then/checkpoint end guarantee is not a fact at an earlier private prefix.
Retain intrinsic member/storage constraints, invalidate changed/dependent flow
facts, and widen unestablished bounds for proofs without changing the destination's
declared contract. Snapshot finiteness survives an intermediate cardinality change.

Normalize a numeric expression before abstracting it: fold admitted closed
constants; expand exact addition/subtraction/products into rational-coefficient
polynomials where their signatures permit this; combine identical monomials.
Split each Nat saturating subtraction into its two order cases. Represent an
unresolved non-affine monomial, division or opaque normal result by one origin
variable with only its established type/interval/sign facts. Do not assert an
unsupported equation. Constant denominators retain exact affine division.
Closed evaluation requires an independently certified dependency graph/body;
no circular evaluation or recursive proof of the same obligation is a premise.

The finite formula vocabulary comprises written/substituted obligations, source
and primitive case guards, normal contracts and the finite rank candidates defined
by [[termination-certification]]. It never grows by inventing arbitrarily deep
terms or enumerating arbitrary mathematical proofs. Theory elimination may build
new finite formulas as specified below; it does not restart term generation.

> [!rule] MUD-CERT-002 — Sound finite abstraction
> Every normal execution satisfying the input premises must satisfy its abstract
> formula. Opaque predicates/results range over all possibilities consistent with
> their established contracts. Their occurrences retain origin/view correlations.
> An abstract countermodel is not automatically a real execution or a violation.

## 2. Elementary proof decision

For a proposition P under established premises A, test unsatisfiability of
A and not P in this abstraction. Enumerate truth assignments to the finite
propositional atoms in canonical order; discard assignments contradicted by
intrinsic category/identity/constructor facts. Keep arbitrary predicate atoms
uninterpreted. An assumed guard is a premise in its own region, not a universal
truth. Primitive/operator preconditions and normal-versus-Fault regions remain
explicit. Canonical Boolean pruning and original operand demand retain their
existing source checks; current inactivity is not an impossible-call proof.

Nominal ancestry uses finite transitive closure. Exact graph comparison checks
all constructor labels/edges on the finite product graph. Contract shape proofs
use their normalized cardinality/authority/order/uniqueness rules. Finite explicit
closed sets can be checked exhaustively, after their production and predicate
termination have been independently certified. Unknown runtime members are not
sampled. Inference, invariant writable contracts and privacy checks retain their
own requirements; these facts cannot be guessed by the arithmetic solver.

### Exact affine arithmetic

Each region contains rational affine inequalities/equalities over scalar and
cardinality variables. Money uses integer hundredths; Nat/Int/cardinalities are
integer variables with their established bounds. Num variables are rational.
Equality becomes two inequalities; disequality splits into its two strict cases.
Non-affine opaque variables retain their supported bounds and correlations only.

Eliminate rational variables first by Fourier–Motzkin elimination: partition
inequalities by positive/negative/zero coefficient of the next variable; combine
each lower/upper pair after positive scaling, preserving strictness if either
premise is strict; keep zero-coefficient rows. With no bound on one side, remove
that variable's rows. Normalize rational coefficients, remove exact duplicates,
and decide constant contradictions. Each round removes one variable. Retain the
rows and choices to reconstruct a rational witness when satisfiable.

For the remaining integer formula, clear positive denominators. Convert strict
integer bounds to adjacent inclusive bounds; use floors/ceilings for rational
constants. Eliminate integer variables in canonical order by the following finite
period procedure, processing each disjunctive conjunction separately:

1. Let L be the least common multiple of its nonzero coefficient magnitudes.
   Substitute y=L*x and add L divides y. Scale each atom so y has coefficient
   +1 or -1. Scaling a divisibility atom by k also scales its modulus by k;
   normalize signs. Equations are paired bounds and negative atoms are split.
2. Express bounds as y>=b or y<=u, and divisibility/nondivisibility as d divides
   (y+t) or its negation, with positive constant d. Let M be the least common
   multiple of those moduli (1 when absent).
3. If lower bounds exist, enumerate each written normalized lower term b and
   residues r=0,...,M-1; substitute y=b+r into all atoms. A satisfying value can
   be chosen within one period above the greatest lower bound.
4. If no lower bound exists, upper bounds can be met sufficiently far below.
   Enumerate residues r=0,...,M-1, retaining their congruence checks and atoms
   independent of y; omit y's upper bounds in this negative-infinity case.
5. Join these finitely many branches and continue with one fewer integer variable.

The constant formula decides feasibility. Large endpoints/moduli do not create
language limits. Exact elimination and residue enumeration terminate mathematically;
a physical resource interruption still supplies no completed judgement. This is
complete for the generated mixed affine abstraction, not arbitrary nonlinear
source predicates. A feasible abstract branch gives Unproved. Defined contrary checks include
closed actual contract contradictions, prohibited graph cycles and the established
infinite/unsupported source kinds; an abstract model alone is insufficient.
Unsatisfiability supplies a proof. Optional stronger reasoning does not change
the target's prescribed classification.

### Intrinsic natural measure facts

Finite container cardinality and finite immutable constructor size are natural.
Forwarding a proper existing constructor child supplies strict size descent;
forwarding the whole value supplies equality. Reconstructing a value needs its
own size proof. Primitive container transformations contribute their checked
cardinality relations, retaining membership/no-op correlations.

For the clamped step count mu=max(0,ceil((v-l)/s)), prove s>0 and unchanged l/s
across the call. If v'<=v-s and the caller's mu>=1, conclude mu'<=mu-1.
Reversed counts use the corresponding upper-bound direction. With mu=0 only
nonincrease follows. These exact counting identities are fixed proof rules,
not arbitrary synthesis of floors or assumptions about decreasing rational values.

### Binary64 facts

Each free Rum variable ranges over the finite canonical values fixed by the
numeric contract, including one zero and excluding nonfinite values. For a formula
requiring Rum reasoning, its baseline decision enumerates those finite valuations
in numerical order. Evaluate primitive Rum sites with their exact represented
operands and prescribed rounding, retaining only normal regions; substitute their
exact dyadic values into the exact-arithmetic formula. Opaque producers range over
all normal values admitted by their supported contract abstraction. Unrepresented
mixed/nonlinear relations remain opaque, never mathematical-real approximations.

An equivalent symbolic implementation may avoid this enumeration without changing
its verdict. In particular positive Rum divided by r2 is strictly smaller after
rounding, including the minimum subnormal's ties-to-even transition to zero.
The closed set's ordinal ranks are proof objects, not source casts/enumerators.
This reasoning neither supplies all Rum nor a Rum interval/by progression.

## 3. Finite source and canonical enumeration certificates

Generate source certificates structurally, then propagate the finite dependency
set to its no-growth fixed point. A certificate identifies source kind, captured
inputs, member/domain constraints, canonical order and production/body obligations.
Only the following constructions generate certificates:

| Construction | Required premises |
| --- | --- |
| Admitted concrete collection/dictionary snapshot | Normal finite value contract; keys/associations use their specified traversal. |
| Explicit finite set or closed family | Checked members and the established finite canonical sequence. |
| Linked-world thing population | Finite canonical identity catalogue, strict membership and supplied activity view. |
| Bounded Nat/Int/Money progression | Finite endpoints and admitted compatible nonzero/default advance. |
| Exact stepped Num domain/progression | Its required exact compatible nonzero step and finite endpoints. |
| Finite product/union | Certificates for all required operands and supported order/identity contracts. |
| Intersection/difference/filter of a witnessed finite superset | Complete terminating pure membership/filter decision in the captured view. |
| Normal result of a certified finite computation | Its checked finite output contract and the computation's termination evidence. |
| Recursive constructor enumeration | Explicitly proved finite rank bound, finite branching and finite component/domain certificates. |

A finite rank certificate enumerates levels 0 through its established bound,
using chapter 11's constructor alternatives and products of previously admitted
levels. It proves coverage of the requested domain, not just finite inhabitation.
All constraints/filter decisions are included. A supplied finite value tree is
not a bound on all possible trees. A finite superset is filtered using actual
membership in the requested domain; it is not returned wholesale.

Proof queries can establish required bounds/nonzero advances using section 2.
A type's infinite domain, unsupported numeric enumeration or an unmet construction
premise generates no guessed certificate. Unstepped general Num, numeric Rum and
Any retain their source-enumeration restrictions. take/filter cannot make an
unadmitted infinite base into a lazy finite prefix. A runtime finite snapshot
needs no compile-time enumeration of its unknown actual members.

## 4. Finite generic application closure

Before unbounded unfolding, collect the finite application templates and their
argument-origin dependencies. Normalize their exact argument forms. Certify
acyclic template components topologically. For a recurrent component, its supported
parametric certificate must show that each forwarded argument is an existing
argument/projection node or a normalized union of a finite pool of those nodes
and written constants. Permutations and duplicated forwarding are allowed.
A constructor wrapping a recurrent carried argument must normalize to one of
those existing nodes; otherwise this nonexpansive certificate is unavailable.
No arbitrary fresh constructor chain is unfolded to a depth cutoff.

For a certified component and concrete input finite type graphs, form the finite
argument pool (including its stable schema projections) and its admitted union
closure. Instantiate reachable application tuples from that pool; each new tuple
is visited once. Process outgoing acyclic components likewise. Check every bound
and every substituted edge, retaining exact arguments and phantom identities.
Stop at the exact no-new-application fixed point. The same template certificate
establishes parametric body closure for admitted inputs. A strictly growing
self-instantiation can supply a contrary witness; unsupported finite closure
remains Unproved rather than falsely labelled infinite.

This procedure supports stable recursion, mutual forwarding/permutation, finite
argument projections/unions and acyclic construction. It is deliberately not a
complete solver for every conceivable finite type-level transformation. The
finite closure certificate is checked before the constructor-productivity and
structural comparison procedures; it never proves those independent properties.

## 5. Global completion and conformance

Use a finite obligation graph. Dependencies may use proved results, never an
assumption of their own conclusion. Process acyclic components in order; the
explicit recursive termination rule is the only certified recursive exception.
Any unresolved circular prerequisite remains Unproved. Attempt each supported
construction and elementary decision in its fixed order until every obligation
is Proven, Violation or Unproved. Report all completed mandatory failures by
source origin and distinct reason; do not change the classification because an
optional solver finds another proof outside this target's abstraction.

Every search above has a finite input vocabulary or removes a variable/obligation.
Completion has no arbitrary time, integer-size, type-depth or iteration bound.
An implementation may share a reference analyzer or reproduce this procedure;
optimizations require the same complete classifications and evidence obligations.

[[test_static_certification_witnesses.py]] checks supplied exact affine decision,
finite/infinite/unsupported source and rank boundaries. Existing interval,
generic and constructor witnesses supply bounded structural evidence. These
checks do not extract Mud source or implement a compiler/runtime.
