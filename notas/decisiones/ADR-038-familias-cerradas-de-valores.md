# ADR-038 — Familias cerradas de valores

- Estado: Vigente en su núcleo; ontología detallada abierta
- Fecha: 2026-07-28
- Pregunta relacionada: Q-024
- Documentos afectados: futuro `13-familias-cerradas.md`

## Decisión

MUD admite una familia nominal finita declarada dentro de una `thing`:

```mud
thing Color {
    values =
        Red,
        Green,
        Blue
}
```

Una familia puede declarar orden semántico:

```mud
thing Severity {
    ordered values =
        Low,
        Medium,
        High,
        Critical
}
```

Los valores:

- Pertenecen nominalmente a su familia.
- Son finitos y enumerables en el orden declarado.
- Se comparan por identidad nominal dentro de la misma familia.
- Solo admiten operadores de orden si la familia usa `ordered values`.

La familia puede declarar campos comunes. La sintaxis y semántica de campos específicos por alternativa permanecen en Q-024.

Una jerarquía abierta de `thing` abstracta y especializaciones no es una familia cerrada y no adquiere enumerabilidad automática.

## Cuestión ontológica

Q-024 deberá precisar si cada alternativa cerrada es una identidad de `thing` restringida o una categoría nominal de valor distinta dentro del sistema formal. Hasta entonces, esta decisión fija sintaxis, finitud, igualdad y orden observables, pero no su representación definitiva en $\mathcal T_P$.

## Verificación futura

1. Familia cerrada ordenada y no ordenada.
2. Igualdad entre valores de la misma y distinta familia.
3. Enumeración canónica.
4. Rechazo de orden en una familia no ordenada.
5. Distinción respecto de una jerarquía abierta.
