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
def replace_case(text, case_id, replacement):
    start_marker = f'- id: {case_id}\n'
    start = text.find(start_marker)
    if start < 0:
        raise SystemExit(f'case not found: {case_id}')
    next_start = text.find('\n- id: ', start + len(start_marker))
    end = len(text) if next_start < 0 else next_start + 1
    return text[:start] + replacement.rstrip('\n') + '\n' + text[end:]

# This is an incremental hardening pass. The semantic contract from stage 4
# must already exist; do not reapply D-032/08/IR edits.
for rel, needle in [
    ('notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal.md', 'ContextualAliasConstructionExpr'),
    ('especificacion/08-sintaxis-abstracta.md', 'ContextualAliasConstructionExpr(literal, target_alias)'),
    ('especificacion/ir/mud-semantic-ir.asdl', 'ContextualAliasConstructionExpr('),
]:
    if needle not in read(rel):
        raise SystemExit(f'missing accepted stage-4 contract: {needle} in {rel}')

# Replace the two typed-expression cases with a form that isolates the alias
# conversion rule from sibling-field initialization semantics.
rel = 'especificacion/sintaxis/casos/cst-ast.yaml'
t = read(rel)
t = replace_case(t, 'typed-representation-does-not-implicitly-become-alias', r'''- id: typed-representation-does-not-implicitly-become-alias
  category: validation-after-resolution
  source: "alias PlayerName := Text\nthing Person {\n    mut name: PlayerName = \"Ada\"\n}\naction Rename for mut person: Person given rawName: Text {\n    then person.name = rawName\n}\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - explicit-nominal-conversion-required
  semantic_expectations:
  - typed-Text-expression-is-not-a-contextual-literal
  produces_ast: true''')
t = replace_case(t, 'explicit-representation-to-alias', r'''- id: explicit-representation-to-alias
  category: validation-after-resolution
  source: "alias PlayerName := Text\nthing Person {\n    mut name: PlayerName = \"Ada\"\n}\naction Rename for mut person: Person given rawName: Text {\n    then person.name = rawName to PlayerName\n}\n"
  cst_root: MudFileSyntax
  semantic_expectations:
  - semantic-ir-uses-explicit-conversion
  produces_ast: true''')

# D-032 also requires bidirectional comparison propagation for literals.
if '- id: contextual-alias-comparison-literal\n' not in t:
    t = t.rstrip() + r'''

- id: contextual-alias-comparison-literal
  category: validation-after-resolution
  source: "alias PlayerName := Text\nthing Person {\n    name: PlayerName = \"Ada\"\n}\nrule IsAda for person: Person {\n    person.name == \"Ada\"\n}\n"
  cst_root: MudFileSyntax
  semantic_expectations:
  - alias-operand-propagates-expected-type-to-literal
  - comparison-literal-uses-contextual-alias-construction
  - both-operands-have-exact-PlayerName-type-after-elaboration
  produces_ast: true
'''
write(rel, t)

# Permanent regression guards so later edits cannot silently erase the
# elaborated distinction or its conformance cases.
rel = 'especificacion/sintaxis/validate_syntax_model.py'
t = read(rel)
if '"ContextualAliasConstructionExpr(",' not in t:
    t = exact(t,
        '''        root / "especificacion/ir/mud-semantic-ir.asdl": [\n            "ExactNominalTypeTestExpr(",\n            "ExactDictionarySetOperationExpr(",\n            "FunctionalDictionarySetOperationExpr(",\n        ],''',
        '''        root / "especificacion/ir/mud-semantic-ir.asdl": [\n            "ExactNominalTypeTestExpr(",\n            "ExactDictionarySetOperationExpr(",\n            "FunctionalDictionarySetOperationExpr(",\n            "ContextualAliasConstructionExpr(",\n        ],''',
        'validator required IR fragment')
for case_id in [
    'contextual-basic-alias-literal',
    'contextual-alias-comparison-literal',
    'typed-representation-does-not-implicitly-become-alias',
    'explicit-representation-to-alias',
]:
    quoted = f'        "{case_id}",\n'
    if quoted not in t:
        t = exact(t,
            '        "metadata-file-assignment-rejected",\n',
            '        "metadata-file-assignment-rejected",\n' + quoted,
            f'validator case {case_id}')
write(rel, t)

print('STAGE4B_OK')
