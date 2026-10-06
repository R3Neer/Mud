# Nominal resolution from the MUD

This directory contains the contract regulatory mechanism for the name resolution. Add [[../09-names-and-anchors|09. Names, paths and anchors]] and does not define a type or semantics dynamics.

## `mud-nominal-hir.asdl`

It is the regulatory solution to nominal resolution on the Surface AST. It preserves symbols, scopes, resolved bindings, pending receiver-call candidate sets with lookup levels, anchors and nominal relationships `Owns`, `Specializes` and `RefersTo`.

It must not contain effective types, effective domains, inferred cardinalities, narrowing, elaborate conversions, effects, semantic dependencies or evidence of termination. These conclusions relate to later stages that have not yet been formalised in technical terms.

`ResolvedReference` names one nominally resolved target. `PendingReceiverCall` retains at least two distinct anchored nominal callables governed by `for`, from the first non-empty lookup level, ordered by anchor for canonical serialisation. It contains no compatibility verdict or chosen target and produces no `RefersTo` edge towards a candidate. Elaboration performs static receiver selection as defined in [[../09-names-and-anchors#Receiver-call selection|chapter 09]].

The Nominal HIR It is derived and reconstructible: it does not constitute a source semantics independent.

## Validation

From the repository root:

```powershell
python specification/syntax/validate_syntax_model.py
python specification/syntax/test_validate_syntax_model.py
```

The validator checks ASDL type references, the resolved/pending reference sum, candidate and lookup-level storage, and the exclusion of elaboration fields. The regression suite checks that malformed contracts are rejected. Neither command resolves or executes MUD calls; candidate-set cardinality, candidate visibility and receiver compatibility remain semantic conformance obligations.

