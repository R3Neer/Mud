---
id: D-019
title: "Mutabilidad ortogonal de colección y miembros"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "futuro `14-campos-y-mutabilidad.md`, futuro `15-colecciones.md`"
---
# ADR-019 — Mutabilidad ortogonal de colección y miembros

- Modificada por: [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]]
- Documentos afectados: futuro `14-campos-y-mutabilidad.md`, futuro `15-colecciones.md`

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
- El `mut` exterior califica un lugar almacenable, no el tipo de miembro: se escribe `mut nombre: Tipo`; `nombre: mut Tipo` es inválido.

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

Un campo derivado también produce semánticamente una colección, pero su pertenencia se recalcula a partir de su expresión. No admite mutabilidad exterior porque no existe una colección almacenada que escribir. Tampoco escribe un modificador `mut` propio: puede inferir capacidad interior desde su expresión cuando todos los miembros resultantes conservan autoridad suficiente. D-039 fija esta propagación para los operadores conjuntistas.

La capacidad interior nunca hace escribible la pertenencia de una colección derivada.

## Participantes `for`

Todo rol `for`, incluido el individual de cardinalidad `[1]`, conserva los mismos dos ejes. En una action:

```mud
mut patients: Person [1..10, unique, mut]
```

el primer `mut` permite cambiar la colección suministrada y el segundo permite modificar las `Person` miembro. La mutabilidad exterior vincula el rol por referencia a un lugar almacenado: el receptor de la llamada debe designar una colección exteriormente mutable. Un literal, una unión u otra colección calculada son valores y no pueden satisfacer ese contrato.

Sin `mut` exterior, el rol recibe el valor de cualquier expresión de colección compatible. La capacidad interior sigue comprobándose con independencia de que la colección proceda de un lugar o de una expresión. Cuando el tipo efectivo no contiene valores con estado modificable, escribir `[mut]` continúa siendo legal, pero el compilador sugiere retirarlo porque la capacidad no puede ejercerse. D-063 sustituye el rechazo anterior por esta sugerencia.

La mutabilidad exterior se aplica también a lugares que almacenan básicos, aliases, miembros de `family`, diccionarios o colecciones de esos valores. Permite sustituir o reorganizar el contenido, pero no vuelve mutables los valores contenidos:

```mud
mut observations: Number [*]
```

Reglas booleanas y `look` son puros y no admiten mutabilidad exterior en sus roles `for`. Los roles automáticos `on` continúan siendo individuales y solo pueden declarar capacidad interior sobre la `thing` vinculada. Los `given` no admiten ninguno de los dos permisos.

## Consecuencias

- Sustituir el único miembro de `[1]` es una mutación exterior.
- Modificar campos del único miembro exige capacidad interior.
- Una acción puede necesitar ambos permisos y debe declararlos de forma explícita.
- La omisión de `[1]` es únicamente azúcar de cardinalidad; no cambia permisos.
- El AST y el IR deben almacenar por separado `outerMutable` e `elementMutable`.
- La fusión hereditaria debe comparar ambos ejes independientemente.
- Una llamada con un rol `for` exteriormente mutable exige un receptor-lugar y conserva en el IR la referencia al destino escrito.

## Compatibilidad

Se retira cualquier interpretación que equipare las dos formas singulares. Antes de una versión estable no se requiere migración de programas publicados; los ejemplos internos deben interpretarse conforme a esta decisión.

## Verificación futura

La suite deberá comprobar las cuatro combinaciones de la tabla tanto para `[1]` como para cardinalidades múltiples, además de:

1. Rechazo de sustitución sin mutabilidad exterior.
2. Rechazo de modificación del miembro sin capacidad interior.
3. Ausencia de capacidad interior implícita en `mut field: T`.
4. Ausencia de mutabilidad exterior implícita en `field: T [mut]`.
5. Rechazo de `mut` exterior sobre un campo derivado.
6. Inferencia conservadora de capacidad interior en una colección derivada.
7. Roles `for` de cardinalidad `[1]` y colectiva con las cuatro combinaciones de capacidad.
8. Rechazo de un literal o resultado calculado como receptor de un rol exteriormente mutable.
9. Rechazo de mutabilidad exterior en reglas booleanas, `look` y roles `on`.
10. Mutabilidad exterior de una colección de valores inmutables sin capacidad interior.
11. Sugerencia para retirar una capacidad interior demostrablemente inútil sobre valores inmutables.
