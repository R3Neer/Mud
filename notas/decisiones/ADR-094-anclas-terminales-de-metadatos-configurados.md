---
id: D-094
title: "Anclas terminales de metadatos configurados"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "metadatos, reflexión, anclas subordinadas, representación semántica posterior a tipado y elaboración, grafo y tooling"
---

# ADR-094 — Anclas terminales de metadatos configurados

- Precisa: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].
- Amplía: [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]] y [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].

## Decisión

Cada metadato configurado o definido por el autor que se materializa como valor `Metadata` posee una ancla pública subordinada a la de su propietario. La grafía canónica usa el mismo separador `~` del acceso reflectivo:

```text
<ancla-del-propietario>~<identificador-metadata>
```

Ejemplos:

```text
thing::game.Person~summary
thing::game.Person::health~description
family::game.Status::Critical~deprecated
family::game.Status::score~summary
action::game.Attack::for::attacker~summary
```

`::` continúa navegando por entidades semánticas subordinadas; `~` entra en el espacio de metadata del propietario. El identificador posterior a `~` es la forma canónica del nombre del metadato y no introduce una categoría superior `metadata`.

Las propiedades intrínsecas como `~type`, `~path`, `~file`, `~kind` o el propio `~anchor` no son objetos `Metadata`, no aparecen en `~metadata` y no reciben una ancla de metadata. Un acceso intrínseco sigue siendo reflectivo, pero su existencia no materializa un descriptor configurable.

`Metadata` expone `~anchor: Anchor`, `~path: MudPath` y `~file: MudFile`. `~path` es el path lógico de la entidad propietaria dentro del programa: entrar en el espacio terminal `~<metadata>` no crea un namespace distinto. `~file` identifica el archivo físico en el que está declarada esa configuración de metadata; en una declaración directa coincide normalmente con el archivo del propietario, pero se deriva de la procedencia del propio `Metadata` y no de una copia almacenada del valor del propietario.

Estas tres propiedades son intrínsecas y calculadas del descriptor. No aparecen en `~metadata`, no materializan nuevos objetos `Metadata` y no requieren campos redundantes en el IR cuando puedan derivarse de ancla, propietario y procedencia.

## Terminalidad

`Metadata` es un descriptor terminal. Aunque sea una entidad estable y anclada, **no puede poseer metadata propia** y no expone `~metadata`. Esta es una excepción deliberada al principio general de admisión de D-087 y evita una torre recursiva `owner~meta~meta...`.

## IR y resolución

La resolución deriva la ancla del objeto `Metadata` a partir de la ancla resuelta del propietario y del identificador canónico del metadato. No aparece sintaxis fuente nueva ni cambia el AST superficial.

El IR distingue:

- `metadata_kind`: categoría de objetos `Metadata` configurados;
- `metadata_property`: propiedad postfix elaborada, que puede ser intrínseca o referir un `metadata_kind` configurable.

Una propiedad intrínseca nunca se convierte accidentalmente en `SemanticMetadata`.

## Consecuencias

- Los objetos `Metadata` pueden ser referenciados de forma estable por tooling y grafo.
- Renombrar un metadato de usuario cambia su ancla; cambiar su valor no.
- Renombrar/mover el propietario cambia también la ancla subordinada del metadato conforme a la migración ordinaria de anclas.
- La metadata de un miembro de `family` posee ancla bajo el miembro; la sobrescritura de un dato de `family` sigue sin ser un descriptor y no puede poseer metadata.

## Verificación

1. `SemanticMetadata` conserva una ancla propia.
2. `thing::game.Person::health~description` es una ancla válida de metadata configurada.
3. Ninguna propiedad intrínseca aparece como objeto `Metadata` ni recibe ancla de metadata.
4. El descriptor `Metadata` expone `~anchor`, `~path` y `~file` y no expone `~metadata`.
5. `Metadata~path` conserva el path lógico del propietario y `Metadata~file` conserva la procedencia física de la declaración de metadata.
6. El AST superficial no cambia por esta decisión.
