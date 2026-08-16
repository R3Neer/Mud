---
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

## Contexto

D-047 hacía que `min` y `max` sobre una fuente con cero iteraciones produjeran un error específico de agregación vacía. El resto del modelo de valores trata normalmente la ausencia de resultado como cardinalidad cero: `empty` no es por sí mismo un fallo y el conflicto aparece solo si el contexto exige una forma que no admite esa cardinalidad.

Fabricar un valor extremo sentinela tampoco es válido porque no existe un mínimo o máximo universal para todos los tipos ordenables.

## Decisión

Si `min` o `max` recorren cero iteraciones, el resultado es `empty` con el tipo de valor que habría producido el cuerpo de la agregación. No se fabrica ningún valor extremo y la vacuidad no genera por sí sola `failed` ni un diagnóstico de agregación vacía.

El resultado de `min` y `max` contiene como máximo un valor. Si el análisis demuestra cero iteraciones, su cardinalidad exterior es `[0]`. Si la fuente puede estar vacía o no vacía, la forma conservadora es `[0..1]`. Si se demuestra al menos un candidato, se estrecha a `[1]`.

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
3. Una fuente demostrablemente vacía produce resultado `[0]`.
4. Una fuente posiblemente vacía produce resultado `[0..1]`.
5. Una fuente demostrablemente no vacía produce resultado `[1]`.
6. No existe diagnóstico específico de agregación extrema vacía.
7. `sum`, `count`, `exists` y `forall` conservan sus resultados sobre cero iteraciones.
