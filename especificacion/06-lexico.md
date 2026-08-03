---
title: Estructura léxica
aliases:
  - Léxico de MUD
tags:
  - mud/especificacion
  - mud/lexico
status: propuesta
normative: true
depends-on:
  - "[[05-texto-fuente]]"
questions:
decisions:
  - D-034
  - D-035
  - D-050
  - D-056
  - D-057
  - D-061
  - D-062
  - D-067
  - D-068
  - D-069
  - D-076
  - D-070
---

# 06. Estructura léxica

## Estado y propósito

Este capítulo define cómo se transforma un flujo Unicode en tokens. La gramática normativa está en [[gramatica/mud-lexico.ebnf]]. La sintaxis que consume esos tokens pertenece a [[07-gramatica-concreta]].

## Valores escalares Unicode

> [!definition] Valor escalar Unicode
> Es un punto de código Unicode excepto el intervalo reservado a sustitutos `U+D800`–`U+DFFF`.

> [!rule] MUD-LEX-010 — Unicode válido
> El texto fuente debe decodificarse como UTF-8 válido. Un sustituto aislado o una secuencia UTF-8 mal formada es un error léxico.

ASCII es el subconjunto Unicode `U+0000`–`U+007F`.

## Identificadores

La forma léxica de un identificador es:

```ebnf
identifier ::= ascii-letter , { ascii-letter | digit } ;
```

> [!rule] MUD-LEX-011 — Identificadores ASCII
> Los identificadores solo pueden contener letras ASCII y cifras, deben comenzar por letra y no pueden contener `_`.

Son sensibles a mayúsculas. `Kingdom`, `kingdom` y `KINGDOM` son tres escrituras distintas.

La convención comprobable por categoría es:

| Categoría | Forma |
| --- | --- |
| Segmento de path de MUD | `lowerCamel` |
| Declaración nominal | `PascalCase` |
| Miembro de `family` | `PascalCase` |
| Unidad, campo, rol, `given`, componente o variable | `lowerCamel` |

Un nombre que incumpla la capitalización es un error estático, no una tokenización alternativa.

## Palabras reservadas y contextuales

Las palabras reservadas no pueden usarse como identificadores. El catálogo normativo es:

```text
using
thing as alias family magnitude
rule action look message test
for on given when changes if then after with otherwise
mut unique ordered
create destroy add to remove from each by
eventually through allowed old
is in
not and or xor
exists forall count sum min max
true false empty all
Text Char Bool Thing Nat Int Num Rum Money
Rand
```

Los terminales `&`, `|`, `^`, `=>` y `<=>` no son palabras. `!` aislado no pertenece al léxico; `!=` continúa siendo un token indivisible de desigualdad y no se interpreta como la composición de negación y asignación.

Son contextuales:

- `abstract` delante de `thing`.
- `always` delante de `rule`.
- `start` como parte de `start with`.
- `name` delante de `=` dentro del cuerpo de una `thing` y en las etiquetas declarativas que lo admiten.
- `name`, `plural`, `abbreviation`, `prefixes`, `format`, `root`, `unit`, `point`, `over` y `cycle` en sus producciones propias.
- `anchor` inmediatamente antes de `{` dentro de una plantilla `Text`.
- `Interval` inmediatamente después de una referencia de tipo dentro de `interval-type`.

Fuera de esas posiciones pueden tokenizarse como `IDENTIFIER`. El clasificador no puede usar esta flexibilidad para aceptar una palabra reservada dura como nombre.

`ordered` es una palabra reservada dura tanto delante de `family` como dentro de una especificación de colección. No puede usarse como identificador en ningún otro contexto.

`all` es un literal contextual que requiere un dominio enumerable esperado. Su carácter reservado permite distinguirlo de una declaración ordinaria aun antes del tipado.

## Adyacencia de unidades

