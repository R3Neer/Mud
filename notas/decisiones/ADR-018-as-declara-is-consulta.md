# ADR-018 — `as` declara especialización e `is` la consulta

- Estado: Vigente; vocabulario actualizado por D-025
- Fecha: 2026-07-27
- Actualizada: 2026-07-28
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], futuro `07-gramatica-concreta.md`, futuro `08-sintaxis-abstracta.md`, futuro `11-things.md`

## Contexto

La primera sintaxis de MUD utilizó `is` tanto para declarar especialización como para consultarla. Una revisión intermedia empleó la palabra ahora retirada `from`. D-025 fijó definitivamente `as` para la declaración y conservó `is` como operador.

Aunque el parser podría distinguir una cabecera de una expresión, ambas operaciones tienen significado diferente: una añade aristas directas y la otra consulta una relación derivada.

## Decisión

Toda declaración de especialización utiliza `as`:

```mud
thing A {
}

abstract thing B as A {
}

thing D as A, B, C {
}

create thing E as D {
}
```

`is` queda reservado para expresiones:

```mud
D is A
E is B
```

Las formas conceptuales son:

```text
[abstract] thing nombre [as lista-de-antecesores] bloque
create [abstract] thing nombre [as lista-de-antecesores] bloque
```

La lista posterior a `as` es finita y su posición no establece prioridad.

## Correspondencia semántica

Una cabecera `thing D as A, B` aporta:

$$
(\mathsf D,\mathsf A),\quad
(\mathsf D,\mathsf B)
\in R_{\mathrm{dir}}.
$$

`D is A` consulta:

$$
(\mathsf D,\mathsf A)
\in
R_{\mathrm{dir}}^*.
$$

Por tanto:

- `as` aporta relaciones directas;
- `is` consulta su clausura reflexiva y transitiva.

## Consecuencias

- El lexer reserva `as` e `is`; `construct` no es palabra reservada y `from` no introduce especialización.
- El AST usa una lista de antecesores en `ThingDecl` y `CreateThingEffect`.
- `IsExpression` es el nodo asociado a la consulta `is`.
- Los diagnósticos hablan de «antecesores declarados con `as`».
- Las cabeceras estáticas y las de `create` son paralelas.

El token `from` puede seguir existiendo en otras producciones independientes, como `remove x from collection`; eso no lo convierte en cláusula de especialización.

## Sintaxis retirada

Estas formas son inválidas:

```mud
construct B is A {
}

thing B from A {
}
```

Se conservan aquí únicamente como contraejemplos de migración.

## Verificación

1. `thing` raíz sin `as`.
2. Declaraciones abstractas y concretas con una o varias antecesoras.
3. `create thing` con las mismas variantes.
4. Rechazo de `is` y `from` como cláusulas de cabecera.
5. Aceptación de `is` como expresión.
6. Correspondencia entre aristas `as` y resultados de `is`.
