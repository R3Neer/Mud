---
id: D-072
title: "Entornos de resolución y migraciones explícitas de anclas"
status: vigente
date: 2026-08-02
supersedes: []
superseded-by: []
questions:
  - "Q-014"
affects:
  - "nombres cualificados, ámbitos, anclas, diagnósticos, migraciones, futuro capítulo 09 y tooling"
---
# ADR-072 — Entornos de resolución y migraciones explícitas de anclas

- Amplía: [[ADR-035-organizacion-nombres-using-y-anclas|D-035]]
- Ampliada por: [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]]
- Ajustada a la frontera de fases de [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].
- Decide parcialmente: [[../preguntas/Q-014-migracion-de-anclas|Q-014]]

## Contexto

La separación entre CST, AST superficial, resultados de resolución nominal e representación semántica posterior a tipado y elaboración exige fijar cómo se representan ámbitos y candidatos. También debe distinguirse qué nombres poseen identidad semántica persistente y qué nombres solo vinculan valores dentro de una declaración.

Las anclas legibles cambian cuando cambia el nombre cualificado de una declaración. Debe conservarse trazabilidad sin convertir el nombre antiguo en un alias fuente silencioso.

## Decisión

### Espacios de nombres

Todas las declaraciones superiores comparten un único espacio de nombres nominal, con independencia de su categoría. Dentro de un mismo path de MUD no pueden coexistir dos declaraciones con el mismo nombre nominal, aunque una sea `thing` y otra `action`, `rule` u otra categoría.

Los campos se identifican dentro de su propietario y pueden repetir su nombre en propietarios distintos. Su ancla incorpora el ancla del propietario. Los demás miembros anidados obedecen el ámbito de su declaración propietaria.

Roles, `given`, variables de iteración y vinculaciones locales son símbolos léxicos sin ancla. Pueden repetir nombre en declaraciones o bloques independientes, pero no dentro de un mismo ámbito ni mediante sombreado de un nombre visible.

### Modelo normativo de resolución

La norma define la resolución mediante entornos y conjuntos de candidatos ordenados. Para un nombre no cualificado se consulta, por niveles, el ámbito léxico, el propietario correspondiente, el mismo path de MUD, los `using` exactos y los `using` recursivos. Se toma el primer nivel no vacío y se exige un único candidato compatible con la categoría requerida.

Los scope graphs pueden usarse como representación de implementación o explicación, pero no son la autoridad normativa de MUD 1.0. Una implementación debe conservar los mismos candidatos, prioridades, ambigüedades y rechazos definidos por los juicios de resolución.

### Referencias diagnósticas

Un símbolo sin ancla puede describirse combinando el ancla de su propietario con una etiqueta humana:

```text
action::game.Heal - given amount
```

La escritura completa es información diagnóstica, no una ancla nueva. Cuando existe fuente disponible, el span continúa siendo la localización principal.

### Migración de anclas

MUD conserva anclas legibles derivadas de categoría y nombre cualificado. Un cambio de path, nombre o categoría cambia el ancla. El tooling registra explícitamente una correspondencia dirigida entre el ancla anterior y la nueva para migrar referencias persistentes, historial y datos asociados.

```text
thing::world.people.Person
→ thing::world.characters.Person
```

La correspondencia no convierte el ancla antigua en alias admitido por la resolución ordinaria de código fuente. El compilador del programa actualizado produce y resuelve únicamente el ancla vigente.

Q-014 permanece parcialmente decidida hasta fijar el formato y ubicación del registro, composición de varias migraciones, colisiones, periodo de conservación y aplicación concreta sobre mundos persistidos.

## Consecuencias

- Una categoría esperada nunca permite reutilizar un nombre superior ya ocupado.
- Los símbolos efímeros no contaminan el espacio global de anclas.
- La resolución puede especificarse y probarse sin imponer una estructura interna al compilador.
- Los movimientos mantienen trazabilidad mediante una operación explícita de tooling.
- La compatibilidad histórica no altera silenciosamente el significado del código fuente.

## Verificación

1. Rechazo de dos declaraciones superiores homónimas de igual o distinta categoría dentro del mismo path.
2. Campos homónimos válidos en propietarios distintos y anclas propietarias distintas.
3. Ausencia de ancla para roles, `given`, iteradores y locales.
4. Reutilización de un nombre local en ámbitos independientes.
5. Determinismo e independencia del orden físico mediante niveles de candidatos.
6. Diagnóstico descriptivo de un símbolo local sin fabricar una ancla.
7. Cambio de ancla al renombrar o mover entre paths.
8. Migración explícita de referencias persistentes sin alias fuente implícito.