Después de reconocer un literal numérico, el flujo significativo puede reconocer inmediatamente una forma de unidad habilitada, sin exigir trivia intermedia. Por ello `3m`, `90km/h` y `r0.1m` producen los mismos tokens significativos que sus formas espaciadas. Un identificador alfanumérico completo conserva prioridad fuera de esa frontera; `R2D2` y `ronto` no se dividen como número y unidad.

La forma canónica inserta un espacio entre número y primera unidad. Esta normalización pertenece al formateador, no al resaltador léxico.

## Comentarios

### Comentario hasta el salto

```mud
# Todo lo restante de la línea es comentario
```

### Comentario de línea cerrado

```mud
value = 1 # explicación # + 2
```

El segundo `#` reanuda el tokenizado de la misma línea. Esta forma nunca atraviesa un salto.

### Comentario multilínea

```mud
###
El contenido puede ocupar varias líneas.
No se anida.
###
```

> [!rule] MUD-LEX-020 — Apertura de comentario multilínea
> El `###` de apertura debe ser el último contenido no blanco de su línea.

> [!rule] MUD-LEX-021 — Cierre de comentario multilínea
> El `###` de cierre debe ser el único contenido no blanco de su línea.

> [!rule] MUD-LEX-022 — No anidamiento
> El primer cierre válido termina el comentario. Un `###` interior no abre otro nivel.

La forma siguiente es inválida:

```mud
### comentario ###
```

Los comentarios no emiten tokens significativos para la gramática, pero se conservan con su texto exacto como trivia en el flujo léxico completo y en la CST sin pérdidas. Un comentario multilínea completo no emite tokens significativos `NEWLINE`; sus saltos interiores permanecen dentro de la trivia del comentario.

## Flujo completo, flujo significativo y trivia

El scanner ofrece dos vistas sincronizadas:

```text
flujo completo      = trivia y tokens significativos en orden fuente
flujo significativo = tokens que consume mud.ebnf
```

La CST se construye con el flujo completo. La gramática consume la vista significativa.

La trivia mínima es:

- Espacio horizontal.
- Comentario abierto de línea.
- Comentario cerrado de línea.
- Comentario multilínea.

Toda trivia pertenece al token significativo siguiente. `EOF` posee la trivia final. Esta convención es normativa para serialización sin pérdidas, aunque una API pueda exponer vistas derivadas de trivia final.

## Tokens sintéticos

Un `TEXT_END` cerrado implícitamente se emite como token sintético de anchura cero y origen `ImplicitTextEnd`. La recuperación del parser puede introducir tokens esperados de anchura cero con origen `MissingForRecovery`; estos últimos no convierten una construcción inválida en un AST normativo.

## `Char`

`Char` comparte con `Text` los literales ordinarios entre comillas dobles:

```mud
letter: Char = "a"
letterEnye: Char = "ñ"
newline: Char = "\n"
face: Char = "\u{1F642}"
```

> [!rule] MUD-LEX-025 — Un único escalar
> Un literal ordinario puede elaborarse como `Char` cuando el contexto lo exige y, después de interpretar escapes, contiene exactamente un valor escalar Unicode. La comilla final explícita es obligatoria y no admite interpolaciones. Sin contexto `Char`, la misma escritura tiene tipo `Text`.

La forma multilínea siempre es `Text`. Las comillas simples no delimitan ningún literal de MUD.

Su orden natural es el valor escalar creciente. No es colación lingüística ni orden por grafemas.

## `Text`

### Forma ordinaria

Un literal comienza por `"`. Puede cerrarse expresamente en la misma línea:

```mud
"Ada"
```

o cerrarse implícitamente antes del salto:

```mud
"Ada
```

Ambos denotan el mismo `Text`. Si después del contenido deben aparecer un operador, delimitador o comentario, la comilla final es obligatoria:

```mud
greeting = "Hello" | ", world"
name = "Ada" # comentario
```

Sin la primera comilla de cierre, `| ", world"` sería contenido. Sin la segunda, `# comentario` también lo sería.

### Forma multilínea

