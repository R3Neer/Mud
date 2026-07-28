# ADR-027 — Salidas del modelo mediante `look` y `message`

- Estado: Vigente
- Fecha: 2026-07-27
- Preguntas abiertas: Q-051, Q-052
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[notas/03-semantica-de-ejecucion]], futuro `22-looks-y-messages.md`, futuro `42-api-publica.md`

## Contexto

Las acciones permiten introducir solicitudes en un modelo MUD, pero faltaba una superficie simétrica y tipada para extraer información. Leer directamente el store o los artefactos de implementación rompería la separación entre semántica y materialización.

MUD incorpora dos entidades de salida:

- `look`, para observar el estado estable actual bajo demanda.
- `message`, para publicar que ocurrió un hecho durante la resolución de una acción.

## Decisión

### `look`

Un `look` declara participantes explícitos con `for`, no admite `given` y publica propiedades calculadas:

```mud
look RealmSummary for kingdom: Kingdom {
    name := kingdom.name
    population: Natural := kingdom.cities.population.sum
}
```

Forma conceptual:

```text
look nombre for participantes {
    propiedad-publica [ : tipo ] := expresión
    ...
}
```

Cada expresión puede ser una lectura de propiedad o cualquier expresión pura bien tipada, incluidas las equivalentes a propiedades derivadas. Un `look` no modifica el mundo. Sus campos se evalúan sobre un único estado estable.

### `message`

Un `message` declara vinculaciones automáticas con `on`, una condición `when`, una guarda `if` opcional y propiedades públicas calculadas:

```mud
message KingChanged on kingdom: Kingdom {
    when kingdom.king changes
    if kingdom.visible

    kingdomName := kingdom.name
    kingName: Text := kingdom.king.name
}
```

Forma conceptual:

```text
message nombre on participantes {
    when expresión-booleana
    [if expresión-booleana]
    propiedad-publica [ : tipo ] := expresión
    ...
}
```

La detección del mensaje pertenece a la secuencia de oleadas causada por una acción. Sus propiedades públicas no se materializan con los valores del instante de detección. Se evalúan sobre el estado estable tentativo alcanzado al terminar toda la secuencia de oleadas de esa acción.

Esta separación requiere que el runtime conserve una ocurrencia pendiente con las vinculaciones de participantes necesarias y difiera la evaluación de las expresiones públicas.

### Frontera semántica

`action`, `look` y `message` forman la frontera explícita del modelo:

- `action`: entrada que puede cambiar el mundo.
- `look`: salida consultada del estado estable.
- `message`: salida eventual causada por un cambio.

Ninguna de estas entidades autoriza a observar detalles de arquitectura, framework, base de datos o materialización.

## Reglas estáticas iniciales

- Los nombres de propiedades públicas son únicos dentro de su entidad.
- Toda propiedad pública posee un tipo estático, declarado opcionalmente o inferido de su expresión.
- La expresión asignada debe ser pura. Si el tipo se declara, debe ser compatible con él; si se omite, su tipo debe poder inferirse unívocamente.
- Un `look` no admite `on`, `given`, `when`, `if`, `then` ni `after`.
- Un `message` no admite `for`, `given`, `then` ni `after`.
- Un `message` exige exactamente un `when` y como máximo un `if`.
- Las expresiones públicas de un `message` deben seguir siendo evaluables en el estado estable final para las vinculaciones conservadas.

## Cuestiones todavía abiertas

### Q-051 — Identidad y selección de un `look`

Falta definir cómo se proporcionan participantes, qué resultado se obtiene cuando no están activos, si una consulta puede devolver varias filas y cómo se serializan cardinalidades, aliases y magnitudes.

### Q-052 — Entrega de `message`

Falta decidir:

- Si una misma vinculación puede producir una o varias ocurrencias durante una acción.
- Cómo se ordenan mensajes distintos y ocurrencias múltiples.
- Si se deduplican detecciones repetidas.
- Qué ocurre con una detección si la acción termina `rejected` o `failed`.
- Qué ocurre si un participante queda inactivo antes del estado estable.
- Si la guarda `if` se evalúa al detectar, al estabilizar o en ambos momentos.

Hasta resolver Q-052, la norma solo fija que los campos publicados se evalúan después de la estabilización; no fija todavía el protocolo de entrega.

## Consecuencias

- El AST incorpora `LookDecl`, `MessageDecl` y `PublicFieldDecl`.
- El runtime necesita una cola transaccional de ocurrencias pendientes, separada de un bus o transporte concreto.
- El grafo semántico incorpora dependencias de lectura desde las expresiones públicas.
- Los mensajes no deben materializarse como efectos externos antes de que la resolución sea confirmable.
- Las materializaciones pueden convertir looks y mensajes en endpoints, consultas, eventos o callbacks, pero esos mecanismos no forman parte de MUD.

## Verificación futura

1. `look` puro con propiedades de tipo declarado e inferido y con una expresión compuesta.
2. Rechazo de `given` en `look`.
3. `message` con y sin `if`.
4. Rechazo de cabeceras y cláusulas incompatibles.
5. Caso donde el valor al detectar difiere del valor estable publicado.
6. Rollback sin emisión externa prematura.
