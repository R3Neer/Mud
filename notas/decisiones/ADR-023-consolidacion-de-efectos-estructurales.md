---
id: D-023
title: "Consolidación de efectos estructurales concurrentes"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-002"
  - "Q-006"
  - "Q-021"
  - "Q-046"
affects:
  - "[[notas/03-semantica-de-ejecucion]], futuros capítulos 25, 28, 29 y 31"
---
# ADR-023 — Consolidación de efectos estructurales concurrentes

- Actualizada: 2026-07-28 para usar el vocabulario de D-025
- Relacionada con: [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]]
- Preguntas relacionadas: [[notas/preguntas/Q-002-modelo-exacto-de-efectos-secuenciales-y-simultaneos|Q-002]], [[notas/preguntas/Q-006-conflictos|Q-006]], [[notas/preguntas/Q-021-analisis-estatico-de-conflictos|Q-021]], [[notas/preguntas/Q-046-creacion-inefectiva-dentro-de-una-raiz|Q-046]]
- Documentos afectados: [[notas/03-semantica-de-ejecucion]], futuros capítulos 25, 28, 29 y 31

## Contexto

Varias reglas pueden solicitar en la misma oleada:

- La activación de la misma `thing` mediante `create`.
- La activación de la misma regla.
- Activaciones y destrucciones incompatibles.
- Adiciones y retiradas sobre una misma estructura.

- Modificada por: [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]]
No siempre es decidible estáticamente si dos reglas producirán efectos en la misma oleada. La semántica tampoco puede depender del orden real en que hilos o estructuras internas recorran los `then`.

Al mismo tiempo, las instrucciones escritas dentro de un único `then` deben conservar su secuencialidad.

## Decisión: dos niveles de evaluación

Sea $W_i$ la instantánea común de una raíz u oleada y sean:

$$
t_1,\ldots,t_n
$$

los bloques `then` aplicables.

Cada $t_j$ se interpreta secuencialmente sobre una superposición privada:

$$
\Delta_j
$$

que comienza sobre $W_i$. Una instrucción posterior del mismo `then` puede observar los efectos anteriores de ese bloque.

Ningún `then` observa durante la misma oleada el delta parcial de otro `then`. La implementación puede intercalar o paralelizar su cálculo, pero esa planificación no es observable.

Al terminar todos los bloques, se normaliza cada delta privado y después se consolidan:

$$
\operatorname{merge}_{W_i}
(\Delta_1,\ldots,\Delta_n)
$$

La consolidación produce un único delta tentativo o un conflicto que hace fallar y revertir la resolución.

## Orden estructural entre bloques

Después de respetar y normalizar el orden interno de cada `then`, los efectos estructurales de bloques distintos se consolidan en este orden:

Una vinculación local `nombre [: tipo] := expresión` se evalúa una vez en su posición textual y puede leer la superposición privada producida por instrucciones anteriores del mismo bloque. No produce un delta y las instrucciones posteriores no recalculan su valor, conforme a D-066.

1. Activaciones `create` supervivientes.
2. Adiciones supervivientes.
3. Retiradas supervivientes.
4. Destrucciones supervivientes.

Por tanto, si un `then` solicita `create A` y otro solicita `destroy A`, el resultado consolidado deja `A` destruida.

Dentro de un único bloque sigue mandando el orden escrito:

```mud
then {
    create A
    destroy A
}
```

termina con una solicitud local de destrucción.

```mud
then {
    destroy A
    create A
}
```

termina con una solicitud local de activación. La normalización local debe conservar cualquier efecto intermedio observable dentro del propio bloque antes de calcular su estado final.

Esta regla no introduce una prioridad temporal oculta entre reglas: define una operación de consolidación declarativa sobre sus deltas.

## Varias activaciones de la misma declaración

Cada `thing` y regla posee una única definición canónica de primer nivel; toda aparición `create d` es una referencia de activación al mismo descriptor. Los aliases quedan fuera del sistema de activación.

Varias solicitudes concurrentes se consolidan idempotentemente:

$$
\{
\operatorname{create}(d),
\ldots,
\operatorname{create}(d)
\}
\rightsquigarrow
\operatorname{create}(d)
$$

Dos definiciones completas no llegan al runtime: son un error de buena formación, incluso si sus cuerpos son iguales. Si la declaración ya estaba activa en $W_i$, una regla cuya aplicabilidad exige esa activación no publica ninguno de sus efectos. Q-046 mantiene abiertos los casos generales de acciones y bloques con varias activaciones de disponibilidad mixta.

## Efectividad temporal

Las activaciones y destrucciones consolidadas producen la proyección efectiva de $W_{i+1}$. No alteran retrospectivamente:

- La instantánea leída por los `then` de la oleada actual.
- Los bindings fijados al comienzo de esa oleada.
- La memoria anterior usada por `when` durante esa oleada.

Las nuevas reglas y suspensiones afectan a la construcción de bindings y evaluación de la oleada siguiente.

## Consecuencias para análisis y runtime

- El compilador puede usar análisis conservadores sin tener que decidir toda coincidencia dinámica.
- El runtime necesita agrupar solicitudes por identidad y clase de efecto.
- Cada activación debe conservar procedencia para explicar su causa.
- La secuencialidad local puede implementarse mediante overlays sin publicar estados parciales.
- La traza causal debe indicar qué solicitudes idempotentes se consolidaron.
- Un conflicto dinámico estructural no produce commit ni estado parcial.

## Cuestiones abiertas

- Activaciones múltiples dentro de un mismo `then`.
- Resultado operativo de una acción cuya activación resulta inefectiva.
- Matriz completa de asignaciones, aritmética y operaciones de colección.
- Interacción exacta con acciones compuestas y sus hojas simultáneas.

## Verificación futura

La suite deberá cubrir:

1. Rechazo estático de dos definiciones de una misma `thing` o regla.
2. Consolidación idempotente de varias activaciones de una misma definición ausente.
3. Creación y destrucción desde bloques distintos, con destrucción final.
4. Orden inverso dentro de un único `then`.
5. Efectos visibles únicamente en la oleada siguiente.
