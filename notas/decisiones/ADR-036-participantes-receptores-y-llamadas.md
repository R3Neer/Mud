# ADR-036 — Participantes, receptores y llamadas

- Estado: Vigente
- Fecha: 2026-07-28
- Amplía: [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|D-025]]
- Preguntas relacionadas: Q-011, Q-012
- Documentos afectados: futuro `07-gramatica-concreta.md`, futuro `19-expresiones.md`, futuros capítulos 21 a 24

## Decisión

### Participantes y `given`

Un participante ocupa un rol semántico desempeñado por uno o varios valores. Determina los sujetos de la operación y, cuando el rol posee capacidades, el acceso a estado o a un lugar de escritura.

Un `given` es un valor suministrado como parámetro auxiliar; no ocupa un rol semántico aunque su tipo también pudiera aparecer en `for`.

D-025 fija las cabeceras:

- `on`: vinculaciones automáticas e individuales de `thing` para reglas reactivas, `always` y `message`.
- `for`: roles individuales o colectivos de cualquier tipo declarado, suministrados a reglas booleanas, actions y `look`.
- `given`: valores auxiliares de reglas booleanas y actions.

Reglas reactivas, `always`, `look` y `message` no admiten `given`.

### Cardinalidad y nombres

Un rol `for` admite cualquier `declared-type`, incluidos tipos básicos, aliases, familias, diccionarios y `thing`, además de la especificación completa de colección: cardinalidad, `unique`, `ordered`, `ordered by` y, cuando sus miembros son `thing`, capacidad interior `mut`. La cardinalidad omitida equivale a `[1]` conforme a D-039. `on` continúa vinculando una sola `thing` por rol y no admite otros tipos, cardinalidad ni los modificadores de colección `unique` u `ordered`.

El nombre de un participante `on`, o de un participante `for` cuya cardinalidad efectiva sea exactamente `[1]`, puede omitirse. Los accesos no cualificados dentro del cuerpo se resuelven contra esos participantes anónimos, además de los nombres ordinariamente visibles:

```mud
rule IsDestroyed for Army {
    soldiers == 0
}

rule CanGovern for Person, Kingdom {
    age >= 18 and treasury > 0
}
```

La omisión es válida únicamente si cada referencia no cualificada posee un solo candidato compatible. Esta resolución se aplica por igual a campos, reglas booleanas y actions accesibles desde los participantes; la firma y los tipos de los argumentos forman parte de la resolución. En el segundo ejemplo, `age` debe resolverse solo contra `Person` y `treasury` solo contra `Kingdom`. Si ambos tipos ofrecieran `name`, una referencia desnuda a `name` sería ambigua y el programa debería cualificarla declarando el nombre del participante correspondiente.

La omisión no crea una variable global ni cambia el tipo de la declaración.

Cuando el cuerpo necesita referirse al participante como valor completo, y no solo resolver un miembro suyo, debe declararle un nombre.

Un valor básico no ofrece miembros que puedan resolverse implícitamente; por tanto, un rol básico anónimo no puede ser utilizado por el cuerpo y el compilador debe sugerir nombrarlo o eliminarlo. Los componentes de un alias estructural y los datos asociados de una `family` sí participan en la resolución implícita cuando esta es unívoca.

Todo rol `for` cuya cardinalidad no sea exactamente `[1]` debe tener nombre. La colección no proyecta implícitamente los campos de sus miembros: el cuerpo debe emplear el nombre en una cuantificación, agregación o iteración explícita.

```mud
rule AllAdults for people: Person [1..*, unique] {
    forall person in people: person.age >= 18
}
```

También son roles válidos los valores sin identidad runtime:

```mud
rule IsWeekend for day: Day {
    day == Saturday or day == Sunday
}
```

### Mutabilidad de participantes `for`

