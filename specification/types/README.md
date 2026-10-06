---
title: Static type contract corpus
status: proposed
normative: true
questions: []
decisions:
  - D-122
  - D-123
  - D-124
  - D-127
---

# Static type contract corpus

The contracts are specified in [[../10-type-system]], [[../14-fields-and-mutability]] and [[../19-expressions]]. The chapters remain proposed; this corpus does not promote their publication status.

- [[typing-cases.yaml]] contains declarative fragments with explicitly stated premises and expected static acceptance, rejection or runtime obligations. Fragments require their stated fixture; they are not claimed to be standalone programmes. source_scope distinguishes ordinary fragments, independently concurrent blocks and individual inclusion/representation judgements. A successful graph-equivalence judgement does not assert that the complete programme is well formed.
- [[expression-coverage.yaml]] associates every current Surface AST expression constructor with a chapter section and a case.
- validate_type_spec.py validates rule/constructor coverage and evaluates finite inclusion, callable-variance, productivity, graph-equivalence and proof-boundary witnesses.
- test_validate_type_spec.py exercises distinctions that must not collapse, including shape equivalence versus finite inhabitation and runtime admission versus mandatory static cardinality evidence.

Run the validator with python specification/types/validate_type_spec.py. Run the regressions with python -m unittest discover -s specification/types -p test_*.py. All diagnostics are in English.

A witness is a finite certificate in the validator's restricted language. Nat includes its intrinsic nonnegative domain; primitive ancestry cannot be overridden. Domain/leaf flags stand for supplied premises; the tool does not prove arbitrary predicates, parse the source fragments, resolve MUD names, typecheck MUD programmes or execute actions. Coverage and expected outcomes for non-witness fragments remain review obligations. The complete implementation conformance suite is separately scoped.
