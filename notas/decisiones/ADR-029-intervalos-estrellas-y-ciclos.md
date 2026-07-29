# ADR-029 — Intervalos, límites efectivos y ciclos de punto

- Estado: Vigente
- Fecha: 2026-07-28
- Modificada por: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Modificada por: [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]]
- Preguntas relacionadas: Q-018, Q-055
- Documentos afectados: futuro `15-colecciones.md`, futuro `17-dominios-e-intervalos.md`, futuro `18-magnitudes.md`

## Contexto

MUD usa intervalos para dominios numéricos, magnitudes y cardinalidades. La referencia inicial no fijaba de forma uniforme el significado lateral de `*` ni integraba el ciclo de una magnitud de punto en su dominio.

## Decisión

### Formas de intervalo

Las cuatro formas delimitadas son:

```mud
[n..m]
(n..m)
[n..m)
(n..m]
```

`n..m` equivale a `[n..m]` y `[n]` equivale a `[n..n]`.

D-059 añade unidades locales y compartidas a las expresiones ordinarias de intervalo y fija que un intervalo lineal con límites efectivos invertidos se normaliza a `empty`. Esta inversión no expresa orden descendente ni ciclo.

La forma `[n]` también coincide superficialmente con una colección unitaria. No se elimina ninguno de los dos usos ni se concede prioridad a uno: el tipo esperado y las restricciones de la expresión deben producir una única elaboración. Si una derivación sin tipo admite ambas, debe declarar el tipo explícitamente conforme a D-037.

### Límites efectivos

`*` representa el límite efectivo del lado en el que aparece. Los dos lados no tienen por qué denotar el mismo valor:

```mud
Natural [*..10]  # [0..10]
Natural [1..*]   # [1..+∞]
[*..*]           # dominio efectivo completo
```

`[*]` es azúcar de `[*..*]`. En una cardinalidad ordinaria, `Thing[*]` comienza en cero y llega hasta el límite superior permitido.

Todo lado escrito con `*` debe ser cerrado:

```mud
[*..10]
[1..*]
[*..*]
[*]
```

Son inválidos `(*..10]`, `[1..*)`, `(*..*)` y cualquier otra forma que deje abierto un extremo escrito con `*`.

### Dominios de magnitud

Una magnitud puede declarar su dominio en la cabecera:

```mud
magnitude PlayerCount: Natural in 1..8 {
    ...
}

magnitude Speed in [0..*] :=
    Length / Time
```

En una magnitud no derivada, la representación numérica opcional precede siempre al dominio:

```text
magnitude nombre [: representación-numérica] [in intervalo] bloque
```

Los límites se escriben como números desnudos. En una magnitud no derivada se interpretan en su unidad raíz; en una derivada, en la combinación canónica inferida de las unidades raíz componentes.

Por tanto, si la unidad canónica de `Speed` es `m/s`, `[0..100]` significa de `0 m/s` a `100 m/s`. No se admiten unidades explícitas ni unidades alternativas dentro de esos límites. Los valores escritos posteriormente con otra unidad se normalizan antes de comprobar el dominio.

### Magnitudes de punto

Una magnitud de punto se declara con `point over` en la cabecera:

```mud
magnitude TimeOfDay point over Time in [0..86_400 cycle) {
    format = "{hour:2}:{minute:2}:{second:2}"
}
```

Representa posiciones sobre una magnitud lineal y utiliza sus unidades. No puede declarar unidades ni `root unit`.
Puede declarar mediante `format` una representación textual. Conforme a D-061, el valor es una plantilla `Text`: `hour`, `minute` y `second` son expresiones contextuales del entorno que Q-055 debe terminar de definir, y `:2` solicita dos posiciones a la izquierda del punto. Q-055 conserva abiertos el catálogo y significado de componentes, el parseo inverso, la unicidad y las colisiones, no una sintaxis de llaves distinta.

Su aritmética es:

| Operación | Resultado |
| --- | --- |
| $P-P$ | $M$ |
| $P+M$ | $P$ |
| $M+P$ | $P$ |
| $P-M$ | $P$ |
| $P+P$ | error |

Solo una magnitud `point over` puede ser cíclica. `cycle` aparece dentro del intervalo, inmediatamente antes del delimitador derecho, y la única forma cíclica válida es:

```mud
[a..b cycle)
```

El dominio debe ser finito, contiguo, no vacío, cerrado a la izquierda y abierto a la derecha. Su periodo es $b-a$ y todo valor se normaliza módulo ese periodo respecto de $a$.

Para `[0..360 cycle)`:

```text
360  → 0
370  → 10
-10  → 350
```

`cycle` modifica la normalización del dominio de punto. No altera la semántica ni la iteración de los intervalos generales. Su periodo debe ser estrictamente positivo: la normalización a `empty` de D-059 no repara un dominio cíclico invertido o degenerado.
Tampoco resuelve ni modifica los ciclos de dependencia entre dominios calculados tratados por Q-017.

## Consecuencias

- El AST de intervalos representará cada límite como concreto o efectivo y conservará la apertura de cada lado.
- La comprobación de dominios de magnitud se realizará después de normalizar unidades.
- El ciclo forma parte del dominio de una magnitud de punto, no es una propiedad independiente del bloque.

## Verificación futura

1. Expansión contextual de `[*]` para tipos, magnitudes y cardinalidades.
2. Rechazo de todos los extremos abiertos escritos con `*`.
3. Interpretación canónica de límites desnudos.
4. Rechazo de unidades explícitas en la cabecera `in` de una magnitud.
5. Normalización cíclica con límite inferior distinto de cero.
6. Rechazo de ciclos en magnitudes no puntuales y dominios no semiabiertos.
7. Resolución contextual de `[n]` como intervalo unitario y rechazo cuando también sea viable como colección sin tipo esperado suficiente.
8. Normalización de intervalos lineales invertidos a `empty` sin interpretación descendente.
9. Rechazo de un periodo cíclico nulo o negativo.
