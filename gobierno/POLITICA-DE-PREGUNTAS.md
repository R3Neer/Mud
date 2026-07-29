---
title: Política de preguntas de MUD
aliases:
  - Ciclo de preguntas
tags:
  - mud/gobierno
  - mud/preguntas
status: vigente
---

# Política de preguntas de MUD

## Propósito

Una pregunta identifica una incertidumbre concreta que puede impedir completar la especificación, una decisión o una prueba de conformidad. No sustituye a una decisión ni conserva indefinidamente como «abierto» un problema ya resuelto.

## Autoridad

Las preguntas se registran en `notas/preguntas/`. No definen semántica por sí mismas. Una respuesta solo pasa a ser una regla de MUD mediante una decisión aceptada y su promoción a `especificacion/` conforme a [[CICLO-DOCUMENTAL]].

Cada pregunta dispone de un archivo estable:

```text
notas/preguntas/Q-NNN-titulo-breve.md
```

El archivo no se mueve al cambiar de estado. Su ubicación estable evita romper enlaces y conserva la trazabilidad.

`notas/preguntas/README.md` enumera únicamente las preguntas activas.

## Identidad

- El identificador `Q-NNN` es único y no se reutiliza.
- El título puede precisarse sin cambiar el identificador cuando la investigación revele la duda real.
- Si una pregunta contiene incertidumbres independientes, se divide y cada nueva pregunta enlaza su procedencia.
- Una decisión puede resolver varias preguntas y una pregunta puede requerir varias decisiones.

## Estados

Los estados permitidos son:

- `abierta`: no existe una respuesta aceptada suficiente.
- `parcialmente-decidida`: una decisión resolvió parte del problema y el archivo enumera de forma exacta qué falta.
- `cerrada`: no queda ninguna incertidumbre dentro de su alcance y el archivo enlaza la decisión o evidencia que la cerró.
- `descartada`: la pregunta perdió aplicabilidad sin convertirse en regla; debe explicar por qué.
- `sustituida`: otras preguntas cubren ahora su alcance; debe enlazarlas.

Solo `abierta` y `parcialmente-decidida` son estados activos.

## Contenido mínimo

Cada archivo usa:

```yaml
---
id: Q-NNN
title:
status: abierta
priority: P0
opened:
closed:
decisions: []
affects: []
superseded-by: []
---
```

La prioridad es `P0`, `P1` o `P2` y determina la sección del índice activo; no forma parte de la identidad estable de la pregunta.

Y contiene, cuando proceda:

```markdown
# Q-NNN — Título

## Pregunta
## Contexto
## Ya decidido
## Pendiente
## Criterio de cierre
## Resolución
```

Una pregunta parcialmente decidida no repite como pendiente lo ya resuelto. La sección `Pendiente` debe permitir reconocer objetivamente cuándo puede cerrarse.

## Apertura

Antes de crear una pregunta se comprueba que:

1. La incertidumbre no esté ya resuelta por la especificación o una decisión vigente.
2. No sea un duplicado de otra pregunta.
3. Su alcance sea suficientemente pequeño para recibir una respuesta comprobable.
4. Identifique los capítulos, decisiones o pruebas afectados.
5. Distinga alternativas reales cuando ya se conozcan.

La nueva pregunta se añade al índice activo y al frontmatter `questions` de cada capítulo cuyo significado impida cerrar.

## Cierre

Una pregunta se cierra cuando:

1. Una decisión o evidencia identificada responde todo su alcance.
2. Se actualizan los documentos normativos y técnicos afectados.
3. Se retira de `notas/preguntas/README.md`.
4. Se retira del frontmatter `questions` y de los callouts abiertos de la especificación.
5. Su archivo conserva la respuesta, la fecha de cierre y los enlaces de procedencia.

Cerrar no elimina ni recicla el archivo. Las referencias históricas pueden seguir enlazándolo, pero no deben describirlo como pendiente.

## Comprobaciones editoriales

Antes de publicar una unidad se verifica:

- que todo identificador incluido en `questions` corresponda a una pregunta activa;
- que toda advertencia normativa sobre una cuestión pendiente enlace una pregunta activa;
- que una pregunta cerrada no permanezca en el índice activo;
- que las decisiones que abren, responden o sustituyen preguntas mantengan enlaces recíprocos;
- que no existan estados parciales sin una enumeración explícita de lo pendiente.

La comprobación mecánica se ejecuta desde la raíz:

```powershell
python tooling/questions/validate_questions.py
```

## Relación con Git

La apertura, división, sustitución o cierre de una pregunta forma parte del mismo commit atómico que la decisión o cambio documental que la provoca, salvo que la pregunta se descubra durante una auditoría independiente.
