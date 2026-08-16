from pathlib import Path

p = Path('especificacion/sintaxis/validate_syntax_model.py')
text = p.read_text(encoding='utf-8')
old = '''        root / "especificacion/sintaxis/mud-resolved-ast.asdl": [
            "ExactNominalTypeTestExpr(",
            "ExactDictionarySetOperationExpr(",
            "FunctionalDictionarySetOperationExpr(",
        ],
'''
new = '''        root / "especificacion/sintaxis/mud-elaborated-ast.asdl": [
            "ExactNominalTypeTestExpr(",
            "ExactDictionarySetOperationExpr(",
            "FunctionalDictionarySetOperationExpr(",
        ],
'''
if old not in text:
    raise SystemExit('D-086 required-fragments block not found')
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8', newline='\n')
print('PHASE6_VALIDATOR_BOUNDARY_OK')
