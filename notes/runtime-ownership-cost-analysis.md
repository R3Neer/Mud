---
title: Runtime ownership cost analysis
status: analysis
tags:
  - mud/analysis
  - mud/runtime
  - mud/performance
---

# Runtime ownership cost analysis

## Result and authority

The first optimisation target should be dependency/cause representation and
completion bookkeeping, before approximate owner assignment. Exact observable
attribution does not require tracing every arithmetic instruction. Grouping by
physical wave alone does not preserve the reviewed completion and rollback
behaviour. An approximate policy remains a candidate for comparison, not a
selected replacement.

This is a cost model and design analysis, not a runtime implementation,
benchmark, instruction-count measurement or completed algorithm. It accompanies
[[causal-runtime-formalisation]] and [[questions/Q-072-causal-work-and-reality-completion-algorithm|Q-072]].
It does not close that question or promote a specification chapter. D-013's
formalisation-before-implementation boundary remains applicable.

## Semantic baseline being costed

The discussion-reviewed baseline distinguishes reality branches/levels,
invocations, protected scopes and pending work. Causes, completion responsibility
and survival dependencies are separate. These discussion conclusions are cost
assumptions here; their full ADR/normative integration is a separate task.

- Temporal attribution uses modified semantic dependencies from both valid
  observations, with no minimum-cause search or reopening of historical owners.
- Guards add current causes. Each effect also carries the relevant data and
  destination dependencies; intermediate values preserve them by component.
- Collection queries include relevant existence, membership and order regions.
- Joint work has a common enclosing responsible invocation, while contributing
  invocations may have completion dependencies on that work.
- Recovery remains pending through its relevant consequences; registering new
  obligations precedes retiring old obligations.
- Discard creates no compensating changes pulse. Invalid joint consequences
  are removed and affected discovery is reconstructed from surviving causes.
- The existing effect algebra, occurrence multiplicity, private views,
  checkpoints and ticket survival constraints continue to apply.

This baseline is stricter than merely choosing a wave owner. A candidate that
returns earlier, drops a different scope or loses surviving reactions changes
observable semantics even when its final numeric value happens to match.

## Accounting vocabulary

Count separate operation classes, not one interchangeable instruction unit:

| Symbol | Counted work |
| --- | --- |
| E | Ordinary arithmetic/computation operations. |
| R | World-read occurrences; D is the number of distinct reusable dependency regions. |
| F | Effect/output records; their existing journal cost is not all new causal overhead. |
| M | Causal matches/work items produced; distinct occurrences remain distinct. |
| K | Distinct live contributing invocations in a cause support. |
| V | Cause-set construction/combination steps. |
| L | Lowest-common-ancestor (LCA) combination calls for responsible owners. |
| W | Stored completion membership/subscription relationships. |
| H | Maximum invocation-tree depth. |
| J | Contributions retained in an affected consolidation region. |
| A | Work/observations reachable through affected invalidation dependencies. |

A combination call is not a CPU instruction. A naive owner-tree walk can cost
O(H) per LCA call; indexed/cached alternatives have preprocessing, storage and
invalidation costs. Cause-set combination costs depend on support size and
representation. Hash lookups have key-comparison and cache costs; arbitrary
precision values and query comparisons have their own data-dependent costs.

Separate: ordinary execution; reactive discovery; effect journal/consolidation;
dependency/cause tracking; owner selection; completion; reconstruction; adapter
conversion; optional diagnostics/textual recording. Removing owner selection
does not remove all the other categories.

## Case 1 — arithmetic region with repeated dependencies

Synthetic input: one stable read view, E = 10,000 arithmetic operations,
R = 200 world-read occurrences over D = 10 fixed scalar regions, F = 20 scalar
outputs, all outputs depending on the same ten inputs. The inputs' current
causes are ten distinct sibling invocations (K = 10). The output computations
are statically understood and have no intervening mutation, dynamic selection,
native operation or effectful call. Thus one source footprint and support can
be shared without changing attribution, result components or observations.

The naive candidate allocates a fresh cause-array label with capacity for ten
IDs at each arithmetic result, independently constructs each output's owner and stores
each output-to-contributor wait relationship. This deliberately expensive
candidate is not a lower bound on exact attribution.

The exact shared candidate obtains the ten input supports once in this view,
constructs one common support, folds its owner once, and uses a completion group
for the twenty outputs. Every contributor waits for all twenty in this case,
so grouping does not change its completion frontier. Other cases cannot assume
that grouping is legal.

| Accounting item | Naive exact | Exact shared candidate |
| --- | ---: | ---: |
| Ordinary arithmetic E | 10,000 | 10,000 |
| Physical value-read occurrences R | 200 | 200 |
| Cause lookups at read occurrences | 200 | 10 reusable input lookups |
| Stored dependency-region entries | 200 | 10 shared entries |
| Arithmetic-result cause combinations V | 10,000 | 0 per arithmetic result; 9 support construction steps |
| Cause-label constructions | 10,000 | 1 common label |
| LCA calls L | 20 × 9 = 180 | 9 |
| Direct output/contributor wait edges | 20 × 10 = 200 | 20 group memberships + 10 contributor subscriptions = 30 |
| Effect/output records F | 20 | 20 |

