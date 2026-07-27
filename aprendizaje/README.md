---
title: Aprendizaje de formalización de MUD
aliases:
  - Itinerario de formalización
tags:
  - mud/aprendizaje
  - mud/formalizacion
status: activo
---

# Aprendizaje de formalización de MUD

> [!abstract]
> Este espacio acompaña la creación de la especificación formal de MUD. Aquí se aprende a definir un lenguaje; la norma resultante vive en [[especificacion/README|Especificación formal de MUD]].

## Mapa

- [[REGLAS-DIDACTICAS|Contrato didáctico]]
- [[PERFIL|Perfil y audiencia]]
- [[PROGRESO|Progreso]]
- [[especificacion/00-convenciones-editoriales|Convenciones editoriales]]
- [[especificacion/README|Índice de la especificación]]

## Secuencia actual

1. [[aprendizaje/unidades/01-modelo-minimo-de-un-mundo|Unidad 01 — Modelo mínimo de un mundo]] — completada con rectificación.
2. [[aprendizaje/unidades/02-constructos-como-orden-parcial|Unidad 02 — Constructos como orden parcial]] — activa.
3. [[aprendizaje/unidades/03-esquema-heredable-y-estado-independiente|Unidad 03 — Esquema heredable y estado independiente]] — planificada.

## Método

El itinerario emplea una transferencia gradual de responsabilidad parecida a Assimil:

1. **Exposición**: Codex construye un ejemplo completo y comenta cada decisión.
2. **Imitación**: el autor completa variaciones pequeñas con apoyo.
3. **Construcción guiada**: ambos redactan partes distintas de una misma sección.
4. **Producción**: el autor escribe un borrador completo y Codex lo revisa.
5. **Autonomía**: el autor formaliza una característica nueva y defiende sus decisiones.

Cada unidad debe dejar dos resultados separados:

- Una capacidad adquirida por el autor.
- Un avance real y revisado de la especificación.

## Ciclo de una unidad

```text
motivación
→ teoría mínima
→ ejemplo completamente resuelto
→ lectura comentada
→ ejercicio de imitación
→ tarea de producción
→ revisión
→ incorporación a la especificación
→ repaso espaciado
```

## Principio central

> [!important]
> Ningún fragmento pasa a ser normativo solo porque parezca razonable. Primero debe entenderse, discutirse, comprobarse con ejemplos y registrarse como decisión cuando cierre una cuestión abierta.

## Organización

```text
aprendizaje/
├── unidades/       # Lecciones y planificación de unidades
├── ejercicios/     # Entregables sin solución
├── respuestas/     # Trabajo del autor
├── revisiones/     # Evaluación y correcciones
├── soluciones/     # Soluciones liberadas después del intento
├── repasos/        # Recuperación espaciada
└── glosario/       # Explicaciones reutilizables de conceptos
```

No es necesario crear todas las carpetas o soluciones de antemano. Se añadirán cuando una unidad las necesite.
