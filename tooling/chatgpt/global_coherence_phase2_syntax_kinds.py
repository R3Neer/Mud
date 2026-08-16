from pathlib import Path

p = Path('especificacion/sintaxis/mud-syntax-kinds.yaml')
text = p.read_text(encoding='utf-8')
for line in ('      | point-form\n', '      | unit-form\n', '    - point-form\n', '    - unit-form\n'):
    if line not in text:
        raise SystemExit(f'missing syntax-kinds line: {line!r}')
    text = text.replace(line, '', 1)
for block in (
    "  unit-form:\n    rhs: '? forma Unicode de unidad habilitada por una declaración magnitude ?'\n    references: []\n",
    "  point-form:\n    rhs: '? forma canónica contextual de D-062 para el tipo de punto esperado ?'\n    references: []\n",
):
    if block not in text:
        raise SystemExit(f'missing syntax-kinds block: {block!r}')
    text = text.replace(block, '', 1)
p.write_text(text, encoding='utf-8', newline='\n')
print('PHASE2_SYNTAX_KINDS_OK')
