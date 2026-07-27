---
title: Unidad 03 — Esquema heredable y estado independiente
aliases:
  - Esquema y estado de constructos
unit: 3
status: planificada
level: 1-a-2
depends-on:
  - "[[aprendizaje/unidades/02-constructos-como-orden-parcial]]"
concepts:
  - esquema efectivo
  - estado independiente
  - posiciones válidas
  - funciones dependientes
  - buena formación
  - valores predeterminados
spec-chapters:
  - "[[especificacion/04-modelo-matematico]]"
  - "[[especificacion/README#11. Constructos, especialización e identidad]]"
  - "[[especificacion/README#14. Campos, mutabilidad y capacidades]]"
decisions:
  - D-014
  - D-015
  - D-016
  - D-017
  - D-019
tags:
  - mud/aprendizaje
  - mud/unidad
---

# Unidad 03 — Esquema heredable y estado independiente

> [!abstract]
> Esta unidad está planificada, pero no activa. Se desarrollará después del intento y la revisión de la Unidad 02 para que la aplicación del orden parcial no aparezca antes de practicarlo.

## Pregunta de MUD

Si `Egypt is Kingdom`, `Egypt` hereda el campo `treasury`, pero una mutación de `Kingdom.treasury` no modifica `Egypt.treasury`.

La pregunta será:

> ¿Cómo derivamos qué campos puede tener cada constructo sin confundir el esquema heredado con el estado independiente de cada cosa concreta?

## Objetivos previstos

La unidad enseñará a:

1. Derivar los antecesores de un constructo mediante el orden parcial.
2. Distinguir campos declarados de campos efectivos.
3. Modelar la fusión de campos heredados sin reducirla a una unión ingenua.
4. Separar expresión predeterminada de valor activo.
5. Definir las posiciones válidas del estado.
6. Comparar un store parcial sobre un producto grande con un store total sobre posiciones válidas.
7. Escribir condiciones iniciales de buena formación.
8. Comprobar que estados de antecesores y descendientes son independientes.
9. Modelar todo campo como colección y separar mutabilidad exterior de capacidad interior.

## Prerrequisito de activación

Antes de activar esta unidad debe existir una revisión de:

[[aprendizaje/respuestas/02-orden-parcial-de-constructos-respuesta]]

que demuestre al menos:

- Orientación correcta de la especialización.
- Distinción entre relación directa y clausura.
- Comprensión de reflexividad, transitividad y antisimetría.
- Detección de ciclos.

## Decisiones ya fijadas

La unidad no volverá a discutir:

- Si existen clases e instancias: no existen como dominios separados.
- Si `is` es reflexivo: sí.
- Si los ciclos están permitidos: no.
- Si se hereda estado activo: no.
- Si los constructos concretos tienen estado propio: sí.

Esas decisiones pertenecen a [[notas/decisiones/ADR-014-ontologia-unificada-de-constructos|D-014]] y [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|D-015]].

La unidad distinguirá además entre la fusión del esquema de varios antecesores y la inicialización de un constructo raíz. [[notas/08-preguntas-abiertas#Q-045 — Contenido declarativo de create|Q-045]] ya está cerrada: el bloque de `create` es un cuerpo declarativo completo y puede añadir esquema local. También incorporará [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|D-017]]: si una propiedad no declara predeterminado explícito, recibe el de su tipo efectivo.

## Secuencia prevista

```text
camino de antecesores
→ campos declarados
→ esquema efectivo
→ conflictos de fusión
→ predeterminado efectivo
→ constructos con estado
→ posiciones válidas
→ store
→ buena formación
```

## Problemas que deberá resolver

### Identidad de campos

Un campo heredado desde la misma ancla debe deduplicarse. Dos campos homónimos de anclas distintas pueden necesitar fusión o producir conflicto.

### Predeterminado frente a estado

Un predeterminado pertenece al esquema. El valor actual pertenece al mundo. Distinguiremos el predeterminado explícito de una propiedad, el predeterminado de su tipo efectivo y una inicialización concreta. Una inicialización de `create` modifica el estado inicial de esa activación, pero no crea por sí misma un predeterminado heredable.

Todo tipo bien formado debe aportar:

$$
\operatorname{default}_P(\tau)
\in
\llbracket\tau\rrbracket_P
$$

La selección concreta para cada constructor de tipos permanece abierta en [[notas/08-preguntas-abiertas#Q-047 — Selección de predeterminados por tipo|Q-047]].

### Todo campo es una colección

La cardinalidad omitida equivale a `[1]`; no crea un caso escalar separado. Tanto los campos almacenados como los derivados producirán valores colección. La diferencia será si ese valor se almacena o se calcula.

Conforme a [[notas/decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|D-019]], estudiaremos por separado:

- Mutabilidad exterior: cambiar pertenencia, orden o multiplicidad.
- Capacidad interior: modificar los constructos alcanzados como miembros.

La cardinalidad `[1]` no fusiona ambos permisos.

### Store total o parcial

Compararemos:

$$
\operatorname{store}_W:
\mathcal K_{P,W}\times\mathcal F_P
\rightharpoonup
\mathcal V_P
$$

con una función total cuyo dominio contenga únicamente posiciones aplicables. No se elegirá entre ambas formas hasta justificar qué invariantes hace explícita cada una.

### Estados tentativos

Un mundo estable puede exigir valor para toda posición almacenada obligatoria. Quedará por estudiar si los estados internos de una inicialización se modelan como stores parciales o si solo aparecen dentro de una transición atómica.

## Reparto didáctico previsto

La responsabilidad será de nivel 1 a 2:

- Codex demostrará la derivación de un esquema efectivo sencillo.
- El autor definirá las posiciones válidas de una variación.
- Ambos compararán las dos representaciones del store.
- El autor construirá un contraejemplo contra la representación elegida.

## Entregables futuros

Cuando se active se crearán:

- `aprendizaje/ejercicios/03-esquema-y-estado-ejercicio.md`
- `aprendizaje/respuestas/03-esquema-y-estado-respuesta.md`

No se crean todavía para no presentar huecos cuya teoría depende de una unidad aún no revisada.
