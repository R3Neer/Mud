---
id: D-120
title: Element-wise block error recovery
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - Q-002
  - Q-007
affects:
  - Language contracts and their developed normative surfaces
---

# ADR-120 — Element-wise block error recovery

- Formalised by: [[ADR-124-expression-and-block-typing-coverage|D-124]].

## Context

The author selects optional on, conjunctive Error roles and recovery by error elements, retaining ordinary participant binding rather than predicates over an Errors aggregate. This completes the recovery contract of D-118.

## Decision

A block failure retains an internal occurrence list, including equal-valued but distinct errors. Handlers inspect these occurrences, not the Errors collection as one participant. On bindings admit only aliases specializing Error. All roles in one header must bind jointly before its if can run. Ordinary subtype matching applies; different roles do not imply distinctness. One occurrence may satisfy overlapping roles, but is consumed only once. Different occurrences remain distinct even if their values compare equal.

For each clause in textual order, enumerate compatible binding tuples in stable causal occurrence order. Evaluate its optional if for each tuple; false leaves those occurrences pending. A true filter (or absent filter) executes one branch for that tuple and removes its selected occurrences from this chain's pending set. Continue with unhandled occurrences; already consumed occurrences cannot be selected again. With no on, apply the catch-all once per pending occurrence. Errors produced by a handler, including its filter, propagate outward; they do not reenter the same handler chain. Their origin/cause is not fabricated: explicit wrapping can preserve the captured original as cause.

The protected block rolls back its own tentative writes before handlers run. Earlier successful work in the enclosing block remains tentative. Failed protected-body locals and partial exports are unavailable; handler bindings and valid enclosing locals are visible. All successful recovery writes remain tentative in a common recovery scope. If any original occurrence remains unhandled or a handler raises/fails, discard that scope and propagate the remaining original occurrences together with newly raised ones. If all occurrences are handled without new errors, the protected block resumes with its normal recovered result.

Then recovery preserves the protected category: expression recovery is externally pure and yields its expected result, value recovery may mutate only its private state and yields the expected value, and effect recovery has the surrounding effect permissions. Recoveries for independent occurrences compose under the ordinary common-view effect rules; compatible effects accumulate. A recovered expression/value has one result slot: equal compatible proposed values agree, and incompatible proposals produce an effect-composition error instead of arbitrarily selecting a value. Recovery cannot grant permission, publish earlier failed writes or convert a Refusal into Error.

Raise is confined to a recovery branch. Its value body yields one Error or a nonempty collection compatible with Errors. Flatten the collection while preserving distinct occurrences; empty and non-Error results are invalid. A long raise body is a normal value block and may have its own block handlers. Then and raise are alternatives; neither an arbitrary in-body raise statement nor finally is introduced. Otherwise raise is catch-all sugar.

Short effect recovery is admitted just like short ordinary then. Declaration/schema/metadata braces are not evaluated block owners. LocalStatementBlock is grouping within the owning ValueBlock and shares its error channel, without an independent handler list. Pure short-local RHSs normalize to ExpressionBlock with handlers, never private mutable ValueBlock storage.

For braces that are syntactically compatible with several block categories, the protected owner determines normalization; typing then checks the branch. A following otherwise belongs to the nearest complete eligible block. Braces delimit the handler when an outer handler chain is intended, so a raise value's own recovery cannot silently be flattened into its parent's chain.

## Verification

Cover joint subtype binding, overlapping roles, equal-valued occurrence multiplicity, false filters, untouched pending errors, rollback before recovery, propagation of newly raised errors, incompatible fallback results and effect recovery in short form. Structural regression tests reject loss of handler lists, branch exclusivity, explicit initialization, abstract aliases and imagine.

## Integration review

The grammar, CST catalogue, coverage, AST conversion and developed grammar/math surfaces agree. Handler names remain local nominal symbols; selection and result compatibility occur after nominal resolution. Complete operational proofs and exhaustive runtime error taxonomy remain Q-002 and Q-007, rather than an adapter ABI or executor implementation claim.
