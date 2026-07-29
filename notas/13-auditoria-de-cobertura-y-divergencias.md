# Auditoría final de migración de la especificación inicial

- Estado: completada
- Fecha: 2026-07-28
- Fuente auditada: [[referencias/retiradas/MUD Especificacion inicial|MUD — Especificación inicial histórica retirada]]
- Alcance: las 78 secciones numeradas, su introducción y las decisiones posteriores

## Resultado

La especificación inicial ya no contiene ningún requisito cuya única copia vigente dependa de ella. Cada sección ha sido:

1. migrada a una nota o decisión actual;
2. sustituida explícitamente por una decisión posterior; o
3. retirada por ser un ejemplo, catálogo o artefacto obsoleto, conservando su intención en el documento dueño.

Esto **no significa que MUD 1.0 esté formalizado por completo**. Significa que la referencia temprana ya no es necesaria para descubrir requisitos. Las tareas aún no resueltas están en [[notas/08-preguntas-abiertas]] y la promoción a capítulos profesionales sigue el índice de [[especificacion/README]].

## Leyenda

- **Migrada**: el contenido no contradictorio tiene un dueño vigente.
- **Sustituida**: una decisión posterior define un comportamiento diferente.
- **Retirada**: el artefacto no era una regla vigente; su propósito se conserva en el plan actual.

## Matriz completa

