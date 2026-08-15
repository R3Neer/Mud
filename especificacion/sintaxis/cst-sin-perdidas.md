---
title: CST sin pérdidas
aliases:
  - Árbol de sintaxis concreta
  - Lossless CST
tags:
  - mud/especificacion
  - mud/sintaxis
status: propuesta
normative: true
depends-on:
  - 03-notacion
  - 05-texto-fuente
  - 06-lexico
  - 07-gramatica-concreta
  - gramatica/mud-lexico.ebnf
  - gramatica/mud.ebnf
questions: []
decisions:
  - D-070
  - D-071
  - D-085
  - D-086
  - D-087
---

# CST sin pérdidas

## Estado y propósito

Este documento define la estructura concreta que conserva un archivo MUD después del análisis léxico y sintáctico. La CST permite reconstruir el flujo original de bytes, mantener comentarios y formato, ofrecer diagnósticos locales y sostener herramientas de edición sin atribuir significado semántico a la disposición física del texto.

La CST es **por archivo**. Un proyecto puede contener varias CST, pero no existe una única CST que abarque físicamente varios archivos.

## Dependencias y autoridad

La autoridad se reparte de esta manera:

- [[mud-lexico]] define qué secuencias forman elementos léxicos.
- [[mud]] define las producciones sintácticas.
- [[06-lexico]] define los algoritmos modales y las reglas que no caben en EBNF.
- [[07-gramatica-concreta]] define precedencia, asociatividad y restricciones contextuales de parsing.
- `mud-syntax-kinds.yaml` mantiene el inventario mecánico de las categorías CST.
- Este documento define el modelo común, la conservación de texto y la recuperación.

Una divergencia entre esos archivos es un defecto de la especificación y debe detectarse mediante `validate_syntax_model.py`.

Entre las categorías concretas inventariadas se encuentra `BooleanBlockSyntax`, que conserva en orden las declaraciones locales iniciales y la expresión booleana final. La CST no amplía por sí sola su ámbito hasta `otherwise`; esa relación se establece al proyectar y resolver la construcción propietaria.

## Terminología

> [!definition] Token significativo
> Elemento léxico que consume la gramática concreta: palabras, identificadores, literales, operadores, delimitadores, `TERMINATOR` y `EOF`.

> [!definition] Trivia
> Texto fuente conservado que no participa como terminal de la gramática: espacio horizontal y comentarios. La trivia mantiene su escritura exacta, incluidos delimitadores y saltos interiores.

> [!definition] Anchura completa
> Intervalo desde el comienzo de la trivia inicial de un elemento hasta el final de su último token o hijo.

> [!definition] Span sintáctico
> Intervalo de los tokens significativos propios del elemento, sin incluir la trivia inicial que pertenece al primer token.

> [!definition] Token sintético
> Token de anchura cero introducido por una regla normativa —como un `TEXT_END` implícito— o por recuperación de errores.

## Dos vistas del análisis léxico

El scanner produce conceptualmente un flujo completo:

```text
trivia* token trivia* token ... trivia* EOF
```

La vista significativa filtra la trivia y es la que consume la gramática:

```text
token token ... EOF
```

Los comentarios se eliminan de la **vista significativa**, no de la representación completa. Por tanto, la frase «los comentarios se eliminan antes del parsing» debe entenderse como «no se presentan al reconocedor como terminales».

## Modelo abstracto

Una implementación conforme puede usar árboles verdes, árboles rojos, arenas, índices o clases ordinarias. Debe ser observacionalmente equivalente al modelo siguiente:

```text
SyntaxTree
    source: SourceId
    root: SyntaxNode
    diagnostics: Diagnostic*

SyntaxElement
    = SyntaxNode
    | SyntaxToken

SyntaxNode
    kind: SyntaxKind
    children: SyntaxElement*
    span: SourceSpan
    fullSpan: SourceSpan

SyntaxToken
    kind: TokenKind
    text: bytes UTF-8
    leadingTrivia: SyntaxTrivia*
    span: SourceSpan
    fullSpan: SourceSpan
    origin: Written | ImplicitTextEnd | MissingForRecovery

SyntaxTrivia
    kind: TriviaKind
    text: bytes UTF-8
    span: SourceSpan
```

`SyntaxNode.children` conserva el orden físico. La puntuación y las palabras clave son hijos reales; no se reconstruyen mediante conocimiento del `kind`.

## Propiedad de pérdida cero

Sea `bytes(t)` la concatenación, en recorrido de izquierda a derecha, de:

