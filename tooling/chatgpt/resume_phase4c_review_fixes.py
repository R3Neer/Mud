from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')

# Restore editorial separation after the canonical relation line.
replace_once(
    'notas/decisiones/ADR-093-extremos-vacios-como-ausencia-tipada.md',
    '- Modifica: [[ADR-047-cuantificadores-e-iteracion-finita|D-047]].\n## Contexto',
    '- Modifica: [[ADR-047-cuantificadores-e-iteracion-finita|D-047]].\n\n## Contexto',
)

# Exact cardinality follows what static analysis can prove: 0, optional, or 1.
replace_once(
    'notas/decisiones/ADR-093-extremos-vacios-como-ausencia-tipada.md',
    'El resultado de `min` y `max` contiene como máximo un valor. Cuando el análisis no demuestra que la agregación recibirá al menos un candidato, su cardinalidad exterior conservadora es `[0..1]`. Si la no-vacuidad se demuestra estáticamente, puede estrecharse a `[1]`.\n',
    'El resultado de `min` y `max` contiene como máximo un valor. Si el análisis demuestra cero iteraciones, su cardinalidad exterior es `[0]`. Si la fuente puede estar vacía o no vacía, la forma conservadora es `[0..1]`. Si se demuestra al menos un candidato, se estrecha a `[1]`.\n',
)
replace_once(
    'notas/decisiones/ADR-093-extremos-vacios-como-ausencia-tipada.md',
    '3. Una fuente posiblemente vacía produce resultado `[0..1]`.\n4. Una fuente demostrablemente no vacía permite resultado `[1]`.\n5. No existe diagnóstico específico de agregación extrema vacía.\n6. `sum`, `count`, `exists` y `forall` conservan sus resultados sobre cero iteraciones.\n',
    '3. Una fuente demostrablemente vacía produce resultado `[0]`.\n4. Una fuente posiblemente vacía produce resultado `[0..1]`.\n5. Una fuente demostrablemente no vacía produce resultado `[1]`.\n6. No existe diagnóstico específico de agregación extrema vacía.\n7. `sum`, `count`, `exists` y `forall` conservan sus resultados sobre cero iteraciones.\n',
)
replace_once(
    'notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md',
    'La fuente debe ser finita y enumerable. La evaluación es pura; `min` y `max` sobre una fuente que produce cero iteraciones devuelven `empty` con el tipo del valor agregado. No se inventa un extremo sentinela ni se genera un fallo por la vacuidad. Cuando no se demuestra no-vacuidad, el resultado extremo conserva cardinalidad exterior `[0..1]`; puede estrecharse a `[1]` si existe al menos un candidato demostrado.\n',
    'La fuente debe ser finita y enumerable. La evaluación es pura; `min` y `max` sobre una fuente que produce cero iteraciones devuelven `empty` con el tipo del valor agregado. No se inventa un extremo sentinela ni se genera un fallo por la vacuidad. El resultado extremo es como máximo singular: usa `[0]` si la vacuidad se demuestra, `[0..1]` si sigue siendo posible y `[1]` si se demuestra al menos un candidato.\n',
)
replace_once(
    'especificacion/07-gramatica-concreta.md',
    'Sobre cero iteraciones, `forall` produce `true`, `exists` produce `false`, `count` produce `0 : Nat` y `sum` conserva su cero aditivo. `min` y `max` producen `empty` con el tipo del valor agregado, no un error ni un extremo sentinela. Su resultado contiene como máximo un valor: usa `[0..1]` cuando la no-vacuidad no puede demostrarse y puede estrecharse a `[1]` cuando el análisis demuestra al menos un candidato. Un contexto que exija `[1]` aplica las reglas generales de cardinalidad; `empty` no se convierte por ello en un fallo especial.\n',
    'Sobre cero iteraciones, `forall` produce `true`, `exists` produce `false`, `count` produce `0 : Nat` y `sum` conserva su cero aditivo. `min` y `max` producen `empty` con el tipo del valor agregado, no un error ni un extremo sentinela. Su resultado contiene como máximo un valor: usa `[0]` si el análisis demuestra vacuidad, `[0..1]` si la vacuidad sigue siendo posible y `[1]` si demuestra al menos un candidato. Un contexto que exija `[1]` aplica las reglas generales de cardinalidad; `empty` no se convierte por ello en un fallo especial.\n',
)

# The two statically empty conformance cases must carry the exact [0] result.
p = Path('especificacion/sintaxis/casos/cst-ast.yaml')
text = p.read_text(encoding='utf-8')
old = '  - result-cardinality-[0..1]\n  - statically-known-empty\n'
if text.count(old) != 2:
    raise SystemExit(f'empty extrema cardinality cases count={text.count(old)}')
text = text.replace(old, '  - result-cardinality-[0]\n  - statically-known-empty\n', 2)
p.write_text(text, encoding='utf-8', newline='\n')

print('PHASE4C_REVIEW_FIXES_OK')
