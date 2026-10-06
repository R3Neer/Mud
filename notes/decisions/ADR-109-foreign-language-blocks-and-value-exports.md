---
id: D-109
title: "Foreign language blocks and value exports"
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - Q-069
  - Q-070
affects:
  - "Foreign blocks, lexical delegation, grammar, CST, Surface AST, nominal resolution, capabilities, adapters and tooling"
---

# ADR-109 — Foreign language blocks and value exports

- Implements the coordination direction of [[ADR-107-executable-language-and-rust-reference-implementation|D-107]].
- Modifies: [[ADR-066-static-values-and-local-bindings-in-then|D-066]], [[ADR-071-local-bindings-in-boolean-blocks|D-071]], [[ADR-096-modules-callables-look-message-and-activation|D-096]] and [[ADR-101-value-blocks-stored-local-variables-and-witness-extrema|D-101]].
- Preserves the nominal phase boundary of [[ADR-097-current-nominal-hir-and-deferred-semantic-ir|D-097]].

## Decision

`from Language` delegates a body to a language-specific adapter. A short body contains exactly one foreign instruction or MUD export; braces are required for multiple instructions, independently of line count. `mud name [: Type] <- foreignExpression` is a bridge: its name and optional annotation use MUD syntax, and its RHS uses the selected foreign language. `mud` is contextual at the bridge position, not a globally reserved name.

Exports are immutable MUD values without a new world identity, mutable slot or public anchor. Their RHSs are evaluated once at their textual positions in each block evaluation. Exports become visible to subsequent MUD statements after successful completion of the `from` block; earlier exports may be read by subsequent foreign items. A failed block publishes no exports. Adapter-owned locals remain private. Only direct body items introduce exports; a native nested computation returns through a direct bridge. A type annotation may be omitted only when conversion and inference determine a unique MUD type.

The construction occupies statement/preamble positions in existing compatible MUD bodies. It does not become a primary expression or a top-level declaration. `ExpressionBlock`, shared behavioural preambles and test assertions' common preambles admit externally pure foreign calculation. `ValueBlock` and local statement blocks additionally permit private mutation confined to the owning value computation. `EffectBlock` admits only its ordinary authorised effects. Static owners still require static evaluation of the complete value body.

Visible MUD values may be supplied to foreign code under their existing visibility and capabilities. Neither declaring a participant immutable nor entering foreign code grants additional writes. Wrappers must preserve final write footprints, track reads and route authorised world writes into the private transaction. No adapter may expose direct confirmed-state storage or retain writable handles beyond the invocation. Arbitrary I/O or irreversible foreign effects cannot be rolled back by MUD patches; they must be deferred to confirmed messages/host delivery or covered by an explicit transactional adapter contract.

Foreign contracts must describe effects, reads, dependency capture, determinism, errors and conversion. A signature claiming that an argument is unmodified is insufficient evidence of purity. Static evaluation requires an explicitly statically evaluable, pure and deterministic adapter contract; it does not execute arbitrary libraries at build time. Guarantees involving foreign code remain conditional on trusted or checked adapter contracts.

Wrappers preserve nominal aliases, domains, exact numbers, collection cardinality, uniqueness, order and capabilities. Native representations are usable only when semantically equivalent. Inbound results are validated and copied or wrapped without hidden mutable aliases. An opaque foreign object is not itself an exported MUD value. The precise ABI, conversion/lifetime and exception rules remain Q-069 and Q-070; unknown contracts cannot be assumed safe.

Rust, Python and Csharp are the initial planned adapter labels; Csharp denotes C#. The adapters parse native code with its language tooling and expose virtual documents and source maps. C# may use Roslyn for semantic tooling. Selection of a Rust backend does not translate Python or C# into Rust. Runtime hosting, dependencies and Unity/AOT build integration need explicit adapter implementations; none is claimed here.

## Verification

The EBNF, CST catalogue, coverage, Surface AST, conversion and nominal chapters are updated together. Declarative conformance cases cover single/multiple instructions, continued expressions, native strings/comments, scopes, inference, capabilities, static evaluation, dependencies, conversion and failure. Mechanical validators verify structural contracts; these cases do not claim an implemented multilingual parser or runtime.
