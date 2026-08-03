---
id: D-057
title: "Gramática concreta, precedencia y continuación"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-001"
affects:
  - "[[especificacion/05-texto-fuente]], [[especificacion/06-lexico]], [[especificacion/07-gramatica-concreta]], `especificacion/gramatica/`"
---
# ADR-057 — Gramática concreta, precedencia y continuación

- Modificada por: [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]]
- Modificada además por: [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]]
- Modificada también por: [[notas/decisiones/ADR-064-orden-por-ruta-estable|D-064]]
- Modificada asimismo por: [[notas/decisiones/ADR-065-cabecera-using-de-fichero|D-065]]
- Modificada finalmente por: [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]]
- Modificada después por: [[ADR-074-uniones-nominales-y-estrechamiento|D-074]], [[ADR-075-dominios-enumerables-all-y-valores-derivados|D-075]], [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]], [[ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]] y [[ADR-079-diagnostico-exterior-de-reglas-always|D-079]]
- Cierra: [[notas/preguntas/Q-001-gramatica-y-saltos-de-linea|Q-001]]
- Documentos afectados: [[especificacion/05-texto-fuente]], [[especificacion/06-lexico]], [[especificacion/07-gramatica-concreta]], `especificacion/gramatica/`

## Contexto

Las decisiones de MUD ya fijaban las construcciones principales, pero no existía una gramática consolidada. Esto dejaba sin una única respuesta:

- Qué formas pertenecen al lenguaje fuente.
- Qué palabras son reservadas o contextuales.
- Cuándo un salto de línea termina una construcción.
- Cómo se agrupan operadores, conversiones y encadenamientos.
- Qué distinciones se resuelven por sintaxis y cuáles por análisis estático.

## Decisión

La sintaxis de MUD 1.0 queda definida por:

1. [[especificacion/gramatica/mud-lexico.ebnf|La gramática léxica]].
2. [[especificacion/gramatica/mud.ebnf|La gramática concreta]].
3. Las restricciones contextuales y el algoritmo de agrupación de [[especificacion/07-gramatica-concreta]].

Las EBNF definen el conjunto de formas sintácticas. No intentan decidir cuestiones que necesitan resolución de nombres o tipos, como distinguir:

- Una llamada a regla de una llamada a acción.
- Pertenencia mediante `in` de presentación de unidades mediante `in`.
- Un nombre de unidad reconocido de un identificador ordinario.
- La variante semántica de operadores sobrecargados.
- Una colección unitaria `[e]` de un intervalo unitario `[e]`.

Esas distinciones producen nodos distintos durante la elaboración y deben diagnosticarse estáticamente cuando sean ambiguas o inválidas.

D-059 añade otra distinción contextual: `1..5 m` se elabora como un intervalo numérico con unidad común, mientras `1 m..5 km` contiene dos extremos de magnitud ordinarios. Una unidad común solo puede seguir a una forma cuyos extremos finitos sean literales numéricos sin unidad.

Las cabeceras usan producciones distintas para participantes `for`, `on` y `given`. La EBNF permite que `for` use cualquier `declared-type`, declare un dominio `in`, escriba una especificación de colección y declare un `mut` exterior. `given` también admite dominio, cardinalidad, unicidad y orden, pero su producción excluye tanto `mut` exterior como capacidad interior. `on` conserva únicamente una referencia de tipo individual y su capacidad interior opcional. El análisis estático exige que ese tipo `on` resuelva a una `thing`; las restricciones de nombre obligatorio, pureza y receptor-lugar pertenecen también a D-036.

### Terminadores

El lexer emite `NEWLINE` y `SEMICOLON`. El parser los convierte en `TERMINATOR`, salvo cuando el salto aparece:

- Dentro de `()`, `[]` o una construcción delimitada todavía abierta.
- Después de una coma.
- Después de un operador que exige operando.
- Después de una palabra introductora que exige contenido.
- Dentro de un literal o comentario multilínea.

La enumeración exhaustiva de introductores y operadores procede de la propia gramática. La sangría no participa en esta decisión.

### Operadores

La precedencia y los encadenamientos se fijan en [[especificacion/07-gramatica-concreta#Precedencia y agrupación]]. `to` y el `in` de presentación son operadores postfix que transforman todo el valor acumulado a su izquierda; después del sufijo pueden aparecer operadores nuevos sobre el resultado convertido. `changes` es un sufijo temporal situado por debajo de comparaciones y por encima de `and` y `or`, conforme a D-058.

Los encadenamientos admitidos se elaboran por pares adyacentes:

```mud
a < b < c
```

equivale a:

```mud
a < b and b < c
```

La misma regla se aplica a cadenas homogéneas de igualdad y de `<=>`. No se encadenan `!=`, `is`, pertenencia `in` ni `=>`.

### Recuperación de errores

La recuperación concreta no forma parte del lenguaje aceptado. Una implementación puede recuperar en `TERMINATOR`, `}` o en el comienzo inequívoco de una declaración, pero no puede aceptar por recuperación una forma rechazada por la gramática.

## Consecuencias

- Q-001 deja de ser una cuestión de diseño abierta.
- La gramática puede evolucionar por cambios normativos explícitos y pruebas de conformidad.
- Un parser puede usar descenso recursivo, Pratt, PEG u otra técnica si acepta y agrupa exactamente las mismas formas.
- Las decisiones semánticas todavía abiertas no impiden reconocer programas ni construir su AST de superficie.

## Verificación

1. Todas las producciones referenciadas están definidas.
2. Todos los símbolos alcanzables parten de `mud-file`.
3. Ejemplos válidos e inválidos por declaración.
4. Terminación y continuación en cada clase de prefijo.
5. Agrupación de cada nivel de precedencia.
6. Diagnósticos de las ambigüedades contextuales.
7. Separación sintáctica de roles `for` colectivos y vinculaciones `on` individuales.
8. Elaboración de intervalos con unidad compartida frente a unidades locales.
9. Rechazo sintáctico de capacidad interior `mut` en `given`.
10. Dominio situado entre el tipo y la colección de un rol `for`.
