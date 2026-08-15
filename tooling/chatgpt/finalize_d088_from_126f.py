from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def read(rel):
    return (root / rel).read_text(encoding='utf-8')

def write(rel, text):
    (root / rel).write_text(text.rstrip('\n') + '\n', encoding='utf-8', newline='\n')

def exact(text, old, new, label, count=1):
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f'{label}: expected {count}, found {actual}')
    return text.replace(old, new, count)

def case_block(text, case_id):
    marker = f'- id: {case_id}\n'
    if text.count(marker) != 1:
        raise SystemExit(f'{case_id}: marker count {text.count(marker)}')
    start = text.index(marker)
    end = text.find('\n- id: ', start + len(marker))
    if end < 0:
        end = len(text)
    return start, end, text[start:end]

def replace_case(text, case_id, old, new, label):
    start, end, block = case_block(text, case_id)
    if block.count(old) != 1:
        raise SystemExit(f'{label}: expected once in {case_id}, found {block.count(old)}')
    block = block.replace(old, new, 1)
    return text[:start] + block + text[end:]

# D-088: valid examples, precise default-step antecedent and scope rules.
rel = 'notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md'
t = read(rel)
t = exact(t,
'  - "for each, filtros, cuantificadores, selección, dominios escalonados, intervalos, magnitudes, bloques de expresión, gramática, CST y AST"',
'  - "for each, filtros, cuantificadores, selección, dominios escalonados, intervalos, magnitudes, bloques de expresión, resolución de nombres, gramática, CST y AST"',
'D088 affects')
t = exact(t,
'''```mud
action Accumulate for mut total: Int {
    then for each i in [1..10]:
        total += i
}
```''',
'''```mud
action Accumulate for values: Int [* ordered], mut total: Int {
    then for each value in values:
        total += value
}
```''', 'D088 first example')
t = exact(t,
'''```mud
action AccumulateDoubled for mut total: Int {
    then for each i in [1..10]: {
        doubled := i * 2
        total += doubled
    }
}
```''',
'''```mud
action AccumulateDoubled for values: Int [* ordered], mut total: Int {
    then for each value in values: {
        doubled := value * 2
        total += doubled
    }
}
```''', 'D088 block example')
t = exact(t,
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
'''```mud
action Forward for mut total: Num {
    then for each value in [1..8] by 2:
        total += value
}
# recorrido: 1, 3, 5, 7

action Backward for mut total: Num {
    then for each value in [1..8] by -3:
        total += value
}
# recorrido: 8, 5, 2
```''', 'D088 signed examples')
t = exact(t,
'Una fuente que ya posee enumeración propia —por ejemplo una colección ordenada, un diccionario exacto o un dominio nominal finito— no necesita `by` para recorrerse. Los pasos predeterminados solo intervienen cuando la enumeración se construye como progresión. En esas fuentes puede omitirse `by` únicamente cuando el tipo recorrido define una diferencia sucesora canónica. MUD fija `Nat -> 1`, `Int -> 1` y `Money -> 0.01`; omitir `by` selecciona siempre esa diferencia positiva. Otros tipos de progresión exacta requieren paso explícito salvo decisión que defina un sucesor canónico.',
'Una fuente que ya posee enumeración propia —por ejemplo una colección, un diccionario exacto o un dominio nominal finito— no necesita `by` para recorrerse. Los pasos predeterminados solo intervienen cuando la enumeración se construye como progresión. En una fuente cuya enumeración se construye como progresión puede omitirse `by` únicamente cuando el tipo recorrido define una diferencia sucesora canónica. MUD fija `Nat -> 1`, `Int -> 1` y `Money -> 0.01`; omitir `by` selecciona siempre esa diferencia positiva. Otros tipos de progresión exacta requieren paso explícito salvo decisión que defina un sucesor canónico.',
'D088 default step antecedent')
anchor = 'Las locales son puras, inmutables, secuenciales y no admiten referencias adelantadas, ciclos, redeclaración ni sombreado.\n'
scope = '''

## Ámbitos de iteración y bloques de expresión

`source` y el `by` opcional se resuelven en el entorno exterior, antes de introducir la vinculación de iteración. Por tanto, la variable iterada —o la pareja `(key, value)`— no es visible dentro de `source` ni de `by`.

En `for each`, la vinculación de iteración sí es visible en el filtro `if` y en el cuerpo ejecutable. Si el filtro usa un `ExpressionBlock`, sus locales son visibles únicamente en las locales posteriores y en la expresión final del propio filtro; desaparecen antes de entrar en el cuerpo de efectos.

En selección y cuantificadores/agregadores, la vinculación introducida es visible en las locales y en la expresión final de su `ExpressionBlock`, pero no fuera de él. Cada local se vuelve visible después de su propia declaración, de modo que puede ser usada por locales posteriores y por el resultado final, nunca por su inicializador ni por declaraciones anteriores.
'''
if scope.strip() in t or t.count(anchor) != 1:
    raise SystemExit('D088 scope insertion precondition failed')
