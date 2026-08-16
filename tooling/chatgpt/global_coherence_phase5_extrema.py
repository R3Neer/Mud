from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def r(p): return (ROOT/p).read_text(encoding='utf-8')
def w(p,t): (ROOT/p).write_text(t,encoding='utf-8',newline='\n')

adr='''---
id: D-093
title: "Extremos vacíos como ausencia ordinaria"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "min, max, agregaciones, empty, cardinalidad, fallos y conformidad"
---
# ADR-093 — Extremos vacíos como ausencia ordinaria

- Modifica: [[ADR-047-cuantificadores-e-iteracion-finita|D-047]].
- Amplía: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].

## Contexto

D-047 remitía `min` y `max` sobre fuente vacía a un supuesto error especial de agregación vacía que nunca fue definido. MUD ya usa `empty` para representar consultas parciales sin convertir la ausencia en fallo inmediato.

## Decisión

`min` y `max` sobre una fuente finita y enumerable sin candidatos producen `empty` con el tipo elemento de la agregación. Su forma de resultado admite cardinalidad `[0..1]`:

```text
min : T [0..1]
max : T [0..1]
```

Sobre una fuente con al menos un candidato producen exactamente un valor de tipo `T`, seleccionado conforme al orden admitido por el cuerpo del agregador. La operación de extremo no introduce por sí misma `failed`.

Si el contexto receptor exige cardinalidad `[1]`, un resultado `empty` se somete a la comprobación ordinaria de tipo, dominio y cardinalidad y puede producir el mismo fallo normal que cualquier otra ausencia incompatible. No existe una categoría especial de «error de agregación extrema vacía».

La cardinalidad estática puede estrecharse cuando el compilador demuestra que la fuente contiene al menos un candidato; en ausencia de esa prueba debe conservar la posibilidad `[0..1]`.

## Consecuencias

- `min` y `max` se comportan como consultas parciales composicionales.
- una variable `[0..1]` puede recibir directamente un extremo ausente;
- una variable `[1]` no obliga al agregador a inventar un error propio: la incompatibilidad se resuelve en el contexto ordinario;
- desaparece la referencia normativa a un error de agregación vacía inexistente.

## Verificación

1. `min` y `max` sobre fuente vacía producen `empty`.
2. La forma conservadora de resultado es `T [0..1]`.
3. Una recepción `[0..1]` acepta la ausencia.
4. Una recepción `[1]` falla por la regla ordinaria de cardinalidad, no por un diagnóstico especial del agregador.
5. Una fuente demostrablemente no vacía puede estrechar el resultado a `[1]`.
'''
p=ROOT/'notas/decisiones/ADR-093-extremos-vacios-como-ausencia-ordinaria.md'
if p.exists(): raise SystemExit('D-093 exists')
p.write_text(adr,encoding='utf-8',newline='\n')

p='notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md'; t=r(p)
marker='- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]\n'
if marker not in t: raise SystemExit('D047 marker')
t=t.replace(marker,marker+'- Modificada por: [[ADR-093-extremos-vacios-como-ausencia-ordinaria|D-093]]\n',1)
old='La fuente debe ser finita y enumerable. La evaluación es pura; `min` y `max` sobre una fuente vacía producen el error definido para agregación vacía, no un valor inventado.'
new='La fuente debe ser finita y enumerable. La evaluación es pura. `min` y `max` son consultas parciales: sobre una fuente vacía producen `empty` con forma de resultado `T [0..1]`; sobre una fuente no vacía producen un valor de tipo `T`. La ausencia solo falla después si el contexto receptor no admite cardinalidad cero, conforme a D-093.'
if old not in t: raise SystemExit('D047 extrema paragraph')
t=t.replace(old,new,1)
t=t.replace('2. Error de agregación extrema vacía.','2. `min` y `max` vacíos producen `empty` y su incompatibilidad posterior usa las reglas ordinarias de cardinalidad.',1)
w(p,t)

p='notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md'; t=r(p)
if 'D-093' not in t:
    marker='- Conserva: [[ADR-034-number-exacto-y-rumber-binary64|D-034]], [[ADR-040-semantica-numerica-basica-restante|D-040]] y la prohibición de azar en filtros de [[ADR-048-azar-reproducible-y-fallos|D-048]].\n'
    if marker not in t: raise SystemExit('D088 marker')
    t=t.replace(marker,marker+'- Modificada por: [[ADR-093-extremos-vacios-como-ausencia-ordinaria|D-093]] en la forma de resultado de `min` y `max` sobre ausencia.\n',1)
needle='`by` de progresión se admite también en selección y en `exists`, `forall`, `count`, `sum`, `min` y `max`, siempre que la fuente ofrezca progresión mediante diferencia. No significa stride sobre una colección arbitraria.'
if needle in t:
    t=t.replace(needle,needle+' La semántica de ausencia de `min` y `max` es la de D-093: ningún candidato produce `empty [0..1]`.',1)
w(p,t)

# 08 records result shape without inventing a surface special node.
p='especificacion/08-sintaxis-abstracta.md'; t=r(p)
if '  - D-093\n' not in t:
    t=t.replace('  - D-092\n','  - D-092\n  - D-093\n',1)
marker='## Magnitudes\n'
addition='''## Resultado de `min` y `max`

`QuantifierExpr(Min|Max, ...)` no necesita un constructor superficial especial para ausencia. La elaboración asigna al resultado el tipo elemento y una cardinalidad conservadora `[0..1]`; un recorrido sin candidatos produce el valor ordinario `empty`. Solo un contexto posterior incompatible con cero elementos introduce el fallo normal de cardinalidad.

'''
if addition.strip() not in t:
    if marker not in t: raise SystemExit('08 marker')
    t=t.replace(marker,addition+marker,1)
w(p,t)

# Cases are semantic expectations, not parse diagnostics.
p='especificacion/sintaxis/casos/cst-ast.yaml'; t=r(p)
cases='''- id: min-empty-is-empty
  category: quantifier-semantics
  source: "min x in empty: x"
  cst_root: ExpressionSyntax
  ast: QuantifierExpr(Min, source=empty)
  semantic_expectations:
  - result-cardinality-0-or-1
  - empty-source-produces-empty
  produces_ast: true
- id: max-empty-is-empty
  category: quantifier-semantics
  source: "max x in empty: x"
  cst_root: ExpressionSyntax
  ast: QuantifierExpr(Max, source=empty)
  semantic_expectations:
  - result-cardinality-0-or-1
  - empty-source-produces-empty
  produces_ast: true
'''
if 'id: min-empty-is-empty' not in t:
    t=t.rstrip()+'\n'+cases
w(p,t)
print('PHASE5_EXTREMA_OK')
