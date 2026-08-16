from pathlib import Path


def patch(path: str, replacements: list[tuple[str, str]]) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    for old, new in replacements:
        if old not in text:
            raise SystemExit(f'{path}: missing review text {old!r}')
        text = text.replace(old, new, 1)
    p.write_text(text, encoding='utf-8', newline='\n')

patch('especificacion/06-lexico.md', [
    ('El lexer representa una coincidencia válida como `POINT_LITERAL`.',
     'El clasificador contextual representa una coincidencia válida como `POINT_LITERAL`; el scanner base conserva su tokenización ordinaria.'),
    ('Si declara `format`, el texto debe coincidir exactamente',
     'Si declara `~format`, el texto debe coincidir exactamente'),
    ('Una magnitud de punto sin `format` usa una cantidad ordinaria',
     'Una magnitud de punto sin `~format` usa una cantidad ordinaria'),
])
patch('notas/decisiones/ADR-062-literales-canonicos-de-magnitudes-de-punto.md', [
    ('La propiedad `format` ya determina cómo se representa una magnitud de punto.',
     'El metadato `~format` ya determina cómo se representa una magnitud de punto.'),
    ('Un `format` de punto debe ser estáticamente invertible:',
     'Un `~format` de punto debe ser estáticamente invertible:'),
    ('dentro del `format` de una magnitud de punto',
     'dentro del `~format` de una magnitud de punto'),
    ('- `format` es simultáneamente la representación canónica y, cuando existe, la forma fuente del tipo de punto.',
     '- `~format` es simultáneamente la representación canónica y, cuando existe, la forma fuente del tipo de punto.'),
])
print('PHASE2_HUMAN_REVIEW_FIX_OK')
