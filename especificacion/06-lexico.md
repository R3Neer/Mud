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
questions: []
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
  - D-080
  - D-081
  - D-082
  - D-085
  - D-086
  - D-087
  - D-089
---

# 06. Estructura léxica

## Estado y propósito

Este capítulo define el scanner base y la clasificación contextual de formas fuente. El scanner base transforma Unicode en tokens sin consultar el modelo; `POINT_LITERAL` y `UNIT_FORM` se añaden únicamente en una vista contextual posterior conforme a D-089. La gramática léxica base está en [[gramatica/mud-lexico.ebnf]]. La sintaxis que consume las vistas significativas pertenece a [[07-gramatica-concreta]].

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
rule action subaction look message test
for on given when changes if then after with otherwise
mut unique ordered
create destroy add to remove from each by take
eventually through allowed old
is iis in
not and or xor
exists forall count sum min max
true false empty all _
Text Char Bool Thing Any Nat Int Num Rum Money
Name MudPath Anchor MudFile Prefix Rand
```

Los terminales `&`, `|`, `^`, `--`, `->`, `-->`, `~`, `=>` y `<=>` no son palabras. `-->` se reconoce por coincidencia más larga antes que `--` y `->`. También son tokens indivisibles `|=`, `&=`, `^=` y `--=`. `!` aislado no pertenece al léxico; `!=` continúa siendo un token indivisible de desigualdad y no se interpreta como la composición de negación y asignación.

El scanner aplica coincidencia más larga: `a--b` contiene el operador `--`, mientras que `a - -b` contiene resta y negación separadas. La forma parentizada `a - (-b)` es equivalente a esta última.

Son contextuales:

- `abstract` delante de `thing`.
- `always` delante de `rule`.
- `start` como parte de `start with`.
- `things` y `rules` como etiquetas obligatorias de sus secciones de `start with`.
- `value` dentro de los selectores y resultados de ramas funcionales `-->`.
- `name`, `path`, `anchor`, `file`, `plural`, `abbreviation`, `prefixes` y `format` después de `~` en las posiciones admitidas.
- `root`, `unit`, `point`, `over` y `cycle` en sus producciones propias.
- `Interval` inmediatamente después de una referencia de tipo dentro de `interval-type`.

`for`, `on` y `given` continúan siendo palabras reservadas duras, pero `metadata-name` las admite explícitamente después de `~` para las propiedades reflectivas `~for`, `~on` y `~given`. Esta excepción sintáctica no las convierte en `IDENTIFIER` ni permite usarlas como nombres ordinarios.

Fuera de esas posiciones pueden tokenizarse como `IDENTIFIER`. El clasificador no puede usar esta flexibilidad para aceptar una palabra reservada dura como nombre.

`ordered` es una palabra reservada dura tanto delante de `family` como dentro de una especificación de colección. No puede usarse como identificador en ningún otro contexto.

`all` es un literal contextual que requiere un dominio enumerable esperado. Su carácter reservado permite distinguirlo de una declaración ordinaria aun antes del tipado.

## Adyacencia de unidades

El scanner base no necesita conocer unidades para reconocer la frontera posterior a un número. Cuando la gramática de cantidad admite una unidad, el clasificador contextual de D-089 consulta el texto fuente desde ese offset y puede cubrir una forma habilitada sin exigir trivia intermedia. Por ello `3m`, `90km/h` y `r0.1m` obtienen la misma clasificación semántica que sus formas espaciadas. Fuera de una posición de unidad, `R2D2`, `ronto` y cualquier secuencia semejante conservan exclusivamente su tokenización base.

La forma canónica inserta un espacio entre número y primera unidad. Esta normalización pertenece al formateador, no al scanner base ni al resaltador.

## Clasificación contextual de formas fuente

> [!rule] MUD-LEX-012 — Independencia del scanner base
> El scanner base solo depende del texto Unicode y del léxico fijo de MUD. No consulta declaraciones, tipos esperados, `~format` ni catálogos de unidad. Todos sus tokens y trivia conservan offsets exactos en el texto fuente.

> [!rule] MUD-LEX-013 — Alternativa contextual por span
> `POINT_LITERAL` y `UNIT_FORM` son clasificaciones contextuales sobre spans del texto original. El clasificador puede cubrir una o varias unidades del tokenizado base, pero debe conservar el intervalo fuente exacto y no puede fabricar caracteres al recomponer tokens.

> [!rule] MUD-LEX-014 — Prioridad dirigida por contexto
> Una alternativa contextual existe únicamente cuando su contexto semántico satisface el contrato de D-089. Cuando un único tipo de punto esperado reconoce exactamente su `~format`, `POINT_LITERAL` prevalece sobre una interpretación ordinaria del mismo span. Sin contexto suficiente, esa alternativa no existe.

> [!rule] MUD-LEX-015 — Determinismo de unidad
> `UNIT_FORM` usa el catálogo semántico ya resuelto. El tipo esperado restringe candidatos; sin él la forma debe ser globalmente unívoca. Entre coincidencias compatibles de distinta longitud gana la forma completa más larga; dos candidatos distintos para el mismo span son ambiguos.

> [!rule] MUD-LEX-016 — Admisibilidad de formas fuente configurables
> El identificador declarado conserva la gramática ordinaria de identificador de unidad. Los valores no vacíos de `~name`, `~plural` y `~abbreviation` comparten un único criterio cuando participan como `UNIT_FORM`: pueden contener espacios U+0020 y puntuación, pero deben contener al menos un carácter alfabético y no pueden coincidir exactamente con una palabra clave de MUD. Un valor que no cumpla este contrato puede seguir siendo presentación, pero no se incorpora al catálogo de formas fuente.

> [!rule] MUD-LEX-017 — Unicidad intramagnitud tras prefijos
> Para cada magnitud, el conjunto de formas fuente de sus unidades se cierra bajo todas las combinaciones de prefijos habilitadas antes de comprobar unicidad. Dos unidades distintas no pueden generar la misma forma completa, directamente o por prefijado. La colisión es un error estático de la declaración de la magnitud y no se resuelve por orden de declaración ni por contexto de uso.

La arquitectura concreta puede usar token lattice, re-tokenización localizada o parsing diferido. Esas estrategias no son observables siempre que reproduzcan las reglas anteriores y el round-trip de la CST.

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

Todo `Text` es una plantilla. `{...}` contiene una expresión MUD ordinaria, que puede usar accesos postfix `~` como `~anchor`. No existe `anchor{...}`. Las llaves de código interpolado se equilibran y `\{`/`\}` escriben llaves literales. El scanner entrega `TEXT_START`, `TEXT_FRAGMENT`, `INTERPOLATION_START`, `INTERPOLATION_END` y `TEXT_END`.

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

Las formas de unidad pueden contener Unicode y no son identificadores generales. El scanner base conserva su tokenización textual ordinaria; únicamente el clasificador contextual de D-089 puede superponer `UNIT_FORM` en una posición donde la sintaxis de cantidad admita una unidad.

> [!warning]
> [[notas/decisiones/ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]] fija el catálogo de prefijos y las formas habilitadas. D-089 fija su reconocimiento sin dependencia circular: `UNIT_FORM` conserva la escritura encontrada y se selecciona contra el catálogo semántico ya resuelto.

`Prefix` es un tipo incorporado. Los nombres SI `quecto`…`quetta` permanecen identificadores ordinarios: en una expresión como `~prefixes = [kilo, milli]` se resuelven como valores incorporados de `Prefix`; no se convierten en palabras reservadas.

## Formas de magnitudes de punto

Una magnitud `point over` puede habilitar escrituras contextuales mediante su metadato `~format`, por ejemplo `12:30:00`. El clasificador contextual representa una coincidencia válida como `POINT_LITERAL`; el scanner base conserva su tokenización ordinaria.

> [!rule]
> `POINT_LITERAL` se interpreta contra el único tipo de magnitud de punto exigido por el contexto. Si declara `~format`, el texto debe coincidir exactamente con su representación canónica y el formato debe ser estáticamente invertible. La precisión inferior no representada toma valor cero.

Una magnitud de punto sin `~format` usa una cantidad ordinaria con una unidad compatible como coordenada completa. En ambos casos, la coordenada reconstruida debe pertenecer al dominio declarado. Los dominios cíclicos no normalizan literales fuera de rango: un literal equivalente a `26 hours` es inválido para `[0..24 hours) cycle`.

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

Dentro de una plantilla se aplica primero `\u{...}`, después los demás escapes, después `{` y por último el fragmento literal más largo posible. Dentro de una interpolación vuelve a aplicarse la prioridad ordinaria. La secuencia `anchor{` no posee tratamiento léxico especial.


## Palabras y tokens añadidos

`subaction` es palabra reservada. `Any`, `Name`, `MudPath`, `Anchor` y `MudFile` son nombres incorporados reservados. `value`, `things`, `rules`, `path` y `file` son contextuales en sus producciones propias. `_` es el fallback reservado de una rama funcional.

`iis` es palabra operadora reservada. `not in` e `iis not` conservan dos tokens de palabra; el parser agrupa cada pareja dentro de una comparación no encadenable.

```mud
value not in domain
value iis PersonId
value iis not PersonId
```

El scanner reconoce `-->` mediante coincidencia más larga antes que `--` y `->`:

```mud
selector --> result
key -> value
left -- right
```

`~` es un token postfix independiente:

```mud
value~name
value~anchor
```

Las plantillas solo abren interpolaciones ordinarias `{...}`. La forma especial `anchor{...}` y `ANCHOR_INTERPOLATION_START` no pertenecen al lenguaje. Un ancla se interpola mediante una expresión ordinaria:

```mud
"Rule: {CanRecruit~anchor}"
```
