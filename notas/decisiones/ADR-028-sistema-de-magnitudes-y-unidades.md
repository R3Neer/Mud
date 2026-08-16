---
id: D-028
title: "Sistema de magnitudes y unidades"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-019"
  - "Q-034"
  - "Q-054"
  - "Q-055"
affects:
  - "futuro `10-sistema-de-tipos.md`, futuro `18-magnitudes.md`, futuro `19-expresiones.md`"
---
# ADR-028 — Sistema de magnitudes y unidades

- Modificada por: [[notas/decisiones/ADR-034-number-exacto-y-rumber-binary64|D-034]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]] y [[notas/decisiones/ADR-083-magnitudes-base-sin-unidades|D-083]]
- Ampliada por: [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]]
- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]
- Preguntas relacionadas: Q-019, Q-034, Q-054, [[notas/preguntas/Q-055-literales-de-magnitudes-de-punto|Q-055]]
- Documentos afectados: futuro `10-sistema-de-tipos.md`, futuro `18-magnitudes.md`, futuro `19-expresiones.md`

## Contexto

La referencia inicial mezclaba representación numérica, dimensión, unidad y sintaxis léxica. También trataba `Percentage` como tipo básico, usaba sufijos para algunos tipos y exigía declarar manualmente unidades compuestas que pueden deducirse dimensionalmente.

MUD necesita distinguir:

- Cómo se representa un número.
- Qué cantidad física o conceptual representa.
- En qué unidad se escribe.
- Qué dimensión resulta de combinar cantidades.

## Decisión

### Tipos básicos

Los tipos básicos no numéricos son:

```mud
Text
Bool
Char
```

Los tipos numéricos básicos son:

```mud
Nat
Int
Num
Rum
Money
```

Los cinco tipos numéricos son representaciones, no magnitudes. Pueden usarse directamente o ser la representación numérica de una magnitud:

```mud
attempts: Nat
factor: Num

magnitude Population: Nat {
    ...
}
```

`Percentage` deja de ser un tipo básico. Un concepto porcentual deberá modelarse mediante el sistema de magnitudes y dominios. D-034 fija `Num` como racional exacto y añade `Rum` como representación aproximada `binary64`.

Los literales numéricos no llevan sufijos de tipo. No existen `30N`, `30I`, `30M` ni formas equivalentes. El contexto de tipado determina la representación exacta. Los literales `Rum` puros constituyen una familia distinta con prefijo `r`, según D-034:

```mud
balance: Money = 30
population: Population = 30 people
rapid: Rum = r0.1
```

### Magnitudes no derivadas

Una magnitud no derivada representa una cantidad independiente:

```mud
magnitude Length {
    ...
}
```

Si omite la representación numérica, usa `Num`. Puede declararla mediante `:`:

```mud
magnitude Population: Nat {
    ...
}

magnitude Temperature: Int {
    ...
}
```

Puede restringir su dominio mediante `in`, situado después de la representación numérica opcional y antes del bloque:

```mud
magnitude Probability: Num in [0..1] {
    ...
}

magnitude Population: Nat in [*] {
    ...
}
```

Su cabecera sigue por tanto este orden:

```text
magnitude nombre [: representación-numérica] [in intervalo] bloque
```

Los límites del intervalo de la cabecera son números desnudos en la representación canónica de la magnitud. Cuando existe una unidad raíz, se interpretan en ella; la unidad no se escribe dentro del intervalo. Esta restricción de declaración no impide que las expresiones ordinarias de intervalo usen unidades locales o una unidad común conforme a D-059.

Una magnitud no derivada que declara unidades contiene exactamente una `root unit`. D-076 exige un identificador `lowerCamel` en su cabecera:

```mud
magnitude Length {
    root unit meter {
        ~name = "meter"
        ~plural = "meters"
        ~abbreviation = "m"
    }
}
```

El identificador determina `~identifier` y participa en el ancla de la unidad. `~name`, `~plural`, `~abbreviation` y `~prefixes` son metadatos estándar opcionales conforme a D-076/D-087; omitirlos no altera la identidad nominal.

