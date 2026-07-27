# Preguntas abiertas

Esta es la agenda de diseño. Una pregunta solo se considera cerrada cuando existe una decisión registrada, una actualización del documento dueño y pruebas cuando corresponda.

Prioridades:

- **P0**: bloquea el núcleo v0 o puede forzar una reescritura cercana.
- **P1**: bloquea una fase posterior concreta.
- **P2**: puede aplazarse sin falsear el núcleo.

## P0 — Antes de congelar el núcleo

### Q-001 — Gramática y saltos de línea

¿Cuál es la gramática completa del subconjunto v0 y cuándo un salto de línea termina una instrucción frente a continuar una expresión?

Hay que definir comentarios, sangría irrelevante, recuperación de errores, precedencia y ambigüedades de `in`, receptores y bloques.

### Q-002 — Modelo exacto de efectos secuenciales y simultáneos

¿Qué estado lee cada instrucción de un `then` elemental y cada hoja de una acción compuesta? ¿Cómo se combinan efectos de una misma raíz?

La fuente afirma secuencialidad interna y simultaneidad de hojas; falta una regla operacional que concilie ambas.

### Q-003 — Puntos de validación

¿En qué momento exacto se validan dominios, cardinalidades y `always`: tras cada escritura, al cerrar la raíz, al cerrar cada onda o en varios de esos puntos?

La respuesta afecta qué estados tentativos son observables para reglas posteriores.

### Q-004 — Rollback de `rejected`

¿Se declara normativamente que un `after` falso revierte raíz y ondas igual que un `failed`?

La atomicidad lo implica, pero debe quedar explícito.

### Q-005 — Identidad y ciclo de vida de vinculaciones

¿Cómo se identifica una vinculación `for`, cuál es el valor anterior de `when` al crearla y cuándo se elimina su memoria?

Bloquea el runtime reactivo.

### Q-006 — Conflictos

¿Cuál es la matriz completa de compatibilidad entre asignaciones, incrementos, multiplicaciones y operaciones estructurales concurrentes?

Sin una matriz, la determinación del resultado puede filtrarse desde el orden de implementación.

### Q-007 — Fallos técnicos

¿Qué estructura tiene un error técnico y cómo se distingue de `failed` semántico, de un límite de recursos y de un defecto del runtime?

Debe existir un contrato estable para CLI, plugin y materializaciones.

### Q-008 — Protocolo Git y `READ`

¿Qué operaciones producen commit? Propuesta: consultas `READ` no; CREATE, UPDATE, RETIRE y migraciones sí.

También hay que decidir política de worktree sucio, formato del mensaje y qué derivados se versionan.

### Q-009 — Forma canónica del IR

¿Cuál es el esquema versionado mínimo, cómo conserva procedencia y qué normalizaciones realiza?

El JSON actual es ilustrativo, no suficiente para compatibilidad.

### Q-010 — Estado de las decisiones de la fuente

La fuente afirma que todas las decisiones son vigentes, pero algunas se describen como provisionales o “se mantienen vigentes” sin definición local completa. ¿Qué texto previo se presupone y qué debe incorporarse a la especificación canónica?

### Q-041 — Ontología de constructos

Estado: **cerrada**.

¿Cuál es la estructura matemática común de los constructos declarados y los creados durante la ejecución, y qué añade `create` al mundo?

Decisión: [[notas/decisiones/ADR-014-ontologia-unificada-de-constructos|ADR-014]].

MUD tiene un único dominio conceptual de constructos. Todo constructo concreto es una cosa con identidad y estado propio que también puede ser antecesora. Los abstractos pertenecen al mismo dominio, pero no denotan directamente una cosa concreta. `create` produce otro constructo concreto relacionado mediante el mismo `is`, e `is` es reflexivo y transitivo.

Las consecuencias se separaron en Q-042 y Q-043 y quedaron resueltas mediante [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]].

### Q-042 — Herencia desde un constructo concreto

Estado: **cerrada**.

Cuando un constructo concreto $B$ se especializa a partir de otro constructo concreto $A$, ¿hereda solo las declaraciones, restricciones y valores predeterminados de $A$, o copia u observa también el estado mutable actual de $A$?

Decisión: [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]].

Se heredan esquema y predeterminados efectivos, nunca estado activo. Cada constructo concreto posee estado independiente y `create` inicializa desde predeterminados antes de aplicar sus asignaciones explícitas.

### Q-043 — Ciclos de especialización

Estado: **cerrada**.

¿Debe rechazarse cualquier ciclo no trivial de especialización directa?

Decisión: [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]].

Todo ciclo de especialización directa es inválido. La relación semántica `is` es un orden parcial.

### Q-044 — Identidad y referencias a constructos futuros

¿Qué designa el nombre introducido por `create A`?

Debe decidirse si:

- `A` es una identidad global reservada y la creación solo puede ocurrir una vez.
- `A` es una vinculación local a una identidad fresca y la misma sentencia puede ejecutarse varias veces.
- Existe otro mecanismo explícito para declarar una identidad futura.

La respuesta determina si una regla o acción compilada puede mencionar exactamente `A` antes de su creación, cómo se detectan errores tipográficos, qué ocurre al solicitar una acción antes de que exista y si destruir y recrear conserva identidad.

También afecta a las vinculaciones `for`: una vinculación exacta no existe antes del constructo; al crearlo habría que determinar cuándo nace la vinculación y cuál es su estado anterior, en coordinación con Q-005.

