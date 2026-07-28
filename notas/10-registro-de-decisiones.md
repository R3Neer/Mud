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
| D-004 | Sustituida parcialmente por D-025 y D-027 | Catálogo histórico de declaraciones principales | [02-modelo-del-lenguaje.md](02-modelo-del-lenguaje.md) | Secciones 3 y 76 |
| D-005 | Sustituida por D-025 | Distribución histórica de `on`, `for` y `given` | [ADR-025](decisiones/ADR-025-vocabulario-cabeceras-y-bloques.md) | Secciones 6 y 76 |
| D-006 | Vigente | Las reglas booleanas son puras y las acciones forman la API de escritura | [02-modelo-del-lenguaje.md](02-modelo-del-lenguaje.md) | Secciones 7, 31, 36 y 62 |
| D-007 | Vigente | Las resoluciones causales ocurren por ondas sobre instantáneas | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | Secciones 45 a 49 |
| D-008 | Vigente | Una acción produce `accepted`, `rejected` o `failed` | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | Sección 42 |
| D-009 | Vigente | `allowed` es especulación descartable y propaga fallos | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | Sección 43 |
| D-010 | Vigente | `eventually` exige prueba de finitud y terminación | [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | Sección 44 |
| D-011 | Vigente | Los derivados no pueden añadir comportamiento de dominio | [04-arquitectura-del-sistema.md](04-arquitectura-del-sistema.md) | Secciones 2.1, 63 a 66 |
| D-012 | Vigente | Los cambios semánticos válidos se validan y versionan atómicamente | [05-cambios-semanticos-y-git.md](05-cambios-semanticos-y-git.md) | Secciones 68 a 71 e introducción del usuario |
| D-013 | Vigente | La especificación formal del lenguaje completo precederá a la continuación de su implementación | [especificacion/README.md](../especificacion/README.md) | Decisión del autor, 2026-07-27 |
| D-014 | Vigente | Los constructos forman un único dominio, los concretos son cosas y posibles antecesores, y `is` es reflexivo | [ADR-014](decisiones/ADR-014-ontologia-unificada-de-constructos.md) | Decisión del autor, 2026-07-27 |
| D-015 | Vigente | La especialización hereda esquema y predeterminados, mantiene estados independientes y rechaza ciclos | [ADR-015](decisiones/ADR-015-especializacion-aciclica-y-estado-independiente.md) | Decisión del autor, 2026-07-27 |
| D-016 | Vigente con sintaxis sustituida por D-025 | `create` puede producir identidades raíz, abstractas o con varios antecesores; la sintaxis vigente usa `thing` y `as` | [ADR-016](decisiones/ADR-016-creacion-generalizada-de-constructos.md) | Decisión del autor, 2026-07-27 |
| D-017 | Vigente | Todo tipo bien formado posee un valor predeterminado perteneciente a su dominio | [ADR-017](decisiones/ADR-017-valor-predeterminado-de-todo-tipo.md) | Decisión del autor, 2026-07-27 |
| D-018 | Sustituida parcialmente por D-025 | Separó la declaración directa de la consulta `is`; su sintaxis `construct`/`from` es histórica | [ADR-018](decisiones/ADR-018-from-declara-is-consulta.md) | Decisión del autor, 2026-07-27 |
| D-019 | Vigente | La mutabilidad de una colección y la capacidad sobre sus miembros son ortogonales incluso en `[1]` | [ADR-019](decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros.md) | Decisión del autor, 2026-07-27 |
| D-020 | Sustituida por D-026 | Propuso `[reflexive]` para habilitar el ancla exacta | [ADR-020](decisiones/ADR-020-membresia-estricta-y-reflexive.md) | Decisión del autor, 2026-07-27 |
| D-021 | Vigente | `destroy` suspende declaraciones y dependientes sin borrar su almacenamiento; `remove` sí elimina una propiedad y su carga | [ADR-021](decisiones/ADR-021-ciclo-de-vida-logico-y-suspension.md) | Decisión del autor, 2026-07-27 |
| D-022 | Vigente | Una llamada a una regla booleana inactiva se borra estructuralmente y la expresión exterior vacía se cierra con verdadero | [ADR-022](decisiones/ADR-022-borrado-de-reglas-booleanas-inactivas.md) | Decisión del autor, 2026-07-27 |
| D-023 | Vigente | Los `then` conservan secuencialidad local y consolidan efectos estructurales de forma determinista; los fragmentos compatibles de constructos se fusionan | [ADR-023](decisiones/ADR-023-consolidacion-de-efectos-estructurales.md) | Decisión del autor, 2026-07-27 |
| D-024 | Vigente | Cada regla y alias tiene una única definición completa; `create Nombre` activa su descriptor canónico y las activaciones concurrentes se consolidan | [ADR-024](decisiones/ADR-024-definicion-unica-y-activacion-abreviada.md) | Decisión del autor, 2026-07-27 |
| D-025 | Vigente | `thing` y `as` sustituyen `construct` y `from`; `on` se usa en observadores y `for` en solicitudes; las cláusulas simples pueden omitir llaves | [ADR-025](decisiones/ADR-025-vocabulario-cabeceras-y-bloques.md) | Decisión del autor, 2026-07-27 |
| D-026 | Vigente | La membresía de `thing` es siempre estricta y cada `then` debe demostrar estáticamente su cardinalidad final y la compatibilidad de consolidación | [ADR-026](decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then.md) | Decisión del autor, 2026-07-27 |
| D-027 | Vigente | `look` consulta el estado estable y `message` publica tras estabilizar valores de un evento detectado durante una acción | [ADR-027](decisiones/ADR-027-salidas-look-y-message.md) | Decisión del autor, 2026-07-27 |
| D-028 | Vigente | Los tipos numéricos básicos representan números; las magnitudes aportan dimensión y derivan automáticamente unidades compatibles | [ADR-028](decisiones/ADR-028-sistema-de-magnitudes-y-unidades.md) | Decisión del autor, 2026-07-28 |
| D-029 | Vigente | `*` designa el límite efectivo lateral; los dominios de magnitud usan límites canónicos desnudos y solo los puntos admiten `[a..b cycle)` | [ADR-029](decisiones/ADR-029-intervalos-estrellas-y-ciclos.md) | Decisión del autor, 2026-07-28 |
| D-030 | Vigente | `in` cambia la unidad de expresión y `to` realiza únicamente conversiones cuantitativas compatibles | [ADR-030](decisiones/ADR-030-conversion-cuantitativa-explicita.md) | Decisión del autor, 2026-07-28 |

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
