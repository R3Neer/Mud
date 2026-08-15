from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def read(rel): return (root / rel).read_text(encoding='utf-8')
def write(rel, text): (root / rel).write_text(text.rstrip('\n') + '\n', encoding='utf-8', newline='\n')
def exact(text, old, new, label, count=1):
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f'{label}: expected {count}, found {actual}')
    return text.replace(old, new, count)
def insert_after(text, anchor, addition, label):
    if addition.strip() in text:
        return text
    if text.count(anchor) != 1:
        raise SystemExit(f'{label}: anchor expected once, found {text.count(anchor)}')
    return text.replace(anchor, anchor + addition, 1)

# D-047: update the original normative body, not only the D-088 appendix.
rel = 'notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md'
t = read(rel)
t = insert_after(t,
    '- Ampliada por: [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]]\n',
    '- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]\n',
    'D047 relation')
t = exact(t,
'''for each item in source if predicate {
    ...
}

for each value in source by step if predicate {
    ...
}''',
'''for each item in source if predicate: {
    ...
}

for each value in source by step if predicate: {
    ...
}''', 'D047 colon examples')
t = exact(t,
'La pertenencia a `source` se toma como instantánea al comienzo del bucle. El filtro es puro, determinista y no puede depender de azar calculado.\n\n- En una fuente ordenada, las iteraciones son secuenciales y cada una observa los efectos de la anterior dentro del delta privado.\n- En una fuente no ordenada, las iteraciones leen la misma instantánea y sus deltas se consolidan como efectos simultáneos; un conflicto revierte la resolución completa.',
'La pertenencia a `source` se toma como instantánea al comienzo del bucle. El filtro es puro, determinista y no puede depender de azar calculado. En una fuente con orden semántico, cada filtro se evalúa inmediatamente antes de su iteración y observa los efectos secuenciales anteriores dentro del delta privado. En una fuente sin orden semántico, todos los filtros leen la misma instantánea inicial y los deltas de las iteraciones aceptadas se consolidan como efectos simultáneos; un conflicto revierte la resolución completa.',
'D047 filter semantics')
t = exact(t,
'- El orden descendente y la sintaxis consolidada de intervalos discontinuos siguen en Q-018.',
'- La sintaxis consolidada de intervalos discontinuos sigue en Q-018; el recorrido descendente explícito se expresa mediante `by` negativo conforme a D-088.',
'D047 consequence')
write(rel,t)

# D-071: the historical decision now uses the generalized representation.
rel='notas/decisiones/ADR-071-vinculaciones-locales-en-bloques-booleanos.md'
t=read(rel)
t=insert_after(t,
'- Modificada después por: [[ADR-079-diagnostico-exterior-de-reglas-always|D-079]]\n',
'- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]\n',
'D071 relation')
t=exact(t,
'''### Representación abstracta

El AST superficial normaliza toda condición a:

```text
BooleanBlock(locals, result)
```

El diagnóstico `otherwise` pertenece a la construcción propietaria y puede resolver los nombres de `locals`. Un `after` de test usa un bloque propio con locales comunes y una secuencia no vacía de `TestAssertion`.''',
'''### Representación abstracta

D-088 generaliza la representación común. El AST superficial normaliza toda condición a:

```text
ExpressionBlock(locals, result)
```

En los contextos definidos por esta decisión, el propietario exige que `result` cumpla el contrato booleano o temporal correspondiente. El diagnóstico `otherwise` pertenece a la construcción propietaria y puede resolver los nombres de `locals`. Un `after` de test usa un bloque propio con locales comunes y una secuencia no vacía de `TestAssertion`.''',
'D071 representation')
write(rel,t)

# D-075: remove the now-contradictory positive-only requirement from the main decision body.
rel='notas/decisiones/ADR-075-dominios-enumerables-all-y-valores-derivados.md'
t=read(rel)
t=insert_after(t,
'- Ampliada por: [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]]\n',
'- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]\n',
'D075 relation')
t=exact(t,
'`by` convierte un intervalo lineal en un dominio discreto. Su paso es estático, positivo, no nulo y compatible con el tipo o dimensión. `Num` usa aritmética racional exacta; un dominio `Rum` no se considera enumerable. La cardinalidad siempre usa corchetes y es independiente del dominio.',
'`by` convierte un intervalo lineal en un dominio discreto. Su paso es estático, firmado, no nulo, exacto y compatible con el tipo o dimensión. Un paso positivo se ancla en el límite inferior y uno negativo en el superior conforme a D-088. `Num` usa aritmética racional exacta; un dominio `Rum` no se considera enumerable. La cardinalidad siempre usa corchetes y es independiente del dominio.',
'D075 signed step')
write(rel,t)

