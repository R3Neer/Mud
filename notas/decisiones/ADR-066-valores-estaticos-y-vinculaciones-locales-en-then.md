---
id: D-066
title: "Valores estáticos y vinculaciones locales en `then`"
status: vigente
date: 2026-07-30
supersedes: []
superseded-by: []
questions: []
affects:
  - "campos almacenados y calculados, familias, predeterminados, acciones, tests, bloques de efectos, AST e IR"
---
# ADR-066 — Valores estáticos y vinculaciones locales en `then`

- Modifica: [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]], [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]], [[notas/decisiones/ADR-038-familias-cerradas-de-valores|D-038]], [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]] y [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|D-057]]
- Amplía: [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]]
- Documentos afectados: campos almacenados y calculados, familias, predeterminados, acciones, tests, bloques de efectos, AST e IR

## Contexto

MUD usa `=` para valores almacenados o predeterminados y `:=` para valores calculados. Faltaba delimitar si un valor escrito con `=` podía ser una expresión y cómo nombrar cálculos intermedios dentro de un `then` sin convertirlos en estado del mundo.

Una restricción a tokens literales sería demasiado estrecha. Expresiones como:

```mud
1..2 | 3..4
```

son constantes aunque combinen varios literales y operadores. A la vez, permitir que `=` leyera estado cambiante confundiría «empieza siendo» con «se calcula como».

## Decisión

### Expresión estática cerrada

Una expresión estática cerrada:

- Es pura, determinista y no estocástica.
- Puede evaluarse por completo durante la compilación.
- No consulta campos de estado, participantes, `given`, valores locales ni actividad del mundo.
- Puede usar literales, miembros de `family`, anclas nominales que denotan valores conocidos estáticamente, constructores y operaciones entre constantes.
- Se elabora bajo el tipo esperado cuando el contexto lo proporciona.

Las referencias nominales permitidas no leen la carga mutable ni la actividad actual de una `thing`.

### Uso de `=`

El valor explícito de un campo almacenado, componente, dato almacenado de `family`, asignación de miembro y predeterminado de `given` debe ser una expresión estática cerrada.

```mud
lives: Natural = 3
king: Person = Arthur
allowed: Integer Interval = 1..2 | 3..4
duration: Time = 1 hour + 30 minutes
```

La unión de intervalos produce un único valor normalizado de intervalo discontinuo; no constituye una excepción especial.

Esto es inválido si `victories` es estado:

```mud
initialScore: Natural = victories * 3
```

La forma calculada es:

```mud
score := victories * 3
```

`=` introduce carga o predeterminado materializable. `:=` declara una dependencia calculada. La distinción no depende de que la expresión escrita parezca sencilla.

### Vinculación local calculada

Un bloque de `then` puede declarar valores locales:

```mud
then {
    cost := amount * price
    remaining: Money := kingdom.money - cost
    kingdom.money -= cost
}
```

La forma es:

```text
nombre [ : tipo ] := expresión
```

Comparte con los campos calculados:

- Inmutabilidad.
- Expresión pura.
- Inferencia de tipo cuando existe una solución única.
- Anotación obligatoria cuando la inferencia es ambigua.
- Ausencia de `mut`, `in`, cardinalidad y modificadores propios.

No crea un campo, un lugar asignable ni estado persistente. El AST y el IR la representan como una vinculación local, no como un efecto.

### Secuencialidad, evaluación y ámbito

La declaración se evalúa exactamente una vez cuando la ejecución alcanza su posición textual. Lee la proyección secuencial privada producida por las instrucciones anteriores del mismo `then`.

El valor queda fijado. Los efectos posteriores no provocan su reevaluación aunque cambien campos consultados por la expresión.

El nombre:

- Es visible desde la instrucción posterior a su declaración hasta el final de su bloque.
- No es visible antes de la declaración.
- Puede ser usado por vinculaciones locales posteriores.
- No puede sombrear otro nombre visible ni redeclararse en el mismo ámbito.
- No admite referencias adelantadas ni ciclos.

```mud
then {
    tax := basePrice / 10
    finalPrice := basePrice + tax
    account.balance -= finalPrice
}
```

Esto es inválido:

```mud
then {
    finalPrice := basePrice + tax
    tax := basePrice / 10
    account.balance -= finalPrice
}
```

Un bloque de `for each` aplica la misma regla en cada iteración y crea un ámbito local nuevo. Las vinculaciones de una iteración no sobreviven a la siguiente.

Un `then` continúa necesitando al menos un efecto o una llamada a acción; un bloque compuesto únicamente por vinculaciones locales no modifica el mundo y es inválido como cuerpo de acción o consecuencia reactiva.

## Consecuencias

- `=` acepta más que literales, pero nunca depende del estado runtime.
- Los intervalos discontinuos constantes se asignan directamente y se normalizan al compilar.
- Los cálculos repetidos dentro de un `then` pueden recibir nombres sin ampliar el store.
- La resolución de locales es estrictamente textual y no requiere un punto fijo.
- Las trazas pueden mostrar el valor local calculado, pero este no recibe ancla ni se publica como estado.

## Verificación

1. Literal, constructor nominal y operación constante con `=`.
2. Unión, intersección, diferencia y diferencia simétrica de intervalos constantes.
3. Rechazo de lectura de estado, participante, `given`, local o azar en una expresión estática.
4. Valor local con tipo inferido y anotado.
5. Rechazo de inferencia ambigua.
6. Lectura local de un efecto secuencial anterior.
7. Conservación del valor frente a efectos posteriores.
8. Dependencia de un local anterior.
9. Rechazo de referencia adelantada, ciclo, redeclaración y sombreado.
10. Ámbito por bloque e iteración.
11. Rechazo de `mut`, `in` o especificación de colección en una vinculación local.
12. Rechazo de un `then` sin ningún efecto observable.
