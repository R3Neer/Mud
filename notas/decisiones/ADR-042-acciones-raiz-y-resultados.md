---
id: D-042
title: "Acciones, raíz y resultados"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-002"
  - "Q-003"
  - "Q-004"
  - "Q-022"
  - "Q-023"
  - "Q-046"
  - "Q-059"
affects:
  - "frontera pública, efectos, solicitud de acciones, semántica de la raíz"
---
# ADR-042 — Acciones, raíz y resultados

- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Relacionada con: [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]]
- Modificada por: [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]], [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Modificada además por: [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]] y [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]]
- Preguntas relacionadas: Q-002, Q-003, Q-004, Q-022, Q-023, Q-046, Q-059
- Documentos afectados: frontera pública, efectos, solicitud de acciones, semántica de la raíz

## Contexto

Una acción es la frontera de escritura de MUD. Su contrato debe separar la inadmisibilidad esperable de una solicitud de los errores que impiden obtener un estado válido.

## Decisión

```mud
action Recruit for kingdom: Kingdom [mut]
given
    amount: Nat in 1..100
{
    if kingdom.treasury >= amount * kingdom.recruitmentCost
    otherwise "The kingdom cannot afford {amount} recruits"
    then {
        kingdom.treasury -= amount * kingdom.recruitmentCost
        kingdom.soldiers += amount
    }
    after kingdom.soldiers >= old kingdom.soldiers
    otherwise "Recruitment did not increase the army"
}
```

Una acción:

- declara participantes mediante `for`;
- puede declarar valores `given` y sus dominios;
- puede declarar `if` y `after`;
- debe declarar `then`;
- no declara `when` ni se activa automáticamente;
- una `action` puede solicitarse desde el exterior y, en ese caso, inicia la resolución causal raíz;
- una `action` o `subaction` invocada desde un `then` se incorpora a la resolución causal ya activa y no abre una raíz independiente;
- la resolución completa es atómica junto con todas sus ondas.

Los participantes son receptores y los `given` son argumentos conforme a D-036 y D-063. Al iniciar la acción se vinculan los roles por identidad, valor o lugar según su contrato, se comprueban sus tipos, cardinalidades y capacidades, se completan los `given` omitidos con sus predeterminados estáticos, se evalúan y validan todos ellos, y después se evalúa `if`. Un rol con `mut` exterior conserva el lugar receptor como destino de efectos y exige que sea almacenable y exteriormente mutable. Un `given` fuera de dominio o un `if` falso no producen efectos.

Dentro de un bloque `then`, D-066 permite vinculaciones locales calculadas. Se resuelven en orden textual, leen el delta privado anterior, quedan inmutables y no forman parte del estado del mundo.

### Secuencia unificada de `then`

No existe una clasificación semántica entre actions elementales y compuestas. Un `then` es una secuencia ordenada de consecuencias y puede mezclar vinculaciones locales, efectos directos, llamadas a `action` o `subaction` y recorridos `for each`.

Cada sentencia lee el delta privado visible en su posición textual. Una llamada interna se valida y ejecuta en ese punto, observa los efectos privados anteriores, aporta sus propios efectos a la misma resolución atómica y deja esos efectos visibles para las sentencias posteriores. No abre una transacción independiente.

Los `after` de todas las actions/subactions ejecutadas se comprueban contra el estado estable tentativo final de la resolución completa. El análisis de llamadas debe impedir ciclos ejecutables; Q-023 conserva abierta la demostración de aciclicidad e impacto cuando la selección del descriptor callable es dinámica, no la posibilidad de invocarlo.

### `after` y `old`

`if` y `after` pueden adjuntar mediante `otherwise` una razón `Text` para su falsedad. Su omisión es legal y produce una sugerencia, no un aviso, porque el rechazo es una respuesta normal; en ese caso se genera una razón a partir de la condición y su procedencia. El diagnóstico es puro y perezoso.

`after` se evalúa tras todas las ondas sobre el estado estable tentativo. Su falsedad produce `rejected`; un error durante su evaluación produce `failed`. Un error al evaluar `if` o `after` no queda capturado por `otherwise`, que solo explica una condición evaluada correctamente como falsa.

En el contexto de acciones y tests, `old e` lee `e` en el estado estable inmediatamente anterior a la acción exterior completa y solo está admitido dentro de `after`. D-058 añade un contexto distinto para `old` dentro de reglas reactivas, donde compara instantáneas de onda.

### Resultados

| Resultado | Causa |
| --- | --- |
| `accepted` | Solicitud válida, raíz compatible, estabilización, invariantes y `after` satisfechos |
| `rejected` | `given` fuera de dominio, `if` falso o `after` falso |
| `failed` | Conflicto, ciclo u oscilación, operación inválida, dominio o referencia inválidos, `always` incumplida o fallo semántico propagado |

La solicitud devuelve al invocador externo un objeto cuyo campo `state` contiene uno de esos tres resultados. Cuando contiene `rejected` o `failed`, el objeto incluye además un campo obligatorio `reason: Text` con la explicación humana. Todo caso normativo distinto de `accepted` debe proporcionar esa razón conforme a D-061; pueden acompañarla códigos y causas estructuradas.

Todo resultado distinto de `accepted` restaura exactamente el estado estable anterior y no publica mensajes ni otros efectos externos.

La normalización de un intervalo lineal con extremos invertidos a `empty` es una evaluación válida conforme a D-059 y no produce `failed` por sí misma. Un `given` que quede fuera de dominio o un `if` o `after` que resulte falso a causa de ese vacío producen `rejected`; un dominio que deje un valor almacenado inválido o una regla `always` incumplida producen `failed` por el estado tentativo resultante.

## Consecuencias

- `rejected` es una respuesta semántica normal; `failed` indica que no se pudo formar una transición válida.
- La atomicidad incluye raíz, ondas, `always`, `after` y salidas pendientes.
- Q-004 queda cerrada: un `after` falso revierte toda la resolución.
- Los valores de dominio devueltos por una acción, si llegaran a admitirse, siguen abiertos en Q-022.

## Verificación

1. Aceptación, rechazo por dominio de `given`, rechazo por `if` y rechazo por `after`.
2. Rollback completo de una acción rechazada al final.
3. `then` mixto con efectos, locales y llamadas en orden textual.
4. Propagación del delta privado a través de llamadas internas y rechazo de un ciclo ejecutable de llamadas.
5. `old` observa la acción exterior, no una hoja intermedia.
6. Vinculación de un receptor-lugar mutable y rechazo de un receptor que sea solo un valor.
7. Intervalo invertido normalizado a `empty` sin fallo intrínseco.
8. Distinción entre rechazo por una guarda falsa sobre `empty` y fallo por estado fuera de dominio.
9. Presencia obligatoria de `reason: Text` en `rejected` y `failed`, y ausencia en `accepted`.
10. Diagnósticos `otherwise` explícitos y generados para `if` y `after`, incluida la evaluación perezosa.

## Modificación vigente por D-096

Se retira la clasificación semántica entre action elemental y compuesta. Todo `then` es una secuencia ordenada que puede mezclar efectos, locales, llamadas y `for each`. Una llamada interna observa el delta privado del punto textual y aporta sus efectos a la misma resolución. `action` conserva capacidad de raíz exterior; `subaction` es reutilizable desde cualquier `then` pero no puede ser raíz exterior. Los `after` anidados se evalúan contra el estado estable tentativo final de la resolución completa.
