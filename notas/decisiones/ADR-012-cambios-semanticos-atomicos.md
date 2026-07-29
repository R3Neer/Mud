---
id: D-012
title: "Validación y versionado atómico de cambios semánticos"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-008"
  - "Q-015"
affects:
  - "gobierno/POLITICA-DE-COMMITS.md"
  - "flujo de autoría del operador semántico"
---

# ADR-012 — Validación y versionado atómico de cambios semánticos

## Contexto

Una modificación de la fuente puede afectar varias anclas y derivados. Publicar
solo una parte, confirmar un cambio inválido o incluir trabajo ajeno destruye la
correspondencia entre intención, modelo e historial.

## Decisión

Cada cambio semántico válido se prepara, analiza, aplica, valida y versiona como
una unidad atómica. Un fallo anterior a la confirmación no publica un estado
parcial. El commit incluye únicamente los archivos pertenecientes al cambio.

Una consulta `READ` pura no crea commit porque no modifica estado.

## Consecuencias

D-053 desarrolla el flujo del operador. La política de commits gobierna la
atomicidad y el tratamiento de cambios previos del repositorio.
