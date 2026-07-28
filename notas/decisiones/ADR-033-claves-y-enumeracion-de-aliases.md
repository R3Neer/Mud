# ADR-033 — Claves compuestas y enumeración de aliases

- Estado: Vigente
- Fecha: 2026-07-28
- Pregunta relacionada: Q-056
- Documentos afectados: futuro `12-aliases.md`, futuro `16-diccionarios.md`, futuro `20-cuantificadores-e-iteracion.md`, futuro `37-finitud-y-enumerabilidad.md`

## Contexto

Los aliases estructurales deben poder actuar como valores compuestos ordinarios: claves de diccionario, fuentes de iteración y dominios de cuantificación. Para que dos implementaciones coincidan, la finitud y el orden de enumeración no pueden quedar implícitos.

## Decisión

### Claves compuestas

Un alias puede ser el tipo único de clave de un diccionario:

```mud
alias Square {
    file: File
    rank: Rank
}

board: Square -> Piece [0..32 ordered]
```

El acceso ordinario construye una única clave contextual:

```mud
board[(E, Four)]
```

La forma:

```mud
board[E, Four]
```

es azúcar sintáctico del mismo acceso. No convierte el diccionario en uno con varias claves ni modifica la identidad nominal de `Square`.

### Finitud

Un alias estructural es finito y enumerable cuando todos sus componentes poseen dominios finitos y enumerables:

```mud
alias Coordinate {
    horizontal: Integer in 0..7
    vertical: Integer in 0..7
}
```

Este alias tiene $8\cdot 8=64$ valores y puede usarse como fuente:

```mud
for each coordinate in Coordinate {
    ...
}

exists destination in Coordinate:
    ...
```

Si algún componente carece de dominio finito y enumerable, el alias sigue siendo un tipo válido, pero su dominio completo no puede recorrerse ni cuantificarse exhaustivamente.

### Orden de enumeración

La enumeración de un alias estructural es el producto cartesiano lexicográfico de las enumeraciones de sus componentes, en orden de declaración. Para `Coordinate`:

```text
(0, 0)
(0, 1)
…
(0, 7)
(1, 0)
…
(7, 7)
```

La enumerabilidad exige que cada componente proporcione no solo un conjunto finito, sino una enumeración canónica finita. La normalización formal de esa propiedad pertenece a Q-056.

## Consecuencias

- El azúcar de clave múltiple se elabora antes de resolver el acceso al diccionario.
- El compilador puede calcular la cardinalidad de un producto finito.
- Los cuantificadores y `for each` comparten la misma enumeración canónica del alias.
- El orden de los componentes afecta tanto a nominalidad estructural como a comparación y enumeración.

## Verificación futura

1. Acceso ordinario y azucarado a una clave alias.
2. Rechazo del azúcar cuando el tipo de clave no acepta esa forma estructural.
3. Cardinalidad de productos finitos.
4. Orden lexicográfico de enumeración.
5. Rechazo de iteración exhaustiva cuando un componente no es finito o enumerable.
