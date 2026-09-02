# Instrucciones de trabajo del repositorio MUD

Estas instrucciones se aplican a todo el repositorio.

## Autoridad

- `especificacion/` contendrá la norma de MUD.
- `notas/` contendrá análisis, planificación, riesgos y decisiones.
- `gobierno/` contendrá procesos editoriales y de control de cambios.

## Instantánea normativa

Los documentos y artefactos normativos de `especificacion/` describen el estado actual de MUD dentro de su alcance. Antes de modificarlos se deben aplicar íntegramente MUD-EDIT-002 y MUD-EDIT-003 de `especificacion/00-convenciones-editoriales.md`.

En particular:

- La historia de introducción, modificación, sustitución o retirada de una regla no se conserva en el cuerpo normativo; pertenece a ADR, Git y metadatos de trazabilidad.
- Las decisiones relacionadas se registran mediante `decisions:` y no se narran como procedencia dentro del cuerpo de `especificacion/`.
- Una pregunta activa puede citarse en el cuerpo solo para delimitar una incertidumbre que afecta al estado actual; debe figurar también en `questions:`.
- Una decisión vigente debe integrarse en toda superficie normativa ya desarrollada cuya responsabilidad cubra su alcance. Si la ubicación canónica todavía no existe, no se inventa una superficie provisional solo para alojarla, pero ninguna superficie existente puede contradecirla.
- Si el cambio afecta resolución nominal, debe aplicarse además MUD-EDIT-004 y revisarse `especificacion/09-nombres-y-anclas.md` junto con `especificacion/nombres/mud-nominal-hir.asdl`.

La barrera mecánica de MUD-EDIT-002 y del tratamiento de preguntas se ejecuta con `python gobierno/validate_spec_editorial.py`. Todo cambio que toque `especificacion/` o `notas/preguntas/` debe pasarla antes del commit. Si se modifica la propia barrera, se ejecuta además `python gobierno/test_validate_spec_editorial.py`.

## Archivos temporales

Los documentos intencionadamente temporales se rigen por `gobierno/POLITICA-DE-ARCHIVOS-TEMPORALES.md`. Los archivos efímeros ordinarios no se versionan.

Antes de crear cualquier commit se debe ejecutar `python gobierno/validate_temporaries.py` y revisar el inventario completo de documentos con `temporary: true`. Si la condición `temporary-delete-when` de alguno ya se cumple, debe eliminarse antes de cerrar el commit, salvo que el propio cambio modifique explícitamente su ciclo de vida.

La temporalidad se declara únicamente en el frontmatter del documento; `gobierno/temporales.base` es una vista derivada y no un registro independiente.

## Git

Antes de modificar archivos se debe leer y seguir `gobierno/POLITICA-DE-COMMITS.md`.

Después de completar y validar una unidad coherente de trabajo, Codex debe:

1. Revisar el estado y el diff.
2. Añadir únicamente los archivos pertenecientes a la tarea.
3. Crear un commit atómico conforme a la política.
4. Verificar el estado posterior.

No se debe hacer push ni reescribir historial sin petición explícita.

## Publicación documental

La publicación y promoción de documentos normativos se rige por `gobierno/CICLO-DOCUMENTAL.md`.

Antes de marcar un capítulo como `vigente` se debe realizar la pasada de publicación y comprobar que su contenido expresa únicamente el estado normativo actual dentro de su alcance.

## Cambios remotos desde ChatGPT

Cuando el entorno permita editar directamente el repositorio mediante GitHub, una rama, una pull request o un checkout escribible, se prefiere un flujo Git normal con candidata aislada, validaciones, revisión exhaustiva del diff, commits atómicos y publicación por fast-forward.

Si una candidata falla en una capa concreta, debe corregirse esa capa y repetirse la revisión desde el punto afectado. Si `main` cambia durante el trabajo, no se fuerza la referencia: se inspecciona el nuevo estado y se reconstruye la candidata sobre la nueva base.

## Preguntas

La apertura, actualización, división y cierre de preguntas se rige por `gobierno/POLITICA-DE-PREGUNTAS.md`.

Las preguntas cerradas no deben permanecer en índices activos ni en el frontmatter `questions` de la especificación. Su archivo estable se conserva como trazabilidad y enlaza las decisiones o evidencias que las resolvieron.
