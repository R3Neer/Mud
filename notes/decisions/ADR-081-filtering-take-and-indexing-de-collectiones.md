---
id: D-081
title: "Filtrado, `take` e indexación de colecciones"
status: current
date: 2026-08-04
supersedes: []
superseded-by: []
questions:
  - "Q-028"
  - "Q-032"
affects:
  - "colecciones, diccionarios, Text, dominios, azar, orden, gramática y AST"
---

# ADR-081 — Filtrado, `take` e indexación de colecciones

- Modificada por: [[ADR-103-inner-capability-in-derived-values|D-103]].

- Modificada por: [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]]
- Modificada por: [[notes/decisions/ADR-084-specialisation-de-aliases-inherited-members-and-derived-views|D-084]]
- Modificada por: [[ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]]
- Modifica: [[ADR-039-collections-and-dictionaries|D-039]], [[ADR-047-quantifiers-and-finite-iteration|D-047]], [[ADR-048-reproducible-randomness-and-errors|D-048]], [[ADR-056-char-text-and-unicode-ordering|D-056]], [[ADR-064-ordering-by-stable-path|D-064]] y [[ADR-075-enumerable-domains-all-and-derived-value-form|D-075]].
- Preguntas relacionadas: [[notes/questions/Q-028-f-finiteness|Q-028]] y [[notes/questions/Q-032-a-reproducible-randomness|Q-032]].

## Contexto

`for each ... if ...` selecciona participantes para producir efectos, pero no construye una colección pura reutilizable. Los cuantificadores consumen testigos para producir booleanos o agregados y `all` enumera un dominio completo; ninguna de esas formas devuelve la subcolección que satisface un predicado.

También faltaba distinguir entre posición observable, selección cuantitativa y elección aleatoria reproducible sin obligar a escribir `Rand` cuando la regla solo dice que se tomen algunos miembros.

## Decisión

### Filtrado como expresión

La forma:

```mud
player in players :
    player.score == 2
```

es una expresión de selección. Vincula cada miembro enumerable de la fuente, evalúa un predicado puro y determinista y devuelve las ocurrencias para las que el predicado es `true`.

La vinculación puede ser simple o una pareja de diccionario, igual que en `for each`:

```mud
(key, value) in stock :
    value > 0
```

La variable solo está disponible en el predicado. La fuente se captura al comenzar la evaluación. Debe ser una colección finita y enumerable; si la fuente conceptual es un dominio, se materializa explícitamente como `all D` antes de seleccionar. Si la finitud o enumerabilidad no puede demostrarse, la expresión es inválida.

El resultado:

- conserva el tipo y la identidad nominal de sus miembros;
- conserva multiplicidades y `unique`;
- conserva el orden y su criterio cuando la fuente es ordenada;
- produce identidades con procedencia y conserva capacidad interior cuando la fuente la garantiza; una forma derivada exterior puede exigir esa capacidad, pero no concederla si falta;
- nunca adquiere mutabilidad exterior;
- tiene cardinalidad conservadora `[0..u]` para una fuente `[l..u]`, estrechable por análisis;
- puede estrechar alternativas mediante pruebas como `is`.

Sobre un diccionario, una vinculación por pareja devuelve un diccionario con las asociaciones aceptadas.

### Expresión general `take`

La forma general es:

```mud
take amount from source
```

`amount` debe elaborar a un `Nat [1]`. La fuente debe ser finita y enumerable. Si contiene $k$ ocurrencias y la cantidad es $n$, el resultado contiene $\min(k,n)$ ocurrencias.

- `take 0 from source` produce `empty`.
- `take n from empty` produce `empty`.
- La falta de miembros nunca falla por sí misma; un contrato exterior puede exigir una cardinalidad mayor.

Para una fuente con cardinalidad estática $[l..u]$ y una cantidad constante $n$, el resultado posee:

$$
[\min(l,n)..\min(u,n)].
$$

Si la fuente posee orden semántico observable o una enumeración canónica propia, `take` conserva su prefijo. Si la fuente es una colección o diccionario sin orden observable, selecciona uniformemente y sin reemplazo entre ocurrencias mediante la semilla reproducible. El resultado no adquiere orden por el orden interno del muestreo.

Un `take` no ordenado es un punto aleatorio aunque no escriba `Rand`: posee identidad semántica, caché por instantánea y las mismas restricciones contextuales. Es determinista y no consume azar cuando `n=0` o cuando puede demostrarse que la fuente contiene como máximo `n` ocurrencias.

`take` se aplica además a:

