# ADR-046 — Álgebra y conflictos de efectos

- Estado: Vigente como núcleo; matriz completa abierta
- Fecha: 2026-07-28
- Preguntas relacionadas: Q-002, Q-006, Q-021, Q-046
- Documentos afectados: efectos, raíz, ondas, conflictos

## Contexto

Los efectos concurrentes deben combinarse por significado, no por el orden accidental en que una implementación los encuentre.

## Decisión

El catálogo de efectos de MUD comprende:

- asignación `=`;
- suma y resta acumulativas;
- multiplicación acumulativa;
- `add` y `remove` sobre colecciones o propiedades;
- `create` y `destroy`;
- llamadas a acciones únicamente en acciones compuestas.

Cada `then` calcula un delta privado secuencial desde una instantánea común. La consolidación de deltas concurrentes es determinista.

Reglas mínimas:

| Efectos sobre el mismo destino | Resultado |
| --- | --- |
| asignaciones al mismo valor | compatibles, una asignación normalizada |
| asignaciones a valores distintos | conflicto |
| actualizaciones aditivas homogéneas | compatibles, suma de deltas |
| actualizaciones multiplicativas homogéneas | compatibles, producto de factores |
| asignación con actualización aritmética | conflicto |
| actualización aditiva con multiplicativa | conflicto |

Para efectos estructurales se aplican D-023, D-026 y D-054:

- las activaciones compatibles mediante `create` preceden a adiciones;
- las retiradas preceden a destrucciones;
- `create` y `destroy` coincidentes dejan el objetivo destruido al cerrar la onda;
- varias activaciones de una misma definición canónica ausente se consolidan idempotentemente;
- cada `then` y toda consolidación posible deben preservar cardinalidades estáticamente.

Un conflicto demostrable se rechaza estáticamente. Si la coincidencia de destinos solo puede conocerse durante una resolución, el runtime la detecta y produce `failed` con rollback completo.

## Consecuencias

- La semántica no depende del orden de reglas ni de hilos.
- La tabla anterior conserva el núcleo histórico, pero Q-006 sigue abierta para combinaciones de colecciones, diccionarios, propiedades, ciclo de vida y solapamientos parciales.
- El análisis conservador especial de cardinalidad de D-026 prevalece sobre la regla general de diferir coincidencias indecidibles.

## Verificación

1. Casos compatibles e incompatibles de cada fila.
2. Igualdad bajo permutación de deltas.
3. Conflicto conocido estáticamente y conflicto dependiente de bindings.
4. Consolidación estructural con activación mediante `create`, adición, retirada y destrucción.
5. Rollback integral ante conflicto tardío.
