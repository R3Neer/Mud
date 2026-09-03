# MUD prescriptive grammars

This directory contains the MUD 1.0 reference grammars:

- `mud-lexico.ebnf`: conversion of Unicode source text into meaningful tokens and lexical forms.
- `mud.ebnf`: conversion of significant tokens into concrete syntax.

Lossless representation, the CST node catalogue and the Surface AST are documented in [[../sintaxis/README|syntax/]].

Both use this dialect EBNF:

```text
regla       ::= expresión ;
alternativa ::= a | b ;
opcional    ::= [ a ] ;
repetición  ::= { a } ;
grupo       ::= ( a | b ) ;
terminal    ::= "texto exacto" ;
especial    ::= ? condición definida en prosa ? ;
```

The normative details of the dialect can be found in [[../03-notacion]].

Symbol initial:

- Glossary: `mud-source`.
- Concrete: `mud-file`.

## Products

`mud-lexico.ebnf` This does not mean that an implementation must ignore comments or spaces. [[../06-lexico]] define a complete workflow using trivia and an important insight into grammar.

`mud.ebnf` is produced by the group listed in:

- `../sintaxis/mud-syntax-kinds.yaml`.
- `../sintaxis/cst-sin-perdidas.md`.

Abstract projection is defined as:

- `../08-sintaxis-abstracta.md`.
- `../sintaxis/mud-surface-ast.asdl`.
- `../sintaxis/cst-a-ast-superficial.md`.

## Modal scanner

The templates `Text` require nested modes. `mud-lexico.ebnf` maintains the inventory of special forms; [[../06-lexico]] define the algorithm; `mud.ebnf` analyses the tokens issued within interpolations.

The ways of unit and from magnitude from point are also context-dependent. The fact that there is a token contextual does not anticipate its resolution semantics.

## Separation of responsibilities

The EBNF distinguishes between recognition of elaboration. It does not attempt to check:

- Existence of names.
- Compatibility of types.
- Record of statements.
- Validity of domains.
- Resolution from potential calls to `action` o `subaction` and verification of the capacity of root outdoors.
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
2. The explanation from [[../07-gramatica-concreta]].
3. `mud-syntax-kinds.yaml`.
4. `cobertura-sintactica.yaml`.
5. The CST → AST transformation, where applicable.
6. The ASDL when an abstract distinction changes.
7. The affected border cases.

Implementations may use any scanning or parsing technique provided they produce the same observable CST, the same rejections and the same Surface AST standardised.

