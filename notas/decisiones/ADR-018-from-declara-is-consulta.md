# ADR-018 — `from` declara especialización e `is` la consulta

- Estado: Vigente
- Fecha: 2026-07-27
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], futuro `07-gramatica-concreta.md`, futuro `08-sintaxis-abstracta.md`, futuro `11-constructos.md`

## Contexto

La sintaxis inicial utilizaba `is` tanto en cabeceras de constructo como en expresiones booleanas:

```mud
construct Egypt is Kingdom {
}

Egypt is Kingdom
```

Aunque el parser podía distinguir ambos contextos, la misma palabra introducía una arista directa en el primero y consultaba una relación derivada en el segundo.

La sintaxis de creación generalizada ya emplea `from` para expresar los antecesores directos:

```mud
create France from Kingdom {
}
```

## Decisión

Toda declaración de especialización utiliza `from`:

```mud
construct A {
}

abstract construct B from A {
}

construct D from A, B, C {
}

create E from D {
}
```

`is` queda reservado para expresiones que consultan la relación reflexiva y transitiva:

```mud
D is A
E is B
```

La forma conceptual de una cabecera estática es:

```text
[abstract] construct nombre [from lista-de-antecesores] bloque
```

La forma conceptual de una creación es:

```text
create [abstract] nombre [from lista-de-antecesores] bloque
```

En ambos casos, la lista posterior a `from` denota un conjunto finito sin prioridad por posición.

## Correspondencia semántica

Una cabecera `construct D from A, B` aporta las aristas directas:

$$
(\mathsf{D},\mathsf{A})
$$

$$
(\mathsf{D},\mathsf{B})
$$

La expresión `D is A` consulta si:

$$
(\mathsf{D},\mathsf{A})
\in
\left(R^{\mathrm{dir}}\right)^*
$$

Por tanto, `from` y `is` operan sobre niveles distintos de la misma estructura:

- `from` aporta relaciones directas.
- `is` consulta la clausura reflexiva y transitiva.

## Consecuencias

- El lexer conserva dos palabras reservadas distintas.
- El AST usa una lista de antecesores en `ConstructDecl` y `CreateEffect`.
- `IsExpression` es el único nodo asociado al token `is`.
- Los diagnósticos pueden hablar de «antecesores declarados con `from`» sin confundirlos con consultas.
- La gramática estática y la dinámica quedan paralelas.

## Compatibilidad

La forma histórica:

```mud
construct B is A {
}
```

queda retirada antes de publicar una versión estable del lenguaje. No se necesita migración de programas publicados, pero los ejemplos y borradores internos deben actualizarse.

## Verificación futura

La suite deberá cubrir:

1. Declaración raíz sin `from`.
2. Declaración abstracta y concreta con uno o varios antecesores.
3. Creación con las mismas variantes.
4. Rechazo de `is` dentro de una cabecera.
5. Aceptación de `is` como expresión booleana.
6. Correspondencia entre las aristas declaradas con `from` y los resultados de `is`.
