---
id: D-039
title: "Colecciones y diccionarios"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-006"
  - "Q-047"
affects:
  - "futuro `15-colecciones.md`, futuro `16-diccionarios.md`, futuro `20-cuantificadores-e-iteracion.md`"
---
# ADR-039 — Colecciones y diccionarios

- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]] y [[ADR-098-rutas-asignables-y-write-back-de-aliases|D-098]]
- Modificada por: [[notas/decisiones/ADR-064-orden-por-ruta-estable|D-064]]
- Modificada por: [[ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|D-080]] y [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]]
- Amplía: D-019, D-026, D-033
- Preguntas relacionadas: Q-006, Q-047
- Documentos afectados: futuro `15-colecciones.md`, futuro `16-diccionarios.md`, futuro `20-cuantificadores-e-iteracion.md`

## Decisión

### Colecciones

La cardinalidad usa intervalos de naturales:

```mud
T[n]
T[min..max]
T[min..*]
T[*]
```

Omitirla equivale a `[1]`; `[n]` equivale a `[n..n]`; `[*]` usa la semántica de límite efectivo de D-029 y normalmente equivale a `[0..*]`.

`empty` representa ausencia sin `null`.

Las colecciones admiten duplicados salvo `unique`. `ordered` conserva un orden observable y `ordered by ruta` declara una clave semántica estable conforme a D-064.

Añadir a una colección `unique` un valor que ya está presente es un no-op. La operación es idempotente: una o varias adiciones del mismo valor producen una sola presencia, también cuando proceden de efectos concurrentes compatibles.

Cuando un literal destinado a una colección `unique` contiene duplicados cuya igualdad puede demostrarse estáticamente, el compilador los normaliza a una sola presencia y emite un aviso no bloqueante. Si la colección normalizada incumple su cardinalidad, el programa contiene además un error estático de cardinalidad y no es válido:

```mud
members: Person [* unique] = [Alice, Alice]  # aviso; equivale a [Alice]
pair: Person [2 unique] = [Alice, Alice]     # error; tras normalizar solo queda un valor
```

Fuentes iniciales de orden:

- Básicos: orden de su tipo.
- `Char`: valor escalar Unicode creciente; `ordered by` está prohibido.
- `thing`: orden de inserción cuando la colección es `ordered`.
- `ordered family`: orden declarado.
- Alias ordenado: orden subyacente o lexicográfico.

En una colección de valores con campos, componentes o datos asociados, `ordered by ruta` puede sustituir el orden ordinario por una clave obtenida mediante accesos singulares desde cada miembro. La clave debe tener orden semántico total y toda la ruta debe ser transitivamente estable. Una `thing` no es una clave final ordenable. Las claves iguales conservan el orden relativo de inserción. Este orden de colección no modifica la comparación intrínseca entre sus miembros.

Cuando el tipo o `ordered by ruta` determina el orden principal, un literal escrito en otro orden se normaliza y produce un aviso no bloqueante. Entre claves iguales se conserva el orden escrito, que actúa como inserción. Este aviso no se aplica a una colección `thing [ordered]` ordenada enteramente por inserción.

### Álgebra de colecciones

Los operadores conjuntistas se aplican también a colecciones compatibles:

| Operación | Forma |
| --- | --- |
| Unión | `A | B` |
| Intersección | `A & B` |
| Diferencia | `A -- B` |
| Diferencia simétrica de conjuntos `unique` | `A ^ B` |

Dos operandos son compatibles cuando poseen el mismo tipo efectivo de miembro. Los refinamientos de dominio y los modificadores de colección pueden diferir y se combinan conforme a las reglas siguientes; no se introducen conversiones implícitas entre tipos distintos.

Sea $\mu_C(v)\in\mathbb N$ la multiplicidad del valor $v$ en la colección $C$. Las operaciones se definen punto a punto:

$$
\begin{aligned}
\mu_{A\mid B}(v) &= \max(\mu_A(v),\mu_B(v)),\\
\mu_{A\mathbin{\&}B}(v) &= \min(\mu_A(v),\mu_B(v)),\\
\mu_{A\mathbin{--}B}(v) &= \max(\mu_A(v)-\mu_B(v),0).
\end{aligned}
$$

