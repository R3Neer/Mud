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
  - Q-041
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

- Constructos proporcionados por un programa y constructos creados durante la ejecución.
- Identidad de constructos.
- Relación de especialización `is`.
- Store de campos y relaciones.
- Identidad frente a igualdad estructural.
- Estados bien formados.
- Estados estables y tentativos.
- Observaciones semánticamente visibles.

## Restricción del modelo

MUD no presupone una separación entre clases y objetos. En particular, un constructo no tiene instancias. El modelo matemático deberá representar dentro de un mismo dominio conceptual los constructos declarados y los creados durante la ejecución.

> [!warning] Modelo retirado
> La representación $W=(\operatorname{kind}_W,\operatorname{store}_W)$ suponía identidades runtime clasificadas por constructos mediante `kind`. Esa separación no corresponde al concepto de constructo de MUD y no es una estructura candidata.

La estructura de $W$ no se propondrá hasta resolver [[notas/08-preguntas-abiertas#Q-041 — Ontología de constructos|Q-041]].

## Cuestiones abiertas

> [!question] Q-041 — Ontología de constructos
> Determinar la estructura matemática común de los constructos declarados y creados durante la ejecución, la semántica exacta de `is` y el efecto de `create`. La resolución debe respetar que un constructo no tiene instancias.
