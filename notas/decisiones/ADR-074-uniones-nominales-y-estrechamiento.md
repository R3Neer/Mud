---
id: D-074
title: "Uniones nominales y estrechamiento de tipos"
status: vigente
date: 2026-08-03
supersedes: []
superseded-by: []
questions:
  - "Q-047"
affects:
  - "gramática, AST, sistema de tipos, aliases, expresiones y diagnósticos"
---
# ADR-074 — Uniones nominales y estrechamiento de tipos

- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]
## Contexto

MUD necesita expresar que un valor puede pertenecer a varias alternativas sin perder la identidad nominal elegida. La misma necesidad aparece en campos, participantes, valores `given`, vinculaciones locales y aliases.

## Decisión

`|` forma una unión de tipos en cualquier posición de tipo:

```mud
value: Nat | Text
alias Result := Nat | Text
```

Una alternativa puede declarar su propio dominio. La especificación de colección solo puede aparecer una vez, al final, y se aplica a la unión completa:

```mud
values: Nat in 0..10 | Int in -10..-1 [1..*]
```

Los paréntesis pueden agrupar, pero la forma canónica los elimina cuando no cambian la asociación. No existen cardinalidades por alternativa.

La unión es asociativa, conmutativa e idempotente respecto de alternativas idénticas. No elimina una alternativa nominal por estar su dominio contenido en el de otra: `Nat | Int` conserva ambas alternativas.

### Elección de alternativa

Una expresión se incorpora implícitamente cuando posee una única alternativa compatible. Si un literal o expresión todavía construible por contexto satisface varias, existe ambigüedad:

```mud
value: Nat | Int = 2        # inválido
value: Nat | Int = 2 to Int # válido
```

La regla es especialmente importante para aliases distintos con la misma representación. El valor unido conserva la alternativa nominal por la que entró. Una unión de tipos `thing` conserva la identidad original y es compatible con `Thing` exactamente cuando todas sus alternativas lo son.

`Thing` continúa siendo universal solo para declaraciones `thing`; no incorpora aliases, families, magnitudes ni otros tipos nominales por el hecho de existir `|`. Cuando se necesite reunir categorías distintas se escribe una unión explícita.

### Operaciones y estrechamiento

Sin información adicional solo se admiten operaciones válidas con resultado compatible para todas las alternativas posibles. `is` se amplía para comprobar pertenencia nominal a una alternativa y `is not` se incorpora como operador compuesto canónico con la misma precedencia:

```mud
rule IsPositive given value: Nat | Text {
    value is Nat and value > 0
}
```

Una condición verdadera estrecha el entorno de la parte cuya evaluación depende de ella: el operando derecho de `and`, la expresión final de un bloque booleano y el `then` gobernado por el `if` de una acción o regla. `is not A` elimina las alternativas o porciones que satisfacen `A`; en tipos solapados no equivale necesariamente a seleccionar una alternativa completa.

`is` observa el tipo nominal, no la inclusión matemática del contenido. Un valor `2 to Int` no satisface `is Nat` por ser no negativo.

### Aliases estructurales

Un componente estructural puede tener tipo unión. No se admite unir cuerpos estructurales anónimos después de `}`. Las formas deben nombrarse y después unirse:

```mud
alias Coordinate := GridCoordinate | NumericCoordinate
```

La definición simple de alias conserva `:=`; `:` continúa siendo anotación de un valor.

### Predeterminados

Una unión que no permita seleccionar un predeterminado nominal único exige inicializador explícito en todo contexto que necesite materializar un valor. El orden textual de alternativas nunca selecciona el predeterminado.

## Consecuencias

- El AST resuelto conserva alternativas nominales normalizadas y la alternativa elegida por cada incorporación.
- Los análisis booleanos necesitan entornos refinados sensibles al flujo.
- D-017 debe distinguir tipos válidos de tipos materializables sin inicializador.
- `|` se desambigua por contexto sintáctico entre unión de tipos y sus usos sobre valores.

## Verificación

1. Uniones en todas las posiciones de tipo.
2. Dominios locales y una única colección exterior.
3. Normalización sin paréntesis redundantes.
4. Ambigüedad de literales y aliases representacionalmente iguales.
5. Estrechamiento mediante `is` e `is not`.
6. Solapamiento por especialización múltiple.
7. Rechazo de cuerpos estructurales anónimos unidos.

## Aclaración por D-084

La unión `A | B` expresa alternativas. No resuelve una especialización múltiple `alias C as A, B`: esta exige que cada valor de `C` satisfaga simultáneamente ambas antecesoras y, por tanto, una representación efectiva común obtenida por intersección compatible.
