---
id: D-103
title: "Capacidad interior en valores derivados"
status: vigente
date: 2026-08-29
supersedes: []
superseded-by: []
questions: []
affects:
  - "colecciones, valores derivados, capacidad interior, identidad semántica y elaboración"
---
# ADR-103 — Capacidad interior en valores derivados

- Modifica: [[ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|D-019]], [[ADR-037-campos-y-dominios-declarativos|D-037]], [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]], [[ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]] y [[ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].
- Se apoya en la forma de colecciones derivadas de [[ADR-075-dominios-enumerables-all-y-valores-derivados|D-075]] y conserva sin cambios las reglas algebraicas de propagación de `mut` de [[ADR-039-colecciones-y-diccionarios|D-039]].

## Contexto

Todo valor MUD denota una colección. La capacidad interior `[mut]` es distinta de la mutabilidad exterior del lugar que almacena una colección y solo tiene efecto sobre `thing` miembros inmediatos. Las formas derivadas ya podían declarar cardinalidad y modificadores, pero coexistían formulaciones incompatibles sobre si una vista podía conceder capacidad interior ausente en su origen.

## Decisión

### Cardinalidad derivada

Una declaración derivada de cardinalidad `[n]` produce una única colección cuyo resultado debe tener exactamente `n` miembros después de las transformaciones aplicables. Una lista de expresiones separadas por comas construye los miembros exteriores de esa colección. Una expresión que produzca otra colección ocupa un miembro y no se aplana implícitamente.

### Capacidad interior

`[mut]` es una garantía de la colección, no mutabilidad exterior de su pertenencia. En una forma derivada actúa como obligación de capacidad: solo puede satisfacerse cuando el valor de origen ya proporciona la autoridad necesaria y las transformaciones conservan la identidad semántica de las mismas `thing`. La forma derivada nunca fabrica autoridad.

La capacidad se razona como garantía de la colección resultante, no como un mapa superficial de permisos por ocurrencia. Una transformación puede conservarla cuando el resultado sigue conteniendo las mismas identidades semánticas con autoridad suficiente. Filtrado, selección, `take`, indexación, secciones, deduplicación, reordenación y cambios de vista nominal son operaciones preservadoras cuando cumplen esa condición. Una proyección o cálculo que produce otros valores no conserva la capacidad de la entidad de origen.

### Álgebra de colecciones

Esta decisión no sustituye las reglas específicas de propagación de capacidad interior del álgebra de colecciones. `|`, `&`, `--` y `^` conservan exactamente las reglas fijadas por D-039, incluida la capacidad que una intersección puede obtener de uno de sus operandos y la que una diferencia conserva desde su operando izquierdo.

### Contenedores anidados

`[mut]` no es recursivo. Solo alcanza a las `thing` que sean miembros inmediatos de la colección calificada. No atraviesa aliases, estructuras ni otros contenedores y no concede mutabilidad exterior a una colección que aparezca como miembro de otra colección.

Cuando el tipo efectivo de miembro no contiene valores con estado modificable, `[mut]` sigue siendo legal conforme a la política general de capacidad inoperante, pero no habilita ninguna escritura adicional.

## Consecuencias

- Una colección derivada nunca posee mutabilidad exterior por declarar `[mut]`.
- Una derivada `[n mut]` combina una obligación de cardinalidad con una obligación de capacidad sobre sus `thing` miembros inmediatos.
- Una vista que conserve identidad semántica puede conservar capacidad ya disponible, pero no crearla.
- Una proyección o cálculo que produzca valores distintos pierde la capacidad de las entidades de origen.
- Las colecciones anidadas mantienen sus propios ejes de mutabilidad; el `[mut]` de la colección exterior no vuelve exteriormente mutable una colección interior.
- El álgebra de multiconjuntos mantiene sus reglas especializadas de D-039 y no se reduce a una regla binaria uniforme.

## Alternativas descartadas

Se descarta que una vista derivada conceda capacidad interior ausente en su fuente, que `[mut]` atraviese contenedores o se convierta en mutabilidad exterior de una colección anidada, y que esta decisión reemplace las reglas de propagación algebraica ya fijadas para operaciones de colecciones.

## Verificación

1. Una forma derivada `[mut]` solo se acepta cuando el origen y las transformaciones pueden garantizar la capacidad requerida.
2. Selección, `take`, indexación, secciones, deduplicación, ordenación y cambios de vista preservan capacidad cuando conservan identidad semántica y autoridad.
3. Proyecciones y cálculos que producen otros valores no fabrican ni conservan por ese hecho la capacidad de la `thing` de origen.
4. D-039 conserva literalmente sus reglas de propagación de `mut` para `|`, `&`, `--` y `^`.
5. `[mut]` no vuelve escribible una colección derivada ni una colección anidada que sea miembro de otra.
6. Una lista derivada conserva su cardinalidad exterior y no aplana colecciones usadas como miembros.
