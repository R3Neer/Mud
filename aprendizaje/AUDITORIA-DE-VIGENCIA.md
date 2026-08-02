---
title: Auditoría de vigencia del itinerario
tags:
  - mud/aprendizaje
  - mud/gobierno
status: activo
---

# Auditoría de vigencia del itinerario

> [!abstract]
> Este documento comprueba que las unidades didácticas enseñan el MUD vigente. No forma parte de la especificación normativa.

## Estado de las unidades fundamentales

| Unidad | Estado | Modelo enseñado |
| --- | --- | --- |
| [[aprendizaje/unidades/01-modelo-minimo-de-un-mundo|01 — Programa, mundo y store mínimo]] | Actualizada | Un solo dominio de `thing`; reserva, materialización, actividad y carga |
| [[aprendizaje/unidades/02-constructos-como-orden-parcial|02 — `Thing` como orden parcial]] | Actualizada y activa | `as` directo, raíz incorporada `Thing`, `is` reflexivo-transitivo, grafo almacenado y grafo efectivo |
| [[aprendizaje/unidades/03-esquema-heredable-y-estado-independiente|03 — Esquema heredable y estado independiente]] | Planificada y alineada | Esquema heredado, estado independiente, propiedades suspendidas y colecciones |

La primera versión de la Unidad 01 usaba una separación entre clases e instancias que MUD ya no admite. Se conserva, junto con el ejercicio, la respuesta y la revisión originales, en [[aprendizaje/historico/01-modelo-clase-instancia/README|el archivo histórico]].

## Lista de control para nuevas unidades

Una unidad nueva o revisada debe comprobar, cuando el tema sea aplicable, que:

- Emplea `thing`, no `construct`, como palabra clave.
- Emplea `as` para declarar especialización directa.
- Emplea `is` como consulta reflexiva y transitiva, no como declaración.
- No introduce clases, objetos ni instancias.
- Distingue definición canónica, activación inicial, materialización almacenada y actividad efectiva.
- Distingue el grafo almacenado del efectivo cuando intervienen `create` o `destroy`.
- No hereda estado activo.
- Rechaza ciclos de especialización.
- Exige membresía estricta $c\neq T\land c\ \mathsf{is}\ T$ en colecciones de tipo `T`.
- No introduce el modificador eliminado `[reflexive]`.
- Trata todos los campos como colecciones y la cardinalidad omitida como `[1]`.
- Mantiene separadas la mutabilidad exterior y la capacidad interior.
- Usa `on` para participantes observados automáticamente y `for` —con posible `given`— para participantes suministrados.
- Comprueba la cardinalidad al final atómico de cada `then`, mediante análisis estático de sus efectos posibles.
- Trata `action` como entrada y `look`/`message` como salidas del modelo.
- Usa `Bool`, no el nombre histórico `Boolean`.
- Distingue representaciones numéricas básicas de magnitudes y no introduce sufijos de tipo.
- Usa `:=` para derivación dimensional, `in` para unidad de expresión y `to` para conversión cuantitativa.
- Solo presenta ciclos mediante un dominio de punto `[a..b cycle)`.
- Presenta todos los aliases como tipos nominales de valores inmutables y sin ciclo de vida runtime.
- Usa `:=` para aliases definidos por expresión de tipo y reserva el bloque para componentes ordenados.
- Distingue construcción contextual de literales y casting nominal explícito mediante `to`.
- No permite reordenar componentes nombrados ni comparar aliases nominales distintos sin conversión.
- Presenta `Num` como racional exacto y `Rum` como aproximación explícita `binary64`.
- Exige `r` en literales `Rum` puros, pero no necesariamente en cantidades de magnitudes `Rum`.
- No mezcla `Num` y `Rum` sin `to` ni enumera intervalos `Rum`.

## Autoridad

Si una lección contradice una decisión aceptada o la especificación vigente, la lección se corrige: el material didáctico nunca tiene autoridad normativa. Las decisiones todavía no promovidas se consultan en [[notas/decisiones/README|el índice de decisiones]] y las cuestiones abiertas en [[notas/preguntas/README|Preguntas activas]].