1. La trivia inicial de cada token.
2. El texto del token cuando su origen sea `Written`.
3. Ningún byte para tokens sintéticos.

Para toda entrada UTF-8 aceptada léxicamente:

```text
bytes(CST(source)) = sourceBytesWithoutConsumedBOM
```

El BOM se conserva como metadato de archivo porque solo puede aparecer antes del primer elemento. La forma física de los saltos (`LF`, `CRLF` o `CR`) permanece en los bytes de los tokens `TERMINATOR` o de la trivia que los contiene.

## Asignación de trivia

MUD usa una regla única y determinista:

> [!rule] MUD-CST-001 — Propiedad de trivia
> Toda trivia situada entre dos tokens significativos pertenece como `leadingTrivia` al token de la derecha. La trivia anterior al primer token pertenece a ese token. La trivia posterior al último token pertenece a `EOF`.

Ejemplo:

```mud
health # explicación # : Nat
```

se representa conceptualmente:

```text
IDENTIFIER("health")
COLON(leadingTrivia = [" ", "# explicación #", " "])
IDENTIFIER("Nat", leadingTrivia = [" "])
EOF
```

Esta regla evita decisiones dependientes de la clase de comentario. Una implementación puede ofrecer una vista derivada de trivia final, pero la serialización normativa utiliza la propiedad anterior.

## Clases de trivia

El catálogo mínimo es:

- `HorizontalWhitespaceTrivia`.
- `OpenLineCommentTrivia`.
- `ClosedLineCommentTrivia`.
- `MultilineCommentTrivia`.
- `SkippedTokensTrivia`, únicamente para recuperación.

Un comentario multilínea conserva sus delimitadores, sangría y saltos internos en un solo elemento de trivia. Sus saltos no producen `TERMINATOR`, conforme a [[06-lexico]].

## `TERMINATOR`

`TERMINATOR` es un token significativo porque interviene en `required-separation`. Su texto conserva la escritura física que lo originó:

- `LF`.
- `CRLF`.
- `CR`.
- `;` cuando la gramática y el scanner lo clasifiquen como terminador.

Los terminadores ignorados por `layout` continúan presentes como tokens dentro de la CST.

## Literales `Text`

Los tokens producidos por el scanner modal se conservan:

- `TEXT_START`.
- `TEXT_FRAGMENT`.
- `INTERPOLATION_START`.
- `INTERPOLATION_END`.
- `TEXT_END`.

Un cierre implícito ante salto o fin de archivo produce un `TEXT_END` sintético de anchura cero con origen `ImplicitTextEnd`. La CST conserva así la distinción concreta entre:

```mud
"Ada"
```

y la forma cerrada implícitamente:

```mud
"Ada
```

El AST superficial normaliza ambas al mismo valor de plantilla.

## Categorías CST

Cada producción de `mud.ebnf` posee una categoría `PascalCaseSyntax` inventariada en `mud-syntax-kinds.yaml`. Por ejemplo:

```text
thing-declaration        → ThingDeclarationSyntax
thing-body               → ThingBodySyntax
thing-body-declaration   → ThingBodyDeclarationSyntax
metadata-assignment       → MetadataAssignmentSyntax
stored-field-declaration → StoredFieldDeclarationSyntax
postfix-expression       → PostfixExpressionSyntax
```

Las producciones auxiliares también tienen categoría, aunque una implementación optimizada pueda representarlas mediante vistas tipadas sobre un nodo genérico.

El catálogo no obliga a generar una clase física por producción. Sí obliga a que:

- La agrupación sea observable.
- Los hijos puedan recorrerse en orden.
- Los tokens concretos sean recuperables.
- La categoría declarada sea identificable.

## Nodos especiales de recuperación

Además de las producciones gramaticales existen:

### `ErrorSyntax`

Agrupa una región para la que el parser no pudo seleccionar una producción válida, sin descartar sus tokens.

### `SkippedTokensSyntax`

Conserva tokens inesperados que se saltaron hasta un punto de sincronización.

Una implementación puede codificar `SkippedTokensSyntax` como `SkippedTokensTrivia` cuando no cambie:

- La reconstrucción exacta.
- El orden.
- Los spans.
- La capacidad de emitir el diagnóstico en la posición correcta.

## Tokens ausentes

> [!rule] MUD-CST-002 — Token ausente
> Cuando la recuperación presuponga un token obligatorio no escrito, la CST contendrá un token del tipo esperado, texto vacío, span de anchura cero y origen `MissingForRecovery`.

Ejemplo:

```mud
thing Person {
    label Text
}
```

