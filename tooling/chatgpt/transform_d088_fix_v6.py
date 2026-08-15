from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()


def read(rel):
    return (root / rel).read_text(encoding="utf-8")


def write(rel, text):
    (root / rel).write_text(text.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def exact(text, old, new, label, count=1):
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"{label}: expected {count}, found {actual}")
    return text.replace(old, new, count)


# -----------------------------------------------------------------------------
# D-088: remove pseudocode, integrate runtime failure taxonomy, and scope
# default steps to progression-based enumeration rather than all enumerable data.
# -----------------------------------------------------------------------------
rel = "notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md"
t = read(rel)
t = exact(
    t,
    '''```mud
for each i in [1..10]:
    process i
```''',
    '''```mud
action Accumulate for mut total: Int {
    then for each i in [1..10]:
        total += i
}
```''',
    "D088 enumerable example",
)
t = exact(
    t,
    '''```mud
for each i in [1..10]: {
    doubled := i * 2
    process doubled
}
```''',
    '''```mud
action AccumulateDoubled for mut total: Int {
    then for each i in [1..10]: {
        doubled := i * 2
        total += doubled
    }
}
```''',
    "D088 block example",
)
t = exact(
    t,
    '''```mud
for each i in [1..8] by 2:
    use i
# 1, 3, 5, 7

for each i in [1..8] by -3:
    use i
# 8, 5, 2
```''',
    '''```mud
action Forward for mut total: Int {
    then for each i in [1..8] by 2:
        total += i
}
# recorrido: 1, 3, 5, 7

action Backward for mut total: Int {
    then for each i in [1..8] by -3:
        total += i
}
# recorrido: 8, 5, 2
```''',
    "D088 signed examples",
)
t = exact(
    t,
    "Se generaliza el antiguo `BooleanBlock` a `ExpressionBlock(locals, result)`. La estructura no decide el tipo de `result`; lo hace su propietario. Reglas booleanas, `if`, selección, `exists`, `forall` y `count` aplican su contrato booleano; `when` exige un activador admitido; `sum` un valor agregable; `min` y `max` un valor ordenable.",
    "Se generaliza el antiguo `BooleanBlock` a `ExpressionBlock(locals, result)`. La estructura no decide el tipo de `result`; lo hace su propietario. Reglas booleanas, guardas `if`, reglas `always`, postcondiciones `after` de acciones, selección, `exists`, `forall` y `count` aplican su contrato booleano; `when` exige un activador admitido; `sum` un valor agregable; `min` y `max` un valor ordenable. El `after` de test conserva su estructura propia de varias aserciones.",
    "D088 expression-block owner contracts",
)
t = exact(
    t,
    "Si un paso runtime es demostrablemente cero, existe error estático. Si no puede demostrarse y finalmente evalúa a cero, la resolución produce `failed` y revierte. En un dominio escalonado el paso es estático, por lo que cero siempre es error de elaboración.",
    "Si un paso runtime es demostrablemente cero, existe error estático. Si no puede demostrarse y finalmente evalúa a cero, se produce un fallo de evaluación `progression-step-zero`. Dentro de una acción real ese fallo produce `failed` y rollback conforme a la taxonomía de D-048 y D-061; en un contexto puro se propaga conforme al contrato de fallos de expresiones, sin convertirse en `false`. En un dominio escalonado el paso es estático, por lo que cero siempre es error de elaboración.",
    "D088 zero runtime taxonomy",
)
t = exact(
    t,
    "Puede omitirse `by` únicamente cuando el tipo define un siguiente valor canónico. MUD fija `Nat -> 1`, `Int -> 1` y `Money -> 0.01`. Omitir `by` siempre selecciona el paso positivo. Otros tipos exactos ordenados requieren paso explícito salvo decisión que defina uno canónico.\n\n`Num` admite progresión con paso exacto explícito, pero un intervalo general de `Num` sin paso es inválido. `Rum` conserva la prohibición de D-034: sus intervalos nunca son enumerables y `by` nunca es válido sobre ellos, ni en iteración ni en dominio escalonado. Una colección explícita de valores `Rum` sí puede enumerarse.",
    "Una fuente que ya posee enumeración propia —por ejemplo una colección ordenada, un diccionario exacto o un dominio nominal finito— no necesita `by` para recorrerse. Los pasos predeterminados solo intervienen cuando la enumeración se construye como progresión. En esas fuentes puede omitirse `by` únicamente cuando el tipo recorrido define una diferencia sucesora canónica. MUD fija `Nat -> 1`, `Int -> 1` y `Money -> 0.01`; omitir `by` selecciona siempre esa diferencia positiva. Otros tipos de progresión exacta requieren paso explícito salvo decisión que defina un sucesor canónico.\n\n`Num` admite progresión con paso exacto explícito, pero un intervalo general de `Num` sin paso es inválido. `Rum` conserva la prohibición de D-034: sus intervalos nunca son enumerables y no admiten progresión `by`, ni en iteración ni en dominio escalonado. Una colección explícita de valores `Rum` sí puede enumerarse sin `by` porque su enumeración procede de la colección, no de una progresión numérica.",
    "D088 default progression scope",
)
t = exact(
    t,
    "El AST superficial reemplaza `BooleanBlock` por `ExpressionBlock`, conserva `step` opcional en `for each`, selección y cuantificadores, conserva filtros/cuerpos como `ExpressionBlock` y normaliza el cuerpo breve de `for each` al mismo `EffectBlock` que usa `then`. `by -2` no necesita nodo especial para el signo.",
    "El AST superficial reemplaza `BooleanBlock` por `ExpressionBlock`. `ForEachEffect` conserva `step?`, conserva su filtro opcional como `ExpressionBlock?` y normaliza tanto el efecto breve como el bloque ejecutable al mismo `EffectBlock` que usa `then`. `SelectionExpr` y `QuantifierExpr` conservan `step?` y su predicado/cuerpo como `ExpressionBlock`. `by -2` no necesita nodo especial para el signo.",
    "D088 AST consequences",
)
t = exact(
    t,
    "Debe diagnosticarse ausencia de `:`, paso cero, diferencia incompatible, falta de paso cuando no exista predeterminado, fuente infinita/no enumerable, `by` con `Rum`, `by` sobre fuente sin progresión, filtro no booleano, azar en filtro y uso de extremos invertidos como supuesto descenso.",
    "Debe diagnosticarse ausencia de `:`, paso cero, diferencia incompatible, falta de paso cuando una progresión no tenga sucesor predeterminado, fuente infinita/no enumerable, intento de progresión sobre un intervalo `Rum`, `by` sobre fuente sin progresión, filtro no booleano, azar en filtro y uso de extremos invertidos como supuesto descenso.",
    "D088 diagnostics wording",
)
t = exact(
    t,
    "Se verifican fuentes enumerables de todas las clases admitidas, `:` con cuerpo breve y con llaves, filtro breve y con locales, pasos positivos/negativos/runtime, cero estático/runtime, límites abiertos/cerrados, intervalos vacíos/infinitos/discontinuos, dominios escalonados firmados y `all`, `Num`, rechazo `Rum`, selección y seis cuantificadores con `by` y bloque, magnitudes con unidades compatibles, puntos con diferencia lineal, ciclo durante un periodo fundamental y diferencia entre filtro ordenado/no ordenado.",
    "Se verifican fuentes enumerables de todas las clases admitidas, `:` con cuerpo breve y con llaves, filtro breve y con locales, pasos positivos/negativos/runtime, evaluación única del paso, cero estático/runtime, límites abiertos/cerrados, intervalos vacíos/infinitos, dominios escalonados firmados y `all`, `Num`, rechazo de progresión `Rum`, colección explícita de `Rum`, selección y los seis cuantificadores con `by` y bloque, magnitudes con unidades compatibles y diferencia entre filtro ordenado/no ordenado. La verificación concreta de intervalos discontinuos y del periodo fundamental cíclico se completa cuando Q-018 cierre la forma fuente consolidada necesaria para expresarlos sin ambigüedad; su semántica queda fijada por esta decisión.",
    "D088 verification coverage",
)
write(rel, t)