```mud
description = """
    First line.
      Second line with two extra spaces.
    """
```

> [!rule] MUD-LEX-030 — Apertura multilínea
> `"""` debe ser el último contenido no blanco de su línea. El valor comienza en la línea siguiente.

> [!rule] MUD-LEX-031 — Cierre multilínea
> El `"""` final debe ser el único contenido no blanco de su línea.

> [!rule] MUD-LEX-032 — Margen
> La sangría horizontal anterior al cierre define el margen. Se elimina exactamente ese prefijo de cada línea no vacía. Una línea no vacía con menos margen es inválida.

> [!rule] MUD-LEX-033 — Saltos estructurales
> El salto posterior al inicio y el inmediatamente anterior al cierre no forman parte del valor. Los demás sí.

> [!rule] MUD-LEX-034 — Contenido
> Una comilla ordinaria no cierra la forma multilínea. Solo `"""` en una línea de cierre válida lo hace.

`Text` conserva la posición de sus caracteres. No equivale a `Char [* ordered]`.

### Plantillas e interpolación

Todo literal `Text`, ordinario o multilínea, es una plantilla. Un fragmento `{...}` abandona temporalmente el modo de texto y contiene una expresión MUD ordinaria. La forma contextual `anchor{...}` contiene un designador de ancla. Ambas vuelven al modo de texto tras su llave de cierre:

```mud
"Kingdom: {kingdom}"
"Population: {kingdom.population:6}"
"Rule: anchor{CanRecruit}"
```

> [!rule] MUD-LEX-036 — Modos anidados de plantilla
> El scanner mantiene una pila de modos de texto y código. Las llaves del código interpolado se equilibran normalmente y un literal `Text` dentro de ese código abre un modo de plantilla anidado. Un salto o fin de archivo no puede cerrar implícitamente un texto ordinario mientras quede abierta una interpolación.

Dentro del contenido literal, una `{` abre una interpolación y la secuencia exacta `anchor{` abre una interpolación de ancla. Cualquier llave que deba formar parte del texto se escribe mediante `\{` o `\}`. Una llave cruda que no pueda formar o cerrar el hueco correspondiente es un error.

El escape Unicode `\u{...}` se reconoce como una unidad antes de buscar delimitadores de interpolación.

El scanner entrega al parser `TEXT_START`, `TEXT_FRAGMENT`, `INTERPOLATION_START`, `ANCHOR_INTERPOLATION_START`, `INTERPOLATION_END` y `TEXT_END`. El último puede ser sintético cuando el texto ordinario se cierra ante un salto o el fin de archivo. La forma multilínea usa el mismo flujo de tokens después de aplicar sus reglas de margen y saltos estructurales.

## Escapes

Las formas mínimas son:

| Escape | Valor |
| --- | --- |
| `\\` | barra inversa |
| `\"` | comilla doble |
| `\'` | comilla simple |
| `\n` | salto `LF` |
| `\r` | retorno `CR` |
| `\t` | tabulador |
| `\u{H...}` | escalar escrito con una o más cifras hexadecimales |
| `\{` | llave de apertura literal en `Text` |
| `\}` | llave de cierre literal en `Text` |

> [!rule] MUD-LEX-035 — Escape Unicode
> El valor de `\u{...}` debe encontrarse entre `U+0000` y `U+10FFFF` y no puede pertenecer al intervalo de sustitutos.

Los escapes de llaves forman parte de la sintaxis textual común. Un literal que, después de procesarlos, contenga exactamente una llave puede elaborarse como `Char` en el contexto correspondiente.

## Números

Los signos son operadores externos. Por ejemplo:

```mud
-10
-r0.5
```

No son válidos `r-10` ni un signo incrustado en el token.

Los racionales exactos admiten parte decimal y exponente:

```mud
10
0.25
.5
3e6
1e-6
```

Los literales `Rum` puros usan `r`:

```mud
r10
r0.25
r.5
r1e-6
```

