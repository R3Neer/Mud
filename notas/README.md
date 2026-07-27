# Notas de trabajo de MUD

Esta carpeta convierte la especificación inicial en un espacio de trabajo para pasar de ideación a formalización e implementación temprana. No sustituye la especificación fuente ni intenta reescribirla entera: la descompone por responsabilidades, identifica dependencias y separa decisiones vigentes de propuestas y preguntas.

Documento de procedencia:

- `C:\Users\Usuario\Downloads\MUD Especificacion inicial.md`
- Estado observado: especificación inicial de 78 secciones.
- Regla de interpretación: cuando estas notas resuman una decisión, la especificación inicial sigue siendo la autoridad hasta que exista una especificación canónica versionada en el repositorio.

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
| [08-preguntas-abiertas.md](08-preguntas-abiertas.md) | ¿Qué falta decidir y qué bloquea? | Decisiones tomadas en silencio |
| [09-riesgos-y-restricciones.md](09-riesgos-y-restricciones.md) | ¿Dónde puede fallar el concepto o la ejecución del proyecto? | Lista de tareas |
| [10-registro-de-decisiones.md](10-registro-de-decisiones.md) | ¿Cómo se documentan decisiones y propuestas? | La explicación normativa completa de cada tema |
| [11-trazabilidad-de-la-fuente.md](11-trazabilidad-de-la-fuente.md) | ¿Dónde quedó cubierta cada parte del documento inicial? | Repetición de la especificación |

## Convenciones para trabajar en esta carpeta

Cada afirmación nueva debería estar marcada mentalmente como una de estas categorías:

- **Decisión vigente**: aparece afirmada como tal en la especificación inicial.
- **Propuesta**: recomendación de estas notas para poder avanzar.
- **Pregunta abierta**: requiere una decisión explícita.
- **Inferencia**: conclusión razonable, pero no declarada literalmente en la fuente.

No se debe convertir una propuesta o inferencia en comportamiento del compilador sin registrarla como decisión. Las preguntas se cierran mediante una entrada en el registro de decisiones y una actualización del documento dueño del tema.

## Regla contra redundancias

Cada concepto tiene un único documento dueño. Los demás documentos lo enlazan y solo añaden el contexto específico que necesitan. Por ejemplo:

- `action`, `rule`, `construct` y `given` pertenecen al modelo del lenguaje.
- Las ondas, `accepted/rejected/failed` y el rollback pertenecen a la semántica de ejecución.
- El AST, el grafo, el IR y los materializadores pertenecen a la arquitectura.
- CREATE, UPDATE, RETIRE, el diff y el commit pertenecen al protocolo de cambios.
- La secuencia de hitos pertenece al plan de formalización.

## Próximo uso recomendado

La siguiente sesión de diseño debería empezar por:

1. Aceptar o corregir el corte de [06-nucleo-vertical-v0.md](06-nucleo-vertical-v0.md).
2. Resolver las preguntas P0 de [08-preguntas-abiertas.md](08-preguntas-abiertas.md).
3. Crear una especificación normativa versionada y una gramática ejecutable.
4. Elegir dos o tres ejemplos canónicos que actúen como pruebas de aceptación.

