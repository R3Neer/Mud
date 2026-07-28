# ADR-038 — Familias cerradas de valores

- Estado: Vigente
- Fecha: 2026-07-28
- Pregunta relacionada: Q-024
- Documentos afectados: futuro `13-familias-cerradas.md`

## Decisión

MUD admite `family` como declaración nominal de primer nivel independiente de `thing`:

```mud
family Color {
    Red,
    Green,
    Blue
}
```

`ordered` es una palabra contextual que, situada inmediatamente antes de `family`, añade orden semántico:

```mud
ordered family Severity {
    Low,
    Medium,
    High,
    Critical
}
```

La declaración introduce un tipo nominal finito y un ancla estática `family::*`. Cada miembro:

- Pertenece nominalmente a su familia.
- Es un valor nominal, no una identidad de `thing`.
- Carece de estado mutable y de ciclo de vida runtime.
- No admite `create`, `destroy`, `as` ni consultas `is`.
- Se enumera en el orden de declaración.
- Es igual a otro miembro si y solo si ambos pertenecen a la misma familia nominal y tienen el mismo nombre.
- Solo admite operadores de orden si la declaración usa `ordered family`.

El orden de declaración es canónico para enumerar cualquier `family`, pero solo forma parte de las relaciones `<`, `<=`, `>` y `>=` cuando aparece `ordered`.

Las declaraciones `family` no participan en especialización ni pueden heredar de otras familias. Una jerarquía abierta de `thing` abstractas y especializaciones no es una familia cerrada y no adquiere enumerabilidad automática.

### Datos asociados

Una `family` puede declarar un esquema uniforme de datos inmutables. Las declaraciones del esquema aparecen directamente en el bloque de la familia, antes de los miembros, sin un subbloque `data`:

```mud
family Terrain {
    movementCost: Natural = 1
    passable: Bool = true

    Plain,
    Forest {
        movementCost = 2
    },
    Mountain {
        movementCost = 4
    },
    Water {
        movementCost = 0
        passable = false
    }
}
```

La forma de una declaración de dato es la de un campo almacenado sin `mut` ni `:=`:

```text
nombre : tipo [in dominio] [especificación-de-colección] [= predeterminado]
```

Todos los miembros comparten exactamente ese esquema. El subbloque opcional de un miembro contiene únicamente asignaciones que sustituyen sus valores predeterminados; no puede declarar datos nuevos, omitir el nombre del dato asignado ni modificar su tipo, dominio o especificación de colección.

Para cada dato de cada miembro, el valor se obtiene en este orden:

1. Asignación explícita en el subbloque del miembro.
2. Predeterminado explícito de la declaración del dato.
3. Predeterminado del tipo efectivo conforme a D-017.

Por tanto, un miembro puede omitir un dato siempre que su valor predeterminado pueda determinarse estáticamente. En particular, un dato `Natural` sin predeterminado explícito obtiene `0`. Aunque la omisión sea válida, se recomienda escribir explícitamente los valores cuyo significado sea importante para comprender el modelo.

Los predeterminados y las asignaciones de miembro deben ser expresiones puras evaluables estáticamente y satisfacer tipo, dominio y colección. Los datos asociados:

- Son inmutables.
- No poseen identidad ni ciclo de vida propios.
- Se consultan como propiedades del valor de familia, por ejemplo `terrain.movementCost`.
- No alteran la identidad ni la igualdad del miembro: siguen dependiendo de la familia nominal y el nombre del miembro.

La selección del miembro predeterminado de la propia familia continúa perteneciendo a Q-047.

## Verificación futura

1. Familia cerrada ordenada y no ordenada.
2. Igualdad entre valores de la misma y distinta familia.
3. Enumeración canónica.
4. Rechazo de orden en una familia no ordenada.
5. Rechazo de `create`, `destroy`, `as` e `is`.
6. Distinción respecto de una jerarquía abierta de `thing`.
7. Formación y estabilidad de anclas `family::*`.
8. Esquema uniforme de datos y rechazo de datos específicos no declarados.
9. Precedencia entre valor de miembro, predeterminado explícito y predeterminado de tipo.
10. Inmutabilidad y acceso a datos asociados.
