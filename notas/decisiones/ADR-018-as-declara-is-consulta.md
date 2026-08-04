---
id: D-018
title: "`as` declara especialización e `is` la consulta"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "futuro `07-gramatica-concreta.md`, futuro `08-sintaxis-abstracta.md`, futuro `11-things.md`"
---
# ADR-018 — `as` declara especialización e `is` la consulta

- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]
- Actualizada: 2026-07-28
- Modificada por: [[notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco|D-068]]
- Modificada además por: [[notas/decisiones/ADR-073-as-thing-explicito-redundante|D-073]]
- Documentos afectados: futuro `07-gramatica-concreta.md`, futuro `08-sintaxis-abstracta.md`, futuro `11-things.md`

## Contexto

La declaración de especialización y su consulta necesitan formas distintas para que una cabecera no se confunda con una expresión. D-025 fija `as` para la declaración y conserva `is` como operador.

Aunque el parser podría distinguir una cabecera de una expresión, ambas operaciones tienen significado diferente: una añade aristas directas y la otra consulta una relación derivada.

## Decisión

Toda declaración de especialización utiliza `as`:

```mud
thing A {}

abstract thing B as A {}

thing D as A, B, C {}

thing E as D {}
```

`is` queda reservado para expresiones:

```mud
D is A
E is B
```

Las formas conceptuales son:

```text
[abstract] thing nombre [as lista-de-antecesores] bloque
```

La lista posterior a `as` es finita y su posición no establece prioridad. Una declaración sin `as` conserva cero antecesoras declaradas y recibe semánticamente la raíz incorporada `Thing`. D-073 admite `as Thing` explícito como redundancia no bloqueante y sugiere eliminarlo.

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

- El lexer reserva `as` e `is`; `abstract` es contextual delante de `thing`, conforme a D-054; `construct` no es palabra reservada y `from` no introduce especialización.
- El AST usa una lista de antecesores en `ThingDecl`; `CreateReference` no contiene antecesores ni cuerpo.
- La ausencia de antecesores en `ThingDecl` se conserva en el AST; la arista hacia `Thing` se incorpora durante la elaboración semántica.
- `IsExpression` es el nodo asociado a la consulta `is`.
- Los diagnósticos hablan de «antecesores declarados con `as`».
- Las cabeceras estáticas y las de `create` son paralelas.

El token `from` puede seguir existiendo en otras producciones independientes, como `remove x from collection`; eso no lo convierte en cláusula de especialización.

## Verificación

1. `thing` raíz sin `as`, con cero antecesoras declaradas y `is Thing` verdadero.
2. Declaraciones abstractas y concretas con una o varias antecesoras.
3. Activación mediante `create Nombre` sin alterar las antecesoras declaradas.
4. Rechazo de `is` como cláusula de cabecera.
5. Aceptación de `is` como expresión.
6. Correspondencia entre aristas `as` y resultados de `is`.
7. Diagnóstico no bloqueante y corrección sugerida para `as Thing` explícito.

## Ampliación por D-084

`as` e `is` se aplican también a aliases. En un alias nominal o estructural, `as` declara especialización directa entre tipos de valor; `is` consulta la clausura nominal conservando el tipo concreto del valor. La especialización múltiple no establece prioridad textual.