t = t.replace(anchor, anchor + scope, 1)
write(rel, t)

# Historical ADR examples touched by D-088 must be actual MUD, not ellipsis pseudocode.
rel = 'notas/decisiones/ADR-033-claves-y-enumeracion-de-aliases.md'
t = read(rel)
t = exact(t,
'''```mud
for each coordinate in Coordinate: {
    ...
}

exists destination in Coordinate:
    ...
```''',
'''```mud
action VisitCoordinates for mut visits: Nat {
    then for each coordinate in Coordinate:
        visits += 1
}

rule HasLeftEdge {
    exists destination in Coordinate:
        destination.horizontal == 0
}
```''', 'D033 examples')
write(rel, t)

rel = 'notas/decisiones/ADR-034-number-exacto-y-rumber-binary64.md'
t = read(rel)
t = exact(t,
'''```mud
for each value in [r0..r1] by r0.1: {}
```''',
'''```mud
action InvalidRumIteration for mut total: Rum {
    then for each value in [r0..r1] by r0.1:
        total += value
}
```''', 'D034 Rum example')
write(rel, t)

rel = 'notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md'
t = read(rel)
t = exact(t,
'''```mud
for each item in source if predicate: {
    ...
}

for each value in source by step if predicate: {
    ...
}
```''',
'''```mud
for each item in source if predicate:
    iterations += 1

for each value in source by step if predicate:
    iterations += 1
```''', 'D047 examples')
write(rel, t)

# Name resolution propagation.
rel = 'especificacion/09-nombres-y-anclas.md'
t = read(rel)
t = exact(t, '  - D-087\n', '  - D-087\n  - D-088\n', '09 frontmatter')
anchor = 'Los accesos con puntos se elaboran por etapas: primero se resuelve la raíz nominal y después cada miembro con el tipo o propietario obtenido. Una ruta cualificada y una cadena de miembros pueden compartir escritura superficial sin compartir resolución interna.\n'
section = '''

## Ámbitos de iteración y bloques de expresión

Las vinculaciones de iteración y las declaraciones locales de `ExpressionBlock` son `LocalSymbol`: no reciben ancla pública y obedecen al primer nivel léxico de resolución.

En `for each`, la fuente y el `by` opcional se resuelven antes de introducir la vinculación. La variable simple o ambas variables de una pareja de diccionario pasan a estar visibles en el filtro `if` y en el cuerpo ejecutable. Una local declarada dentro del `ExpressionBlock` del filtro solo amplía el entorno de las locales posteriores y de la expresión final del filtro; no permanece visible en el cuerpo de efectos.

En una selección o un cuantificador/agregador, `source` y `by` se resuelven igualmente en el entorno exterior. Después se introduce la vinculación y se resuelve el `ExpressionBlock`: cada local ve las vinculaciones exteriores y las locales anteriores; el resultado final ve todas las locales del bloque. La vinculación y esas locales dejan de existir al terminar la expresión propietaria.

Ninguno de estos ámbitos permite referencias adelantadas, ciclos, redeclaración o sombreado de un nombre ya visible. El AST resuelto usa la variante genérica `LocalSymbol(owner, kind, name, ordinal)`; D-088 no introduce una clase de símbolo ni una categoría de ancla nuevas.
'''
if section.strip() in t or t.count(anchor) != 1:
    raise SystemExit('09 scope insertion precondition failed')
t = t.replace(anchor, anchor + section, 1)
write(rel, t)

# CST frontmatter attribution/order.
rel = 'especificacion/sintaxis/cst-sin-perdidas.md'
t = read(rel)
t = exact(t,
'''  - D-085
  - D-086
  - D-088
  - D-087
''',
'''  - D-085
  - D-086
  - D-087
  - D-088
''', 'CST decision order')
write(rel, t)

rel = 'especificacion/sintaxis/cst-a-ast-superficial.md'
t = read(rel)
t = exact(t, '  - D-087\n', '  - D-087\n  - D-088\n', 'CST-AST frontmatter')
write(rel, t)

