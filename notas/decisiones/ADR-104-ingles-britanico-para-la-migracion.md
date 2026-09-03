---
id: D-104
title: "Inglés británico para la migración editorial"
status: current
date: 2026-09-02
supersedes: []
superseded-by: []
questions: []
affects:
  - "notas/glosario-de-traduccion-es-en.md"
  - "README.md"
  - "LICENSE"
  - "TRADEMARKS.md"
  - "migración integral del contenido y de las rutas al inglés"
---

# ADR-104 — Inglés británico para la migración editorial

## Contexto

Mud comienza una migración editorial integral del español al inglés. Los
primeros documentos públicos en inglés y el glosario temporal ya establecen
parte del vocabulario que utilizará esa migración.

Sin una variedad de referencia, las traducciones independientes pueden mezclar
grafías y formas equivalentes, haciendo que el repositorio parezca incoherente
y que el glosario deje de ser una fuente fiable.

## Decisión

El inglés británico será la variedad canónica de toda la migración editorial de
Mud. La decisión se aplica al texto visible, títulos, metadatos traducidos,
glosarios, documentación pública y futuros nombres de archivo o carpeta que
sean palabras naturales.

En particular, se preferirán sistemáticamente formas como *behaviour*,
*modelling*, *materialisation*, *normalisation*, *stabilisation*,
*organisation* y *authorisation*.

Los identificadores, construcciones de Mud, extensiones, formatos,
dependencias, comandos, nombres propios externos y rutas sujetas a un contrato
técnico conservarán su grafía establecida. `LICENSE`, por ejemplo, sigue siendo
el nombre convencional del archivo aunque el sustantivo en la prosa sea
*licence*.

## Consecuencias

- El glosario temporal fija las formas británicas y las traducciones futuras
  deben consultarlo antes de automatizarse o revisarse.
- Los documentos ingleses ya publicados se corrigen para no introducir una
  excepción inicial.
- La revisión de cada lote de traducción debe detectar y resolver grafías
  estadounidenses accidentales, salvo en los elementos técnicos excluidos.
- Esta decisión no modifica la sintaxis de Mud ni traduce texto dentro de
  bloques de código o identificadores que formen parte de la especificación.

## Alternativas consideradas

- Inglés estadounidense: descartado por preferencia editorial del autor.
- Mezclar variantes según el documento o el traductor: descartado porque
  debilita la consistencia que debe garantizar el glosario.