> [!rule] MUD-LEX-040 — Exponente decimal
> Si una mantisa $m$ lleva un exponente entero $n$ introducido por `e` o `E`, el literal denota $m\times 10^n$. El signo opcional situado inmediatamente después del introductor pertenece al exponente; los signos aplicados al valor completo continúan siendo operadores externos.

Por ejemplo, `3e6` denota `3_000_000` y `3e-6` denota `0.000_003`.

La parte entera de la mantisa, su parte fraccionaria y las cifras del exponente son tres componentes independientes a efectos de agrupación.

> [!rule] MUD-LEX-041 — Agrupación numérica completa
> Cada componente puede escribirse sin `_` o agruparse mediante `_`. Si un componente contiene `_`, todas sus cifras deben quedar agrupadas dentro de ese componente. La presencia de `_` en uno no obliga a agrupar los demás.
>
> La parte entera y el exponente se agrupan desde la derecha: el primer grupo contiene de una a tres cifras y todos los posteriores contienen exactamente tres. La parte fraccionaria se agrupa desde el punto decimal hacia la derecha: todos los grupos salvo el último contienen exactamente tres cifras y el último contiene de una a tres.

Son válidos:

```mud
1_000
r1_000.25
1_000.123456e1000
1000.123_456
3e1_000
```

Son inválidos `_1`, `1_`, `1__000`, `1_.0`, `1_000000`, `1.123_456789` y `3e1_000000`.

## Unidades

Las formas de unidad pueden contener Unicode y no son identificadores generales. Se reconocen contextualmente contra el catálogo construido a partir de las declaraciones `magnitude`.

> [!warning]
> [[notas/decisiones/ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]] fija el catálogo de prefijos, la resolución de colisiones y la identidad estable. `UNIT_FORM` conserva la escritura encontrada; la resolución semántica selecciona después una unidad declarada o una forma prefijada estructural.

## Formas de magnitudes de punto

Una magnitud `point over` puede habilitar escrituras contextuales mediante su propiedad `format`, por ejemplo `12:30:00`. El lexer representa una coincidencia válida como `POINT_LITERAL`.

> [!rule]
> `POINT_LITERAL` se interpreta contra el único tipo de magnitud de punto exigido por el contexto. Si declara `format`, el texto debe coincidir exactamente con su representación canónica y el formato debe ser estáticamente invertible. La precisión inferior no representada toma valor cero.

Una magnitud de punto sin `format` usa una cantidad ordinaria con una unidad compatible como coordenada completa. En ambos casos, la coordenada reconstruida debe pertenecer al dominio declarado. Los dominios cíclicos no normalizan literales fuera de rango: un literal equivalente a `26 hours` es inválido para `[0..24 hours cycle)`.

Las reglas completas pertenecen a [[notas/decisiones/ADR-062-literales-canonicos-de-magnitudes-de-punto|D-062]].

## Spans léxicos

Todo token y trivia posee `SourceSpan`. El texto de un token escrito ocupa exactamente su intervalo de bytes. Un token sintético tiene inicio y final iguales. El `fullSpan` de un token comienza en su primera trivia inicial.

La decodificación de escapes o la normalización de margen de `Text` no cambia los spans de sus tokens concretos; el valor decodificado pertenece al AST.

## Prioridad del scanner

En una misma posición se intenta:

1. Delimitadores multilínea.
2. Operadores de tres caracteres.
3. Operadores de dos caracteres.
4. Literales `Rum`, números e identificadores.
5. Operadores de un carácter.

Se elige la coincidencia válida más larga dentro de la misma categoría. Los comentarios y espacios horizontales se excluyen del flujo significativo, pero se conservan como trivia en el flujo completo; `NEWLINE` se conserva como token significativo para decidir terminación.

Dentro de una plantilla se aplica primero `\u{...}`, después los demás escapes, después `anchor{` y `{`, y por último el fragmento literal más largo posible. Dentro de una interpolación vuelve a aplicarse la prioridad ordinaria.
