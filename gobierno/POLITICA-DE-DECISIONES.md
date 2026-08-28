---
title: Política de decisiones de MUD
aliases:
  - Ciclo de decisiones
tags:
  - mud/gobierno
  - mud/decisiones
status: vigente
---

# Política de decisiones de MUD

## Propósito

Una decisión registra una elección aceptada que condiciona el lenguaje, su arquitectura, el producto o el proceso editorial. Explica el contexto y la justificación de la elección, pero no sustituye su integración en las superficies normativas ya desarrolladas que entren en su alcance.

Cuando la ubicación canónica de una regla todavía no exista como superficie desarrollada de `especificacion/`, un ADR vigente puede conservar autoridad transitoria hasta que esa superficie se redacte. Esta situación no autoriza a mantener contradicciones en documentos ya existentes ni obliga a crear un capítulo provisional en una ubicación impropia.

## Autoridad

Cada decisión dispone de un archivo estable:

```text
notas/decisiones/ADR-NNN-titulo-breve.md
```

El archivo es la fuente de verdad sobre la identidad, estado, procedencia y relaciones de la decisión. `notas/decisiones/README.md` es un índice generado: puede reconstruirse y nunca se edita manualmente.

La especificación prevalece como norma del lenguaje dentro de las superficies ya formalizadas. Un ADR conserva el porqué de una regla y sirve de autoridad transitoria mientras su ubicación normativa canónica aún no haya sido desarrollada.

La relación de un documento de `especificacion/` con las decisiones que lo sustentan se registra mediante su frontmatter `decisions:`. La historia decisional no se conserva en el cuerpo normativo, conforme a MUD-EDIT-002.

## Identidad

- El identificador `D-NNN` es único y no se reutiliza.
- El archivo correspondiente usa el mismo número con el prefijo `ADR-`.
- El título puede precisarse sin cambiar el identificador.
- Los números omitidos se declaran en `notas/decisiones/identificadores-reservados.txt`.
- Una decisión nueva recibe el siguiente identificador libre; no rellena un hueco histórico.

## Metadatos obligatorios

Cada ADR comienza con:

```yaml
---
id: D-NNN
title: "Título"
status: propuesta
date: YYYY-MM-DD
supersedes: []
superseded-by: []
questions: []
affects: []
---
```

Significado:

- `id`: identidad estable.
- `title`: título sin el prefijo `ADR-NNN`.
- `status`: estado del ADR.
- `date`: fecha de adopción o apertura.
- `supersedes`: decisiones sustituidas por completo por esta.
- `superseded-by`: decisiones que sustituyen por completo esta.
- `questions`: identificadores `Q-NNN` relacionados.
- `affects`: documentos, capítulos, artefactos o dominios que deben incorporar o comprobar la decisión cuando esas superficies existan.

`supersedes` no se usa para una mera ampliación, precisión o modificación parcial. Esas relaciones se explican en el ADR y, cuando resulte útil, mediante enlaces recíprocos.

### Vigencia efectiva del cuerpo

Un ADR con `status: vigente` debe poder leerse literalmente como descripción de la decisión actual dentro de su alcance. Cuando una decisión posterior modifica solo parte de un ADR vigente, el mismo cambio editorial debe retirar o reescribir en el ADR anterior las reglas que hayan dejado de aplicarse y conservar una nota de procedencia hacia la decisión modificadora. El historial de la redacción anterior pertenece a Git y no se mantiene como semántica afirmativa dentro de un ADR vigente.

Cuando una decisión posterior sustituye todo el alcance, no se reescribe el ADR anterior como si siempre hubiera dicho otra cosa: se aplica `status: sustituida` con `superseded-by` recíproco. `retirada` se reserva para alcance que deja de aplicarse sin una regla sustituta.

## Estados

Estados permitidos:

- `propuesta`: todavía no aceptada.
- `vigente`: elección aceptada.
- `sustituida`: otra decisión reemplaza todo su alcance.
- `retirada`: dejó de aplicarse sin ser reemplazada por otra regla.
- `rechazada`: alternativa evaluada y no aceptada.

