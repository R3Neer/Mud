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

Añadir a una colección `unique` un valor que ya está presente es un no-op. La operación es idempotente: una o varias adiciones del mismo valor producen una sola presencia, también cuando proceden de efectos concurrentes compatibles.

Cuando un literal destinado a una colección `unique` contiene duplicados cuya igualdad puede demostrarse estáticamente, el compilador los normaliza a una sola presencia y emite un aviso no bloqueante. Si la colección normalizada incumple su cardinalidad, el programa contiene además un error estático de cardinalidad y no es válido:

```mud
members: Person [* unique] = [Alice, Alice]  # aviso; equivale a [Alice]
pair: Person [2 unique] = [Alice, Alice]     # error; tras normalizar solo queda un valor
```

Fuentes iniciales de orden:

- Básicos: orden de su tipo.
- `Character`: valor escalar Unicode creciente; `ordered by` está prohibido.
- `thing`: orden de inserción cuando la colección es `ordered`.
- `ordered family`: orden declarado.
- Alias ordenado: orden subyacente o lexicográfico.

En una colección de `ordered family`, `ordered by expression` puede sustituir el orden declarado por una clave calculada a partir de los datos asociados de cada miembro. Durante la evaluación de la clave, los nombres no cualificados de esos datos se resuelven sobre el miembro actual. La clave debe tener orden semántico total y el orden declarado de la familia desempata claves iguales. Este orden de colección no modifica la comparación intrínseca entre miembros de la familia.

Cuando el tipo o `ordered by expression` determina un orden canónico, un literal escrito en otro orden se normaliza y produce un aviso no bloqueante. Este aviso no se aplica a una colección `thing [ordered]` ordenada por inserción: en ella el orden escrito es el orden elegido por el autor.

`Text` no equivale a `Character [* ordered]`: conserva el orden posicional de sus caracteres y no admite modificadores de colección. D-056 fija esta distinción.

La consolidación simultánea de inserciones distintas con orden observable deberá integrarse en la matriz de Q-006.

### Diccionarios

La forma:

```mud
Key -> Value [cardinality modifiers]
```

declara un diccionario con claves únicas. `unique` no se aplica porque la unicidad de clave es intrínseca y escribirlo es un error estático. Tampoco se reinterpreta como unicidad de valores: esa restricción debe expresarse, si se incorpora en el futuro, mediante una construcción distinta y explícita.

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

## Alternativa descartada

### Unicidad predeterminada

Se descarta hacer `unique` implícito, tanto para todas las colecciones como en función del tipo de miembro. La multiplicidad es información observable y necesaria en colecciones como `Number [*]`; eliminarla de manera predeterminada cambiaría el significado de datos que representan observaciones, tiradas o frecuencias. Un valor predeterminado dependiente del tipo haría además que una misma forma de colección cambiara de semántica entre código genérico, aliases y conversiones.

La regla uniforme es que la ausencia de `unique` conserva multiplicidad y su presencia impone una sola ocurrencia por valor.

## Verificación futura

1. Cardinalidad omitida y `empty`.
2. Duplicados, normalización, aviso e idempotencia de `unique`.
3. Orden natural, de inserción, semántico y `ordered by`, incluida una `ordered family` ordenada por dato asociado y con aviso solo para órdenes canónicos.
4. Lectura, escritura y retirada de clave ausente.
5. Igualdad independiente de representación interna.
6. Clave alias ordinaria y azucarada.
