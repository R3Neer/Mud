---
id: D-079
title: "Diagnóstico exterior de reglas `always`"
status: current
date: 2026-08-04
supersedes: []
superseded-by: []
questions: []
affects:
  - "reglas always, gramática, CST, AST, ejemplos y diagnósticos"
---
# ADR-079 — Diagnóstico exterior de reglas `always`

## Contexto

El diagnóstico `otherwise` de una regla `always` se escribía dentro de las llaves que contienen sus locales y su expresión final. Esa posición hacía parecer que el diagnóstico era otro elemento del bloque booleano y rompía la forma compartida por los diagnósticos de `if`, `after` y `then`.

## Decisión

El cuerpo entre llaves de una regla `always` contiene exclusivamente cero o más vinculaciones locales seguidas por una única expresión booleana final. Su `otherwise` opcional se escribe después de la llave de cierre:

```mud
always rule ValidPopulation on kingdom: Kingdom {
    population := kingdom.population
    population >= 0 people
}
otherwise "Population cannot be negative: {population}"
```

El diagnóstico sigue perteneciendo a la regla completa, se evalúa perezosamente solo cuando la invariante es falsa y puede resolver las vinculaciones locales del cuerpo. Un `otherwise` situado dentro de las llaves es inválido.

## Consecuencias

- `InvariantBodySyntax` deja de contener el diagnóstico.
- `AlwaysRuleDeclarationSyntax` conserva el `DiagnosticTailSyntax` opcional posterior al cuerpo.
- `AlwaysRuleDecl` no cambia: continúa almacenando por separado el bloque booleano y el diagnóstico opcional.
- Las reglas de terminadores continúan siendo uniformes; las llaves no convierten varias expresiones completas en una sola.

## Verificación

1. Regla con diagnóstico exterior en la misma línea y en la siguiente.
2. Regla sin diagnóstico y aviso correspondiente.
3. Rechazo de `otherwise` dentro del cuerpo.
4. Visibilidad de locales del cuerpo en el diagnóstico exterior.
