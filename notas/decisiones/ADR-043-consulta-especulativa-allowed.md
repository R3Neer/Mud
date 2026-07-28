# ADR-043 — Consulta especulativa `allowed`

- Estado: Vigente
- Fecha: 2026-07-28
- Preguntas relacionadas: Q-007, Q-035, Q-053
- Documentos afectados: expresiones, acciones, análisis de admisibilidad

## Contexto

Una regla debe poder preguntar si una acción sería admisible sin ejecutar una versión simplificada de ella ni alterar el mundo.

## Decisión

```mud
allowed game.Move(origin, destination)
allowed (source, destination).Transfer(amount)
```

`allowed call` evalúa la acción indicada mediante el mismo protocolo completo que una solicitud real, pero en una copia especulativa:

1. vincula participantes;
2. suministra y valida `given`;
3. evalúa `if`;
4. calcula y consolida la raíz;
5. ejecuta ondas hasta estabilizar;
6. comprueba `always`;
7. evalúa `after`;
8. descarta la copia.

La traducción de resultado es:

$$
\begin{aligned}
\mathsf{accepted} &\mapsto \mathsf{true},\\
\mathsf{rejected} &\mapsto \mathsf{false},\\
\mathsf{failed} &\mapsto \text{fallo propagado}.
\end{aligned}
$$

Un fallo no se degrada a falso.

La evaluación especulativa no modifica el mundo, la cola de acciones, los logs, el azar global ni el identificador de resolución. Si interviene azar, utiliza una rama concreta, sembrada y reproducible que no consume la rama de la ejecución real.

Cuando la acción declara un rol `for` con mutabilidad exterior, el receptor-lugar se resuelve dentro de la copia especulativa. Sus efectos nunca conservan una referencia de escritura hacia el mundo real.

`allowed` puede aparecer en reglas booleanas, `if`, `after`, `when`, reglas `always` y cuantificadores, siempre dentro de una expresión pura. El grafo de dependencias de admisibilidad debe ser acíclico.

## Consecuencias

- Una implementación puede reutilizar el motor transaccional ordinario, sustituyendo la confirmación por descarte.
- El coste o un límite de recursos no puede cambiar silenciosamente verdadero por falso.
- La identidad de subsemillas y la política de caché permanecen en Q-032 y Q-035.

## Verificación

1. Correspondencia de los tres resultados.
2. Igualdad de la traza interna entre ejecución real y especulativa con la misma rama.
3. Ausencia de mutaciones, mensajes y consumo de azar global.
4. Rechazo estático de ciclos de admisibilidad.
