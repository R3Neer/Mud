---
id: D-038
title: "Familias cerradas de valores"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-024"
  - "Q-047"
affects:
  - "futuro `13-familias-cerradas.md`"
---
# ADR-038 — Familias cerradas de valores

- Ampliada por: [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]]
- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]

- Modificada por: [[notas/decisiones/ADR-064-orden-por-ruta-estable|D-064]]
- Modificada además por: [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]]
- Modificada por: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
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

`ordered` es una palabra reservada que, situada inmediatamente antes de `family`, añade orden semántico:

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

Cada miembro posee un `name: Text` intrínseco cuyo predeterminado es su nombre nominal declarado. Puede sobrescribirse mediante `name = "..."` sin cambiar identidad, igualdad, ancla ni orden. Una sobrescritura idéntica recibe sugerencia de eliminación. En una plantilla `Text`, interpolar un miembro produce su `name` efectivo.

El orden de declaración es canónico para enumerar cualquier `family`, pero solo forma parte de las relaciones `<`, `<=`, `>` y `>=` cuando aparece `ordered`.

Las declaraciones `family` no participan en especialización ni pueden heredar de otras familias. Una jerarquía abierta de `thing` abstractas y especializaciones no es una familia cerrada y no adquiere enumerabilidad automática.

### Datos asociados

Una `family` puede declarar un esquema uniforme de datos inmutables. Las declaraciones del esquema aparecen directamente en el bloque de la familia, antes de los miembros, sin un subbloque `data`:

```mud
family Terrain {
    movementCost: Nat = 1
    passable: Bool = true
    costly := movementCost >= 3

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

Un dato asociado puede ser almacenado o calculado. El dato almacenado no admite `mut`:

```text
nombre : tipo [in dominio] [especificación-de-colección] [= predeterminado]
```

El dato calculado reutiliza la forma general definida por D-037:

```text
nombre [: tipo] := expresión
```

La anotación de tipo de un dato calculado es opcional. Si se omite, el compilador debe inferir un único tipo estático; si no puede hacerlo, la declaración es inválida. Un dato calculado no admite `mut`, `in`, especificación de colección, predeterminado ni almacenamiento propio: su forma y su valor proceden de la expresión.

Todos los miembros comparten exactamente ese esquema. El subbloque opcional de un miembro contiene únicamente asignaciones que sustituyen los valores predeterminados de datos almacenados; no puede declarar datos nuevos, omitir el nombre del dato asignado, modificar su tipo, dominio o especificación de colección ni asignar un dato calculado.

Para cada dato de cada miembro, el valor se obtiene en este orden:

1. Asignación explícita en el subbloque del miembro.
2. Predeterminado explícito de la declaración del dato.
3. Predeterminado del tipo efectivo conforme a D-017.

Por tanto, un miembro puede omitir un dato almacenado siempre que su valor predeterminado pueda determinarse estáticamente. En particular, un dato `Nat` sin predeterminado explícito obtiene `0`. Aunque la omisión sea válida, se recomienda escribir explícitamente los valores cuyo significado sea importante para comprender el modelo.

Después de resolver los datos almacenados de un miembro, sus datos calculados se evalúan para ese miembro. La expresión puede consultar mediante nombres no cualificados otros datos asociados de la misma familia, incluidos datos calculados declarados antes o después. Las dependencias entre datos calculados deben ser acíclicas y resolverse sin depender del orden textual de declaración. Los predeterminados y las asignaciones de miembro deben ser expresiones estáticas cerradas conforme a D-066. Los datos calculados también se evalúan estáticamente por miembro y deben ser puros, además de satisfacer los tipos y, donde correspondan, el dominio y la colección.

En el ejemplo, `Mountain.costly` es `true`, mientras que `Plain.costly` es `false`. Los datos asociados, almacenados o calculados:

- Son inmutables.
- No poseen identidad ni ciclo de vida propios.
- Se consultan como propiedades del valor de familia, por ejemplo `terrain.movementCost`.
- No alteran la identidad ni la igualdad del miembro: siguen dependiendo de la familia nominal y el nombre del miembro.

### Datos asociados como clave de colección

Una colección de miembros de una `ordered family` puede usar `ordered by ruta`. La ruta parte de cada miembro y selecciona un dato asociado estable:

```mud
ordered family Terrain {
    movementCost: Nat = 1

    Plain,
    Forest {
        movementCost = 2
    },
    Mountain {
        movementCost = 4
    }
}

route: Terrain [* ordered by movementCost]
```

Dentro de `ordered by movementCost`, `movementCost` designa el dato del miembro de `Terrain` que se está ordenando. El resultado debe poseer un orden semántico total. Los datos de una familia son inmutables, por lo que esta ruta es estable. Una fórmula debe declararse primero como dato calculado y ordenarse después por su nombre; `ordered by` no contiene expresiones arbitrarias.

`ordered by` sustituye el orden de declaración como criterio principal de esa colección, pero no cambia los operadores de comparación propios de la familia. Cuando dos ocurrencias producen la misma clave, conservan su orden relativo de inserción. Las ocurrencias repetidas conservan su multiplicidad salvo que la colección sea también `unique`.

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
11. Colección de `ordered family` ordenada por una ruta de datos asociados, con empates por inserción y conservación de multiplicidad.
12. Inferencia de tipo, evaluación por miembro y dependencias acíclicas de datos calculados.
13. Rechazo de asignaciones de miembro dirigidas a datos calculados.
14. Renderización nominal de un miembro y acceso explícito a un dato `Text` alternativo.
