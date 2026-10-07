---
title: Textual patches and host observation design
status: analysis
tags:
  - mud/analysis
  - mud/runtime
---

# Textual patches and host observation design

## Accepted boundary

[[decisions/ADR-140-readable-patches-and-host-only-confirmation-tickets|D-140]] fixes automatic incorporation, readable textual patches and host-only tickets. A patch represents incorporated work for inspection/reproduction, not executable source or a second application caused by reading it. Success is already an alias; its component/accessor choice is still [[questions/Q-073-textual-patch-contract-and-reproduction|Q-073]].

Do not define a concrete Patch alias, serializer or file extension before completing the causal foundation in [[questions/Q-072-causal-work-and-reality-completion-algorithm|Q-072]]. Distinguish the public semantic format from private physical journal entries and the later semantic IR.

## Candidate semantic contents — not a schema

Consider programme/world/base-projection identity, typed destinations and materialisation generations, evaluated transforms, read dependencies/application conditions, contribution and parent/joint identities, lifecycle continuity and ordered causal observations. Identify how an aggregate accounts for already incorporated children exactly once. Keep exterior intentions distinguishable from state operations.

A final-value map alone loses concurrent increments; raw transformations alone do not prove admissibility after the base changes. A patch library must validate application, detect duplicates and preserve the existing effect algebra rather than invent textual merge rules.

## Host confirmation and delivery

Existing message observations use the specified Ticket envelope. Generalised observation objects remain [[questions/Q-074-generalised-host-ticket-and-exterior-intentions|Q-074]]. Provisional read-only patch views are a candidate, not currently a complete API. Inner confirmation is not Kept; terminal Kept follows surviving stable-root incorporation. Dropped records containing-scope disposal. Neither state gives mutation/cancellation authority.

Prepare an exterior write provisionally, confirm its origin, then execute it under the adapter contract. A disk or network write can fail after world confirmation: Kept cannot stand in for its execution result. Failure reporting, retries, idempotency and recovery are pending; no automatic compensating action or new source syntax is selected. Transactional adapters must state their real guarantees instead of assuming atomicity between a world and a database.

## Recording products — not TOML options

| Product | Intended purpose | Remaining obligations |
| --- | --- | --- |
| Confirmed patch records | Reconstruct admitted state transitions. | Format, base/preconditions, compatibility and duplicate handling. |
| Execution input records | Re-execute under admitted contracts. | Requests, native inputs, versions, environment and randomness; limits on nondeterministic operations. |
| Diagnostic traces | Explain waves, waits, failures and discarded scopes. | Access, retention, level/branch distinctions and no publication as confirmed activity. |

These products have different guarantees. No combination promises automatic replay of irreversible exterior effects. Configuration names, defaults, record destinations and retention remain open; examples in descriptor design are not selected fields.
