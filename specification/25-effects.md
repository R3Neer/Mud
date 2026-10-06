---
title: Effects and batch consolidation
status: proposed
normative: true
depends-on:
  - "[[03-notation]]"
  - "[[04-mathematical-model]]"
  - "[[14-fields-and-mutability]]"
  - "[[19-expressions]]"
questions:
  - Q-007
  - Q-019
  - Q-020
  - Q-023
  - Q-058
  - Q-069
  - Q-070
decisions:
  - D-023
  - D-026
  - D-039
  - D-046
  - D-060
  - D-080
  - D-098
  - D-100
  - D-105
  - D-110
  - D-111
  - D-117
  - D-118
  - D-119
  - D-120
  - D-121
  - D-123
  - D-125
  - D-126
  - D-127
  - D-128
---

# 25. Effects and batch consolidation

## Scope

This chapter defines execution of statically admitted effect families over private projections and consolidation of finite branch contributions at root/wave boundaries. [[14-fields-and-mutability]] supplies authority and static proof obligations; [[19-expressions]] supplies expression evaluation contracts. A successful batch produces a tentative next view, not an independent commit.

The judgment is parameterised by expression evaluation, the invocation completion protocol and checked/trusted adapter operations. It does not implement those interfaces, select a wave scheduler or define missing arithmetic overloads. Detailed Error categories remain Q-007; numeric limits/operations remain Q-019 and binary64 portability Q-058; oscillation detection remains Q-020; dynamic callable acyclicity remains Q-023; native hosting/conversion protocols remain Q-069/Q-070. None grants permission to change the effect laws below.

## 1. Configurations and outcomes

Let $W_0$ be a batch's common tentative entry view. A branch configuration $C=(W_0,\rho,L,I,U,\omega)$ contains its lexical environment $\rho$, private local storage $L$, ordered semantic intents $I$, tentative causal outputs $U$ and invocation owner $\omega$. Let $\operatorname{view}(C)$ be its private projection after applying its preceding intents. These components are semantic observations, not a required IR or memory layout.

A destination $\lambda=(r,g,p)$ identifies storage root $r$, materialisation generation $g$ where applicable, and resolved component/key path $p$. Local roots additionally identify their computation/frame. Intents retain the evaluated operand, destination, operation, causal owner and stable provenance. Causal outputs retain occurrence identity and joint causes, not only equal payloads.

Write $C\vdash e\Downarrow v$ for successful evaluation on this private view, with the owner's ordinary purity/capability contract. Failure produces a nonempty Error occurrence collection. Destination resolution gives $\lambda$, MissingIntermediate or a fault; an invalid/unwritable path is not MissingIntermediate. Resolving an intermediate absent exact key does not fabricate a default value or association.

The effect result $o$ is one of $\mathsf{Continue}$, $\mathsf{Refuse}(r)$ or $\mathsf{Fault}(E)$. These are metalanguage labels, not extra MUD values. Refuse carries a Refusal; Fault carries nonempty Errors-compatible occurrences. Continue supplies the updated private configuration. Effect blocks have no additional domain return result.

## 2. Sequential statement judgment

