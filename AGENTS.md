# Instrucciones de trabajo del repositorio MUD

Estas instrucciones se aplican a todo el repositorio.

## Formalización didáctica

Antes de crear o modificar material relacionado con la especificación formal de MUD, se debe leer y seguir íntegramente:

- `aprendizaje/REGLAS-DIDACTICAS.md`
- `especificacion/00-convenciones-editoriales.md`

El objetivo no es sustituir al autor escribiendo toda la especificación, sino enseñarle progresivamente a formalizar el lenguaje. Debe respetarse la distribución de trabajo indicada por el nivel didáctico actual en `aprendizaje/PROGRESO.md`.

Los espacios marcados como trabajo del autor no deben completarse automáticamente antes de que haya realizado un intento, salvo que lo solicite expresamente.

## Autoridad

- `especificacion/` contendrá la norma de MUD.
- `aprendizaje/` contendrá explicaciones, ejercicios y seguimiento; no define la semántica del lenguaje.
- `notas/` contendrá análisis, planificación, riesgos y decisiones.
- `gobierno/` contendrá procesos editoriales y de control de cambios.

Una explicación didáctica nunca puede introducir silenciosamente una regla normativa.

## Git

Antes de modificar archivos se debe leer y seguir `gobierno/POLITICA-DE-COMMITS.md`.

Después de completar y validar una unidad coherente de trabajo, Codex debe:

1. Revisar el estado y el diff.
2. Añadir únicamente los archivos pertenecientes a la tarea.
3. Crear un commit atómico conforme a la política.
4. Verificar el estado posterior.

No se debe hacer push ni reescribir historial sin petición explícita.

## Publicación documental

La promoción desde material didáctico hasta norma se rige por `gobierno/CICLO-DOCUMENTAL.md`.

La especificación no debe contener ejercicios, pistas ni referencias al proceso personal de aprendizaje. Cuando el autor indique que una parte está revisada, se debe realizar la pasada de publicación antes de marcarla vigente.

## Patches descargables

Cuando el usuario solicite expresamente un patch descargable, o cuando el entorno no permita modificar directamente el repositorio y los cambios deban ser aplicados localmente por el usuario, debe leerse y seguirse `gobierno/USO-DE-REPO-PATCHER.md`.

Esta regla no se aplica cuando el agente puede editar directamente el repositorio mediante Codex, un checkout escribible, GitHub, una rama o una pull request.
## Preguntas

La apertura, actualización, división y cierre de preguntas se rige por `gobierno/POLITICA-DE-PREGUNTAS.md`.

Las preguntas cerradas no deben permanecer en índices activos ni en el frontmatter `questions` de la especificación. Su archivo estable se conserva como trazabilidad y enlaza las decisiones o evidencias que las resolvieron.
