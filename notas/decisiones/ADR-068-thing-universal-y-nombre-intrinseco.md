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

- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]
- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]
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
- Un participante `on value: Thing` selecciona todas las `thing` concretas y activas; la identidad abstracta `Thing` no constituye por sí misma una vinculación.

`Thing` es una palabra reservada y un tipo incorporado sensible a mayúsculas y minúsculas. La arista efectiva no se duplica ni se serializa como una antecesora semántica adicional cuando el autor escribe el redundante `as Thing`; la CST y el AST superficial sí conservan esa escritura hasta que se aplica la corrección sugerida.

Su ancla canónica es `thing::Thing`; `Thing~anchor` devuelve ese valor reflectivo. El ancla pertenece al lenguaje y no ocupa un path declarable por el programa. La forma especial `anchor{...}` dejó de existir con D-087.

Esta decisión no selecciona un miembro predeterminado para posiciones de tipo `Thing` con cardinalidad mínima positiva. `Thing` es abstracta y la membresía continúa siendo estricta; Q-047 conserva pendiente cuándo debe exigirse un inicializador explícito u otra selección válida.

### Identificador y presentación reflectiva

D-085 y D-087 sustituyen la antigua propiedad ordinaria `name` por dos conceptos separados en el espacio postfix `~`:

```text
~identifier : Name
~name       : Name
```

`~identifier` es intrínseco y refleja el identificador fuente de la `thing`. `~name` es un metadato estándar configurable de presentación humana; toma por defecto una presentación derivada de `~identifier` y no participa en resolución, igualdad ni formación de anclas.

```mud
thing BlackCastle {
    ~name = "El Castillo Negro"
}
```

La configuración de `~name` se rige por las reglas generales de metadatos de D-087. Todo acceso `~` es runtime-readonly: una ejecución puede leer `value~name`, pero no asignarlo. La forma antigua `name = "..."` no configura presentación y `value.name` no es acceso reflectivo.

Los espacios siguen siendo distintos. Un campo ordinario llamado `name`, si satisface las reglas generales de campos, se declara como `name: Text` y se accede con `value.name`; no colisiona sintácticamente con `~name`.

La configuración de presentación pertenece al descriptor concreto. Una descendiente sin `~name` explícito usa su propio valor predeterminado derivado de su `~identifier`, no la presentación configurada de una antecesora.

Dos `thing` pueden compartir el mismo `~name`: la igualdad, la resolución y el anclaje continúan dependiendo de la identidad nominal. La conversión textual canónica de una `thing` usa su presentación `~name` efectiva. Cuando se necesita la identidad reflectiva se consulta explícitamente `value~identifier` o `value~anchor`; no existe una interpolación especial `anchor{...}`.

## Consecuencias

- Existe un tipo común garantizado para todas las `thing` y para colecciones heterogéneas.
- El grafo distingue antecesoras declaradas de la arista implícita de las raíces hacia `Thing`.
- La presentación humana puede cambiar mediante `~name` sin alterar `~identifier`, identidad, path de MUD ni ancla.
- `~name` no introduce un lugar mutable del store ni escrituras runtime.
- El identificador ordinario de campo `name` pertenece al espacio de campos y permanece separado del metadato `~name`.

## Verificación

1. `T is Thing` para toda `thing` declarada y `Thing is Thing`.
2. Rechazo de declaración, `create` y `destroy` de `Thing`; aceptación no bloqueante de `as Thing` con sugerencia de eliminación.
3. Ancla incorporada `thing::Thing` y lectura mediante `Thing~anchor`.
4. Participantes nombrados `on value: Thing` y `for value: Thing` sobre cualquier `thing` concreta activa.
5. Colección `Thing [*]` con identidades de ramas no relacionadas.
6. `~identifier` igual al identificador fuente y `~name` predeterminado derivado de él.
7. Configuración de presentación mediante `~name` y lectura runtime de solo lectura.
8. Rechazo de escritura runtime sobre `~name` y de la forma reflectiva antigua sin `~`.
9. Una descendiente sin configuración propia no hereda la presentación explícita de su antecesora.
10. La conversión textual de una `thing` usa su `~name` efectivo; `~identifier` y `~anchor` permanecen accesos explícitos distintos.
11. Presentaciones `~name` duplicadas sin fusión de identidades.
12. Un campo ordinario `name: Text` permanece distinto del metadato `~name`.

## Aclaración por D-084

D-084 excluye una propiedad ordinaria `name` incorporada en los valores alias. D-087 regula por separado los metadatos del descriptor de la declaración `alias`, incluido `~name` cuando sea compatible. Un alias estructural puede declarar un componente ordinario `name: Text`; ese componente pertenece a su forma de valor y no es el metadato `~name`. Los miembros de `family` usan igualmente `~identifier` y `~name` conforme a D-087.
