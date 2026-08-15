---
id: D-088
title: "Iteración, progresiones firmadas y bloques de expresión"
status: vigente
date: 2026-08-15
supersedes: []
superseded-by: []
questions:
  - "Q-018"
  - "Q-028"
  - "Q-029"
affects:
  - "for each, filtros, cuantificadores, selección, dominios escalonados, intervalos, magnitudes, bloques de expresión, gramática, CST y AST"
---

# ADR-088 — Iteración, progresiones firmadas y bloques de expresión

- Modifica: [[ADR-047-cuantificadores-e-iteracion-finita|D-047]], [[ADR-057-gramatica-concreta-y-continuacion|D-057]], [[ADR-071-vinculaciones-locales-en-bloques-booleanos|D-071]], [[ADR-075-dominios-enumerables-all-y-valores-derivados|D-075]], [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]] y [[ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]].
- Conserva: [[ADR-034-number-exacto-y-rumber-binary64|D-034]], [[ADR-040-semantica-numerica-basica-restante|D-040]] y la prohibición de azar en filtros de [[ADR-048-azar-reproducible-y-fallos|D-048]].
- Preguntas relacionadas: [[notas/preguntas/Q-018-intervalos-discontinuos|Q-018]], [[notas/preguntas/Q-028-finitud|Q-028]] y [[notas/preguntas/Q-029-terminacion|Q-029]].

## Contexto

MUD ya dispone de `for each`, cuantificadores, selección pura y dominios escalonados, pero las reglas anteriores mezclaban enumerabilidad, progresión mediante una diferencia y estructura del cuerpo posterior a `:`. D-075 exigía además un paso positivo y D-047 no distinguía con precisión cuándo el filtro de una iteración ordenada puede observar efectos anteriores.

## Fuentes enumerables y `for each`

`for each` acepta cualquier fuente cuya finitud y enumerabilidad puedan demostrarse: colecciones, diccionarios exactos, intervalos enumerables, dominios finitos enumerables y cualquier otro valor con enumeración canónica definida. Un intervalo sigue siendo un intervalo; poder enumerarlo no lo convierte en colección.

```mud
action Accumulate for values: Int [* ordered], mut total: Int {
    then for each value in values:
        total += value
}
```

La pertenencia de la fuente se captura al comenzar el bucle. Un intervalo vacío produce cero iteraciones. Un intervalo infinito no puede alimentar una construcción que exija enumeración exhaustiva.

## Separador `:` y cuerpos

Cuando una construcción usa `:` para separar una cabecera de un cuerpo subordinado, las llaves pertenecen al cuerpo posterior y nunca sustituyen al separador.

```mud
action AccumulateDoubled for values: Int [* ordered], mut total: Int {
    then for each value in values: {
        doubled := value * 2
        total += doubled
    }
}
```

La forma sin `:` es inválida. Tras `:` el cuerpo puede comenzar en la misma línea o después de una separación física por terminadores; el salto no cambia el AST. El cuerpo de `for each` usa exactamente el contrato ejecutable de `then`: un único efecto o llamada a acción, o un bloque de efectos que puede intercalar vinculaciones locales `:=`.

Selecciones y cuantificadores/agregadores conservan igualmente su `:` obligatorio. Su cuerpo puede ser una expresión breve o un bloque de expresión con cero o más vinculaciones locales seguidas de una única expresión final.

## Bloque de expresión

Se generaliza el antiguo `BooleanBlock` a `ExpressionBlock(locals, result)`. La estructura no decide el tipo de `result`; lo hace su propietario. Reglas booleanas, guardas `if`, reglas `always`, postcondiciones `after` de acciones, selección, `exists`, `forall` y `count` aplican su contrato booleano; `when` exige un activador admitido; `sum` un valor agregable; `min` y `max` un valor ordenable. El `after` de test conserva su estructura propia de varias aserciones.

Las locales son puras, inmutables, secuenciales y no admiten referencias adelantadas, ciclos, redeclaración ni sombreado.

## Filtro de `for each`

El `if` opcional aparece después de `by` y puede ser una expresión o un bloque de expresión. El predicado es puro y no estocástico conforme a D-048.

- Con orden semántico, cada filtro se evalúa inmediatamente antes de su iteración y observa los efectos secuenciales producidos por iteraciones anteriores.
- Sin orden semántico, todos los filtros observan la misma instantánea inicial y las iteraciones aceptadas producen deltas que se consolidan como simultáneos.

Por ello `for each ... if ...` no se define universalmente como desazucaración literal a una selección materializada previa.

## `by` como progresión

`by δ` recibe una expresión ordinaria cuyo valor es una diferencia firmada compatible con la fuente. En construcciones runtime se evalúa exactamente una vez antes de comenzar el recorrido y su valor queda fijado durante esa ejecución.

La compatibilidad se determina por la operación de avance y por las conversiones implícitas exactas admitidas, no por igualdad nominal del tipo recorrido y la diferencia. Un intervalo `Nat` puede usar una diferencia `Int`; un intervalo `Num`, `Nat`, `Int` o `Num` compatibles; una magnitud puede usar otra unidad compatible. En magnitudes de punto el paso es una diferencia de la magnitud lineal subyacente, no otro punto.

Un paso positivo se ancla en el límite inferior; uno negativo, en el superior. Si el límite inicial es abierto, se aplica una vez el paso antes de comprobar el primer candidato. Tras cada valor emitido se suma el paso y el recorrido termina antes del primer candidato exterior. No es necesario alcanzar exactamente el extremo opuesto.