puede representarse con un `COLON` ausente entre `label` y `Text` y un diagnóstico asociado.

Un token ausente nunca se serializa como si lo hubiera escrito el usuario.

## Puntos de sincronización

El parser puede sincronizar en:

- `TERMINATOR` al nivel de declaraciones y sentencias.
- `,` dentro de listas.
- `)`, `]` o `}` para la construcción delimitada correspondiente.
- El comienzo inequívoco de otra declaración de primer nivel.
- `EOF`.

La elección concreta puede variar si conserva la misma región de error y no produce un AST normativo para una construcción inválida.

## CST de archivos inválidos

La construcción de CST no implica validez. Debe ser posible obtener una CST para entradas con errores sintácticos recuperables.

La cadena de fases es:

```text
bytes UTF-8
→ scanner completo
→ CST sin pérdidas
→ validación sintáctica contextual
→ AST superficial normalizado
```

Un archivo puede tener CST y no producir un AST superficial completo.

## Validación sintáctica contextual

La validación situada después de la CST y antes del AST comprueba condiciones que no merece la pena codificar como expansión EBNF, entre ellas:

- Modificadores de colección duplicados.
- Dos criterios `ordered` incompatibles.
- Declaraciones de metadatos duplicadas en un mismo propietario, incluidas las unidades.
- Propiedades obligatorias ausentes.
- Mezcla de argumentos posicionales después de un argumento nombrado.
- Combinaciones que la prosa de sintaxis concreta prohíba.
- Capitalización exigida por categoría cuando todavía se clasifique como regla sintáctica contextual.

La validación de nombres existentes, tipos, dominios y efectos pertenece a fases posteriores.

## Spans

Los offsets de `SourceSpan` son:

- Basados en cero.
- Medidos en bytes UTF-8.
- De extremo final exclusivo.

Las líneas y columnas también comienzan en cero. La columna cuenta valores escalares Unicode desde el inicio lógico de la línea. Una interfaz LSP convierte a unidades UTF-16 en su frontera; esa conversión no modifica el modelo normativo.

Para un token escrito:

```text
span.start.byteOffset < span.end.byteOffset
```

salvo tokens textualmente vacíos permitidos. Para un token sintético:

```text
span.start = span.end
```

`fullSpan` comienza en la primera trivia inicial y termina al final del token. El `span` de un nodo va desde el primer token significativo hasta el último. Si todos sus tokens son sintéticos, se ancla en el punto de recuperación.

## Orden y archivos

La CST conserva siempre el orden fuente:

- `using`.
- Declaraciones.
- Antecesores.
- Campos.
- Miembros.
- Argumentos.
- Efectos.
- Aserciones.

La ausencia de significado semántico del orden de ciertas listas no autoriza a ordenarlas en la CST.

## Comentarios documentales futuros

MUD 1.0 no define comentarios documentales estructurados. Todos los comentarios actuales son trivia ordinaria. Una extensión futura puede:

- Clasificar una forma de comentario como documentación.
- Construir un árbol documental separado.
- Asociarlo a un propietario sintáctico.
- Resolver referencias breves a anclas.

Esa extensión no convertirá los comentarios ordinarios en declaraciones del AST ejecutable.

## Correspondencia con el AST

La CST no realiza:

- Desazucarado.
- Resolución de nombres.
- Inferencia de tipos.
- Clasificación elemental o compuesta de acciones.
- Interpretación de una tupla como receptores múltiples.
- Cálculo de predeterminados.
- Ordenación canónica de archivos.

La transformación normativa está en [[cst-a-ast-superficial]].

## Conformidad

Un frontend conforme debe satisfacer:

1. Reconstrucción exacta del archivo, salvo el BOM separado como metadato.
2. Inventario de todas las producciones alcanzables.
3. Conservación de trivia y tokens inesperados.
4. Spans coherentes y finales exclusivos.
5. Distinción entre tokens escritos y sintéticos.
6. Ausencia de decisiones de resolución o tipado en la CST.
7. Resultado compatible con las normalizaciones del AST superficial.


## Tokens añadidos y retirados por D-085

La CST conserva los tokens fijos `-->` y `~`, la palabra operadora `iis` y las palabras contextuales escritas en sus posiciones ordinarias. La coincidencia más larga debe impedir que `-->` se divida en `--` y `>` o en `-` y `->`. `not in` e `iis not` conservan dos tokens con trivia propia. No existe `ANCHOR_INTERPOLATION_START`; una expresión `~anchor` dentro de `{...}` usa los mismos nodos y tokens que fuera de una plantilla.
