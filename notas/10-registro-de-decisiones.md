# Registro de decisiones

Este archivo es un índice de decisiones, no una duplicación de la especificación. Cada decisión nueva debería tener su propio archivo futuro en `notas/decisiones/ADR-NNN-titulo.md` cuando necesite razonamiento amplio.

## Estados

- **Vigente**: norma actual.
- **Propuesta**: candidata pendiente de aprobación.
- **Sustituida**: reemplazada por otra decisión.
- **Rechazada**: considerada y descartada.

## Decisiones vigentes

| ID | Estado | Decisión | Documento dueño | Procedencia |
| --- | --- | --- | --- | --- |
| D-001 | Vigente | `.mud` es la fuente semántica de verdad | [01-vision-y-alcance.md](01-vision-y-alcance.md) | Secciones 2.1 y 76 |
| D-002 | Vigente | MUD describe dominio, no arquitectura de aplicación | [01-vision-y-alcance.md](01-vision-y-alcance.md) | Secciones 2.2 y 66 |
| D-003 | Vigente | MUD es un lenguaje declarativo, no lenguaje natural controlado | [01-vision-y-alcance.md](01-vision-y-alcance.md) | Sección 2.3 |
| D-004 | Vigente | Declaraciones principales: `construct`, `magnitude`, `rule`, `action`; `alias` es auxiliar | [02-modelo-del-lenguaje.md](02-modelo-del-lenguaje.md) | Secciones 3 y 76 |
| D-005 | Vigente | `on`, `for` y `given` tienen funciones semánticas distintas | [02-modelo-del-lenguaje.md](02-modelo-del-lenguaje.md) | Secciones 6 y 76 |
| D-006 | Vigente | Las reglas booleanas son puras y las acciones forman la API de escritura | [02-modelo-del-lenguaje.md](02-modelo-del-lenguaje.md) | Secciones 7, 31, 36 y 62 |
| D-007 | Vigente | Las resoluciones causales ocurren por ondas sobre instantáneas | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | Secciones 45 a 49 |
| D-008 | Vigente | Una acción produce `accepted`, `rejected` o `failed` | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | Sección 42 |
| D-009 | Vigente | `allowed` es especulación descartable y propaga fallos | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | Sección 43 |
| D-010 | Vigente | `eventually` exige prueba de finitud y terminación | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | Sección 44 |
| D-011 | Vigente | Los derivados no pueden añadir comportamiento de dominio | [04-arquitectura-del-sistema.md](04-arquitectura-del-sistema.md) | Secciones 2.1, 63 a 66 |
| D-012 | Vigente | Los cambios semánticos válidos se validan y versionan atómicamente | [05-cambios-semanticos-y-git.md](05-cambios-semanticos-y-git.md) | Secciones 68 a 71 e introducción del usuario |
| D-013 | Vigente | La especificación formal del lenguaje completo precederá a la continuación de su implementación | [especificacion/README.md](../especificacion/README.md) | Decisión del autor, 2026-07-27 |
| D-014 | Vigente | Los constructos forman un único dominio, los concretos son cosas y posibles antecesores, `create` crea otro constructo e `is` es reflexivo | [ADR-014](decisiones/ADR-014-ontologia-unificada-de-constructos.md) | Decisión del autor, 2026-07-27 |
| D-015 | Vigente | La especialización hereda esquema y predeterminados, mantiene estados independientes y rechaza ciclos | [ADR-015](decisiones/ADR-015-especializacion-aciclica-y-estado-independiente.md) | Decisión del autor, 2026-07-27 |
| D-016 | Vigente | `create` puede producir constructos raíz, abstractos o con varios antecesores mediante `from` | [ADR-016](decisiones/ADR-016-creacion-generalizada-de-constructos.md) | Decisión del autor, 2026-07-27 |

## Propuestas de estas notas

| ID | Estado | Propuesta | Motivo | Pregunta relacionada |
| --- | --- | --- | --- | --- |
| P-001 | Sustituida | Adoptar el corte de núcleo vertical v0 como objetivo inmediato de implementación | Sustituida por D-013; el corte v0 se conserva como futuro primer objetivo de implementación y como primer ciclo de formalización | Q-001 a Q-009 |
| P-002 | Propuesta | Separar AST de superficie e IR canónico | Conservar procedencia y desacoplar sintaxis de semántica | Q-009 |
| P-003 | Propuesta | No crear commits para consultas `READ` puras | Git registra cambios de estado, no lecturas | Q-008 |
| P-004 | Propuesta | Preparar cambios en un área aislada y publicar al validar | Evitar rollback incompleto y commits contaminados | Q-008 |
| P-005 | Propuesta | Posponer `allowed`, `eventually` y azar hasta estabilizar el runtime | Reutilizar una semántica transaccional probada | Q-026 a Q-035 |

## Plantilla ADR

```markdown
# ADR-NNN — Título

- Estado: Propuesta
- Fecha:
- Preguntas: Q-NNN
- Documentos afectados:

## Contexto

Qué problema obliga a decidir y qué comportamiento ya está comprometido.

## Decisión

Regla normativa, expresada de forma comprobable.

## Alternativas

Opciones consideradas y por qué se descartan.

## Consecuencias

Impacto en sintaxis, AST, IR, runtime, grafo, tooling, compatibilidad y tests.

## Ejemplos

Casos válidos, inválidos y límites.

## Verificación

Pruebas o propiedades que demuestran la decisión.
```

## Proceso

1. Una pregunta abierta motiva una propuesta.
2. La propuesta enumera alternativas y consecuencias.
3. Se aprueba, rechaza o sustituye explícitamente.
4. Se actualizan especificación, nota dueña y tests.
5. El registro enlaza la decisión sin repetir toda su argumentación.
