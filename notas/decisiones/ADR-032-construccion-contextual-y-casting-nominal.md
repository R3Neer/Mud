# ADR-032 — Construcción contextual y casting nominal de aliases

- Estado: Vigente
- Fecha: 2026-07-28
- Amplía: [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]]
- Pregunta relacionada: Q-056
- Documentos afectados: futuro `10-sistema-de-tipos.md`, futuro `12-aliases.md`, futuro `19-expresiones.md`

## Contexto

La nominalidad de los aliases exige distinguir:

- La construcción directa de un valor bajo un tipo esperado.
- La conversión de un valor que ya posee otro tipo.
- La comparación de literales todavía no tipados.

Sin esta separación, escribir valores ordinarios sería innecesariamente pesado o se perdería la garantía nominal.

## Decisión

### Dos familias de `to`

`to` posee dos familias estáticamente distinguibles:

1. Conversión cuantitativa, definida por D-030.
2. Casting nominal entre un alias y una representación estructuralmente compatible.

```mud
rawText to PlayerName
playerName to Text
cityName to PlayerName
coordinate to Square
```

Un casting nominal:

- Conserva el valor subyacente.
- Cambia la identidad nominal del tipo.
- Exige compatibilidad estructural.
- Valida las restricciones y dominios del destino.
- No redondea ni transforma el contenido.

La afirmación de D-030 de que `to` no es un casting general continúa vigente para valores no cuantitativos que no participan en esta relación nominal. `to` no habilita conversiones arbitrarias entre `thing`, texto y números o tipos estructuralmente incompatibles.

### Compatibilidad estructural

Dos representaciones son compatibles cuando tienen la misma forma normalizada. Para aliases estructurales deben coincidir, como mínimo:

1. Número de componentes.
2. Nombre de cada componente.
3. Orden de los componentes.
4. Tipo subyacente de cada componente.
5. Cardinalidades.
6. Estructura de colecciones y diccionarios.
7. Modificadores estructurales como `ordered` y `unique`.

Los dominios no cambian esa forma mínima: se validan contra el valor al construir o convertir al destino. La definición inductiva completa de normalización y sus posibles ciclos quedan en Q-056.

### Literales contextuales

Un literal estructural desnudo no posee por sí solo identidad de alias:

```mud
(E, Four)
```

El tipo esperado puede construir directamente el valor nominal:

```mud
square: Square = (E, Four)
game.Move((E, Four)) # si el `given` esperado es Square
board[E, Four]       # si la clave esperada es Square
```

Lo mismo se aplica a literales básicos:

```mud
playerName: PlayerName = "Ada"
```

Esta construcción contextual no requiere `to`. En cambio, una expresión ya tipada conserva su tipo y necesita conversión explícita:

```mud
rawName: Text = "Ada"
playerName: PlayerName =
    rawName to PlayerName
```

### Literales estructurales posicionales y nombrados

La forma posicional sigue el orden de declaración:

```mud
(E, Four)
```

La forma nombrada exige los mismos componentes en el mismo orden:

```mud
(
    file = E,
    rank = Four
)
```

Los nombres validan y documentan posiciones; no permiten reordenarlas. Todo componente debe aparecer exactamente una vez. Faltas, duplicados, componentes desconocidos o cambios de orden son errores estáticos.

### Contexto de comparación

Dos literales estructurales desnudos no pueden compararse porque ninguno aporta un tipo esperado:

```mud
(E, Four) == (E, Four) # inválido
```

Si un operando ya está resuelto como un alias y el otro es un literal sintáctico compatible todavía construible por contexto, el tipo nominal se propaga como expectativa al literal:

```mud
(E, Four) to Square == (E, Four)
(E, Four) == (E, Four) to Square
```

La propagación es bidireccional respecto de la posición izquierda o derecha y se aplica tanto a literales básicos como estructurales. Solo construye literales; no convierte silenciosamente variables, accesos, llamadas ni otras expresiones que ya tengan tipo.

Por ejemplo, si `playerName` tiene tipo `PlayerName`, el literal de:

```mud
playerName == "Ada"
```

puede construirse contextualmente como `PlayerName`. En cambio, si `rawText` es una variable de tipo `Text`, `playerName == rawText` continúa siendo inválido sin `to`.

Los literales de `Text`, `Char`, `Bool` y los tipos numéricos básicos poseen tipo básico contextual suficiente para compararse directamente.

Después de resolver los literales, ambos operandos deben tener exactamente el mismo tipo nominal. Comparar aliases diferentes o un alias con una expresión ya tipada como su representación subyacente es un error:

```mud
square == coordinate
playerName == rawText
```

Debe convertirse explícitamente uno de los operandos:

```mud
square == coordinate to Square
playerName to Text == rawText
```

### Igualdad y orden

Dos valores son iguales si poseen el mismo alias nominal y el mismo contenido.

Los aliases simples heredan la disponibilidad de orden de su tipo subyacente, pero solo se comparan con valores del mismo alias. Un alias estructural admite comparaciones de orden si todos sus componentes están ordenados; el orden es lexicográfico según la declaración.

La igualdad `==` y la desigualdad `!=` están disponibles aunque la representación no posea orden. `<`, `<=`, `>` y `>=` requieren una representación ordenada.

## Consecuencias

- El tipado de literales es dirigido por el tipo esperado.
- La elaboración debe distinguir literales sin tipo fijado de expresiones ya tipadas.
- La comparación aporta expectativas en ambas direcciones sin introducir coerciones implícitas.
- El AST tipado conserva el alias nominal incluso cuando su representación coincide con otro tipo.
- D-030 pasa a describir la rama cuantitativa de `to`; este ADR describe la rama nominal.

## Verificación futura

1. Construcción contextual simple y estructural.
2. Casting en ambos sentidos entre alias y representación.
3. Casting entre aliases compatibles.
4. Rechazo por forma incompatible o dominio de destino.
5. Formas posicional y nombrada completas.
6. Rechazo de reordenación, omisión, duplicado y componente extra.
7. Comparación con propagación desde ambos lados.
8. Rechazo de dos literales estructurales desnudos.
9. Rechazo de aliases nominales distintos sin `to`.
10. Igualdad y orden lexicográfico.
