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

- `Gate` es:
- `northGate#1` es:
- `unlocked` y `open` son:
- `true` y `false` son:

## 2. Conjuntos del ejemplo

Define:

$$
C_G=
$$

$$
I_G=
$$

$$
F_G=
$$

$$
V_G=
$$

## 3. Tipo runtime

Completa:

$$
\operatorname{kind}_{W_G}:
\underline{\hspace{3cm}}
\to
\underline{\hspace{3cm}}
$$

$$
\operatorname{kind}_{W_G}
(\underline{\hspace{3cm}})
=
\underline{\hspace{3cm}}
$$

## 4. Store

Escribe el tipo de la función:

$$
\operatorname{store}_{W_G}:
\underline{\hspace{4cm}}
\rightharpoonup
\underline{\hspace{3cm}}
$$

Después define sus dos asociaciones:

$$
\operatorname{store}_{W_G}
(\underline{\hspace{3cm}},\underline{\hspace{3cm}})
=
\underline{\hspace{2cm}}
$$

$$
\operatorname{store}_{W_G}
(\underline{\hspace{3cm}},\underline{\hspace{3cm}})
=
\underline{\hspace{2cm}}
$$

## 5. Mundo

Escribe la tupla completa:

$$
W_G=
\left(
\underline{\hspace{3cm}},
\underline{\hspace{3cm}},
\underline{\hspace{3cm}}
\right)
$$

## 6. Explicación

Explica con tus palabras por qué hemos utilizado una función parcial para el store en lugar de una función total:

> Escribe aquí.
## 7. Caso límite

Supón que también existe el campo `treasury` en el programa, pero solo pertenece a `Kingdom`.

¿Debería estar definido lo siguiente?

$$
\operatorname{store}_{W_G}
(\mathit{northGate\#1},\mathsf{treasury})
$$

Respuesta y justificación:

> Escribe aquí.

## 8. Duda o parte insegura

Indica al menos una parte en la que hayas dudado, aunque finalmente creas que está bien:

> Escribe aquí.
