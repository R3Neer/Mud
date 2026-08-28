---
title: Ciclo documental de MUD
aliases:
  - Promoción a normativa
tags:
  - mud/gobierno
  - mud/especificacion
status: vigente
---

# Ciclo documental de MUD

Gestión de cuestiones abiertas: [[POLITICA-DE-PREGUNTAS|Política de preguntas de MUD]].

## Propósito

La formalización se aprende de manera didáctica, pero la especificación publicada debe tener apariencia y precisión profesionales. Este proceso impide que ejercicios, ayudas personales, razonamientos provisionales o historia decisional se filtren dentro de la exposición de la norma vigente.

## Dos superficies

### Superficie de aprendizaje

Ubicación: `aprendizaje/`.

Puede contener:

- Explicaciones graduales.
- Analogías.
- Ejercicios.
- Huecos para completar.
- Pistas.
- Soluciones comentadas.
- Errores frecuentes.
- Reflexiones del autor.
- Versiones deliberadamente simplificadas.

Nada de esta superficie es normativo.

### Superficie normativa

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

- Ejercicios dirigidos al autor.
- Pistas.
- Seguimiento del aprendizaje.
- Conversación.
- Explicaciones que presupongan el historial personal del proyecto.
- Historia de introducción, modificación, sustitución o retirada de reglas como parte de la exposición normativa.
- Secciones aditivas que corrijan una regla anterior en vez de reescribir su ubicación canónica.
- Soluciones incompletas presentadas como norma.
- Simplificaciones didácticas no etiquetadas.

La separación entre estado vigente, decisiones y cuestiones abiertas se rige por MUD-EDIT-002 y MUD-EDIT-003 de [[especificacion/00-convenciones-editoriales]].

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
- **En revisión**: el autor la ha revisado y se ejecuta la pasada de publicación.
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

## Promoción de material

El aprendizaje no se copia mecánicamente a la especificación. La promoción sigue estos pasos:

1. El autor completa y revisa el ejercicio.
2. Se identifican las decisiones semánticas que contiene.
3. Las cuestiones abiertas se resuelven o se registran.
4. Se redacta de nuevo en estilo normativo.
5. Se unifica la notación con [[especificacion/03-notacion]].
6. Se añaden identificadores normativos.
7. Se comprueban ejemplos, contraejemplos e interacciones.
8. Se verifican enlaces, dependencias y metadatos de trazabilidad.
9. Se elimina del cuerpo cualquier andamiaje didáctico, historia decisional o procedencia que no forme parte del estado vigente.
10. Se comprueba la integración en todas las superficies ya desarrolladas afectadas.
11. El autor revisa el texto publicable.
12. Se cambia el estado y se crea un commit atómico.

## Pasada de publicación

Cuando el autor indique que ha terminado de revisar o completar una parte, Codex realizará:

### Revisión semántica

- Correspondencia entre prosa, fórmulas y ejemplos.
- Ausencia de casos sin definir.
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

- Eliminación de ejercicios, pistas y referencias al proceso personal.
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
- Validadores editoriales específicos de MUD-EDIT-002 y MUD-EDIT-003 cuando existan.
- Aplicación de MUD-EDIT-004 y coherencia entre capítulo 09 + HIR nominal cuando el cambio afecte resolución de nombres.

## Conservación del material didáctico

La publicación no obliga a borrar `aprendizaje/`. El material puede conservarse como cuaderno de formación y procedencia. Si queda obsoleto, se marca como tal o se mueve a un archivo; no se confunde con la norma.
