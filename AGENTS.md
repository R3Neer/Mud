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
