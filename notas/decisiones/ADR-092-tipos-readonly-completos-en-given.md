---
id: D-092
title: "Tipos de solo lectura completos en `given`"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "firmas given, diccionarios, capacidades, gramática, CST, AST y diagnósticos"
---
# ADR-092 — Tipos de solo lectura completos en `given`

- Modifica: [[ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]].
- Amplía: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].

## Contexto

`given` representa parámetros auxiliares de solo lectura. D-063 prohíbe tanto mutabilidad exterior como capacidad interior `mut`, pero la gramática concreta restringía además accidentalmente el tipo superior de un `given` a `union-type-expression`, de modo que una flecha de diccionario válida en campos o participantes `for` no podía escribirse como parámetro auxiliar.

## Decisión

Un `given` admite la misma familia estructural de tipos necesaria para representar valores auxiliares, incluidos diccionarios exactos y decisionales y cadenas de flechas:

```mud
given prices: Product -> Money
given policy: Person --> Permission
given nested: A -> B -> C
```

La aceptación de diccionarios **no** concede capacidad de escritura. Ningún `collection-specification` contenido en el tipo completo de un `given`, a ninguna profundidad, puede contener `mut`. Esta regla es recursiva y se aplica también a colecciones o diccionarios escondidos por paréntesis, productos o componentes anidados.

La sintaxis directa usa `given-type-expression`, `given-dictionary-type` y `given-dictionary-link`, cuyas especificaciones de colección son las variantes readonly ya existentes. Los paréntesis continúan reutilizando `type-expression` para conservar la gramática general; después de construir el AST superficial, la validación estática recorre toda la forma y rechaza cualquier `collection_spec.elements_mutable = true` alcanzable desde el `given`.

El AST superficial no introduce una jerarquía paralela de tipos: normaliza las flechas readonly a los mismos `ExactDictionaryType` y `DecisionDictionaryType`, fijando a `false` toda capacidad interior procedente de la sintaxis `given`. `readonly_value_shape` conserva el contrato exterior de la firma.

## Consecuencias

- `given prices: Product -> Money` es válido.
- `given prices: Product -> Money [ordered]` es válido.
- `given prices: Product -> Money [mut]` se rechaza sintácticamente en la forma directa.
- `given prices: (Product -> Money [mut])` también se rechaza, esta vez por validación recursiva de la forma normalizada.
- La corrección no convierte `given` en sujeto mutable ni altera el contrato de llamada de D-063.

## Verificación

1. Diccionario exacto y decisional en `given`.
2. Cadena de diccionarios anidados.
3. Cardinalidad, `unique` y `ordered` readonly en cada enlace.
4. Rechazo de `mut` directo.
5. Rechazo de `mut` oculto bajo paréntesis, producto o nivel anidado.
6. Normalización a los constructores de diccionario generales con capacidad interior falsa.
