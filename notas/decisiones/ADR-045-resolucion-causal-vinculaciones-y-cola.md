# ADR-045 — Resolución causal, vinculaciones y cola

- Estado: Vigente en su núcleo
- Fecha: 2026-07-28
- Preguntas relacionadas: Q-003, Q-005, Q-020, Q-052
- Documentos afectados: semántica dinámica, reglas reactivas, mensajes

## Contexto

El resultado de MUD no puede depender del orden de evaluación de reglas, archivos, hilos o estructuras internas. Las reacciones se organizan en ondas sobre instantáneas.

## Decisión

Una resolución sigue esta secuencia:

```text
estado estable anterior
→ validación de la solicitud
→ raíz tentativa
→ onda 1
→ onda 2
→ …
→ estado estable tentativo
→ always y after
→ confirmar o revertir
```

En cada onda:

1. se construye el conjunto de vinculaciones `on` activas;
2. todas las reglas leen la misma instantánea de inicio;
3. se evalúan transiciones de `when` y pulsos de `changes`;
4. cada `then` produce secuencialmente un delta privado;
5. los deltas se consolidan mediante D-023 y D-046;
6. el estado resultante, si es válido, alimenta la onda siguiente.

Las vinculaciones se fijan al comienzo de la onda. Cambios de pertenencia, activaciones o suspensiones producidos durante ella solo alteran la siguiente. Ningún bloque observa deltas parciales de otro bloque.

Una resolución termina cuando una onda no produce efectos ni nuevas consecuencias pendientes. Un ciclo u oscilación detectados producen `failed`; un límite de recursos es una salvaguarda técnica distinguible, no una definición alternativa de estabilización.

Solo hay una resolución causal activa por mundo. Las solicitudes externas que llegan durante ella entran en una cola y vinculan participantes, evalúan `given`, dominios e `if` cuando les corresponde comenzar, no cuando fueron encoladas.

Los `message` detectados se conservan como ocurrencias tentativas. Sus propiedades se calculan sobre el estado final y solo se publican al confirmar; una reversión no entrega ninguna.

## Consecuencias

- El orden de ejecución física no altera el resultado.
- La identidad y memoria exactas de las vinculaciones siguen abiertas en Q-005.
- La detección semántica de oscilaciones y la salvaguarda técnica siguen abiertas en Q-020.
- La multiplicidad, orden y deduplicación de mensajes siguen en Q-052.

## Verificación

1. Permutaciones del orden físico producen la misma transición.
2. Una vinculación creada en una onda solo participa en la siguiente.
3. Una acción encolada se valida contra el estado en que comienza.
4. Una oscilación no confirma estado parcial.
5. Una resolución revertida no publica mensajes.
