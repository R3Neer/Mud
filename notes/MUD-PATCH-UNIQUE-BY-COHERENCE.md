---
temporary: true
temporary-reason: "Control plan for the /patch that integrates keyed collection uniqueness."
temporary-delete-when: "The published unique-by change has completed its post-publication fixed-point audit."
---

# Keyed uniqueness patch coherence plan

## Accepted decisions

- `unique` keeps its existing whole-value uniqueness semantics.
- `unique by path` adds keyed uniqueness: at most one occurrence may survive for each semantically equal key obtained by evaluating `path` from a member.
- When several occurrences have the same keyed-uniqueness key, the first by stable provenance survives; later occurrences are discarded.
- Adding or inserting a value whose key is already represented is a no-op.
- When a source-level initialiser or literal contains a key collision that is statically provable, normalisation retains the first occurrence and emits a non-blocking warning identifying exactly which occurrence survives. Cardinality is checked after normalisation, as for ordinary `unique`.
- Concurrent distinct insertions with the same key are resolved by the existing stable-provenance machinery; the earliest surviving provenance wins. They are not treated as a conflict and are not merged into one value.
- `unique` and `unique by path` are mutually exclusive forms of one uniqueness axis.
- The key path has the same non-empty, singular and transitively stable path shape used by `ordered by`; unlike an ordering key, its final value needs semantic equality but not a total order.
- `unique by` is available anywhere the collection uniqueness modifier is available, including local collection transformations and derived collection shapes.
- On dictionaries, the uniqueness axis continues to constrain associated values. `unique by path` interprets `path` from each associated/result value, never from the dictionary key. Exact-dictionary insertions or replacements that collide on that projected key are no-ops; functional results use the same per-application normalisation rule.

## Open questions

None block this patch. Existing unrelated open questions must remain open. Q-006 remains partially decided, but its already-decided inventory must be extended to cover keyed-uniqueness insertions; the remaining closure criteria are unchanged.

## Rejected alternatives

- Treating a keyed collision as an error or conflict.
- Replacing the first occurrence with the last occurrence.
- Allowing both ordinary `unique` and `unique by ...` simultaneously as independent modifiers.
- Requiring a total ordering merely because a key is used for uniqueness.
- Reinterpreting `unique by` on a dictionary as a second uniqueness constraint on dictionary keys.

## Expected interactions and invariants

- Normalisation order remains domain restriction -> uniqueness -> order -> cardinality.
- `ordered by` retains its existing total-order requirement; `unique by` does not weaken it.
- Stable provenance remains distinct from logical order and is the source of the first-survivor rule.
- `unique by` implies ordinary whole-value uniqueness because equal values necessarily yield the same stable key, but it carries an additional keyed invariant.
- Binary collection algebra remains defined over whole-value multiplicities. Result uniqueness metadata must be conservative: keyed uniqueness is retained only when the result is guaranteed to preserve that exact invariant without inventing a new criterion. Union and symmetric difference may therefore degrade a keyed guarantee to ordinary value uniqueness rather than silently deduplicating by key.
- Exact-dictionary algebra retains its established left-association precedence and no-op enforcement of result value uniqueness; keyed uniqueness applies the same mechanism to projected value keys. Functional-dictionary algebra remains pointwise collection algebra.
- No new keyword is introduced: `unique` and `by` are already reserved.
- No new declaration, scope, owner or public anchor is introduced. Existing name-resolution surfaces must nevertheless be checked because the new keyed path contains member references.

## Impact matrix

| Surface | Conclusion | Reason |
| --- | --- | --- |
| Accepted decision archive | modificar | Record D-105 and reciprocal/current-state amendments where existing ADR wording would otherwise be incomplete. |
| Decision index | regenerar | New D-105 must appear in the generated index. |
| Questions | modificar | Q-006 must cite D-105 and record keyed-collision insertion compatibility while remaining partially decided. Other open questions remain unchanged. |
| Lexicon | validar sin cambios | `unique` and `by` already exist as reserved words. |
| Concrete grammar / EBNF | modificar | `unique by path` must be recognised in stored and local collection modifiers; genericise the shared key-path production. |
| Concrete grammar prose | modificar | Document syntax, duplicate-modifier rules, dictionary interpretation and keyed normalisation diagnostics. |
| Lossless CST model | modificar | Existing nodes can preserve the form, but contextual validation prose must treat ordinary and keyed uniqueness as one axis. |
| Syntax kinds catalogue | modificar | Mirror the EBNF and shared key-path production. |
| Syntax coverage | modificar | Rename/generalise the path mapping and preserve modifier coverage. |
| CST -> Surface AST | modificar | Project ordinary and keyed uniqueness into distinct AST constructors and reject duplicate uniqueness-axis forms. |
| Surface AST ASDL | modificar | Replace Boolean uniqueness with an explicit uniqueness sum and add keyed local uniqueness. |
| Abstract-syntax prose | modificar | Describe the new uniqueness representation and invalid-state prevention. |
| CST/AST conformance cases | modificar | Add valid keyed forms, duplicate-axis rejection and projection cases. |
| Nominal resolution chapter | validar sin cambios | Path components reuse existing member resolution; no names/scopes/anchors are introduced. |
| Nominal HIR ASDL | validar sin cambios | Keyed uniqueness is elaboration/type semantics, not a nominal symbol or graph edge. |
| Collection algebra semantics | modificar | Generalise result uniqueness guarantees conservatively across value-unique and keyed-unique operands. |
| Local transformation semantics | modificar | Deduplicate by key in provenance order before ordering/cardinality. |
| Concurrent effect semantics | modificar | Key collisions use stable provenance to select one survivor rather than conflict/merge. |
| Dictionary semantics and algebra | modificar | Extend associated-value uniqueness and pointwise functional results to keyed criteria without changing intrinsic dictionary-key uniqueness. |
| Reflection / metadata | validar sin cambios | No existing reflective contract currently exposes collection uniqueness criteria; global search must confirm. |
| Validators / generators | modificar | Run official generators/gates and extend persistent syntax coverage checks for the new cases; otherwise preserve validator semantics. |
| Residue search | modificar | Search for `is_unique`, `make_unique`, `order_key_path`, `order-key-path`, prose stating uniqueness is only whole-value, and duplicate-modifier assumptions. |

## Fixed-point audit checklist

- Every positive statement that collections permit only `unique` by whole value has been generalised where necessary.
- Every structural grammar surface agrees on `unique [by path]`.
- Surface AST cannot encode ordinary and keyed uniqueness simultaneously.
- Local transforms can encode keyed uniqueness without manufacturing inner `[mut]`.
- Keyed collisions in literals, sequential additions and concurrency all select the same first-by-provenance survivor.
- Ordering and uniqueness path requirements differ only at the final-key comparator requirement.
- Algebra never claims a keyed invariant that an operation can violate through cross-operand collisions.
- Exact and functional dictionaries interpret keyed uniqueness on associated/result values, not dictionary keys.
- Q-006 records the newly fixed compatibility without closing unrelated conflict work.
- No temporary control file or workflow is present in the publication commit.
