---
title: Respuesta 01 — Modelo mínimo de una puerta
unit: 1
status: pendiente
author: Samuel
tags:
  - mud/aprendizaje
  - mud/respuesta
---

# Respuesta 01 — Modelo mínimo de una puerta

Referencia: [[aprendizaje/unidades/01-modelo-minimo-de-un-mundo]].

## Enunciado

Considera:

```mud
construct Gate {
    mut unlocked: Boolean
    mut open: Boolean
}
```

Existe una puerta con identidad didáctica `northGate#1`, tipo runtime `Gate`, `unlocked = true` y `open = false`.

## 1. Clasificación

Completa con una frase breve:

- `Gate` es: un constructo
- `northGate#1` es: una identidad
- `unlocked` y `open` son: campos (fields)
- `true` y `false` son: valores

## 2. Conjuntos del ejemplo

Define:

$$
C_G= \{Gate\}
$$

$$
I_G= \{northGate\#1\}
$$

$$
F_G= \{unlocked, open\}
$$

$$
V_G= \{true, false\}
$$

## 3. Tipo runtime

Completa:

$$
\operatorname{kind}_{W_G}:
I_{G}
\to
C_{G}
$$

$$
\operatorname{kind}_{W_G}
(northGate\#1)
=
Gate
$$

## 4. Store

Escribe el tipo de la función:

$$
\operatorname{store}_{W_G}:
I_{G} \times F_{G}
\rightharpoonup
V_{G}
$$

Después define sus dos asociaciones:

$$
\operatorname{store}_{W_G}
(northGate\#1,unlocked)
=
true
$$

$$
\operatorname{store}_{W_G}
(northGate\#1,open)
=
false
$$

## 5. Mundo

Escribe la tupla completa:

$$
W_G=
\left(
I_{G},
kind_{G},
store_{G}
\right)
$$

## 6. Explicación

Explica con tus palabras por qué hemos utilizado una función parcial para el store en lugar de una función total:

> Porque si fuera total significaría que para cada identidad todos los campos existentes en el mundo tendrían valor. Esto no tiene sentido porque solo hay ciertos campos por constructo (las identidades están relacionadas de forma total con los constructos)
## 7. Caso límite

Supón que también existe el campo `treasury` en el programa, pero solo pertenece a `Kingdom`.

¿Debería estar definido lo siguiente?

$$
\operatorname{store}_{W_G}
(\mathit{northGate\#1},\mathsf{treasury})
$$

Respuesta y justificación:

>No. Precisamente es gracias a que $store_{W_{G}}$ es una aplicación parcial y no total que se puede no definir en este caso.

## 8. Duda o parte insegura

Indica al menos una parte en la que hayas dudado, aunque finalmente creas que está bien:

> Realmente dudado en ninguna. Pero si he necesitado consultar la teoría en varias ocasiones. Sobre todo para la parte de cómo se define el mundo. También para los nombres de los conjuntos. Y un un par de veces para latex, ya que no sé escribirlo y estoy aprendiendo conforme escribo estas respuestas.
