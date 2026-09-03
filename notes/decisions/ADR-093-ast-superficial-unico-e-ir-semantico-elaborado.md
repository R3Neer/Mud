---
id: D-093
title: "AST superficial, HIR nominal y fase semántica posterior"
status: current
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "pipeline, AST superficial, HIR nominal, resolución de nombres, tabla de símbolos, grafo nominal, tipado, elaboración, futura representación semántica y validadores"
---

# ADR-093 — AST superficial, HIR nominal y fase semántica posterior

- Modifica: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].
- Modificada por: [[ADR-097-hir-nominal-vigente-e-ir-semantico-diferido|D-097]].
- Precisa: [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]], [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]], [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]].

## Contexto

Una representación que mezcle resolución nominal con tipos efectivos, dominios elaborados, cardinalidades inferidas y pruebas de terminación borra fronteras de fase útiles. La arquitectura debe distinguir la forma fuente, el resultado de resolución nominal y el significado que solo puede conocerse después de tipado y elaboración, sin obligar a fijar prematuramente la representación de esta última fase.

## Decisión

MUD posee un único AST de fuente: el **AST superficial** producido a partir de la CST sin pérdidas. Conserva la forma abstracta escrita y su procedencia sin anticipar resolución, tipado ni elaboración.

La resolución de nombres consume ese AST y produce un **HIR nominal** normativo. El HIR no duplica toda la sintaxis de fuente: registra exclusivamente información cuya existencia depende de resolución nominal:

- símbolos anclados y `LocalSymbol`;
- propietarios y ámbitos léxicos;
- bindings de cada referencia superficial a un símbolo;
- anclas públicas;
- aristas nominales de propiedad, especialización y referencia.

El HIR nominal no puede contener tipos efectivos, narrowing, dominios efectivos, formas de colección, cardinalidades efectivas o inferidas, conversiones elaboradas, pruebas de terminación ni ninguna otra conclusión que requiera tipado o elaboración. Su esquema normativo vive en `specification/names/mud-nominal-hir.asdl`.

El tipado y la elaboración consumen el AST superficial junto con el HIR nominal. Su resultado semántico pertenece a una fase arquitectónica posterior, pero el repositorio no fija todavía un esquema mecánico normativo para representarlo. Ese contrato se diseñará cuando las superficies de tipos y elaboración estén suficientemente desarrolladas.

Ningún artefacto derivado es una fuente semántica independiente: se reconstruye desde los archivos `.mud`, las decisiones de versión y las fases anteriores aplicables.

## Pipeline

```text
texto fuente
→ scanner y clasificación contextual
→ CST sin pérdidas
→ AST superficial
→ resolución nominal
→ HIR nominal: símbolos + scopes + bindings + anclas + grafo nominal parcial
→ tipado y elaboración
→ representación semántica posterior por formalizar
→ análisis posteriores / ejecución
```

El HIR nominal es deliberadamente menor que un AST resuelto completo y no anticipa conclusiones de tipos.

## Consecuencias

- `mud-surface-ast.asdl` continúa siendo el único esquema AST de fuente.
- `specification/names/mud-nominal-hir.asdl` es el contrato de salida de resolución nominal.
- No existe actualmente un ASDL normativo posterior a tipado/elaboración.
- D-078 describe la construcción del HIR nominal y no promete tipos o dominios elaborados.
- Los validadores deben comprobar la autoconsistencia del HIR nominal y prohibir en él conceptos reservados a elaboración.

## Verificación

1. El directorio de sintaxis contiene un único esquema AST de fuente: `mud-surface-ast.asdl`.
2. El pipeline contiene explícitamente `Surface AST → HIR nominal → tipado/elaboración → representación semántica futura`.
3. El HIR nominal representa símbolos, scopes, bindings, anclas y `Owns | Specializes | RefersTo`.
4. El HIR nominal no contiene tipos efectivos, dominios efectivos, cardinalidades ni evidencia de terminación.
5. No se exige un esquema semántico posterior antes de formalizar las fases que lo producen.
6. El validador rechaza tipos ASDL desconocidos y conceptos elaborados dentro del HIR nominal.
