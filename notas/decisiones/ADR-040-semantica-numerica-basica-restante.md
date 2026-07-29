# ADR-040 — Semántica numérica básica restante

- Estado: Vigente con fallos aritméticos pendientes
- Fecha: 2026-07-28
- Amplía: D-028, D-030, D-034
- Modificada por: [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]]
- Preguntas relacionadas: Q-001, Q-019
- Documentos afectados: futuro `06-lexico.md`, futuro `10-sistema-de-tipos.md`, futuro `17-dominios-e-intervalos.md`

## Decisión

### Ampliaciones exactas

Se admiten las ampliaciones implícitas:

$$
\mathsf{Natural}
\longrightarrow
\mathsf{Integer}
\longrightarrow
\mathsf{Number}
$$

No se extienden a `Rumber` ni a `Money`. Una operación mixta usa la representación exacta común menos ampliada. Los estrechamientos requieren `to`.

### `Natural`

Una operación aritmética pura que produciría un entero negativo bajo representación `Natural` satura en cero antes de comprobar el dominio declarado.

Esta saturación no se aplica a `to Natural`: D-030 exige redondear y después validar, sin saturación correctiva.

D-060 distingue de esta operación pura los efectos `+=` y `-=`. Estos producen deltas enteros firmados, se suman antes de saturar y solo entonces forman el siguiente valor `Natural`. Por tanto, no pueden expandirse a una asignación que aplique la resta saturada por separado.

### `Money`

`Money` usa aritmética decimal exacta con escala de dos cifras decimales. El contexto aporta el tipo de sus literales.

Cuando una operación o conversión necesita reducir escala, se aplica la política global de empates al par fijada por D-034. Las reglas de overflow, división y combinación con magnitudes permanecen en Q-019.

### Separadores numéricos

`_` puede agrupar cifras para legibilidad, incluidas formas exactas y `Rumber`:

```mud
1_000
r1_000
```

No altera el valor. La gramática exacta de posiciones admitidas y diagnósticos pertenece a Q-001; los ejemplos canónicos agrupan de tres en tres.

### Intervalos tipados

La forma nominal de tipo de intervalo es:

```text
Natural Interval
Integer Interval
Number Interval
Rumber Interval
Money Interval
```

Los valores de intervalo se normalizan por el conjunto que denotan. D-029 gobierna límites y D-034 prohíbe enumerar intervalos `Rumber`.

## Consecuencias

- La inferencia exacta no autoriza mezcla aproximada.
- Saturación de `Natural` y validación de dominio son fases distintas.
- `Money` deja de depender de sufijos léxicos.
- El IR debe preservar valor, no separadores escritos.

## Verificación futura

1. Cadena de ampliación exacta.
2. Rechazo de mezcla implícita con `Rumber` y `Money`.
3. Saturación de la aritmética pura de `Natural`, consolidación previa de deltas aditivos y no saturación de `to Natural`.
4. Escala y redondeo de `Money`.
5. Separadores válidos e inválidos.
6. Normalización de tipos de intervalo.
