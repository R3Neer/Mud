# ADR-056 — `Char`, `Text` y orden Unicode

- Estado: Vigente
- Fecha: 2026-07-28
- Modificada por: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Cierra parcialmente: [[notas/08-preguntas-abiertas#Q-001 — Gramática y saltos de línea|Q-001]]
- Documentos afectados: [[especificacion/06-lexico]], [[especificacion/07-gramatica-concreta]], futuros capítulos 10 y 15

## Contexto

Modelar `Text` literalmente como `Char [* ordered]` confundiría dos conceptos distintos:

1. La posición de los caracteres en un texto.
2. La ordenación canónica de una colección.

Si ambas cosas fueran equivalentes, un texto ordinario como `"cba"` tendría que normalizarse o rechazarse por no estar ordenado.

## Decisión

### `Char`

`Char` es un tipo básico no numérico. Cada valor denota exactamente un valor escalar Unicode; no admite puntos de código sustitutos aislados.

Sus literales usan comillas simples:

```mud
'a'
'ñ'
'界'
'\n'
'\u{1F642}'
```

Después de interpretar escapes, un literal debe contener exactamente un valor escalar Unicode.

ASCII es el subconjunto de Unicode comprendido entre `U+0000` y `U+007F`. No constituye un tipo separado.

El valor predeterminado de `Char` es el escalar `U+0000`, escrito `'\u{0}'`. Es un valor ordinario de `Char`, no ausencia ni terminador de texto. MUD no introduce el escape especial `\0`; la escritura Unicode general ya expresa el valor sin importar una convención específica de C.

### Orden

El orden natural de `Char` es el orden creciente de su valor escalar Unicode. Por tanto, en una colección:

```mud
letters: Char [* ordered] = "abc"
```

`ordered` exige ese orden canónico. Esta inicialización es inválida:

```mud
letters: Char [* ordered] = "cba"
```

`ordered by` no se admite para `Char`: no puede reemplazar su orden Unicode natural.

### `Text`

`Text` continúa siendo un tipo básico distinto. Denota una secuencia finita de valores `Char` y conserva el orden posicional escrito:

```mud
word: Text = "cba"
```

Este valor sigue siendo `"cba"`. En particular:

$$
\mathsf{Text}
\not\equiv
\mathsf{Char}[\ast\ \mathsf{ordered}]
$$

`Text` puede exponer operaciones de secuencia como indexación, pertenencia, longitud e iteración sin convertirse por ello en una colección ordenada canónicamente. No admite modificadores de colección ni `ordered by`.

El operador `|` concatena valores `Text`. Los operadores conjuntistas `&`, `^` y `-` no se aplican a `Text`. Un alias nominal basado en `Text` necesita una conversión explícita a `Text` para concatenar y otra al alias de destino.

Los literales `Text` son además plantillas conforme a D-061. Sus fragmentos literales y los valores interpolados producen una única secuencia de `Char`; esta elaboración no convierte `Text` en una colección ni introduce conversiones implícitas generales.

## Consecuencias

- El lexer incorpora literales `Char` separados de los literales `Text`.
- El sistema de tipos incorpora `Char` entre los tipos básicos no numéricos.
- La iteración de `Text` conserva posición; la enumeración de `Char [* ordered]` usa Unicode.
- Una materialización no puede ordenar texto como efecto de su representación.
- El orden Unicode se define por escalares, no por idioma, colación, grafema visible ni normalización cultural.

## Verificación

1. Literales ASCII y no ASCII válidos.
2. Rechazo de cero o varios escalares tras interpretar escapes.
3. Rechazo de sustitutos Unicode aislados.
4. Confirmación de que ASCII ocupa `U+0000`–`U+007F`.
5. Conservación de `"cba"` como `Text`.
6. Rechazo de `"cba"` como valor de `Char [* ordered]`.
7. Rechazo de `ordered by` para `Char` y de modificadores de colección sobre `Text`.
8. Predeterminado `'\u{0}'` de `Char` y rechazo de `'\0'` como escape no declarado.
9. Conservación posicional de fragmentos literales e interpolados dentro de una plantilla.
