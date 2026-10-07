# MUD prescriptive grammars

This directory contains the MUD 1.0 reference grammars:

- `mud-lexico.ebnf`: conversion of Unicode source text into meaningful tokens and lexical forms.
- `mud.ebnf`: conversion of significant tokens into concrete syntax.
- `validate_grammar.py`: editorial checks of production uniqueness, references and reachability.
- `ebnf_analysis.py`: EBNF structure, nullability and left-corner analysis, plus BNF lowering and token-fixture recognition for regression tests. It is not a complete Mud scanner or source parser.

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
- Concrete: `mud-input`, selecting `mud-file` or `part-file` by physical filename.

## Products

`mud-lexico.ebnf` does not mean that an implementation must ignore comments or spaces. [[../07-lexicon]] defines a complete workflow using trivia and a significant grammar insight.

`mud.ebnf` is produced from the artefacts listed in:

- `../syntax/mud-syntax-kinds.yaml`.
- `../syntax/cst-lossless.md`.

Abstract projection is defined by:

- `../09-abstract-syntax.md`.
- `../syntax/mud-surface-ast.asdl`.
- `../syntax/cst-to-surface-ast.md`.

## Modal scanner

`Text` templates require nested modes. `mud-lexico.ebnf` maintains the inventory of special forms; [[../07-lexicon]] defines the algorithm; `mud.ebnf` analyses tokens emitted within interpolations.

The ways of unit and from magnitude from point are also context-dependent. The fact that there is a token contextual does not anticipate its resolution semantics.

`from` adds native-language delegation: `FOREIGN_STATEMENT` and `FOREIGN_EXPRESSION` are contextual, lossless regions classified by the selected adapter. The MUD parser owns bridge names/types and body cardinality; it does not lex native source with ordinary MUD rules.

`HEADER_WITH` is the contextual view of an ungrouped `with` in a declaration's ancestor/parameter portion, as defined in [[../07-lexicon#Generic header boundary]]. Only parameter groups consume that terminal; explicit applications consume ordinary `with`. Classification preserves the base token and does not require type lookup.

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

The joint validator also uses `ebnf_analysis.py` to reject left-recursive paths through generic argument/application entry points, including their stored-annotation counterparts. This is a targeted structural guarantee, not a claim that the whole grammar is LL/LR-unambiguous. `../syntax/test_generic_grammar.py` checks accepted and rejected token fixtures for application forms and header boundaries.

## Policy exchange

Any structural alteration to a production You must update this in the same commit:

1. The EBNF.
2. The explanation from [[../08-concrete-grammar]].
3. `mud-syntax-kinds.yaml`.
4. `syntax-coverage.yaml`.
5. The CST → AST transformation, where applicable.
6. The ASDL when an abstract distinction changes.
7. The affected border cases.

Implementations may use any scanning or parsing technique provided they produce the same observable CST, the same rejections and the same Surface AST standardised.


The concrete grammar inventory starts at `mud-input`; filenames select `.mud` → `mud-file` and `mud.part` → `part-file`. Manifests contain only exact `uses` statements and layout. Source header placement is validated against retained trivia under [[../05-source-text]].
