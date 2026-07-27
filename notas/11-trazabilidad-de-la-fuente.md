# Trazabilidad de la especificación inicial

Esta matriz demuestra cobertura sin copiar las 78 secciones. Los rangos indican el documento dueño principal; algunos temas también aparecen enlazados desde otras notas.

| Secciones de la fuente | Tema | Documento dueño |
| --- | --- | --- |
| Introducción, 1, 2 | Objetivo, fuente de verdad, límites y principios | [01-vision-y-alcance.md](01-vision-y-alcance.md) |
| 3 a 19 | Declaraciones, organización, nombres, participantes, tipos, campos, colecciones y dominios | [02-modelo-del-lenguaje.md](02-modelo-del-lenguaje.md) |
| 20 a 30 | Magnitudes, operadores, intervalos, precedencia y literales | [02-modelo-del-lenguaje.md](02-modelo-del-lenguaje.md) |
| 31 a 44 | Reglas, acciones, `after`, `old`, resultados, `allowed` y `eventually` | [02-modelo-del-lenguaje.md](02-modelo-del-lenguaje.md) y [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) |
| 45 a 49 | Ondas, vinculaciones, cola, conflictos y terminación | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) |
| 50 a 59 | Efectos, iteración, creación, destrucción, azar, fallos y predeterminados | [02-modelo-del-lenguaje.md](02-modelo-del-lenguaje.md) y [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) |
| 60, 61, 74 | Léxico, comentarios, terminadores y palabras clave | [07-plan-de-formalizacion.md](07-plan-de-formalizacion.md) y Q-001 en [08-preguntas-abiertas.md](08-preguntas-abiertas.md) |
| 62 | Lectura, escritura y contratos externos | [01-vision-y-alcance.md](01-vision-y-alcance.md) y [04-arquitectura-del-sistema.md](04-arquitectura-del-sistema.md) |
| 63 a 66 | Grafo, IR, compilador y TypeScript | [04-arquitectura-del-sistema.md](04-arquitectura-del-sistema.md) |
| 67 a 71 | Plugin, clasificación, inferencias, agenda y flujo atómico | [04-arquitectura-del-sistema.md](04-arquitectura-del-sistema.md) y [05-cambios-semanticos-y-git.md](05-cambios-semanticos-y-git.md) |
| 72, 73 | Tests y editor | [06-nucleo-vertical-v0.md](06-nucleo-vertical-v0.md) y [07-plan-de-formalizacion.md](07-plan-de-formalizacion.md) |
| 75 | Ejemplo integral | Base para seleccionar ejemplos canónicos en [06-nucleo-vertical-v0.md](06-nucleo-vertical-v0.md) |
| 76 | Decisiones esenciales | [10-registro-de-decisiones.md](10-registro-de-decisiones.md) |
| 77 | Cuestiones abiertas | [08-preguntas-abiertas.md](08-preguntas-abiertas.md) |
| 78 | Instrucciones operativas | Distribuidas por documento dueño y preservadas como restricciones en [09-riesgos-y-restricciones.md](09-riesgos-y-restricciones.md) |

## Observaciones de procedencia

- La fuente usa expresiones como “se mantiene vigente” o “el resto se mantiene” que parecen depender de versiones anteriores no incluidas. Esto se registra como Q-010.
- La lista de 35 cuestiones abiertas se conserva temáticamente en Q-001 a Q-035; algunas se agrupan cuando comparten una única decisión normativa.
- Q-036 a Q-040 son preguntas inferidas del objetivo de producto y del protocolo de automatización; no se presentan como preguntas originales.
- P-001 a P-005 nacieron como propuestas de estas notas y no como decisiones de la fuente. P-001 quedó posteriormente sustituida por D-013.

## Cobertura que requiere ejemplos

La trazabilidad temática no sustituye pruebas normativas. Antes de implementar cada bloque deberán existir:

- Un ejemplo mínimo válido.
- Un ejemplo representativo.
- Al menos un contraejemplo por restricción.
- Resultado esperado en AST o IR.
- Diagnóstico esperado cuando sea inválido.
