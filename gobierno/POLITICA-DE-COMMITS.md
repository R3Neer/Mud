---
title: Política de commits de MUD
aliases:
  - Política Git
tags:
  - mud/gobierno
  - mud/git
status: vigente
---

# Política de commits de MUD

## Objetivo

El historial Git debe permitir reconstruir la evolución conceptual, normativa y técnica de MUD. Un commit representa una unidad coherente que puede entenderse y revertirse de manera independiente.

## Responsabilidad

Codex se encargará de preparar y crear los commits del repositorio.

El autor no necesita indicar expresamente “haz commit” después de cada tarea. Cuando una modificación solicitada:

1. Esté completa dentro de su alcance.
2. Haya sido revisada en proporción a su riesgo.
3. No contenga cambios ajenos.
4. Mantenga el repositorio en un estado coherente.

Codex debe crear el commit correspondiente antes de cerrar la tarea.

No se hará commit cuando:

- El autor pida explícitamente dejarlo sin confirmar.
- El trabajo esté incompleto o no pueda validarse.
- Exista una cuestión bloqueante que cambie sustancialmente el resultado.
- El diff incluya trabajo ajeno que no pueda aislarse con seguridad.

En esos casos, Codex informará de qué queda sin confirmar y por qué.

## Atomicidad

Cada commit debe tener una única razón principal para existir.

Un commit puede modificar varios archivos cuando todos forman parte de la misma decisión, por ejemplo:

- Norma, ejemplo y prueba de conformidad de una característica.
- Decisión y capítulos afectados.
- Política y reglas persistentes que la aplican.

No se mezclarán:

- Cambios normativos no relacionados.
- Reformateo masivo con cambios semánticos.
- Trabajo del autor ajeno a la tarea.
- Archivos efímeros ordinarios, builds, logs, caches, volcados o estado local de Obsidian.

Un documento intencionadamente temporal puede permanecer versionado únicamente bajo [[POLITICA-DE-ARCHIVOS-TEMPORALES|la política de archivos temporales]]. Su temporalidad no lo exime de la atomicidad del commit ni convierte residuos efímeros en material versionable.

## Formato del mensaje

Primera línea:

```text
tipo(ámbito): resumen imperativo
```

Tipos:

| Tipo | Uso |
| --- | --- |
| `spec` | Norma, gramática, semántica o conformidad |
| `decision` | ADR o cambio explícito de dirección |
| `docs` | Documentación informativa sin cambio normativo |
| `govern` | Procesos editoriales, Git o gobierno |
| `fix` | Corrección de un error |
| `refactor` | Reorganización sin cambio de significado |
| `test` | Suite o casos de conformidad |
| `chore` | Infraestructura y mantenimiento |

Ámbitos frecuentes:

```text
language
notation
lexicon
grammar
types
actions
waves
random
reachability
git
editorial
```

Ejemplos:

```text
spec(types): define nominal equality for aliases
decision(language): require full MUD 1.0 specification first
govern(git): establish atomic commit policy
fix(waves): clarify binding lifetime after destruction
```

El resumen:

- Se escribe en presente imperativo.
- No termina en punto.
- Describe el resultado, no la actividad genérica.
- Evita mensajes como `changes`, `updates` o `work`.

## Cuerpo del commit

Se añadirá cuando el motivo no sea evidente. Estructura recomendada:

```text
Context:
- ...

Changes:
- ...

Validation:
- ...

Open questions:
- ...
```

Para cambios normativos se incluirán, cuando proceda:

- Reglas o anclas afectadas.
- Decisión relacionada.
- Compatibilidad.
- Preguntas cerradas o creadas.
- Pruebas de conformidad.

## Gate de archivos temporales

Antes de cualquier commit se ejecuta:

```powershell
python gobierno/validate_temporaries.py
```

El inventario impreso debe revisarse completo. Si la condición `temporary-delete-when` de algún documento ya se cumple, ese documento debe eliminarse antes de cerrar el commit, salvo que el propio cambio modifique explícitamente su ciclo de vida. Una fecha `temporary-delete-after` vencida bloquea mecánicamente el commit.

## Proceso previo

Antes de crear un commit, Codex debe:

1. Leer las instrucciones aplicables.
2. Revisar `git status`.
3. Identificar archivos previos o ajenos.
4. Inspeccionar el diff.
5. Ejecutar `python gobierno/validate_temporaries.py` y revisar semánticamente todo su inventario.
6. Ejecutar las demás validaciones disponibles.
7. Añadir únicamente los archivos de la unidad atómica.
8. Revisar el diff staged.
9. Crear el commit.
10. Confirmar que el estado posterior es el esperado.

## Rama principal

La rama principal local se denomina `main`.

Mientras solo exista trabajo local y un único flujo de autoría, pueden crearse commits directamente en `main`. Cuando aparezcan cambios experimentales, implementación paralela o colaboración externa, se adoptarán ramas temáticas.

## Reescritura de historial

Codex no debe:

- Ejecutar `git reset --hard`.
- Forzar un push.
- Reescribir commits publicados.
- Hacer `commit --amend` sobre trabajo que pueda pertenecer a otra persona.

Una corrección ordinaria se registra en un commit nuevo. La limpieza de historia antes de publicar se realizará solo por petición explícita del autor y después de comprobar los límites exactos.

## Publicación remota

Esta política autoriza commits locales, no:

- Crear repositorios remotos.
- Hacer push.
- Abrir pull requests.
- Publicar versiones.

Esas acciones requieren una petición explícita.

## Relación con los cambios semánticos futuros

Cuando el repositorio contenga modelos `.mud`, los commits que cambien semántica deberán añadir en el cuerpo operaciones como:

```text
Operations:
- CREATE action::warfare.Recruit
- UPDATE rule::warfare.CanRecruit
- RETIRE construct::warfare.LegacyArmy
```

Una consulta `READ` pura no produce commit.
