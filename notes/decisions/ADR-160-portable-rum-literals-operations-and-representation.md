---
id: D-160
title: Portable Rum literals operations and representation
status: current
date: 2026-10-13
supersedes: []
superseded-by: []
questions:
  - Q-058
affects:
  - specification/11-type-system.md
  - specification/21-expressions.md
  - specification/28-effects.md
  - specification/08-concrete-grammar.md
  - specification/types
---

# ADR-160 — Portable Rum literals operations and representation

## Decision

The author accepts nearest binary64 literal conversion with ties to even, subnormal support and gradual underflow to zero, and truncating-quotient Rum remainder. The author directs remaining choices toward ordinary portable double behavior: each arithmetic site rounds to binary64, and constant evaluation preserves the same sites and errors. Automatic contraction/reassociation is invalid whenever it changes observable values, errors or dependencies. No source FMA API is introduced.

Retain Mud's established exceptions from D-034: nonfinite results/zero divisors produce errors and negative zero normalizes to positive zero. Explicit quantitative integer conversions retain their existing ties-to-even policy; remainder's internal mathematical quotient is not such a source conversion.

Use the rational-to-binary64 procedure and unique finite canonical word in MUD-TYPE-038. Subnormal and zero results undergo ordinary domain admission; underflow alone is not an error. Reject unrepresentable literals; producing computations retain their Normal/Fault and protected recovery contracts. Required static evaluation must finish normally after applicable recovery. Folding cannot turn a skipped computation into demanded work or erase a demanded fault.

Derived magnitude representation uses existing signatures at each original product/quotient: Rum/Rum yields Rum; implicit mixed exact/Rum or Money/Rum remains invalid. An explicit result annotation cannot create a mixed signature or hidden conversion. Unit literals use the already-contextualized numeric literal then checked unit-to-canonical scaling; the symbolic exact unit factor is not a source Num operand or authority for arbitrary mixing. Unit presentation remains distinct from canonical coordinate identity.

## Verification and scope

Completes Q-058's numeric/static semantics: decimal spelling, one literal rounding, each operation, subnormals/underflow, intermediate precision, observable FMA/constant behavior, canonical finite bits and derived representation inference. Physical IR schema is Q-009 and foreign conversion protocols remain Q-069/Q-070; these do not reopen the numeric contract.

Chapter rules and finite exact-rational certificates cover halfway values, 0.1, the subnormal boundary, zero, overflow, remainder signs and double-rounding/contracted arithmetic differences. They are supplied witnesses, not a compiler or runtime implementation. D-034/D-028 current bodies and active indexes are reconciled.
