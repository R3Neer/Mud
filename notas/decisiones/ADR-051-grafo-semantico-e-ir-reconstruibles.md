---
id: D-051
title: "Grafo semántico futuro e información reconstruible"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-009"
  - "Q-016"
  - "Q-027"
  - "Q-034"
  - "Q-054"
  - "Q-059"
affects:
  - "arquitectura, HIR nominal, futuro grafo semántico, futura representación posterior a tipado y elaboración, conformidad"
---
# ADR-051 — Grafo semántico futuro e información reconstruible

- Modificada por: [[ADR-097-hir-nominal-vigente-e-ir-semantico-diferido|D-097]].
- Ampliada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]] y [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]].
- Modificada por: [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]], [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]], [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]] y [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].
- Relacionada con: [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]].

## Contexto

Los análisis de impacto, explicación y ejecución necesitarán información semántica derivada, pero esa información no debe convertirse en una fuente alternativa de verdad ni fijarse mecánicamente antes de que las fases que la producen estén formalizadas.

## Decisión

Los archivos `.mud` y las decisiones de versión son la fuente semántica. El AST superficial y el HIR nominal son derivados reconstruibles actuales. La resolución nominal produce `especificacion/nombres/mud-nominal-hir.asdl`, con símbolos, scopes, bindings, anclas y relaciones nominales, sin conclusiones de tipado o elaboración.

Tras tipado y elaboración podrá existir una representación semántica posterior y un grafo semántico consultable derivado de ella. Su codificación concreta queda deliberadamente sin fijar mientras esas fases no dispongan de superficies normativas desarrolladas suficientes.

Cuando se diseñe esa representación futura deberá poder conservar o reconstruir, según corresponda, al menos estas distinciones conceptuales:

- procedencia hasta archivo y rango de origen;
- símbolos y anclas resueltos;
- las tres variantes de regla;
- participantes `for` y `on`, valores `given`, cardinalidad, mutabilidad y modos de vinculación;
- tipos, aliases, dominios, cardinalidades, unidades e intervalos ya elaborados;
- vinculaciones locales y su orden de evaluación;
- efectos, lecturas, escrituras, llamadas y dependencias;
- actividad lógica y dependencias suspendidas;
- `look`, `message`, sus salidas y dependencias diferidas;
- tests, activación local, efectos, aserciones y diagnósticos;
- dependencias de `allowed`, `eventually`, `when`, `if`, `after`, `old` y `always`;
- efectos estructurales `create`, `destroy`, adición y retirada de colecciones;
- derivación dimensional, magnitudes, unidades y equivalencias;
- dependencias generales, de dominio, estocásticas y duras cuando formen parte del análisis definido.

La decisión de qué información se almacena explícitamente, qué se deriva y cómo se serializa pertenece al diseño futuro de tipado/elaboración. Si se introduce un formato de intercambio persistente, deberá llevar versión de esquema compatible y permitir reconstrucción determinista desde las fuentes normativas anteriores.

Q-009 conserva abierto el formato externo y los nombres concretos cuando llegue a existir tal representación; esa pregunta no obliga a crearla anticipadamente.

## Consecuencias

- Una discrepancia en un derivado se resuelve descartándolo y reconstruyéndolo desde las fuentes normativas.
- No existe actualmente un contrato mecánico de IR semántico ni un grafo semántico final normativo.
- El HIR nominal no puede absorber tipos efectivos, dominios efectivos, cardinalidades inferidas, efectos ni evidencia de terminación para compensar esa ausencia.
- Las futuras herramientas de análisis deben esperar a la superficie semántica correspondiente o derivar únicamente información autorizada por las fases ya formalizadas.

## Verificación

1. El HIR nominal es reconstruible desde AST superficial + resolución nominal.
2. El HIR nominal permanece libre de conclusiones de tipado/elaboración.
3. No existe un esquema normativo de IR semántico mientras no estén desarrolladas sus fases productoras.
4. Las obligaciones conceptuales anteriores permanecen disponibles para auditar el diseño futuro sin fijar hoy su representación mecánica.
