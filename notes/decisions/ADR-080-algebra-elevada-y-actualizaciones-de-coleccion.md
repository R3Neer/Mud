---
id: D-080
title: "Álgebra elevada y actualizaciones de colección"
status: current
date: 2026-08-04
supersedes: []
superseded-by: []
questions:
  - "Q-006"
  - "Q-019"
affects:
  - "colecciones, operadores, efectos, gramática, AST y análisis de cardinalidad"
---

# ADR-080 — Álgebra elevada y actualizaciones de colección

- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]
- Ampliada por: [[ADR-098-rutas-asignables-y-write-back-de-aliases|D-098]]
- Modificada por: [[ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].

- Modifica: [[ADR-039-colecciones-y-diccionarios|D-039]], [[ADR-046-algebra-y-conflictos-de-efectos|D-046]], [[ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]] y [[ADR-057-gramatica-concreta-y-continuacion|D-057]].
- Preguntas relacionadas: [[notes/questions/Q-006-conflictos|Q-006]] y [[notes/questions/Q-019-numeros|Q-019]].

## Contexto

Todo campo MUD denota una colección y la cardinalidad omitida equivale a `[1]`. Faltaba determinar cómo reciben los operadores aritméticos esos valores, separar la resta numérica de la diferencia de colecciones y completar las actualizaciones compuestas correspondientes al álgebra de colecciones.

La diferencia simétrica de multiconjuntos definida por diferencia absoluta de multiplicidades tampoco era asociativa. Esa propiedad impedía consolidar `^=` y hacía que una cadena de `^` pareciera poseer las leyes habituales de XOR cuando no las poseía.

## Decisión

### Elevación aritmética restringida

Los operadores aritméticos binarios `+`, `-`, `*`, `/` y `%` se elevan sobre colecciones cuando al menos uno de los operandos tiene límite superior estático de cardinalidad menor o igual que uno.

Para un operador de miembros `\odot`:

$$
A\mathbin{\odot}B
=
[\,a\mathbin{\odot}b\mid a\in A,\ b\in B\,].
$$

La colección conserva una ocurrencia por cada pareja de ocurrencias. Si las cardinalidades son $[\ell_A..u_A]$ y $[\ell_B..u_B]$, la cardinalidad anterior a cualquier normalización `unique` es:

$$
[\ell_A\ell_B..u_Au_B].
$$

Por tanto, `empty` es absorbente: si cualquiera de los operandos está vacío no existe ninguna pareja ni se evalúa una operación de miembros. En particular, `empty / [0]` produce `empty` sin efectuar una división por cero.

Dos operandos cuyos límites superiores puedan superar uno no admiten elevación aritmética implícita. MUD no elige silenciosamente entre emparejamiento posicional, producto cartesiano completo, reducción o difusión mutua.

Cuando intervienen uniones, cada pareja posible de alternativas debe admitir el operador de miembros y sus resultados deben formar un tipo unión bien formado. Un estrechamiento previo puede retirar parejas imposibles.

Si solo un operando puede ser múltiple, el resultado conserva su orden cuando este era observable. `unique` solo se conserva cuando el análisis demuestra que la operación no puede colapsar miembros distintos; en otro caso el resultado conserva multiplicidad ordinaria.

### Diferencia de colecciones

`--` es la diferencia de colecciones. Para cada valor $v$:

$$
\mu_{A\mathbin{--}B}(v)
=
\max(\mu_A(v)-\mu_B(v),0).
$$

`-` deja de denotar diferencia de colecciones y queda reservado a la resta aritmética elevada. Así, sobre colecciones unitarias numéricas:

```text
[5] -  [3] = [2]
[5] -- [3] = [5]
[5] -- [5] = empty
```

`--` tiene la misma precedencia y asociación izquierda que `+` y `-`. La escritura `a--b` forma un único operador; la resta de un valor negativo se escribe `a - -b` o `a - (-b)`.

### Diferencia simétrica

`^` y `^=` solo se admiten cuando todos sus operandos efectivos son colecciones `unique`. Conservan entonces la diferencia simétrica ordinaria de conjuntos y sus leyes asociativa, conmutativa e involutiva.

La diferencia absoluta binaria de dos multiconjuntos continúa siendo expresable sin introducir un operador engañosamente asociativo:

```mud
(left -- right) | (right -- left)
```

### Actualizaciones compuestas

La gramática admite:

```mud
target |= value
target &= value
target ^= value
target --= value
```

Una actualización `target op= value` exige que `target` designe directamente un lugar exteriormente mutable o una ruta asignable reconstruible cuyo write-back termina en uno, que `target op value` esté bien tipado y que el resultado sea asignable al tipo efectivo de la hoja. Los aliases inmutables intermedios se reconstruyen sin adquirir mutabilidad propia. La capacidad interior `[mut]` no sustituye la exigencia de una raíz exteriormente escribible.

Dentro de un `then`, la actualización observa el valor proyectado por los efectos secuenciales anteriores del mismo delta privado. No se reduce en el AST a una asignación ordinaria porque su operador determina la consolidación concurrente.

Las actualizaciones homogéneas sobre un mismo destino se consolidan así cuando el orden observable y las restricciones del destino también pueden preservarse:

| Operador | Consolidación |
| --- | --- |
| `|=` sobre colección | Unión de todos los operandos; idempotente |
| `&=` | Intersección de todos los operandos; idempotente |
| `--=` | Suma de multiplicidades retiradas y un único truncado en cero |
| `^=` | Diferencia simétrica por paridad; solo sobre `unique` |

La mezcla de clases distintas de actualización sobre un mismo destino es conflicto salvo que otra decisión fije expresamente una consolidación. La preservación de cardinalidad, dominio, orden y unicidad continúa siendo una obligación estática de cada `then` y de toda consolidación posible.

Cuando varias actualizaciones concurrentes compatibles incorporan miembros nuevos a una colección `ordered` y el criterio semántico existente no determina por sí solo un orden total, la procedencia se completa reproduciblemente conforme a D-100, respetando toda causalidad real. Esta situación ya no constituye por sí sola un caso abierto de Q-006. Las operaciones que solo filtran el destino conservan su orden relativo.

Sobre `Text`, `|=` concatena secuencialmente como `|`. Varias concatenaciones concurrentes no son idempotentes ni conmutativas: solo se consolidan si existe un orden total semánticamente determinado; en otro caso entran en conflicto.

### Sobrecarga tipada

`|=`, `&=` y `^=` siguen la operación simbólica resuelta por tipos, sin ampliar por sí mismos los dominios de `|`, `&` o `^`. En particular, no sustituyen a los operadores booleanos de palabra. `|=` puede corresponder a concatenación de `Text` o unión de colecciones; `&=` y `^=` corresponden a las operaciones de colección allí donde estén definidas, y `^=` conserva la exigencia `unique`. `--=` solo corresponde a diferencia de colecciones.

## Consecuencias

- La cardinalidad singular deja de necesitar una categoría escalar distinta.
- La aritmética sobre una colección múltiple y otra opcional o unitaria tiene significado uniforme.
- `empty` absorbe toda aritmética elevada sin evaluar parejas inexistentes.
- La resta numérica y la diferencia de colecciones dejan de competir por `-`.
- XOR conserva las leyes que un lector espera porque solo opera sobre conjuntos `unique`.
- Los nuevos operadores compuestos conservan intención algebraica hasta el IR.

## Verificación

1. Elevación `[1]` con `[n..m]` en ambos órdenes.
2. Elevación `[0..1]` y absorción por `empty`.
3. Rechazo cuando ambos límites superiores pueden superar uno.
4. Matriz de alternativas nominales y estrechamiento previo.
5. Distinción entre `-`, `--`, `-=` y `--=`.
6. Rechazo de `^` y `^=` sobre colecciones no `unique`.
7. Consolidación homogénea de `|=`, `&=`, `^=` y `--=`.
8. Conflicto entre clases distintas y preservación de cardinalidad y orden.
