from pathlib import Path

p = Path('especificacion/sintaxis/mud-syntax-kinds.yaml')
text = p.read_text(encoding='utf-8')
start = text.index('  stored-family-data-declaration:\n')
end = text.index('  family-member:\n', start)
replacement = '''  stored-family-data-declaration:
    kind: StoredFamilyDataDeclarationSyntax
    rhs: 'field-name , ":" , type-expression\\n        , [ "=" , constant-expression ]\\n        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]'
    references:
    - field-name
    - type-expression
    - constant-expression
    - declaration-layout
    - metadata-assignment
    - required-separation
  calculated-family-data-declaration:
    kind: CalculatedFamilyDataDeclarationSyntax
    rhs: 'field-name , [ derived-value-shape ] , ":=" , value-expression\\n        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]'
    references:
    - field-name
    - derived-value-shape
    - value-expression
    - declaration-layout
    - metadata-assignment
    - required-separation
'''
text = text[:start] + replacement + text[end:]
p.write_text(text, encoding='utf-8', newline='\n')
print('PHASE3B_SYNTAX_KINDS_OK')
