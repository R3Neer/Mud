---
id: D-098
title: "Rutas asignables y write-back de aliases inmutables"
status: current
date: 2026-08-28
supersedes: []
superseded-by: []
questions:
  - Q-006
affects:
  - "aliases estructurales, diccionarios exactos, destinos asignables, efectos, tipado y elaboración, capítulos 07 y 08, futuros capítulos 12, 16 y 25"
---

# ADR-098 — Rutas asignables y write-back de aliases inmutables

- Modifica: [[ADR-031-aliases-nominales-e-inmutables|D-031]], [[ADR-039-colecciones-y-diccionarios|D-039]] y [[ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|D-080]].
- Relacionada con: [[ADR-046-algebra-y-conflictos-de-efectos|D-046]], [[ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]] y [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]].
- Mantiene abierta: [[notas/preguntas/Q-006-conflictos|Q-006]] para la compatibilidad de efectos concurrentes sobre destinos parcialmente solapados.

## Contexto

Los valores de alias son inmutables y los diccionarios exactos permiten mantener poblaciones dinámicas identificadas por clave. La gramática y el AST superficial ya admiten destinos formados por una base seguida de accesos a miembros e índices, por ejemplo `orders[id].status`. Sin una regla de elaboración específica, actualizar un componente de un alias almacenado obligaría a reconstruir manualmente el valor completo y a sustituir después la asociación o campo que lo contiene.

La comodidad superficial no debe convertir los aliases en objetos mutables ni introducir identidad runtime en sus valores. Tampoco debe confundir una actualización parcial con la asignación directa de una asociación, que ya puede materializar una clave ausente.

## Decisión

### Ruta asignable reconstruible

Una ruta asignable puede atravesar uno o más valores de alias estructural inmutables cuando existe un lugar de almacenamiento exteriormente escribible al que propagar finalmente la sustitución. Una vez localizado ese lugar raíz por las reglas ordinarias de asignabilidad, los pasos que esta decisión añade como reconstruibles son exclusivamente accesos a componentes almacenados de alias e indexaciones de diccionarios exactos. Cada paso debe estar bien tipado y determinar de forma unívoca qué valor debe reconstruirse; no se concede write-back implícito a otras clases de selección.

La escritura:

```mud
orders[id].status = Shipped
```

no muta el valor `Order` obtenido de `orders[id]`. Es azúcar de elaboración para:

1. leer el valor actual alcanzado por la ruta;
2. construir un nuevo valor del mismo tipo nominal exacto del alias, sustituyendo únicamente el componente objetivo;
3. conservar sin cambios los demás componentes almacenados;
4. recalcular los campos derivados a partir del nuevo valor;
5. propagar la sustitución hacia fuera, reconstruyendo los aliases contenedores necesarios y sustituyendo las asociaciones de diccionario atravesadas hasta alcanzar el lugar raíz escribible.

Los predeterminados de componentes no vuelven a aplicarse durante la reconstrucción. La operación conserva la nominalidad exacta del valor existente y no crea identidad runtime para el alias.

La misma regla se aplica recursivamente a rutas más profundas:

```mud
users[userId].profile.address.city = Madrid
games[gameId].players[playerId].score += 10
```

Los operadores compuestos `+=`, `-=`, `*=`, `/=`, `|=`, `&=`, `^=` y `--=` usan el valor alcanzado por la ruta y aplican el mismo write-back cuando su operación de hoja está bien tipada.

### Inmutabilidad conservada

Una vinculación local que contiene únicamente un valor de alias no se convierte en lugar escribible:

```mud
order := orders[id]
order.status = Shipped # inválido
```

La segunda línea intenta modificar un valor inmutable sin una ruta de retorno a almacenamiento. Del mismo modo, un campo derivado de alias no puede ser destino: solo los componentes almacenados pueden sustituirse durante la reconstrucción.

La raíz de la ruta debe poseer la autoridad de escritura que ya exige MUD. El write-back no atraviesa una frontera de mutabilidad exterior inexistente y no transforma capacidad interior `[mut]` en permiso para sustituir un valor.

