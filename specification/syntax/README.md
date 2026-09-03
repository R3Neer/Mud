# MUD syntactic models

This directory contains the standardised and verifiable artefacts that link the concrete grammar with the Surface AST.

## Artefacts

| Archive | State | Function |
|---|---|---|
| `lossless-cst.md` | Normative | Model of CST, trivia, spans and recovery. |
| `mud-syntax-kinds.yaml` | Mechanical regulations | List of productions, tokens, trivia and CST categories. |
| `mud-surface-ast.asdl` | Mechanical regulations | Outline of the Surface AST standardised. |
| `cst-to-surface-ast.md` | Normative | Transformation and standardisation. |
| `syntax-coverage.yaml` | Mechanical normative | Comprehensive EBNF → CST → AST mapping. |
| `validate_syntax_model.py` | Publishing tool | Detects discrepancies between the previous artefacts. |
| `cases/cst-ast.yaml` | Starter suite | Transformation and pre-AST rejection cases. |

## Order of authority

The files complement one another; there is no general rule that ‘the latest one takes precedence’.

1. `mud-lexicon.ebnf` and `06-lexicon.md` determine lexical recognition.
2. `mud.ebnf` and `07-concrete-grammar.md` determine concrete grouping.
3. `lossless-cst.md` determines preservation, trivia and recovery.
4. `mud-surface-ast.asdl` defines the abstract constructors.
5. `cst-to-surface-ast.md` determines the projection.
6. YAML files make it possible to list and verify the correspondence.

A contradiction is a fault in the proposal and must be resolved in all the files concerned.

## Flow

```text
archivo .mud
→ scanner completo
→ tokens significativos + trivia
→ lossless CST
→ contextual syntactic validation
→ normalised Surface AST
→ nominal resolution: symbols + bindings + partial graph
→ typing/elaboration
→ later semantic representation not yet formalised
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

## Validation

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

## Change policy

A change to the grammar must be updated, in the same commit:

1. The EBNF affected.
2. The CST catalogue.
3. The coverage.
4. The transformation when the standardisation changes.
5. The ASDL when an abstract distinction appears or disappears.
6. Relevant test cases.

An internal change that does not affect observable behaviour may modify an implementation without changing these files.

## Naming conventions

- EBNF production: `kebab-case`.
- CST category: `PascalCaseSyntax`.
- Tipo ASDL: `snake_case`.
- Builder ASDL: `PascalCase`.
- Campo ASDL: `snake_case`.
- Conceptual flag: `Disabled | Enabled`.

## Limits

This directory does not define:

- Name resolution and anchors.
- Subtyping.
- Inference of types.
- Static analysis.
- Effect semantics.
- Causal waves.
- Mechanical representation following typing and elaboration, which has not yet been formalised.

References to these phases serve solely to prevent the Surface AST anticipate them.

