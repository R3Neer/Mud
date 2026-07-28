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
  - Q-054
decisions:
  - D-034
  - D-035
  - D-050
  - D-056
  - D-057
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
| Namespace | `lowerCamelCase` |
| Declaración nominal | `PascalCase` |
| Miembro de `family` | `PascalCase` |
| Campo, rol, `given`, componente o variable | `lowerCamelCase` |

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
true false empty
Text Char Bool Natural Integer Number Rumber Money
Rand
```

Los terminales `&`, `|`, `^`, `=>` y `<=>` no son palabras. `!` aislado no pertenece al léxico; `!=` continúa siendo un token indivisible de desigualdad y no se interpreta como la composición de negación y asignación.

Son contextuales:

- `abstract` delante de `thing`.
- `always` delante de `rule`.
- `start` como parte de `start with`.
- `name`, `plural`, `abbreviation`, `prefixes`, `format`, `root`, `unit`, `point`, `over` y `cycle` en sus producciones propias.

Fuera de esas posiciones pueden tokenizarse como `IDENTIFIER`. El clasificador no puede usar esta flexibilidad para aceptar una palabra reservada dura como nombre.

`ordered` es una palabra reservada dura tanto delante de `family` como dentro de una especificación de colección. No puede usarse como identificador en ningún otro contexto.

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

Los comentarios se eliminan antes del parsing. Un comentario multilínea completo no emite los `NEWLINE` de su contenido.

## `Char`

Los literales usan comillas simples:

```mud
'a'
'ñ'
'\n'
'\u{1F642}'
```

> [!rule] MUD-LEX-025 — Un único escalar
> Después de interpretar escapes, un literal `Char` debe contener exactamente un valor escalar Unicode. La comilla final es obligatoria.

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

> [!rule] MUD-LEX-035 — Escape Unicode
> El valor de `\u{...}` debe encontrarse entre `U+0000` y `U+10FFFF` y no puede pertenecer al intervalo de sustitutos.

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

Los literales `Rumber` puros usan `r`:

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
> Q-054 todavía debe fijar prefijos, colisiones y la identidad estable de cada forma. La existencia del token contextual `UNIT_FORM` no resuelve esa semántica.

## Formas de magnitudes de punto

Una magnitud `point over` puede habilitar escrituras contextuales mediante su propiedad `format`, por ejemplo `12:30:00`. El lexer representa una coincidencia válida como `POINT_LITERAL`.

> [!warning]
> Q-055 todavía debe definir el minilenguaje de `format`, su parseo y la resolución de colisiones. Hasta entonces, `POINT_LITERAL` es un punto de extensión identificado, no una autorización para que cada implementación invente formatos distintos y los declare conformes.

## Prioridad del scanner

En una misma posición se intenta:

1. Delimitadores multilínea.
2. Operadores de tres caracteres.
3. Operadores de dos caracteres.
4. Literales `Rumber`, números e identificadores.
5. Operadores de un carácter.

Se elige la coincidencia válida más larga dentro de la misma categoría. Los comentarios y espacios horizontales se descartan; `NEWLINE` se conserva para decidir terminación.
