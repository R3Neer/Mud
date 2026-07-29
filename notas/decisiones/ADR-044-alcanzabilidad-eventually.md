---
id: D-044
title: "Alcanzabilidad `eventually`"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-026"
  - "Q-027"
  - "Q-028"
  - "Q-029"
  - "Q-030"
  - "Q-031"
affects:
  - "expresiones, alcanzabilidad, finitud, terminación"
---
# ADR-044 — Alcanzabilidad `eventually`

- Preguntas relacionadas: Q-026 a Q-031
- Documentos afectados: expresiones, alcanzabilidad, finitud, terminación

## Contexto

`eventually` expresa una pregunta de alcanzabilidad sobre el propio modelo. Para conservar una respuesta decidible no puede ejecutarse sobre un espacio arbitrario.

## Decisión

```mud
eventually game.Checkmate(White)
    through game.Move

eventually game.Checkmate(White)
    through game.Move, game.Pass

eventually game.Checkmate(White)
    through [game.Move, game.Pass]
```

La expresión es verdadera si existe una secuencia finita de solicitudes aceptadas de las acciones admitidas por `through` que conduce a un estado donde el objetivo es verdadero. La secuencia vacía está incluida: el estado actual puede satisfacer el objetivo.

Cada arista explorada es una transición MUD completa con validación de solicitud, raíz, ondas, reglas `always` y `after`. Las solicitudes rechazadas no forman aristas; un fallo durante una transición no se convierte en una transición válida.

Los participantes y todos los `given` que deban generarse tienen que proceder de dominios finitos, enumerables y con orden canónico. Para un rol `for` colectivo se enumeran colecciones completas que satisfacen su contrato, no miembros que ocupen posiciones de receptor separadas. Si el rol posee mutabilidad exterior, también debe existir un conjunto finito, enumerable y canónico de lugares almacenados candidatos; no basta con enumerar sus valores actuales.

El compilador solo admite la expresión cuando demuestra, conservadoramente:

- finitud del espacio de estado relevante;
- enumerabilidad de todas las solicitudes;
- terminación de cada transición;
- comparabilidad y canonicalización de estados;
- ausencia de creación no acotada.

Si existe azar, la cuantificación es existencial sobre secuencias de resultados posibles de probabilidad positiva:

$$
\exists \vec a,\vec r.\;
\Pr(\vec r)>0
\land
W \xRightarrow[\vec r]{\vec a} W'
\land
W'\models goal.
$$

`through` acepta una o varias referencias a acciones mediante la sintaxis contextual de colección, con corchetes opcionales. Sus elementos son referencias a acciones, no llamadas con participantes y `given` ya fijados: el análisis enumera las solicitudes admisibles a partir de sus dominios.

El orden textual de las referencias no cambia la verdad de la consulta. El orden canónico de enumeración y la estrategia concreta de búsqueda no forman parte todavía del significado normativo, siempre que el algoritmo sea completo para el perfil admitido y termine. No se introduce recursión general en el lenguaje fuente.

## Consecuencias

- La incapacidad de demostrar las condiciones rechaza estáticamente el uso de `eventually`; no responde falso.
- El orden canónico de enumeración y la definición mínima de estado relevante siguen abiertos.
- La implementación inicial puede usar búsqueda en anchura, pero la elección solo será normativa si se decide que afecta a diagnósticos o testigos.

## Verificación

1. Objetivo verdadero mediante secuencia vacía.
2. Camino finito existente e inexistente.
3. Rechazo de un `given` infinito o no enumerable.
4. Rechazo de creación no acotada.
5. Caso aleatorio con resultado de probabilidad positiva.
