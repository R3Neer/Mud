---
id: Q-061
title: Forma declarable de datos calculados de family
priority: P1
opened: 2026-08-16
resolved: false
closed:
decisions:
  - D-037
  - D-038
  - D-085
  - D-091
affects:
  - especificacion/07-gramatica-concreta.md
  - especificacion/08-sintaxis-abstracta.md
  - especificacion/gramatica/mud.ebnf
  - especificacion/sintaxis/mud-surface-ast.asdl
superseded-by: []
---

# Q-061 — Forma declarable de datos calculados de `family`

## Pregunta

¿Qué forma puede declarar un dato calculado de `family`: solo un tipo opcional antes de `:=`, como afirma D-038, o el `derived-value-shape` más amplio que reconoce actualmente la EBNF?

## Contexto

D-038 escribe `nombre [: tipo] := expresión` y excluye `in` y especificaciones de colección. D-085 modificó D-037 y consolidó para los valores calculados una forma derivada más amplia; la EBNF vigente de `family` usa `[ derived-value-shape ]`, que también reconoce dominio y forma colectiva, y el AST superficial conserva esa forma. No está decidido si D-038 debe mantener su excepción estrecha o alinearse con la ampliación posterior. D-091 añade identidad de descriptor y metadata-body a los datos asociados, pero no necesita elegir entre ambas variantes y por tanto deja esta contradicción abierta.

## Ya decidido

- Un dato calculado es inmutable y se evalúa estáticamente por miembro.
- Su tipo puede inferirse cuando la expresión determina uno de forma unívoca.
- La declaración del dato posee descriptor `Field`, ancla subordinada y metadatos propios conforme a D-091.
- Una asignación de miembro no puede dirigirse a un dato calculado.

## Pendiente

- C1: decidir si el contrato declarable es `[: tipo]` o todo `derived-value-shape`.
- C2: si se elige la forma estrecha, fijar qué construcciones cuentan como `tipo` sin reintroducir por dentro dominio o especificación de colección.
- C3: alinear EBNF, catálogo CST, AST superficial y ejemplos con una única respuesta.

## Criterio de cierre

- C1: existe una única forma normativa no contradictoria.
- C2: la gramática expresa esa forma sin aceptar por otra ruta lo que la semántica prohíba.
- C3: `CalculatedFamilyDataDecl` conserva exactamente las distinciones que sobrevivan al parsing y ninguna forma declarada válida se pierde.

## Resolución

Pendiente.
