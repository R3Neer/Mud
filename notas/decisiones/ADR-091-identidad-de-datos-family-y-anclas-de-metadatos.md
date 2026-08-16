---
id: D-091
title: "Identidad de datos de `family` y anclas de metadatos"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "family, datos asociados, metadatos, anclas subordinadas, reflexión, gramática, CST y AST"
---
# ADR-091 — Identidad de datos de `family` y anclas de metadatos

- Modifica: [[ADR-038-familias-cerradas-de-valores|D-038]] y [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].
- Amplía: [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].

## Contexto

Los datos declarados por una `family` ya constituyen un esquema estable compartido por todos sus miembros, pero D-038 los describía sin identidad propia mientras el capítulo de anclas los agrupaba con la `family`. A la vez, D-087 introdujo valores reflectivos `Metadata` sin asignarles una identidad pública, pese a que tooling y reflexión necesitan poder referirse de forma estable a un metadato configurado concreto.

## Decisión

### Datos declarados de `family`

Cada dato almacenado o calculado declarado directamente en una `family` es un descriptor `Field` estable propiedad de esa `family`. Posee ancla pública subordinada:

```text
family::path.Family::field
```

Usa `FieldKind.Stored` o `FieldKind.Calculated` según corresponda, es siempre inmutable exteriormente y puede poseer metadatos configurados/de usuario mediante un cuerpo de metadatos inmediatamente unido a la declaración:

```mud
family Terrain {
    movementCost: Nat = 1 {
        ~summary = "Coste base de movimiento"
    }

    Plain,
    Mountain { movementCost = 4 }
}
```

El cuerpo del dato contiene exclusivamente declaraciones `~...` y no altera el valor del dato.

### Sobrescrituras por miembro

Una asignación `movementCost = 4` dentro de un miembro es únicamente la sobrescritura del valor efectivo del descriptor `movementCost` para ese miembro. No declara un nuevo `Field`, no posee ancla, no puede poseer metadatos y no crea una identidad `family::Family::Member::movementCost`.

El miembro sí conserva su propia ancla y sus propios metadatos. Por tanto `Mountain~summary` y `Terrain::movementCost~summary` describen entidades distintas, pero no existe un propietario metadata-bearing para la ocurrencia `Mountain.movementCost`.

### Anclas de `Metadata`

Todo metadato estándar configurado o metadato de usuario materializado como valor `Metadata` posee ancla propia. La grafía canónica concatena la ancla del propietario y el nombre de metadato mediante `~`:

```text
thing::game.Person~summary
thing::game.Person::health~description
family::game.Terrain::movementCost~summary
family::game.Terrain::Mountain~deprecated
```

`::` continúa navegando por entidades subordinadas; `~` entra en el espacio de metadatos del propietario. El nombre posterior a `~` es el `~identifier` del descriptor `Metadata`.

Las propiedades intrínsecas `~identifier`, `~anchor`, `~path`, `~file`, `~kind`, `~type` y demás propiedades reflectivas no se convierten por ello en objetos `Metadata` ni reciben una segunda ancla. Solo los valores que aparecen en `owner~metadata` como metadatos configurados o de usuario poseen esta identidad.

`Metadata` expone `~anchor: Anchor`. Esta decisión no añade por mera simetría `~path` ni `~file` al descriptor `Metadata`; esas propiedades solo se incorporarán si su semántica se especifica expresamente.

### Terminalidad

Un valor `Metadata` **no puede poseer metadatos propios**. Su ancla existe para referencia, reflexión y tooling, pero `Metadata` es un descriptor terminal y queda excluido explícitamente del conjunto metadata-bearing. No existe una cadena como `Person~summary~summary`.

## Consecuencias

- los datos de `family` dejan de ser una excepción de identidad y usan el mismo contrato `Field` almacenado/calculado;
- las sobrescrituras de miembro siguen siendo datos del valor, no declaraciones;
- toda metadata materializada tiene identidad estable sin confundirla con propiedades intrínsecas;
- el AST superficial de datos de `family` conserva sus asignaciones de metadatos;
- el AST resuelto de `Metadata` conserva su ancla pública.

## Verificación

1. Dato almacenado y calculado de `family` con ancla estable.
2. Metadata-body válido en una declaración de dato.
3. Rechazo de metadata-body unido a una sobrescritura de miembro.
4. `Field` reflectivo de un dato con `~kind`, `~owner`, `~anchor` y `~metadata` coherentes.
5. Anclas `owner~metadata` para estándar configurado y metadata de usuario.
6. Ausencia de anclas para propiedades intrínsecas.
7. Rechazo de metadata sobre un valor `Metadata`.
8. Una sobrescritura de miembro no crea `family::F::Member::field`.
