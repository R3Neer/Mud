# ADR-039 — Colecciones y diccionarios

- Estado: Vigente
- Fecha: 2026-07-28
- Amplía: D-019, D-026, D-033
- Preguntas relacionadas: Q-006, Q-047
- Documentos afectados: futuro `15-colecciones.md`, futuro `16-diccionarios.md`, futuro `20-cuantificadores-e-iteracion.md`

## Decisión

### Colecciones

La cardinalidad usa intervalos de naturales:

```mud
T[n]
T[min..max]
T[min..*]
T[*]
```

Omitirla equivale a `[1]`; `[n]` equivale a `[n..n]`; `[*]` usa la semántica de límite efectivo de D-029 y normalmente equivale a `[0..*]`.

`empty` representa ausencia sin `null`.

Las colecciones admiten duplicados salvo `unique`. `ordered` conserva un orden observable y `ordered by expression` declara una clave semántica.

Fuentes iniciales de orden:

- Básicos: orden de su tipo.
- `thing`: orden de inserción cuando la colección es `ordered`.
- Familias `ordered values`: orden declarado.
- Alias ordenado: orden subyacente o lexicográfico.

La consolidación simultánea de inserciones con orden observable deberá integrarse en la matriz de Q-006.

### Diccionarios

La forma:

```mud
Key -> Value [cardinality modifiers]
```

declara un diccionario con claves únicas. `unique` no se aplica porque la unicidad de clave es intrínseca.

```mud
stock =
    Grain -> 2_000,
    Bronze -> 500
```

Asignar una clave sustituye su valor; escribir una clave ausente materializa la entrada si tipo, dominio, capacidad y cardinalidad lo permiten; retirar una clave ausente es no-op.

Leer una clave ausente produce el predeterminado del tipo de valor cuando la lectura exige un valor. D-017 y Q-047 gobiernan la existencia y selección de ese predeterminado. Los contextos que preserven ausencia deberán hacerlo mediante cardinalidad, no mediante `null`.

El acceso encadenado solo es válido cuando el resultado intermedio es otro diccionario.

### Orden e iteración

Un diccionario `ordered` recorre claves según su orden canónico. Puede recorrerse por claves o por pares `(key, value)`.

Un alias estructural puede actuar como una única clave compuesta y usar el azúcar definido en D-033:

```mud
board[(E, Four)]
board[E, Four]
```

### Igualdad

- Colección ordenada: misma secuencia y multiplicidad.
- Colección no ordenada: mismo multiconjunto.
- Diccionario: mismas asociaciones clave–valor; el orden de almacenamiento no altera igualdad.

## Consecuencias

- Cardinalidad, orden, unicidad y mutabilidad son ejes separados.
- Los diccionarios no exponen `null`.
- La iteración no depende del hash o estructura interna del materializador.
- Las operaciones de colección y diccionario deben ser totales donde esta decisión lo indica.

## Verificación futura

1. Cardinalidad omitida y `empty`.
2. Duplicados y `unique`.
3. Orden natural, de inserción, semántico y `ordered by`.
4. Lectura, escritura y retirada de clave ausente.
5. Igualdad independiente de representación interna.
6. Clave alias ordinaria y azucarada.
