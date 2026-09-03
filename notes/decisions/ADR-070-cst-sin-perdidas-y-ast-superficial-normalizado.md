---
id: D-070
title: "Lossless CST and normalised surface AST"
status: current
date: 2026-08-02
supersedes: []
superseded-by: []
questions: []
affects:
  - "source text, lexicon, concrete grammar, CST, surface AST and editorial validation"
---

# ADR-070 — Lossless CST and normalised surface AST

- Amended by: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]
- Extended by: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]
- Adjusted to the phase boundary of [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].
- Amended by: [[ADR-096-modulos-callables-look-message-y-activacion|D-096]].

## Status

Current.

This decision has been updated to the current vocabulary and grammar: it uses the short numeric types from [[ADR-067-nombres-breves-de-tipos-numericos|D-067]], incorporates the intrinsic `name` from [[ADR-068-thing-universal-y-nombre-intrinseco|D-068]] and represents double-quoted literals in accordance with [[ADR-069-literales-char-con-comillas-dobles|D-069]]. In particular, the surface AST does not invent a distinct lexical node for `Char`; that elaboration requires type context.

## Context

MUD's concrete grammar defines which programmes can be recognised, but is not enough to:

- Reconstruct a file exactly.
- Preserve comments and formatting.
- Implement a formatter or refactoring tool.
- Distinguish punctuation from semantic structure.
- Specify which syntactic sugar survives parsing.
- Keep name resolution and typing out of the parser.

One tree cannot meet all these needs. A fully concrete tree is awkward for semantic analysis; a normalised one loses information required for editing.

## Decision

MUD defines two separate normative syntactic representations:

1. A **per-file lossless CST**.
2. A **normalised surface AST**, aggregatable in `MudProject`.

The phase chain is:

```text
text
→ complete scanner
→ lossless CST
→ contextual syntactic validation
→ surface AST
→ nominal resolution: symbols + bindings + partial graph
→ typing/elaboration
→ semantic representation after typing and elaboration
```

## CST

The CST:

- Preserves every written token.
- Preserves whitespace and comments as trivia.
- Preserves the physical form of line breaks.
- Preserves explicit and implicit closing of `Text`.
- Can represent invalid input through missing tokens and error regions.
- Reconstructs the original bytes except for the BOM, which is retained as metadata.
- Does not resolve names or types.

All trivia belongs to the following significant token. `EOF` owns the final trivia.

## Surface AST

The surface AST:

- Removes trivia, delimiters and terminators.
- Normalises cardinalities, intervals, blocks and declared sugar.
- Preserves source order for internal lists.
- Preserves unresolved names.
- Preserves distinct operators when their spelling carries meaning.
- Uses `flag = Disabled | Enabled` for boolean properties.
- Carries provenance on every node except `MudProject`.
- Contains no ordinary comments.

## Project and file

The CST has a root only per file. The project is a semantic aggregation of files, not concrete text.

`MudProject` orders files canonically by normalised path solely for structural serialisation. The order has no semantic meaning.

## Comments

Current comments are ordinary trivia. They are removed from the significant stream consumed by the grammar, but not from the CST.

A future structured documentation system will use a separate document tree and resolvable references to anchors; it will not turn ordinary comments into executable AST declarations.

## CST-to-AST validation

Forms that the EBNF can recognise but that cannot be represented unambiguously in the normalised AST are validated before it is built. Examples include:

- Duplicate modifiers.
- Duplicate metadata declarations for one owner, including units.
- Missing mandatory properties.
- Invalid argument order.

Name resolution and typing remain outside this phase.

## Deferred ambiguities

The surface AST retains these undecided:

- Qualified path versus a chain of semantic accesses.
- Structural literal versus receiver tuple.
- Postfix call versus action call.
- Contextual type of literals.

These decisions belong to nominal resolution when they depend only on identity and bindings, or to later typing and elaboration phases when they require types or other elaborated conclusions.

## Provenance

`SourceSpan` uses UTF-8 byte offsets, zero-based positions and an exclusive end. The column counts Unicode scalar values. LSP converts to UTF-16 at the boundary.

A synthesised node retains an anchoring span and a synthesis reason.

## Normative artefacts

The decision is embodied in:

- `specification/syntax/cst-sin-perdidas.md`.
- `specification/syntax/mud-syntax-kinds.yaml`.
- `specification/08-sintaxis-abstracta.md`.
- `specification/syntax/mud-surface-ast.asdl`.
- `specification/syntax/cst-a-ast-superficial.md`.
- `specification/syntax/cobertura-sintactica.yaml`.

## Positive consequences

- Parser and IDE share a lossless representation.
- Semantic analysis does not depend on punctuation.
- Normalisations are auditable.
- Grammar coverage can be validated automatically.
- Future refactorings can preserve comments and formatting.
- Resolution is not introduced prematurely into the parser.

## Costs

- There are two trees and one normative transformation.
- Error recovery must preserve text.
- Grammar changes require updating several artefacts.
- Even a minimal implementation needs more initial infrastructure.

## Rejected alternatives

### AST only

Rejected because it would lose comments, spacing, punctuation and concrete forms needed by tooling.

### CST only

Rejected because resolution, types and semantics would have to interpret punctuation and sugar continuously.

### Comments inside the executable AST

Rejected because comments do not alter programme meaning and would create false dependencies. Future structured documentation will have a separate model.

### Resolving callable calls in the parser

Rejected because `action-call-effect ::= postfix-expression` requires resolving names and signatures to determine whether the effect is really a callable call. D-096 removes the former elementary/compound classification: what is deferred is call resolution, not an action class.

## Derived changes

- `06-lexico.md` must distinguish complete and significant streams.
- `07-gramatica-concreta.md` must state that parsing produces a CST.
- `08-sintaxis-abstracta.md` replaces the planned skeleton.
- READMEs must incorporate the new phase chain.
- The numeric representation of magnitudes uses declared type syntax and is statically validated as numeric.
