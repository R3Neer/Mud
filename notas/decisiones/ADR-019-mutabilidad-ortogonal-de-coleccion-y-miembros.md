# ADR-019 — Mutabilidad ortogonal de colección y miembros

- Estado: Vigente
- Fecha: 2026-07-27
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], futuro `14-campos-y-mutabilidad.md`, futuro `15-colecciones.md`

## Contexto

Todo campo MUD se interpreta uniformemente como una colección con cardinalidad. La cardinalidad omitida equivale a `[1]`; no convierte el campo en una categoría semántica distinta.

MUD distingue dos permisos:

1. Cambiar la colección almacenada: añadir, retirar, sustituir o reordenar miembros.
2. Modificar las `thing` alcanzadas como miembros de la colección.

La formulación previa sugería una excepción para cardinalidad singular por la que:

```mud
mut capital: City [1]
```

podía interpretarse como:

```mud
capital: City [1 mut]
```

Esa equivalencia colapsaba dos permisos distintos precisamente en el caso `[1]`.

## Decisión

Los dos ejes son ortogonales para toda cardinalidad, incluida `[1]`.

- `mut` antes del nombre concede mutabilidad exterior de la colección almacenada.
- `mut` dentro de la especificación de cardinalidad concede capacidad interior sobre sus miembros.
- Ninguna posición implica la otra.
- No existe una excepción para campos singulares.

| Declaración | Cambiar colección | Modificar miembros |
| --- | --- | --- |
| `capital: City [1]` | No | No |
| `mut capital: City [1]` | Sí | No |
| `capital: City [1 mut]` | No | Sí |
| `mut capital: City [1 mut]` | Sí | Sí |

La cardinalidad omitida mantiene exactamente la misma regla:

```mud
mut capital: City
capital: City [mut]
```

equivalen, respectivamente, a:

```mud
mut capital: City [1]
capital: City [1 mut]
```

La primera forma no equivale a la segunda: omitir `[1]` no desplaza `mut` entre los dos ejes.

## Campos almacenados y derivados

Un campo almacenado posee un valor colección cuya estructura solo puede cambiar cuando declara mutabilidad exterior.

Un campo derivado también produce semánticamente una colección, pero su pertenencia se recalcula a partir de su expresión. No admite mutabilidad exterior porque no existe una colección almacenada que escribir. Puede declarar capacidad interior si el lenguaje permite modificar sus miembros a través de esa vista.

La capacidad interior nunca hace escribible la pertenencia de una colección derivada.

## Consecuencias

- Sustituir el único miembro de `[1]` es una mutación exterior.
- Modificar campos del único miembro exige capacidad interior.
- Una acción puede necesitar ambos permisos y debe declararlos de forma explícita.
- La omisión de `[1]` es únicamente azúcar de cardinalidad; no cambia permisos.
- El AST y el IR deben almacenar por separado `outerMutable` e `elementMutable`.
- La fusión hereditaria debe comparar ambos ejes independientemente.

## Compatibilidad

Se retira cualquier interpretación que equipare las dos formas singulares. Antes de una versión estable no se requiere migración de programas publicados; los ejemplos internos deben interpretarse conforme a esta decisión.

## Verificación futura

La suite deberá comprobar las cuatro combinaciones de la tabla tanto para `[1]` como para cardinalidades múltiples, además de:

1. Rechazo de sustitución sin mutabilidad exterior.
2. Rechazo de modificación del miembro sin capacidad interior.
3. Ausencia de capacidad interior implícita en `mut field: T`.
4. Ausencia de mutabilidad exterior implícita en `field: T [mut]`.
5. Rechazo de `mut` exterior sobre un campo derivado.