# -----------------------------------------------------------------------------
# Chapter 07 mirrors the same normative distinctions.
# -----------------------------------------------------------------------------
rel = "especificacion/07-gramatica-concreta.md"
t = read(rel)
t = exact(
    t,
    "Un paso runtime demostrablemente cero es error estático; si puede variar y finalmente vale cero, produce `failed`. En un dominio escalonado cero siempre es error estático. La compatibilidad usa la operación de avance y conversiones implícitas exactas, no identidad nominal: `Nat` puede avanzar por `Int`, `Num` por diferencias exactas compatibles y las magnitudes por unidades compatibles. En una magnitud de punto el paso es una diferencia lineal.",
    "Un paso runtime demostrablemente cero es error estático; si puede variar y finalmente vale cero, produce el fallo de evaluación `progression-step-zero`. En una acción real ese fallo termina como `failed` y rollback; en una expresión pura se propaga como fallo de evaluación y nunca se convierte en `false`. En un dominio escalonado cero siempre es error estático. La compatibilidad usa la operación de avance y conversiones implícitas exactas, no identidad nominal: `Nat` puede avanzar por `Int`, `Num` por diferencias exactas compatibles y las magnitudes por unidades compatibles. En una magnitud de punto el paso es una diferencia lineal.",
    "07 zero runtime taxonomy",
)
t = exact(
    t,
    "`Nat` e `Int` usan `1`; `Money`, `0.01`. Omitir `by` elige siempre el paso positivo. Otros tipos exactos ordenados requieren paso explícito salvo siguiente canónico definido. `Num` admite paso exacto explícito y un intervalo general de `Num` sin paso es inválido. Los intervalos de `Rum` nunca admiten `by`, ni en iteración ni en dominios escalonados; una colección explícita de valores `Rum` sí es enumerable.",
    "Una fuente con enumeración propia no necesita `by`. Cuando la enumeración depende de una progresión, `Nat` e `Int` usan por defecto `1` y `Money`, `0.01`; omitir `by` elige siempre esa diferencia positiva. Otros tipos de progresión exacta requieren paso explícito salvo sucesor canónico definido. `Num` admite paso exacto explícito y un intervalo general de `Num` sin paso es inválido. Los intervalos de `Rum` nunca admiten progresión `by`, ni en iteración ni en dominios escalonados; una colección explícita de valores `Rum` sí es enumerable sin `by`.",
    "07 default progression scope",
)
write(rel, t)


