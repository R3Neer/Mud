---
id: D-095
title: "Extremos vacíos como ausencia ordinaria"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "min, max, cuantificadores, empty, cardinalidad, fallos y conformidad"
---
# ADR-095 — Extremos vacíos como ausencia ordinaria

- Modifica: [[ADR-047-cuantificadores-e-iteracion-finita|D-047]].
- Amplía: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]].
- Modificada por: [[ADR-101-bloques-de-valor-variables-locales-y-extremos|D-101]].

## Contexto

D-047 remitía `min` y `max` sobre fuente vacía a un supuesto error especial de agregación vacía que nunca fue definido. MUD ya usa `empty` para representar consultas parciales sin convertir la ausencia en fallo inmediato.

## Decisión

`min` y `max` sobre una fuente finita, enumerable y ordenada sin candidatos aceptados por su predicado producen `empty` con el tipo miembro de la fuente. Su forma de resultado admite cardinalidad `[0..1]`:

```text
min : T [0..1]
max : T [0..1]
```

Sobre una fuente con al menos un candidato aceptado producen exactamente un valor de tipo `T`: `min`, el primer testigo aceptado; `max`, el último, siempre según el orden semántico de la fuente. El `ExpressionBlock` solo filtra y no calcula un criterio de orden. La operación de extremo no introduce por sí misma `failed`.

Si el contexto receptor exige cardinalidad `[1]`, un resultado `empty` se somete a la comprobación ordinaria de tipo, dominio y cardinalidad y puede producir el mismo fallo normal que cualquier otra ausencia incompatible. No existe una categoría especial de «error de agregación extrema vacía».

La cardinalidad estática puede estrecharse cuando el compilador demuestra que existe al menos un candidato aceptado por el predicado; en ausencia de esa prueba debe conservar la posibilidad `[0..1]`.

## Consecuencias

- `min` y `max` se comportan como consultas parciales composicionales.
- una variable `[0..1]` puede recibir directamente un extremo ausente;
- una variable `[1]` no obliga a la operación de extremo a inventar un error propio: la incompatibilidad se resuelve en el contexto ordinario;
- desaparece la referencia normativa a un error de agregación vacía inexistente.

## Verificación

1. `min` y `max` sin testigos aceptados, incluida una fuente no vacía cuyo predicado rechaza todos sus miembros, producen `empty`.
2. La forma conservadora de resultado es `T [0..1]`.
3. Una recepción `[0..1]` acepta la ausencia.
4. Una recepción `[1]` falla por la regla ordinaria de cardinalidad, no por un diagnóstico especial del agregador.
5. Una prueba de que existe al menos un testigo aceptado puede estrechar el resultado a `[1]`.
