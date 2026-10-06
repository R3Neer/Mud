---
id: D-121
title: Typed foreign adapter contracts
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - Q-007
  - Q-069
  - Q-070
affects:
  - Language contracts and their developed normative surfaces
---

# ADR-121 — Typed foreign adapter contracts

- Formalised by: [[ADR-123-static-capabilities-and-conflict-proof-boundaries|D-123]].

## Context

The author retains access to native ecosystems, including Python, through checked or explicitly trusted contracts rather than requiring every native library to prove purity. This refines D-109 at the abstract type/effect boundary; it does not implement native hosting.

## Decision

Each foreign operation contract identifies captured inputs, their MUD/native representations, output conversions and inferred types, read dependencies, writable footprints, determinism, static-evaluation eligibility, error translation and isolation/lifetime obligations. Capture resolution uses the surrounding nominal environment; typing validates each capability and domain. Contracts distinguish native private mutation from externally observable writes. Read-only parameters alone do not imply purity: global state, retained references, callbacks and I/O also matter.

Contracts may be checked by the adapter or explicitly trusted by their author. Trust supports libraries whose native signatures do not express MUD's guarantees. Tooling reports the specific trusted obligation and its call site in English; it does not pretend that an unanalysed Python function has been proved pure. Unknown effects cannot acquire a pure/static contract by omission. Static owners require an explicit pure, deterministic and statically evaluable contract. Effect owners admit authorised tentative writes; expression owners admit only externally pure work, and value owners may additionally mutate private local state.

Wrappers preserve outer and inner capabilities, domains, cardinality, dictionary uniqueness/order and effective nominal types. A native representation may be used directly only when semantically equivalent. Text is immutable text; exact Num cannot silently become a binary float; Rum preserves its binary64 semantics. Nominal aliases retain their nominal identity even when represented by native records. Copy/freeze or checked wrappers prevent hidden mutable aliases from escaping. Identity-bearing inputs remain handles governed by MUD permissions rather than copies that acquire new world identity. An inbound conversion fails instead of clipping, rounding, changing cardinality or guessing between incompatible types. Omitted bridge annotations require a unique converted MUD type.

All world reads are dependency-tracked, and authorised writes enter the owning tentative journal. Exceptions, failed conversion and failed native calls publish neither partial exports nor attempted writes. Wrappers cannot retain writable access beyond the owning evaluation. Imagination needs isolation of external work too; irreversible I/O is deferred to confirmed delivery or requires an explicit transactional adapter guarantee. Rollback does not promise that arbitrary native side effects can be undone. Native resource cleanup belongs to adapter lifetime management; no MUD finally is introduced.

A translated native semantic failure is an Error specialization with mandatory MUD Declaration origin, specific reason and optional cause. Diagnostics carry a source-mapped native call site. Native source locations do not become fictional MUD Declaration values. Wrapping may retain a translated inner Error through cause; a returned native error-shaped record is still an ordinary value until a contract translates it into the error channel. Engine defects/resource interruption are not silently translated into model errors.

The baseline named Error aliases are ArithmeticError, DomainError, CardinalityError, EffectConflictError and AdapterError, each specializing Error and inheriting its required reason/origin and optional cause. Static conceptual descriptions are metadata, not duplicate message fields. Adapter-specific/user specializations may add required ordinary components. This baseline does not exhaust all invalid operations or prescribe an ABI error code format; Q-007 retains that catalogue/proof work.

The abstract obligations are fixed. Rust/Python/Csharp wire representations, ABI/version negotiation, borrowing/copying tables, native hosting/AOT, cancellation/reentrancy, dependency installation and source-map protocols remain Q-069/Q-070. Initial planned adapters and the Rust reference backend are not claims of delivered implementations.

## Verification

Conformance cases distinguish checked/trusted purity from read-only signatures, reject uncontracted pure calls, preserve immutable exports and nominal/collection conversion, reject retained writable handles, and discard partial writes/exports on translated failure. Native implementation tests belong to their adapters when implemented.

## Integration review

The existing foreign grammar and AST already preserve language label, code, capture/export names, source provenance and annotations. Nominal resolution supplies bindings; later typing/effect checking consumes contracts. No semantic type, native ABI layout or ownership journal is inserted into nominal HIR. Developed syntax/name chapters record these boundaries; no temporary type chapter is created.
