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

Una decisión registra una elección aceptada que condiciona el lenguaje, su
arquitectura, el producto o el proceso editorial. Explica el contexto y la
justificación de la elección, pero no sustituye su promoción a
`especificacion/` cuando afecta a la norma de MUD.

## Autoridad

Cada decisión dispone de un archivo estable:

```text
notas/decisiones/ADR-NNN-titulo-breve.md
```

El archivo es la fuente de verdad sobre la identidad, estado, procedencia y
relaciones de la decisión. `notas/decisiones/README.md` es un índice generado:
puede reconstruirse y nunca se edita manualmente.

La especificación prevalece como norma del lenguaje. Un ADR conserva el porqué
de una regla y sirve de autoridad transitoria mientras esa regla aún no haya
sido promovida.

## Identidad

- El identificador `D-NNN` es único y no se reutiliza.
- El archivo correspondiente usa el mismo número con el prefijo `ADR-`.
- El título puede precisarse sin cambiar el identificador.
- Los números omitidos se declaran en
  `notas/decisiones/identificadores-reservados.txt`.
- Una decisión nueva recibe el siguiente identificador libre; no rellena un
  hueco histórico.

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
- `affects`: documentos, capítulos o dominios que deben incorporar o comprobar
  la decisión.

`supersedes` no se usa para una mera ampliación, precisión o modificación
parcial. Esas relaciones se explican en el ADR y, cuando resulte útil, mediante
enlaces recíprocos.

## Estados

Estados permitidos:

- `propuesta`: todavía no aceptada.
- `vigente`: elección aceptada.
- `sustituida`: otra decisión reemplaza todo su alcance.
- `retirada`: dejó de aplicarse sin ser reemplazada por otra regla.
- `rechazada`: alternativa evaluada y no aceptada.

Una decisión `sustituida` debe declarar `superseded-by`. Una decisión que
declare `supersedes` debe aparecer recíprocamente en `superseded-by` de cada
decisión sustituida.

Los matices como «vigente en su núcleo» o «esquema exacto abierto» se explican
en el cuerpo y mediante preguntas activas; no crean estados adicionales.

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

Una decisión semántica debe ser suficientemente precisa para reconocer qué se
eligió, pero su redacción normativa final pertenece a `especificacion/`.

## Apertura y aceptación

Antes de crear una decisión:

1. Se comprueba que no exista otra con el mismo alcance.
2. Se identifican las preguntas que responde.
3. Se describen alternativas y consecuencias relevantes.
4. Se asigna un identificador nuevo.
5. Se actualizan las preguntas y documentos afectados en el mismo cambio.

Una propuesta pasa a `vigente` cuando el autor acepta la elección. Si todavía
quedan incertidumbres independientes, se conservan como preguntas abiertas.

## Sustitución y retirada

Los ADR no se eliminan al dejar de estar vigentes. La sustitución:

1. crea o acepta la nueva decisión;
2. actualiza `supersedes` y `superseded-by` de forma recíproca;
3. cambia el estado anterior a `sustituida`;
4. actualiza especificación, preguntas y referencias afectadas.

La retirada usa `retirada`, explica el motivo y conserva el archivo como
trazabilidad.

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

La promoción a norma sigue [[CICLO-DOCUMENTAL]]. La creación, aceptación,
sustitución o retirada de una decisión forma parte del mismo commit atómico que
sus preguntas y documentos afectados, salvo que una auditoría independiente
descubra una inconsistencia preexistente.
