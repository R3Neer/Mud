# Destrucción, estado latente y grafo efectivo

- Estado: decisión consolidada con cuestiones locales abiertas
- Preguntas relacionadas: [[notas/preguntas/Q-048-destruccion-con-descendientes-activos|Q-048]], [[notas/preguntas/Q-049-destruccion-y-colecciones-de-thing|Q-049]]
- Decisión principal: [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]]

## Resultado

La destrucción runtime es una retirada lógica reversible, no una limpieza física del almacenamiento.

```mud
destroy Kingdom
```

produce tres efectos conceptuales:

1. `Kingdom` deja de ser efectivo.
2. Su estructura y las declaraciones con dependencia dura de `Kingdom` se suspenden.
3. Su definición canónica permanece en el programa y sus cargas runtime permanecen almacenadas para una reactivación posterior.

La recomendación anterior de podar destructivamente colecciones queda sustituida por D-021.

## Ejemplo canónico

Antes:

```mud
thing King {
    kingdom: Kingdom[1] = Panama
}
```

```text
Stored(W):
    King.kingdom
        type  = Kingdom[1]
        value = Panama

Effective(W):
    King.kingdom = Panama
```

Después de:

```mud
destroy Kingdom
```

```text
Stored(W'):
    King.kingdom
        type  = Kingdom[1]
        value = Panama

Effective(W'):
    la propiedad King.kingdom no está disponible
```

Después de recrear `Kingdom`, la misma propiedad reaparece con `Panama`.

## Diferencia respecto de `remove`

```mud
remove kingdom from King
```

elimina la declaración y el valor almacenado. Una adición posterior crea una propiedad nueva.

```mud
destroy Kingdom
```

solo suspende la propiedad por dependencia. La recreación de `Kingdom` restaura la propiedad anterior.

## Colecciones

No se eliminan miembros almacenados por el mero hecho de ejecutar `destroy`. Por tanto:

- No se necesita mutabilidad exterior para conservar el estado.
- No se buscan predeterminados para rellenar cardinalidades.
- No se pierde orden, multiplicidad ni claves.
- La cardinalidad de la representación almacenada permanece estable.

Cuando el tipo declarado de una propiedad queda inactivo, se suspende la propiedad completa. No se presenta al programa una colección visible que incumpla temporalmente su cardinalidad.

Permanece abierta la observación de una identidad inactiva desde una colección cuyo tipo declarado sigue activo. Por ejemplo, si `Panama` está en `Thing[*]` y se destruye `Panama`, debe decidirse si la colección efectiva omite el miembro, expone una referencia latente o suspende una operación concreta.

## Grafo efectivo

Las aristas `as` originales permanecen en las definiciones canónicas del programa. La proyección efectiva atraviesa cadenas de antecesores inactivos y conecta cada descendiente activo con sus antecesores activos más próximos.

Este mecanismo:

- Mantiene activos a los descendientes.
- Retira las propiedades heredadas desde nodos destruidos.
- Conserva las propiedades propias cuyos tipos continúen efectivos.
- Restaura exactamente la forma declarada cuando reaparecen los antecesores.

## Aliases

D-031 retira los aliases del ciclo de vida runtime. `destroy AliasName` y cualquier forma de `create alias` son errores estáticos.

Un alias es un tipo nominal declarado estáticamente. Sus valores son inmutables y carecen de identidad runtime; por tanto, no existen componentes suspendidos, cargas latentes por inactividad del tipo ni restauración de su declaración.

## Participantes

Un participante suspendido no se elimina de una firma. La declaración completa deja de ser efectiva:

- Una regla reactiva deja de producir bindings.
- Una `always rule` deja de imponer su condición.
- Una regla booleana pasa a la semántica de borrado de reglas inactivas.
- Una acción deja de poder solicitarse mientras falte su dependencia.

## Próxima formalización

El capítulo de ciclo de vida deberá definir:

1. La estructura exacta de `Stored(W)` y `Effective(W)`.
2. La clausura de dependencias duras.
3. El algoritmo declarativo de compresión del grafo.
4. La observación de referencias latentes desde tipos todavía activos.
5. La interacción con `old`, bindings y serialización.
6. La restauración simultánea de varias dependencias.
