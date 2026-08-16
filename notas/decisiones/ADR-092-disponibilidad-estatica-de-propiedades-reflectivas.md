---
id: D-092
title: "Disponibilidad estática de propiedades reflectivas"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "reflexión, metadatos, participantes, resolución, tipado, AST resuelto, diagnósticos y tooling"
---

# ADR-092 — Disponibilidad estática de propiedades reflectivas

- Precisa: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].
- Amplía: [[ADR-074-uniones-nominales-y-estrechamiento|D-074]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].

## Contexto

La sintaxis postfix `expression~property` debe poder reconocer nombres que son keywords duras, como `for`, `on` y `given`. La regla concreta `metadata-name ::= identifier | "for" | "on" | "given"` permite esa escritura, pero no puede determinar durante el parsing qué categoría denota una expresión receptora.

D-087 decía además que una cláusula ausente produce `empty`. Leída sin la restricción de propietario, esa frase permite interpretar erróneamente que cualquier declaración tiene siempre `~for`, `~on` y `~given`. Eso haría válido, por ejemplo, `thing A; A~for`, aunque una `thing` no posee firma `for`.

## Decisión

La existencia de una propiedad reflectiva se comprueba estáticamente después de resolver y tipar el receptor. Cada propiedad tiene un conjunto de categorías o descriptores propietarios. Si la categoría estática del receptor no garantiza pertenencia a ese conjunto, el acceso es un error estático.

El reconocimiento sintáctico del nombre después de `~` no concede la propiedad. No existe lookup dinámico por nombre, fallback a `empty` ni metadato de usuario implícito para una propiedad no soportada. Un narrowing que haga suficientemente precisa la categoría del receptor puede volver válido un acceso que antes no estaba garantizado.

Para las propiedades de participantes, la matriz es:

| Subcategoría resuelta | `~for` | `~on` | `~given` |
| --- | --- | --- | --- |
| `RuleKind.Boolean` | sí | no | sí |
| `RuleKind.Reactive` | no | sí | no |
| `RuleKind.Always` | no | sí | no |
| `ActionKind.Action` | sí | no | sí |
| `ActionKind.Subaction` | sí | no | sí |
| `look` | sí | no | no |
| `message` | no | sí | no |
| cualquier otra declaración | no | no | no |

La matriz describe capacidad de la subcategoría, no presencia concreta de la cláusula. Cuando una propiedad está soportada y la cláusula opcional fue omitida en esa declaración, el acceso es válido y devuelve `empty` con tipo `Participant [* unique ordered]`. Cuando la cláusula está presente, devuelve sus descriptores en orden de firma.

Por tanto:

```mud
thing A

# error estático: Thing no soporta ~for
check := A~for
```

y, conceptualmente:

```mud
action Ping {
    then create A
}

# válido: Action soporta ~for; Ping omitió la cláusula
participants := Ping~for  # empty
```

La regla de disponibilidad se aplica también al resto de propiedades reflectivas conforme al conjunto de propietarios de su contrato. Una propiedad cuyo resultado admita ausencia o colección vacía sigue distinguiendo esa ausencia de la inexistencia de la propiedad.

## Consecuencias por fase

### Parser y CST

No cambian. Deben aceptar la forma postfix siempre que el nombre sea sintácticamente válido. En particular, `for`, `on` y `given` siguen admitiéndose tras `~` porque son keywords duras.

### AST superficial

Conserva `MetadataAccessExpr(receiver, metadata)` aunque el acceso vaya a resultar semánticamente inválido. No posee información suficiente para aplicar la matriz.

### Resolución y tipado

Determinan la categoría estática del receptor, aplican narrowing cuando exista y seleccionan el contrato de propiedad. Si ninguna propiedad compatible existe para todos los casos todavía posibles del receptor, emiten error estático. Solo los accesos válidos llegan al AST resuelto con tipo de resultado.

### Ejecución

No realiza búsqueda dinámica para rescatar un acceso inválido. `empty` aparece únicamente como valor de un contrato válido que lo permita.

## Casos frontera

- `thing A; A~for` es inválido.
- Una `action` sin `for` tiene `ActionName~for == empty`.
- Una regla booleana sin `given` tiene `RuleName~given == empty`.
- Una regla reactiva sin `on` tiene `RuleName~on == empty`.
- `ActionName~on` es inválido aunque la acción no tenga participantes.
- Un receptor estático demasiado amplio debe estrecharse antes de acceder a una propiedad que no esté garantizada por todas sus alternativas posibles.

## Alternativas descartadas

### Todas las propiedades de firma existen y las no aplicables devuelven `empty`

Descartada porque borra la diferencia entre una categoría que admite una cláusula opcional y otra que carece de ese concepto.

### Rechazo durante parsing según el texto del receptor

Descartada porque el receptor es una expresión general y su categoría se conoce después de resolución; vincular la gramática al nombre textual rompería aliases, referencias cualificadas y narrowing.

## Verificación

1. La EBNF sigue aceptando `for`, `on` y `given` como `metadata-name`.
2. `thing A; A~for` produce AST superficial y después error estático de propiedad no soportada.
3. Una declaración de categoría compatible sin cláusula concreta devuelve `empty`.
4. `AssignableExpr` no contiene ningún sufijo de metadata.
5. El AST resuelto solo contiene `MetadataAccessExpr` para propiedades compatibles con la categoría estática resuelta.
