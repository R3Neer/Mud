---
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
