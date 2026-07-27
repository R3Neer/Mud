# ADR-023 — Consolidación de efectos estructurales concurrentes

- Estado: Vigente para efectos estructurales; no cierra la matriz general de conflictos
- Fecha: 2026-07-27
- Modificada por: [[notas/decisiones/ADR-024-definicion-unica-y-activacion-abreviada|D-024]]
- Preguntas relacionadas: [[notas/08-preguntas-abiertas#Q-002 — Modelo exacto de efectos secuenciales y simultáneos|Q-002]], [[notas/08-preguntas-abiertas#Q-006 — Conflictos|Q-006]], [[notas/08-preguntas-abiertas#Q-021 — Análisis estático de conflictos|Q-021]], [[notas/08-preguntas-abiertas#Q-046 — Creación inefectiva dentro de una raíz|Q-046]]
- Documentos afectados: [[notas/03-semantica-de-ejecucion]], futuros capítulos 25, 28, 29 y 31

## Contexto

> [!note] Vocabulario histórico
> D-025 sustituyó `construct`/`from` por `thing`/`as`. La consolidación decidida aquí sigue vigente; sus ejemplos conservan la sintaxis histórica.

Varias reglas pueden solicitar en la misma oleada:

- La creación del mismo constructo.
- La activación de la misma regla.
- Creaciones y destrucciones incompatibles.
- Adiciones y retiradas sobre una misma estructura.

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

1. Creaciones supervivientes.
2. Adiciones supervivientes.
3. Retiradas supervivientes.
4. Destrucciones supervivientes.

Por tanto, si un `then` solicita `create A` y otro solicita `destroy A`, el resultado consolidado deja `A` destruida.

Dentro de un único bloque sigue mandando el orden escrito:

```mud
then {
    create construct A {
    }
    destroy A
}
```

termina con una solicitud local de destrucción.

```mud
then {
    destroy A
    create construct A {
    }
}
```

termina con una solicitud local de creación. La normalización local debe conservar cualquier efecto intermedio observable dentro del propio bloque antes de calcular su estado final.

Esta regla no introduce una prioridad temporal oculta entre reglas: define una operación de consolidación declarativa sobre sus deltas.

## Varias creaciones del mismo constructo

Si el constructo estaba ausente en $W_i$, las solicitudes concurrentes se fusionan mediante una operación parcial:

$$
D_1\sqcup\cdots\sqcup D_m
$$

Los antecesores directos se unen sin prioridad por orden. Los campos homónimos se combinan con las reglas de herencia múltiple:

- Tipo, dominio, cardinalidad, mutabilidad, capacidad, unicidad, orden y naturaleza almacenada o calculada deben ser compatibles.
- Si ninguna aparición declara valor inicial, se obtiene un único campo.
- Si exactamente una aparición declara valor inicial, se conserva ese valor.
- Si dos o más apariciones declaran valor inicial, existe conflicto, aunque los valores escritos sean iguales.

Si la operación $\sqcup$ no está definida, la resolución falla y revierte.

La fusión es idempotente respecto de la activación de identidad, pero no convierte cuerpos incompatibles en una declaración arbitraria.

Si el constructo ya estaba activo en $W_i$, se conserva la regla de D-016: una regla cuya aplicabilidad exige esa creación no publica ninguno de sus efectos. Q-046 mantiene abiertos los casos generales de acciones y bloques con varias creaciones de disponibilidad mixta.

## Varias activaciones de la misma regla o alias

D-024 sustituye el conflicto dinámico que este ADR establecía inicialmente. Cada regla y alias posee una única definición completa; las demás apariciones son referencias de activación al mismo descriptor.

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

Dos definiciones completas no llegan al runtime: son un error de buena formación, incluso si sus cuerpos son iguales.

## Efectividad temporal

Las creaciones y destrucciones consolidadas producen la proyección efectiva de $W_{i+1}$. No alteran retrospectivamente:

- La instantánea leída por los `then` de la oleada actual.
- Los bindings fijados al comienzo de esa oleada.
- La memoria anterior usada por `when` durante esa oleada.

Las nuevas reglas y suspensiones afectan a la construcción de bindings y evaluación de la oleada siguiente.

## Consecuencias para análisis y runtime

- El compilador puede usar análisis conservadores sin tener que decidir toda coincidencia dinámica.
- El runtime necesita agrupar solicitudes por identidad y clase de efecto.
- Las creaciones de constructo deben conservar procedencia de cada fragmento para diagnosticar conflictos.
- La secuencialidad local puede implementarse mediante overlays sin publicar estados parciales.
- La traza causal debe indicar qué solicitudes se fusionaron y qué regla aportó cada fragmento.
- Un conflicto dinámico estructural no produce commit ni estado parcial.

## Cuestiones abiertas

- Combinación de una recreación con fragmentos que no estaban presentes en la carga almacenada.
- Creaciones múltiples dentro de un mismo `then`.
- Resultado operativo de una acción cuya creación resulta inefectiva.
- Matriz completa de asignaciones, aritmética y operaciones de colección.
- Interacción exacta con acciones compuestas y sus hojas simultáneas.

## Verificación futura

La suite deberá cubrir:

1. Dos fragmentos compatibles del mismo constructo.
2. Unión de antecesores.
3. Campo homónimo sin inicializadores.
4. Un único inicializador entre varios fragmentos.
5. Conflicto por dos inicializadores iguales y distintos.
6. Conflicto de tipo, dominio, cardinalidad y mutabilidad.
7. Rechazo estático de dos definiciones de la misma regla o alias.
8. Consolidación idempotente de varias activaciones de la misma regla o alias.
9. Creación y destrucción desde bloques distintos, con destrucción final.
10. Orden inverso dentro de un único `then`.
11. Efectos visibles únicamente en la oleada siguiente.
