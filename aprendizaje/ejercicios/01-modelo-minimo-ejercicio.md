---
title: Ejercicio 01 — Programa, mundo y store mínimo
tags:
  - mud/aprendizaje
  - mud/ejercicio
status: disponible
depends-on:
  - "[[aprendizaje/unidades/01-modelo-minimo-de-un-mundo]]"
---

# Ejercicio 01 — Programa, mundo y store mínimo

Referencia: [[aprendizaje/unidades/01-modelo-minimo-de-un-mundo]].

> [!note]
> Este es el ejercicio correspondiente al modelo actual. El primer ejercicio realizado y su revisión se conservan en [[aprendizaje/historico/01-modelo-clase-instancia/README|el archivo histórico]]. No es obligatorio repetirlo para conservar el progreso ya demostrado.

## Enunciado

Considera:

```mud
abstract thing Gate {
    open: Boolean
}

thing NorthGate as Gate {
    open = true
}

thing SouthGate as Gate {
    open = false
}
```

En el mundo $W$:

- `NorthGate` está activa y materializada.
- `SouthGate` fue destruida: está materializada, pero suspendida.
- Ambas conservan su valor almacenado de `open`.

## 1. Conjuntos

Escribe:

$$
\mathcal T_P,\qquad
\mathcal A_W,\qquad
\mathcal M_W
$$

e indica a qué estructura pertenece cada uno: programa o mundo.

## 2. Posiciones y store

Escribe el dominio de:

$$
\operatorname{store}_W
$$

y sus dos asociaciones.

Recuerda que el valor de un campo de cardinalidad omitida es una colección singleton.

## 3. Buena formación

Explica por qué:

$$
\mathcal A_W
\subsetneq
\mathcal M_W
$$

en este ejemplo y por qué eso no es un error.

## 4. Contraejemplo

Refuta esta propuesta:

$$
\mathcal A_W
=
\{
t
\mid
\exists f.\,
(t,f)\in
\operatorname{dom}(\operatorname{store}_W)
\}
$$

## 5. Pregunta crítica

¿Qué información se duplicaría si incluyésemos $\mathcal T_P$ como componente de $W$?

## Criterio de corrección

- No aparecen instancias ni una función `kind`.
- Reserva, materialización y actividad están separadas.
- El store conserva la carga de `SouthGate`.
- La explicación distingue información estática y dinámica.
