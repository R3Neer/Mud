# ADR-025 — Vocabulario de `thing`, cabeceras y bloques

- Estado: Vigente
- Fecha: 2026-07-27
- Pregunta posteriormente resuelta: Q-053 mediante D-030
- Decisiones actualizadas o sustituidas: D-004, D-005, [[notas/decisiones/ADR-018-as-declara-is-consulta|D-018]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[especificacion/04-modelo-matematico]], futuro `07-gramatica-concreta.md`, futuro `11-things.md`, futuro `20-reglas.md`, futuro `21-acciones.md`

## Contexto

La terminología y las cabeceras históricas de MUD acumulaban tres problemas:

1. `construct` sonaba a artefacto del lenguaje en vez de a cosa del mundo.
2. `from` declaraba especialización, aunque la lectura infantil natural es «`A` es como `B`».
3. `on` y `for` se asignaban al revés de la distinción que se quiere hacer entre declaraciones observadoras y operaciones solicitadas.

Además, la documentación no distinguía con suficiente precisión cuándo las llaves pertenecen a una cláusula y cuándo son obligatorias.

## Decisión

### `thing` y `as`

`thing` sustituye a `construct` como palabra reservada:

```mud
thing Kingdom {
}

abstract thing Place {
}
```

`as` introduce los antecesores directos de una `thing`:

```mud
thing Egypt as Kingdom, Place {
}

create thing Alexandria as City {
}
```

La lista posterior a `as` sigue denotando un conjunto finito de antecesores directos sin prioridad por posición. El operador booleano `is` conserva su semántica: consulta la clausura reflexiva y transitiva de esa relación.

`as` deja de ser un operador de conversión explícita. D-030 fija posteriormente la rama cuantitativa de `to` y D-032 añade el casting nominal de aliases compatibles.

### Matriz de participantes

Las cabeceras quedan distribuidas así:

| Entidad | Participantes | `given` |
| --- | --- | --- |
| Regla de cambio | `on` | No |
| Regla `always` | `on` | No |
| `message` | `on` | No |
| `action` | `for` | Sí |
| Regla booleana | `for` | Sí |
| `look` | `for` | No |

`on` declara vinculaciones que el motor observa y construye automáticamente para detectar hechos del mundo. `for` declara participantes proporcionados al solicitar una operación o consulta. `given` aporta valores auxiliares que no son participantes y solo pertenece a acciones y reglas booleanas.

### Llaves de las cláusulas

Las cláusulas `when`, `if`, `after` y `then` admiten una forma desnuda cuando su cuerpo tiene un único elemento:

```mud
when door.open
if person is Citizen
then open gate
after gate.open
```

También admiten llaves con ese único elemento cuando mejoren la lectura:

```mud
when {
    door.open
}
```

Un `then` con varias instrucciones debe usar llaves:

```mud
then {
    remove oldKing from kingdom.kings
    add newKing to kingdom.kings
}
```

`when`, `if` y `after` contienen una única expresión booleana, aunque esa expresión sea compuesta. Por ello, el único caso actual en que la pluralidad hace obligatorias las llaves es `then`.

## Compatibilidad

Quedan retiradas de la sintaxis vigente:

```mud
construct Egypt from Kingdom {
}

action Enter on person: Person {
}
```

Los fragmentos anteriores de esta sección son contraejemplos históricos. Los ADR vigentes relacionados se han actualizado para usar `thing`, `as` y la distribución actual de participantes.

## Consecuencias

- El lexer reserva `thing` y `as`; `construct` deja de ser palabra reservada.
- El AST utiliza `ThingDecl` y una lista `directAncestors` introducida por `as`.
- `is` sigue siendo el único operador de consulta de especialización.
- El parser puede seleccionar la forma de cabecera a partir de la clase de entidad.
- El analizador debe rechazar `given` en `look`, `message`, reglas de cambio y reglas `always`.
- El futuro formateador puede preferir la forma desnuda para cuerpos breves y llaves para expresiones extensas, sin cambiar el AST.

## Verificación futura

1. Declaración raíz, abstracta y de especialización múltiple con `thing` y `as`.
2. Rechazo de `construct` y de `from` como introductores de especialización; otros usos gramaticales de `from`, como `remove x from c`, no cambian.
3. Rechazo de `as` como conversión explícita.
4. Una prueba positiva y otra negativa para cada fila de la matriz de participantes.
5. Aceptación de cada cláusula con y sin llaves cuando contiene un elemento.
6. Rechazo de un `then` desnudo con varias instrucciones.
