---
id: Q-061
title: Forma declarable de datos calculados de family
priority: P1
opened: 2026-08-16
resolved: true
closed: 2026-08-29
decisions:
  - D-037
  - D-038
  - D-085
  - D-091
  - D-102
affects:
  - especificacion/07-gramatica-concreta.md
  - especificacion/08-sintaxis-abstracta.md
  - especificacion/gramatica/mud.ebnf
  - especificacion/sintaxis/mud-surface-ast.asdl
superseded-by: []
---

# Q-061 — Forma declarable de datos calculados de `family`

## Pregunta

¿Qué forma puede declarar un dato calculado de `family`: solo un tipo opcional antes de `:=` o el `derived-value-shape` completo de los campos calculados?

## Contexto

D-038 conservaba una excepción estrecha, mientras la EBNF y el AST superficial ya representaban `[ derived-value-shape ]`. D-102 adopta expresamente la forma amplia y elimina la divergencia.

## Ya decidido

- Un dato calculado es inmutable y se evalúa estáticamente por miembro.
- Su tipo puede inferirse cuando la expresión determina uno de forma unívoca.
- La declaración del dato posee descriptor `Field`, ancla subordinada y metadatos propios conforme a D-091.
- Una asignación de miembro no puede dirigirse a un dato calculado.

## Criterio de cierre

- C1: existe una única forma normativa no contradictoria para el dato calculado de `family`.
- C2: la forma completa reutiliza el contrato de `derived-value-shape` de los campos calculados sin conceder mutabilidad exterior ni almacenamiento.
- C3: EBNF, cobertura CST, proyección AST y AST superficial conservan exactamente esa forma.

## Resolución

Se adopta el `derived-value-shape` completo de los campos calculados. El dato calculado de `family` puede declarar tipo, dominio y forma de colección compatibles como restricciones o coerciones del resultado, pero sigue siendo inmutable, sin `mut` exterior y sin almacenamiento propio.

## Evidencia de cierre

- C1: D-102 fija `nombre [forma-derivada] := value-body` y D-038 incorpora literalmente esa regla.
- C2: D-102 remite a la semántica de D-037 y conserva explícitamente la ausencia de `mut` exterior, predeterminado almacenado y almacenamiento propio.
- C3: `especificacion/gramatica/mud.ebnf` conserva `[ derived-value-shape ]`; `cobertura-sintactica.yaml` y `cst-a-ast-superficial.md` proyectan esa forma; `mud-surface-ast.asdl` conserva `derived_value_shape? shape` en `CalculatedFamilyDataDecl`.
