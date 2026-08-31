---
id: D-047
title: "Cuantificadores e iteración finita"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-018"
  - "Q-028"
  - "Q-029"
affects:
  - "expresiones, intervalos, iteración"
---
# ADR-047 — Cuantificadores e iteración finita

- Modificada por: [[ADR-101-bloques-de-valor-variables-locales-y-extremos|D-101]].

- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Ampliada por: [[ADR-075-dominios-enumerables-all-y-valores-derivados|D-075]]
- Ampliada por: [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]]
- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]
- Modificada por: [[ADR-095-extremos-vacios-como-ausencia-ordinaria|D-095]]

- Preguntas relacionadas: Q-018, Q-028, Q-029
- Documentos afectados: expresiones, intervalos, iteración

## Contexto

MUD necesita recorrer conjuntos de dominio sin introducir bucles generales cuya terminación o resultado dependan del contenedor interno.

## Decisión

Las expresiones admiten:

```mud
exists x in source : predicate
forall x in source : predicate
count x in source : predicate
min x in source : predicate
max x in source : predicate
```

La fuente debe ser finita y enumerable. La evaluación es pura. Los cinco cuerpos son predicados booleanos. `min` y `max` devuelven el primer o último testigo aceptado según el orden semántico de la fuente; requieren una fuente con orden utilizable. Son consultas parciales: sin testigos aceptados producen `empty` con cardinalidad `[0..1]` y, en otro caso, un valor del tipo de miembro de la fuente. La ausencia solo falla después si el contexto receptor no admite cardinalidad cero, conforme a D-095.

D-081 añade una selección pura que devuelve los testigos en lugar de consumirlos:

```mud
item in source : predicate
```

Comparte la obligación de finitud y enumerabilidad, pero produce la subcolección aceptada y puede alimentar después un cuantificador, `take` u otra expresión.

El `for each` ejecutable aparece dentro de un `then`; D-101 admite además `LocalForEach` dentro de `ValueBlock`, con `LocalStatementBlock` y sin efectos exteriores. La forma ejecutable conserva:

```mud
for each item in source if predicate :
    iterations += 1

for each value in source by step if predicate :
    iterations += 1
```

La cláusula `by` opcional precede siempre a `if`. Un diccionario puede vincular un par mediante `(key, value)`.

La pertenencia a `source` se toma como instantánea al comienzo del bucle. El filtro es puro, determinista y no puede depender de azar calculado. En una fuente con orden semántico, cada filtro se evalúa inmediatamente antes de su iteración y observa los efectos secuenciales anteriores dentro del delta privado. En una fuente sin orden semántico, todos los filtros leen la misma instantánea inicial y los deltas de las iteraciones aceptadas se consolidan como efectos simultáneos; un conflicto revierte la resolución completa.

La enumeración canónica procede del tipo: orden declarado de una familia cerrada, producto lexicográfico de un alias estructural, orden del diccionario o colección, u orden ascendente de un intervalo cuando se materializa canónicamente. El orden de recorrido de una progresión explícita es independiente: `by` negativo recorre desde el límite superior hacia valores menores conforme a D-088 sin cambiar el orden canónico del tipo o dominio.

Cuando una enumeración se obtiene mediante progresión, los intervalos finitos de `Nat` e `Int` usan paso predeterminado uno y `Money`, paso `0.01`. Las fuentes que ya poseen enumeración propia no necesitan fabricar un paso. Un intervalo general de `Num` requiere paso exacto explícito. Los intervalos de `Rum` nunca son enumerables. El último valor es el último punto generado que pertenece al intervalo; no se fuerza la inclusión del extremo.

Un intervalo discontinuo se normaliza en segmentos disjuntos y se recorre segmento a segmento, reiniciando el paso en cada segmento. Un intervalo vacío produce cero iteraciones.

## Consecuencias

- No existe iteración implícita sobre dominios infinitos o no enumerables.
- La sintaxis consolidada de intervalos discontinuos sigue en Q-018; el recorrido descendente explícito se expresa mediante `by` negativo conforme a D-088.
- Las pruebas de finitud y terminación pueden ser conservadoras.

## Verificación

1. Cuantificadores sobre fuente finita, incluidos extremos filtrados sobre fuente ordenada.
2. `min` y `max` vacíos producen `empty` y su incompatibilidad posterior usa las reglas ordinarias de cardinalidad.
3. Diferencia observable entre bucle ordenado y no ordenado.
4. Intervalos abiertos, cerrados, discontinuos y con paso.
5. Rechazo de una enumeración `Rum` o infinita.
6. Orden sintáctico `by` antes de `if` y vinculación de pares de diccionario.

## Modificación por D-088

D-088 generaliza `by` a diferencias firmadas compatibles, evaluadas una vez, y distingue filtros ordenados (ven efectos secuenciales anteriores) de no ordenados (leen la instantánea inicial). Los cinco cuantificadores admiten `by` cuando la fuente define progresión y bloques de expresión booleanos. `Rum` sigue sin ser enumerable y los dominios cíclicos de punto se recorren como máximo durante un periodo fundamental.
