# ADR-045 — Resolución causal, vinculaciones y cola

- Estado: Vigente en su núcleo
- Fecha: 2026-07-28
- Modificada por: [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]], [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]]
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
3. se evalúan los activadores temporales de `when`;
4. cada `then` produce secuencialmente un delta privado;
5. los deltas se consolidan mediante D-023, D-046 y D-060;
6. los valores se normalizan a sus tipos básicos y se validan;
7. el estado resultante, si es válido, alimenta la onda siguiente.

Las vinculaciones se fijan al comienzo de la onda. Cambios de pertenencia, activaciones o suspensiones producidos durante ella solo alteran la siguiente. Ningún bloque observa deltas parciales de otro bloque.

La raíz y cada onda forman lotes causales con la misma frontera de consolidación. Para un destino `Natural`, todos los deltas aditivos compatibles se suman como enteros firmados y el total se satura una sola vez en cero antes de construir la instantánea siguiente. Ninguna regla observa el acumulador firmado.

Para una vinculación con memoria, los disparos comparan valores en las instantáneas de inicio de dos ondas consecutivas conforme a D-041 y D-058. Un `when e` puramente booleano detecta únicamente $\mathsf{false}\rightarrow\mathsf{true}$; `e changes` compara directamente ambos valores y puede pulsar en ondas consecutivas. `and` y `or` componen pulsos de cambio y transiciones booleanas sin convertirlos en estado persistente.

Una vinculación que no estaba presente en la primera instantánea materializada por `start with` se incorpora al conjunto en la primera onda posterior en que resulte activa. Esa onda inicializa toda su memoria temporal sin dispararla. Su primer disparo posible se produce en la onda siguiente. Las vinculaciones presentes desde la primera instantánea son la excepción expresa: cada rama booleana elevada comienza con anterior virtual `false` y puede pulsar durante la estabilización inicial; `changes` y `old` comparan esa instantánea consigo misma.

Una resolución termina cuando una onda no produce efectos ni nuevas consecuencias pendientes. Un ciclo u oscilación detectados producen `failed`; un límite de recursos es una salvaguarda técnica distinguible, no una definición alternativa de estabilización.

Solo hay una resolución causal activa por mundo. Las solicitudes externas que llegan durante ella entran en una cola y vinculan participantes, evalúan `given`, dominios e `if` cuando les corresponde comenzar, no cuando fueron encoladas.

Los `message` detectados se conservan como ocurrencias tentativas. Sus propiedades se calculan sobre el estado final y solo se publican al confirmar; una reversión no entrega ninguna.

## Consecuencias

- El orden de ejecución física no altera el resultado.
- La identidad canónica y la conservación de memoria tras desaparecer una vinculación siguen abiertas en Q-005; su valor inicial ya está fijado.
- La detección semántica de oscilaciones y la salvaguarda técnica siguen abiertas en Q-020.
- La multiplicidad, orden y deduplicación de mensajes siguen en Q-052.

## Verificación

1. Permutaciones del orden físico producen la misma transición.
2. Una vinculación creada en una onda solo participa en la siguiente.
3. Una acción encolada se valida contra el estado en que comienza.
4. Una oscilación no confirma estado parcial.
5. Una resolución revertida no publica mensajes.
6. Una vinculación inicial verdadera dispara durante la estabilización de `start with`.
7. Una vinculación creada en una onda toma línea base en la siguiente y solo puede disparar a partir de la posterior.
8. Dos cambios netos consecutivos producen dos pulsos `changes`.
9. Dos activadores unidos por `and` solo disparan cuando ambos pulsan en la misma onda.
10. Un cambio unido mediante `or` a una transición booleana preserva cualquiera de los dos pulsos.
11. Deltas `-2` y `+3` sobre un `Natural` inicial cero producen uno en la siguiente instantánea.
12. Ninguna instantánea de onda expone un `Natural` negativo.