# -----------------------------------------------------------------------------
# D-047: make the default/progression distinction visible in the older decision.
# -----------------------------------------------------------------------------
rel = "notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md"
t = read(rel)
t = exact(
    t,
    "Los intervalos finitos de `Nat` e `Int` usan paso predeterminado uno; `Money`, paso `0.01`. Un intervalo de `Num` no discreto requiere paso exacto explícito. Los intervalos de `Rum` nunca son enumerables. El último valor es el último punto generado que pertenece al intervalo; no se fuerza la inclusión del extremo.",
    "Cuando una enumeración se obtiene mediante progresión, los intervalos finitos de `Nat` e `Int` usan paso predeterminado uno y `Money`, paso `0.01`. Las fuentes que ya poseen enumeración propia no necesitan fabricar un paso. Un intervalo general de `Num` requiere paso exacto explícito. Los intervalos de `Rum` nunca son enumerables. El último valor es el último punto generado que pertenece al intervalo; no se fuerza la inclusión del extremo.",
    "D047 default progression scope",
)
write(rel, t)


# -----------------------------------------------------------------------------
# Conformance corpus: add the edge cases that the decision explicitly promises.
# Additional semantic_expectations keys are documentary expectations; the current
# syntax-model validator only requires stable ids and produces_ast.
# -----------------------------------------------------------------------------
rel = "especificacion/sintaxis/casos/cst-ast.yaml"
t = read(rel)
marker = "- id: d088-runtime-zero-step-action\n"
if marker in t:
    raise SystemExit("D088 v6 cases already present")