# Traceability relations for the other directly modified ADRs.
relations = [
('notas/decisiones/ADR-057-gramatica-concreta-y-continuacion.md',
 '- Modificada finalmente por: [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]]\n',
 '- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]\n', 'D057 relation'),
('notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones.md',
 '- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]\n',
 '- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]\n', 'D081 relation'),
('notas/decisiones/ADR-082-cycle-como-modificador-de-dominio-de-punto.md',
 '- Pregunta relacionada: [[notas/preguntas/Q-018-intervalos-discontinuos|Q-018]].\n',
 '- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]\n', 'D082 relation'),
]
for rel,anchor,addition,label in relations:
    t=read(rel); t=insert_after(t,anchor,addition,label); write(rel,t)

# General grammar terminology: this body is no longer exclusive to clauses.
for rel in [
    'especificacion/gramatica/mud.ebnf',
    'especificacion/sintaxis/mud-syntax-kinds.yaml',
    'especificacion/sintaxis/cobertura-sintactica.yaml',
]:
    t=read(rel)
    t=t.replace('expression-clause-body','expression-body')
    t=t.replace('ExpressionClauseBodySyntax','ExpressionBodySyntax')
    write(rel,t)

# Explain the generalized body name in transformation prose if old wording exists.
rel='especificacion/sintaxis/cst-a-ast-superficial.md'
t=read(rel)
if 'expression-clause-body' in t:
    t=t.replace('expression-clause-body','expression-body')
write(rel,t)

# Tighten stale wording in 08 after BooleanBlock -> ExpressionBlock mechanical rename.
rel='especificacion/08-sintaxis-abstracta.md'
t=read(rel)
t=exact(t,
'- Activador `when` como bloque booleano.\n- Guardia `if` opcional como bloque booleano.',
'- Activador `when` como `ExpressionBlock` con contrato temporal.\n- Guardia `if` opcional como `ExpressionBlock` con contrato booleano.',
'08 rule block wording')
t=exact(t,
'`binding in source: predicate` posee `SelectionExpr`. Conserva la vinculación, la fuente y el predicado sin materializar la colección resultante. La vinculación solo introduce nombres dentro del predicado.',
'`binding in source [by step]: predicate` posee `SelectionExpr`. Conserva la vinculación, la fuente, el paso opcional y el predicado como `ExpressionBlock` sin materializar la colección resultante. La vinculación solo introduce nombres dentro del predicado.',
'08 selection summary')
t=exact(t,
'`exists`, `forall`, `count`, `sum`, `min` y `max` comparten `QuantifierExpr` con un enum propio.',
'`exists`, `forall`, `count`, `sum`, `min` y `max` comparten `QuantifierExpr` con un enum propio, un `step?` opcional y un `ExpressionBlock` como cuerpo.',
'08 quantifier summary')
write(rel,t)

# Postconditions.
checks = {
'notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md': [
    'for each item in source if predicate: {',
    'recorrido descendente explícito se expresa mediante `by` negativo',
],
'notas/decisiones/ADR-071-vinculaciones-locales-en-bloques-booleanos.md': ['ExpressionBlock(locals, result)'],
'notas/decisiones/ADR-075-dominios-enumerables-all-y-valores-derivados.md': ['Su paso es estático, firmado, no nulo, exacto'],
'especificacion/gramatica/mud.ebnf': ['expression-body'],
}
for rel,needles in checks.items():
    text=read(rel)
    for needle in needles:
        if needle not in text: raise SystemExit(f'missing {needle!r} in {rel}')
for rel in ['especificacion/gramatica/mud.ebnf','especificacion/sintaxis/mud-syntax-kinds.yaml','especificacion/sintaxis/cobertura-sintactica.yaml']:
    if 'expression-clause-body' in read(rel): raise SystemExit(f'stale expression-clause-body in {rel}')
print('D088_FIX_V3_OK')
