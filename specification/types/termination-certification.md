---
title: Normative body termination certification
status: current
normative: true
depends-on:
  - "[[contextual-call-analysis]]"
  - "[[finite-static-certification]]"
  - "[[../17-dictionaries]]"
questions:
  - Q-020
  - Q-030
  - Q-072
decisions:
  - D-169
  - D-167
  - D-168
  - D-085
  - D-155
  - D-166
---

# Normative body termination certification

## Scope and classes

The certificate proves that an admitted source body completes normally, faults
or refuses as applicable; it does not guarantee a successful normal result.
It covers finite primitives/compositions/traversals and certified recursion in
functional dictionaries, Boolean rules, looks/sublooks and alias operator bodies.

```mud
alias Counters { major: Nat; minor: Nat }
let finish: Counters --> Nat [ordered] =
    value.minor > 0 --> finish[value.major, value.minor - 1],
    value.major > 0 --> finish[value.major - 1, value.major],
    _ --> 0
```

Composite functional input sugar constructs one contextual value, just like a
composite exact key. Named alias components may be supplied positionally; an
anonymous named tuple does not thereby become an anonymous positional tuple.

> [!rule] MUD-TERM-001 — Certified pure recursion
> Every recursive normal/recovery call in an eligible pure component must strictly
> descend in one well-founded measure. Purity, complete result/signature checking
> and all independent acyclicity prohibitions remain mandatory. No certificate
> introduces recursion in actions/tests, computed-domain cycles or local/schema
> definition cycles prohibited by their owners.

Action/subaction/test and speculative admissibility call components retain their
acyclic contextual graphs. Nonrecursive source bodies follow structural induction:
primitive sites complete or fault, subordinate certified bodies complete, finite
traversals have certified source production and finite iterations, and handlers
have the same requirements. Local mutation supplies no unbounded while loop.
Opaque native work needs its established checked/trusted termination contract;
this document invents no foreign guarantee or wait/cancellation protocol.

## 1. Natural measures and strict edge relation

For a finite recursive component C, each node d has input bindings a in one
coherent pure view W. A measure mu_d(a,W) is a total natural-valued proof expression
on admitted inputs. It cannot depend circularly on execution of the component,
replay stochastic computation or change W. It is not evaluated as an extra
runtime instruction. Existing stored values and stable captures retain their
ordinary contracts. A measure proof cannot assume a world invariant that is not
established in the actual caller view.

Generate a finite elementary candidate catalogue at each node:

- Natural input/components and established immutable lexical captures named by
  finite written signature/projection/binding paths. Policy code-origin frames
  include their established capture inputs without exposing a public schema.
- Cardinality of a finite input/projection and structural size of a finite
  immutable value; existing proper child/member projections supply strict
  substructure evidence, not thing-relation traversal or newly reconstructed data.
- Natural-valued noncircular pure expressions already written in the body, after
  substitution/normalization; mutation-dependent locals are not entry measures.
- Distances from proved lower/upper bounds for integral values, and clamped exact
  step counts for rational/integer/Money values with a proved positive unchanged
  advance. These are max(0,ceil((v-l)/s)) or their reversed direction, using only
  written bounds/advances and supported proof facts. Merely decreasing a Num
  towards zero supplies no positive stable advance.
- Ordinal rank, or reversed rank, in a proved finite semantic order. Rum uses its
  canonical finite represented value order; ordered families use member position.
- Constants 0,...,|D(C)|-1 as declaration phases, where D(C) is the set
  of original applied declarations/policy code origins in C.

For a candidate whose necessary definedness premise is guarded (for example
a positive step), totalize it to zero outside that premise. Include those
finitely generated definedness cases in the proof regions. Its descent identity
may be used only after the relevant premises are proved; this is not an arbitrary
boolean/data phase or an extra runtime computation.

Validate total natural-valuedness and permitted dependencies independently.
A source/projection without that evidence contributes no candidate. Identity
rank of a finite thing catalogue does not prove that a relationship decreases.
Source expressions are not invented arbitrarily beyond this catalogue and the
affine synthesis below.

For each source call region d(a)→e(b), derive its supported normal transition
formula from input contracts, guards, ordered-branch exclusions, argument transfer,
actual rounding and flow facts. Recovery calls are separate regions. Missing
relationships remain conservative; a runtime sample is never a premise.
Require mu_e(b,W) < mu_d(a,W) on every possible continuing recursive edge.

## 2. Lexicographic search and phases

> [!rule] MUD-TERM-002 — Finite lexicographic descent
> A fixed finite tuple of natural measures is well founded. On each recursive
> edge its first differing component must decrease and every earlier component
> must be equal; later components may increase. Phases may distinguish different
> declarations but are constant within each declaration context.

A profile selects one elementary measure for each node of C. There are finitely
many profiles. Enumerate finite ordered lists of distinct profiles in canonical
order, testing shorter lists first. Repeating an identical profile adds no power:
its earlier comparison already decided equality/descent. Thus the maximum useful
length is the number of profiles, not an arbitrary language depth cap.

