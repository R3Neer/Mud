# ADR-038 — Familias cerradas de valores

- Estado: Vigente
- Fecha: 2026-07-28
- Pregunta relacionada: Q-024
- Documentos afectados: futuro `13-familias-cerradas.md`

## Decisión

MUD admite `family` como declaración nominal de primer nivel independiente de `thing`:

```mud
family Color {
    Red,
    Green,
    Blue
}
```

`ordered` es una palabra contextual que, situada inmediatamente antes de `family`, añade orden semántico:

```mud
ordered family Severity {
    Low,
    Medium,
    High,
    Critical
}
```

La declaración introduce un tipo nominal finito y un ancla estática `family::*`. Cada miembro:

- Pertenece nominalmente a su familia.
- Es un valor nominal, no una identidad de `thing`.
- Carece de estado mutable y de ciclo de vida runtime.
- No admite `create`, `destroy`, `as` ni consultas `is`.
- Se enumera en el orden de declaración.
- Es igual a otro miembro si y solo si ambos pertenecen a la misma familia nominal y tienen el mismo nombre.
- Solo admite operadores de orden si la declaración usa `ordered family`.

El orden de declaración es canónico para enumerar cualquier `family`, pero solo forma parte de las relaciones `<`, `<=`, `>` y `>=` cuando aparece `ordered`.

Las declaraciones `family` no participan en especialización ni pueden heredar de otras familias. Una jerarquía abierta de `thing` abstractas y especializaciones no es una familia cerrada y no adquiere enumerabilidad automática.

La sintaxis y la semántica de posibles datos inmutables comunes o específicos de cada miembro permanecen abiertas en Q-024. La selección del valor predeterminado de una familia pertenece a Q-047.

## Compatibilidad

Quedan retiradas las formas históricas:

```mud
thing Color {
    values =
        Red,
        Green,
        Blue
}

thing Severity {
    ordered values =
        Low,
        Medium,
        High
}
```

Su migración exige convertir la `thing` contenedora en una declaración `family` u `ordered family`. Esta migración es semántica: los miembros dejan de pertenecer al dominio de identidades $\mathcal T_P$.

## Verificación futura

1. Familia cerrada ordenada y no ordenada.
2. Igualdad entre valores de la misma y distinta familia.
3. Enumeración canónica.
4. Rechazo de orden en una familia no ordenada.
5. Rechazo de `create`, `destroy`, `as` e `is`.
6. Distinción respecto de una jerarquía abierta de `thing`.
7. Formación y estabilidad de anclas `family::*`.
