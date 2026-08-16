---
id: D-094
title: "Frontera entre AST resuelto y representación elaborada"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "pipeline, AST superficial, resolución nominal, tipado, elaboración, IR, símbolos, anclas y validadores"
---
# ADR-094 — Frontera entre AST resuelto y representación elaborada

- Modifica: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]], [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].

## Contexto

El esquema llamado `mud-resolved-ast.asdl` mezclaba la salida de resolución nominal con datos que solo pueden existir después del tipado y otros análisis: `resolved_type`, dominios elaborados, cardinalidades efectivas, conversiones, narrowing, formas de resultado y `termination_evidence`. Esa mezcla contradecía el pipeline documentado, que situaba tipado/elaboración **después** del AST resuelto.

## Decisión

MUD conserva cuatro fronteras semánticas distintas después de la CST:

```text
CST sin pérdidas
→ Surface AST
→ Resolved AST/HIR nominal
→ Elaborated AST/HIR tipado
→ IR
```

### Surface AST

Conserva la estructura normalizada escrita y las ambigüedades cuyo significado depende de resolución o tipos. No contiene símbolos ni tipos inferidos.

### Resolved AST/HIR nominal

`mud-resolved-ast.asdl` contiene exclusivamente información disponible tras resolución nominal:

- `AnchoredSymbol` y `LocalSymbol`;
- anclas públicas ya determinadas;
- ámbitos y destinos de referencias;
- clase nominal de declaraciones/miembros;
- identidad y propietario de metadata materializada;
- claves locales de ramas decisionales;
- aristas de dependencia cuya identidad no requiere tipado.

No contiene `resolved_type`, dominios efectivos, cardinalidades inferidas, `collection_shape`, `decision_shape`, conversiones, narrowing ni `termination_evidence`.

Una referencia cuya validez final depende de tipo puede quedar nominalmente resuelta a su símbolo y ser aceptada o rechazada después; resolver un nombre no equivale a certificar que su uso es bien tipado.

### Elaborated AST/HIR

`mud-elaborated-ast.asdl` toma la resolución nominal como entrada y añade:

- tipos y dominios efectivos;
- cardinalidades y su procedencia;
- formas de colección y diccionario;
- conversiones y narrowing;
- resultados efectivos de operaciones y accesos;
- evidencia de terminación y otros análisis estáticos necesarios antes del IR.

Esta capa puede conservar las mismas anclas y `symbol_id`; no crea una segunda identidad para las declaraciones.

### IR

El IR sigue siendo una representación posterior orientada a ejecución, tooling y grafo semántico. No se convierte en fuente de verdad: todas las capas son reconstruibles desde `.mud`.

## Consecuencias

- el nombre “AST resuelto” vuelve a significar resolución, no tipado encubierto;
- diagnósticos de nombre pueden producirse sin construir tipos efectivos;
- tooling puede usar símbolos/anclas aunque el tipado posterior falle;
- los datos de análisis que antes estaban prematuramente en `mud-resolved-ast.asdl` pasan al nuevo esquema elaborado;
- el grafo nominal inicial y el grafo semántico elaborado dejan de fingir ser la misma fase.

## Verificación

1. `mud-resolved-ast.asdl` no define tipos efectivos, dominios elaborados, conversiones ni `termination_evidence`.
2. `mud-elaborated-ast.asdl` conserva esas distinciones y referencia los mismos símbolos/anclas.
3. README, capítulos 08/09 y ADR vigentes describen el mismo orden de fases.
4. El validador comprueba que los tres ASDL normativos no contienen tipos ASDL sin definir y que existen los módulos esperados.
5. Un programa puede construir catálogo de símbolos/anclas aunque un error de tipos impida construir la capa elaborada.