Bloquea resolución de nombres, anclas runtime, repetición de `create`, firmas con participantes y ciclo de vida reactivo.

### Q-045 — Contenido declarativo de `create`

¿Puede el bloque de `create` declarar nuevos campos, restricciones o predeterminados, o solo inicializar el estado permitido por el esquema heredado?

La cuestión es especialmente importante para:

```mud
create abstract B from A
```

Un constructo abstracto no tiene estado concreto que inicializar. Si debe ser plenamente equivalente a una declaración estática con cuerpo, el mundo adquiriría también esquema nuevo durante la ejecución y el compilador no podría conocerlo íntegramente de antemano.

Bloquea la frontera programa–mundo, el sistema de tipos, el IR dinámico y la Unidad 03.

## P1 — Antes de ampliar el lenguaje

### Q-011 — Vinculación nombrada de participantes

Sintaxis canónica, exhaustividad, orden y compatibilidad con receptores multiparte.

### Q-012 — Valores `given` nombrados

Sintaxis en consultas y acciones compuestas; mezcla o no con argumentos posicionales.

### Q-013 — Restricciones relacionales entre participantes `on`

¿Se expresan solo en `if`, mediante tipos/dominios o también en la cabecera?

### Q-014 — Migración de anclas

¿Cómo se renombra o mueve una declaración sin perder historia, referencias ni compatibilidad?

### Q-015 — Retirada

¿`RETIRE` marca obsolescencia, exige reemplazo, elimina físicamente o admite varias fases?

### Q-016 — Canonicalización de constructos creados durante la ejecución

Formato estable de identidad, snapshots, comparación y referencias entre constructos creados.

### Q-017 — Dominios dinámicos circulares

Qué ciclos son inválidos y si existe un punto fijo admisible.

### Q-018 — Intervalos discontinuos

Normalización canónica, igualdad, orden descendente y varias claves.

### Q-019 — Números

Redondeo de `Money`, conversiones estrechas, límites numéricos, overflow y división por cero.

### Q-020 — Oscilaciones y límite de ondas

Detección semántica, salvaguarda técnica, diagnósticos y reproducibilidad.

### Q-021 — Análisis estático de conflictos

Qué conflictos pueden probarse en compilación y cuáles solo en una resolución concreta.

### Q-022 — Valores de retorno de acciones

¿Además del resultado operativo, una acción puede producir valores de dominio? Si sí, ¿cómo interactúan con atomicidad y composición?

### Q-023 — Composición dinámica

Si una acción puede seleccionar dinámicamente otras acciones, cómo se conserva aciclicidad y análisis de impacto.

### Q-024 — Familias cerradas

Campos específicos por valor y herencia de familias cerradas.

### Q-025 — Destrucción de constructos estáticos

Si está permitida y qué significa para anclas, referencias y estados.

## P2 — Funciones avanzadas

### Q-026 — Varias acciones en `eventually`

Sintaxis, unión de espacios de entrada y orden de enumeración.

### Q-027 — Estado relevante

Cómo calcular la proyección mínima de estado que conserva la verdad de una consulta de alcanzabilidad.

### Q-028 — Finitud

Límites del análisis, aproximaciones conservadoras y mensajes cuando no puede demostrarse.

### Q-029 — Terminación

Qué clases de acciones y reglas puede certificar el compilador.

### Q-030 — Perfil de mundos finitos

Conjunto explícito de restricciones que habilita `eventually`.

### Q-031 — Subconjunto no Turing completo

Si merece la pena definirlo, qué garantías ofrece y cómo convive con el lenguaje general.

### Q-032 — Aleatoriedad reproducible

Subsemillas, cachés, identidad de puntos aleatorios y exposición de campos estocásticos.

### Q-033 — Calendarios y localización

Calendario civil inicial, zonas horarias, formatos, idiomas y separación entre valor y presentación.

### Q-034 — Magnitudes derivadas

Composición dimensional, simplificación, equivalencias y errores.

### Q-035 — Coste de `allowed`

Memorización, profundidad especulativa, ciclos y límites de recursos sin cambiar su verdad semántica.

## Preguntas de producto adicionales

### Q-036 — Unidad de interacción humana

¿La persona aprueba un plan completo, cada operación o solo los cambios clasificados como peligrosos?

### Q-037 — Convivencia con código manual

¿Qué partes de una materialización pueden editarse a mano y cómo se evita que una regeneración las destruya o introduzca semántica oculta?

### Q-038 — Compatibilidad entre versiones del lenguaje

¿Cómo se declara la versión MUD de un proyecto y cómo se migran fuente, IR y materializaciones?

### Q-039 — Explicación suficiente

¿Qué evidencia mínima debe presentar el sistema antes y después de un cambio para que una persona pueda confiar en él?

### Q-040 — Amenazas y permisos

¿Qué operaciones puede ejecutar automáticamente la IA y cuáles requieren autorización por afectar Git, archivos, materializaciones o sistemas externos?

## Formato para cerrar una pregunta

Al resolver una cuestión:

1. Crear una decisión en [10-registro-de-decisiones.md](10-registro-de-decisiones.md).
2. Incluir alternativas y consecuencias.
3. Actualizar el documento dueño.
4. Añadir ejemplos y contraejemplos.
5. Añadir pruebas de conformidad si ya existe implementación.
6. Marcar aquí la pregunta como cerrada con enlace a la decisión.
