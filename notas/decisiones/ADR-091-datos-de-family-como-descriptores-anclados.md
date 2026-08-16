---
id: D-091
title: "Datos de family como descriptores anclados"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "family, datos asociados, metadatos, anclas, gramática, CST, AST superficial, AST resuelto, reflexión y tooling"
---

# ADR-091 — Datos de family como descriptores anclados

- Modifica: [[ADR-038-familias-cerradas-de-valores|D-038]].
- Precisa: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].
- Amplía: [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].

## Contexto

D-038 definió datos asociados uniformes para una `family` y afirmó que no poseían identidad propia, hablando de los valores proyectados por cada miembro. D-087 estableció después que los elementos metadata-bearing necesitan descriptor tipado y ancla pública estable. La especificación de anclas ya clasificaba los datos de `family` bajo la categoría `family`, pero la gramática y el AST superficial no permitían adjuntarles metadatos.

Existe además una contradicción previa entre D-038 y la EBNF sobre la forma exacta del dato calculado. D-091 no la resuelve; queda aislada en Q-061.

## Decisión

La declaración de un dato asociado almacenado o calculado es una entidad semántica estable del esquema uniforme de la `family`. Posee:

- descriptor reflectivo `Field`;
- `FieldKind.Stored` o `FieldKind.Calculated`;
- ancla subordinada `family::<nombre-cualificado>::<dato>`;
- secuencia propia de metadatos.

No se introduce `FamilyDataKind` ni una categoría de ancla nueva.

Un dato puede llevar inmediatamente un cuerpo formado exclusivamente por declaraciones `~...`:

```mud
family Terrain {
    movementCost: Nat = 1 {
        ~summary = "Coste base de movimiento"
    }
    costly := movementCost >= 3 {
        ~summary = "Indica terreno costoso"
    }

    Plain,
    Mountain {
        movementCost = 4
    }
}
```

El metadata-body pertenece al descriptor `movementCost` o `costly`, no al valor obtenido para `Plain`, `Mountain` u otro miembro. Consultar `Mountain.movementCost` produce el valor asociado; no crea un descriptor nuevo por miembro.

Una `family-data-assignment` dentro del cuerpo de un miembro es únicamente una sobrescritura del valor efectivo de un dato almacenado. No posee ancla, no admite metadata-body y no puede modificar los metadatos del dato declarado.

El metadata-body se añade después de la forma de declaración del dato calculado que resulte vigente. Esta decisión no determina si dicha forma debe admitir todo `derived-value-shape` o limitarse al tipo opcional descrito por D-038; Q-061 conserva esa elección abierta.

`~private` continúa sin ser válido en datos asociados de `family`: D-087 lo restringe a declaraciones de primer nivel compatibles y a campos pertenecientes a una `thing`.

## Consecuencias

- Renombrar un dato asociado cambia el ancla de su descriptor.
- Cambiar el valor de un miembro no cambia anclas ni metadatos.
- Los descriptores de datos participan en `~fields` y `~declaredFields` de la `family` como `Field`.
- `StoredFamilyDataDecl` y `CalculatedFamilyDataDecl` conservan `metadata_assignment* metadata`.
- `CalculatedFamilyDataDecl` conserva provisionalmente `derived_value_shape?` hasta resolver Q-061.
- `FamilyDataAssignment` permanece sin metadatos.

## Alternativas descartadas

### Descriptor independiente por miembro y dato

Descartado porque multiplicaría artificialmente entidades que comparten un único esquema y haría que una sobrescritura de valor pareciese una declaración.

### Nueva categoría reflectiva `FamilyData`

Descartada porque el contrato ya coincide con `Field` y `FieldKind`; añadir otra familia reflectiva no aporta una diferencia semántica.

### Permitir metadata-body en una sobrescritura de miembro

Descartado porque los metadatos describen el slot declarado, no una ocurrencia de su valor.

## Verificación

1. La EBNF admite metadata-body en ambos datos declarados y no lo admite en `family-data-assignment`.
2. CST, cobertura y proyección AST conservan el metadata-body en el descriptor sin cerrar Q-061.
3. El AST superficial almacena metadatos en ambos constructores de datos y no en `FamilyDataAssignment`.
4. La especificación de anclas identifica el descriptor bajo la categoría `family`.
5. D-038 distingue la identidad del descriptor de la ausencia de identidad runtime del valor proyectado.

## Cuestión abierta relacionada

[[notas/preguntas/Q-061-forma-de-datos-calculados-de-family|Q-061]] debe reconciliar la forma estrecha de D-038 con el `derived-value-shape` que hoy reconoce la EBNF. Nada en D-091 prejuzga esa resolución.
