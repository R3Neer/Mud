---
id: D-034
title: "`Num` exacto y `Rum` binary64"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-019"
  - "Q-058"
affects:
  - "futuro `06-lexico.md`, futuro `10-sistema-de-tipos.md`, futuro `17-dominios-e-intervalos.md`, futuro `18-magnitudes.md`, futuro `19-expresiones.md`, futuro `20-cuantificadores-e-iteracion.md`"
---
# ADR-034 — `Num` exacto y `Rum` binary64

- Modifica: [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]]
- Preguntas relacionadas: Q-019, Q-058
- Sintaxis actualizada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]
- Documentos afectados: futuro `06-lexico.md`, futuro `10-sistema-de-tipos.md`, futuro `17-dominios-e-intervalos.md`, futuro `18-magnitudes.md`, futuro `19-expresiones.md`, futuro `20-cuantificadores-e-iteracion.md`

## Contexto

Un único tipo general de número no puede ofrecer a la vez:

- Igualdad decimal intuitiva y aritmética exacta.
- Rendimiento directo de coma flotante para simulación.
- Visibilidad sintáctica de cuándo se acepta aproximación.

MUD separa esas necesidades. `Num` es el tipo general predeterminado y exacto; `Rum`, abreviatura de *rapid number*, es una elección explícita de aritmética aproximada.

## Decisión

### `Num`

`Num` denota el conjunto de los números racionales:

$$
\llbracket\mathsf{Num}\rrbracket=\mathbb Q
$$

Cada valor posee una representación canónica:

$$
\frac{n}{d}
\qquad
n\in\mathbb Z
\quad
d\in\mathbb N_{>0}
$$

tal que:

$$
\gcd(|n|,d)=1
$$

El denominador es siempre positivo y cero se representa como $0/1$.

Las operaciones son exactas mientras su resultado sea racional. En contexto `Num`, en particular:

```mud
0.1 + 0.2 == 0.3
1 / 3 * 3 == 1
1 == 1.0
```

son verdaderas.

La semántica no usa coma flotante binaria. Una implementación puede comenzar con enteros nativos, pero debe promover a enteros de precisión arbitraria antes de que ocurra desbordamiento observable. Los límites de recursos pertenecen a la taxonomía de fallos técnicos, no al dominio matemático de `Num`.

### `Rum`

`Rum` representa valores aproximados con formato IEEE 754 `binary64`. Una materialización puede usar el flotante nativo únicamente si reproduce el contrato fijado para MUD.

```mud
value: Rum = r0.1
```

La aproximación forma parte del significado:

```mud
r0.1 + r0.2 == r0.3
```

no está garantizada como verdadera; la aproximación forma parte del contrato.

Los parámetros de evaluación binary64 necesarios para portabilidad bit a bit se cerrarán en Q-058. Ninguna implementación puede aprovechar esa cuestión para usar otra anchura, exponer precisión extendida como resultado observable o sustituir la semántica por decimal.

### Literales

Un literal `Rum` puro exige el prefijo léxico `r`:

```mud
r10
r0.1
r1.25
r1_000
r1e-6
```

La negación es un operador exterior:

```mud
-r10
```

`r-10` es inválido.

El prefijo sigue siendo obligatorio aunque exista un tipo esperado `Rum`:

```mud
value: Rum = 0.1
```

es inválido. Debe escribirse:

```mud
value: Rum = r0.1
```

Tampoco se mezclan literales exactos y rápidos:

```mud
r0.1 + 0.2 # inválido
```

### Magnitudes basadas en `Rum`

Una magnitud puede seleccionar `Rum` como representación:

```mud
magnitude SimulationDistance: Rum {
    ...
}
```

Cuando un literal lleva una unidad de una magnitud basada en `Rum`, la unidad aporta el contexto aproximado y `r` es opcional:

```mud
10 meters
0.5 meters
r10 meters
r0.5 meters
```

Se recomienda omitir `r` en cantidades con unidad porque la magnitud ya hace visible la representación. La omisión no convierte el valor en `Num`.

### Separación y conversiones

`Num` y `Rum` no se mezclan implícitamente en aritmética ni comparación:

```mud
exactValue + rapidValue
exactValue == rapidValue
```

son errores estáticos.

Debe elegirse un dominio de cálculo:

```mud
exactValue to Rum + rapidValue
exactValue + rapidValue to Num

exactValue to Rum == rapidValue
exactValue == rapidValue to Num
```

`Num to Rum` produce el valor `binary64` más cercano conforme al redondeo global al par.

`Rum to Num` produce el racional exacto representado por el patrón binario finito almacenado. No reconstruye necesariamente el decimal que apareció en el programa.

### Política global de redondeo

La política global de MUD es redondeo al más cercano con empates al par, equivalente a `roundTiesToEven`. Se aplica a toda conversión cuantitativa estrecha que necesite redondear. No existe selección local de política.

### Valores especiales y errores

`Rum` no contiene valores observables `NaN`, `Infinity` ni `-Infinity`. La división por cero, un resultado no finito y el desbordamiento fuera del rango finito admitido producen error.

El cero negativo de `binary64` se normaliza a cero y no constituye un valor observable distinto.

### Intervalos

Un intervalo de `Rum` puede declarar un dominio:

```mud
value: Rum in [r0..r1]
```

No es enumerable. Por tanto, no puede ser fuente de `for each` ni de otra construcción que requiera enumeración exhaustiva:

```mud
for each value in [r0..r1] by r0.1: {}
```

Ese bucle es inválido. La prohibición evita que la acumulación aproximada defina pertenencia, orden de recorrido o terminación.

## Consecuencias

- `Rum` se añade a los tipos numéricos básicos.
- `Num` sigue siendo la representación numérica general predeterminada.
- El lexer incorpora una familia propia de literales prefijados con `r`.
- El AST distingue literales racionales exactos y literales `binary64`.
- El IR de `Num` necesita una forma racional canónica independiente de la implementación.
- El IR de `Rum` necesita una representación canónica del valor `binary64` finito.
- El análisis de enumerabilidad rechaza siempre intervalos de `Rum`.
- D-030 deja de tener abierta la elección de la política global de redondeo.

## Verificación futura

1. Normalización de signo, máximo común divisor y cero racional.
2. Igualdades exactas con decimales y fracciones.
3. Promoción antes de overflow entero observable.
4. Reconocimiento y rechazo de formas literales con `r`.
5. Omisión de `r` únicamente bajo una unidad de magnitud `Rum`.
6. Rechazo de mezclas implícitas entre `Num` y `Rum`.
7. Conversiones en ambos sentidos con resultados exactos conocidos.
8. Empates de conversiones estrechas resueltos al par.
9. Rechazo de división por cero y resultados no finitos.
10. Normalización de cero negativo.
11. Uso de intervalos `Rum` como dominio y rechazo como fuente enumerable.
