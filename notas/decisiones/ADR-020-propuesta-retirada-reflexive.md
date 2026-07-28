# ADR-020 — Propuesta retirada de `[reflexive]`

- Estado: Sustituida por [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]]
- Fecha: 2026-07-27
- Actualizada: 2026-07-28 para separar con claridad historia y sintaxis vigente
- Documentos afectados: historial de diseño de colecciones

## Contexto histórico

Como `is` es reflexivo, se consideró permitir que una colección cuyo tipo escrito fuese una `thing` pudiera contener esa misma identidad. La propuesta introducía el modificador:

```mud
person: Person[1 reflexive]
```

Sin él, habría exigido membresía estricta:

$$
x\neq T
\land
x\ \mathsf{is}\ T.
$$

Con él, habría bastado:

$$
x\ \mathsf{is}\ T.
$$

## Decisión histórica

La propuesta permitía `[reflexive]` únicamente en colecciones de `thing`, de forma ortogonal a `mut`, `unique` y `ordered`.

Una descendiente estricta nunca habría necesitado el modificador:

```mud
create thing Alice as Person {
}
```

`Alice` habría sido válida en `Person[1]` porque:

$$
\mathsf{Alice}\neq\mathsf{Person}
\land
\mathsf{Alice}\ \mathsf{is}\ \mathsf{Person}.
$$

## Sustitución

D-026 retiró por completo esta posibilidad. La norma vigente es siempre:

$$
x\in\operatorname{Members}(T[k])
\Rightarrow
x\neq T
\land
x\ \mathsf{is}\ T.
$$

No existe `reflexive` ni ningún modificador equivalente en el léxico, la gramática, el AST o el IR actuales. Incluso una `thing` concreta que pueda actuar como cosa y antecesora queda excluida de una colección cuyo tipo escrito sea exactamente ella misma.

## Motivo de la retirada

El modificador añadía sintaxis y casos de interacción sin un caso de uso suficiente. La membresía estricta universal es más fácil de explicar, comprobar y trasladar al principio de diseño de MUD:

> Una colección de `Person` contiene cosas que son `Person`, pero no contiene la propia regla conceptual `Person`.

## Valor documental

Este ADR no define sintaxis vigente. Se conserva para explicar:

- por qué la reflexividad matemática de `is` no determina la pertenencia a colecciones;
- por qué D-026 formula una desigualdad explícita;
- por qué `reflexive` aparece como token rechazado en pruebas de migración.

## Verificación vigente

La suite actual debe cubrir:

1. aceptación de una descendiente estricta;
2. rechazo del ancla exacta;
3. rechazo léxico o sintáctico de `reflexive`;
4. aplicación de la misma regla a cardinalidad singular y plural.
