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

Decisiones relacionadas: [[POLITICA-DE-DECISIONES|Política de decisiones de MUD]].

## Propósito

Una pregunta identifica una incertidumbre concreta que puede impedir completar la especificación, una decisión o una prueba de conformidad. No sustituye a una decisión ni conserva indefinidamente como «abierto» un problema ya resuelto.

## Autoridad

Las preguntas se registran en `notas/preguntas/`. No definen semántica por sí mismas. Una respuesta solo pasa a ser una regla de MUD mediante una decisión aceptada conforme a [[POLITICA-DE-DECISIONES]] y su promoción a `especificacion/` conforme a [[CICLO-DOCUMENTAL]].

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

## Estado de resolución

El campo `resolved` es la única fuente de verdad del estado de una pregunta:

- `resolved: false` (`[ ]`): abierta; no existe una respuesta aceptada suficiente.
- `resolved:` (`[-]`): parcialmente decidida; el archivo enumera de forma exacta qué falta.
- `resolved: true` (`[x]`): cerrada; no queda ninguna incertidumbre dentro de su alcance.

Las preguntas abiertas y parcialmente decididas son activas. Si una pregunta se
cierra porque fue descartada, la sección `Resolución` explica el motivo. Si fue
sustituida, `superseded-by` enlaza las preguntas que cubren ahora su alcance.

## Contenido mínimo

Cada archivo usa:

```yaml
---
id: Q-NNN
title:
priority: P0
opened: YYYY-MM-DD
resolved: false
closed:
decisions: []
affects: []
superseded-by: []
---
```

La prioridad es `P0`, `P1` o `P2` y determina la sección del índice activo; no forma parte de la identidad estable de la pregunta.

`opened` contiene en formato `YYYY-MM-DD` la fecha de creación del archivo
estable de la pregunta y no cambia
durante su ciclo de vida. En preguntas migradas desde un registro anterior,
`closed` puede ser anterior a `opened` porque documenta el cierre de la pregunta,
no la creación posterior de su archivo individual.

`closed` queda vacío mientras la pregunta esté activa. Cuando pasa a un estado
inactivo contiene la fecha de cierre en formato `YYYY-MM-DD`. Los campos
`resolved` y `closed` deben actualizarse en el mismo cambio.

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

### Criterios y evidencia de cierre

Los criterios de cierre que se usen para declarar una pregunta resuelta llevan
identificadores locales `C1`, `C2`, ... y describen condiciones comprobables, no
la mera existencia de una decisión enlazada. Una pregunta puede conservar texto
explicativo adicional, pero el conjunto de criterios identificados constituye la
lista que debe quedar satisfecha para cerrarla.

Una pregunta `resolved: true` contiene además `## Evidencia de cierre`. Por cada
criterio existe exactamente una entrada con el mismo identificador que cita la
evidencia concreta: decisiones, reglas normativas, artefactos mecánicos, casos de
conformidad o un descarte explícito. El validador comprueba la correspondencia
estructural entre criterios y evidencia; la revisión semántica humana continúa
siendo responsable de comprobar que esa evidencia demuestra realmente el
criterio.

Las preguntas históricas cerradas se migran a esta estructura cuando se adopta
esta política; una evidencia generada durante la migración no exime de revisar su
suficiencia cuando el alcance vuelva a tocarse.

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

1. Todos sus criterios `C1`, `C2`, ... tienen evidencia identificada y la revisión semántica confirma que esa evidencia responde el criterio.
2. El conjunto de criterios cubre todo el alcance de la pregunta; un ADR enlazado por sí solo no constituye cierre.
3. Se actualizan los documentos normativos y técnicos afectados.
4. Se retira de `notas/preguntas/README.md`.
5. Se retira del frontmatter `questions` y de los callouts abiertos de la especificación.
6. Su archivo conserva la respuesta, la fecha de cierre, los criterios, la evidencia y los enlaces de procedencia.

Cerrar no elimina ni recicla el archivo. Las referencias históricas pueden seguir enlazándolo, pero no deben describirlo como pendiente.

## Comprobaciones editoriales

Antes de publicar una unidad se verifica:

- que todo identificador incluido en `questions` corresponda a una pregunta activa;
- que toda advertencia normativa sobre una cuestión pendiente enlace una pregunta activa;
- que una pregunta cerrada no permanezca en el índice activo;
- que `opened` contenga una fecha válida y que `closed` solo esté vacío en
  preguntas activas según `resolved`;
- que las decisiones que abren, responden o sustituyen preguntas mantengan enlaces recíprocos;
- que no existan estados parciales sin una enumeración explícita de lo pendiente.
- que toda pregunta cerrada tenga criterios `C1`, `C2`, ... y una evidencia exactamente correspondiente a cada criterio;
- que ninguna entrada de evidencia invoque un criterio inexistente;
- que la revisión de cierre no confunda un enlace a ADR con evidencia suficiente por sí misma.

El índice activo se regenera desde los metadatos y después se valida desde la
raíz:

```powershell
python tooling/questions/validate_questions.py generate
python tooling/questions/validate_questions.py
```

## Relación con Git

La apertura, división, sustitución o cierre de una pregunta forma parte del mismo commit atómico que la decisión o cambio documental que la provoca, salvo que la pregunta se descubra durante una auditoría independiente.