- materializaciones `all D` de dominios finitos enumerables, tomando sus primeros valores canónicos;
- diccionarios, conservando asociaciones completas;
- `Text`, produciendo el prefijo de hasta `n` valores `Char` como otro `Text`.

Un dominio desnudo no es fuente directa de `take`: al producir una colección, la materialización debe quedar explícita en el programa.

La nominalidad de un alias contenedor no se reconstruye implícitamente: el resultado conserva la colección o secuencia subyacente y necesita una construcción o conversión nominal explícita cuando el contexto exija de nuevo el alias.

### Composición

`take` y la selección son expresiones ordinarias y se componen sin azúcar exclusivo:

```mud
# Hasta n coincidencias.
best := take n from player in players :
    player.score == 2

# Coincidencias dentro de una selección previa.
best := player in take m from players :
    player.score == 2

# Ambas restricciones.
best := take n from player in take m from players :
    player.score == 2
```

La anotación de la declaración es independiente de la selección:

```mud
chosen [3] := take 3 from player in players :
    player.score == 2
```

`take 3` selecciona hasta tres; `[3]` exige exactamente tres.

### Indexación y secciones

Una colección solo admite acceso posicional cuando posee orden observable. Los índices comienzan en uno.

```mud
queue[1]
queue[2..5]
```

Un índice singular produce una colección `[1]` si la cardinalidad de la fuente demuestra que la posición existe y `[0..1]` en otro caso. Un intervalo de índices produce las posiciones existentes dentro del intervalo y nunca falla por exceder el final. Conserva orden, multiplicidad, tipo de miembro y capacidad interior.

Sobre una colección no ordenada, el acceso posicional es inválido; se usa `take` cuando la intención es seleccionar una cantidad. Los diccionarios conservan la indexación por clave y `Text` conserva su indexación de secuencia; la resolución por tipos distingue esas formas.

### `ordered by` sobre uniones

Cuando el miembro de una colección es una unión, cada ruta `ordered by` debe ser total sobre todas las alternativas posibles:

1. Cada segmento existe en cada alternativa alcanzable.
2. Cada acceso intermedio es singular.
3. Toda la ruta es transitivamente estable.
4. Las claves finales elaboran hacia un único tipo común con orden semántico total.

Se admiten ampliaciones implícitas únicas, como `Nat` hacia `Int`. No se eliminan identidades nominales de aliases ni se elige entre varias conversiones. Si hace falta adaptar una alternativa, se declara primero un campo calculado común y se ordena por él.

## Consecuencias

- Las consultas pueden construir grupos definidos por una regla sin introducir variables mutables ni efectos auxiliares.
- `for each` continúa siendo la forma de actuar sobre miembros; la selección es la forma de obtenerlos como valor.
- `take` expresa una restricción cuantitativa general y usa orden o semilla según la semántica de la fuente.
- La indexación nunca inventa posiciones para colecciones no ordenadas.
- Una unión no puede hacer parcial una clave `ordered by`.

## Verificación

1. Filtro ordenado, no ordenado, `unique`, con multiplicidades y sobre diccionario.
2. Estrechamiento de unión dentro del predicado.
3. `take` sobre colección ordenada, no ordenada, `all D`, diccionario y `Text`, y rechazo de un dominio desnudo como fuente productora de colección.
4. Muestreo sin reemplazo, reproducibilidad y estabilidad por instantánea.
5. Simplificación determinista cuando no existe elección real.
6. Composición de `take` antes y después del filtro.
7. Separación entre selección y contrato de cardinalidad.
8. Índice y sección ordenados, incluidos límites fuera de rango.
9. Rechazo de indexación posicional no ordenada.
10. Ruta `ordered by` total e inválida sobre alternativas de unión.

## Modificación por D-084

Una selección usada para definir un campo derivado conserva la capacidad interior de su fuente porque devuelve las mismas identidades aceptadas. Una vista `[mut]` exige que esa capacidad esté disponible; la declaración no la fabrica. La lista seleccionada permanece estable durante la instantánea y se recalcula tras consolidar efectos.

## Modificación por D-088

La selección pura admite `item in source by step : predicate` cuando la fuente define progresión por diferencia. No es stride sobre una colección arbitraria. El predicado puede ser una expresión breve o un `ExpressionBlock` con locales y sigue siendo puro y determinista. El AST conserva `step?` y el predicado como `ExpressionBlock`.

## Modificación vigente por D-096

Selección y `take` producen colecciones. Cuando su fuente conceptual es un dominio, debe materializarse explícitamente mediante `all D`; por ejemplo `candidate in all Actions : ...` y `take n from all D`. Recorridos y cuantificadores que no producen una colección pueden consumir directamente un dominio finito enumerable.
