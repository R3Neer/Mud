from pathlib import Path

p = Path('especificacion/sintaxis/mud-syntax-kinds.yaml')
text = p.read_text(encoding='utf-8')
start = text.index('  given-declaration:\n')
end = text.index('  boolean-rule-declaration:\n', start)
replacement = '''  given-declaration:
    kind: GivenDeclarationSyntax
    rhs: 'given-name , { "," , given-name } , ":" , type-expression , [ "=" , constant-expression ]\\n        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]'
    references:
    - given-name
    - type-expression
    - constant-expression
    - declaration-layout
    - metadata-assignment
    - required-separation
'''
text = text[:start] + replacement + text[end:]
p.write_text(text, encoding='utf-8', newline='\n')
print('PHASE4B_SYNTAX_KINDS_OK')
