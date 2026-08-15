---
id: D-082
title: "`cycle` como modificador de dominio de punto"
status: vigente
date: 2026-08-04
supersedes: []
superseded-by: []
questions:
  - "Q-018"
affects:
  - "magnitudes de punto, intervalos, gramática, CST y AST"
---

# ADR-082 — `cycle` como modificador de dominio de punto

- Modifica: [[ADR-029-intervalos-estrellas-y-ciclos|D-029]], [[ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]] y [[ADR-062-literales-canonicos-de-magnitudes-de-punto|D-062]].
- Pregunta relacionada: [[notas/preguntas/Q-018-intervalos-discontinuos|Q-018]].
- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]

## Contexto

La forma `[a..b cycle)` colocaba `cycle` dentro de los delimitadores de un intervalo aunque no determina la inclusión del extremo. Esto mezclaba la notación matemática del dominio con una propiedad exclusiva de las magnitudes de punto y sugería que `cycle` formaba parte de la expresión general de intervalo.

Las cardinalidades de colección no comparten este problema: su forma `[cardinalidad modificadores]` es una especificación especializada cuyos límites son siempre cerrados y naturales.

## Decisión

`cycle` pasa a ser un modificador posterior del dominio completo de una magnitud de punto:

```mud
magnitude TimeOfDay point over Time in [0..86_400) cycle {
}
```

La forma anterior `[a..b cycle)` deja de ser válida.

El modificador continúa siendo exclusivo de `point over`. El intervalo que precede a `cycle` debe ser finito, contiguo, no vacío, cerrado a la izquierda y abierto a la derecha. Su periodo es la diferencia entre el límite superior y el inferior y debe ser estrictamente positivo.

`cycle` modifica la normalización del dominio de punto, no el valor intervalo. Por ello `[a..b)` conserva el mismo AST de intervalo ordinario y la presencia posterior de `cycle` selecciona `CyclicPointDomain` durante la transformación del dominio.

La sintaxis de cardinalidad no cambia:

```mud
players: Player [1..3 unique mut]
```

No se admiten intervalos abiertos ni intervalos anidados como cardinalidad.

## Consecuencias

- Los delimitadores `[` `(` `]` `)` vuelven a describir únicamente la pertenencia de los extremos del intervalo.
- La fuente distingue visualmente el dominio `[a..b)` de su comportamiento `cycle`.
- La gramática puede diagnosticar por separado un dominio cíclico con forma de intervalo inadecuada.
- El AST semántico `OrdinaryPointDomain` / `CyclicPointDomain` no cambia.

## Verificación

1. Aceptación de `in [a..b) cycle` en una magnitud de punto.
2. Rechazo de la forma retirada `in [a..b cycle)`.
3. Rechazo de `cycle` en magnitudes no puntuales.
4. Rechazo de `cycle` tras intervalos cerrados, abiertos a la izquierda, infinitos, vacíos o degenerados.
5. Conservación de las formas de cardinalidad `[1]`, `[1..3]` y `[1..3 mut]`.

## Modificación por D-088

Un dominio cíclico de punto puede alimentar una progresión exacta mediante diferencia compatible. La enumeración cubre un único periodo fundamental y nunca repite el ciclo indefinidamente. El signo y los límites se aplican al intervalo fundamental `[a..b)`.
