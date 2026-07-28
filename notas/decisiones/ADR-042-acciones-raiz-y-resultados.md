# ADR-042 — Acciones, raíz y resultados

- Estado: Vigente
- Fecha: 2026-07-28
- Preguntas relacionadas: Q-002, Q-003, Q-004, Q-022, Q-023, Q-046
- Documentos afectados: frontera pública, efectos, solicitud de acciones, semántica de la raíz

## Contexto

Una acción es la frontera de escritura de MUD. Su contrato debe separar la inadmisibilidad esperable de una solicitud de los errores que impiden obtener un estado válido.

## Decisión

```mud
action Recruit for kingdom: Kingdom [mut]
given
    amount: Natural in 1..100
{
    if kingdom.treasury >= amount * kingdom.recruitmentCost
    then {
        kingdom.treasury -= amount * kingdom.recruitmentCost
        kingdom.soldiers += amount
    }
    after kingdom.soldiers >= old kingdom.soldiers
}
```

Una acción:

- declara participantes mediante `for`;
- puede declarar valores `given` y sus dominios;
- puede declarar `if` y `after`;
- debe declarar `then`;
- no declara `when` ni se activa automáticamente;
- puede solicitarse desde el exterior o desde otra acción;
- inicia una resolución causal y es atómica junto con todas sus ondas.

Los participantes son receptores y los `given` son argumentos conforme a D-036. Al iniciar la acción se vinculan participantes, se evalúan y validan los `given`, y después se evalúa `if`. Un `given` fuera de dominio o un `if` falso no producen efectos.

### Acciones elementales

Su `then` contiene efectos. Las instrucciones del bloque son secuenciales dentro de su delta privado y la acción es atómica para cualquier observador exterior.

### Acciones compuestas

Su `then` contiene exclusivamente llamadas a acciones. No se mezclan llamadas y efectos directos en el mismo `then`.

Todas las hojas de una composición:

1. leen el mismo estado estable inicial;
2. evalúan participantes, `given`, dominios e `if` sobre ese estado;
3. generan una raíz simultánea consolidada;
4. comprueban sus `after` después de estabilizar la resolución completa.

El grafo estático de llamadas entre acciones debe ser acíclico. La selección dinámica de acciones permanece abierta en Q-023.

### `after` y `old`

`after` se evalúa tras todas las ondas sobre el estado estable tentativo. Su falsedad produce `rejected`; un error durante su evaluación produce `failed`.

`old e` lee `e` en el estado estable inmediatamente anterior a la acción exterior completa. En MUD 1.0 solo está admitido dentro de `after`.

### Resultados

| Resultado | Causa |
| --- | --- |
| `accepted` | Solicitud válida, raíz compatible, estabilización, invariantes y `after` satisfechos |
| `rejected` | `given` fuera de dominio, `if` falso o `after` falso |
| `failed` | Conflicto, ciclo u oscilación, operación inválida, dominio o referencia inválidos, `always` incumplida o fallo propagado |

Todo resultado distinto de `accepted` restaura exactamente el estado estable anterior y no publica mensajes ni otros efectos externos.

## Consecuencias

- `rejected` es una respuesta semántica normal; `failed` indica que no se pudo formar una transición válida.
- La atomicidad incluye raíz, ondas, `always`, `after` y salidas pendientes.
- Q-004 queda cerrada: un `after` falso revierte toda la resolución.
- Los valores de dominio devueltos por una acción, si llegaran a admitirse, siguen abiertos en Q-022.

## Verificación

1. Aceptación, rechazo por dominio, rechazo por `if` y rechazo por `after`.
2. Rollback completo de una acción rechazada al final.
3. Acción elemental y compuesta válidas.
4. Rechazo de un `then` mixto y de un ciclo de llamadas.
5. `old` observa la acción exterior, no una hoja intermedia.