Una decisión `sustituida` debe declarar `superseded-by`. Una decisión que declare `supersedes` debe aparecer recíprocamente en `superseded-by` de cada decisión sustituida.

Los matices como «vigente en su núcleo» o «esquema exacto abierto» se explican en el cuerpo y mediante preguntas activas; no crean estados adicionales.

## Contenido

Un ADR incluye, cuando proceda:

```markdown
## Contexto
## Decisión
## Alternativas
## Consecuencias
## Ejemplos
## Verificación
```

Una decisión semántica debe ser suficientemente precisa para reconocer qué se eligió. Su redacción normativa final pertenece a la superficie canónica de `especificacion/` cuando esa superficie exista.

## Integración en la especificación

La integración sigue MUD-EDIT-003 de [[especificacion/00-convenciones-editoriales]].

Para cada decisión vigente:

1. Se identifican las superficies normativas ya desarrolladas cuya responsabilidad declarada cubre su alcance.
2. Esas superficies deben expresar literalmente el estado resultante de la decisión y no conservar la formulación sustituida.
3. La integración no se satisface añadiendo una sección posterior que explique que una decisión cambia el contenido anterior.
4. Si la superficie canónica todavía no existe, la regla se clasifica como semántica aceptada pendiente de formalización; no se fuerza dentro de otro capítulo por conveniencia documental.
5. Mientras esté pendiente de formalización, ninguna superficie existente puede contradecirla y los índices o descripciones de capítulos futuros deben permanecer compatibles con ella.
6. Cuando se cree finalmente la superficie canónica, la regla se promueve allí y el ADR conserva contexto y procedencia, no una segunda copia normativa destinada a competir con la especificación.

La integración es por superficie afectada, no una propiedad binaria de la decisión completa: una misma decisión puede estar integrada en gramática y AST y seguir pendiente de formalización en semántica dinámica si el capítulo correspondiente aún no existe.

## Apertura y aceptación

Antes de crear una decisión:

1. Se comprueba que no exista otra con el mismo alcance.
2. Se identifican las preguntas que responde.
3. Se describen alternativas y consecuencias relevantes.
4. Se asigna un identificador nuevo.
5. Se actualizan las preguntas y superficies ya desarrolladas afectadas en el mismo cambio.
6. Se comprueba que los índices o mapas de superficies futuras no queden contradiciendo la decisión.

Una propuesta pasa a `vigente` cuando el autor acepta la elección. Si todavía quedan incertidumbres independientes, se conservan como preguntas abiertas.

## Sustitución y retirada

Los ADR no se eliminan al dejar de estar vigentes. La sustitución:

1. crea o acepta la nueva decisión;
2. actualiza `supersedes` y `superseded-by` de forma recíproca;
3. cambia el estado anterior a `sustituida`;
4. actualiza las superficies desarrolladas, preguntas e índices afectados.

La retirada usa `retirada`, explica el motivo y conserva el archivo como trazabilidad.

## Índice y comprobación mecánica

Desde la raíz:

```powershell
python tooling/decisions/manage_decisions.py generate
python tooling/decisions/manage_decisions.py validate
```

`generate` reconstruye `notas/decisiones/README.md`. `validate` comprueba:

- nombres, identificadores y metadatos obligatorios;
- estados y fechas;
- unicidad y huecos de numeración;
- existencia de preguntas y decisiones enlazadas;
- reciprocidad de sustituciones;
- correspondencia exacta del índice generado;
- ausencia del antiguo registro manual.

## Relación con publicación y Git

La integración en norma sigue [[CICLO-DOCUMENTAL]]. La creación, aceptación, sustitución o retirada de una decisión forma parte del mismo commit atómico que sus preguntas y superficies ya desarrolladas afectadas, salvo que una auditoría independiente descubra una inconsistencia preexistente.
