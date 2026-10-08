---
id: D-147
title: Explicit raise in executable bodies
status: current
date: 2026-10-08
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/11-type-system.md
  - specification/21-expressions.md
  - specification/28-effects.md
  - specification/grammar/
  - specification/syntax/
  - specification/types/
  - specification/effects/
---

# ADR-147 — Explicit raise in executable bodies

## Context

The author accepts raise outside handlers and propagation through the existing block fault/recovery mechanism. This amends the handler-only restrictions in D-118/D-120, retaining their recovery and ordinary Error-value contracts.

## Decision

Raise is admitted in evaluated expression/value/effect positions, including alias operator bodies. Its value body must yield one Error or a nonempty Errors-compatible collection. Text, Refusal and empty are invalid payloads. Evaluate the payload under the context's existing permissions; success introduces Fault with those distinct Error occurrences and no normal result. Payload computation faults follow ordinary recovery first; no arbitrary Error subtype is introduced. Existing admission rules govern uncertain payload cardinality; no successful empty raise is possible.

A raised expression can check against the enclosing expected normal-result contract because it produces no normal value. It does not synthesize a nominal result from nothing; result-only raise computations without a determining context need annotation. This metalanguage property introduces no storable bottom/never type.

Deliver the fault to the producing block's recovery, then propagate unhandled errors outward under existing call/protected/invocation ownership. Newly raised handler errors leave that handler chain, while nested payload blocks keep their own recovery. Existing explicit ActionReply capture/observation boundaries remain in force. No alternative catch search, transaction or scheduler is introduced.

Pure contexts may fault but gain no world-write permission. A statically evaluated initializer with an unhandled fault is inadmissible. Resolve/type all source, including skipped continuations. A fault skips dependent runtime continuation and discards the applicable failed scope before recovery. Constructing/passing an Error remains ordinary value production; empty, false and Refusal retain their ordinary meanings. Raise is not return/break/continue and no finally is introduced.

## Alternatives and consequences

Reject handler-only raise and automatic throwing of Error-shaped values. Explicit faults simplify partial computations without requiring fabricated return values. Recovery/propagation stays shared with existing computation failures.

## Verification

MUD-TYPE-030, RaiseExpr/RaiseEffect/RaiseValueStatement, token fixtures and reviewed nested recovery/value-versus-fault cases cover the contract. Error subtype naming remains the existing Q-007 scope. No chapter is promoted.
