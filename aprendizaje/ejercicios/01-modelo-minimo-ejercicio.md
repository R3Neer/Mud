---
title: Ejercicio 01 — Modelo mínimo de una puerta
unit: 1
status: sustituido
level: 1
tags:
  - mud/aprendizaje
  - mud/ejercicio
---

# Ejercicio 01 — Modelo mínimo de una puerta

> [!warning] Ejercicio histórico
> Este ejercicio conserva el contramodelo clase–instancia que fue retirado tras su revisión. No debe utilizarse como modelo semántico de MUD. Se mantiene como procedencia del aprendizaje de funciones parciales y redundancia representacional.

Referencia: [[aprendizaje/unidades/01-modelo-minimo-de-un-mundo]].

## Enunciado

Considera:

```mud
construct Gate {
    mut unlocked: Boolean
    mut open: Boolean
}

construct Kingdom {
    mut treasury: Money
}
```

Existe una puerta con identidad didáctica `northGate#1`, tipo runtime `Gate`, `unlocked = true` y `open = false`. En este mundo no existe todavía ninguna instancia de `Kingdom`.

## 1. Clasificación

Clasifica:

- `Gate`.
- `northGate#1`.
- `unlocked`, `open` y `treasury`.
- `true` y `false`.

## 2. Contexto estático

Define conjuntos de ejemplo para:

$$
\mathcal C_P
$$

$$
\mathcal F_P
$$

$$
\mathcal V_P
$$

Incluye `treasury` en el conjunto de campos aunque no pertenezca a `Gate`.

## 3. Tipo runtime

Escribe:

$$
\operatorname{kind}_{W_G}:
\mathcal I
\rightharpoonup
\mathcal C_P
$$

y define la asociación correspondiente a `northGate#1`.

Después deriva:

$$
I_{W_G}:=
\operatorname{dom}(\operatorname{kind}_{W_G})
$$

## 4. Store

Escribe:

$$
\operatorname{store}_{W_G}:
I_{W_G}\times\mathcal F_P
\rightharpoonup
\mathcal V_P
$$

Define sus asociaciones para `unlocked` y `open`.

## 5. Mundo

Completa:

$$
W_G=
\left(
\underline{\hspace{4cm}},
\underline{\hspace{4cm}}
\right)
$$

## 6. Parcialidad

Explica por qué:

$$
\operatorname{store}_{W_G}
(\mathit{northGate\#1},\mathsf{treasury})
$$

no está definida.

Después explica por qué el ejemplo no justificaría la parcialidad si el segundo componente del dominio fuese únicamente:

$$
\{\mathsf{unlocked},\mathsf{open}\}
$$

## 7. Pregunta crítica

¿Añadirías $I_{W_G}$ como tercer componente explícito del mundo? Justifica qué información aporta o repite.

> [!hint]- Pista 1
> El dominio forma parte de la definición matemática de una función.

> [!hint]- Pista 2
> Compara $\operatorname{dom}(\operatorname{kind}_{W_G})$ con $I_{W_G}$.
