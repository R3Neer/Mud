---
id: D-076
title: "Unidades nombradas, prefijos y escritura adyacente"
status: vigente
date: 2026-08-03
supersedes: []
superseded-by: []
questions: []
affects:
  - "magnitudes, unidades, léxico, nombres, anclas y tooling de edición"
---
# ADR-076 — Unidades nombradas, prefijos y escritura adyacente

- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]] y [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].

## Decisión

Toda unidad declara un identificador `lowerCamel` que participa en su ancla. D-087 integra la configuración de la unidad en el sistema general de metadatos: `~name: Name`, `~plural: Text`, `~abbreviation: Text` y `~prefixes: Prefix [* unique] = empty`. Ninguna de estas propiedades usa una producción sintáctica especial de unidad.

```mud
root unit meter {
    ~name = "meter"
    ~plural = "meters"
    ~abbreviation = "m"
    ~prefixes = all
}
```

Identificador, nombre, plural, abreviatura y formas prefijadas deben ser inequívocos dentro de una magnitud. Una colisión entre magnitudes se resuelve mediante el tipo esperado o cualificación como `Length.meter`; sin contexto suficiente es un error.

La forma contextual por identificador es válida y el tooling puede sugerir una abreviatura inequívoca más breve. Una sobrescritura de `~name` idéntica al predeterminado recibe sugerencia de eliminación. Los miembros de `family` usan igualmente el metadato estándar `~name` sin alterar su identidad.

### Prefijos

`Prefix` es un tipo nominal incorporado. Los nombres del catálogo SI (`quecto`, `ronto`, ..., `quetta`) son valores incorporados de tipo `Prefix`; se tokenizan como identificadores ordinarios y se resuelven en el nivel de incorporados, no como palabras reservadas nuevas.

`~prefixes` tiene tipo `Prefix [* unique]` y default de lenguaje `empty`. Por tanto, omitirlo y escribir `~prefixes = empty` admiten ninguno; `~prefixes = all` usa todos los valores incorporados de `Prefix`; una colección como `~prefixes = [kilo, milli]` selecciona exactamente ese subconjunto. Micro acepta `µ`, `μ` y `u` como entrada de forma de unidad y normaliza a `µ`. No existen prefijos binarios ni composición de prefijos.

El catálogo normativo es el siguiente. Los símbolos distinguen mayúsculas y minúsculas:

| Nombre | Símbolo canónico | Factor |
|---|---:|---:|
| `quecto` | `q` | 10^-30 |
| `ronto` | `r` | 10^-27 |
| `yocto` | `y` | 10^-24 |
| `zepto` | `z` | 10^-21 |
| `atto` | `a` | 10^-18 |
| `femto` | `f` | 10^-15 |
| `pico` | `p` | 10^-12 |
| `nano` | `n` | 10^-9 |
| `micro` | `µ` | 10^-6 |
| `milli` | `m` | 10^-3 |
| `centi` | `c` | 10^-2 |
| `deci` | `d` | 10^-1 |
| `deca` | `da` | 10^1 |
| `hecto` | `h` | 10^2 |
| `kilo` | `k` | 10^3 |
| `mega` | `M` | 10^6 |
| `giga` | `G` | 10^9 |
| `tera` | `T` | 10^12 |
| `peta` | `P` | 10^15 |
| `exa` | `E` | 10^18 |
| `zetta` | `Z` | 10^21 |
| `yotta` | `Y` | 10^24 |
| `ronna` | `R` | 10^27 |
| `quetta` | `Q` | 10^30 |

Las unidades prefijadas se elaboran estructuralmente y no reciben anclas adicionales. Los valores `Prefix` tampoco son declaraciones de unidad.

### Adyacencia y formato

El léxico acepta una unidad inmediatamente después del literal numérico:

```mud
3m
90km/h
r0.1m
```

La forma canónica inserta exactamente un espacio después del número y conserva compactos los productos y cocientes:

```mud
3 m
90 km/h
r0.1 m
```

El resaltador reconoce número y unidad como tokens distintos aun sin espacio. La edición inteligente y el formateador insertan el espacio; el mero resaltado nunca modifica el archivo.

Las cantidades con unidades pueden ser miembros de colecciones. Las declaraciones de unidad como valores de primera clase quedan fuera de MUD 1.0.

## Anclas

Una unidad usa una forma estable derivada de la magnitud y el identificador, por ejemplo:

```text
unit::physics.Length::meter
```

Cambiar metadatos no cambia el ancla; renombrar el identificador sí y requiere migración explícita.

## Verificación

1. Metadatos opcionales y colisiones locales o contextuales.
2. Catálogo SI completo y tres entradas de micro.
3. `empty`, `all` y subconjuntos de prefijos.
4. Literales adyacentes exactos, `Rum` y expresiones compuestas.
5. Normalización de espacios sin partir identificadores con dígitos.
6. Ancla estable y ausencia de anclas para unidades prefijadas.