Por tanto, la unión es idempotente incluso sin `unique`: `A | A == A`. No es concatenación ni suma de bolsas. Si ambos operandos son `unique`, estas definiciones coinciden con la unión, intersección y diferencia ordinarias de conjuntos.

`^` exige que ambos operandos sean `unique` y aplica la diferencia simétrica ordinaria. No se define mediante diferencia absoluta de multiplicidades porque esa operación no es asociativa. La forma binaria equivalente sobre multiconjuntos se escribe `(A -- B) | (B -- A)`.

#### Cardinalidad y dominio inferidos

Sean $[a..b]$ y $[c..d]$ las cardinalidades estáticas de $A$ y $B$. Sin información adicional sobre solapamiento, el compilador puede garantizar:

| Resultado | Cardinalidad conservadora |
| --- | --- |
| `A | B` | $[\max(a,c)..b+d]$ |
| `A & B` | $[0..\min(b,d)]$ |
| `A -- B` | $[\max(0,a-d)..b]$ |
| `A ^ B` (`unique`) | $[\max(0,a-d,c-b)..b+d]$ |

La aritmética de límites conserva `*` como límite superior efectivo. El análisis debe estrechar estos intervalos cuando pueda demostrar disjunción, inclusión, igualdad, un dominio finito o cualquier otra restricción relevante.

Si $D_A$ y $D_B$ son los dominios semánticos de los miembros:

| Resultado | Dominio de miembro |
| --- | --- |
| `A | B` | $D_A\cup D_B$ |
| `A & B` | $D_A\cap D_B$ |
| `A -- B` | $D_A$ |
| `A ^ B` (`unique`) | $D_A\cup D_B$ |

El IR conserva el dominio resultante aunque su forma más precisa no posea una escritura superficial abreviada.

#### Propagación de modificadores

Para cada modificador $m$ de `unique`, `ordered` o capacidad interior `mut`, su presencia en el resultado se obtiene mediante la misma tabla:

| Resultado | Presencia de $m$ |
| --- | --- |
| `A | B` | $m(A)\land m(B)$ |
| `A & B` | $m(A)\lor m(B)$ |
| `A -- B` | $m(A)$ |
| `A ^ B` | $m(A)\land m(B)$; `unique` está garantizado |

Para `unique`, la tabla se deduce directamente de las multiplicidades: la intersección es única si cualquiera de los operandos limita cada multiplicidad a uno y la unión necesita esa garantía en ambos lados. La diferencia simétrica ya exige `unique` en sus operandos.

Para `mut`, la tabla se refiere exclusivamente a la capacidad interior sobre miembros, nunca a la mutabilidad exterior de un campo almacenado. Una unión o diferencia simétrica mixta podría contener un miembro alcanzado únicamente desde el operando sin capacidad; una intersección, en cambio, solo contiene miembros que también son alcanzables desde el operando con capacidad. Una diferencia `--` solo conserva miembros del operando izquierdo. Un campo calculado no adquiere mutabilidad exterior.

Para `ordered`, si solo la intersección conserva orden se filtra el operando ordenado; la diferencia `--` filtra el operando izquierdo. Unión y diferencia simétrica mixtas son no ordenadas porque pueden incorporar miembros exclusivos del operando no ordenado.

Cuando ambos operandos son `ordered`, deben usar criterios de orden compatibles. Si sus claves o modos de orden son incompatibles, la operación es un error estático. Un orden por tipo o por una misma ruta `ordered by` normaliza el resultado con ese criterio y preserva inserción entre empates. Para orden de inserción, el resultado es estable respecto del operando izquierdo:

- La unión recorre primero $A$ y añade después, en el orden de $B$, solo las ocurrencias adicionales necesarias para alcanzar cada multiplicidad máxima.
- La intersección y la diferencia `--` filtran $A$ sin reordenarlo.
- La diferencia simétrica conserva primero las ocurrencias excedentes de $A$ y después las de $B$.

En consecuencia, para colecciones ordenadas por inserción, las operaciones conmutativas conservan el mismo multiconjunto al intercambiar operandos, pero pueden producir secuencias observables distintas. La igualdad ordenada continúa comparando la secuencia completa.

Ejemplo de inferencia:

```mud
leftChars: Char [1..5] = ["a"]
rightChars: Char [0..2] = empty
combinedChars := leftChars | rightChars
```

El tipo estático de `combinedChars` es `Char [1..7]`: no es `unique`, `ordered` ni `mut`, y su dominio de miembro es el dominio completo de `Char`.

