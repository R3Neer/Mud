---
id: D-090
title: "Ramas funcionales sin ancla pública"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "diccionarios funcionales, anclas, IR semántico, grafo de dependencias, operador semántico y tooling"
---

# ADR-090 — Ramas funcionales sin ancla pública

- Modifica: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].
- Precisa: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].
- Amplía: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].

## Contexto

D-085 asignaba anclas propias a las ramas de diccionarios funcionales para poder editarlas de forma independiente. D-087 fijó después un principio más estricto: una entidad metadata-bearing necesita descriptor tipado y ancla pública estable, y excluyó expresamente las ramas funcionales por carecer de descriptor estable. Mantener una ancla pública de rama conservaría dos modelos de identidad incompatibles.

## Decisión

Una rama de diccionario funcional no posee ancla pública, no introduce `AnchoredSymbol` y no puede poseer metadatos propios. La entidad persistente es el diccionario propietario.

El IR semántico asigna a cada rama una clave local `decision_branch_key`:

```text
SelectorBranchKey(canonical_selector)
FallbackBranchKey
```

`canonical_selector` es la forma canónica del selector después de resolución y normalización semántica suficiente para reconstruir la rama. Dentro de un mismo diccionario no pueden existir dos ramas ordinarias con el mismo selector canónico: la parte izquierda actúa como clave estructural local. El fallback `_` usa una variante propia y única por diccionario.

La variante de `decision_branch_key` determina por sí sola si la rama es ordinaria o fallback; el IR semántico no conserva un segundo flag `is_fallback` que pudiera contradecirla. El `source_ordinal` continúa conservándose por separado. En `FirstMatch` forma parte del valor funcional porque decide prioridad; en `AllMatches` conserva procedencia y diagnóstico, pero no se convierte en identidad persistente.

Las dependencias de una rama se representan mediante el par formado por el ancla del diccionario propietario y su clave local. Una operación externa que necesite persistencia se dirige al diccionario y expresa la edición de sus ramas como estructura interna del propietario; no puede tratar la rama como entidad global independiente.

## Consecuencias

- Se elimina la contradicción entre D-085 y el principio de admisión de D-087.
- Mover una rama ordenada puede cambiar semántica sin requerir migración de ancla.
- Cambiar el selector puede cambiar la clave local sin constituir un renombrado de entidad pública.
- Dos selectores canónicamente iguales dentro del mismo diccionario son inválidos porque representarían la misma clave estructural local.
- Las operaciones conjuntistas de diccionarios funcionales siguen siendo extensionales y no fusionan identidad de ramas.

## Alternativas descartadas

### Mantener anclas subordinadas por posición

Descartada porque reordenar ramas de `FirstMatch` cambiaría identidad además de semántica y porque D-087 excluye la rama como entidad con descriptor estable.

### Permitir selectores canónicamente duplicados mediante un índice local

Descartada porque la rama ya posee una clave estructural natural: su selector canónico. Introducir un índice permitiría dos entradas con la misma clave y haría depender las operaciones editoriales de una distinción que no existe en el modelo del diccionario.

## Verificación

1. `especificacion/ir/mud-semantic-ir.asdl` no representa la identidad de `ResolvedDecisionBranch` mediante `anchor`.
2. `ResolvedDecisionBranch` no duplica la condición de fallback mediante un flag separado.
3. `DecisionDependsOn` conserva el ancla del diccionario y una clave local de rama sin índice de colisión.
4. El catálogo de anclas no enumera ramas funcionales como entidades públicas.
5. D-085 ya no promete `CREATE`, `UPDATE`, `REMOVE` o `MOVE` dirigidos a una ancla de rama.
6. D-087 mantiene las ramas fuera de la superficie metadata-bearing.
