---
id: D-048
title: "Azar reproducible y fallos"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-007"
  - "Q-032"
  - "Q-035"
  - "Q-058"
affects:
  - "expresiones, efectos, runtime, diagnósticos"
---
# ADR-048 — Azar reproducible y fallos

- Modificada por: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Preguntas relacionadas: Q-007, Q-032, Q-035, Q-058
- Documentos afectados: expresiones, efectos, runtime, diagnósticos

## Contexto

MUD admite azar, pero no permite que este o los errores introduzcan resultados dependientes de la plataforma ni conviertan consultas fallidas en falsedades.

## Decisión

MUD 1.0 expone una única forma sintáctica de muestreo:

```mud
Rand(source)
```

La fuente debe ser una colección o dominio muestreable. No existen todavía argumentos de pesos, distribuciones ni política local.

`Rand` puede intervenir de tres formas:

- campo almacenado inicializado aleatoriamente mediante `=`;
- campo calculado aleatorio mediante `:=`;
- muestreo dentro de un efecto.

Todo punto aleatorio posee identidad semántica y deriva su resultado de una semilla reproducible. Un campo calculado aleatorio conserva el mismo resultado dentro de una misma instantánea de evaluación. No puede leerse directamente desde reglas booleanas, dominios, `if`, `when`, `always` ni filtros de iteración.

`allowed` usa una rama concreta, sembrada y descartable. `eventually` cuantifica existencialmente sobre resultados de probabilidad positiva conforme a D-044.

Los resultados no finitos de `Rum`, la división por cero, una referencia no disponible, una operación fuera de dominio y cualquier efecto que no pueda producir un estado bien formado son fallos. Dentro de una acción real producen `failed` y rollback. Dentro de `allowed` se propagan como fallo de evaluación y no equivalen a falso.

Cada uno de esos fallos debe tener un diagnóstico humano `Text`. Cuando alcanza la frontera de una acción real, ese diagnóstico forma el `reason` obligatorio de su resultado `failed` conforme a D-061.

Los límites de recursos y defectos internos de una implementación no deben confundirse con un `failed` semántico. Q-007 debe fijar su representación externa y la frontera exacta entre ambas categorías.

## Consecuencias

- Una implementación no puede usar tiempo de máquina ni orden de evaluación como fuente semántica de azar.
- Las reglas de subsemillas, caché, reintentos y exposición de resultados siguen abiertas en Q-032.
- La portabilidad aritmética de `Rum` sigue en Q-058.
- La semántica de errores dentro de expresiones booleanas ordinarias, fuera de `allowed`, requiere una tabla normativa dentro de Q-007.

## Verificación

1. Repetición con la misma semilla y divergencia controlada con otra.
2. Estabilidad de un campo calculado aleatorio dentro de una instantánea.
3. Prohibición en condiciones y filtros.
4. Aislamiento del azar especulativo.
5. Rollback y propagación de fallos.
6. Aceptación exclusiva de `Rand(source)` y rechazo de firmas adicionales.
