---
id: D-050
title: "Comentarios, terminadores, texto y separadores numéricos"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-001"
affects:
  - "[[especificacion/06-lexico]], [[especificacion/07-gramatica-concreta]], formateador"
---
# ADR-050 — Comentarios, terminadores, texto y separadores numéricos

- Relacionada con: [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]], [[notas/decisiones/ADR-056-char-texto-y-orden-unicode|D-056]], [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|D-057]]
- Modificada por: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Cierra parcialmente: [[notas/preguntas/Q-001-gramatica-y-saltos-de-linea|Q-001]]
- Documentos afectados: [[especificacion/06-lexico]], [[especificacion/07-gramatica-concreta]], formateador

## Contexto

Estas reglas léxicas son independientes de la ontología y deben quedar fijadas sin mantener manualmente un catálogo paralelo de palabras clave. Los delimitadores de comentario y texto siguen una simetría deliberada entre formas ordinarias y multilínea.

## Decisión

### Comentarios

MUD admite:

1. Comentario de línea desde `#` hasta el salto de línea.
2. Comentario de línea cerrado por un segundo `#` antes del salto.
3. Comentario multilínea cuyo delimitador de apertura y cierre es `###`.

```mud
soldiers = 1_000 # hasta fin de línea
soldiers = 1_000 # comentario # morale = 100
###
Comentario multilínea.
###
```

El `###` de apertura debe ser el último elemento no blanco de su línea. El contenido comienza en la línea siguiente. El `###` de cierre debe aparecer solo, salvo espacio horizontal, en su propia línea. La línea de apertura y la de cierre no forman parte del comentario. La forma `### comentario ###` es inválida.

Los comentarios multilínea no se anidan. El lexer reconoce `###` antes que `#`. Dentro de un literal `Text` o `Char`, los delimitadores de comentario no tienen significado léxico.

El contenido de un comentario no genera tokens, instrucciones ni terminadores. Después de retirarlo, el texto restante debe seguir siendo sintácticamente válido.

Un comentario de línea cerrado explícitamente no atraviesa un salto. Un delimitador multilínea sin pareja, un inicio con contenido en su misma línea o un cierre que no esté aislado producen diagnóstico.

### Literales de texto

Un literal ordinario de `Text` comienza con `"`. Puede cerrarse con otro `"` en la misma línea o cerrarse implícitamente al llegar al salto:

```mud
name = "Ada"
name = "Ada
```

Ambas formas producen el mismo valor. El cierre explícito es obligatorio cuando deben aparecer otros tokens en esa línea.

Un literal multilínea utiliza `"""`. El delimitador de apertura debe ser el último elemento no blanco de su línea; el contenido comienza en la siguiente. El cierre debe aparecer aislado, salvo espacio horizontal, en su propia línea.

```mud
description = """
    First line.
      Indented line.
    """
```

La sangría del delimitador de cierre define el margen que se retira de cada línea no vacía. Una línea no vacía con menos sangría que el margen es un error. La primera línea posterior al inicio y el salto inmediatamente anterior al cierre son estructurales y no forman parte del valor. La sangría adicional se conserva. Los escapes y las interpolaciones de D-061 continúan activos.

Un literal `Char` usa comillas simples y, después de procesar escapes, debe contener exactamente un valor escalar Unicode conforme a D-056.

### Terminadores

Una instrucción termina mediante `;` o un salto de línea.

El salto no actúa como terminador cuando aparece dentro de una construcción sintácticamente abierta. Un prefijo está abierto cuando todavía no puede formar una unidad sintáctica completa, pero puede completarse con tokens posteriores. La gramática de D-057 proporciona la enumeración exhaustiva. Incluye:

- Un delimitador `(` o `[` todavía sin cerrar.
- Una cabecera que todavía exige participantes, argumentos u otro contenido.
- Una línea terminada en coma u operador que exige un operando posterior.
- Una cabecera o cláusula terminada en una palabra que exige contenido, como `for`, `given`, `if`, `then` o `:=`.
- El contenido de un literal o comentario multilínea.

Las llaves `{}` no suprimen los terminadores de su interior: un bloque contiene instrucciones o declaraciones separadas por saltos o `;`.

Si el prefijo anterior al salto ya puede formar una unidad completa, el salto la termina aunque la línea siguiente pudiera comenzar otra expresión. La continuación nunca depende de la sangría.

```mud
rule CanAttack for
    attacker: Army,
    defender: Army
{
    attacker.strength >
        defender.strength
}
```

D-057 y la gramática consolidada cierran Q-001.

### Separadores numéricos

La notación científica usa `e` o `E`: una mantisa $m$ seguida de un exponente entero $n$ denota $m\times 10^n$. El signo opcional situado tras `e` o `E` pertenece al exponente; el signo del valor completo continúa siendo un operador exterior.

`_` puede agrupar cifras para lectura y no altera el valor. La parte entera de la mantisa, su parte fraccionaria y las cifras del exponente se agrupan independientemente: usar `_` en un componente no obliga a usarlo en los demás.

Cuando un componente contiene `_`, su agrupación debe ser completa. La parte entera y el exponente se agrupan desde la derecha, con un primer grupo de una a tres cifras y los restantes de tres. La parte fraccionaria se agrupa desde el punto decimal hacia la derecha, con grupos de tres salvo el último, que puede contener de una a tres cifras.

Por tanto, `1_000.123456e1000`, `1000.123_456` y `3e1_000` son válidos. `1_000000`, `1.123_456789` y `3e1_000000` son inválidos por dejar sin agrupar cifras del mismo componente. El prefijo `r` se rige por D-034 y no modifica estas reglas.

## Consecuencias

- El lexer retira comentarios y emite tokens de salto; el parser determina cuáles son terminadores a partir de si el prefijo sintáctico está completo.
- El resaltador puede implementar el léxico sin conocer el modelo semántico.
- El catálogo de palabras reservadas se genera desde la gramática consolidada.
- El catálogo distingue palabras reservadas de palabras contextuales conforme a D-035, D-054 y D-055. `using`, `with`, `test`, `otherwise` y `ordered` están reservadas; `start`, `abstract`, `always`, `name` y `prefixes` son contextuales en sus posiciones gramaticales.

## Verificación

1. Las tres formas de comentario.
2. Apertura y cierre multilínea en líneas propias.
3. Delimitadores dentro de cadenas.
4. Prioridad de `###` y rechazo del anidamiento.
5. Texto ordinario con cierre explícito e implícito.
6. Margen, líneas estructurales y escapes del texto multilínea.
7. `Char` con exactamente un escalar.
8. Símbolos sintácticos inocuos dentro de comentarios.
9. Terminación por `;` y por salto.
10. Continuación tras delimitador, coma, operador y palabra introductora.
11. Terminación cuando el prefijo anterior ya es completo.
12. Independencia respecto de la sangría fuera de literales multilínea.
13. Literales sin separadores y con agrupación completa independiente en la parte entera, fraccionaria y exponencial.
14. Rechazo de agrupaciones parciales, grupos interiores de tamaño distinto de tres y `_` en los extremos o duplicado.
15. Equivalencia decimal de exponentes positivos, negativos y con signo explícito en literales exactos y `Rum`.
16. Modos anidados de texto y código, escapes de llaves y rechazo de un cierre implícito con interpolación abierta.
