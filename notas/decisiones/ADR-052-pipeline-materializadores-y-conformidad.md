# ADR-052 — Pipeline, materializadores y conformidad

- Estado: Vigente como frontera arquitectónica
- Fecha: 2026-07-28
- Preguntas relacionadas: Q-007, Q-009, Q-037, Q-038
- Documentos afectados: arquitectura, tooling, conformidad

## Contexto

La referencia mezclaba requisitos del lenguaje con una implementación TypeScript, un plugin y soporte de editor. MUD necesita exigir conservación semántica sin imponer esas tecnologías.

## Decisión

El pipeline conceptual separa:

1. lexer;
2. parser;
3. AST de superficie;
4. resolución de namespaces, imports, nombres y anclas;
5. sistema de tipos, aliases, dominios, cardinalidades, mutabilidad y magnitudes;
6. análisis de pureza, efectos, ciclos, finitud, terminación y estocasticidad;
7. IR canónico;
8. grafo, diagnósticos, formateo y materializaciones.

El parser no produce directamente IR: debe conservarse procedencia suficiente para diagnósticos, formato y evolución sintáctica.

Un materializador puede usar funciones, parámetros, tuplas, mapas, transacciones, copias especulativas o exploración exhaustiva. No puede:

- inventar reglas de dominio;
- cambiar identidad, nominalidad o especialización;
- confundir participantes con `given`;
- cambiar atomicidad, orden causal o resultados;
- convertir `failed` en falso;
- usar coma flotante para la semántica observable de `Number`;
- adelantar la publicación de `message`.

La conformidad se prueba mediante programas válidos e inválidos, diagnósticos requeridos, IR esperado, transiciones, trazas y propiedades. El soporte de editor debe diferenciar participantes `on`, participantes `for`, `given`, dominios, variantes de regla y firmas públicas, pero no constituye semántica.

## Consecuencias

- TypeScript es un destino posible, no una parte de MUD.
- La suite histórica se retira como autoridad porque contiene sintaxis sustituida; sus intenciones de prueba se conservan en el plan de conformidad.
- El catálogo de palabras reservadas se genera o verifica contra la gramática normativa, no se mantiene manualmente como lista provisional.

## Verificación

1. Dos materializadores distintos producen observaciones equivalentes.
2. AST e IR conservan funciones distintas.
3. Casos de conformidad para participantes, `given`, acciones, reglas y salidas.
4. El editor muestra la firma semántica resuelta.
5. Ningún artefacto derivado es necesario para reconstruir el modelo.
