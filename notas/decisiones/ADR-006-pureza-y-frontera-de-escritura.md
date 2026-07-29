---
id: D-006
title: "Pureza de reglas booleanas y frontera de escritura"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "capítulos de reglas, acciones y API pública"
---

# ADR-006 — Pureza de reglas booleanas y frontera de escritura

## Contexto

Una consulta que modifica el mundo vuelve dependiente del orden de evaluación
la respuesta obtenida. Permitir escrituras externas fuera de operaciones
identificables también impide validar y revertir una mutación como unidad.

## Decisión

Las reglas booleanas son puras. Las modificaciones externas del mundo se
solicitan mediante acciones, que forman su API de escritura.

Las reglas reactivas y `always` participan en la resolución causal conforme a
sus contratos propios; no convierten una consulta booleana en una operación con
efectos.

## Consecuencias

D-041 precisa las tres clases de regla y D-042 desarrolla las acciones como
transacciones causales atómicas.

## Verificación

El análisis estático rechaza efectos en reglas booleanas y cualquier frontera
externa de escritura que no invoque una acción conforme.
