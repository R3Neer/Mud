# ADR-034 — `Number` exacto y `Rumber` binary64

- Estado: Vigente
- Fecha: 2026-07-28
- Modifica: [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]]
- Preguntas relacionadas: Q-019, Q-058
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], futuro `06-lexico.md`, futuro `10-sistema-de-tipos.md`, futuro `17-dominios-e-intervalos.md`, futuro `18-magnitudes.md`, futuro `19-expresiones.md`, futuro `20-cuantificadores-e-iteracion.md`

## Contexto

Un único tipo general de número no puede ofrecer a la vez:

- Igualdad decimal intuitiva y aritmética exacta.
- Rendimiento directo de coma flotante para simulación.
- Visibilidad sintáctica de cuándo se acepta aproximación.

MUD separa esas necesidades. `Number` es el tipo general predeterminado y exacto; `Rumber`, abreviatura de *rapid number*, es una elección explícita de aritmética aproximada.

## Decisión

### `Number`

`Number` denota el conjunto de los números racionales:

$$
\llbracket\mathsf{Number}\rrbracket=\mathbb Q
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

Las operaciones son exactas mientras su resultado sea racional. En contexto `Number`, en particular:

```mud
0.1 + 0.2 == 0.3
1 / 3 * 3 == 1
1 == 1.0
```

son verdaderas.

La semántica no usa coma flotante binaria. Una implementación puede comenzar con enteros nativos, pero debe promover a enteros de precisión arbitraria antes de que ocurra desbordamiento observable. Los límites de recursos pertenecen a la taxonomía de fallos técnicos, no al dominio matemático de `Number`.

### `Rumber`

`Rumber` representa valores aproximados con formato IEEE 754 `binary64`. Una materialización puede usar el flotante nativo únicamente si reproduce el contrato fijado para MUD.

```mud
value: Rumber = r0.1
```

La aproximación forma parte del significado:

```mud
r0.1 + r0.2 == r0.3
```

no está garantizada como verdadera; la aproximación forma parte del contrato.

Los parámetros de evaluación binary64 necesarios para portabilidad bit a bit se cerrarán en Q-058. Ninguna implementación puede aprovechar esa cuestión para usar otra anchura, exponer precisión extendida como resultado observable o sustituir la semántica por decimal.

### Literales

Un literal `Rumber` puro exige el prefijo léxico `r`:

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

El prefijo sigue siendo obligatorio aunque exista un tipo esperado `Rumber`:

```mud
value: Rumber = 0.1
```

es inválido. Debe escribirse:

```mud
value: Rumber = r0.1
```

Tampoco se mezclan literales exactos y rápidos:

```mud
r0.1 + 0.2 // inválido
```

### Magnitudes basadas en `Rumber`

Una magnitud puede seleccionar `Rumber` como representación:

```mud
magnitude SimulationDistance: Rumber {
    ...
}
```

Cuando un literal lleva una unidad de una magnitud basada en `Rumber`, la unidad aporta el contexto aproximado y `r` es opcional:

```mud
10 meters
0.5 meters
r10 meters
r0.5 meters
```

Se recomienda omitir `r` en cantidades con unidad porque la magnitud ya hace visible la representación. La omisión no convierte el valor en `Number`.

### Separación y conversiones

`Number` y `Rumber` no se mezclan implícitamente en aritmética ni comparación:

```mud
exactValue + rapidValue
exactValue == rapidValue
```

son errores estáticos.

Debe elegirse un dominio de cálculo:

```mud
exactValue to Rumber + rapidValue
exactValue + rapidValue to Number

exactValue to Rumber == rapidValue
exactValue == rapidValue to Number
```

`Number to Rumber` produce el valor `binary64` más cercano conforme al redondeo global al par.

`Rumber to Number` produce el racional exacto representado por el patrón binario finito almacenado. No reconstruye necesariamente el decimal que apareció en el programa.

### Política global de redondeo

La política global de MUD es redondeo al más cercano con empates al par, equivalente a `roundTiesToEven`. Se aplica a toda conversión cuantitativa estrecha que necesite redondear. No existe selección local de política.

### Valores especiales y errores

`Rumber` no contiene valores observables `NaN`, `Infinity` ni `-Infinity`. La división por cero, un resultado no finito y el desbordamiento fuera del rango finito admitido producen error.

El cero negativo de `binary64` se normaliza a cero y no constituye un valor observable distinto.

### Intervalos

Un intervalo de `Rumber` puede declarar un dominio:

```mud
value: Rumber in [r0..r1]
```

No es enumerable. Por tanto, no puede ser fuente de `for each` ni de otra construcción que requiera enumeración exhaustiva:

```mud
for each value in [r0..r1] by r0.1 {
}
```

Ese bucle es inválido. La prohibición evita que la acumulación aproximada defina pertenencia, orden de recorrido o terminación.

## Consecuencias

- `Rumber` se añade a los tipos numéricos básicos.
- `Number` sigue siendo la representación numérica general predeterminada.
- El lexer incorpora una familia propia de literales prefijados con `r`.
- El AST distingue literales racionales exactos y literales `binary64`.
- El IR de `Number` necesita una forma racional canónica independiente de la implementación.
- El IR de `Rumber` necesita una representación canónica del valor `binary64` finito.
- El análisis de enumerabilidad rechaza siempre intervalos de `Rumber`.
- D-030 deja de tener abierta la elección de la política global de redondeo.

## Verificación futura

1. Normalización de signo, máximo común divisor y cero racional.
2. Igualdades exactas con decimales y fracciones.
3. Promoción antes de overflow entero observable.
4. Reconocimiento y rechazo de formas literales con `r`.
5. Omisión de `r` únicamente bajo una unidad de magnitud `Rumber`.
6. Rechazo de mezclas implícitas entre `Number` y `Rumber`.
7. Conversiones en ambos sentidos con resultados exactos conocidos.
8. Empates de conversiones estrechas resueltos al par.
9. Rechazo de división por cero y resultados no finitos.
10. Normalización de cero negativo.
11. Uso de intervalos `Rumber` como dominio y rechazo como fuente enumerable.
