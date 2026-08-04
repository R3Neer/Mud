---
id: D-030
title: "Conversión cuantitativa explícita mediante `to`"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-019"
  - "Q-053"
affects:
  - "futuro `10-sistema-de-tipos.md`, futuro `18-magnitudes.md`, futuro `19-expresiones.md`"
---
# ADR-030 — Conversión cuantitativa explícita mediante `to`

- Preguntas relacionadas: Q-019, Q-053
- Ampliada por: [[notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal|D-032]]
- Modificada por: [[notas/decisiones/ADR-034-number-exacto-y-rumber-binary64|D-034]]
- Modificada además por: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Modificada después por: [[notas/decisiones/ADR-083-magnitudes-base-sin-unidades|D-083]]
- Documentos afectados: futuro `10-sistema-de-tipos.md`, futuro `18-magnitudes.md`, futuro `19-expresiones.md`

## Contexto

`as` queda reservado para declarar especialización de `thing`, por lo que no puede seguir expresando conversiones. MUD necesita distinguir el cambio de unidad de una cantidad de la conversión de su representación numérica.

## Decisión

`to` es el operador de conversión cuantitativa explícita:

```mud
value to Int
value to Nat
value to Money
value to Population
value to Price
```

Puede convertir:

1. Entre representaciones numéricas compatibles.
2. Una cantidad a una magnitud dimensionalmente compatible.
3. Una expresión cuantitativa más amplia a la representación declarada por la magnitud de destino.
4. Una expresión numérica básica a una magnitud base sin unidades, como materialización nominal explícita.

La cuarta forma, fijada por D-083, comprueba la compatibilidad de la representación y el dominio de destino. No permite convertir entre dos magnitudes nominales distintas por el mero hecho de que ninguna tenga unidad.

```mud
averagePopulation: Population :=
    population / regions to Population
```

En su rama cuantitativa, `to` no es un casting general. D-032 añade por separado el casting nominal de aliases estructuralmente compatibles. Continúan rechazándose conversiones como:

```mud
army to Kingdom
place to House
text to Num
distance to Time
Bool to Nat
```

### Redondeo y validación

Cuando la representación de destino no puede conservar una fracción, `to` aplica la única política global de redondeo de MUD. La sintaxis no permite seleccionar una política local:

```mud
value to Int
```

La política global, fijada por D-034, es redondeo al más cercano con empates al par (`roundTiesToEven`).

Después del redondeo, el resultado debe pertenecer al dominio de destino. `to` no satura ni corrige automáticamente un valor fuera de dominio.

`Num to Rum` redondea al valor `binary64` más cercano. `Rum to Num` recupera exactamente el racional representado por el valor binario almacenado. Ambas formas son explícitas.

### Diferencia respecto de `in`

`in` cambia la unidad con la que se expresa una cantidad, sin cambiar su magnitud:

```mud
distance in kilometers
speed in km/h
```

Se aplica tanto a magnitudes lineales como a magnitudes de punto. En una magnitud de punto transforma la coordenada completa y evita su `format`: si `time` representa las 13:30, `time in hour` expresa `13.5 h`, no el componente horario `13`.

La presentación seleccionada es observable al convertirla después a una representación numérica, interpolarla en `Text` o publicarla en un campo de `look` o `message`:

```mud
speed in km/h to Rum
"{distance in kilometer}"
```

Si ninguna operación posterior observa la presentación, el compilador puede sugerir retirar un `in` redundante. La extracción de una parte de un punto usa la forma distinta `picosecond from second in time`, fijada por D-061.

`to` cambia la representación numérica o materializa una magnitud cuantitativamente compatible:

```mud
average to Int
averagePopulation to Population
amount to Money
```

## Consecuencias

- El AST distingue `UnitPresentationExpr` de `QuantitativeConversionExpr`.
- El sistema de tipos debe probar compatibilidad numérica y dimensional antes de aceptar `to`.
- Una conversión inválida conocida estáticamente se diagnostica en compilación; una violación dependiente del valor deberá tener un resultado dinámico explícito todavía por integrar con la semántica general de fallos.
- `as` deja definitivamente de participar en conversiones.
- D-032 añade la rama nominal sin alterar estas reglas cuantitativas.

## Verificación futura

1. Ampliaciones y estrechamientos entre representaciones numéricas.
2. Conversión a una magnitud compatible.
3. Rechazo de dimensiones incompatibles.
4. Rechazo de valores fuera del dominio tras redondear.
5. Diferencia observable entre `quantity in unit` y `quantity to type`.
6. Presentación de una magnitud de punto en una unidad sin aplicar su `format`.
7. Materialización de una magnitud base sin unidades y rechazo entre magnitudes nominales distintas.