Una unidad alternativa se declara mediante una equivalencia positiva:

```mud
unit minute := 60 seconds {
    ~name = "minute"
    ~plural = "minutes"
    ~abbreviation = "min"
}
```

Toda equivalencia de unidad debe:

1. Ser estrictamente positiva.
2. Pertenecer a la misma magnitud.
3. Reducirse a la unidad raíz.
4. No participar en ciclos.

La ausencia del metadato `~prefixes` no habilita prefijos. `~prefixes = empty` es equivalente, `~prefixes = all` habilita el catálogo decimal SI completo y `~prefixes = [p1, p2, ...]` habilita solo el subconjunto enumerado. La forma desnuda `~prefixes` no es válida.

### Magnitudes derivadas

`:=` define una relación dimensional, no herencia ni conversión:

```mud
magnitude Speed :=
    Length / Time

magnitude Area :=
    Length * Length
```

Una magnitud derivada no puede declarar `root unit`. Su unidad canónica se obtiene combinando las unidades raíz de las magnitudes componentes. Las expresiones de unidad dimensionalmente compatibles son válidas automáticamente:

```mud
10 m/s
90 km/h
3 Mm/ps
5 cm/min
```

Los prefijos habilitados en las unidades componentes siguen disponibles en esas expresiones. No es necesario declarar cada producto o cociente nominalmente.

Una magnitud derivada puede añadir una forma nominal para una equivalencia que ya sea dimensionalmente válida:

```mud
magnitude Speed :=
    Length / Time
{
    unit fastie := 1 m/s {
        ~name = "fastie"
        ~plural = "fasties"
        ~abbreviation = "fst"
    }
}
```

Esa unidad no se convierte en raíz ni restringe las demás expresiones compatibles.

### Inferencia de representación

Una magnitud derivada sin tipo explícito elige la representación menos ampliada capaz de representar la operación. Para la jerarquía ordinaria:

$$
\mathsf{Nat}
\prec
\mathsf{Int}
\prec
\mathsf{Num}
$$

se aplican inicialmente estas reglas:

| Operación de representaciones | Resultado |
| --- | --- |
| `Nat * Nat` | `Nat` |
| `Nat * Int` | `Int` |
| `Int * Int` | `Int` |
| Cualquier operación con `Num` | `Num` |
| Cualquier división | `Num` |

Puede declararse una representación explícita:

```mud
magnitude DiscreteArea: Nat :=
    Width * Height
```

La tabla describe operaciones exactas. Operaciones cuyos operandos sean todos `Rum` producen `Rum`; `Rum` no se mezcla implícitamente con representaciones exactas. La inferencia de magnitudes derivadas que combinen componentes `Rum` se completará en Q-058.

La anotación explícita no introduce redondeo. El programa debe satisfacer las reglas estáticas de representabilidad correspondientes. Las reglas de `Money` y la matriz completa de operadores permanecen abiertas en Q-019.

## Consecuencias

- El AST separará `NumericType`, `MagnitudeDecl`, `UnitDecl` y expresiones dimensionales.
- El análisis estático necesitará normalizar dimensiones y factores de escala.
- Las unidades derivadas son expresiones estructurales, no una enumeración nominal.
- La clasificación contextual y la resolución distinguen el identificador de unidad de sus metadatos de presentación, abreviación y prefijos bajo el contexto de magnitud.
- `r` es un prefijo de literal aproximado.

## Verificación futura

1. Magnitud no derivada con representación predeterminada, explícita y dominio opcional en el orden canónico.
2. Rechazo de cero, signo negativo y ciclos en equivalencias.
3. Normalización de `km/h` a la unidad canónica de `Speed`.
4. Inferencia de cada combinación ordinaria de tipos numéricos.
5. Rechazo de `root unit` en una magnitud derivada.
6. Equivalencia entre una unidad nominal derivada y su expresión estructural.
7. Ningún prefijo por omisión o `~prefixes = empty`, catálogo completo mediante `~prefixes = all` y subconjunto mediante una colección explícita.
