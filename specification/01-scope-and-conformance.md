---
title: Scope conformance and versions
aliases:
  - Scope from the specification MUD
tags:
  - mud/specification
status: current
normative: true
depends-on:
  - "[[00-editorial-conventions]]"
questions:
  - Q-038
decisions:
  - D-167
  - D-168
  - D-159
  - D-157
  - D-155
  - D-148
  - D-013
---

# 01. Scope, conformance and versions

## Scope and authority

This specification defines Mud syntax, static contracts, applicable observable semantics and conformance evidence. Compiler implementation language, physical IR/storage layout, backend and analysis implementation are not language rules. Source and mechanical normative contracts are complementary; discrepancies are defects under [[00-editorial-conventions]].

A chapter's normative surface and publication status are distinct. A proposed/draft chapter may integrate accepted contracts but cannot replace current decisions or introduce semantics for an active question. A conformance claim cannot rely on an illustrative example alone or silently choose a result for an unspecified feature. Complete language conformance requires all applicable contracts; a checked subset must be identified as partial conformance.

This chapter publishes fixed-target source/static conformance and the interpretation of partial claims. Descriptor version selection/discovery, source/IR/state migration and complete dynamic conformance are separate protocols, not prerequisites silently supplied by this chapter.

## Target language version and static conformance

> [!rule] MUD-CONF-001 — Fixed-target static claims
> A static conformance claim identifies the effective language target and covered constructs. Changing compiler releases under that target must preserve its normative grammar, type/visibility/capability contracts, reflective catalogues and certification procedure. A tool resource interruption is incomplete verification, not an invalid-program judgement or a new admission policy.

Let $V$ be a specified language target, $P$ a resolved program under that target and $C$ the claimed construct scope. Write $\mathsf{Check}_V(P,C)$ for the completed normative static procedure over that scope, with its explicit premises and permitted runtime admission obligations. Its result distinguishes accepted, proved-violation rejection and completed-but-unproved rejection. Resource-interrupted checking does not supply a completed judgement. [[11-type-system]] defines the evidence/admission boundary; source/application finiteness and body termination follow [[types/finite-static-certification]] and [[types/termination-certification]].

For conforming implementations $I$ and $J$ which both complete this procedure under the same $V$, equal input contracts and scope imply equal acceptance/rejection results and normalized static contracts. Internal caches or a shared reference analyzer do not alter the judgement. This is a conformance requirement, not a claim of an implemented analyzer or completed operational/advanced-profile certification.

An implementation may support several language targets. Its supported targets and actual selected target are distinct from its software release identifier. It must not report completed conformance to an unsupported target or substitute a newer target without identifying that change. This does not select a default project version, command-line option or descriptor field.

## Catalogue and source compatibility

TypeKind and other fixed reflective families are interpreted under the selected target. A later target's members are not merged into the earlier one. Source rechecked under another target must satisfy that target's complete contracts; added closed-family members may affect exhaustive uses. No implicit Other/unknown member is synthesized.

Define static compatibility for a particular source and target pair as acceptance under both with equivalent relevant normalized public contracts. Source acceptance alone does not imply unchanged numeric evaluation, observable execution, persistence or migration compatibility. Those properties require their own applicable guarantees; no major/minor version numbering policy or future backwards-compatibility promise is assumed.

| Case | Required treatment |
| --- | --- |
| New compiler release, same language target | Preserve the same grammar/catalogue/analysis contract. |
| New compiler with a stronger nonnormative solver | May explain/suggest; cannot expand admission under the same target. |
| Same source checked under another language target | Recheck all affected contracts; no automatic compatibility conclusion. |
| Another target adds a closed-family member | Earlier target retains its original family; exhaustive use must be rechecked under the newer one. |
| Tool cannot complete due to memory/time | Report incomplete verification, not semantic invalidity. |
| Library adds an alias or family | Use existing public TypeKind forms; no programme-defined TypeKind extension. |

## Independent static scope and unresolved protocols

Static scopes may document established construct contracts over explicit proof/effect premises while related advanced analysis procedures remain incomplete. They must not claim a complete admission algorithm or operational conformance on that basis. Reactive/always/public-operation typing does not define the causal scheduler, host protocol or foreign ABI.

Project version declaration, default selection/discovery and migration of source/IR/materialized worlds remain [[../notes/questions/Q-038-c-compatibility-between-language-versions|Q-038]]. Their descriptor/distribution, semantic IR, migration and persistent runtime protocols are not supplied by a fixed-target conformance claim. Supporting static chapters may use this boundary without inventing those protocols.
