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
- Ampliada por: [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]]
- Modificada por: [[ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].
- Preguntas relacionadas: Q-007, Q-032, Q-035, Q-058
- Documentos afectados: expresiones, efectos, runtime, diagnósticos

## Contexto

MUD admite azar, pero no permite que este o los errores introduzcan resultados dependientes de la plataforma ni conviertan consultas fallidas en falsedades.

## Decisión

MUD 1.0 expone una forma explícitamente aleatoria de muestreo:

```mud
Rand(source)
```

La fuente debe ser una colección o dominio muestreable. No existen todavía argumentos de pesos, distribuciones ni política local.

D-081 añade `take amount from source`. Sobre una fuente sin orden observable y con más ocurrencias que `amount`, `take` es un punto aleatorio reproducible aunque no escriba `Rand`: selecciona uniformemente y sin reemplazo. Posee la misma identidad, caché por instantánea y restricciones contextuales. Sobre una fuente ordenada, o cuando no existe elección real, `take` es determinista y no consume azar.

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
- Todo punto aleatorio posee identidad semántica estable y su elección debe derivarse de la semilla reproducible y de esa identidad sin depender del consumo secuencial accidental de un PRNG global. El algoritmo concreto de derivación o subsemillas es un detalle de implementación mientras preserve ese contrato. Q-032 mantiene abiertas las reglas de caché y reintentos y la exposición de resultados.
- La portabilidad aritmética de `Rum` sigue en Q-058.
- La semántica de errores dentro de expresiones booleanas ordinarias, fuera de `allowed`, requiere una tabla normativa dentro de Q-007.

## Verificación

1. Repetición con la misma semilla y divergencia controlada con otra.
2. Estabilidad de un campo calculado aleatorio dentro de una instantánea.
3. Prohibición en condiciones y filtros.
4. Aislamiento del azar especulativo.
5. Rollback y propagación de fallos.
6. Aceptación de `Rand(source)`, rechazo de firmas adicionales y clasificación contextual de `take` ordenado o estocástico.
