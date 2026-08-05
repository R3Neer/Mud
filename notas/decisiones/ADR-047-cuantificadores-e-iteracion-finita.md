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

- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Ampliada por: [[ADR-075-dominios-enumerables-all-y-valores-derivados|D-075]]
- Ampliada por: [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]]

- Preguntas relacionadas: Q-018, Q-028, Q-029
- Documentos afectados: expresiones, intervalos, iteración

## Contexto

MUD necesita recorrer conjuntos de dominio sin introducir bucles generales cuya terminación o resultado dependan del contenedor interno.

## Decisión

Las expresiones admiten:

```mud
exists x in source: predicate
forall x in source: predicate
count x in source: predicate
sum x in source: expression
min x in source: expression
max x in source: expression
```

La fuente debe ser finita y enumerable. La evaluación es pura; `min` y `max` sobre una fuente vacía producen el error definido para agregación vacía, no un valor inventado.

D-081 añade una selección pura que devuelve los testigos en lugar de consumirlos:

```mud
item in source: predicate
```

Comparte la obligación de finitud y enumerabilidad, pero produce la subcolección aceptada y puede alimentar después un cuantificador, `take` u otra expresión.

`for each` aparece dentro de un `then`:

```mud
for each item in source if predicate {
    ...
}

for each value in source by step if predicate {
    ...
}
```

La cláusula `by` opcional precede siempre a `if`. Un diccionario puede vincular un par mediante `(key, value)`.

La pertenencia a `source` se toma como instantánea al comienzo del bucle. El filtro es puro, determinista y no puede depender de azar calculado.

- En una fuente ordenada, las iteraciones son secuenciales y cada una observa los efectos de la anterior dentro del delta privado.
- En una fuente no ordenada, las iteraciones leen la misma instantánea y sus deltas se consolidan como efectos simultáneos; un conflicto revierte la resolución completa.

La enumeración canónica procede del tipo: orden declarado de una familia cerrada, producto lexicográfico de un alias estructural, orden del diccionario o colección, u orden ascendente de un intervalo.

Los intervalos finitos de `Nat` e `Int` usan paso predeterminado uno; `Money`, paso `0.01`. Un intervalo de `Num` no discreto requiere paso exacto explícito. Los intervalos de `Rum` nunca son enumerables. El último valor es el último punto generado que pertenece al intervalo; no se fuerza la inclusión del extremo.

Un intervalo discontinuo se normaliza en segmentos disjuntos y se recorre segmento a segmento, reiniciando el paso en cada segmento. Un intervalo vacío produce cero iteraciones.

## Consecuencias

- No existe iteración implícita sobre dominios infinitos o no enumerables.
- El orden descendente y la sintaxis consolidada de intervalos discontinuos siguen en Q-018.
- Las pruebas de finitud y terminación pueden ser conservadoras.

## Verificación

1. Cuantificadores y agregaciones sobre fuente finita.
2. Error de agregación extrema vacía.
3. Diferencia observable entre bucle ordenado y no ordenado.
4. Intervalos abiertos, cerrados, discontinuos y con paso.
5. Rechazo de una enumeración `Rum` o infinita.
6. Orden sintáctico `by` antes de `if` y vinculación de pares de diccionario.
