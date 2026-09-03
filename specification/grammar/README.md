# MUD prescriptive grammars

This directory contains the MUD 1.0 reference grammars:

- `mud-lexicon.ebnf`: conversion of Unicode source text into meaningful tokens and lexical forms.
- `mud.ebnf`: conversion of significant tokens into concrete syntax.

Lossless representation, the CST node catalogue and the Surface AST are documented in [[../syntax/README|syntax/]].

Both use this dialect EBNF:

```text
rule        ::= expression ;
alternative ::= a | b ;
optional    ::= [ a ] ;
repetition  ::= { a } ;
group       ::= ( a | b ) ;
terminal    ::= "exact text" ;
special     ::= ? condition defined in prose ? ;
```

The normative details of the dialect can be found in [[../03-notation]].

Symbol initial:

- Glossary: `mud-source`.
- Concrete: `mud-file`.

## Products

`mud-lexicon.ebnf` does not mean that an implementation must ignore comments or spaces. [[../06-lexicon]] defines a complete workflow using trivia and a significant grammar insight.

`mud.ebnf` is produced from the artefacts listed in:

- `../syntax/mud-syntax-kinds.yaml`.
- `../syntax/lossless-cst.md`.

Abstract projection is defined by:

- `../08-abstract-syntax.md`.
- `../syntax/mud-surface-ast.asdl`.
- `../syntax/cst-to-surface-ast.md`.

## Modal scanner

`Text` templates require nested modes. `mud-lexicon.ebnf` maintains the inventory of special forms; [[../06-lexicon]] defines the algorithm; `mud.ebnf` analyses tokens emitted within interpolations.

The ways of unit and from magnitude from point are also context-dependent. The fact that there is a token contextual does not anticipate its resolution semantics.

## Separation of responsibilities

The EBNF distinguishes between recognition of elaboration. It does not attempt to check:

- Existence of names.
- Compatibility of types.
- Record of statements.
- Validity of domains.
- Resolution of potential calls to `action` or `subaction` and verification of external root capability.
- Selection of receiver multiple.

The specific restrictions that are not clearly set out in EBNF are validated after the CST and before the AST.

Validation editorial:

```powershell
python specification/grammar/validate_grammar.py
```

The check detects duplicate, undefined or unachievable outputs. It does not replace future tests of conformance of the parser.

Joint checking of grammar, CST and AST:

```powershell
python specification/syntax/validate_syntax_model.py
```

The first check identifies duplicate, undefined or unachievable production targets. The second checks CST stock levels, coverage and destinations ASDL. None of them replace the tests for conformance of a parser.

## Policy exchange

Any structural alteration to a production You must update this in the same commit:

1. The EBNF.
2. The explanation from [[../07-concrete-grammar]].
3. `mud-syntax-kinds.yaml`.
4. `syntax-coverage.yaml`.
5. The CST → AST transformation, where applicable.
6. The ASDL when an abstract distinction changes.
7. The affected border cases.

Implementations may use any scanning or parsing technique provided they produce the same observable CST, the same rejections and the same Surface AST standardised.

