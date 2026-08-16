---
id: D-062
title: "Literales canónicos de magnitudes de punto"
status: vigente
date: 2026-07-29
supersedes: []
superseded-by: []
questions:
  - "Q-055"
affects:
  - "léxico, gramática concreta, magnitudes de punto, scanner, parser y pruebas de conformidad"
---
# ADR-062 — Literales canónicos de magnitudes de punto

- Modificada por: [[ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]]
- Amplía: [[notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos|D-029]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Responde parcialmente: [[notas/preguntas/Q-055-literales-de-magnitudes-de-punto|Q-055]]
- Documentos afectados: léxico, gramática concreta, magnitudes de punto, scanner, parser y pruebas de conformidad

## Contexto

La propiedad `format` ya determina cómo se representa una magnitud de punto. La gramática reservaba `POINT_LITERAL`, pero no fijaba si el formato era solo de salida ni cómo reconstruir un punto cuando omitía precisión, coincidía con el formato de otro tipo o describía un valor fuera del dominio.

## Decisión

### Selección contextual

`POINT_LITERAL` es un literal contextual. Solo se admite cuando el contexto exige un único tipo de magnitud `point over`. Si el tipo esperado no existe o no es unívoco, el programa contiene un error estático.

La selección por tipo ocurre antes de interpretar el formato. Por tanto, dos magnitudes pueden producir la misma secuencia visible sin colisionar cuando el contexto determina una de ellas.

### Magnitud con `format`

Cuando el tipo esperado declara `format`, el literal debe coincidir exactamente con la representación canónica que ese formato produciría. Debe contener:

- todos los fragmentos fijos;
- todos los componentes, en el orden declarado;
- los separadores y caracteres exactos;
- la forma numérica canónica determinada por cada especificación de anchura y precisión.

No se aceptan escrituras alternativas aunque produzcan los mismos componentes. Por ejemplo, si el formato canónico produce `07:05:00`, `7:05:00` no es el mismo literal.

Un `format` de punto debe ser estáticamente invertible: sus fragmentos y huecos deben permitir reconstruir un único punto. Una declaración cuyo formato no tenga una inversión unívoca es inválida. Esta obligación restringe el uso de expresiones arbitrarias dentro del `format` de una magnitud de punto, aunque esas expresiones sean renderizables en una plantilla `Text` ordinaria.

La comprobación canónica equivale a:

1. reconocer los fragmentos y componentes del formato;
2. reconstruir el punto;
3. representarlo de nuevo con el mismo formato;
4. exigir igualdad exacta con el texto fuente.

### Precisión omitida

Todo componente de precisión inferior a la menor unidad representada por el formato toma valor cero. Así, un formato que termina en segundos construye un punto con cero fracciones de segundo, incluidos milisegundos, microsegundos, nanosegundos y picosegundos cuando esas unidades existan.

La omisión no redondea ni conserva información implícita.

### Magnitud sin `format`

Cuando el tipo esperado no declara `format`, su literal usa la sintaxis ordinaria de cantidad y debe escribir una unidad compatible habilitada para la magnitud subyacente. La cantidad se interpreta como la coordenada completa del punto respecto de su origen canónico.

### Dominio

Después de reconstruir la coordenada, el compilador comprueba que pertenezca al dominio declarado por la magnitud de punto. Un literal fuera del dominio es un error de compilación.

La comprobación se realiza antes de cualquier normalización cíclica. Un dominio `[0..86_400) cycle` cuya unidad raíz sea el segundo no autoriza un literal de `26 hour` ni su equivalente formateado; los valores fuente fuera de rango no se envuelven.

La normalización cíclica continúa aplicándose a las operaciones runtime según las reglas de magnitudes de punto, pero no corrige un literal inválido.

## Consecuencias

- `format` es simultáneamente la representación canónica y, cuando existe, la forma fuente del tipo de punto.
- El lexer conserva `POINT_LITERAL` como token contextual, pero el análisis requiere el tipo esperado y la declaración de magnitud resuelta.
- Los formatos de punto tienen una restricción de invertibilidad que no afecta a las plantillas `Text` generales.
- Las colisiones entre formatos se resuelven por el tipo esperado, no por prioridad léxica global.
- La precisión no escrita tiene un valor definido y reproducible.
- Los ciclos no convierten errores fuente en valores válidos.

## Ejemplos

```mud
magnitude TimeOfDay point over Time in [0..86_400) cycle {
    format = "{hour:2}:{minute:2}:{second:2}"
}

opening: TimeOfDay = 07:05:00
```

El valor de `opening` tiene cero fracciones de segundo.

```mud
opening: TimeOfDay = 7:05:00   # inválido: no es la forma canónica
opening: TimeOfDay = 26:00:00  # inválido: queda fuera del dominio
```

Sin formato:

```mud
magnitude Timestamp point over Time {}

created: Timestamp = 90 second
```

## Verificación

1. Aceptación de la representación canónica exacta.
2. Rechazo de variantes de anchura, separadores o componentes.
3. Inicialización a cero de toda precisión inferior omitida.
4. Resolución de formatos coincidentes mediante tipos esperados distintos.
5. Rechazo sin tipo esperado o con tipo ambiguo.
6. Rechazo estático de formatos no invertibles.
7. Literal con unidad para una magnitud sin `format`.
8. Rechazo de coordenadas fuera de dominios lineales y cíclicos.
