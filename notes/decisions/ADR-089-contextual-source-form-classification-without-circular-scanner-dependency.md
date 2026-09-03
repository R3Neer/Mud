---
id: D-089
title: "Contextual classification of source forms without circular scanner dependency"
status: current
date: 2026-08-16
supersedes: []
superseded-by: []
questions:
  - "Q-054"
  - "Q-055"
affects:
  - "scanner, unit forms, point-magnitude literals, CST, parser, contextual elaboration and conformance"
---
# ADR-089 — Contextual classification of source forms without circular scanner dependency

- Modifies: [[ADR-062-canonical-point-magnitude-literals|D-062]] and [[ADR-076-named-units-prefixes-and-adjacent-notation|D-076]].
- Closes: [[notes/questions/Q-054-c-catalogue-and-lexical-resolution-of-units-and-prefixes|Q-054]] and [[notes/questions/Q-055-l-point-magnitude-literals|Q-055]].

## Context

D-062 and D-076 allow information declared by the program itself to participate in source forms: `~format` defines the canonical spelling of a point magnitude, and units admit an identifier, name, plural, abbreviation and prefixed forms. The initial scanner cannot depend on those declarations without introducing a cycle between tokenisation, parsing and resolution.

## Decision

### Base scanner and contextual classifier

The base scanner depends exclusively on Unicode, trivia and MUD's fixed lexical catalogue. It produces a lossless stream with source offsets, but **does not** consult `magnitude` declarations, unit catalogues, `~format` or expected types.

`POINT_LITERAL` and `UNIT_FORM` are contextual tokens, not base-scanner productions. A contextual classifier may add a tokenisation alternative over an exact source-text interval when resolution and the expected type provide the required information. The alternative retains the same `source_span`; it does not reconstruct the spelling by concatenating base tokens.

An implementation may represent this boundary as a token lattice, local re-tokenisation, deferred parsing or an equivalent strategy. It conforms if the base scanner is model-independent and contextual classification produces exactly the same spans and observable results.

### Point literals

When an expression position has a single expected type that is a `point over` magnitude with `~format`, the classifier attempts to consume a complete canonical representation of that format from the source offset. If it matches exactly and invertibly, it produces a `POINT_LITERAL` covering the whole recognised span, even if the same text could be decomposed into several base tokens or form an ordinary expression.

In that context, the `POINT_LITERAL` interpretation takes priority over the base-tokenisation route for the same span. Without a single expected type, that contextual alternative is not created. The match must end exactly where the canonical representation ends; it cannot accept a prefix of a longer form that the same format could consume.

D-062's invertibility requirement therefore includes deterministic delimitation of the complete representation. A `~format` that does not allow the end of its own canonical form to be recognised unambiguously is invalid for a point magnitude.

### Unit forms

Unit forms are classified after the semantic magnitude and unit catalogue is known. The classifier consults source text directly from a position where the quantity grammar admits a unit. It may produce `UNIT_FORM` for the declared identifier, an admissible `~name`, `~plural` or `~abbreviation`, or an enabled prefixed form.

The declared identifier retains the ordinary lexical rules for a unit identifier. The three configurable values `~name`, `~plural` and `~abbreviation`, however, share the same criterion when used as source forms: they may contain U+0020 spaces and punctuation, but must contain at least one alphabetic character; consequently they cannot consist entirely of digits or entirely of non-alphabetic characters. A complete form that exactly matches a MUD keyword is invalid as a source form. These restrictions affect syntactic use and do not prevent retaining the same value for presentation when it is not admissible as a source form.

Validation is performed over the closure of enabled forms for each magnitude, including all combinations with permitted prefixes. Two distinct units of the same magnitude cannot produce the same source form, either directly or after applying a prefix. A collision within a magnitude is a static declaration error and is not deferred to the use site. Between distinct magnitudes, the contextual disambiguation described below continues to apply.

When an expected type or magnitude exists, only forms compatible with it compete. Without an expected type, a form is valid only if the resolved catalogue determines a unit uniquely. Two distinct semantic candidates with the same visible form across different magnitudes are ambiguous unless qualified as permitted by the grammar.

If several compatible forms share a prefix, the longest complete canonical match is selected. Two distinct candidates consuming exactly the same span remain ambiguous; declaration order does not break the tie. Contextual classification may cover several base tokens and does not grant that sequence new lexical meaning outside a unit position.

The adjacency `3m` is resolved at the same offset immediately following the number. The presence or absence of trivia before a unit does not change the selected unit; the formatter retains D-076's canonical normalisation.

### CST and AST

The lossless CST retains the base tokens and enough source span to reproduce contextual classification. An implementation may materialise the contextual token in a derived view, but never loses the original characters. The Surface AST retains `PointLiteral(source_form)` and already-classified unit forms; it contains no dependency on the base scanner's catalogue.

## Consequences

- The initial scanner no longer consults future semantic information.
- `~format` continues to define a direct literal source form, without an additional mandatory delimiter.
- Collisions between a contextual form and an ordinary expression are resolved by semantic context, not by global scanner priority.
- Units may retain Unicode or configured forms without turning them into general identifiers.
- The implementation may be multi-pass, but base tokenisation remains reproducible from isolated text.

## Verification

1. The base scanner produces the same stream before and after resolving magnitude declarations.
2. `07:05:00` is classified as a single `POINT_LITERAL` when the expected type selects its magnitude.
3. The same sequence without a single expected type receives no point classification.
4. A format colliding with an ordinary expression wins only under the expected point type.
5. A format whose end cannot be recognised unambiguously is rejected.
6. A unique unit form resolves without an expected type, while a collision requires context or qualification.
7. Prefix-based unit matches use the longest complete form without depending on declaration order.
8. `3m` and `3 m` classify the same unit and the formatter produces the canonical spaced form.
9. `~name`, `~plural` and `~abbreviation` accept spaces, but an entirely numeric or non-alphabetic source form is rejected.
10. A source form identical to a MUD keyword is rejected.
11. Collisions between units of the same magnitude are also detected after expanding all enabled prefixes.
12. CST and round-trip preserve exactly the source text preceding contextual classification.
