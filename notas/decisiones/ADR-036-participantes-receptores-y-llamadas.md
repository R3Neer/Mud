---
id: D-036
title: "Participantes, receptores y llamadas"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-011"
  - "Q-012"
  - "Q-013"
affects:
  - "futuro `07-gramatica-concreta.md`, futuro `19-expresiones.md`, futuros capítulos 21 a 24"
---
# ADR-036 — Participantes, receptores y llamadas

- Amplía: [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|D-025]]
- Modificada por: [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]]
- Preguntas relacionadas: Q-011, Q-012, Q-013
- Documentos afectados: futuro `07-gramatica-concreta.md`, futuro `19-expresiones.md`, futuros capítulos 21 a 24

## Decisión

### Participantes y `given`

Un participante ocupa un rol semántico desempeñado por uno o varios valores. Determina los sujetos de la operación y, cuando el rol posee capacidades, el acceso a estado o a un lugar de escritura.

Un `given` es un valor suministrado como parámetro auxiliar; no ocupa un rol semántico aunque su tipo también pudiera aparecer en `for`.

Todo `given` tiene nombre obligatorio, es de solo lectura y no admite mutabilidad exterior ni capacidad interior. Puede declarar un predeterminado estático cerrado conforme a D-063.

D-025 fija las cabeceras:

- `on`: vinculaciones automáticas e individuales de `thing` para reglas reactivas, `always` y `message`.
- `for`: roles individuales o colectivos de cualquier tipo declarado, suministrados a reglas booleanas, actions y `look`.
- `given`: valores auxiliares de reglas booleanas y actions.

Reglas reactivas, `always`, `look` y `message` no admiten `given`.

### Cardinalidad y nombres

Un rol `for` admite cualquier `declared-type`, incluidos tipos básicos, aliases, familias, diccionarios y `thing`, un dominio `in` y la especificación completa de colección. El dominio restringe los valores admisibles del rol y se escribe entre el tipo y la especificación de colección. La cardinalidad omitida equivale a `[1]` conforme a D-039. `on` continúa vinculando una sola `thing` por rol y no admite otros tipos, cardinalidad ni los modificadores de colección `unique` u `ordered`.

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
rule AllAdults for people: Person in EligibleCitizens [1..*, unique] {
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

El `mut` incluido en la especificación de colección concede capacidad interior sobre los valores miembro que posean estado modificable. Escribirlo cuando el tipo efectivo solo contiene valores inmutables es legal, pero produce una sugerencia porque el permiso es inútil. Ambos permisos son ortogonales conforme a D-019:

| Declaración | Cambiar colección | Modificar miembros |
| --- | --- | --- |
| `patients: Person [*]` | No | No |
| `mut patients: Person [*]` | Sí | No |
| `patients: Person [* mut]` | No | Sí |
| `mut patients: Person [* mut]` | Sí | Sí |

Reglas booleanas y `look` no admiten `mut` exterior porque son puros. Los participantes `on` tampoco lo admiten: su `[mut]` opcional es exclusivamente capacidad interior sobre la `thing` individual vinculada. Los `given` no admiten ninguna forma de `mut`.

La mutabilidad exterior no exige que los miembros sean `thing`: modifica el lugar que contiene la colección, no los valores inmutables contenidos. Por ejemplo:

```mud
action Record for mut observations: Num [*]
given value: Num {
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

La anotación puede conservarse delante de `in` para refinar nominalmente el elemento:

```mud
rule MutualFriends on
    alice: Person in bob.friends,
    bob in alice.friends
{
    ...
}
```

Los nombres son visibles en toda la cabecera y sus restricciones se resuelven conjuntamente, no de izquierda a derecha. Para cada rol se parte de las `thing` concretas y activas de su tipo efectivo; el conjunto de vinculaciones es el join finito que satisface todas las pertenencias. Una solución de tipos ambigua exige anotaciones adicionales. Los ciclos relacionales no son puntos fijos y leen una única instantánea, conforme a D-063.

Las asignaciones de roles conservan orientación, permiten que dos roles reciban la misma `thing` y no deduplican automáticamente parejas simétricas. En participantes suministrados mediante `for`, las restricciones relacionales adicionales se expresan mediante tipos o condiciones.

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

La vinculación ordinaria de participantes y `given` puede ser posicional. Reordenar la declaración cambia el orden canónico de la API.

La separación no depende del tipo. Un valor es `for` cuando constituye un sujeto semántico de la declaración y `given` cuando solo parametriza la operación:

```mud
action Record for mut observations: Num [*]
given value: Num {
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

La forma nombrada es válida en cualquier orden, pero el compilador sugiere el orden de declaración. No puede mezclarse con receptores posicionales.

Los argumentos `given` pueden vincularse realmente por nombre mediante `=` dentro de los paréntesis:

```mud
game.InCheck(color = White)
(source, destination).Transfer(amount = 10)
```

Una llamada admite posiciones, nombres o un prefijo posicional seguido por nombres. Después del primer nombre no puede aparecer una posición. Los nombres pueden reordenar los `given`, aunque el compilador sugiere el orden de declaración.

Los predeterminados estáticos permiten omisiones. Posicionalmente solo puede omitirse un sufijo completo de `given` predeterminados; los nombres permiten omitir cualquier predeterminado intermedio:

```mud
game.Search(origin, depth = 3)
game.Search(depth = 3)
```

Si la firma declara `origin = Capital`, `depth` y `exhaustive = false` en ese orden, ambas llamadas son válidas. Esto no lo sería:

```mud
game.Search(depth = 3, origin)
```

porque una posición no puede aparecer después del primer argumento nombrado.

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
5. Argumentos `given` posicionales, nombrados y con prefijo posicional seguido por nombres.
6. Omisión de predeterminados finales por posición e intermedios por nombre.
7. Separación entre participantes y `given`.
8. Vinculación `on` relacionada, refinada, adelantada y cíclica mediante `in`.
9. Rechazo de cabeceras incompatibles.
10. Diferencia entre la referencia exacta `World` y un participante `on World` o `for World`.
11. Reflexividad para una raíz concreta y ausencia de vinculación directa para una raíz abstracta.
12. Rol `for` colectivo con dominio, cardinalidad y cada modificador de colección.
13. Nombre obligatorio para cardinalidad distinta de `[1]` y para mutabilidad exterior.
14. Receptor colectivo ocupando una sola posición, sin expansión implícita.
15. Las cuatro combinaciones de mutabilidad exterior e interior.
16. Aceptación de un lugar mutable y rechazo de literales o expresiones calculadas para `mut nombre`.
17. Rechazo de colecciones en `on` y de mutabilidad exterior en construcciones puras.
18. Roles `for` básicos, alias, `family`, diccionario y `thing`.
19. Vinculación por identidad, valor y lugar.
20. Sugerencia para capacidad interior demostrablemente inútil sobre valores inmutables.
21. Diferencia entre un valor sujeto `for` y un valor auxiliar `given` del mismo tipo.
22. Rechazo de mutabilidad exterior e interior en `given`.
23. Conservación de orientaciones simétricas y de roles reflexivos en `on`.
