# Syntactic models of MUD

This directory contains the standardised and verifiable artefacts that link the concrete grammar with the Surface AST.

## Archives

| Archive | State | Function |
|---|---|---|
| `cst-sin-perdidas.md` | Regulations | Model from CST, trivia, spans and recovery. |
| `mud-syntax-kinds.yaml` | Mechanical regulations | List of productions, tokens, trivia and CST categories. |
| `mud-surface-ast.asdl` | Mechanical regulations | Outline of the Surface AST standardised. |
| `cst-a-ast-superficial.md` | Regulations | Transformation and standardisation. |
| `cobertura-sintactica.yaml` | Mechanical regulations | Comprehensive mapping EBNF → CST → AST. |
| `validate_syntax_model.py` | Publishing tool | Detects discrepancies between the previous artefacts. |
| `casos/cst-ast.yaml` | Starter Suite | Cases of transformation and rejection prior to AST. |

## Order of authority

The files complement one another; there is no general rule that ‘the latest one takes precedence’.

1. `mud-lexico.ebnf` y `06-lexicon.md` determine lexical recognition.
2. `mud.ebnf` y `07-concrete-grammar.md` determine the specific grouping.
3. `cst-sin-perdidas.md` determines conservation, trivia and recovery.
4. `mud-surface-ast.asdl` defines the abstract constructors.
5. `cst-a-ast-superficial.md` determines the projection.
6. YAML files make it possible to list and verify the correspondence.

A contradiction is a fault in the proposal and must be resolved in all the files concerned.

## Flow

```text
archivo .mud
→ scanner completo
→ tokens significativos + trivia
→ CST sin pérdidas
→ validación sintáctica contextual
→ AST superficial normalizado
→ resolución nominal: símbolos + bindings + grafo parcial
→ tipado/elaboración
→ representación semántica posterior todavía no formalizada
```

## Code generation

`mud-surface-ast.asdl` can power generators from:

- Classes or structs.
- Visitors.
- Serialisers.
- Structural comparators.
- Validated builders.

`mud-syntax-kinds.yaml` can power:

- Lists of `SyntaxKind`.
- Typed wrappers for CST nodes.
- Parser coverage tests.
- Production documentation.

Generation must not convert mechanical files into derivatives without authority. The generated files will be saved outside `specification/` or they will be expressly marked as such.

## Validación

Validator dependency:

```powershell
python -m pip install -r specification/syntax/requirements.txt
```

From the root from the repository:

```bash
python specification/syntax/validate_syntax_model.py
```

The command checks:

- Coverage of all syntactic constructions.
- An inventory of all lexical productions.
- No orphaned entries.
- Correlation between CST categories and coverage.
- Availability of destinations ASDL as stated.
- Existence of standard contracts under the scheme.

Not yet verified:

- Ambiguity LL/LR.
- Semantics static.
- Correcting MUD examples using a real parser.
- Dynamic properties.

## Policy of changes

A change to the grammar must be updated, in the same commit:

1. The EBNF affected.
2. The CST catalogue.
3. The coverage.
4. The transformation when the standardisation changes.
5. The ASDL when an abstract distinction appears or disappears.
6. Relevant test cases.

An internal change that does not affect observable behaviour You can modify an implementation without changing these files.

## Naming conventions

- Producción EBNF: `kebab-case`.
- CST category: `PascalCaseSyntax`.
- Tipo ASDL: `snake_case`.
- Builder ASDL: `PascalCase`.
- Campo ASDL: `snake_case`.
- Conceptual flag: `Disabled | Enabled`.

## Limits

This directory does not define:

- Name resolution and anchors.
- Subtyped.
- Inference of types.
- Static assessment.
- Semantics effects.
- Causal waves.
- Mechanical representation following typing and elaboration, which has not yet been formalised.

References to these phases serve solely to prevent the Surface AST anticipate them.

