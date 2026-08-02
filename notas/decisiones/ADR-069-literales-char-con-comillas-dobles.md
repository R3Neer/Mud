---
id: D-069
title: "Literales `Char` con comillas dobles"
status: vigente
date: 2026-08-02
supersedes: []
superseded-by: []
questions:
  - "Q-047"
affects:
  - "léxico, elaboración de literales, Char, Text, predeterminados y resaltado sintáctico"
---
# ADR-069 — Literales `Char` con comillas dobles

- Modifica: [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|D-017]], [[notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal|D-032]], [[notas/decisiones/ADR-050-comentarios-terminadores-y-separadores-numericos|D-050]] y [[notas/decisiones/ADR-056-char-texto-y-orden-unicode|D-056]]
- Pregunta relacionada: [[notas/preguntas/Q-047-seleccion-de-predeterminados-por-tipo|Q-047]]
- Documentos afectados: léxico, elaboración de literales, `Char`, `Text`, predeterminados y resaltado sintáctico

## Contexto

Separar `Char` con comillas simples y `Text` con comillas dobles importa una convención de lenguajes técnicos que no aporta una diferencia visual evidente a la audiencia de MUD. El tipo esperado ya resuelve otras formas contextuales y puede distinguir un texto de un único escalar sin introducir una segunda puntuación.

## Decisión

Los literales ordinarios de `Char` y `Text` comienzan con comillas dobles. Una misma forma se elabora así:

- Su tipo preferido y predeterminado es `Text`.
- Cuando el contexto exige `Char`, puede elaborarse como `Char` si, después de interpretar escapes, contiene exactamente un valor escalar Unicode.
- La forma `Char` exige comilla final explícita y no admite interpolaciones de valor o ancla.
- La forma multilínea siempre es `Text`.
- Sin tipo esperado, `value := "a"` infiere `Text`.
- Un literal vacío o con varios escalares es inválido cuando se exige `Char`.

```mud
letter: Char = "a"
newline: Char = "\n"
face: Char = "\u{1F642}"
word: Text = "a"
```

En una comparación u otra expresión bidireccional, el otro operando puede aportar el tipo esperado:

```mud
pressedKey == "x"
```

Las comillas simples dejan de delimitar literales y no forman parte del léxico de MUD. Un apóstrofo continúa siendo un carácter ordinario dentro de un literal con comillas dobles.

El predeterminado de `Char` se escribe `"\u{0}"` en contexto `Char`. La escritura no cambia el dominio Unicode, el orden natural ni la distinción semántica entre `Char` y `Text`.

El resaltado sintáctico clasifica las formas con comillas dobles como texto porque la elección `Char`/`Text` requiere información de tipos. La categoría interna histórica de carácter puede conservarse para compatibilidad de temas, pero el tokenizador de MUD no la emite para comillas simples.

## Consecuencias

- Solo existe una clase de comillas para contenido textual en MUD.
- Los literales de un escalar siguen siendo `Text` cuando falta un contexto `Char`.
- El parser produce una forma textual común y la elaboración estática decide si puede convertirse en literal `Char`.
- Código anterior con comillas simples deja de ser válido y debe migrarse a comillas dobles.

## Verificación

1. `"a"`, `"ñ"`, `"\n"` y `"\u{1F642}"` en contexto `Char`.
2. Inferencia de `Text` para `value := "a"`.
3. Rechazo de `""`, `"ab"`, texto multilínea e interpolaciones en contexto `Char`.
4. Resolución de `charValue == "x"` como comparación de `Char`.
5. Rechazo léxico de las formas entre comillas simples.
6. Predeterminado `"\u{0}"` de `Char`.
7. Resaltado con comillas dobles y ausencia de resaltado `character` para comillas simples en MUD.
