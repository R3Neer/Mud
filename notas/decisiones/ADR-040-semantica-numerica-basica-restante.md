---
id: D-040
title: "Semántica numérica básica restante"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-001"
  - "Q-019"
affects:
  - "futuro `06-lexico.md`, futuro `10-sistema-de-tipos.md`, futuro `17-dominios-e-intervalos.md`"
---
# ADR-040 — Semántica numérica básica restante

- Amplía: D-028, D-030, D-034
- Modificada por: [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]]
- Preguntas relacionadas: Q-001, Q-019
- Documentos afectados: futuro `06-lexico.md`, futuro `10-sistema-de-tipos.md`, futuro `17-dominios-e-intervalos.md`

## Decisión

### Ampliaciones exactas

Se admiten las ampliaciones implícitas:

$$
\mathsf{Nat}
\longrightarrow
\mathsf{Int}
\longrightarrow
\mathsf{Num}
$$

No se extienden a `Rum` ni a `Money`. Una operación mixta usa la representación exacta común menos ampliada. Los estrechamientos requieren `to`.

### `Nat`

Una operación aritmética pura que produciría un entero negativo bajo representación `Nat` satura en cero antes de comprobar el dominio declarado.

Esta saturación no se aplica a `to Nat`: D-030 exige redondear y después validar, sin saturación correctiva.

D-060 distingue de esta operación pura los efectos `+=` y `-=`. Estos producen deltas enteros firmados, se suman antes de saturar y solo entonces forman el siguiente valor `Nat`. Por tanto, no pueden expandirse a una asignación que aplique la resta saturada por separado.

### `Money`

`Money` usa aritmética decimal exacta con escala de dos cifras decimales. El contexto aporta el tipo de sus literales.

Cuando una operación o conversión necesita reducir escala, se aplica la política global de empates al par fijada por D-034. Las reglas de overflow, división y combinación con magnitudes permanecen en Q-019.

### Separadores numéricos

`_` puede agrupar cifras para legibilidad, incluidas formas exactas y `Rum`:

```mud
1_000
r1_000
```

No altera el valor. La gramática exacta de posiciones admitidas y diagnósticos pertenece a Q-001; los ejemplos canónicos agrupan de tres en tres.

### Intervalos tipados

La forma nominal de tipo de intervalo es:

```text
Nat Interval
Int Interval
Num Interval
Rum Interval
Money Interval
```

Los valores de intervalo se normalizan por el conjunto que denotan. D-029 gobierna límites y D-034 prohíbe enumerar intervalos `Rum`.

## Consecuencias

- La inferencia exacta no autoriza mezcla aproximada.
- Saturación de `Nat` y validación de dominio son fases distintas.
- `Money` deja de depender de sufijos léxicos.
- El IR debe preservar valor, no separadores escritos.

## Verificación futura

1. Cadena de ampliación exacta.
2. Rechazo de mezcla implícita con `Rum` y `Money`.
3. Saturación de la aritmética pura de `Nat`, consolidación previa de deltas aditivos y no saturación de `to Nat`.
4. Escala y redondeo de `Money`.
5. Separadores válidos e inválidos.
6. Normalización de tipos de intervalo.
