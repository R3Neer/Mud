# ADR-028 — Sistema de magnitudes y unidades

- Estado: Vigente
- Fecha: 2026-07-28
- Modificada por: [[notas/decisiones/ADR-034-number-exacto-y-rumber-binary64|D-034]]
- Preguntas relacionadas: Q-019, Q-034, Q-054, Q-055
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], futuro `10-sistema-de-tipos.md`, futuro `18-magnitudes.md`, futuro `19-expresiones.md`

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
```

Los tipos numéricos básicos son:

```mud
Natural
Integer
Number
Rumber
Money
```

Los cinco tipos numéricos son representaciones, no magnitudes. Pueden usarse directamente o ser la representación numérica de una magnitud:

```mud
attempts: Natural
factor: Number

magnitude Population: Natural {
    ...
}
```

`Percentage` deja de ser un tipo básico. Un concepto porcentual deberá modelarse mediante el sistema de magnitudes y dominios. D-034 fija `Number` como racional exacto y añade `Rumber` como representación aproximada `binary64`.

Los literales numéricos no llevan sufijos de tipo. No existen `30N`, `30I`, `30M` ni formas equivalentes. El contexto de tipado determina la representación exacta. Los literales `Rumber` puros constituyen una familia distinta con prefijo `r`, según D-034:

```mud
balance: Money = 30
population: Population = 30 people
rapid: Rumber = r0.1
```

### Magnitudes no derivadas

Una magnitud no derivada representa una cantidad independiente:

```mud
magnitude Length {
    ...
}
```

Si omite la representación numérica, usa `Number`. Puede declararla mediante `:`:

```mud
magnitude Population: Natural {
    ...
}

magnitude Temperature: Integer {
    ...
}
```

Puede restringir su dominio mediante `in`, situado después de la representación numérica opcional y antes del bloque:

```mud
magnitude Probability: Number in [0..1] {
    ...
}

magnitude Population: Natural in [*] {
    ...
}
```

Su cabecera sigue por tanto este orden:

```text
magnitude nombre [: representación-numérica] [in intervalo] bloque
```

Los límites del intervalo son números desnudos en la representación canónica de la magnitud. Cuando existe una unidad raíz, se interpretan en ella; la unidad no se escribe dentro del intervalo.

Una magnitud no derivada que declara unidades contiene exactamente una `root unit`. Las unidades no tienen identificador en su cabecera; sus formas léxicas se declaran dentro del bloque:

```mud
magnitude Length {
    root unit {
        name = "meter"
        plural = "meters"
        abbreviation = "m"
        prefixes
    }
}
```

`name` es obligatorio e identifica la unidad dentro de la magnitud. `plural`, `abbreviation` y `prefixes` son opcionales.

Una unidad alternativa se declara mediante una equivalencia positiva:

```mud
unit := 60 seconds {
    name = "minute"
    plural = "minutes"
    abbreviation = "min"
}
```

Toda equivalencia de unidad debe:

1. Ser estrictamente positiva.
2. Pertenecer a la misma magnitud.
3. Reducirse a la unidad raíz.
4. No participar en ciclos.

La ausencia de `prefixes` no habilita ninguno. `prefixes` habilita el catálogo incorporado completo y `prefixes = ...` habilita solo el subconjunto enumerado. El catálogo concreto y la resolución de colisiones permanecen en Q-054.

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
    unit := 1 m/s {
        name = "fastie"
        plural = "fasties"
        abbreviation = "fst"
    }
}
```

Esa unidad no se convierte en raíz ni restringe las demás expresiones compatibles.

### Inferencia de representación

Una magnitud derivada sin tipo explícito elige la representación menos ampliada capaz de representar la operación. Para la jerarquía ordinaria:

$$
\mathsf{Natural}
\prec
\mathsf{Integer}
\prec
\mathsf{Number}
$$

se aplican inicialmente estas reglas:

| Operación de representaciones | Resultado |
| --- | --- |
| `Natural * Natural` | `Natural` |
| `Natural * Integer` | `Integer` |
| `Integer * Integer` | `Integer` |
| Cualquier operación con `Number` | `Number` |
| Cualquier división | `Number` |

Puede declararse una representación explícita:

```mud
magnitude DiscreteArea: Natural :=
    Width * Height
```

La tabla describe operaciones exactas. Operaciones cuyos operandos sean todos `Rumber` producen `Rumber`; `Rumber` no se mezcla implícitamente con representaciones exactas. La inferencia de magnitudes derivadas que combinen componentes `Rumber` se completará en Q-058.

La anotación explícita no introduce redondeo. El programa debe satisfacer las reglas estáticas de representabilidad correspondientes. Las reglas de `Money` y la matriz completa de operadores permanecen abiertas en Q-019.

## Consecuencias

- El AST separará `NumericType`, `MagnitudeDecl`, `UnitDecl` y expresiones dimensionales.
- El análisis estático necesitará normalizar dimensiones y factores de escala.
- Las unidades derivadas son expresiones estructurales, no una enumeración nominal.
- El lexer y el resolvedor deberán distinguir nombres, plurales, abreviaturas y prefijos sin depender de un identificador de cabecera.
- `r` es un prefijo de literal aproximado.

## Verificación futura

1. Magnitud no derivada con representación predeterminada, explícita y dominio opcional en el orden canónico.
2. Rechazo de cero, signo negativo y ciclos en equivalencias.
3. Normalización de `km/h` a la unidad canónica de `Speed`.
4. Inferencia de cada combinación ordinaria de tipos numéricos.
5. Rechazo de `root unit` en una magnitud derivada.
6. Equivalencia entre una unidad nominal derivada y su expresión estructural.
