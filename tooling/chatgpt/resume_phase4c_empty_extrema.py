from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding='utf-8', newline='\n')


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one match, got {count}: {old!r}')
    write(path, text.replace(old, new, 1))


d93 = '''---
id: D-093
title: "Extremos vacíos como ausencia tipada"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "min, max, agregaciones, empty, cardinalidad y evaluación pura"
---
# ADR-093 — Extremos vacíos como ausencia tipada

- Modifica: [[ADR-047-cuantificadores-e-iteracion-finita|D-047]].
- Alinea con: [[ADR-039-colecciones-y-diccionarios|D-039]] y [[ADR-075-dominios-enumerables-all-y-valores-derivados|D-075]].

## Contexto

D-047 hacía que `min` y `max` sobre una fuente con cero iteraciones produjeran un error específico de agregación vacía. El resto del modelo de valores trata normalmente la ausencia de resultado como cardinalidad cero: `empty` no es por sí mismo un fallo y el conflicto aparece solo si el contexto exige una forma que no admite esa cardinalidad.

Fabricar un valor extremo sentinela tampoco es válido porque no existe un mínimo o máximo universal para todos los tipos ordenables.

## Decisión

Si `min` o `max` recorren cero iteraciones, el resultado es `empty` con el tipo de valor que habría producido el cuerpo de la agregación. No se fabrica ningún valor extremo y la vacuidad no genera por sí sola `failed` ni un diagnóstico de agregación vacía.

El resultado de `min` y `max` contiene como máximo un valor. Cuando el análisis no demuestra que la agregación recibirá al menos un candidato, su cardinalidad exterior conservadora es `[0..1]`. Si la no-vacuidad se demuestra estáticamente, puede estrecharse a `[1]`.

Un contexto posterior que exija cardinalidad `[1]` usa las reglas generales de compatibilidad y obligaciones de cardinalidad. Esta decisión no convierte `empty` en un fallo especial ni modifica esas reglas.

El cambio se limita al caso de cero iteraciones. No redefine cómo se trata una expresión de cuerpo cuya propia forma no satisfaga el contrato de valor ordenable exigido por `min` o `max`.

Se conservan los demás neutros de agregación y cuantificación:

- `forall` sobre cero iteraciones produce `true`;
- `exists` produce `false`;
- `count` produce `0 : Nat`;
- `sum` produce el cero aditivo del tipo correspondiente.

## Consecuencias

- `min` y `max` pasan a ser agregaciones parciales expresadas mediante cardinalidad, no mediante una excepción de vacuidad.
- una fuente demostrablemente vacía permite conocer el resultado como `empty` durante análisis estático;
- la ausencia de extremo se compone con las mismas reglas que otras expresiones opcionales;
- no cambia la exigencia de fuente finita/enumerable ni de cuerpo totalmente ordenable.

## Verificación

1. `min` sobre una fuente vacía produce `empty`.
2. `max` sobre una fuente vacía produce `empty`.
3. Una fuente posiblemente vacía produce resultado `[0..1]`.
4. Una fuente demostrablemente no vacía permite resultado `[1]`.
5. No existe diagnóstico específico de agregación extrema vacía.
6. `sum`, `count`, `exists` y `forall` conservan sus resultados sobre cero iteraciones.
'''
path = ROOT / 'notas/decisiones/ADR-093-extremos-vacios-como-ausencia-tipada.md'
if path.exists():
    raise SystemExit('D-093 already exists')
path.write_text(d93, encoding='utf-8', newline='\n')

path = 'notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md'
replace_once(
    path,
    '- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]\n',
    '- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]\n- Modificada por: [[ADR-093-extremos-vacios-como-ausencia-tipada|D-093]]\n',
)
replace_once(
    path,
    'La fuente debe ser finita y enumerable. La evaluación es pura; `min` y `max` sobre una fuente vacía producen el error definido para agregación vacía, no un valor inventado.\n',
    'La fuente debe ser finita y enumerable. La evaluación es pura; `min` y `max` sobre una fuente que produce cero iteraciones devuelven `empty` con el tipo del valor agregado. No se inventa un extremo sentinela ni se genera un fallo por la vacuidad. Cuando no se demuestra no-vacuidad, el resultado extremo conserva cardinalidad exterior `[0..1]`; puede estrecharse a `[1]` si existe al menos un candidato demostrado.\n',
)
replace_once(path, '2. Error de agregación extrema vacía.\n', '2. `empty` y cardinalidad opcional en agregación extrema vacía.\n')

path = 'especificacion/07-gramatica-concreta.md'
replace_once(path, '  - D-092\n', '  - D-092\n  - D-093\n')
needle = '''Una selección devuelve directamente las ocurrencias aceptadas y conserva multiplicidad, unicidad y orden demostrables. Su predicado sigue siendo puro y determinista.
'''
addition = '''Una selección devuelve directamente las ocurrencias aceptadas y conserva multiplicidad, unicidad y orden demostrables. Su predicado sigue siendo puro y determinista.

Sobre cero iteraciones, `forall` produce `true`, `exists` produce `false`, `count` produce `0 : Nat` y `sum` conserva su cero aditivo. `min` y `max` producen `empty` con el tipo del valor agregado, no un error ni un extremo sentinela. Su resultado contiene como máximo un valor: usa `[0..1]` cuando la no-vacuidad no puede demostrarse y puede estrecharse a `[1]` cuando el análisis demuestra al menos un candidato. Un contexto que exija `[1]` aplica las reglas generales de cardinalidad; `empty` no se convierte por ello en un fallo especial.
'''
replace_once(path, needle, addition)

path = 'especificacion/sintaxis/casos/cst-ast.yaml'
text = read(path)
if 'id: min-empty-source' in text:
    raise SystemExit('empty extrema cases already exist')
addition = r'''- id: min-empty-source
  category: aggregation
  source: "thing Sample {\n    values: Nat [0] = empty\n    minimum := min value in values: value\n}\n"
  cst_root: MudFileSyntax
  ast: QuantifierExpr(Minimum, value, values, value)
  semantic_expectations:
  - result-type-Nat
  - result-cardinality-[0..1]
  - statically-known-empty
  - no-empty-extrema-failure
  produces_ast: true
- id: max-empty-source
  category: aggregation
  source: "thing Sample {\n    values: Nat [0] = empty\n    maximum := max value in values: value\n}\n"
  cst_root: MudFileSyntax
  ast: QuantifierExpr(Maximum, value, values, value)
  semantic_expectations:
  - result-type-Nat
  - result-cardinality-[0..1]
  - statically-known-empty
  - no-empty-extrema-failure
  produces_ast: true
- id: extrema-proven-nonempty
  category: aggregation
  source: "thing Sample {\n    values: Nat [1..*] = [1]\n    minimum := min value in values: value\n}\n"
  cst_root: MudFileSyntax
  ast: QuantifierExpr(Minimum, value, values, value)
  semantic_expectations:
  - result-type-Nat
  - result-cardinality-[1]
  produces_ast: true
'''
if not text.endswith('\n'):
    text += '\n'
write(path, text + addition)

print('PHASE4C_EMPTY_EXTREMA_OK')
