---
id: D-077
title: "Destrucción condicionada por cardinalidad y diagnóstico de transición"
status: vigente
date: 2026-08-03
supersedes: []
superseded-by: []
questions:
  - "Q-049"
affects:
  - "ciclo de vida, colecciones, efectos, resultados y `otherwise`"
---
# ADR-077 — Destrucción condicionada por cardinalidad y diagnóstico de transición

## Contexto

Ocultar miembros destruidos y permitir que la cardinalidad efectiva diverja de la declarada rompe las garantías de consumidores posteriores. Cambiar dinámicamente el tipo o propagar colecciones degradadas tampoco es aceptable.

## Decisión

`destroy c` calcula la transición completa y valida todas las propiedades afectadas. Si retirar `c` de la proyección efectiva infringe una cardinalidad o dominio, la transición devuelve `failed` y se revierte por completo:

```mud
members: Person [2] = Alice, Bob

destroy Bob # failed
```

No existe un estado confirmado cuya cardinalidad efectiva contradiga la declaración.

Cuando la retirada es válida, una relación sin capacidad `mut` conserva latentemente la pertenencia y `create c` la restaura. Una relación `mut` elimina la pertenencia almacenada y `create c` no la recompone. `remove` autorizado elimina también una pertenencia latente. Toda restauración de `create` se valida de forma atómica y puede devolver `failed`.

Destruir el tipo declarado de una propiedad mantiene la suspensión estructural de D-021: la propiedad completa y su carga permanecen almacenadas. Esta suspensión se distingue de destruir una identidad que aparece como valor.

### `otherwise` de transición

Un bloque `then` puede terminar con un diagnóstico `otherwise`:

```mud
then {
    destroy Bob
}
otherwise "Bob is still required by {team}"
```

El texto se evalúa perezosamente solo cuando la transición atómica resulta `failed`. No recupera, no ejecuta una rama alternativa y no convierte `failed` en `rejected`. El diagnóstico debe identificar además la propiedad, cardinalidad o dominio que bloqueó la operación.

## Consecuencias

- D-021 deja de descartar que `mut` afecte a la retirada de miembros.
- La comprobación de D-026 incluye efectos de ciclo de vida y su consolidación.
- No hay cascadas de estados cardinalmente degradados: hay commit válido o rollback.
- `otherwise` pertenece al resultado del `then` completo, no a una instrucción individual.

## Verificación

1. `destroy` bloqueado por cardinalidad exacta.
2. Retirada válida dentro de un rango.
3. Restauración inmutable y retirada permanente `mut`.
4. Rollback con varias colecciones afectadas.
5. Restauración de `create` que excede un máximo.
6. Distinción entre identidad destruida y tipo destruido.
7. Evaluación perezosa de `otherwise` y diagnóstico de la causa.