# Conformance corpus isolation and scope rules.
rel = 'especificacion/sintaxis/casos/cst-ast.yaml'
t = read(rel)
repls = [
('for-each-requires-colon', 'source: "action Iterate for mut total: Nat {\\n    then for each i in [1..5] {\\n        total += i\\n    }\\n}\\n"', 'source: "action Iterate for items: Nat [*], mut total: Nat {\\n    then for each i in items {\\n        total += i\\n    }\\n}\\n"', 'missing colon source'),
('for-each-negative-step', 'source: "action Iterate for mut total: Int {\\n    then for each i in [1..8] by -3:\\n        total += i\\n}\\n"', 'source: "action Iterate for mut total: Num {\\n    then for each i in [1..8] by -3:\\n        total += i\\n}\\n"', 'negative step accumulator'),
('for-each-static-zero-step', 'source: "action Broken for mut total: Int {\\n    then for each i in [1..8] by 0:\\n        total += i\\n}\\n"', 'source: "action Broken for mut total: Num {\\n    then for each i in [1..8] by 0:\\n        total += i\\n}\\n"', 'static zero accumulator'),
('d088-for-each-body-after-terminator', 'source: "action Accumulate for mut total: Int {\\n    then for each i in [1..3]:\\n        total += i\\n}\\n"', 'source: "action Accumulate for values: Int [*], mut total: Int {\\n    then for each i in values:\\n        total += i\\n}\\n"', 'newline for source'),
('d088-for-each-body-after-terminator', 'ast: ForEachEffect(binding=i, source=[1..3], body=EffectBlock(...))', 'ast: ForEachEffect(binding=i, source=values, body=EffectBlock(...))', 'newline for AST'),
('d088-selection-body-after-terminator', 'source: "thing Sample {\\n    selected := x in [1..3]:\\n        x > 1\\n}\\n"', 'source: "thing Sample {\\n    values: Int [*]\\n    selected := x in values:\\n        x > 1\\n}\\n"', 'newline selection source'),
('d088-selection-body-after-terminator', 'ast: SelectionExpr(binding=x, source=[1..3], predicate=ExpressionBlock([], x > 1))', 'ast: SelectionExpr(binding=x, source=values, predicate=ExpressionBlock([], x > 1))', 'newline selection AST'),
('d088-quantifier-block-after-terminator', 'source: "rule HasLarge {\\n    exists x in [1..3]:\\n        {\\n            limit := 1\\n            x > limit\\n        }\\n}\\n"', 'source: "rule HasLarge for values: Int [*] {\\n    exists x in values:\\n        {\\n            limit := 1\\n            x > limit\\n        }\\n}\\n"', 'newline quantifier source'),
('d088-quantifier-block-after-terminator', 'ast: QuantifierExpr(Exists, x, [1..3], body=ExpressionBlock([limit], x > limit))', 'ast: QuantifierExpr(Exists, x, values, body=ExpressionBlock([limit], x > limit))', 'newline quantifier AST'),
('d088-runtime-zero-step-action', 'source: "action Accumulate for mut total: Int given step: Int {\\n    then for each i in [1..8] by step:\\n        total += i\\n}\\n"', 'source: "action Accumulate for mut total: Num given step: Int {\\n    then for each i in [1..8] by step:\\n        total += i\\n}\\n"', 'runtime zero accumulator'),
('d088-infinite-interval-not-enumerable', 'source: "action Infinite for mut total: Int {\\n    then for each value in [0..*]:\\n        total += value\\n}\\n"', 'source: "action Infinite for mut total: Num {\\n    then for each value in [0..*] by 1:\\n        total += value\\n}\\n"', 'infinite source isolation'),
('d088-filter-must-be-bool', 'source: "action Broken for mut total: Int {\\n    then for each value in [1..4] if value + 1:\\n        total += value\\n}\\n"', 'source: "action Broken for mut total: Num {\\n    then for each value in [1..4] by 1 if value + 1:\\n        total += value\\n}\\n"', 'filter type isolation'),
('d088-random-filter-rejected', 'source: "action Broken for mut total: Int {\\n    then for each value in [1..4] if Rand([true, false]):\\n        total += value\\n}\\n"', 'source: "action Broken for mut total: Num {\\n    then for each value in [1..4] by 1 if Rand([true, false]):\\n        total += value\\n}\\n"', 'random filter isolation'),
('d088-step-evaluated-once', 'source: "thing Counter {\\n    mut step: Int = 2\\n    mut total: Int = 0\\n}\\naction Advance {\\n    then for each value in [1..8] by Counter.step: {\\n        Counter.step = 1\\n        Counter.total += value\\n    }\\n}\\n"', 'source: "thing Counter {\\n    mut step: Int = 2\\n    mut total: Num = 0\\n}\\naction Advance {\\n    then for each value in [1..8] by Counter.step: {\\n        Counter.step = 1\\n        Counter.total += value\\n    }\\n}\\n"', 'step once accumulator'),
('d088-open-lower-positive-step', 'source: "action OpenLower for mut total: Int {\\n    then for each value in (1..8] by 2:\\n        total += value\\n}\\n"', 'source: "action OpenLower for mut total: Num {\\n    then for each value in (1..8] by 2:\\n        total += value\\n}\\n"', 'open lower accumulator'),
('d088-open-upper-negative-step', 'source: "action OpenUpper for mut total: Int {\\n    then for each value in [1..8) by -2:\\n        total += value\\n}\\n"', 'source: "action OpenUpper for mut total: Num {\\n    then for each value in [1..8) by -2:\\n        total += value\\n}\\n"', 'open upper accumulator'),
('d088-empty-inverted-interval-zero-iterations', 'source: "action EmptyLoop for mut total: Int {\\n    then for each value in [8..1] by -1:\\n        total += value\\n}\\n"', 'source: "action EmptyLoop for mut total: Num {\\n    then for each value in [8..1] by -1:\\n        total += value\\n}\\n"', 'empty inverted accumulator'),
]
for cid, old, new, label in repls:
    t = replace_case(t, cid, old, new, label)
