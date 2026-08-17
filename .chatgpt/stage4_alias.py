from pathlib import Path
import os

ROOT = Path(os.environ['MUD_TARGET']).resolve()

def read(rel): return (ROOT / rel).read_text(encoding='utf-8')
def write(rel, text): (ROOT / rel).write_text(text.rstrip('\n') + '\n', encoding='utf-8', newline='\n')
def exact(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1, found {n}')
    return text.replace(old, new, 1)

# D-032: modern phase terminology and explicit IR distinction.
rel = 'notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal.md'
t = read(rel)
t = exact(t,
          '- El AST tipado conserva el alias nominal incluso cuando su representación coincide con otro tipo.',
          '- El IR semántico conserva explícitamente la construcción contextual y el alias nominal incluso cuando su representación coincide con otro tipo.',
          'D032 consequence')
if 'ContextualAliasConstructionExpr' not in t:
    t = exact(t,
              '- La elaboración debe distinguir literales sin tipo fijado de expresiones ya tipadas.',
              '- La elaboración debe distinguir literales sin tipo fijado de expresiones ya tipadas.\n- El IR usa `ContextualAliasConstructionExpr` para la construcción dirigida por tipo esperado y reserva `ConversionExpr` para un `to` explícito.',
              'D032 IR consequence')
write(rel, t)

# 08: promote D-032 into the current normative boundary.
rel = 'especificacion/08-sintaxis-abstracta.md'
t = read(rel)
if '  - D-032\n' not in t:
    t = exact(t, 'decisions:\n', 'decisions:\n  - D-032\n', '08 frontmatter D032')
needle = '''Los literales estructurales siguen siendo contextuales. `PositionalStructuralLiteralExpr` exige al menos dos valores y `NamedStructuralLiteralExpr` conserva uno o más componentes nombrados; no se selecciona todavía un alias concreto. Por tanto, los miembros del alias solo quedan disponibles después de elaboración contextual o de una conversión nominal explícita.\n'''
replacement = needle + '''\n### Construcción contextual de aliases\n\nD-032 distingue un literal todavía construible de una expresión que ya posee tipo. Cuando el contexto exige exactamente un alias nominal estructuralmente compatible, un literal básico o estructural puede construirse directamente como valor de ese alias sin escribir `to`. Esto se aplica a inicializadores, argumentos o `given`, claves con tipo esperado y al literal opuesto de una comparación cuyo otro operando ya determina el alias nominal.\n\nLa regla **solo construye literales**. Una variable, acceso, llamada u otra expresión que ya tenga tipo efectivo conserva ese tipo y no se convierte implícitamente al alias, aunque su representación sea estructuralmente compatible; necesita una conversión nominal explícita mediante `to`. Dos aliases nominales distintos tampoco se coercionan entre sí.\n\nEl AST superficial conserva el literal sin seleccionar alias. Tras resolver el tipo esperado, la elaboración emite `ContextualAliasConstructionExpr(literal, target_alias)` en el IR semántico. Una conversión escrita con `to` continúa elaborándose como `ConversionExpr`, de modo que el IR distingue construcción contextual de conversión explícita.\n\nLos miembros de un alias estructural solo quedan disponibles después de esa construcción contextual o de una conversión nominal explícita; el nombre de un miembro no se usa para buscar candidatos de alias.\n'''
t = exact(t, needle, replacement, '08 contextual alias section')
write(rel, t)

# Semantic IR preserves the elaborated distinction.
rel = 'especificacion/ir/mud-semantic-ir.asdl'
t = read(rel)
t = exact(t,
          '                  | ConversionExpr(semantic_expr value, anchor target_type)\n',
          '                  | ContextualAliasConstructionExpr(semantic_expr literal, anchor target_alias)\n                  | ConversionExpr(semantic_expr value, anchor target_type)\n',
          'semantic IR contextual alias')
write(rel, t)

# Conformance cases: direct construction, comparison propagation, explicit conversion and rejection of typed implicit conversion.
rel = 'especificacion/sintaxis/casos/cst-ast.yaml'
t = read(rel)
if 'id: contextual-basic-alias-literal' not in t:
    t += r'''
- id: contextual-basic-alias-literal
  category: validation-after-resolution
  source: "alias PlayerName := Text\nthing Person {\n    name: PlayerName = \"Ada\"\n}\n"
  cst_root: MudFileSyntax
  semantic_expectations:
  - elaborate-basic-literal-as-expected-nominal-alias
  - semantic-ir-uses-contextual-alias-construction
  produces_ast: true
- id: contextual-alias-comparison-literal
  category: validation-after-resolution
  source: "alias PlayerName := Text\nthing Person {\n    name: PlayerName = \"Ada\"\n}\nrule IsAda for person: Person {\n    person.name == \"Ada\"\n}\n"
  cst_root: MudFileSyntax
  semantic_expectations:
  - alias-operand-propagates-expected-type-to-literal
  - comparison-literal-uses-contextual-alias-construction
  - both-operands-have-exact-PlayerName-type-after-elaboration
  produces_ast: true
- id: typed-representation-does-not-implicitly-become-alias
  category: validation-after-resolution
  source: "alias PlayerName := Text\nthing Person {\n    mut name: PlayerName = \"Ada\"\n}\naction Rename for mut person: Person given rawName: Text {\n    then person.name = rawName\n}\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - explicit-nominal-conversion-required
  semantic_expectations:
  - typed-Text-expression-is-not-a-contextual-literal
  produces_ast: true
- id: explicit-representation-to-alias
  category: validation-after-resolution
  source: "alias PlayerName := Text\nthing Person {\n    mut name: PlayerName = \"Ada\"\n}\naction Rename for mut person: Person given rawName: Text {\n    then person.name = rawName to PlayerName\n}\n"
  cst_root: MudFileSyntax
  semantic_expectations:
  - semantic-ir-uses-explicit-conversion
  produces_ast: true
'''
write(rel, t)

# Permanent regression guard.
rel = 'especificacion/sintaxis/validate_syntax_model.py'
t = read(rel)
needle = '''        root / "especificacion/ir/mud-semantic-ir.asdl": [\n            "ExactNominalTypeTestExpr(",\n            "ExactDictionarySetOperationExpr(",\n            "FunctionalDictionarySetOperationExpr(",\n        ],'''
replacement = '''        root / "especificacion/ir/mud-semantic-ir.asdl": [\n            "ExactNominalTypeTestExpr(",\n            "ExactDictionarySetOperationExpr(",\n            "FunctionalDictionarySetOperationExpr(",\n            "ContextualAliasConstructionExpr(",\n        ],'''
t = exact(t, needle, replacement, 'validator required IR fragment')
needle = '''        "metadata-file-assignment-rejected",\n        "iis-negation-equivalence",'''
replacement = '''        "metadata-file-assignment-rejected",\n        "contextual-basic-alias-literal",\n        "contextual-alias-comparison-literal",\n        "typed-representation-does-not-implicitly-become-alias",\n        "explicit-representation-to-alias",\n        "iis-negation-equivalence",'''
t = exact(t, needle, replacement, 'validator required alias cases')
write(rel, t)

print('STAGE4_OK')
