---
id: D-073
title: "`as Thing` explícito válido pero redundante"
status: vigente
date: 2026-08-02
supersedes: []
superseded-by: []
questions: []
affects:
  - "especialización de thing, diagnósticos, resolución nominal, IR semántico, formateadores y acciones de código"
---
# ADR-073 — `as Thing` explícito válido pero redundante

- Modifica: [[ADR-018-as-declara-is-consulta|D-018]] y [[ADR-068-thing-universal-y-nombre-intrinseco|D-068]]
- Ajustada a la frontera de fases de [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].

## Contexto

D-068 introdujo `Thing` como raíz abstracta incorporada y rechazó escribirla en una cláusula `as`. Sin embargo, `thing Place as Thing {}` expresa una relación que ya es necesariamente verdadera y no introduce ambigüedad, estado ni una segunda ruta semántica.

Rechazar una afirmación correcta y fácilmente reparable resulta desproporcionado, en especial para una persona que está haciendo explícita la jerarquía mientras aprende el lenguaje.

## Decisión

`Thing` puede aparecer explícitamente como antecesora en una cláusula `as`:

```mud
thing Place as Thing {}
```

La declaración es válida y tiene exactamente la misma semántica efectiva que:

```mud
thing Place {}
```

El compilador emite un diagnóstico no bloqueante de redundancia y ofrece una corrección automática que elimina `as Thing`. El diagnóstico debe explicar que toda `thing` ya alcanza la raíz incorporada.

La CST y el AST superficial conservan la escritura explícita para permitir round-trip, procedencia y acciones de código. La resolución normaliza `Thing` como la raíz efectiva ya garantizada: no crea una segunda arista, no altera la linealización y no la publica como una antecesora declarada distinta en el grafo semántico.

Si `Thing` aparece junto a otras antecesoras, se elimina solo ese elemento al aplicar la corrección:

```mud
thing Port as Place, Thing {}
```

se sugiere como:

```mud
thing Port as Place {}
```

Las demás restricciones permanecen: `Thing` no puede declararse, redefinirse, activarse, crearse ni destruirse.

## Consecuencias

- Una redundancia pedagógicamente comprensible no impide compilar.
- El modelo semántico continúa teniendo una única raíz incorporada.
- La simplificación se aplica mediante una acción de código explícita, no silenciosamente.
- Linters y LSP pueden señalar la redundancia sin presentarla como error de tipos o nombres.

## Verificación

1. `thing Place {}` y `thing Place as Thing {}` producen el mismo grafo efectivo.
2. La segunda forma produce un diagnóstico no bloqueante y una corrección que elimina `as Thing`.
3. La CST y el AST superficial de la segunda forma conservan `Thing` con su procedencia.
4. `thing Port as Place, Thing {}` se simplifica a `thing Port as Place {}` sin alterar `Place`.
5. La normalización no crea aristas duplicadas ni cambia el resultado de `is`.
6. Se mantiene el rechazo de declarar, crear, destruir o activar `Thing`.
