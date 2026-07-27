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
  - Q-046
  - Q-047
  - Q-048
decisions:
  - D-014
  - D-015
  - D-016
  - D-017
  - D-018
---

# 04. Modelo matemático del mundo

## Estado y propósito

Este capítulo definirá las estructuras matemáticas que representan un programa y un estado del mundo MUD antes de introducir su sintaxis concreta o su ejecución.

El contenido normativo todavía no ha sido redactado.

## Dependencias

- [[02-terminologia|Terminología]].
- [[03-notacion|Notación matemática y metalenguaje]].

## Contenido previsto

- Identidades reservadas por el programa e identidades activas en cada mundo.
- Activación inicial, creación, destrucción y reactivación.
- Identidad de constructos.
- Relación de especialización `is`.
- Store de campos y relaciones.
- Identidad frente a igualdad estructural.
- Estados bien formados.
- Estados estables y tentativos.
- Observaciones semánticamente visibles.

## Restricción del modelo

MUD no presupone una separación entre clases y objetos. En particular, un constructo no tiene instancias. El modelo matemático deberá representar dentro de un mismo dominio conceptual las identidades activadas inicialmente y las activadas mediante `create`, distinguiendo reserva de identidad y presencia activa sin convertirlas en clase e instancia.

> [!warning] Modelo retirado
> La representación $W=(\operatorname{kind}_W,\operatorname{store}_W)$ suponía identidades runtime clasificadas por constructos mediante `kind`. Esa separación no corresponde al concepto de constructo de MUD y no es una estructura candidata.

## Restricciones confirmadas

La decisión [[notas/decisiones/ADR-014-ontologia-unificada-de-constructos|D-014]] fija:

1. Todo constructo posee identidad semántica.
2. Todo constructo concreto denota una cosa concreta con estado propio y puede ser antecesor de otros constructos.
3. Un constructo abstracto pertenece al mismo dominio, pero no denota directamente una cosa concreta con estado propio.
4. `create` puede activar identidades reservadas raíz, abstractas o concretas y añadir cero o varios antecesores mediante `from`.
5. La relación semántica `is` es reflexiva y transitiva.
6. La especialización directa es acíclica, por lo que `is` es también antisimétrica y forma un orden parcial.
7. Se heredan declaraciones, restricciones, dominios y predeterminados efectivos, pero no estado mutable activo.
8. Cada constructo concreto posee estado independiente.
9. El bloque de `create` es un cuerpo declarativo completo, no solo una lista de asignaciones.
10. Si la identidad reservada está ausente, `create` la activa; tras destruirla, una creación posterior reactiva la misma identidad.
11. Todo tipo bien formado posee un valor predeterminado perteneciente a su dominio.
12. `from` introduce especialización directa; `is` queda reservado para consultar su clausura reflexiva y transitiva.
13. Una regla que contiene `create A` solo se ejecuta si la identidad reservada `A` está ausente.

Estas restricciones proceden de [[notas/decisiones/ADR-014-ontologia-unificada-de-constructos|D-014]], [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|D-015]], [[notas/decisiones/ADR-016-creacion-generalizada-de-constructos|D-016]], [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|D-017]] y [[notas/decisiones/ADR-018-from-declara-is-consulta|D-018]].

## Próximo desarrollo

El siguiente borrador deberá separar formalmente el grafo de constructos, el esquema heredable y el estado independiente de cada constructo concreto antes de proponer los componentes definitivos de $W$.

> [!question] Q-046 — Creación inefectiva
> Determinar el resultado de acciones y de bloques con varias creaciones. Para una regla con una sola creación ya se ha decidido que la regla completa no se ejecuta si la identidad está activa.

> [!question] Q-047 — Predeterminados concretos
> Determinar el valor predeterminado de cada constructor de tipos y su comportamiento cuando el dominio depende del mundo.

> [!question] Q-048 — Destrucción y descendientes
> Determinar el efecto de destruir un constructo con descendientes activos.