En una action, `mut` antes del nombre de cualquier rol `for`, incluido uno de cardinalidad `[1]`, concede mutabilidad exterior sobre la colección suministrada. Ese rol siempre debe tener nombre. El receptor correspondiente debe ser un lugar almacenado exteriormente mutable; un literal o una expresión calculada no son lugares y se rechazan.

El `mut` incluido en la especificación de colección concede capacidad interior sobre las `thing` miembro. Es inválido cuando el tipo efectivo de miembro no es una `thing`. Ambos permisos son ortogonales conforme a D-019:

| Declaración | Cambiar colección | Modificar miembros |
| --- | --- | --- |
| `patients: Person [*]` | No | No |
| `mut patients: Person [*]` | Sí | No |
| `patients: Person [* mut]` | No | Sí |
| `mut patients: Person [* mut]` | Sí | Sí |

Reglas booleanas y `look` no admiten `mut` exterior porque son puros. Los participantes `on` tampoco lo admiten: su `[mut]` opcional es exclusivamente capacidad interior sobre la `thing` individual vinculada.

La mutabilidad exterior no exige que los miembros sean `thing`: modifica el lugar que contiene la colección, no los valores inmutables contenidos. Por ejemplo:

```mud
action Record for mut observations: Number [*]
given value: Number {
    then add value to observations
}
```

### Modos de vinculación

El modo de vinculación depende del contrato del rol:

| Rol | Modo |
| --- | --- |
| `thing` sin `mut` exterior | identidad de cada `thing` |
| básico, alias, `family`, diccionario u otro valor inmutable | valor |
| cualquier tipo con `mut` exterior | identidad del lugar almacenado y valor actual |

Una colección conserva además cardinalidad, multiplicidad y orden. Repetir un valor o una identidad produce tantas ocurrencias como permita el contrato salvo que el rol sea `unique`.

### Varios participantes

Varios participantes declaran roles ordenados. El orden forma parte de la API semántica:

```mud
rule CanAttack for
    attacker: Army,
    defender: Army
{
    ...
}
```

Los participantes relacionados automáticamente pueden usar `in`:

```mud
rule ApplyStarvation on
    world: World,
    kingdom in world.kingdoms [mut]
{
    ...
}
```

Esto crea una vinculación por pertenencia real y no un producto cartesiano. En participantes suministrados mediante `for`, las restricciones relacionales adicionales se expresan mediante tipos o condiciones.

### Identidad exacta y selección por tipo

Una referencia cualificada escrita en el cuerpo sin cabecera de participantes designa la identidad canónica exacta:

```mud
rule AdvanceCalendar {
    when World.day changes
    then World.date += 1 day
}
```

Aquí `World` no significa «toda `thing` que sea `World`», sino la única identidad `World`.

En cambio, un participante individual `on World` o `for World` selecciona `thing` concretas activas cuyo tipo satisface `is World`. Cada miembro `thing` de un rol `for` colectivo se somete a la misma selección. La selección es reflexiva: incluye la identidad exacta `World` cuando es concreta y activa, además de sus especializaciones activas. Una `thing` abstracta no aporta por sí misma una vinculación concreta, aunque sus especializaciones sí puedan aportarla. Esta regla de selección no se aplica a roles de valor.

Para excluir deliberadamente la identidad raíz debe declararse un rol y expresarse la condición:

```mud
rule DescendantOnly for world: World {
    world != World and ...
}
```

La selección por tipo nunca sustituye una referencia nominal exacta escrita fuera de una cabecera.

### Receptores y argumentos

Los receptores vinculan participantes; los argumentos vinculan `given`.

```mud
army.IsDestroyed()
game.InCheck(White)
(attacker, defender).CanAttack()
(source, destination).Transfer(amount)
```

La vinculación ordinaria de participantes y `given` es posicional. Reordenar la declaración cambia la API.

La separación no depende del tipo. Un valor es `for` cuando constituye un sujeto semántico de la declaración y `given` cuando solo parametriza la operación:

```mud
action Record for mut observations: Number [*]
given value: Number {
    then add value to observations
}
```

