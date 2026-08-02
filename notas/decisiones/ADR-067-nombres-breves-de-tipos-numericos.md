---
id: D-067
title: "Nombres breves de los tipos numéricos"
status: vigente
date: 2026-08-02
supersedes: []
superseded-by: []
questions: []
affects:
  - "tipos numéricos incorporados, léxico, gramática concreta, ejemplos, diagnósticos y resaltado sintáctico"
---
# ADR-067 — Nombres breves de los tipos numéricos

- Modifica: [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]], [[notas/decisiones/ADR-034-number-exacto-y-rumber-binary64|D-034]], [[notas/decisiones/ADR-040-semantica-numerica-basica-restante|D-040]], [[notas/decisiones/ADR-050-comentarios-terminadores-y-separadores-numericos|D-050]] y [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]]
- Documentos afectados: tipos numéricos incorporados, léxico, gramática concreta, ejemplos, diagnósticos y resaltado sintáctico

## Contexto

Los nombres `Integer`, `Natural`, `Number` y `Rumber` procedían de terminología técnica inglesa y hacían especialmente largo el tipo de uso más frecuente. MUD está dirigido también a personas no programadoras y a la creación infantil de juegos; su vocabulario debe ser breve, reconocible y cómodo de escribir sin perder la distinción entre dominios numéricos.

`Money` ya expresa una idea cotidiana y no necesita abreviarse. El nombre `Rum` no colisiona con ninguna declaración vigente del lenguaje y la distinción entre mayúsculas y minúsculas permite seguir usando `rum` como identificador ordinario.

## Decisión

Los tipos numéricos incorporados se escriben:

| Nombre anterior | Nombre vigente | Dominio |
| --- | --- | --- |
| `Integer` | `Int` | Enteros con signo. |
| `Natural` | `Nat` | Enteros no negativos. |
| `Number` | `Num` | Números exactos ordinarios. |
| `Rumber` | `Rum` | Números de coma flotante `binary64`. |
| `Money` | `Money` | Cantidades monetarias exactas. |

`Int`, `Nat`, `Num`, `Rum` y `Money` son palabras reservadas y nombres de tipos incorporados sensibles a mayúsculas y minúsculas.

Las cuatro formas sustituidas dejan de ser palabras reservadas y no actúan como alias. Un programa que todavía las use como tipos debe recibir un diagnóstico de nombre no resuelto que sugiera la forma vigente cuando la intención resulte inequívoca.

Esta decisión cambia el vocabulario concreto, no los dominios, conversiones, operadores, literales ni reglas de normalización definidos para cada tipo.

## Consecuencias

- Las declaraciones y anotaciones resultan más breves.
- Solo existe un nombre canónico para cada tipo numérico.
- El cambio es incompatible en el nivel de fuente y exige sustituir las cuatro formas anteriores.
- La gramática, la documentación y las herramientas deben reconocer y mostrar los nombres vigentes.
- Los identificadores internos de herramientas pueden conservar nombres históricos cuando no sean visibles y su cambio rompa configuraciones existentes.

## Verificación

1. Reconocimiento de `Int`, `Nat`, `Num`, `Rum` y `Money` como tipos incorporados.
2. Rechazo de las cuatro formas anteriores como tipos incorporados.
3. Conservación de la semántica, los literales y las conversiones de cada dominio.
4. Resaltado de las cinco formas vigentes como tipos incorporados.
5. Diagnóstico de migración que sugiera el nombre vigente para cada forma anterior.
6. Ausencia de colisión entre el tipo `Rum` y un identificador ordinario `rum`.
