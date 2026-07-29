# Notas de trabajo de MUD

Esta carpeta convierte la especificación inicial en un espacio de trabajo para pasar de ideación a formalización e implementación temprana. La descompone por responsabilidades, identifica dependencias y separa decisiones vigentes de propuestas y preguntas.

Documento de procedencia:

- [[referencias/retiradas/MUD Especificacion inicial|MUD — Especificación inicial histórica retirada]].
- Estado: sus 78 secciones han sido migradas, sustituidas o retiradas conforme a [[notas/13-auditoria-de-cobertura-y-divergencias]].
- Regla de interpretación: la referencia conserva únicamente procedencia; nunca completa silencios de la especificación actual.

## Qué se está construyendo

MUD no es solamente una sintaxis ni solamente un compilador. Es un sistema de ingeniería semántica formado por:

1. Un lenguaje declarativo que representa lógica de dominio.
2. Un modelo semántico direccionable mediante anclas.
3. Un motor transaccional y causal que ejecuta acciones y reglas.
4. Un compilador que valida y produce artefactos reconstruibles.
5. Una capa de interacción para que una persona trabaje principalmente en lenguaje natural.
6. Un protocolo Git que convierte cada cambio semántico válido en una unidad trazable.
7. Materializadores reemplazables que generan código y otros derivados.

La dificultad principal no es analizar texto. Es garantizar que una intención expresada en lenguaje natural se convierta en un cambio semántico correcto, explicable, atómico, reversible y reproducible.

## Mapa de las notas

| Documento | Pregunta que responde | No contiene |
| --- | --- | --- |
| [01-vision-y-alcance.md](01-vision-y-alcance.md) | ¿Qué producto es MUD y dónde termina? | Sintaxis detallada o plan de implementación |
| [02-modelo-del-lenguaje.md](02-modelo-del-lenguaje.md) | ¿Qué conceptos expresa el lenguaje? | Algoritmo de ondas o arquitectura del tooling |
| [03-semantica-de-ejecucion.md](03-semantica-de-ejecucion.md) | ¿Cómo pasa el mundo de un estado estable a otro? | Diseño del parser o experiencia conversacional |
| [04-arquitectura-del-sistema.md](04-arquitectura-del-sistema.md) | ¿Qué componentes necesita la plataforma? | Roadmap y decisiones sintácticas finas |
| [05-cambios-semanticos-y-git.md](05-cambios-semanticos-y-git.md) | ¿Cómo se consulta, cambia, valida y versiona un modelo? | Semántica completa del DSL |
| [06-nucleo-vertical-v0.md](06-nucleo-vertical-v0.md) | ¿Cuál es el primer corte ejecutable y demostrable? | Funcionalidades avanzadas |
| [07-plan-de-formalizacion.md](07-plan-de-formalizacion.md) | ¿En qué orden se reduce la incertidumbre y se implementa? | Inventario completo de dudas |
| [preguntas/README.md](preguntas/README.md) | ¿Qué falta decidir y qué bloquea? | Decisiones tomadas en silencio |
| [09-riesgos-y-restricciones.md](09-riesgos-y-restricciones.md) | ¿Dónde puede fallar el concepto o la ejecución del proyecto? | Lista de tareas |
| [10-registro-de-decisiones.md](10-registro-de-decisiones.md) | ¿Cómo se documentan decisiones y propuestas? | La explicación normativa completa de cada tema |
| [11-trazabilidad-de-la-fuente.md](11-trazabilidad-de-la-fuente.md) | ¿Qué documento es dueño de cada parte del documento inicial? | Afirmaciones sobre cobertura completa |
| [12-destruccion-colecciones-y-grafo-activo.md](12-destruccion-colecciones-y-grafo-activo.md) | ¿Cómo interactúan destrucción, estado latente y dependencias? | La norma definitiva del ciclo de vida |
| [13-auditoria-de-cobertura-y-divergencias.md](13-auditoria-de-cobertura-y-divergencias.md) | ¿Dónde fue a parar cada una de las 78 secciones de la fuente retirada? | La formalización que aún queda por hacer |

## Convenciones para trabajar en esta carpeta

Cada afirmación nueva debería estar marcada mentalmente como una de estas categorías:

- **Decisión vigente**: figura como vigente en [[10-registro-de-decisiones]] o en un capítulo normativo.
- **Propuesta**: recomendación de estas notas para poder avanzar.
- **Pregunta abierta**: requiere una decisión explícita.
- **Inferencia**: conclusión razonable, pero no declarada literalmente en la fuente.

No se debe convertir una propuesta o inferencia en comportamiento del compilador sin registrarla como decisión. Las preguntas se cierran mediante una entrada en el registro de decisiones y una actualización del documento dueño del tema.

## Regla contra redundancias

Cada concepto tiene un único documento dueño. Los demás documentos lo enlazan y solo añaden el contexto específico que necesitan. Por ejemplo:

- `action`, `rule`, `thing`, `look`, `message` y `given` pertenecen al modelo del lenguaje.
- Las ondas, `accepted/rejected/failed` y el rollback pertenecen a la semántica de ejecución.
- El AST, el grafo, el IR y los materializadores pertenecen a la arquitectura.
- CREATE, UPDATE, RETIRE, el diff y el commit pertenecen al protocolo de cambios.
- La secuencia de hitos pertenece al plan de formalización.

## Próximo uso recomendado

La siguiente sesión de diseño debería empezar por:

1. Continuar el índice de [la especificación formal](../especificacion/README.md) con sus convenciones editoriales y notación matemática.
2. Resolver las preguntas P0 del [índice de preguntas activas](preguntas/README.md) y.
3. Formalizar el modelo matemático de mundo, estado, valor, identidad y ancla.
4. Elegir ejemplos canónicos que actúen como testigos de cada regla normativa.
