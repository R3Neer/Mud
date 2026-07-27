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
  - Q-042
  - Q-043
decisions:
  - D-014
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

## Restricciones confirmadas

La decisión [[notas/decisiones/ADR-014-ontologia-unificada-de-constructos|D-014]] fija:

1. Todo constructo posee identidad semántica.
2. Todo constructo concreto denota una cosa concreta con estado propio y puede ser antecesor de otros constructos.
3. Un constructo abstracto pertenece al mismo dominio, pero no denota directamente una cosa concreta con estado propio.
4. `create C N` crea otro constructo concreto $N$ relacionado con $C$ mediante el mismo `is` que una declaración estática.
5. La relación semántica `is` es reflexiva y transitiva.

La estructura de $W$ no se propondrá hasta determinar qué se hereda desde un constructo concreto y si la especialización directa debe ser acíclica.

## Cuestiones abiertas

> [!question] Q-042 — Herencia desde un constructo concreto
> Determinar si un descendiente hereda únicamente declaraciones y predeterminados o también copia u observa estado mutable actual.

> [!question] Q-043 — Ciclos de especialización
> Determinar si se prohíben los ciclos entre identidades distintas y, por tanto, si `is` forma un orden parcial.