For each candidate list, use the elementary proof decision to prove the full
lexicographic disjunction on every edge region. Constant phase assignments range
over 0,...,|D(C)|-1 and agree for contexts sharing an original applied declaration
or policy code origin; arbitrary larger phase numbers can be order-compressed without
changing strict/equal comparisons. Accept the first valid certificate. If none
works, continue with affine synthesis. Unknown edge proofs do not remove edges.

For F(n)→G(n)→F(n−1), use (n,1) for F and (n,0) for G. Every edge descends.
For finish above, (major,minor) descends although minor resets when major decreases.
The proof is induction on the well-founded tuple, with finite subordinate work
at each invocation. It does not bound recursion by a fixed constant for all inputs.

## 3. Exact affine scalar synthesis

> [!rule] MUD-TERM-003 — Synthesized natural affine ranking
> The mandatory procedure also searches for a scalar measure
> rho_d=c_d+sum(w_di*m_di), with nonnegative rational coefficients over elementary
> natural measures. A common positive denominator scale turns the result into
> natural coefficients/values. It must prove strict descent, optionally with a
> finite declaration phase, for every recursive transition.

Use each region's finite closed rational linear overapproximation: supported
exact affine argument equations/guards and proved measure comparisons, plus
natural lower bounds. Replace unsupported relations by only their proved facts.
Integer strict bounds use their adjacent integral bound; rational open premises
may be relaxed to closed ones here. An infeasible relaxation is vacuous, while
a feasible spurious model is not a real nontermination witness.

Enumerate phase assignments p_d in 0,...,|D(C)|-1, respecting that same-origin equality. For each edge d→e require:

- rho_e<=rho_d when p_e<p_d;
- rho_e<=rho_d−1 otherwise.

These requirements make (scaled rho,p) strictly lexicographic. For each feasible
closed transition polyhedron A*z<=b, express implication by nonnegative rational
Farkas multipliers lambda: the desired row h*z<=k is certified by
lambda*A=h and lambda*b<=k. The row coefficients are affine in the unknown
ranking weights/constants. Together with nonnegativity this is a finite rational
linear feasibility problem. Decide it by the exact Fourier–Motzkin procedure,
reconstruct a rational solution, scale all denominators together and verify the
resulting implications with the elementary decision. Empty regions are checked
before using implication multipliers. No enumeration of unbounded integer
coefficients or resource-derived coefficient cap is used.

Choose phase assignments and variables in canonical order; witness reconstruction
chooses a rational endpoint when admitted, the midpoint of a bounded open interval,
or a unit beyond a sole strict bound. For a free variable choose zero. The final
scaled certificate's validity is mandatory, not its cosmetic coefficient size.
If every assignment's feasibility is false/unproved under this fixed abstraction,
return Unproved. Nonlinear/arbitrary ranking synthesis is not part of the method.

For natural transitions (x,y)→(x−1,y+1) and (x,y)→(x+1,y−2) under their guards,
3*x+2*y decreases by one. Neither elementary counter order suffices.

## 4. Rum, counterexamples and completion

A Rum rank compares actual canonical binary64 outputs, not the mathematical
unrounded expression. Positive value/r2 is strictly smaller, including subnormal
rounding to zero. A decrement absorbed by rounding is unchanged and fails the
strict test. Finite-order rank does not grant source all Rum or numeric progression.
For Num, 1→1/2→1/4… is an infinite chain and not well-founded descent.

The source component has finitely many nodes, regions and elementary profiles;
lexicographic profile search and phase enumeration are finite. Each affine query
eliminates finitely many variables. Every subordinate proof uses the completed
procedure in [[finite-static-certification]]. Return Proven with a checked tuple
or affine certificate, or Unproved after exhausting those searches. The contrary
check inspects finite simple call-region cycles with identity argument/capture
transfer and a closed admitted entry drawn from normalized written constants.
A cycle establishes Violation only when that entry satisfies every cycle region,
and the view and finite normal prefixes are independently certified unchanged.
Unsupported prefix evaluation supplies no witness. There is no unbounded runtime
simulation or arbitrary input search. Equal code origins alone do not compare
functional policy values. Other unproved recursion is Unproved, not a guessed
nontermination claim. Tool interruption is Incomplete. All compilers under the
target must reproduce these distinctions.

Body termination and contextual action acyclicity do not prove that reactive
waves stabilize, exterior work returns or a complete resolution finishes.
Oscillation and causal completion remain Q-020/Q-072; deeper eventually state
profiles remain Q-030. Pure recursively enumerated values remain finite but do
not thereby make all possible states finite.

[[test_static_certification_witnesses.py]] supplies finite strict/lexicographic,
phase, affine, rational-stalling and binary64 certificates. It does not analyze
Mud source or implement the compiler, runtime or an arbitrary synthesis solver.
