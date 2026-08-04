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
decisions:
  - D-014
  - D-015
  - D-054
  - D-017
  - D-025
  - D-019
  - D-026
  - D-021
  - D-055
  - D-068
  - D-077
---

# 04. Modelo matemático del mundo

## Estado y propósito

Este capítulo definirá las estructuras matemáticas que representan un programa y un estado del mundo MUD antes de introducir su sintaxis concreta o su ejecución.

El contenido normativo todavía no ha sido redactado.

## Dependencias

- [[02-terminologia|Terminología]].
- [[03-notacion|Notación matemática y metalenguaje]].

## Contenido previsto

- Definiciones canónicas del programa e identidades activas en cada mundo.
- Conjunto inicial `start with`, creación, destrucción y reactivación.
- Identidad de `thing`.
- Relación de especialización `is`.
- Store de campos y relaciones.
- Información almacenada y proyección efectiva.
- Suspensión transitiva por dependencias duras.
- Identidad frente a igualdad estructural.
- Estados bien formados.
- Estados estables y tentativos.
- Observaciones semánticamente visibles.
- Mundos aislados y descartables de los tests.

## Restricción del modelo

MUD no presupone una separación entre clases y objetos. En particular, una `thing` no tiene instancias. El modelo matemático deberá representar dentro de un mismo dominio conceptual las definiciones canónicas del programa y las identidades activas en cada mundo, sin convertirlas en clase e instancia.

> [!warning] Modelo retirado
> La representación $W=(\operatorname{kind}_W,\operatorname{store}_W)$ suponía identidades runtime clasificadas por cosas mediante `kind`. Esa separación no corresponde al concepto de `thing` de MUD y no es una estructura candidata.

## Restricciones confirmadas

Las decisiones aceptadas fijan:

1. Toda `thing` posee identidad semántica.
2. Toda `thing` concreta denota una cosa concreta con estado propio y puede ser antecesora de otras.
3. Una `thing` abstracta pertenece al mismo dominio, pero no denota directamente una cosa concreta con estado propio.
4. Cada `thing` tiene una única definición canónica de primer nivel, que fija su carácter abstracto o concreto, sus antecesoras directas y su cuerpo.
5. La relación semántica `is` es reflexiva y transitiva.
6. La especialización directa es acíclica, por lo que `is` es también antisimétrica y forma un orden parcial.
7. Se heredan declaraciones, restricciones, dominios y predeterminados efectivos, pero no estado mutable activo.
8. Cada `thing` concreta posee estado independiente.
9. `create Nombre` solo activa una `thing` o regla definida; no admite categoría, antecesoras ni cuerpo.
10. Si la identidad canónica está ausente, `create` la activa; tras destruirla, una creación posterior reactiva la misma identidad, descriptor y carga.
11. Todo tipo bien formado posee un valor predeterminado perteneciente a su dominio.
12. `as` introduce especialización directa; `is` queda reservado para consultar su clausura reflexiva y transitiva.
13. Una regla que contiene `create A` solo se ejecuta si la identidad canónica `A` está ausente.
14. Todo campo denota una colección; su mutabilidad exterior y la capacidad sobre sus miembros son permisos ortogonales incluso con cardinalidad `[1]`.
15. Una colección de `thing` exige siempre membresía estricta: $c\neq T\land c\ \mathsf{is}\ T$. No existe `reflexive`.
16. `destroy` solo confirma una retirada si todas las cardinalidades y dominios resultantes son válidos; en otro caso produce `failed` y rollback.
17. Una declaración con una dependencia dura inactiva se suspende completa; no se reescriben parcialmente sus campos ni participantes.
18. `remove` sobre una propiedad elimina su declaración y carga almacenadas, a diferencia de la suspensión reversible producida por `destroy`.
19. Una única declaración global `start with` determina un conjunto finito y no ordenado de `thing` y reglas inicialmente activas.
20. `start with` contiene referencias separadas por comas sin coma final y no admite instrucciones ni efectos.
21. Las definiciones no están activas por defecto; si se omite `start with`, el conjunto inicial de declaraciones con ciclo de vida está vacío.
22. Cada test construye un mundo fresco y aislado cuyo `start with` local sustituye al global.
23. Los tests no son declaraciones activables ni forman parte del mundo o de su API pública.
24. El mundo construido para un test y todas sus salidas se descartan al terminar su ejecución.
25. `Thing` es una `thing` abstracta incorporada, siempre efectiva y superior a toda `thing` mediante `is`.
26. Una raíz sin `as` conserva cero antecesoras declaradas y recibe una arista semántica implícita hacia `Thing`.
27. `Thing` no posee estado concreto ni ciclo de vida controlable por el programa.
28. Toda `thing` posee un `name: Text` intrínseco, inmutable y local a su descriptor.
29. El `name` predeterminado es el nombre nominal no cualificado y una sobrescritura no se hereda.
30. La identidad y el ancla no dependen de `name`; varias `thing` pueden compartir la misma presentación.
31. Una relación inmutable conserva latentemente una identidad retirada y la restaura con `create`; una relación `mut` elimina esa pertenencia almacenada.
32. Ningún estado confirmado contiene una colección cuya cardinalidad efectiva contradiga su declaración.

Estas restricciones proceden de [[notas/decisiones/ADR-014-ontologia-unificada-de-things|D-014]], [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|D-015]], [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]], [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|D-017]], [[notas/decisiones/ADR-018-as-declara-is-consulta|D-018]], [[notas/decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|D-019]], [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]], [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|D-025]], [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]], [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]], [[notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco|D-068]] y [[notas/decisiones/ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]].

## Próximo desarrollo

El siguiente borrador deberá separar formalmente el grafo de `thing`, el esquema heredable y el estado independiente de cada `thing` concreta antes de proponer los componentes definitivos de $W$.

> [!question] Q-046 — Creación inefectiva
> Determinar el resultado de acciones y de bloques con varias creaciones. Para una regla con una sola creación ya se ha decidido que la regla completa no se ejecuta si la identidad está activa.

> [!question] Q-047 — Predeterminados concretos
> Determinar el valor predeterminado de cada constructor de tipos y su comportamiento cuando el dominio depende del mundo.

## Extensión confirmada para aliases

D-084 añade un segundo orden parcial nominal sobre aliases. Sus nodos son tipos de valor, no identidades activables. La especialización directa es acíclica y su clausura `is` es reflexiva, transitiva y antisimétrica.

Para un alias nominal con varias antecesoras, el conjunto de valores del descendiente debe estar contenido en la intersección de los conjuntos de valores de todas ellas. La unión `A | B` no satisface esta obligación. Para aliases estructurales, la forma efectiva se obtiene acumulando miembros por origen: un mismo miembro heredado por varias rutas se deduplica y miembros independientes con el mismo nombre producen conflicto.

Los campos derivados denotan colecciones recalculadas. Su pertenencia se fija durante una instantánea de evaluación y se vuelve a calcular sobre el estado posterior consolidado. La capacidad interior es parte del contrato de la colección derivada y no del linaje de la fuente. Las colecciones almacenadas, en cambio, conservan su pertenencia hasta una modificación estructural explícita.