Una expresión de colección ocupa una sola posición de receptor cuando el rol correspondiente es colectivo; no se expande en varios receptores. Si el rol declara mutabilidad exterior, la expresión debe ser un lugar mutable compatible y la vinculación conserva ese destino para los efectos de la action.

Un receptor multiparte puede usar forma nombrada:

```mud
(
    attacker = leftArmy,
    defender = rightArmy
).CanAttack()
```

Debe nombrar roles existentes exactamente una vez, ser exhaustivo y aportar tipos compatibles. Los nombres permiten reordenar roles en esta construcción de llamada; no se confunden con la regla de orden de componentes nombrados de alias.

Los argumentos `given` también pueden vincularse por nombre mediante `=` dentro de los paréntesis:

```mud
game.InCheck(color = White)
(source, destination).Transfer(amount = 10)
```

La vinculación de los `given` continúa siendo siempre posicional. El nombre escrito es una etiqueta opcional de legibilidad y comprobación: debe coincidir con el `given` que ocupa esa misma posición y no permite reordenar argumentos.

Los argumentos posicionales y etiquetados pueden mezclarse en cualquier posición:

```mud
game.Search(origin, depth = 3, true)
```

Si la firma declara `given origin`, `given depth` y `given exhaustive` en ese orden, la llamada anterior es válida. Esto no lo sería:

```mud
game.Search(depth = 3, origin, true)
```

porque la primera posición corresponde a `origin`, no a `depth`.

### Naturaleza de la llamada

Una llamada a regla no crea una función general. Una solicitud o composición de action tampoco permite invocar código arbitrario. Ambas elaboran una vinculación semántica comprobable hacia una declaración conocida.

## Consecuencias

- AST e IR separan receptores de argumentos.
- La omisión del nombre de participante individual es azúcar sometido a resolución estática no ambigua, no una firma distinta.
- Un rol colectivo conserva cardinalidad, modificadores de colección y ambos ejes de capacidad en AST e IR.
- Una vinculación exteriormente mutable conserva el lugar receptor, no solo su valor.
- El IR distingue vinculaciones de rol por identidad, por valor y por lugar.
- D-025 y esta decisión resuelven Q-011 para participantes nombrados.
- El compilador puede reconstruir lecturas, escrituras y dependencias desde la firma.

## Verificación futura

1. Participante individual anónimo y nombrado.
2. Varios participantes individuales anónimos con accesos unívocos y rechazo de un acceso ambiguo.
3. Receptor multiparte posicional y nombrado.
4. Rol ausente, duplicado, desconocido o mal tipado.
5. Mezcla de argumentos `given` sin etiqueta y etiquetados, conservando siempre la posición.
6. Rechazo de una etiqueta que no coincide con el `given` de su posición.
7. Separación entre participantes y `given`.
8. Vinculación `on` relacionada mediante `in`.
9. Rechazo de cabeceras incompatibles.
10. Diferencia entre la referencia exacta `World` y un participante `on World` o `for World`.
11. Reflexividad para una raíz concreta y ausencia de vinculación directa para una raíz abstracta.
12. Rol `for` colectivo con cardinalidad y cada modificador de colección.
13. Nombre obligatorio para cardinalidad distinta de `[1]` y para mutabilidad exterior.
14. Receptor colectivo ocupando una sola posición, sin expansión implícita.
15. Las cuatro combinaciones de mutabilidad exterior e interior.
16. Aceptación de un lugar mutable y rechazo de literales o expresiones calculadas para `mut nombre`.
17. Rechazo de colecciones en `on` y de mutabilidad exterior en construcciones puras.
18. Roles `for` básicos, alias, `family`, diccionario y `thing`.
19. Vinculación por identidad, valor y lugar.
20. Rechazo de capacidad interior `mut` sobre miembros que no sean `thing`.
21. Diferencia entre un valor sujeto `for` y un valor auxiliar `given` del mismo tipo.
