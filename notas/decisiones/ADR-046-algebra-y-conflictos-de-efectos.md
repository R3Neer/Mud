---
id: D-046
title: "Álgebra y conflictos de efectos"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-002"
  - "Q-006"
  - "Q-021"
  - "Q-046"
affects:
  - "efectos, raíz, ondas, conflictos"
---
# ADR-046 — Álgebra y conflictos de efectos

- Modificada por: [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]]
- Ampliada por: [[ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|D-080]]
- Modificada por: [[ADR-096-modulos-callables-look-message-y-activacion|D-096]].
- Preguntas relacionadas: Q-002, Q-006, Q-021, Q-046
- Documentos afectados: efectos, raíz, ondas, conflictos
- Modificada por: [[ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].

## Contexto

Los efectos concurrentes deben combinarse por significado, no por el orden accidental en que una implementación los encuentre.

## Decisión

El catálogo de efectos de MUD comprende:

- asignación `=`;
- suma y resta acumulativas;
- multiplicación acumulativa;
- unión, intersección, diferencia simétrica `unique` y diferencia acumulativas;
- `add` y `remove` sobre colecciones o propiedades;
- `create` y `destroy`;
- invocaciones de `action` o `subaction` dentro de cualquier contexto semántico `then`; la llamada incorpora secuencialmente sus efectos al delta privado activo conforme a D-096.

Cada `then` calcula un delta privado secuencial desde una instantánea común. La consolidación de deltas concurrentes es determinista.

Reglas mínimas:

| Efectos sobre el mismo destino | Resultado |
| --- | --- |
| asignaciones al mismo valor | compatibles, una asignación normalizada |
| asignaciones a valores distintos | conflicto |
| actualizaciones aditivas homogéneas | compatibles, suma de deltas antes de normalizar el destino |
| actualizaciones multiplicativas y divisivas homogéneas | compatibles, acumulación en numerador `P` y denominador `Q` |
| asignación con actualización aritmética | conflicto |
| actualización aditiva con multiplicativa o divisiva | compatibles; forma normal `((x + Δ) * P) / Q` |
| actualizaciones `|=` homogéneas sobre colecciones | unión de operandos |
| concatenaciones `|=` homogéneas sobre `Text` | compatibles solo con orden total determinado |
| actualizaciones `&=` homogéneas | intersección de operandos |
| actualizaciones `--=` homogéneas | suma de multiplicidades retiradas y truncado final |
| actualizaciones `^=` homogéneas sobre `unique` | diferencia simétrica por paridad |
| clases distintas de actualización de colección | conflicto |

Para efectos estructurales se aplican D-023, D-026 y D-054:

- las activaciones compatibles mediante `create` preceden a adiciones;
- las retiradas preceden a destrucciones;
- `create` y `destroy` coincidentes dejan el objetivo destruido al cerrar la onda;
- varias activaciones de una misma definición canónica ausente se consolidan idempotentemente;
- varias adiciones del mismo valor a una colección `unique` se consolidan idempotentemente en una sola presencia;
- cada `then` y toda consolidación posible deben preservar cardinalidades estáticamente.

Un conflicto verdadero que el compilador demuestra inevitable es error estático. Si demuestra que es posible pero no inevitable, emite warning. Si demuestra que los destinos no pueden coincidir o que los efectos consolidan de forma compatible, no emite diagnóstico de conflicto. Si un conflicto advertido o no decidible estáticamente se materializa durante una resolución, el runtime produce `failed` con rollback completo.

Los deltas aditivos dirigidos a un `Nat` son enteros firmados, aunque el valor del destino nunca pueda ser negativo. Para un valor inicial $n$ y deltas compatibles $\delta_i$, D-060 fija:

$$
n'=\max\left(0,n+\sum_i\delta_i\right).
$$

Dentro de un `then`, una lectura posterior observa la proyección saturada del valor inicial más su delta privado acumulado, pero esa proyección no recorta el delta pendiente. Los bloques no observan deltas privados ajenos.

## Consecuencias

- La semántica no depende del orden de reglas ni de hilos.
- La saturación de `Nat` no rompe la conmutatividad de las actualizaciones aditivas.
- Q-006 sigue abierta para las combinaciones restantes de colecciones, diccionarios, propiedades, ciclo de vida y solapamientos parciales.
- El análisis conservador especial de cardinalidad de D-026 prevalece sobre la regla general de diferir coincidencias indecidibles.

## Verificación

1. Casos compatibles e incompatibles de cada fila.
2. Igualdad bajo permutación de deltas.
3. Conflicto conocido estáticamente y conflicto dependiente de bindings.
4. Consolidación estructural con activación mediante `create`, adición, retirada y destrucción.
5. Rollback integral ante conflicto tardío.
6. Consolidación de deltas firmados sobre `Nat` antes de saturar.
7. Lectura secuencial proyectada sin recorte del delta privado.
