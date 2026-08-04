---
id: D-068
title: "`Thing` universal y nombre intrínseco"
status: vigente
date: 2026-08-02
supersedes: []
superseded-by: []
questions:
  - "Q-041"
  - "Q-047"
affects:
  - "ontología de thing, especialización, tipos incorporados, cuerpos de thing, representación Text y herramientas"
---
# ADR-068 — `Thing` universal y nombre intrínseco

- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]
- Modificada por: [[ADR-073-as-thing-explicito-redundante|D-073]]
- Modifica: [[notas/decisiones/ADR-014-ontologia-unificada-de-things|D-014]], [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|D-015]], [[notas/decisiones/ADR-018-as-declara-is-consulta|D-018]], [[notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas|D-035]], [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|D-036]], [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]], [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Pregunta relacionada: [[notas/preguntas/Q-041-ontologia-de-thing|Q-041]]
- Cuestión pendiente relacionada: [[notas/preguntas/Q-047-seleccion-de-predeterminados-por-tipo|Q-047]]
- Documentos afectados: ontología de `thing`, especialización, tipos incorporados, cuerpos de `thing`, representación `Text` y herramientas

## Contexto

MUD necesita expresar operaciones que acepten cualquier `thing`, colecciones heterogéneas y un tipo común para identidades sin una antecesora declarada compartida. Dejar que cada programa declare su propia raíz no garantiza que módulos independientes compartan la misma ni permite que las herramientas reconozcan universalmente ese contrato.

La interpolación de una `thing` usa hasta ahora su nombre nominal. Ese valor es estable para identidad y resolución, pero un juego puede necesitar una presentación humana distinta sin renombrar anclas ni introducir un campo mutable repetido en cada declaración.

## Decisión

### Tipo superior `Thing`

`Thing` es una `thing` abstracta incorporada, distinguida y siempre efectiva. Pertenece al mismo dominio conceptual que las demás `thing`, pero no posee cuerpo fuente, estado concreto ni ciclo de vida controlable por el programa.

- Toda `thing` satisface `is Thing`.
- Una `thing` sin cláusula `as` conserva cero antecesoras declaradas y recibe una arista semántica implícita hacia `Thing`.
- Una `thing` con antecesoras declaradas alcanza `Thing` transitivamente.
- `Thing is Thing` por reflexividad.
- `Thing` no puede declararse, redefinirse, activarse ni destruirse. D-073 permite escribirla explícitamente en `as`, pero la forma es redundante y recibe una sugerencia de eliminación.
- `Thing` sí puede usarse como tipo de campos, roles, argumentos, colecciones y demás posiciones de tipo compatibles.
- `on Thing` selecciona todas las `thing` concretas y activas; la identidad abstracta `Thing` no constituye por sí misma una vinculación.

`Thing` es una palabra reservada y un tipo incorporado sensible a mayúsculas y minúsculas. La arista efectiva no se duplica ni se serializa como una antecesora semántica adicional cuando el autor escribe el redundante `as Thing`; la CST y el AST superficial sí conservan esa escritura hasta que se aplica la corrección sugerida.

Su ancla canónica es `thing::Thing`; `anchor{Thing}` produce esa escritura. El ancla pertenece al lenguaje y no ocupa un path declarable por el programa.

Esta decisión no selecciona un miembro predeterminado para posiciones de tipo `Thing` con cardinalidad mínima positiva. `Thing` es abstracta y la membresía continúa siendo estricta; Q-047 conserva pendiente cuándo debe exigirse un inicializador explícito u otra selección válida.

### Propiedad intrínseca `name`

Toda `thing` posee una propiedad intrínseca, pública, inmutable e individual:

```text
name: Text
```

No es un campo de esquema, no ocupa una posición mutable del store y no se hereda. Su valor pertenece al descriptor canónico de la identidad.

Si no se escribe una sobrescritura, `name` vale exactamente el nombre nominal no cualificado de la `thing`:

```mud
thing BlackCastle {}
```

produce `name = "BlackCastle"`.

El cuerpo puede sobrescribirlo una sola vez mediante:

```mud
thing BlackCastle {
    name = "El Castillo Negro"
}
```

La parte derecha debe ser un literal `Text` sin interpolaciones. No se admiten `name: Text`, `mut name`, `name :=`, escrituras runtime ni una segunda sobrescritura. Otros contextos que ya usan la etiqueta contextual `name`, como las unidades, conservan sus reglas propias.

La sobrescritura es estrictamente local. Si una antecesora cambia su presentación, una descendiente sin sobrescritura continúa usando su propio nombre nominal:

```mud
thing Kingdom {
    name = "Reino"
}

thing Egypt as Kingdom {}
```

`Egypt.name` vale `"Egypt"`, no `"Reino"`.

Dos `thing` pueden compartir el mismo `name`; la igualdad, resolución y anclaje continúan usando identidad. En una plantilla, `{value}` para un valor `thing` inserta su `name`, mientras que `anchor{value}` conserva el ancla canónica.

`name` puede leerse como una propiedad estable y usarse donde se admita un `Text`, incluidas claves estables `ordered by name`. No concede acceso a una `thing` inactiva ni convierte el nombre desnudo de una declaración en un valor ordinario.

## Consecuencias

- Existe un tipo común garantizado para todas las `thing` y para colecciones heterogéneas.
- El grafo distingue antecesoras declaradas de la arista implícita de las raíces hacia `Thing`.
- La presentación humana puede cambiar sin alterar identidad, path de MUD ni ancla.
- `name` no introduce estado heredado, conflictos de fusión ni escrituras adicionales.
- Los campos ordinarios llamados `name` dejan de ser válidos dentro de cuerpos de `thing`; aliases, familias y otros contextos conservan sus propios espacios estructurales.

## Verificación

1. `T is Thing` para toda `thing` declarada y `Thing is Thing`.
2. Rechazo de declaración, `create` y `destroy` de `Thing`; aceptación no bloqueante de `as Thing` con sugerencia de eliminación.
3. Ancla incorporada `thing::Thing` y renderización mediante `anchor{Thing}`.
4. `on Thing` y roles `for` de tipo `Thing` sobre cualquier `thing` concreta activa.
5. Colección `Thing [*]` con identidades de ramas no relacionadas.
6. `name` predeterminado igual al nombre nominal no cualificado.
7. Sobrescritura mediante un único literal `Text` sin interpolaciones.
8. Rechazo de redeclaración, mutabilidad, cálculo, escritura runtime e interpolación en la sobrescritura.
9. Ausencia de herencia del `name` sobrescrito.
10. `{value}` usa `value.name` y `anchor{value}` conserva la identidad canónica.
11. Nombres visibles duplicados sin fusión de identidades.

## Aclaración por D-084

Los aliases no reciben una propiedad intrínseca `name`. Su declaración conserva un nombre nominal y un ancla de tipo, pero cada valor alias solo posee los componentes declarados. Un alias estructural puede declarar un componente ordinario `name: Text`. Los miembros de `family` conservan su nombre intrínseco propio.