Write $C\vdash s\Downarrow(C',o)$ for one admitted statement. The empty sequence continues unchanged. A nonempty sequence evaluates its head, then its tail only on Continue:

$$
\frac{C\vdash s\Downarrow(C_1,\mathsf{Continue})\quad
 C_1\vdash S\Downarrow(C_2,o)}
 {C\vdash s;S\Downarrow(C_2,o)}\;\mathsf{EffectSequence}
$$

Refuse/Fault stops dependent evaluation and skips the remaining statements. The applicable protected/invocation scope is rolled back before recovery or reply observation. Failed locals and partial native exports do not survive. Independent concurrent branches may produce several Error occurrences; they are not deduplicated by equal values.

> [!rule] MUD-EFFECT-007 — Private sequencing
> Operands and paths observe preceding effects of their own branch, never siblings' private deltas. Evaluate each operand/path once at its textual site and retain its result and provenance. Internal calls continue in the same causal resolution. Reordering instructions is valid only if it preserves these observations and surviving intents.

Calculated local statements evaluate a value and extend $\rho$ immutably. Stored local statements allocate admitted frame-local storage with their explicit value and permissions. Both propagate evaluation faults and obey no-shadowing/no-forward-reference. Local mutation does not acquire world authority.

## 3. Assignment and relative update

Assignment resolves an authorised destination and evaluates its RHS on the current private view. A complete exact-key assignment may insert an absent final association. MissingIntermediate produces no intent for a partial path. Otherwise append a replacement/update intent and project the new private value under the established operation laws. Domain/type checks remain mandatory; permitted temporary stored-cardinality deviations follow section 9.

For assignment, record an absolute replacement, even when the RHS reads the target. `x = x + 5` is not `x += 5`. For arithmetic updates retain signed addition/subtraction amounts and multiplication/division operands; for collection updates retain the specified algebraic operator. No unsupported overload is inferred.

> [!rule] MUD-EFFECT-008 — Semantic replacement normalisation
> A later absolute replacement supersedes earlier intents of that branch within its replaced destination/subtree. It does not erase sibling contributions. Retain subsequent relative/descendant changes. Equal concurrent replacements at one semantic destination merge; unequal ones fault. A whole-container replacement supplies the base for compatible surviving descendant changes. Reconstruct immutable ancestors once after their semantic component intents have composed.

Independent alias components compose without becoming conflicting whole-root assignments. A diamond-inherited field retains its declaration origin; spelling alone does not establish destination equality. A whole replacement lacking a required compatible descendant path/contract cannot be patched by guessing an alias type or shape.

## 4. Numeric stages

For each numeric destination, project each normalised branch onto its surviving ordered relative operations. Position $k$ is counted in that destination's sequence, excluding operations on unrelated destinations. Missing positions contribute the identity operation. All operands remain the values frozen during private evaluation.

> [!rule] MUD-EFFECT-009 — Staged numeric composition
> Start from the common entry or the compatible replacement base. At stage $k$, add all signed additive contributions, multiply all factors and divide by the product of divisors: $z_{k+1}=((z_k+\Delta_k)P_k)/Q_k$. Advance through all stages. This preserves the order of each branch and applies addition-before-multiplication only within a concurrent stage, not across successive statements.

The identities are $\Delta_k=0$, $P_k=Q_k=1$. Preserve the denominator as a divisor product, not an obligatory inverse. Cancel factors only where the representation's laws prove exact semantic preservation; no simplification hides a zero denominator, refined domain error or invalid dimensional operation.

Nat's additive bookkeeping retains signed pending quantities through private reads and consolidation stages. Its visible projection is nonnegative, and saturation does not overwrite the ledger. In a homogeneous additive sequence from $n$, a private read is $\max(0,n+\sum\delta_i)$; the completed additive batch uses the same total. Do not truncate a negative pending total between stages. Pure Nat subtraction still saturates immediately.

Other arithmetic applies its established representation, rounding and validation rules. This chapter does not silently supply unresolved Money/Rum operations. In an exact arithmetic witness, one branch from 5 with *=2; +=3 yields 13; branches *=2; +=3 and *=3; +=4 yield 37. A +=2 and B *=3 still yield 21. An absolute replacement first removes that branch's overwritten updates before stages are numbered.

## 5. Collections, add/remove and exact dictionaries

Homogeneous concurrent collection updates retain their canonical algebra:

| Update family | Joint contribution |
| --- | --- |
| union | Pointwise maximum operand multiplicities |
| intersection | Pointwise minimum operand multiplicities |
| difference | Sum removed multiplicities, then truncate remaining counts at zero |
| symmetric difference | Parity by whole value; whole-value uniqueness is required |
| Text concatenation | Requires the specified total semantic order of contributions |

Unlike concurrent operations with no specified compatible composition fault rather than inventing a universal priority. Different collection operations within one sequential branch still execute in textual order; this incompatibility concerns their composition across concurrent branches. Ordered values retain their logical sequence. Stable causal provenance resolves cases expressly requiring an order; hashes, source-file order and scheduler timing are not semantic priorities.

Add/remove resolve an authorised collection, evaluate their operand and contribute the established insertion/removal intent. MissingIntermediate remains a no-op. Additions respect occurrence multiplicity; unique insertions merge equivalent occurrences with their joint causes, while keyed uniqueness retains the first admissible occurrence by stable provenance. Remove withdraws the specified occurrence/membership, including latent membership where admitted. They never change the static field schema.

> [!rule] MUD-EFFECT-010 — Exact-association composition
> Different exact keys compose. On one key, equal complete replacements merge, unequal replacements fault, replacements precede compatible partial changes, and independent partial components compose. Repeated deletion is idempotent; deletion wins over insertion, replacement and partial change. An intermediate missing-key no-op from a branch is not resurrected by another branch inserting that key.

Functional dictionaries have no writable runtime branch/result path. Full dictionary assignment is a replacement checked against its complete contract, not a collection of association proposals that can be silently repaired.

For value/key uniqueness over association proposals, first construct the joint candidate (so an atomic swap is valid). Unchanged existing associations have priority over colliding proposals; conflicting proposals are ordered by the established stable provenance. Reject each losing complete association proposal as a no-op, restoring its prior association if present. Recheck collisions after restoration, treating restored associations as unchanged. Each pass permanently rejects at least one proposal, so a finite group terminates in at most the number of proposals passes. The valid original dictionary is the fallback. Final domains/cardinalities are still checked.

## 6. Lifecycle and generations

Create/destroy resolve a permitted canonical lifecycle target and consult its explicit activity in the current private view. Create on active or destroy on inactive continues unchanged. Effective create introduces the initialised fresh materialisation/rule activation according to [[04-mathematical-model]]; effective destroy ends its owned load/memory. Suspension alone does not discard independently owned storage.

> [!rule] MUD-EFFECT-011 — Generation-bound structural composition
> Consolidate compatible activation before addition, then withdrawal before destruction. Concurrent activation of one absent identity is idempotent; concurrent create/destroy leaves it destroyed. This canonical order is unobservable and does not reorder instructions within one branch. A branch's sequential destroy/create ends the old generation and introduces a fresh one. Writes to the ended generation do not migrate to the new one.

Retain branch-local lifecycle continuity as well as its final activity; reducing destroy/create to an unchanged activity bit would lose reinitialisation. A no-op create does not reapply an initialiser or reset an observation episode. Relation withdrawal/restoration and whole-declaration suspension follow the established projection contract and are jointly validated, not destructive pruning of unrelated owners.

## 7. Traversal, calls and native effects

ForEach captures its finite enumerable source and semantic order at entry. Its optional step and filter obey the established type/purity/termination contracts. Bind each member (or complete exact key/value association) in the iteration scope; a false filter skips that iteration. Later source mutations do not add visits to this captured traversal.

Ordered iterations execute sequentially and see preceding iteration writes. Unordered iterations start from the same prior projection, including shared outer local slots, and combine their contributions by this chapter's batch algebra. They do not receive an invented source order. Fault/refusal and recovery retain the owning scopes; membership/generation permissions remain applicable to each destination.

An ActionCallCandidateEffect must elaborate into a permitted effectful action/subaction call. Execute it through the invocation-owned completion protocol of [[04-mathematical-model]]: bind/validate inputs, evaluate its guard, execute its private work, stabilise owned consequences, and check its after once before returning. Successful child contributions remain tentative; non-success rolls back their applicable scope. A bare call propagates Refusal/Fault; explicit capture obtains the ordinary ActionReply after settlement. No call opens an independent commit or exports an extra domain return value.

ForeignBlockEffect executes through its checked/trusted native contract. The adapter receives the permitted private read/write view, emits only authorised intents/occurrences, validates immutable bridge values and source maps failures to Error occurrences. A failed body exports no locals. It cannot write confirmed storage, retain writable handles or publish irreversible effects lacking a transactional/confirmed-delivery contract. ABI/hosting details are separate from this effect interface.

## 8. Block recovery and causal work

A protected block preserves its entry configuration. Refusal bypasses otherwise. Fault rolls back the failed protected work before clause selection. Select Error occurrences in stable causal order, with conjunctive role bindings and no implicit distinctness; a false filter leaves them pending. Clauses consume selected occurrences once in textual order. No on is catch-all.

Successful handler effects compose tentatively under ordinary authority. For value/expression recovery, equal compatible proposals agree and incompatible proposals fault. Unhandled or newly raised errors discard the recovery scope and propagate without reentering the same chain. Then and raise remain exclusive; there is no finally. Constructing an Error value alone does not raise it.

Causal outputs/firings preserve occurrence identity, multiplicity and all initiating owners. Jointly caused consequences belong to the nearest common enclosing invocation. They are available to the appropriate later wave, not by immediate physical execution order. This chapter neither collapses outputs by payload nor completes host projection for disappeared participants.

## 9. Root/wave batch judgment

Let $B$ be a finite set of sibling branch configurations with common entry $W_0$. Define $\operatorname{Batch}(W_0,B)$ by this algorithm:

1. Evaluate each branch privately under its owner, preserving its outcome and generation-bound intents. No sibling observes another's private prefix.
2. Apply protected-scope recovery/invocation settlement where owned by that branch; retain only surviving tentative contributions.
3. Normalise each surviving branch's replacements and lifecycle continuity; partition its intents by semantic root/generation/path. Preserve ancestor/descendant overlaps instead of treating reconstructed aliases as unrelated whole writes.
4. Compose compatible replacements, numeric stages, homogeneous collection operations, exact associations and lifecycle contributions using sections 3–6. Apply joint uniqueness after proposals are known; preserve causal outputs separately.
5. Rebuild the candidate effective projection. Normalise values under their type laws, validate all affected domains and completed stored cardinalities, including restored latent references and fresh initialised payloads.
6. Check effective always rules after the consolidated root/wave. A false condition yields AlwaysRefusal; unsuccessful evaluation yields Fault. A later wave cannot repair this failed checkpoint.
7. On success expose the consolidated tentative next view and pending causal outputs; on non-success discard the affected batch/resolution scope under the owner contract. Never publish a partial confirmed world or host delivery.

> [!rule] MUD-EFFECT-012 — Batch boundary
> A root and each wave use the same composition/validation boundary. Completed private blocks and all possible consolidations must satisfy the static stored-cardinality proof. Temporary deviations within an admitted private sequence are not observable by siblings or later waves. Runtime validation is a safeguard, not permission to omit the proof. Only successful outer completion confirms the world and delivers outputs.

The judgment can be written $W_0;B\Downarrow_{\mathrm{batch}}(W_1,U,o)$. On Continue, $W_1$ is the consolidated tentative next view; it may feed later waves. On Fault/Refuse there is no accepted next view from that attempt. Checkpoint/after ownership distinguishes a protected child scope from outer rollback; an explicitly observed child reply does not commit its effects.

This finite batch algorithm does not decide which causal wave comes next or certify that the resolution eventually stabilises. Those responsibilities belong to the invocation/wave/constraint chapters and their separately active questions. Imagine uses this same boundary in isolation and always discards its result state/outputs.

## 10. Coverage and conformance

[[effects/README]] maps all eight current Surface AST effect constructors and nine assignment operators to these sections. It contains contrasting declarative traces and bounded executable witnesses for sequencing and composition. Its validator checks finite witnesses and inventory synchronisation; it is not a MUD parser/typechecker/runtime or a proof about arbitrary native code, predicates, cycles or numeric portability.
