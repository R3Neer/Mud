---
id: D-102
title: "Forma completa de datos calculados de family"
status: vigente
date: 2026-08-29
supersedes: []
superseded-by: []
questions:
  - "Q-061"
affects:
  - "family, datos calculados, forma derivada, gramática, CST y AST superficial"
---
# ADR-102 — Forma completa de datos calculados de family

- Resuelve: [[notas/preguntas/Q-061-forma-de-datos-calculados-de-family|Q-061]].
- Modifica: [[ADR-038-familias-cerradas-de-valores|D-038]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]].
- Aplica a los datos calculados de `family` la forma derivada de [[ADR-037-campos-y-dominios-declarativos|D-037]].

## Contexto

Los datos calculados de `family` ya se representaban en EBNF y AST con `derived-value-shape`, mientras D-038 conservaba una excepción más estrecha que solo pretendía admitir tipo opcional y excluía dominio y forma colectiva. Q-061 aisló esa divergencia.

## Decisión

Un dato calculado de `family` usa la misma forma declarable completa que un campo calculado:

```text
nombre [forma-derivada] := value-body
```

`forma-derivada` es el `derived-value-shape` ordinario: puede fijar un `type-expression`, declarar un dominio con forma de colección opcional o declarar directamente una forma de colección. Si no fija tipo, el tipo debe inferirse unívocamente.

El dato calculado continúa siendo inmutable, no posee almacenamiento propio, no admite `mut` exterior, no tiene predeterminado almacenado y no puede ser destino de una asignación de miembro. La forma derivada describe y, donde corresponda, coacciona el valor producido; no convierte el dato en un slot escribible.

Tipo explícito, dominio, cardinalidad, `unique` y orden reutilizan exactamente la semántica general de campos calculados de D-037. Una forma derivada no puede fabricar capacidad interior `[mut]` ni otra autoridad ausente en el valor de origen.

El RHS admite la expresión breve o el `ValueBlock` ya definido para datos calculados de `family`; esta decisión no modifica su contrato de pureza ni su evaluación estática por miembro.

## Ejemplos

```mud
family Tier {
    score: Nat := baseScore
    normalized in 0..100 := rawScore
    tags: Text [* unique ordered] := inheritedTags

    Low,
    High
}
```

Las tres declaraciones son calculadas e inmutables. Las formas escritas restringen o normalizan el resultado conforme al contrato ordinario de `derived-value-shape`.

## Alternativas descartadas

### Limitar los datos calculados de `family` a `[: tipo]`

Descartado. Introduciría una excepción sin diferencia de mutabilidad o almacenamiento que la justifique y perdería las coerciones declarativas disponibles en otros campos calculados.

## Consecuencias

- Q-061 queda cerrada.
- La EBNF vigente no necesita cambiar: ya usa `[ derived-value-shape ]`.
- `CalculatedFamilyDataDecl` conserva definitivamente `derived_value_shape? shape`; deja de ser una representación provisional.
- La gramática, CST y AST de `family` quedan alineados con la forma general de campo calculado.

## Verificación

1. Un dato calculado de `family` acepta tipo explícito, dominio o forma de colección mediante `derived-value-shape`.
2. La forma sigue rechazando `mut` exterior y no crea almacenamiento.
3. La EBNF y `CalculatedFamilyDataDecl` conservan la forma derivada completa.
4. Q-061 desaparece de las superficies normativas como cuestión activa.
