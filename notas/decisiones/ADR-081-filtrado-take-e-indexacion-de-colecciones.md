---
id: D-081
title: "Filtrado, `take` e indexación de colecciones"
status: vigente
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

- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]
- Modifica: [[ADR-039-colecciones-y-diccionarios|D-039]], [[ADR-047-cuantificadores-e-iteracion-finita|D-047]], [[ADR-048-azar-reproducible-y-fallos|D-048]], [[ADR-056-char-texto-y-orden-unicode|D-056]], [[ADR-064-orden-por-ruta-estable|D-064]] y [[ADR-075-dominios-enumerables-all-y-valores-derivados|D-075]].
- Preguntas relacionadas: [[notas/preguntas/Q-028-finitud|Q-028]] y [[notas/preguntas/Q-032-aleatoriedad-reproducible|Q-032]].

## Contexto

`for each ... if ...` selecciona participantes para producir efectos, pero no construye una colección pura reutilizable. Los cuantificadores consumen testigos para producir booleanos o agregados y `all` enumera un dominio completo; ninguna de esas formas devuelve la subcolección que satisface un predicado.

También faltaba distinguir entre posición observable, selección cuantitativa y elección aleatoria reproducible sin obligar a escribir `Rand` cuando la regla solo dice que se tomen algunos miembros.

## Decisión

### Filtrado como expresión

La forma:

```mud
player in players:
    player.score == 2
```

es una expresión de selección. Vincula cada miembro enumerable de la fuente, evalúa un predicado puro y determinista y devuelve las ocurrencias para las que el predicado es `true`.

La vinculación puede ser simple o una pareja de diccionario, igual que en `for each`:

```mud
(key, value) in stock:
    value > 0
```

La variable solo está disponible en el predicado. La fuente se captura al comenzar la evaluación. Debe ser finita y enumerable; si esa propiedad no puede demostrarse, la expresión es inválida.

El resultado:

- conserva el tipo y la identidad nominal de sus miembros;
- conserva multiplicidades y `unique`;
- conserva el orden y su criterio cuando la fuente es ordenada;
- produce identidades con procedencia; la capacidad interior del lugar derivado que la contiene se decide por su propio contrato conforme a D-084;
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

- dominios finitos enumerables, produciendo una colección de sus primeros valores canónicos;
- diccionarios, conservando asociaciones completas;
- `Text`, produciendo el prefijo de hasta `n` valores `Char` como otro `Text`.

La nominalidad de un alias contenedor no se reconstruye implícitamente: el resultado conserva la colección o secuencia subyacente y necesita una construcción o conversión nominal explícita cuando el contexto exija de nuevo el alias.

### Composición

`take` y la selección son expresiones ordinarias y se componen sin azúcar exclusivo:

```mud
# Hasta n coincidencias.
best := take n from player in players:
    player.score == 2

# Coincidencias dentro de una selección previa.
best := player in take m from players:
    player.score == 2

# Ambas restricciones.
best := take n from player in take m from players:
    player.score == 2
```

La anotación de la declaración es independiente de la selección:

```mud
chosen [3] := take 3 from player in players:
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
3. `take` sobre colección ordenada, no ordenada, dominio, diccionario y `Text`.
4. Muestreo sin reemplazo, reproducibilidad y estabilidad por instantánea.
5. Simplificación determinista cuando no existe elección real.
6. Composición de `take` antes y después del filtro.
7. Separación entre selección y contrato de cardinalidad.
8. Índice y sección ordenados, incluidos límites fuera de rango.
9. Rechazo de indexación posicional no ordenada.
10. Ruta `ordered by` total e inválida sobre alternativas de unión.

## Modificación por D-084

Una selección usada para definir un campo derivado puede alimentar una colección `[mut]` aunque la fuente no conceda capacidad interior. La declaración de la vista concede esa autoridad. La lista seleccionada permanece estable durante la instantánea y se recalcula tras consolidar efectos.
