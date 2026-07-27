---
title: Ejercicio 02 — Orden parcial de constructos
unit: 2
status: vigente
level: 1
tags:
  - mud/aprendizaje
  - mud/ejercicio
---

# Ejercicio 02 — Orden parcial de constructos

Referencia: [[aprendizaje/unidades/02-constructos-como-orden-parcial]].

Completa la plantilla [[aprendizaje/respuestas/02-orden-parcial-de-constructos-respuesta]].

## Enunciado

Considera:

```mud
abstract construct Entity {
}

abstract construct Place is Entity {
}

construct Settlement is Place {
    name: Text = ""
}

construct Alexandria is Settlement {
    name = "Alexandria"
}

construct NileDelta is Place {
    name = "Nile Delta"
}
```

Durante la ejecución ocurre:

```mud
create Settlement Memphis {
    name = "Memphis"
}
```

## 1. Conjuntos declarados

Define por extensión:

$$
\mathcal C_P
$$

$$
\mathcal A_P
$$

y deriva:

$$
\mathcal K_P
:=
\mathcal C_P\setminus\mathcal A_P
$$

## 2. Especialización directa estática

Escribe:

$$
R_P^{\mathrm{dir}}
\subseteq
\mathcal C_P\times\mathcal C_P
$$

y enumera todos sus pares.

Usa la orientación:

$$
(\text{más específico},\text{antecesor directo})
$$

## 3. Creación

Define la asociación de:

$$
\operatorname{base}_W
$$

correspondiente a `Memphis`.

Después deriva:

$$
\mathcal D_W
:=
\operatorname{dom}(\operatorname{base}_W)
$$

y:

$$
\mathcal C_{P,W}
:=
\mathcal C_P\cup\mathcal D_W
$$

Comprueba además:

1. Que `Memphis` es una identidad fresca respecto a $\mathcal C_P$.
2. Que su base pertenece a $\mathcal C_{P,W}$.
3. Que la nueva arista no forma un ciclo.

## 4. Relación directa completa

Construye:

$$
R_{P,W}^{\mathrm{dir}}
$$

incluyendo el par introducido por `create`.

## 5. Consultas `is`

Indica si son verdaderas o falsas y justifica cada respuesta mediante:

- Identidad.
- Arista directa.
- Camino de más de una arista.
- Ausencia de camino.

Consultas:

```mud
Alexandria is Settlement
Alexandria is Entity
Place is Place
Place is Alexandria
Memphis is Entity
NileDelta is Settlement
```

## 6. Antecesores

Define:

$$
\operatorname{Anc}_{P,W}(c)
:=
\{
a\in\mathcal C_{P,W}
\mid
c\preceq_{P,W}a
\}
$$

Calcula:

$$
\operatorname{Anc}_{P,W}(\mathsf{Memphis})
$$

Incluye el propio constructo si la relación es reflexiva.

## 7. Ciclo inválido

Supón que se añade:

```mud
construct Entity is Alexandria {
}
```

Escribe el camino no vacío que demostraría el ciclo y explica qué propiedad del orden parcial quedaría destruida si `Entity` y `Alexandria` siguieran siendo identidades distintas.

## 8. Función o relación

Explica por qué:

$$
\operatorname{parent}:\mathcal C\to\mathcal C
$$

no basta para representar toda la especialización de MUD.

Construye un ejemplo mínimo de especialización múltiple que lo demuestre.

## 9. Dos usos de `is`

Clasifica cada aparición de `is` como:

- Introducción de una arista directa.
- Consulta de la relación reflexiva y transitiva.

```mud
construct Alexandria is Settlement {
}

Alexandria is Place
```

Explica por qué el parser puede distinguirlas aunque el lexer produzca el mismo token.

## 10. Parte insegura

Indica al menos una parte en la que hayas dudado o que hayas tenido que comprobar.

## Criterio de corrección

La respuesta debe:

1. Contener todos los pares directos y solo esos pares.
2. Mantener la orientación acordada.
3. Distinguir relación directa y clausura.
4. Aplicar correctamente reflexividad y transitividad.
5. Exhibir el ciclo mediante un camino.
6. Justificar por qué la especialización general es una relación.

> [!hint]- Pista 1
> Hay cinco constructos declarados y uno creado.

> [!hint]- Pista 2
> `Memphis` no pertenece a $\mathcal C_P$, pero sí a $\mathcal C_{P,W}$.

> [!hint]- Pista 3
> Para demostrar el ciclo, comienza en `Entity`, sigue todas las aristas y regresa al punto inicial.