### Clave exacta ausente

Cuando una indexación de diccionario exacto aparece como paso intermedio de una ruta de write-back y su clave no existe, la consulta produce ausencia `empty` y el efecto no aporta ningún cambio al delta. La ausencia de esa clave:

- no materializa una asociación;
- no construye un alias a partir de sus predeterminados;
- no produce `failed` por sí misma.

Por tanto:

```mud
orders[missingId].status = Shipped
```

es un no-op si `missingId` no está presente.

Esta regla no modifica la asignación directa de una asociación completa:

```mud
orders[id] = order
```

La escritura directa conserva la semántica de los diccionarios exactos: sustituye una asociación existente y puede materializar una clave ausente cuando el valor y el contrato del diccionario lo permiten.

### Secuencialidad y concurrencia

Dentro de un mismo `then`, una ruta reconstruible observa el valor proyectado por los efectos secuenciales anteriores del delta privado y su write-back queda visible para las sentencias posteriores, como cualquier otro efecto.

Esta decisión no completa la matriz de conflictos concurrentes. En particular, permanece abierta en Q-006 la compatibilidad entre actualizaciones concurrentes a componentes distintos de un mismo alias reconstruido, entre una actualización parcial y la sustitución completa de su contenedor, y otros destinos parcialmente solapados.

## Alternativas descartadas

### Hacer mutables los aliases

Se descarta. La escritura abreviada no cambia la ontología del valor: el alias anterior y el posterior son valores inmutables distintos.

### Exigir reconstrucción explícita

Se descarta obligar al autor a copiar todos los componentes no modificados y volver a insertar manualmente el valor. Esa ceremonia expone un detalle mecánico de persistencia y hace especialmente costoso modelar poblaciones dinámicas mediante diccionarios.

### Crear una clave ausente con predeterminados

Se descarta para el write-back parcial. Sin un valor existente no hay una base inequívoca que reconstruir, y materializar silenciosamente el alias confundiría actualización con creación. La inserción explícita continúa disponible mediante asignación directa de la asociación completa o `add`.

### Producir `failed` por clave ausente

Se descarta. La consulta exacta ausente ya representa ausencia ordinaria mediante `empty`; el write-back parcial conserva esa filosofía y se reduce a no-op.

## Consecuencias

- `dictionary[key].component = value` es la forma idiomática de actualizar un componente de un alias almacenado en un diccionario exacto.
- Los aliases siguen siendo valores inmutables y sin identidad runtime.
- La elaboración, no el AST superficial, reconstruye los valores intermedios y obtiene el destino de almacenamiento real.
- Las rutas profundas evitan introducir APIs de copia, registries o reconstrucciones manuales solo para actualizar estado de poblaciones keyed.
- Una clave ausente distingue limpiamente actualización parcial de inserción completa.
- La compatibilidad de write-backs concurrentes parcialmente solapados sigue pendiente de la matriz general de conflictos.

## Verificación

1. `orders[id].status = Shipped` reconstruye un `Order` del mismo tipo nominal exacto y conserva sus demás componentes.
2. Una ruta con aliases estructurales anidados reconstruye de dentro hacia fuera.
3. Una actualización compuesta sobre el componente usa el valor previo y escribe el alias reconstruido.
4. Una local de tipo alias no se vuelve asignable por contener un valor leído desde almacenamiento.
5. Un campo derivado de alias no puede ser destino de write-back.
6. Una clave exacta ausente en un paso intermedio produce no-op sin inserción ni `failed` por esa ausencia.
7. `dictionary[key] = wholeValue` conserva la capacidad de crear o sustituir la asociación completa.
8. Una raíz sin mutabilidad exterior suficiente hace inválida la ruta.
9. La semántica secuencial dentro de un `then` observa write-backs anteriores.
10. Los solapamientos concurrentes no reciben una regla nueva fuera de lo ya fijado y permanecen delimitados por Q-006.