| Sección | Tema histórico | Resultado | Dueño vigente |
| ---: | --- | --- | --- |
| 1 | Objetivo | Migrada | [[notas/01-vision-y-alcance]] |
| 2 | Principios fundamentales | Migrada | [[notas/01-vision-y-alcance]], [[notas/09-riesgos-y-restricciones]] |
| 3 | Declaraciones principales | Sustituida y migrada | D-025, D-027, D-031; [[notas/02-modelo-del-lenguaje]] |
| 4 | Organización física | Migrada | D-035 |
| 5 | Convenciones de nombres | Migrada | D-035 |
| 6 | Participantes, `on`, `for` y `given` | Sustituida y migrada | D-025, D-036 |
| 7 | Llamadas a reglas booleanas | Sustituida y migrada | D-036, D-041 |
| 8 | Solicitud y composición de acciones | Sustituida y migrada | D-036, D-042 |
| 9 | Acceso, nombres cualificados y anclas | Migrada | D-035 |
| 10 | Constructos | Sustituida por `thing` y migrada | D-014, D-015, D-025, D-054 |
| 11 | Aliases y valores estructurales | Sustituida y migrada | D-031 a D-033 |
| 12 | Familias cerradas | Migrada; esquema uniforme de datos asociados resuelto | D-038 |
| 13 | Campos | Migrada | D-017, D-019, D-037 |
| 14 | Tipos básicos | Sustituida y migrada | D-028, D-034, D-040 |
| 15 | Conversiones | Sustituida y migrada | D-030, D-032 |
| 16 | Mutabilidad y capacidades | Sustituida y migrada | D-019 |
| 17 | Cardinalidades y colecciones | Sustituida y migrada | D-026, D-039 |
| 18 | Diccionarios | Migrada | D-033, D-039 |
| 19 | Dominios declarativos | Migrada | D-037 |
| 20 | Magnitudes | Sustituida y migrada | D-028, D-059 |
| 21 | Magnitudes lineales | Sustituida y migrada | D-028, D-059 |
| 22 | Prefijos | Sustituida y migrada; catálogo abierto en Q-054 | D-028 |
| 23 | Operaciones de magnitud | Sustituida y migrada | D-028, D-030, D-040 |
| 24 | Magnitudes de punto | Sustituida y migrada | D-028, D-029 |
| 25 | Formato de puntos | Migrada como requisito abierto | D-028; Q-055 |
| 26 | Magnitudes temporales estándar | Migrada como requisito abierto | D-028; Q-033 |
| 27 | Operadores | Migrada y actualizada | D-030, D-032, D-034, D-049 |
| 28 | Intervalos | Sustituida y migrada | D-029, D-047, D-049, D-059 |
| 29 | Precedencia | Migrada como base; ampliación en Q-001 | D-049 |
| 30 | Literales numéricos y `_` | Sustituida y migrada | D-028, D-034, D-050 |
| 31 | Reglas booleanas | Sustituida y migrada | D-022, D-025, D-041 |
| 32 | Reglas reactivas | Sustituida y migrada | D-025, D-041, D-058 |
| 33 | Reglas `always` | Sustituida y migrada | D-025, D-041 |
| 34 | Transición de `when` | Migrada | D-041, D-045, D-058 |
| 35 | `changes` | Sustituida y migrada | D-041, D-058 |
| 36 | Acciones | Sustituida y migrada | D-025, D-036, D-042 |
| 37 | `after` | Migrada | D-042 |
| 38 | `old` | Ampliada y migrada | D-042, D-058 |
| 39 | Acciones elementales | Migrada | D-042 |
| 40 | Acciones compuestas | Migrada | D-042 |
| 41 | Formas exclusivas de `then` | Migrada | D-042 |
| 42 | Resultados de acción | Actualizada y migrada | D-021, D-026, D-042 |
| 43 | `allowed` | Migrada | D-043 |
| 44 | `eventually` | Migrada; análisis abiertos en Q-026 a Q-031 | D-044 |
| 45 | Ondas causales | Actualizada y migrada | D-023, D-045, D-060 |
| 46 | Vinculaciones durante ondas | Migrada; identidad abierta en Q-005 | D-045 |
| 47 | Cola de acciones | Migrada | D-045 |
| 48 | Conflictos | Migrada como núcleo; matriz abierta en Q-006 | D-046, D-060 |
| 49 | Ciclos y terminación | Migrada; algoritmo abierto en Q-020 y Q-029 | D-045 |
| 50 | Efectos permitidos | Actualizada y migrada | D-021, D-023, D-046, D-060 |
| 51 | Asignaciones y actualizaciones | Migrada como núcleo | D-046, D-060 |
| 52 | Cuantificadores y agregaciones | Migrada | D-047 |
| 53 | `for each` | Migrada | D-047 |
| 54 | Operaciones de colección | Actualizada y migrada | D-021, D-026, D-039, D-046 |
| 55 | Creación runtime | Sustituida y migrada | D-023, D-025, D-054 |
| 56 | Destrucción runtime | Sustituida y migrada | D-021, D-023 |
| 57 | Aleatoriedad | Migrada como núcleo | D-048 |
| 58 | Fallos semánticos | Actualizada y migrada | D-042, D-043, D-048 |
| 59 | Valores predeterminados | Sustituida y migrada | D-017, D-034 |
| 60 | Comentarios | Migrada | D-050 |
| 61 | Terminadores | Migrada como base; saltos exactos en Q-001 | D-050 |
| 62 | Lectura y escritura externas | Sustituida y migrada | D-027, D-042 |
| 63 | Grafo semántico | Actualizada y migrada | D-051 |
| 64 | Representación intermedia | Ejemplos retirados; contrato migrado | D-051; Q-009 |
| 65 | Compilador | Actualizada y migrada | D-052 |
| 66 | Materialización TypeScript | Retirada como tecnología normativa; obligaciones migradas | D-052 |
| 67 | Plugin para Codex | Retirado como API normativa; capacidades migradas | D-053 |
| 68 | Clasificación de peticiones | Migrada | D-053 |
| 69 | Inferencias permitidas | Actualizada y migrada | D-053 |
| 70 | Agenda de especificación | Migrada | [[notas/07-plan-de-formalizacion]], [[notas/08-preguntas-abiertas]] |
| 71 | Flujo atómico del plugin | Actualizada y migrada | D-012, D-053 |
| 72 | Tests | Suite obsoleta retirada; obligaciones migradas y tests declarativos añadidos | D-052, D-055; capítulos 43 y 44 previstos |
| 73 | Soporte de editor | Migrada como requisito de tooling | D-052 |
| 74 | Palabras clave provisionales | Catálogo obsoleto retirado; política migrada | D-050, D-052; capítulo 46 previsto |
| 75 | Ejemplo integral | Ejemplo no conforme retirado; propósito preservado | capítulo 47 previsto y corpus de conformidad |
| 76 | Decisiones esenciales | Sustituida por el registro vivo | [[notas/10-registro-de-decisiones]] |
| 77 | Cuestiones abiertas | Sustituida por la agenda viva | [[notas/08-preguntas-abiertas]] |
| 78 | Instrucciones finales | Migradas y actualizadas | D-013, D-053; [[notas/07-plan-de-formalizacion]] |

## Divergencias deliberadas principales

La procedencia detallada vive en cada ADR. Los cambios transversales que explican más sustituciones son:

- `construct` → `thing`; declaración de especialización con `as`, consulta con `is`.
- Intercambio de los usos históricos de `on` y `for`.
- Aliases nominales, inmutables y sin ciclo de vida runtime.
- `look` y `message` como frontera pública de salida.
- Membresía de `thing` estricta y cardinalidad demostrada por cada `then`.
- Suspensión reversible por `destroy` frente a eliminación real por `remove`.
- Nuevo sistema de magnitudes, unidades, puntos, intervalos y `to`.
- `Number` racional exacto y `Rumber` `binary64` explícito.

## Criterio de jubilación satisfecho

La referencia puede permanecer archivada únicamente para:

- comprobar procedencia;
- reconstruir cómo cambió una decisión;
- consultar ejemplos históricos sabiendo que pueden ser inválidos.

No se usa para resolver dudas actuales, completar silencios de la especificación ni implementar MUD. Si un documento vigente depende de una regla, debe enlazar su ADR, capítulo o pregunta abierta, nunca esta referencia.
