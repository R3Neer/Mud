---
id: D-093
title: "AST superficial único e IR semántico elaborado"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "pipeline, AST superficial, resolución nominal, tabla de símbolos, grafo nominal, tipado, elaboración, IR y validadores"
---

# ADR-093 — AST superficial único e IR semántico elaborado

- Modifica: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].
- Precisa: [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]], [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]], [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]].

## Contexto

El pipeline vigente ya separa CST, AST superficial, resolución nominal y tipado/elaboración, pero `mud-resolved-ast.asdl` mezclaba en un artefacto denominado «AST resuelto» referencias nominales con tipos efectivos, dominios elaborados, cardinalidades inferidas y pruebas de terminación. Esa mezcla hacía imposible interpretar el archivo como salida exclusiva de resolución de nombres y duplicaba innecesariamente el árbol abstracto de fuente.

## Decisión

MUD posee un único AST normativo: el **AST superficial** producido a partir del CST sin pérdidas. Conserva la forma abstracta escrita, procedencia y las distinciones sintácticas que necesitan diagnósticos y tooling, sin anticipar tipado ni elaboración.

La resolución nominal no construye un segundo AST normativo. Produce sobre el AST superficial:

- tabla de símbolos y bindings de referencias;
- anclas y propietarios resueltos;
- ámbitos léxicos;
- claves estructurales locales como `decision_branch_key`;
- un grafo nominal parcial de propiedad, especialización y dependencias cuyos extremos ya puedan identificarse.

El tipado y la elaboración consumen el AST superficial junto con esos resultados de resolución y producen el **IR semántico**. El IR contiene el significado elaborado necesario para análisis posteriores y ejecución, incluidos cuando proceda:

- tipos efectivos y narrowing;
- dominios y formas de colección;
- cardinalidades efectivas y su procedencia;
- modos y formas de aplicación de diccionarios;
- conversiones ya resueltas;
- dependencias semánticas;
- pruebas o evidencias de terminación.

El esquema mecánico del IR vive en `especificacion/ir/mud-semantic-ir.asdl`. No es una segunda fuente de verdad: conforme a D-051 se reconstruye a partir del programa, el AST superficial y las decisiones de versión.

## Pipeline

```text
texto fuente
→ scanner y clasificación contextual
→ CST sin pérdidas
→ AST superficial
→ resolución nominal: símbolos + bindings + grafo nominal parcial
→ tipado y elaboración
→ IR semántico
→ análisis posteriores / ejecución
```

Una implementación puede materializar internamente un HIR intermedio si le resulta útil, pero ese artefacto no es normativo ni puede introducir significado que no aparezca en el AST superficial, las reglas de resolución o la elaboración.

## Consecuencias

- Se retira `especificacion/sintaxis/mud-resolved-ast.asdl` como contrato normativo.
- Los contratos semánticos que allí vivían se trasladan al IR y dejan de llamarse «AST resuelto».
- `mud-surface-ast.asdl` continúa siendo el único esquema AST.
- D-078 describe exclusivamente resolución nominal, símbolos, anclas y grafo inicial; no promete tipos o dominios ya elaborados.
- Los validadores deben comprobar que el IR semántico sea ASDL autoconsistente y que el antiguo archivo no reaparezca.

## Verificación

1. El directorio de sintaxis contiene un único esquema AST: `mud-surface-ast.asdl`.
2. El flujo documental no sitúa un «AST resuelto» entre resolución y tipado.
3. El IR semántico conserva tipos, dominios, cardinalidades y terminación que antes estaban mezclados en el AST resuelto.
4. D-051 y D-078 describen la misma frontera de fases.
5. El validador rechaza tipos ASDL desconocidos en el esquema del IR y la reaparición del contrato retirado.
