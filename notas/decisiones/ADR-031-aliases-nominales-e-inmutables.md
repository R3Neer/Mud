---
id: D-031
title: "Aliases nominales, inmutables y sin ciclo de vida"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-057"
affects:
  - "futuro `12-aliases.md`, futuro `25-efectos.md`"
---
# ADR-031 — Aliases nominales, inmutables y sin ciclo de vida

- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]] y [[ADR-098-rutas-asignables-y-write-back-de-aliases|D-098]]
- Ampliada por: [[ADR-074-uniones-nominales-y-estrechamiento|D-074]]

- Relacionada con: [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]], [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]]
- Resuelve: [[notas/preguntas/Q-057-capacidad-interior-dentro-de-valores-de-alias|Q-057]]
- Documentos afectados: futuro `12-aliases.md`, futuro `25-efectos.md`

## Contexto

Un alias debe proporcionar identidad nominal a valores, no identidad runtime ni estado mutable. Por tanto, su declaración es estática y no participa en el ciclo de vida del mundo.

## Decisión

### Definición de tipo

Un alias definido mediante una expresión de tipo usa `:=`:

```mud
alias PlayerName :=
    Text

alias Board :=
    Square -> Piece [0..32 ordered]

alias Path :=
    Position [* ordered]
```

En este contexto, `:=` introduce una definición estática de tipo. No declara un campo calculado ni una evaluación runtime.

Un alias estructural declara un bloque ordenado de componentes:

```mud
alias Square {
    file: File
    rank: Rank
}

alias Pagination {
    page: Nat = 1
    size: Nat = 20
}
```

Cada componente:

1. Forma parte obligatoria de todo valor construido.
2. Ocupa una posición semántica según el orden de declaración.
3. Forma parte de la estructura del alias.
4. Puede declarar un dominio.
5. No puede declarar mutabilidad exterior: la forma `mut nombre: tipo` no existe para componentes.
6. Puede declarar capacidad interior `[mut]` sobre las `thing` contenidas directamente por una colección.
7. Puede declarar un valor predeterminado mediante `=`.

El predeterminado explícito debe ser una expresión pura evaluable estáticamente y satisfacer el tipo, dominio y especificación de colección del componente. El valor predeterminado de un alias estructural se obtiene componente a componente:

1. Predeterminado explícito del componente, si existe.
2. Predeterminado del tipo efectivo del componente conforme a D-017, en otro caso.

Los predeterminados no eliminan componentes de la representación. Después de construir un valor, todos están presentes y participan normalmente en igualdad y orden.

### Nominalidad

Todo alias introduce un tipo nominal nuevo. Dos aliases distintos no son intercambiables automáticamente aunque sus representaciones normalizadas coincidan:

```mud
alias PlayerName :=
    Text

alias CityName :=
    Text
```

`PlayerName`, `CityName` y `Text` son tres tipos diferentes. La representación común permite una conversión nominal explícita conforme a D-032, no una asignación implícita.

### Inmutabilidad

Un valor de alias es inmutable. Una vinculación que contiene solo ese valor no puede actualizar uno de sus componentes:

```mud
square := Piece.square
square.file = B # inválido
```

Un lugar con mutabilidad exterior puede sustituir el valor completo y una ruta asignable puede atravesar componentes almacenados del alias mediante reconstrucción y write-back:

```mud
thing Piece {
    mut square: Square
}

Piece.square = (B, Four)
Piece.square.file = C
```

La segunda escritura no muta el valor `Square`: construye otro `Square` del mismo tipo nominal exacto, conserva los componentes no modificados y sustituye el valor almacenado de `Piece.square`. La misma reconstrucción puede propagarse a través de aliases anidados e indexaciones de diccionarios exactos mientras exista una ruta de retorno a un lugar escribible. Los campos derivados se recalculan y no son destinos de write-back.

El `mut` de la especificación de colección de un componente concede capacidad interior sobre las `thing` contenidas directamente por esa colección. No vuelve reemplazable la colección ni convierte por sí solo un valor de alias en lugar escribible: la reconstrucción exige una raíz con mutabilidad exterior suficiente. La capacidad tampoco atraviesa implícitamente otro alias o contenedor anidado; cada nivel que deba concederla debe declararla expresamente cuando la operación ejercida sea capacidad interior.

### Ausencia de identidad runtime

La declaración posee un ancla estática para resolución y nominalidad, pero sus valores no poseen identidad runtime. Un alias:

- No puede aparecer como objetivo de `create`.
- No puede aparecer como objetivo de `destroy`.
- No puede ser `abstract`.
- Participa en especialización nominal acíclica conforme a D-084, sin adquirir identidad ni ciclo de vida runtime.
- No mantiene estado mutable propio.

Los valores se comparan por tipo nominal y contenido. La declaración existe durante todo el programa bien formado y no forma parte de la proyección de actividad del mundo.

## Consecuencias

- D-021 gobierna el ciclo de vida de `thing` y reglas; los aliases no pertenecen a esas categorías.
- D-054 exige definiciones canónicas de primer nivel y reserva `create Nombre` para activar `thing` y reglas; los aliases quedan fuera de ese ciclo de vida.
- El AST solo necesita `AliasDecl`; elimina `DefineAndCreateAlias` y cualquier efecto `create`/`destroy` de alias.
- El runtime no necesita marcas de actividad, almacenamiento latente ni restauración para aliases.
- Las propiedades y declaraciones que usan un alias no pueden quedar suspendidas por inactividad de ese alias.
- La inmutabilidad del contenedor alias es compatible con autoridad explícita para modificar las `thing` alcanzadas mediante un componente colectivo `[mut]`.

## Verificación futura

1. Alias simple mediante `:=`.
2. Alias de colección y diccionario mediante `:=`.
3. Alias estructural con componentes ordenados.
4. Componente con predeterminado explícito y predeterminado procedente de su tipo.
5. Rechazo de predeterminado impuro, no estático o fuera de tipo, dominio o colección.
6. Rechazo de `mut` exterior y aceptación de `[mut]` interior en un componente colectivo de `thing`.
7. Rechazo de actualización parcial sobre una local alias y aceptación de reconstrucción/write-back cuando la ruta termina en almacenamiento escribible.
8. Sustitución completa desde un campo mutable y conservación de los componentes no modificados durante un write-back parcial.
9. Rechazo de `create`, `destroy` y `abstract`; aceptación de `as` e `is` como especialización nominal conforme a D-084.

## Modificación por D-084

Los aliases pueden declarar especialización simple o múltiple. Los nominales raíz conservan `:= tipo`; los descendientes heredan una representación efectiva común. Los estructurales heredan componentes y campos derivados. Un descendiente puede sobrescribir el predeterminado de un componente almacenado heredado y refinar contratos heredados cuando el refinamiento fortalece garantías sin retirar capacidades observables o de escritura: la mutabilidad exterior no cambia, la capacidad interior puede fortalecerse de ausencia de `[mut]` a presencia de `[mut]` y tipo, dominio, cardinalidad, `unique` y orden se rigen por sustituibilidad. Los campos derivados heredados conservan su expresión definitoria y solo pueden fortalecer el contrato de su resultado. Esta modificación no introduce identidad runtime ni mutabilidad del valor alias.