`Text` no equivale a `Char [* ordered]`: conserva el orden posicional de sus caracteres y no admite modificadores de colección. D-056 fija esta distinción.

La consolidación simultánea de inserciones distintas con orden observable deberá integrarse en la matriz de Q-006.

### Diccionarios

La forma:

```mud
Key -> Value [cardinality modifiers]
```

declara un diccionario con claves intrínsecamente únicas. El modificador `unique`, cuando se escribe, se aplica a los **valores asociados** conforme a D-085: exige que un mismo valor no quede asociado a más de una clave. Una inserción o sustitución que violaría esa unicidad es una no-op completa y no produce `failed`.

```mud
stock =
    Grain -> 2_000,
    Bronze -> 500
```

Asignar una clave sustituye su valor; escribir una clave ausente materializa la entrada si tipo, dominio, capacidad y cardinalidad lo permiten; retirar una clave ausente es no-op.

Leer una clave ausente produce `empty` con la forma de salida declarada. La ausencia no produce `failed` por sí misma; solo un contexto posterior cuyo tipo, dominio o cardinalidad no admita cero elementos puede fallar. No se usa `null` ni se sustituye silenciosamente por el predeterminado del tipo de valor.

Una indexación de diccionario puede ir seguida por acceso a miembros del valor obtenido cuando su tipo lo permite. Otra indexación encadenada exige que el resultado intermedio sea a su vez un diccionario compatible.

Cuando una indexación exacta es un paso intermedio de una ruta asignable que atraviesa un alias inmutable, la elaboración puede reconstruir el alias y propagar la sustitución hasta el diccionario y el lugar exteriormente mutable que lo contiene. Si la clave intermedia está ausente, la consulta produce `empty` y el write-back parcial es un no-op: no materializa la clave, no aplica predeterminados y no produce `failed` por esa ausencia. La asignación directa `dictionary[key] = wholeValue` continúa siendo distinta y puede materializar una clave ausente.

### Orden e iteración

Un diccionario `ordered` recorre claves según su orden canónico. Puede recorrerse por claves o por pares `(key, value)`.

Un alias estructural puede actuar como una única clave compuesta y usar el azúcar definido en D-033:

```mud
board[(E, Four)]
board[E, Four]
```

### Igualdad

- Colección ordenada: misma secuencia y multiplicidad.
- Colección no ordenada: mismo multiconjunto.
- Diccionario: mismas asociaciones clave–valor; el orden de almacenamiento no altera igualdad.

## Consecuencias

- Cardinalidad, orden, unicidad y mutabilidad son ejes separados.
- Los diccionarios no exponen `null`.
- La iteración no depende del hash o estructura interna del materializador.
- Las operaciones de colección y diccionario deben ser totales donde esta decisión lo indica.

## Alternativa descartada

### Unicidad predeterminada

Se descarta hacer `unique` implícito, tanto para todas las colecciones como en función del tipo de miembro. La multiplicidad es información observable y necesaria en colecciones como `Num [*]`; eliminarla de manera predeterminada cambiaría el significado de datos que representan observaciones, tiradas o frecuencias. Un valor predeterminado dependiente del tipo haría además que una misma forma de colección cambiara de semántica entre código genérico, aliases y conversiones.

La regla uniforme es que la ausencia de `unique` conserva multiplicidad y su presencia impone una sola ocurrencia por valor.

## Verificación futura

1. Cardinalidad omitida y `empty`.
2. Duplicados, normalización, aviso e idempotencia de `unique`.
3. Orden natural, de inserción, semántico y `ordered by`, incluida una ruta estable sobre dato asociado y empates por inserción.
4. Lectura ausente como `empty`, escritura y retirada de clave ausente, y `unique` global sobre valores.
5. Igualdad independiente de representación interna.
6. Clave alias ordinaria y azucarada.
7. Multiplicidades de unión, intersección y diferencia; rechazo de `^` sin `unique`.
8. Inferencia conservadora y estrechada de cardinalidad y dominio.
9. Propagación de `unique`, `ordered` y capacidad interior `mut` en las cuatro operaciones admitidas.
10. Orden canónico y orden estable por inserción, incluida la posible diferencia secuencial al intercambiar operandos.
11. Ausencia de mutabilidad exterior en resultados calculados.
