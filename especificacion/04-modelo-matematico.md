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
  - Q-044
  - Q-045
decisions:
  - D-014
  - D-015
  - D-016
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
4. `create` puede crear constructos raíz, abstractos o concretos y añadir cero o varios antecesores mediante `from`.
5. La relación semántica `is` es reflexiva y transitiva.
6. La especialización directa es acíclica, por lo que `is` es también antisimétrica y forma un orden parcial.
7. Se heredan declaraciones, restricciones, dominios y predeterminados efectivos, pero no estado mutable activo.
8. Cada constructo concreto posee estado independiente.
9. Un `create` concreto inicializa desde los predeterminados efectivos combinados y aplica después sus asignaciones explícitas.

Estas restricciones proceden de [[notas/decisiones/ADR-014-ontologia-unificada-de-constructos|D-014]], [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|D-015]] y [[notas/decisiones/ADR-016-creacion-generalizada-de-constructos|D-016]].

## Próximo desarrollo

El siguiente borrador deberá separar formalmente el grafo de constructos, el esquema heredable y el estado independiente de cada constructo concreto antes de proponer los componentes definitivos de $W$.

> [!question] Q-044 — Identidad y referencias futuras
> Determinar si el nombre de `create` es una identidad global reservada o una vinculación local a una identidad fresca, y si puede resolverse antes de existir.

> [!question] Q-045 — Esquema dinámico
> Determinar si `create` puede declarar esquema nuevo o únicamente relaciones de especialización e inicialización de estado.
