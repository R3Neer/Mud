---
id: D-090
title: "Claves locales de entradas de diccionario sin anclas de rama"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "diccionarios exactos y decisionales, edición semántica, anclas, AST resuelto y dependencias"
---
# ADR-090 — Claves locales de entradas de diccionario sin anclas de rama

- Modifica: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].
- Amplía: [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].

## Contexto

Las asociaciones de un diccionario exacto son entradas estructurales identificables por su clave y nunca necesitaron identidad pública propia. D-085, en cambio, otorgó anclas a las ramas decisionales para que la edición del modelo pudiera localizarlas. Esa asimetría es innecesaria: direccionar una entrada dentro de su contenedor no exige convertirla en entidad nominal persistente.

## Decisión

### Entradas estructurales

Ni una asociación `key -> value` ni una rama `selector --> result` posee ancla pública, descriptor nominal independiente ni metadatos propios. Ambas forman parte del valor diccionario que las contiene.

La identidad local de una entrada se expresa mediante su clave dentro del diccionario:

- en un diccionario exacto, la clave ordinaria de la asociación;
- en un diccionario decisional, la representación canónica del selector;
- `_` es la clave especial única del fallback decisional.

Una clave local no pertenece al espacio global de anclas y no puede copiarse como sustituto de `~anchor`.

### Clave canónica decisional

La clave decisional depende **solo del selector**, nunca del resultado ni de la posición. Se obtiene de la forma canónica estructural del selector después de la normalización sintáctica necesaria para eliminar diferencias no semánticas de escritura. Whitespace, trivia y separadores numéricos no crean claves distintas cuando el AST superficial normalizado ya los ha eliminado.

MUD no exige demostrar equivalencia lógica para identificar claves. Dos selectores con formas canónicas distintas, como `value.age < 18` y `value.age <= 17`, siguen siendo claves distintas aunque en un dominio concreto pudieran coincidir extensionalmente.

Dentro de un mismo diccionario dos ramas no pueden tener la misma clave canónica. La restricción se aplica también en modo `ordered`. El fallback `_` puede aparecer como máximo una vez.

### Edición

Cambiar únicamente el resultado de una rama conserva su clave local. Cambiar el selector retira la entrada con la clave anterior y crea una entrada con la nueva.

`CREATE`, `UPDATE`, `REMOVE` y, en un decisional `ordered`, `MOVE` localizan una rama mediante el par conceptual `(diccionario, clave-canónica)`. `MOVE` cambia exclusivamente la posición y no altera la clave. Para indicar una posición relativa, las entradas vecinas se direccionan por sus propias claves locales.

La representación concreta del protocolo editorial puede serializar este par de otra manera, pero no lo eleva a ancla pública.

### Representación resuelta

El AST/IR puede conservar una `decision_branch_key` interna formada por el símbolo propietario del diccionario y el selector canónico. Ese identificador local sirve para dependencias y edición, pero no es `AnchoredSymbol` ni participa en migración de anclas.

## Consecuencias

- desaparece la categoría conceptual de «ancla de rama funcional»;
- las ramas continúan sin ser metadata-bearing;
- `MOVE` ya no se usa como argumento para fabricar identidad global;
- exactos y decisionales comparten el principio de «entrada direccionada por clave»;
- cambiar una condición decisional cambia la clave local de la entrada.

## Verificación

1. Ningún descriptor de rama expone `~anchor`.
2. Dos ramas con selector canónico idéntico se rechazan incluso en `ordered`.
3. Cambiar solo el resultado conserva la clave.
4. Cambiar el selector equivale a `REMOVE` + `CREATE` a efectos de identidad local.
5. `MOVE` conserva selector y clave.
6. El AST resuelto no usa `anchor` como identidad de una rama.
