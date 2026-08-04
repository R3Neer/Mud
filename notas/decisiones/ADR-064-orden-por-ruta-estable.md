---
id: D-064
title: "Orden por ruta estable"
status: vigente
date: 2026-07-30
supersedes: []
superseded-by: []
questions: []
affects:
  - "colecciones, familias, aliases, campos, tipos ordenables, normalización e iteración"
---
# ADR-064 — Orden por ruta estable

- Ampliada por: [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]]

- Modifica: [[notas/decisiones/ADR-038-familias-cerradas-de-valores|D-038]], [[notas/decisiones/ADR-039-colecciones-y-diccionarios|D-039]] y [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|D-057]]
- Documentos afectados: colecciones, familias, aliases, campos, tipos ordenables, normalización e iteración

## Contexto

`ordered by expression` permitía una expresión arbitraria como clave. Esa libertad dificultaba:

- Explicar el criterio como una propiedad del mundo.
- Garantizar que la clave permaneciera estable.
- Reconstruir y comparar criterios de orden.
- Evitar cálculos equivalentes escritos de formas distintas.

MUD favorece que las reglas del mundo nombren sus conceptos. Si un criterio requiere un cálculo, ese cálculo debe declararse primero como campo o dato calculado y la colección se ordena después por ese nombre.

## Decisión

### Forma de la clave

`ordered by` acepta exclusivamente una ruta no vacía de campos, componentes o datos asociados:

```mud
route: Terrain [* ordered by movementCost]
teams: Team [* ordered by captain.age]
```

No acepta operadores, llamadas, literales, cuantificadores ni otras expresiones arbitrarias.

Cada acceso intermedio debe ser singular y resolverse unívocamente sobre el elemento anterior. La ruta se interpreta desde cada miembro de la colección.

Cuando el criterio natural sea una fórmula, se le da un nombre:

```mud
priority := baseValue * rarityWeight
cards: Card [* ordered by priority]
```

En este ejemplo, `baseValue` y `rarityWeight` deben ser transitivamente inmutables.

### Tipo ordenable

El resultado final de la ruta debe poseer un orden semántico total. Una `thing` carece por sí misma de ese orden y no puede ser la clave final:

```mud
players: Player [* ordered by team]       # inválido si team es una thing
players: Player [* ordered by team.name]  # puede ser válido
```

Los tipos básicos, magnitudes, familias ordenadas y aliases solo son claves cuando sus reglas de tipo les conceden un orden total. La mera existencia de `<` o `>` en otro contexto no introduce automáticamente una clave válida.

### Estabilidad

Toda la ruta debe ser estable durante la vida de la colección:

- Ningún campo almacenado consultado puede ser exteriormente mutable.
- Un campo o dato calculado solo es válido si todas sus dependencias transitivas son estables.
- Una referencia singular intermedia a una `thing` no basta por ser inmutable si algún campo posterior puede cambiar.
- Ninguna lectura puede depender de azar, actividad cambiante ni estado cuya variación altere la clave.

La comprobación es transitiva. Si no puede demostrarse la estabilidad, la colección es inválida.

Cuando el miembro es una unión, la ruta debe existir y permanecer singular y estable sobre todas las alternativas alcanzables. Las claves finales deben elaborar hacia un único tipo común con orden total mediante, como máximo, una ampliación implícita única. La coincidencia representacional de aliases nominales no basta. Si una alternativa necesita adaptación, se declara un campo calculado común y se ordena por él.

### Empates

Dos ocurrencias con la misma clave conservan su orden relativo de inserción. La normalización por clave es estable y no introduce un desempate nominal, por identidad, por ancla ni por orden de declaración de una `family`.

Las ocurrencias repetidas de un mismo valor permanecen contiguas cuando así resulta de la clave y conservan su multiplicidad salvo `unique`.

El criterio completo de dos colecciones `ordered` solo es compatible cuando usan la misma ruta resuelta y el mismo orden del tipo final. La estabilidad relativa de empates forma parte del comportamiento de inserción, no de la identidad sintáctica de la ruta.

### Ausencias y órdenes personalizados

Una ruta que atraviese una cardinalidad opcional no es válida mientras MUD no defina una posición semántica para `empty` en esa clase de acceso.

MUD 1.0 no incorpora declaraciones personalizadas de comparación ni expresiones de orden. Tampoco infiere una comparación entre `thing`. Esta decisión no añade múltiples claves ni una cláusula de desempate: los empates usan inserción.

## Consecuencias

- El AST conserva una ruta resuelta, no una expresión general.
- El IR registra cada componente de la ruta, el tipo final y la prueba de estabilidad.
- Renombrar el cálculo que define una clave obliga a actualizar la ruta, pero concentra la semántica de la fórmula en un campo explicable.
- Los cambios de estado nunca reordenan implícitamente una colección almacenada.
- El orden de inserción continúa siendo observable solo entre claves iguales o en colecciones `ordered` sin clave canónica.

## Verificación

1. Ruta simple sobre dato de `family`.
2. Ruta anidada singular.
3. Rechazo de una expresión aritmética directa y aceptación del campo calculado equivalente.
4. Rechazo de una `thing` como clave final.
5. Clave final básica, magnitud, familia ordenada y alias lexicográfico.
6. Rechazo de campo mutable directo.
7. Rechazo de dependencia mutable transitiva o de acceso intermedio inestable.
8. Rechazo de ruta opcional sin orden de `empty`.
9. Conservación del orden de inserción entre empates.
10. Compatibilidad e incompatibilidad entre rutas resueltas.
