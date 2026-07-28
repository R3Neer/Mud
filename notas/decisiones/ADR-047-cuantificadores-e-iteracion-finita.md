# ADR-047 — Cuantificadores e iteración finita

- Estado: Vigente
- Fecha: 2026-07-28
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

`for each` aparece dentro de un `then`:

```mud
for each item in source if predicate {
    ...
}
```

La pertenencia a `source` se toma como instantánea al comienzo del bucle. El filtro es puro, determinista y no puede depender de azar calculado.

- En una fuente ordenada, las iteraciones son secuenciales y cada una observa los efectos de la anterior dentro del delta privado.
- En una fuente no ordenada, las iteraciones leen la misma instantánea y sus deltas se consolidan como efectos simultáneos; un conflicto revierte la resolución completa.

La enumeración canónica procede del tipo: orden declarado de una familia cerrada, producto lexicográfico de un alias estructural, orden del diccionario o colección, u orden ascendente de un intervalo.

Los intervalos finitos de `Natural` e `Integer` usan paso predeterminado uno; `Money`, paso `0.01`. Un intervalo de `Number` no discreto requiere paso exacto explícito. Los intervalos de `Rumber` nunca son enumerables. El último valor es el último punto generado que pertenece al intervalo; no se fuerza la inclusión del extremo.

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
5. Rechazo de una enumeración `Rumber` o infinita.