# Runtime zero is not a compile-time diagnostic when the step is unknown statically.
t = replace_case(t, 'd088-runtime-zero-step-action',
'''  expected_diagnostics:
  - progression-step-zero-runtime-when-step-is-zero
  semantic_expectations:
''',
'''  semantic_expectations:
  - runtime-zero-step-produces-progression-step-zero
''', 'runtime zero phase')

if '- id: d088-step-cannot-see-iteration-binding\n' in t:
    raise SystemExit('scope cases already present')
append = r'''
- id: d088-step-cannot-see-iteration-binding
  category: validation-after-resolution
  source: "action Broken for mut total: Num {\n    then for each value in [1..8] by value:\n        total += value\n}\n"
  cst_root: MudFileSyntax
  ast: ForEachEffect(binding=value, step=DottedPathExpr(value), ...)
  expected_diagnostics:
  - iteration-binding-not-visible-in-step
  semantic_expectations:
  - source-and-step-resolve-before-iteration-binding
  produces_ast: true
- id: d088-filter-local-not-visible-in-body
  category: validation-after-resolution
  source: "action Broken for values: Int [*], mut total: Int {\n    then for each value in values if {\n        adjusted := value + 1\n        adjusted > 0\n    }:\n        total += adjusted\n}\n"
  cst_root: MudFileSyntax
  ast: ForEachEffect(binding=value, filter=ExpressionBlock(locals=[adjusted], result=...), body=EffectBlock(...))
  expected_diagnostics:
  - filter-local-not-visible-in-loop-body
  semantic_expectations:
  - filter-expression-block-scope-ends-before-effect-body
  produces_ast: true
- id: d088-selection-binding-visible-in-expression-block
  category: expression
  source: "thing Sample {\n    values: Int [*]\n    selected := value in values: {\n        adjusted := value + 1\n        adjusted > 0\n    }\n}\n"
  cst_root: MudFileSyntax
  ast: SelectionExpr(binding=value, source=values, predicate=ExpressionBlock(locals=[adjusted], result=...))
  semantic_expectations:
  - selection-binding-visible-to-expression-block-locals-and-result
  produces_ast: true
'''
t = t.rstrip('\n') + '\n' + append.lstrip('\n')
write(rel, t)

# Final postconditions.
requirements = {
'D088': ('notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md', [
'## Ámbitos de iteración y bloques de expresión',
'En una fuente cuya enumeración se construye como progresión',
'action Accumulate for values: Int [* ordered]',
'action Forward for mut total: Num',
'no depende de Q-018',
]),
'09': ('especificacion/09-nombres-y-anclas.md', ['  - D-088', '## Ámbitos de iteración y bloques de expresión', 'LocalSymbol(owner, kind, name, ordinal)']),
'CST': ('especificacion/sintaxis/cst-sin-perdidas.md', ['  - D-087\n  - D-088']),
'CST-AST': ('especificacion/sintaxis/cst-a-ast-superficial.md', ['  - D-087\n  - D-088']),
'cases': ('especificacion/sintaxis/casos/cst-ast.yaml', ['id: d088-step-cannot-see-iteration-binding', 'id: d088-filter-local-not-visible-in-body', 'runtime-zero-step-produces-progression-step-zero']),
}
for label, (rel, needles) in requirements.items():
    text = read(rel)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'{label}: missing {needle!r}')
if 'En esas fuentes puede omitirse `by`' in read('notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md'):
    raise SystemExit('ambiguous D088 antecedent remains')
for rel in ('notas/decisiones/ADR-033-claves-y-enumeracion-de-aliases.md','notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md'):
    if '    ...' in read(rel):
        raise SystemExit(f'ellipsis pseudocode remains in {rel}')
_,_,rz = case_block(read('especificacion/sintaxis/casos/cst-ast.yaml'),'d088-runtime-zero-step-action')
if 'expected_diagnostics:' in rz:
    raise SystemExit('runtime zero remains compile diagnostic')
print('D088_FINALIZE_FROM_126F_OK')