```mud
action Forward for mut total: Num {
    then for each value in [1..8] by 2:
        total += value
}
# recorrido: 1, 3, 5, 7

action Backward for mut total: Num {
    then for each value in [1..8] by -3:
        total += value
}
# recorrido: 8, 5, 2
```

Los extremos invertidos continúan normalizándose a `empty`; nunca expresan recorrido descendente.

## Paso cero

Si un paso runtime es demostrablemente cero, existe error estático. Si no puede demostrarse y finalmente evalúa a cero, se produce un fallo de evaluación `progression-step-zero`. Dentro de una acción real ese fallo produce `failed` y rollback conforme a la taxonomía de D-048 y D-061; en un contexto puro se propaga conforme al contrato de fallos de expresiones, sin convertirse en `false`. En un dominio escalonado el paso es estático, por lo que cero siempre es error de elaboración.

## Pasos predeterminados

Una fuente que ya posee enumeración propia —por ejemplo una colección ordenada, un diccionario exacto o un dominio nominal finito— no necesita `by` para recorrerse. Los pasos predeterminados solo intervienen cuando la enumeración se construye como progresión. En esas fuentes puede omitirse `by` únicamente cuando el tipo recorrido define una diferencia sucesora canónica. MUD fija `Nat -> 1`, `Int -> 1` y `Money -> 0.01`; omitir `by` selecciona siempre esa diferencia positiva. Otros tipos de progresión exacta requieren paso explícito salvo decisión que defina un sucesor canónico.

`Num` admite progresión con paso exacto explícito, pero un intervalo general de `Num` sin paso es inválido. `Rum` conserva la prohibición de D-034: sus intervalos nunca son enumerables y no admiten progresión `by`, ni en iteración ni en dominio escalonado. Una colección explícita de valores `Rum` sí puede enumerarse sin `by` porque su enumeración procede de la colección, no de una progresión numérica.

## Dominios escalonados

`interval by δ` define un dominio mediante la misma progresión exacta. El paso debe ser estático, no nulo y compatible, y puede ser negativo.

```text
[1..8] by 2   -> {1, 3, 5, 7}
[1..8] by -2  -> {2, 4, 6, 8}
(1..8] by 2   -> {3, 5, 7}
[1..8) by -2  -> {2, 4, 6}
```

El signo determina el anclaje y puede cambiar los miembros del dominio, pero el orden de generación no forma parte del tipo. `all` materializa los miembros en el orden canónico del tipo.

Los dominios escalonados pueden aparecer en cualquier contexto que admita un dominio: campos, componentes, participantes, `given`, formas derivadas, campos públicos y otros propietarios compatibles.

## Intervalos discontinuos y dominios cíclicos de punto

En una forma normalizada con varios segmentos disjuntos el paso se reinicia en cada segmento. Un paso positivo recorre segmentos de menor a mayor y se ancla en el extremo inferior; uno negativo recorre de mayor a menor y se ancla en el superior.

La sintaxis consolidada de intervalos discontinuos sigue abierta en Q-018. D-088 cierra el recorrido descendente explícito: se expresa mediante paso negativo, nunca invirtiendo extremos.

Un dominio cíclico de punto puede enumerarse con diferencia compatible, pero solo durante un periodo fundamental. No se envuelve indefinidamente.

## Otras construcciones con `by`

`by` de progresión se admite también en selección y en `exists`, `forall`, `count`, `sum`, `min` y `max`, siempre que la fuente ofrezca progresión mediante diferencia. No significa stride sobre una colección arbitraria. Una fuente futura puede definir expresamente esa capacidad; esta decisión no introduce un protocolo general. `ordered by path` conserva una semántica distinta.

## Azar

D-088 no permite azar en el filtro de una iteración. Se conserva la prohibición de D-048 hasta que Q-032 cierre identidad de puntos aleatorios, subsemillas y caché por ocurrencia.

## Consecuencias para AST

El AST superficial reemplaza `BooleanBlock` por `ExpressionBlock`. `ForEachEffect` conserva `step?`, conserva su filtro opcional como `ExpressionBlock?` y normaliza tanto el efecto breve como el bloque ejecutable al mismo `EffectBlock` que usa `then`. `SelectionExpr` y `QuantifierExpr` conservan `step?` y su predicado/cuerpo como `ExpressionBlock`. `by -2` no necesita nodo especial para el signo.

## Diagnósticos

Debe diagnosticarse ausencia de `:`, paso cero, diferencia incompatible, falta de paso cuando una progresión no tenga sucesor predeterminado, fuente infinita/no enumerable, intento de progresión sobre un intervalo `Rum`, `by` sobre fuente sin progresión, filtro no booleano, azar en filtro y uso de extremos invertidos como supuesto descenso.

## Verificación

Se verifican fuentes enumerables de todas las clases admitidas, `:` con cuerpo breve y con llaves, filtro breve y con locales, pasos positivos/negativos/runtime, evaluación única del paso, cero estático/runtime, límites abiertos/cerrados, intervalos vacíos/infinitos, dominios escalonados firmados y `all`, `Num`, rechazo de progresión `Rum`, colección explícita de `Rum`, selección y los seis cuantificadores con `by` y bloque, magnitudes con unidades compatibles y diferencia entre filtro ordenado/no ordenado. La verificación concreta de intervalos discontinuos y del periodo fundamental cíclico se completa cuando Q-018 cierre la forma fuente consolidada necesaria para expresarlos sin ambigüedad; su semántica queda fijada por esta decisión.
