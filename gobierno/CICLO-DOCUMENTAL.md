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

La formalización se aprende de manera didáctica, pero la especificación publicada debe tener apariencia y precisión profesionales. Este proceso impide que ejercicios, ayudas personales o razonamientos provisionales se filtren dentro de la norma.

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
- Cuestiones abiertas explícitas.
- Referencias a decisiones.
- Criterios de conformidad.

No puede contener:

- Ejercicios dirigidos al autor.
- Pistas.
- Seguimiento del aprendizaje.
- Conversación.
- Explicaciones que presupongan el historial personal del proyecto.
- Soluciones incompletas presentadas como norma.
- Simplificaciones didácticas no etiquetadas.

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

## Promoción de material

El aprendizaje no se copia mecánicamente a la especificación. La promoción sigue estos pasos:

1. El autor completa y revisa el ejercicio.
2. Se identifican las decisiones semánticas que contiene.
3. Las cuestiones abiertas se resuelven o se registran.
4. Se redacta de nuevo en estilo normativo.
5. Se unifica la notación con [[especificacion/03-notacion]].
6. Se añaden identificadores normativos.
7. Se comprueban ejemplos, contraejemplos e interacciones.
8. Se verifican enlaces, dependencias y procedencia.
9. Se elimina cualquier andamiaje didáctico de la superficie normativa.
10. El autor revisa el texto publicable.
11. Se cambia el estado y se crea un commit atómico.

## Pasada de publicación

Cuando el autor indique que ha terminado de revisar o completar una parte, Codex realizará:

### Revisión semántica

- Correspondencia entre prosa, fórmulas y ejemplos.
- Ausencia de casos sin definir.
- Compatibilidad con capítulos vigentes.
- Distinción entre norma, propuesta y cuestión abierta.
- Búsqueda de contraejemplos.

### Revisión formal

- Símbolos definidos antes de usarse.
- Juicios y reglas bien formados.
- Hipótesis explícitas.
- Cuantificadores y dominios inequívocos.
- Nombres consistentes.

### Revisión editorial

- Eliminación de ejercicios, pistas y referencias al proceso personal.
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

## Conservación del material didáctico

La publicación no obliga a borrar `aprendizaje/`. El material puede conservarse como cuaderno de formación y procedencia. Si queda obsoleto, se marca como tal o se mueve a un archivo; no se confunde con la norma.
