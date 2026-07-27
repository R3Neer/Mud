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

abstract construct Place from Entity {
    name: Text = ""
}

construct Settlement from Place {
}

construct Alexandria from Settlement {
    name = "Alexandria"
}

construct NileDelta from Place {
    name = "Nile Delta"
}
```

Durante la ejecución ocurre:

```mud
create construct Memphis from Settlement {
    name = "Memphis"
}

create construct Monument {
}

create abstract construct RiverRegion from Place {
}

create construct DeltaCapital from NileDelta, Settlement {
    name = "Delta Capital"
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

Define por extensión el conjunto de identidades reservadas:

$$
\mathcal R_P^{\mathsf{create}}
$$

Después define las cuatro asociaciones de:

$$
\operatorname{shape}_P
$$

Cada resultado de $\operatorname{shape}_P$ debe indicar:

1. Si el constructo es abstracto o concreto.
2. Su conjunto finito de antecesores directos.

Como las cuatro creaciones son efectivas en el escenario, define:

$$
\mathcal D_W
$$

restringe $\operatorname{shape}_P$ para obtener $\operatorname{created}_W$ y comprueba:

$$
\operatorname{dom}(\operatorname{created}_W)
=
\mathcal D_W
$$

Después deriva:

$$
\mathcal A_W
:=
\{
c\in\mathcal D_W
\mid
\pi_1(\operatorname{created}_W(c))
=
\mathsf{abstract}
\}
$$

y:

$$
\mathcal C_{P,W}
:=
\mathcal C_P\cup\mathcal D_W
$$

Comprueba además:

1. Que todas las identidades estaban reservadas antes de activarse.
2. Que ninguna estaba activa inmediatamente antes de su creación efectiva.
3. Que todos los antecesores indicados pertenecen a $\mathcal C_{P,W}$.
4. Que las nuevas aristas no forman ciclos.
5. Que `Monument` continúa perteneciendo a $\mathcal D_W$ aunque no añada ninguna arista.

## 4. Relación directa completa

Construye:

$$
R_{P,W}^{\mathrm{dir}}
$$

Primero deriva $R_W^{\mathrm{dir}}$ y después construye $R_{P,W}^{\mathrm{dir}}$, incluyendo todos los pares introducidos por las creaciones.

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
Monument is Monument
Monument is Entity
RiverRegion is Entity
DeltaCapital is NileDelta
DeltaCapital is Settlement
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
construct Entity from Alexandria {
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

## 9. `from` e `is`

Clasifica `from` e `is` como:

- Introducción de una arista directa.
- Consulta de la relación reflexiva y transitiva.

```mud
construct Alexandria from Settlement {
}

Alexandria is Place
```

Explica qué nodo del AST corresponde a cada construcción y por qué emplear palabras distintas refleja sus niveles semánticos.

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
7. Representar correctamente creaciones raíz, abstractas y con varios antecesores.

> [!hint]- Pista 1
> Hay cinco constructos declarados y cuatro creados.

> [!hint]- Pista 2
> `Monument` no aparece en $R_W^{\mathrm{dir}}$, pero sí en el dominio de $\operatorname{created}_W$.

> [!hint]- Pista 3
> Para demostrar el ciclo, comienza en `Entity`, sigue todas las aristas y regresa al punto inicial.
