# Nominal resolution from the MUD

This directory contains the contract regulatory mechanism for the name resolution. Add [[../09-nombres-y-anclas|09. Names, paths and anchors]] and does not define a type or semantics dynamics.

## `mud-nominal-hir.asdl`

It is the regulatory solution to nominal resolution on the Surface AST. It preserves symbols, scopes, bindings, anchors and nominal relationships `Owns`, `Specializes` y `RefersTo`.

It must not contain effective types, effective domains, inferred cardinalities, narrowing, elaborate conversions, effects, semantic dependencies or evidence of termination. These conclusions relate to later stages that have not yet been formalised in technical terms.

The Nominal HIR It is derived and reconstructible: it does not constitute a source semantics independent.