append = r'''
- id: d088-runtime-zero-step-action
  category: runtime
  source: "action Accumulate for mut total: Int given step: Int {\n    then for each i in [1..8] by step:\n        total += i\n}\n"
  cst_root: MudFileSyntax
  ast: ForEachEffect(binding=i, source=[1..8], step=step, body=EffectBlock(...))
  expected_diagnostics:
  - progression-step-zero-runtime-when-step-is-zero
  semantic_expectations:
  - step-evaluated-once-before-traversal
  - zero-runtime-step-is-evaluation-failure
  - action-evaluation-failure-produces-failed-and-rollback
  produces_ast: true
- id: d088-num-interval-without-step-rejected
  category: validation-after-resolution
  source: "action SumNum for mut total: Num {\n    then for each value in [0.0..1.0]:\n        total += value\n}\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - progression-step-required
  produces_ast: true
- id: d088-infinite-interval-not-enumerable
  category: validation-after-resolution
  source: "action Infinite for mut total: Int {\n    then for each value in [0..*]:\n        total += value\n}\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - source-not-finitely-enumerable
  produces_ast: true
- id: d088-arbitrary-collection-by-is-not-stride
  category: validation-after-resolution
  source: "action Broken for values: Nat [*], mut total: Nat {\n    then for each value in values by 2:\n        total += value\n}\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - source-does-not-support-progression
  produces_ast: true
- id: d088-filter-must-be-bool
  category: validation-after-resolution
  source: "action Broken for mut total: Int {\n    then for each value in [1..4] if value + 1:\n        total += value\n}\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - iteration-filter-requires-bool
  produces_ast: true
- id: d088-random-filter-rejected
  category: validation-after-resolution
  source: "action Broken for mut total: Int {\n    then for each value in [1..4] if Rand([true, false]):\n        total += value\n}\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - random-not-allowed-in-iteration-filter
  produces_ast: true
- id: d088-step-evaluated-once
  category: runtime
  source: "thing Counter {\n    mut step: Int = 2\n    mut total: Int = 0\n}\naction Advance {\n    then for each value in [1..8] by Counter.step: {\n        Counter.step = 1\n        Counter.total += value\n    }\n}\n"
  cst_root: MudFileSyntax
  ast: ForEachEffect(step=MemberAccessExpr(Counter, step), body=EffectBlock(...))
  semantic_expectations:
  - step-read-once-before-first-iteration
  - later-step-writes-do-not-change-current-progression
  - visited-values-are-1-3-5-7
  produces_ast: true
- id: d088-explicit-rum-collection-enumerable
  category: iteration
  source: "action Visit for values: Rum [*], mut seen: Nat {\n    then for each value in values:\n        seen += 1\n}\n"
  cst_root: MudFileSyntax
  ast: ForEachEffect(binding=value, source=values, step=None, body=EffectBlock(...))
  semantic_expectations:
  - enumeration-comes-from-collection-not-rum-progression
  produces_ast: true
- id: d088-ordered-filter-sees-previous-effects
  category: runtime
  source: "thing OrderedFilter {\n    mut budget: Int = 1\n    items: Int [2 ordered] = [1, 1]\n}\naction SpendOrdered {\n    then for each value in OrderedFilter.items if OrderedFilter.budget > 0:\n        OrderedFilter.budget -= 1\n}\n"
  cst_root: MudFileSyntax
  ast: ForEachEffect(filter=ExpressionBlock([], ...), ...)
  semantic_expectations:
  - source-membership-captured-at-loop-start
  - second-filter-sees-budget-after-first-iteration
  - exactly-one-iteration-is-accepted
  produces_ast: true
- id: d088-unordered-filter-sees-initial-snapshot
  category: runtime
  source: "thing UnorderedFilter {\n    mut budget: Int = 1\n    items: Int [2] = [1, 1]\n}\naction SpendUnordered {\n    then for each value in UnorderedFilter.items if UnorderedFilter.budget > 0:\n        UnorderedFilter.budget -= 1\n}\n"
  cst_root: MudFileSyntax
  ast: ForEachEffect(filter=ExpressionBlock([], ...), ...)
  semantic_expectations:
  - source-membership-captured-at-loop-start
  - all-filters-read-the-same-initial-snapshot
  - both-iterations-are-accepted-before-delta-consolidation
  produces_ast: true
- id: d088-remaining-quantifiers-with-by
  category: expression
  source: "thing Quantified {\n    any := exists value in [1..10] by 2: value > 5\n    every := forall value in [1..10] by 2: value > 0\n    smallest := min value in [1..10] by 2: value\n    largest := max value in [1..10] by 2: value\n}\n"
  cst_root: MudFileSyntax
  ast: QuantifierExpr(Exists, step=2); QuantifierExpr(ForAll, step=2); QuantifierExpr(Minimum, step=2); QuantifierExpr(Maximum, step=2)
  produces_ast: true
- id: d088-open-lower-positive-step
  category: runtime
  source: "action OpenLower for mut total: Int {\n    then for each value in (1..8] by 2:\n        total += value\n}\n"
  cst_root: MudFileSyntax
  semantic_expectations:
  - visited-values-are-3-5-7
  produces_ast: true
- id: d088-open-upper-negative-step
  category: runtime
  source: "action OpenUpper for mut total: Int {\n    then for each value in [1..8) by -2:\n        total += value\n}\n"
  cst_root: MudFileSyntax
  semantic_expectations:
  - visited-values-are-6-4-2
  produces_ast: true
- id: d088-empty-inverted-interval-zero-iterations
  category: runtime
  source: "action EmptyLoop for mut total: Int {\n    then for each value in [8..1] by -1:\n        total += value\n}\n"
  cst_root: MudFileSyntax
  semantic_expectations:
  - interval-normalizes-to-empty
  - loop-performs-zero-iterations
  produces_ast: true
'''
t = t.rstrip("\n") + "\n" + append.lstrip("\n")
write(rel, t)