There is no aggregate sum: lookups, combinations and memberships have different
costs. Reuse needs a sound read-view/footprint identity; variable lookups cannot
be reduced to D when mutation or dynamic selection invalidates that assumption.
Label canonicalisation/version checks also have costs, not included as free
work in a runtime performance prediction.

For an illustrative eight-byte contributor ID, the naive candidate reserves
10,000 × 10 × 8 = 800,000 bytes of label payload capacity cumulatively. A support
can contain fewer IDs before all inputs have been combined; capacity is not
the number of populated or copied IDs. The shared label
contains 10 × 8 = 80 bytes; twenty eight-byte references add 160 bytes. The 240
bytes are one retained label plus output handles, not total runtime memory and
not directly comparable to cumulative allocation traffic. Naive temporary
labels may die quickly; their 800,000 bytes are not necessarily peak residency.
Headers, dependency entries, the journal, grouping and allocator overhead are
excluded. An inline bit mask could avoid this label heap allocation altogether
for a sufficiently small bounded owner universe.

Exact sharing removes the 10,000 per-arithmetic label combinations in this
constructed case. Coarsening ownership further could avoid the nine LCA calls,
but cannot drop support identities/completion obligations if selective survival
must remain exact. This case does not establish a general speedup percentage.

## Case 2 — many independent owners in one physical wave

Synthetic input: N = 1,000 independent invocations, each producing one effect
and one one-cause work item. No match joins them. One invocation later waits
for unrelated exterior work; no asynchronous source syntax is assumed.

Exact attribution needs no nontrivial cause union or LCA for a singleton
support: V = 0, L = 0. It retains 1,000 support/owner associations and 1,000
individual completion associations in a direct representation. Owner handles
can refer directly to invocation records and completion counters; no fresh
cause-set allocation is intrinsically required.

Coarse wave ownership could replace 1,000 per-item owner associations by one
group association (saving 999 associations in that selected layout). However,
if all members now wait for the whole group, 999 independent invocations may
wait for the unrelated exterior request. Selective discard also needs the
original contributor/scope distinctions. Retaining those distinctions retains
much of the exact bookkeeping; removing them changes semantics.

The layout count alone does not establish an execution-time saving. Whole-wave
grouping is not an exact optimisation for this case. Exact grouping requires
proved identical completion/survival obligations, not merely co-occurrence.

## Case 3 — a genuinely large conjunctive join

Synthetic input: 100 distinct occurrences on the left and 100 on the right,
with compatible disjoint bindings. The accepted conjunction is a Cartesian
product, yielding M = 100 × 100 = 10,000 distinct matches. Each match has two
causes; assume each produces a distinct message occurrence.

| Accounting item | Direct exact representation |
| --- | ---: |
| Match/observable occurrence count | 10,000 |
| Pair support constructions | 10,000 |
| LCA calls without structural reuse | 10,000 |
| Contributor-to-match completion relationships | 20,000 |

If all occurrence producers are known children of one common invocation, the
owner result can be shared or obtained directly; the 10,000 repeated LCA calls
need not be performed. Pair supports can refer to their two source records,
and matches can be streamed or arena-allocated. Factorised row/column completion
counters can avoid explicitly storing all 20,000 wait edges in this example,
but each completed pair still needs to update the relevant accounting and its
survival remains tied to both sources.

The 10,000 distinct messages cannot be replaced by one message or deduplicated
by payload. Their generation/delivery remains a workload lower bound here.
Not every join emits a message: aggregating effects may admit other exact
optimisations, with occurrence, validation and rollback equivalence proved.

## Case 4 — selective discard and reconstruction

Synthetic input: an enclosing attempt retains B after explicitly observing
A's Refusal. Starting from x = 0, A contributes +=2 and B contributes +=3.
One established reactive binding observes x changes and produces seen = x.
The first consolidation gives x = 5 and a joint consequence seen = 5. A is
then discarded. Its joint consequence is invalidated; B survives. A corrected
transition from the valid entry 0 to survivor value 3 discovers a new match,
giving seen = 3. There is no rollback pulse from 5 to 3.

Minimal logical ledger for the model:

| Item | Count |
| --- | ---: |
| Original numeric contributions | 2 |
| First relevant consolidation/discovery passes | 1 each |
| Invalidated joint match/consequence | 1 |
| Surviving numeric contributions reconsidered | 1 |
| Replacement discovery pass and match | 1 each |

These are logical passes, not exact hash/queue/CPU operation counts. Additional
work arises if the consequence has descendants or other observations depend
on the affected region. Invalidated tickets drop; reconstructed occurrences
have distinct identities. Calls that fail as bare effects may instead discard
the enclosing attempt; the example explicitly uses reply observation to retain B.

Coarse owner selection alone cannot avoid this reconstruction while preserving
selective survival and reactions. Dropping both A and B saves work by changing
the outcome. Keeping the old joint consequence is incorrect. When all members
of a proved-common survival region are discarded together, whole-region release
can be exact and cheap. This is scope/lifetime optimisation, not justification
for treating all physical-wave members as that region.

