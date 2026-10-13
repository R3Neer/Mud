---
title: Static type contract corpus
status: proposed
normative: true
questions: []
decisions:
  - D-163
  - D-162
  - D-161
  - D-160
  - D-158
  - D-157
  - D-156
  - D-155
  - D-154
  - D-152
  - D-151
  - D-150
  - D-149
  - D-148
  - D-147
  - D-146
  - D-145
  - D-144
  - D-143
  - D-142
  - D-137
  - D-136
  - D-135
  - D-134
  - D-122
  - D-123
  - D-124
  - D-127
  - D-129
  - D-130
---

# Static type contract corpus

The contracts are specified in [[../11-type-system]], [[../15-fields-and-mutability]] and [[../21-expressions]]. The chapters remain proposed; this corpus does not promote their publication status.

- [[typing-cases.yaml]] contains declarative fragments with explicitly stated premises and expected static acceptance, rejection or runtime obligations. Fragments require their stated fixture; they are not claimed to be standalone programmes. source_scope distinguishes ordinary fragments, independently concurrent blocks and individual inclusion/representation judgements. A successful graph-equivalence judgement does not assert that the complete programme is well formed.
- [[expression-coverage.yaml]] associates every current Surface AST expression constructor with a chapter section and a case.
- validate_type_spec.py validates rule/constructor coverage and evaluates finite inclusion, callable-variance, productivity, graph-equivalence, structural-equality, static-given-selection and proof-boundary witnesses.
- generic_contract_witnesses.py checks supplied normalized type graphs with alias erasure and opaque nominal leaves, and independently supplied static call candidates from one lookup level.
- test_generic_contract_witnesses.py checks observable member/shape labels, recursive mismatches, phantom-family identity, candidate independence, defaults and selection failures.
- test_validate_type_spec.py exercises distinctions that must not collapse, including shape equivalence versus finite inhabitation and runtime admission versus mandatory static cardinality evidence.

Run the validator with python specification/types/validate_type_spec.py. Run the regressions with python -m unittest discover -s specification/types -p test_*.py. All diagnostics are in English.

Generic variance, application closure and inference fragments are declarative obligations, not claims of implemented solvers. Structural witnesses supply normalized symbolic labels and complete normalized union alternatives, matched independently of source order; they do not normalize MUD source or prove domain equivalence. Static-given witnesses supply pretyped possibilities and cannot use expected outputs or evaluate expressions. A structural equality judgement may be false without making its comparison expression ill typed; representation-judgement-fragment records that distinction.

A witness is a finite certificate in the validator's restricted language. Nat includes its intrinsic nonnegative domain; primitive ancestry cannot be overridden. Domain/leaf flags stand for supplied premises; the tool does not prove arbitrary predicates, parse the source fragments, resolve MUD names, typecheck MUD programmes or execute actions. Coverage and expected outcomes for non-witness fragments remain review obligations. The complete implementation conformance suite is separately scoped. Stored whole/partial holes, unique inference diagnostics, immutable pattern scopes and live-local sequential/temporal observations have reviewed declarative cases in typing-cases.yaml; these do not claim an implemented inference/evaluation engine.

- test_pruning_witnesses.py checks finite Bool/erased kernel pairs and demand sharing, plus empty/nonempty no-filter witnesses. It also checks derived/stored capture, ordered prefix demand and faults under and/or and equality, erased-initial-goal demand, and ordinary domain/collection boundaries. The witnesses operate on supplied residuals and callbacks, not Mud source or a general runtime.

- test_interval_witnesses.py checks supplied finite integral segment normal forms and descending step restart. It also contrasts a supplied exact rational grid with a rational inside the bounds but outside the grid. Continuous and domain-dependent interval normalization remain semantic review obligations.

- operator_contract_witnesses.py and test_operator_contract_witnesses.py check supplied finite operand-admission sets: strict specificity, crossed ambiguity, source-origin deduplication, duplicate local declarations, narrowed union coverage and direct/builtin/lifting priority. They do not discover Mud candidates, infer source types, encode arbitrary anchors or execute operator bodies.

- test_operator_identity_witnesses.py certifies canonical numbering of supplied small quotient graphs, nominal/domain/binder distinctions, ordered versus set edges and escaped scalar labels. Quotient construction and source normalization are supplied premises; it is not a complete operator identity encoder.

- test_dimension_witnesses.py checks supplied finite anchor/exponent maps, exact positive unit ratios, nominal unitless distinctions and Money signature rejection before cancellation. It is not a source unit/representation analyzer.

- test_rum_witnesses.py checks exact-rational certificates with supplied candidate/spacings: nearest-even ties, gradual underflow, overflow carry, mathematical truncating remainder and observable FMA differences. It does not implement a general binary64 converter, compiler or runtime.

`test_declaration_witnesses.py` checks supplied ancestry/strict-membership and initializer-origin certificates, applied family identity, shared datum origins and enumeration/key/member-order distinctions. Chapters 12 and 14 own these declaration contracts. These witnesses do not evaluate source programs.

The declaration certificates also check supplied comparison edges for the transitive functional-value exclusion, separately from derived fields, empty containers and supported projected keys. This does not implement whole-program equality eligibility analysis.

`test_quantitative_catalogue.py` compares the normative SI catalogue with its accepted decision and checks finite unitless-point identity/domain certificates, including literal rejection before cycle repair. It does not implement point evaluation or format inversion.
