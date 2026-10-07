---
id: Q-073
title: Textual patch contract and reproduction
priority: P1
opened: 2026-10-07
resolved:
closed:
decisions:
  - D-140
affects:
  - Patch schema, action reply access, state integration and reproduction
superseded-by: []
---

# Q-073 — Textual patch contract and reproduction

## Already decided

Incorporation is automatic. Successful incorporated changes must be obtainable as a readable serialisable textual Mud patch. No mandatory disk file, extra action-domain return or source-level patch schema has been chosen. Patches do not replace the accepted effect algebra.

## Pending

Define the patch's semantic contents and textual grammar/version, success access, originating world/programme/projection identity, preconditions, transforms and read dependencies, generations, nested/joint contributions, once-only incorporation and validation against an incompatible destination. Distinguish state changes from exterior intentions and transition reconstruction from programme re-execution. Derive these rules from Q-072's completed causal algorithm, not a physical journal or semantic IR schema from Q-009.

## Closure criteria

- C1: Specify canonical semantic patch contents and versioned textual encoding, with parsing/round-trip and compatibility examples.
- C2: Specify the ActionReply/Success access contract without a second domain return and without confusing observation with application.
- C3: Specify incorporation/replay admission, dependency/precondition checks, ownership/generations, duplicate detection and conflict cases, including relative child and joint changes.
- C4: Define required records and guarantees for transition reconstruction versus re-execution, covering exterior inputs, randomness, failed attempts and excluding unsupported replay of irreversible operations.
