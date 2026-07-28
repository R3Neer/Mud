# ADR-036 — Participantes, receptores y llamadas

- Estado: Vigente
- Fecha: 2026-07-28
- Amplía: [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|D-025]]
- Preguntas relacionadas: Q-011, Q-012
- Documentos afectados: futuro `07-gramatica-concreta.md`, futuro `19-expresiones.md`, futuros capítulos 21 a 24

## Decisión

### Participantes y `given`

Un participante ocupa un rol semántico desempeñado por una `thing` existente. Determina sujetos, acceso a estado y, cuando sea mutable, capacidad de escritura.

Un `given` es un valor suministrado; no ocupa un rol de identidad del mundo.

D-025 fija las cabeceras:

- `on`: vinculaciones automáticas de reglas reactivas, `always` y `message`.
- `for`: participantes suministrados de reglas booleanas, actions y `look`.
- `given`: valores auxiliares de reglas booleanas y actions.

Reglas reactivas, `always`, `look` y `message` no admiten `given`.

### Participante único

Una declaración con exactamente un participante puede omitir su nombre. Los accesos no cualificados dentro del cuerpo se resuelven contra ese participante implícito.

La omisión no crea una variable global ni cambia el tipo de la declaración.

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

Esto crea una vinculación por pertenencia real y no un producto cartesiano. En participantes suministrados mediante `for`, las restricciones adicionales se expresan mediante tipos, dominios o condiciones.

### Receptores y argumentos

Los receptores vinculan participantes; los argumentos vinculan `given`.

```mud
army.IsDestroyed()
game.InCheck(White)
(attacker, defender).CanAttack()
(source, destination).Transfer(amount)
```

La vinculación ordinaria de participantes y `given` es posicional. Reordenar la declaración cambia la API.

Un receptor multiparte puede usar forma nombrada:

```mud
(
    attacker = leftArmy,
    defender = rightArmy
).CanAttack()
```

Debe nombrar roles existentes exactamente una vez, ser exhaustivo y aportar tipos compatibles. Los nombres permiten reordenar roles en esta construcción de llamada; no se confunden con la regla de orden de componentes nombrados de alias.

Q-012 mantiene abierta la sintaxis de argumentos `given` nombrados.

### Naturaleza de la llamada

Una llamada a regla no crea una función general. Una solicitud o composición de action tampoco permite invocar código arbitrario. Ambas elaboran una vinculación semántica comprobable hacia una declaración conocida.

## Consecuencias

- AST e IR separan receptores de argumentos.
- La forma de participante único es azúcar, no una firma distinta.
- D-025 y esta decisión resuelven Q-011 para participantes nombrados.
- El compilador puede reconstruir lecturas, escrituras y dependencias desde la firma.

## Verificación futura

1. Participante único anónimo y nombrado.
2. Receptor multiparte posicional y nombrado.
3. Rol ausente, duplicado, desconocido o mal tipado.
4. Separación entre participantes y `given`.
5. Vinculación `on` relacionada mediante `in`.
6. Rechazo de cabeceras incompatibles.
