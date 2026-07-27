---
title: Respuesta 01 — Modelo mínimo de una puerta
unit: 1
status: revisada-con-rectificacion
author: Samuel
tags:
  - mud/aprendizaje
  - mud/respuesta
---

# Respuesta 01 — Modelo mínimo de una puerta

> [!warning] Contexto de la respuesta
> Esta respuesta resolvió correctamente el ejercicio planteado, pero el ejercicio empleaba una interpretación posteriormente descartada: un constructo MUD no es una clase con instancias. La notación se conserva como evidencia del aprendizaje; `northGate#1` y $\operatorname{kind}_{W_G}$ no forman parte de una propuesta normativa.

Referencia: [[aprendizaje/unidades/01-modelo-minimo-de-un-mundo]].

## Enunciado

Considera:

```mud
thing Gate {
    mut unlocked: Boolean
    mut open: Boolean
}
```

Existe una puerta con identidad didáctica `northGate#1`, tipo runtime `Gate`, `unlocked = true` y `open = false`.

## 1. Clasificación

Completa con una frase breve:

- `Gate` es un constructo.
- `northGate#1` es una identidad runtime didáctica.
- `unlocked` y `open` son campos.
- `true` y `false` son valores booleanos.

## 2. Conjuntos del ejemplo

Define:

Para el ejemplo local:

$$
C_G=\{\mathsf{Gate}\}
$$

$$
I_{W_G}=\{\mathit{northGate\#1}\}
$$

$$
F_G=\{\mathsf{unlocked},\mathsf{open}\}
$$

$$
V_G=\{\mathsf{true},\mathsf{false}\}
$$

El apartado 7 presupone además un conjunto global de campos del programa $\mathcal F_P$ tal que:

$$
\mathsf{treasury}\in\mathcal F_P
$$

## 3. Tipo runtime

Completa:

$$
\operatorname{kind}_{W_G}:
\mathcal I
\rightharpoonup
\mathcal C_P
$$

$$
\operatorname{kind}_{W_G}
(\mathit{northGate\#1})
=
\mathsf{Gate}
$$

Las identidades existentes se derivan del dominio de la función:

$$
I_{W_G}
:=
\operatorname{dom}(\operatorname{kind}_{W_G})
=
\{\mathit{northGate\#1}\}
$$

## 4. Store

Escribe el tipo de la función:

$$
\operatorname{store}_{W_G}:
I_{W_G}\times\mathcal F_P
\rightharpoonup
\mathcal V_P
$$

Después define sus dos asociaciones:

$$
\operatorname{store}_{W_G}
(\mathit{northGate\#1},\mathsf{unlocked})
=
\mathsf{true}
$$

$$
\operatorname{store}_{W_G}
(\mathit{northGate\#1},\mathsf{open})
=
\mathsf{false}
$$

## 5. Mundo

Escribe la tupla completa:

$$
W_G=
\left(
\operatorname{kind}_{W_G},
\operatorname{store}_{W_G}
\right)
$$

## 6. Explicación

Explica con tus palabras por qué hemos utilizado una función parcial para el store en lugar de una función total:

> Si fuera total sobre $I_{W_G}\times\mathcal F_P$, cada identidad tendría que poseer un valor para todos los campos declarados por el programa. Esto no tiene sentido porque cada constructo solo admite determinados campos.

## 7. Caso límite

Supón que también existe el campo `treasury` en el programa, pero solo pertenece a `Kingdom`.

¿Debería estar definido lo siguiente?

$$
\operatorname{store}_{W_G}
(\mathit{northGate\#1},\mathsf{treasury})
$$

Respuesta y justificación:

> No. El par $(\mathit{northGate\#1},\mathsf{treasury})$ pertenece a $I_{W_G}\times\mathcal F_P$, pero $\operatorname{store}_{W_G}$ no está definida para él porque `treasury` no es un campo aplicable a `Gate`. Esto es posible porque el store es una función parcial.

## 8. Duda o parte insegura

Indica al menos una parte en la que hayas dudado, aunque finalmente creas que está bien:

> Realmente no he dudado en ninguna parte, pero sí he necesitado consultar la teoría en varias ocasiones, sobre todo para recordar cómo se define el mundo y los nombres de los conjuntos. También he tenido que consultar un par de veces la sintaxis de LaTeX, que estoy aprendiendo mientras escribo estas respuestas.
