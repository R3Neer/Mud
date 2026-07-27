---
title: Modelo matemático del mundo
aliases:
  - Modelo formal del mundo MUD
tags:
  - mud/especificacion
  - mud/normativa
status: esqueleto
normative: true
depends-on:
  - "[[02-terminologia]]"
  - "[[03-notacion]]"
questions:
  - Q-WORLD-001
decisions: []
---

# 04. Modelo matemático del mundo

## Estado y propósito

Este capítulo definirá las estructuras matemáticas que representan un programa y un estado del mundo MUD antes de introducir su sintaxis concreta o su ejecución.

El contenido normativo todavía no ha sido redactado.

## Dependencias

- [[02-terminologia|Terminología]].
- [[03-notacion|Notación matemática y metalenguaje]].

## Contenido previsto

- Universos estáticos proporcionados por un programa.
- Identidades runtime y tipos de constructo.
- Store de campos y relaciones.
- Identidad frente a igualdad estructural.
- Estados bien formados.
- Estados estables y tentativos.
- Observaciones semánticamente visibles.

## Estructuras candidatas

La fase preparatoria estudia representar un mundo mediante las funciones que contienen su información:

$$
W=(\operatorname{kind}_W,\operatorname{store}_W)
$$

En ese planteamiento, el conjunto de identidades existentes no es un componente independiente, sino una cantidad derivada:

$$
I_W:=\operatorname{dom}(\operatorname{kind}_W)
$$

Estas fórmulas son candidatas y no serán normativas hasta que se definan sus universos, condiciones de buena formación e interacciones.

## Cuestiones abiertas

> [!question] Q-WORLD-001 — Representación canónica del mundo
> Determinar la estructura mínima del estado del mundo y qué información debe ser primitiva o derivada. La propuesta inicial elimina $I_W$ como componente independiente y lo deriva de $\operatorname{kind}_W$.
