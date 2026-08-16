from pathlib import Path

path = Path('tooling/markdown_export/profiles.toml')
text = path.read_text(encoding='utf-8')
for question in (
    'notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos.md',
    'notas/preguntas/Q-055-literales-de-magnitudes-de-punto.md',
):
    line = f'    "{question}",\n'
    count = text.count(line)
    if count != 2:
        raise SystemExit(f'expected {question} excluded in language/current exactly twice, got {count}')
    text = text.replace(line, '')
path.write_text(text, encoding='utf-8', newline='\n')
print('PHASE1_PROFILES_OK')
