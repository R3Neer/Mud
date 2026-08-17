---
id: D-093
title: "AST superficial, HIR nominal e IR semántico elaborado"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "pipeline, AST superficial, HIR nominal, resolución de nombres, tabla de símbolos, grafo nominal, tipado, elaboración, IR y validadores"
---

# ADR-093 — AST superficial, HIR nominal e IR semántico elaborado

- Modifica: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].
- Precisa: [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]], [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]], [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]].

## Contexto

El antiguo `mud-resolved-ast.asdl` mezclaba referencias nominales con tipos efectivos, dominios elaborados, cardinalidades inferidas y pruebas de terminación. Esa representación híbrida permanece retirada. La frontera correcta distingue la forma fuente, el resultado de resolución nominal y el significado tipado/elaborado.

## Decisión

MUD posee un único AST de fuente: el **AST superficial** producido a partir del CST sin pérdidas. Conserva la forma abstracta escrita y su procedencia sin anticipar resolución, tipado ni elaboración.

La resolución de nombres consume ese AST y produce un **HIR nominal** normativo. El HIR no duplica toda la sintaxis de fuente: registra exclusivamente información cuya existencia depende de resolución nominal:

- símbolos anclados y `LocalSymbol`;
- propietarios y ámbitos léxicos;
- bindings de cada referencia superficial a un símbolo;
- anclas públicas;
- claves estructurales nominales cuando formen parte de identidad local;
- aristas nominales parciales de propiedad, especialización y referencia.

El HIR nominal **no puede contener** tipos efectivos, narrowing, dominios efectivos, formas de colección, cardinalidades efectivas o inferidas, conversiones elaboradas, pruebas de terminación ni ninguna otra conclusión que requiera tipado o elaboración. Su esquema normativo vive en `especificacion/ir/mud-nominal-hir.asdl`.

El tipado y la elaboración consumen el AST superficial junto con el HIR nominal y producen el **IR semántico** de `especificacion/ir/mud-semantic-ir.asdl`. Ese IR sí puede contener tipos efectivos, dominios, cardinalidades, conversiones resueltas, dependencias y evidencia de terminación.

Ninguno de los tres artefactos es una fuente semántica independiente: todos se reconstruyen desde los archivos `.mud`, las decisiones de versión y las fases anteriores.

## Pipeline

```text
texto fuente
→ scanner y clasificación contextual
→ CST sin pérdidas
→ AST superficial
→ resolución nominal
→ HIR nominal: símbolos + scopes + bindings + anclas + grafo nominal parcial
→ tipado y elaboración
→ IR semántico tipado/elaborado
→ análisis posteriores / ejecución
```

El archivo retirado `especificacion/sintaxis/mud-resolved-ast.asdl` no reaparece. El HIR nominal es una representación distinta y deliberadamente más pequeña, no el antiguo AST resuelto rebautizado.

## Consecuencias

- `mud-surface-ast.asdl` continúa siendo el único esquema AST de fuente.
- `mud-nominal-hir.asdl` es el contrato de salida de resolución nominal.
- `mud-semantic-ir.asdl` es posterior a tipado/elaboración.
- D-078 describe la construcción del HIR nominal y no promete tipos o dominios elaborados.
- Los validadores deben comprobar la autoconsistencia ASDL de ambos contratos de `ir/` y prohibir en el HIR conceptos reservados a elaboración.

## Verificación

1. El directorio de sintaxis contiene un único esquema AST de fuente: `mud-surface-ast.asdl`.
2. El pipeline contiene explícitamente `Surface AST → HIR nominal → IR semántico`.
3. El HIR nominal representa símbolos, scopes, bindings, anclas y aristas nominales.
4. El HIR nominal no contiene tipos efectivos, dominios efectivos, cardinalidades ni evidencia de terminación.
5. El IR semántico conserva las conclusiones de tipado/elaboración.
6. El validador rechaza tipos ASDL desconocidos, la reaparición de `mud-resolved-ast.asdl` y conceptos elaborados dentro del HIR nominal.
