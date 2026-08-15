---
id: D-070
title: "CST sin pérdidas y AST superficial normalizado"
status: vigente
date: 2026-08-02
supersedes: []
superseded-by: []
questions: []
affects:
  - "texto fuente, léxico, gramática concreta, CST, AST superficial y validación editorial"
---

# ADR-070 — CST sin pérdidas y AST superficial normalizado

- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]
- Ampliada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]

## Estado

Vigente.

Esta decisión se ha actualizado al vocabulario y a la gramática vigentes: usa los tipos numéricos breves de [[ADR-067-nombres-breves-de-tipos-numericos|D-067]], integra el `name` intrínseco de [[ADR-068-thing-universal-y-nombre-intrinseco|D-068]] y representa los literales de comillas dobles conforme a [[ADR-069-literales-char-con-comillas-dobles|D-069]]. En particular, el AST superficial no inventa un nodo léxico distinto para `Char`; esa elaboración requiere contexto de tipos.

## Contexto

La gramática concreta de MUD define qué programas pueden reconocerse, pero no basta para:

- Reconstruir exactamente un archivo.
- Conservar comentarios y formato.
- Implementar un formateador o refactorizador.
- Distinguir puntuación de estructura semántica.
- Fijar qué azúcares sobreviven al parsing.
- Evitar que resolución y tipado se mezclen con el parser.

Un único árbol no satisface simultáneamente esas necesidades. Un árbol completamente concreto es incómodo para análisis semántico; uno normalizado pierde información necesaria para edición.

## Decisión

MUD define dos representaciones sintácticas normativas y separadas:

1. Una **CST sin pérdidas por archivo**.
2. Un **AST superficial normalizado**, agregable en `MudProject`.

La cadena de fases es:

```text
texto
→ scanner completo
→ CST sin pérdidas
→ validación sintáctica contextual
→ AST superficial
→ resolución
→ AST resuelto
→ tipado/elaboración
→ IR
```

## CST

La CST:

- Conserva todos los tokens escritos.
- Conserva espacios y comentarios como trivia.
- Conserva la forma física de saltos.
- Conserva cierres explícitos e implícitos de `Text`.
- Puede representar entradas inválidas mediante tokens ausentes y regiones de error.
- Permite reconstruir los bytes originales salvo el BOM, conservado como metadato.
- No resuelve nombres ni tipos.

Toda trivia pertenece al token significativo siguiente. `EOF` posee la trivia final.

## AST superficial

El AST superficial:

- Elimina trivia, delimitadores y terminadores.
- Normaliza cardinalidades, intervalos, bloques y azúcares declarados.
- Conserva el orden fuente de listas internas.
- Conserva nombres no resueltos.
- Conserva operadores distintos cuando su escritura tiene significado.
- Usa `flag = Disabled | Enabled` para propiedades booleanas.
- Lleva procedencia en todos sus nodos salvo `MudProject`.
- No contiene comentarios ordinarios.

## Proyecto y archivo

La CST solo tiene raíz por archivo. El proyecto es una agregación semántica de archivos, no un texto concreto.

`MudProject` ordena archivos canónicamente por ruta normalizada únicamente para serialización estructural. El orden no adquiere significado semántico.

## Comentarios

Los comentarios actuales son trivia ordinaria. Se eliminan del flujo significativo que consume la gramática, pero no de la CST.

Una documentación estructurada futura usará un árbol documental separado y referencias resolubles a anclas; no convertirá comentarios ordinarios en declaraciones del AST ejecutable.

## Validación entre CST y AST

Las formas que la EBNF puede reconocer pero que no caben unívocamente en el AST normalizado se validan antes de construirlo. Ejemplos:

- Modificadores duplicados.
- Declaraciones de metadatos duplicadas en un mismo propietario, incluidas las unidades.
- Propiedades obligatorias ausentes.
- Orden inválido de argumentos.

La resolución de nombres y el tipado siguen fuera de esta fase.

## Ambigüedades diferidas

El AST superficial conserva sin decidir:

- Camino cualificado frente a cadena de accesos semánticos.
- Literal estructural frente a tupla de receptores.
- Llamada postfix frente a llamada de acción.
- Acción elemental frente a compuesta.
- Tipo contextual de literales.

Estas decisiones pertenecen al AST resuelto o elaborado.

## Procedencia

`SourceSpan` usa offsets de bytes UTF-8, posiciones basadas en cero y final exclusivo. La columna cuenta valores escalares Unicode. LSP convierte a UTF-16 en la frontera.

Un nodo sintetizado conserva un span de anclaje y una razón de síntesis.

## Artefactos normativos

La decisión se materializa en:

- `especificacion/sintaxis/cst-sin-perdidas.md`.
- `especificacion/sintaxis/mud-syntax-kinds.yaml`.
- `especificacion/08-sintaxis-abstracta.md`.
- `especificacion/sintaxis/mud-surface-ast.asdl`.
- `especificacion/sintaxis/cst-a-ast-superficial.md`.
- `especificacion/sintaxis/cobertura-sintactica.yaml`.

## Consecuencias positivas

- El parser y el IDE comparten una representación sin pérdida.
- El análisis semántico no depende de puntuación.
- Las normalizaciones son auditables.
- La cobertura de gramática puede validarse automáticamente.
- Las refactorizaciones futuras pueden conservar comentarios y formato.
- La resolución no se introduce prematuramente en el parser.

## Costes

- Existen dos árboles y una transformación normativa.
- La recuperación de errores debe conservar texto.
- Los cambios gramaticales requieren actualizar varios artefactos.
- Una implementación mínima necesita más infraestructura inicial.

## Alternativas rechazadas

### Solo AST

Rechazada porque perdería comentarios, espaciado, puntuación y formas concretas necesarias para tooling.

### Solo CST

Rechazada porque obligaría a resolución, tipos y semántica a interpretar continuamente puntuación y azúcares.

### Comentarios dentro del AST ejecutable

Rechazada porque no alteran el significado de un programa y crearían dependencias falsas. La documentación estructurada futura tendrá modelo separado.

### Clasificar acciones en el parser

Rechazada porque `action-call-effect ::= postfix-expression` exige resolver nombres para saber si el efecto es realmente una llamada de acción.

## Cambios derivados

- `06-lexico.md` debe distinguir flujo completo y significativo.
- `07-gramatica-concreta.md` debe declarar que el parsing produce CST.
- `08-sintaxis-abstracta.md` sustituye el esqueleto previsto.
- Los README deben incorporar la nueva cadena de fases.
- La representación numérica de magnitudes usa sintaxis de tipo declarada y se valida estáticamente como numérica.
