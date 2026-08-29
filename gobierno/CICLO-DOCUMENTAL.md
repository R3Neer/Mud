---
title: Ciclo documental de MUD
aliases:
  - Publicación normativa
tags:
  - mud/gobierno
  - mud/especificacion
status: vigente
---

# Ciclo documental de MUD

Gestión de cuestiones abiertas: [[POLITICA-DE-PREGUNTAS|Política de preguntas de MUD]].

## Propósito

La especificación de MUD debe mantener una separación estricta entre el estado normativo actual, la procedencia de las decisiones y las cuestiones todavía abiertas. Este proceso define cómo se prepara, revisa y publica un documento normativo sin convertir borradores, historia decisional o razonamientos provisionales en parte de la norma vigente.

La separación entre estado vigente, decisiones y cuestiones abiertas se rige por MUD-EDIT-002 y MUD-EDIT-003 de [[especificacion/00-convenciones-editoriales]].

## Superficie normativa

Ubicación: `especificacion/`.

Puede contener:

- Definiciones.
- Reglas normativas identificadas.
- Notación formal.
- Ejemplos y contraejemplos informativos.
- Teoremas, lemas, demostraciones y conjeturas claramente clasificados.
- Cuestiones abiertas explícitas cuando delimitan el estado actual.
- Metadatos de trazabilidad hacia decisiones y preguntas.
- Criterios de conformidad.

No puede contener:

- Conversación.
- Razonamientos provisionales presentados como norma.
- Historia de introducción, modificación, sustitución o retirada de reglas como parte de la exposición normativa.
- Secciones aditivas que corrijan una regla anterior en vez de reescribir su ubicación canónica.
- Soluciones incompletas presentadas como norma.

## Estados de un capítulo

```text
esqueleto
→ borrador
→ propuesta
→ en-revisión
→ vigente
```

- **Esqueleto**: estructura sin contenido suficiente.
- **Borrador**: contenido incompleto que puede cambiar ampliamente.
- **Propuesta**: semántica completa candidata a revisión.
- **En revisión**: el contenido se considera candidato a publicación y se ejecuta la pasada de publicación.
- **Vigente**: texto aceptado como norma actual.

Un capítulo `vigente` puede contener cuestiones abiertas solo si la característica afectada queda marcada fuera de MUD 1.0 o si la cuestión no altera su significado.

### Autoridad durante la promoción

La ubicación en `especificacion/` y `normative: true` indican que un archivo pertenece a la superficie normativa, no que todo su contenido esté ya aprobado. La autoridad del capítulo como unidad aparece al alcanzar `status: vigente`.

Antes de `vigente`, un capítulo puede recoger reglas que ya tengan autoridad por decisiones vigentes y por artefactos mecánicos normativos coherentes. Esa transcripción no concede al capítulo potestad para cambiar esas reglas, cerrar preguntas o introducir una semántica alternativa. Si diverge de una decisión vigente, existe un defecto documental que bloquea la promoción. Si prosa y artefacto mecánico divergen, se aplica la regla editorial MUD-EDIT-001: la divergencia debe resolverse explícitamente y ninguna de las dos superficies adquiere prioridad silenciosa.

Por tanto, la promoción a `vigente` certifica el capítulo completo; no es el mecanismo que hace vigentes retroactivamente las decisiones que ya documentaba.

### Integración de decisiones vigentes

La promoción de una decisión no obliga a crear anticipadamente todos los capítulos futuros de la especificación. Se aplica MUD-EDIT-003:

1. Se identifican las superficies normativas ya desarrolladas cuya responsabilidad cubre la decisión.
2. Todas ellas se actualizan en el mismo cambio o se registra explícitamente un bloqueo que impida hacerlo.
3. Si la ubicación canónica todavía es solo un capítulo previsto, el ADR vigente mantiene autoridad transitoria sobre esa parte hasta su formalización.
4. Ningún documento existente, incluidos índices y mapas de capítulos futuros, puede conservar una descripción incompatible con la decisión vigente.
5. No se considera suficiente añadir al final de un documento una sección de «actualización»: la regla vigente debe quedar integrada en su lugar canónico.

## Flujo de publicación

La promoción de un capítulo sigue estos pasos:

1. Se identifica el alcance normativo que el capítulo pretende cubrir.
2. Se comprueba qué decisiones vigentes y cuestiones abiertas afectan a ese alcance.
3. Se resuelven o registran las cuestiones que impidan expresar un contrato inequívoco.
4. Se redacta el estado actual en estilo normativo.
5. Se unifica la notación con [[especificacion/03-notacion]].
6. Se añaden identificadores normativos cuando correspondan.
7. Se comprueban ejemplos, contraejemplos e interacciones.
8. Se verifican enlaces, dependencias y metadatos de trazabilidad.
9. Se elimina del cuerpo cualquier historia decisional o procedencia que no forme parte del estado vigente.
10. Se comprueba la integración en todas las superficies ya desarrolladas afectadas.
11. Se ejecuta la pasada de publicación.
12. Se cambia el estado y se crea un commit atómico.

## Pasada de publicación

Antes de promover un capítulo a `vigente` se realizan las siguientes revisiones.

### Revisión semántica

- Correspondencia entre prosa, fórmulas y ejemplos.
- Ausencia de casos sin definir dentro del alcance declarado.
- Compatibilidad con capítulos vigentes.
- Compatibilidad con decisiones vigentes aplicables.
- Distinción entre norma, propuesta y cuestión abierta.
- Búsqueda de contraejemplos.
- Comprobación de que ninguna superficie existente conserve semántica sustituida.

### Revisión formal

- Símbolos definidos antes de usarse.
- Juicios y reglas bien formados.
- Hipótesis explícitas.
- Cuantificadores y dominios inequívocos.
- Nombres consistentes.

### Revisión editorial

- Aplicación de MUD-EDIT-002: el cuerpo describe el estado vigente y no la historia de las decisiones.
- Ausencia de identificadores `D-NNN` o `ADR-NNN` usados como procedencia o justificación en el cuerpo normativo.
- Preguntas corporales limitadas a preguntas activas, registradas además en `questions:`, y formuladas como incertidumbre presente.
- Ausencia de secciones aditivas de actualización o retirada.
- Aplicación de MUD-EDIT-003 a todas las superficies ya desarrolladas afectadas.
- Redacción normativa uniforme.
- Identificadores estables.
- Wikilinks y referencias.
- Frontmatter y estado correctos.
- Ejemplos informativos claramente marcados.

### Revisión mecánica

- Enlaces resolubles.
- Markdown y LaTeX bien delimitados.
- Gramática o esquemas verificables cuando existan.
- Suite de conformidad actualizada cuando corresponda.
- Barrera mecánica de MUD-EDIT-002 y del tratamiento de preguntas mediante `python gobierno/validate_spec_editorial.py`; MUD-EDIT-003 conserva además su revisión semántica por superficies afectadas.
- Aplicación de MUD-EDIT-004 y coherencia entre capítulo 09 + HIR nominal cuando el cambio afecte resolución de nombres.