For an affected region, reconstruction includes visiting retained contributions
(at least proportional to J when all must be reconsidered), invalidating reachable
work and affected discovery. A can be large; sorting, joins, queries and
validation add their own costs. Repeated invalidations can require repeated
work. No universal O(J + A) runtime bound is asserted.

## Growth and memory limits

- Naively recording dependencies at every computation node can grow with E.
  Static footprint propagation and liveness can move runtime metadata to read,
  query, effect and observation boundaries in suitable programmes.
- Independently materialised K-owner sets at M nodes can take O(MK) ID storage.
  Small supports, shared immutable support DAGs, interned labels and appropriate
  sparse/dense sets reduce selected cases, not every possible programme.
- Bitsets scale with the chosen owner universe; they can waste memory for very
  sparse large worlds. Compressed support DAGs can shift work to membership,
  traversal and invalidation. No representation is uniformly optimal.
- Completion subscriptions also admit O(MK) direct expansion. Exact factorisation
  requires known equal obligations and preserves barriers/registration order.
- Observing old and new query regions can retain their union, up to D_old + D_new
  before deduplication. Shared immutable footprints avoid wholesale copies.
- Filters and ordering queries may genuinely consult many candidates, including
  rejected candidates. Precise footprint recording does not make the query cheap.
- Pending exterior requests retain their scopes/supports. Slow completion can
  increase residency without generating additional executable work.
- Finalisation cannot retain history forever. Retention of observation baselines,
  surviving supports, tickets and patch/reproduction data needs explicit lifetimes.
  No selected global memory-management strategy or GC-free guarantee is assumed.

## Candidate comparison

| Candidate | Expected saving | Semantic condition |
| --- | --- | --- |
| Static scalar/component footprints | Avoid arithmetic-level tracking | Exact dynamic read regions and component uses must still be represented. |
| Shared causes and cached owner folds | Avoid repeated unions/copies/ancestor walks | Read views, generations, source identities and disposal remain valid. |
| Exact block/lifetime grouping | Fewer completion edges and allocations | All grouped items have the same relevant completion/survival obligations. |
| Factorised joins and streamed matches | Less metadata allocation/edge storage | Preserve every required distinct match and outcome. |
| Adaptive sparse/dense cause representation | Better memory/cache use | Representation changes cannot change support membership. |
| One owner per physical wave | Potentially fewer owner associations | Approximate unless independence/frontiers/selective survival are separately preserved. |
| Ancestor promotion after a support-size threshold | Cap some completion bookkeeping | May delay after, enlarge discard or alter results; needs an explicitly reviewed alternate semantics. |

A conservative approximation is not automatically sound for observable execution.
In particular, adding causes can change after timing, recovery reach and surviving
effects. Heuristic candidate selection followed by exact checking is different
from accepting an approximate cause set. Hashes alone are not equality proofs.

## What can be concluded now

1. An exact runtime need not perform one causal-set operation per arithmetic
   operation. Case 1 demonstrates a legal boundary-level design under stated
   assumptions, rather than a prediction for all dynamic computations.
2. Owner selection alone can be zero-cost beyond a reused/direct handle for
   singleton supports, or cheap after structural reuse. The expensive categories
   may instead be query discovery, support storage, waits and reconstruction.
3. Coarse wave ownership has the least attractive tradeoff for independent
   work: it may save little routing work while visibly coupling completion.
4. Large joins and broad invalidation impose real work that an owner heuristic
   cannot eliminate without losing required behaviour.
5. First cost an exact shared implementation. Compare any approximate candidate
   against that implementation, not only against per-instruction tracing.

The earlier C# factors 2x/3x are provisional discussion targets, not adopted
requirements or demonstrated results. These unweighted model counts cannot
establish whether they are achievable. Arithmetic representation, adapter
conversion, memory locality, latency and workload mix require later measurement.

## Next evidence and measurement plan

During remaining formalisation, attach operation/memory costs to barrier
formation, support registration, completion, scope discard, reconstructed
discovery and retention. Vary E, D, F, M, K, H, changed fraction, cause-support
reuse, invalidation depth and waiting duration independently. Include dynamic
key selection, negative lookup, membership, order and discarded filter candidates.

Once the implementation gate permits an experimental executor, instrument the
same traces for each candidate. Count dependency lookups/registrations, set
cardinality and combinations, LCA cache misses, work and subscription records,
invalidation visits, recomputation, allocations and bytes retained. Measure
elapsed CPU/wall time, hardware instructions where available, p50/p95/p99,
peak memory and allocator behaviour in separately identified recording modes.
Warm and cold costs, compiler preparation and exterior service time are separate.

Compare traces/results, after frontiers, Refusal/Errors, rollback scopes,
occurrence identity/order and ticket outcomes before comparing speed. Different
results are alternate semantics, not a faster implementation of the same model.
Pin hardware, optimisations, versions, dataset and numerical representations.
Use both a same-guarantees reference and a direct implementation to distinguish
implementation overhead from the price of the guarantees. Numeric operation
counts, allocation counts and total elapsed time must remain separate measures.
