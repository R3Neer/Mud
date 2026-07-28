# ADR-024 — Definición única y activación abreviada de reglas

- Estado: Vigente para reglas; aliases sustituidos por D-031
- Fecha: 2026-07-27
- Modifica: [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]], [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]]
- Modificada por: [[notas/decisiones/ADR-031-aliases-nominales-e-inmutables|D-031]]
- Preguntas relacionadas: [[notas/08-preguntas-abiertas#Q-006 — Conflictos|Q-006]], [[notas/08-preguntas-abiertas#Q-046 — Creación inefectiva dentro de una raíz|Q-046]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[notas/03-semantica-de-ejecucion]], futuros capítulos 07, 08, 21 a 23, 25 y 32

## Contexto

> [!note] Vocabulario histórico
> D-025 sustituyó `construct`/`from` por `thing`/`as` e intercambió los usos de `on` y `for`. La unicidad y activación abreviada de reglas decididas aquí siguen vigentes; sus ejemplos conservan la sintaxis histórica.

Permitir varios cuerpos para una misma regla obliga a decidir en runtime qué cuerpo queda activo o a rechazar dos creaciones coincidentes. Repetir un cuerpo idéntico en cada punto de activación tampoco aporta semántica y exige definir una noción artificial de igualdad entre cuerpos.

Los constructos son distintos. Sus creaciones pueden aportar fragmentos compatibles y fusionables con casos de uso causales reales.

## Decisión

Cada identidad de regla tiene exactamente una definición completa en todo el programa. Esa definición puede ser:

- Una declaración inicial ordinaria, efectiva desde el estado inicial.
- Una declaración incluida en un `create`, conocida estáticamente pero efectiva solo cuando se ejecute esa creación.

Ejemplos de definición inicial:

```mud
rule FrozenGround for person: Person {
    ...
}
```

Una aparición definitoria dinámica incluye categoría y cuerpo:

```mud
create rule FrozenGround for person: Person {
    ...
}
```

```mud
create always rule ValidKingdom for kingdom: Kingdom {
    ...
}
```

Una aparición definitoria dinámica cumple dos funciones:

1. Proporciona al compilador el descriptor canónico.
2. Solicita su activación cuando se ejecuta el `then` que la contiene.

Las activaciones posteriores a cualquiera de las dos formas de definición omiten tanto el cuerpo como la categoría:

```mud
create FrozenGround
create ValidKingdom
```

El nombre se resuelve estáticamente a la definición canónica. La forma abreviada solo es válida para una regla.

## Buena formación

Sea $\mathcal R_P$ el conjunto de identidades de reglas conocidas por el programa. Sea:

$$
\mathcal D_P^{\mathsf{single}}
:=
\mathcal R_P
$$

la unión de ambas categorías. Sea $\mathcal S_P^{\mathsf{def}}$ el conjunto de declaraciones iniciales y apariciones de `create` con cuerpo completo, y sea:

$$
\operatorname{defines}_P:
\mathcal S_P^{\mathsf{def}}
\to
\mathcal D_P^{\mathsf{single}}
$$

la identidad definida por cada aparición.

Se exige:

$$
\forall d\in\mathcal D_P^{\mathsf{single}}.
\left|
\{
s\in\mathcal S_P^{\mathsf{def}}
\mid
\operatorname{defines}_P(s)=d
\}
\right|
=1
$$

Por tanto:

- Una activación abreviada sin definición completa es un error estático.
- Dos definiciones completas de la misma identidad son un error estático.
- También se rechazan dos cuerpos textualmente o estructuralmente iguales.
- El orden de archivos y declaraciones no afecta a la resolución.
- Una definición puede aparecer después de cualquiera de sus activaciones abreviadas.
- Una declaración inicial y una definición completa dentro de `create` para la misma identidad cuentan como dos definiciones y son inválidas.

No se intenta decidir equivalencia semántica entre cuerpos. La unicidad es de aparición definitoria.

## Sintaxis abstracta

Las formas de superficie se elaboran, como mínimo, a nodos distintos:

```text
DefineInitialRule(anchor, descriptor)
DefineAndCreateRule(anchor, descriptor)
CreateReference(anchor)
```

`CreateReference` no contiene un cuerpo duplicado. Después de resolver nombres, su ancla determina la regla que activa.

La omisión de categoría no introduce ambigüedad porque D-021 exige resolución unívoca de las identidades destruibles. Si un nombre no puede resolverse a una única ancla, la activación es inválida.

## Activaciones concurrentes

Varias solicitudes abreviadas o definitorias dinámicas de la misma regla se consolidan idempotentemente:

$$
\{
\operatorname{create}(d),
\ldots,
\operatorname{create}(d)
\}
\rightsquigarrow
\operatorname{create}(d)
$$

Ya no existe un conflicto runtime por dos activaciones de la misma regla: todas remiten al mismo descriptor canónico.

El compilador tampoco necesita demostrar que las reglas activadoras sean mutuamente excluyentes.

La creación y destrucción del mismo objetivo desde `then` distintos mantiene el orden estructural de D-023: la destrucción se aplica después y el objetivo termina inactivo.

## Excepción de los constructos

Los constructos mantienen definiciones fragmentarias:

```mud
create construct Storm from WeatherEvent {
    intensity: Number
}
```

```mud
create construct Storm from SeaHazard {
    affectedShips: Ship[*]
}
```

Si ambas solicitudes son efectivas en la misma oleada, sus antecesores y propiedades se fusionan conforme a D-023.

No se admite:

```mud
create Storm
```

como activación abreviada de constructo. Sin un descriptor canónico único, esa forma no determina qué fragmento debe aportar, especialmente si la identidad nunca se materializó antes.

Los aliases, las acciones y las magnitudes no admiten `create`.

## Ausencia de abstracciones de efectos

Esta decisión resuelve la repetición sin introducir procedimientos, funciones de efectos ni bloques reutilizables de `then`.

Una abstracción de efectos exigiría definir parámetros, capturas, resultados, recursión, orden, pureza y llamadas desde reglas y acciones. No se añade mientras no exista un caso de uso independiente que justifique esa capacidad.

## Consecuencias para tooling

Un LSP debe poder:

- Navegar con Ctrl-click desde `create FrozenGround` hasta su definición.
- Enumerar todas las activaciones y destrucciones de una identidad.
- Diagnosticar una segunda definición y señalar la primera.
- Ofrecer reemplazar un cuerpo duplicado por una activación abreviada.
- Distinguir visualmente definición y referencia sin alterar la semántica.

## Verificación futura

La suite deberá cubrir:

1. Una definición completa y varias activaciones abreviadas.
2. Activación abreviada anterior textualmente a la definición.
3. Error por ausencia de definición.
4. Error por dos definiciones diferentes.
5. Error por dos definiciones idénticas.
6. Consolidación de varias activaciones en una oleada.
7. Definición completa y activación abreviada coincidentes.
8. Activación abreviada de regla booleana, reactiva y `always`.
9. Destrucción y reactivación abreviada de una regla declarada inicialmente.
10. Rechazo de una declaración inicial y un `create` definitorio para la misma identidad.
11. Rechazo de activación abreviada de `thing`, alias, acción o magnitud.
12. Conservación de fragmentos múltiples de `thing`.