# -----------------------------------------------------------------------------
# Postconditions.
# -----------------------------------------------------------------------------
checks = {
    "notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md": [
        "fallo de evaluación `progression-step-zero`",
        "Una fuente que ya posee enumeración propia",
        "`ForEachEffect` conserva `step?`",
        "La verificación concreta de intervalos discontinuos",
    ],
    "especificacion/07-gramatica-concreta.md": [
        "produce el fallo de evaluación `progression-step-zero`",
        "Una fuente con enumeración propia no necesita `by`",
    ],
    "notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md": [
        "Las fuentes que ya poseen enumeración propia no necesitan fabricar un paso",
    ],
    "especificacion/sintaxis/casos/cst-ast.yaml": [
        "id: d088-runtime-zero-step-action",
        "id: d088-num-interval-without-step-rejected",
        "id: d088-infinite-interval-not-enumerable",
        "id: d088-arbitrary-collection-by-is-not-stride",
        "id: d088-random-filter-rejected",
        "id: d088-step-evaluated-once",
        "id: d088-explicit-rum-collection-enumerable",
        "id: d088-ordered-filter-sees-previous-effects",
        "id: d088-unordered-filter-sees-initial-snapshot",
        "id: d088-remaining-quantifiers-with-by",
        "id: d088-open-lower-positive-step",
        "id: d088-open-upper-negative-step",
        "id: d088-empty-inverted-interval-zero-iterations",
    ],
}
for rel, needles in checks.items():
    text = read(rel)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"missing {needle!r} in {rel}")

for bad in ("process i", "process doubled", "use i"):
    if bad in read("notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md"):
        raise SystemExit(f"pseudocode remains in D088: {bad}")

print("D088_FIX_V6_OK")
