# ADR-020 — Membresía estricta y modificador `reflexive`

- Estado: Sustituida por [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]]
- Fecha: 2026-07-27
- Pregunta relacionada: [[notas/08-preguntas-abiertas#Q-047 — Selección de predeterminados por tipo|Q-047]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[especificacion/04-modelo-matematico]], futuro `10-sistema-de-tipos.md`, futuro `15-colecciones.md`

## Contexto

> [!warning] Decisión histórica
> D-026 elimina `reflexive` y conserva únicamente la membresía estricta. Este documento se mantiene para registrar la alternativa descartada y no define la sintaxis vigente.

La relación `is` es reflexiva:

$$
T\ \mathsf{is}\ T
$$

Si una colección de constructos aceptase sin más todos los valores que satisfacen `is`, una declaración:

```mud
person: Person[1]
```

podría contener tanto un descendiente como `Alice` como el propio constructo `Person`. Se desea que el caso exacto sea una elección visible, no una consecuencia implícita de la reflexividad matemática.

También debe distinguirse este problema de que el propietario de un campo se almacene a sí mismo. Si el campo pertenece a `Alice`, el valor `Alice` no coincide con el ancla de tipo `Person`.

## Decisión

Las posiciones de colección cuyo tipo de miembro sea un constructo utilizan membresía estricta por defecto. Sea $T$ el constructo que aparece como tipo y sea $x$ un valor candidato. Sin el modificador `reflexive`, se exige:

$$
x\ \mathsf{is}\ T
\land
x\neq T
$$

El modificador:

```mud
[reflexive]
```

o su combinación con una cardinalidad:

```mud
[1 reflexive]
[* reflexive]
```

habilita también el testigo reflexivo:

$$
x\ \mathsf{is}\ T
$$

Por tanto:

```mud
person: Person[1]
```

admite `Alice` cuando `Alice is Person`, pero no admite `Person`.

```mud
person: Person[1 reflexive]
```

admite tanto `Alice` como `Person`.

## Significado preciso de `reflexive`

`reflexive` se refiere al caso:

$$
T\ \mathsf{is}\ T
$$

No se refiere al propietario del campo. Por ejemplo:

```mud
create construct Alice from Person {
    friend: Person[1]
}
```

puede almacenar `Alice` en `friend` sin declarar `[reflexive]`, porque:

$$
\mathsf{Alice}\neq\mathsf{Person}
$$

aunque el propietario de la colección y su miembro sean la misma identidad.

El modificador se interpreta respecto del tipo escrito en la declaración original. Heredar un campo no cambia el ancla respecto de la cual se calcula el caso reflexivo.

## Restricciones estáticas

`reflexive` solo puede aparecer en una colección cuyo tipo de miembro sea un constructo concreto.

Debe rechazarse en:

- Tipos primitivos.
- Aliases.
- Magnitudes.
- Familias que no utilicen la relación de especialización de constructos.
- Un constructo abstracto que no puede denotar directamente un valor concreto.

La ubicación y el orden canónico de `reflexive` respecto de `mut`, `unique` y `ordered` se fijarán en la gramática de colecciones.

## Alternativas

### `self`

Se rechaza porque normalmente se interpretaría como «la identidad propietaria de este campo». Esa no es la condición que se modifica.

### `base` o `anchor`

Expresan mejor la representación interna, pero peor la razón semántica por la que el valor exacto queda admitido.

### Permitir siempre el caso reflexivo

Se rechaza porque hace invisible una elección con consecuencias sobre defaults, cuantificación y colecciones obligatorias.

### Prohibir siempre el caso reflexivo

Se rechaza porque un constructo concreto es una cosa además de un posible antecesor. Una prohibición absoluta impediría utilizar su faceta concreta dentro de una colección cuyo tipo natural es ese mismo constructo.

## Consecuencias para los valores predeterminados

Un valor predeterminado para una colección no reflexiva con mínimo positivo debe satisfacer la condición estricta. En particular, el propio constructo $T$ no puede ser el predeterminado de `T[1]` salvo que aparezca `[reflexive]`.

La decisión D-017 continúa vigente: todo tipo **bien formado** posee un valor predeterminado. Q-047 deberá determinar cuándo existe un predeterminado estricto o cuándo una declaración necesita un inicializador explícito para estar bien formada.

## Verificación futura

La suite deberá cubrir:

1. Aceptación de un descendiente estricto sin `[reflexive]`.
2. Rechazo del ancla exacta sin `[reflexive]`.
3. Aceptación del ancla exacta con `[reflexive]`.
4. Independencia entre reflexividad respecto del tipo y autorreferencia respecto del propietario.
5. Rechazo del modificador sobre tipos no constructo.
6. Interacción con constructos abstractos.
7. Interacción con cardinalidades obligatorias y predeterminados.
