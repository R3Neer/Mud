# ADR-016 — Creación generalizada de constructos

- Estado: Vigente
- Fecha: 2026-07-27
- Preguntas resueltas: [[notas/08-preguntas-abiertas#Q-044 — Identidad y referencias a constructos futuros|Q-044]], [[notas/08-preguntas-abiertas#Q-045 — Contenido declarativo de create|Q-045]]
- Pregunta abierta relacionada: [[notas/08-preguntas-abiertas#Q-046 — Creación inefectiva dentro de una raíz|Q-046]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[especificacion/04-modelo-matematico]], futuro `24-acciones.md`, futuro `32-ciclo-de-vida-runtime.md`

## Contexto

La sintaxis inicial:

```mud
create EgyptianArmy AirForce {
}
```

presuponía una única base y no hacía evidente cuál de los dos nombres designaba el constructo nuevo. Tampoco podía expresar con naturalidad un constructo raíz, un constructo abstracto o especialización múltiple.

## Decisión

`create` admite las siguientes familias:

```mud
create A {
}
```

activa un constructo concreto sin antecesores directos;

```mud
create abstract B from A {
}
```

activa un constructo abstracto cuyo antecesor directo es `A`; y:

```mud
create D from A, B, C {
}
```

activa un constructo concreto con los tres antecesores directos indicados.

Las variantes se combinan de manera uniforme:

```text
create [abstract] nombre [from lista-de-antecesores] bloque
```

El nombre reservado aparece antes de `from`. La lista posterior a `from` denota un conjunto finito de antecesores directos y no establece prioridad por orden. El bloque es una declaración completa: puede contener las propiedades admitidas por una declaración ordinaria de constructo, no solo asignaciones de inicialización.

La creación modifica el mundo runtime. No añade texto al programa `.mud`, no modifica el historial Git y no convierte el constructo creado en una categoría ontológica distinta.

## Efecto semántico

Sea $\mathcal C$ un universo de identidades posibles de constructo. El análisis del programa reserva un conjunto:

$$
\mathcal R_P^{\mathsf{create}}
\subseteq
\mathcal C
$$

de identidades mencionadas como resultado de `create`. Cada aparición debe resolverse contra esa identidad incluso antes de que esté activa.

Sea $\mathcal B$ el espacio todavía abstracto de cuerpos declarativos completos y sea:

$$
\mathcal M
:=
\{
\mathsf{abstract},
\mathsf{concrete}
\}
$$

El descriptor resuelto de cada creación es:

$$
\operatorname{createDecl}_P:
\mathcal R_P^{\mathsf{create}}
\to
\left(
\mathcal M
\times
\mathcal P_{\mathrm{fin}}(\mathcal C)
\times
\mathcal B
\right)
$$

Sea $\mathcal E_W\subseteq\mathcal C$ el conjunto de todas las identidades activas en el mundo. Definimos:

$$
\mathcal D_W
:=
\mathcal E_W
\cap
\mathcal R_P^{\mathsf{create}}
$$

el conjunto de identidades reservadas mediante `create` que están activas en el mundo $W$. La vista activa del descriptor es la restricción:

$$
\operatorname{created}_W
:=
\left.
\operatorname{createDecl}_P
\right|_{\mathcal D_W}
$$

Por tanto:

$$
\operatorname{dom}(\operatorname{created}_W)
=
\mathcal D_W
$$

La reserva de identidad pertenece al programa resuelto; la presencia activa pertenece al mundo. No son una clase y una instancia, sino dos aspectos de la misma identidad semántica.

Para abreviar las dos primeras proyecciones, definimos:

$$
\operatorname{shape}_P(c)
:=
\left(
\pi_1(\operatorname{createDecl}_P(c)),
\pi_2(\operatorname{createDecl}_P(c))
\right)
$$

Ejemplos:

$$
\operatorname{shape}_P(\mathsf{A})
=
(\mathsf{concrete},\varnothing)
$$

$$
\operatorname{shape}_P(\mathsf{B})
=
(\mathsf{abstract},\{\mathsf{A}\})
$$

$$
\operatorname{shape}_P(\mathsf{D})
=
\left(
\mathsf{concrete},
\{\mathsf{A},\mathsf{B},\mathsf{C}\}
\right)
$$

La relación directa añadida por el mundo se deriva:

$$
R_W^{\mathrm{dir}}
:=
\{
(c,p)
\mid
c\in\mathcal D_W
\land
p\in\pi_2(\operatorname{shape}_P(c))
\}
$$

Las dos primeras proyecciones de $\operatorname{createDecl}_P$ recuperan el modo y los antecesores; la tercera recupera el cuerpo declarativo. Un constructo raíz continúa perteneciendo a $\mathcal D_W$ aunque no contribuya ninguna arista a $R_W^{\mathrm{dir}}$.

Esta representación sustituye la candidata $\operatorname{base}_W$, que no podía representar raíces ni varias bases.

## Buena formación mínima

Una creación efectiva exige que la identidad reservada no esté activa:

$$
c\notin\mathcal E_W
$$

Si nunca se creó o fue destruida, `create c` puede añadirla a $\mathcal E_W$. Si ya existe, no se crea una identidad alternativa.

Cuando `create c` pertenece a una regla, la ausencia es una condición de aplicabilidad de la regla completa:

$$
c\in\mathcal E_W
\implies
\text{la regla no se ejecuta}
$$

Por tanto, tampoco se publican otros efectos de esa ejecución de la regla. Q-046 conserva únicamente los casos todavía no decididos: acciones solicitadas y bloques con varias creaciones de disponibilidad mixta.

Una creación efectiva debe preservar además:

- Reserva y resolución previa de la identidad.
- Existencia de todos los antecesores indicados en `from`.
- Aciclicidad de la relación directa combinada.
- Compatibilidad de los esquemas heredados.
- Ausencia de estado concreto propio cuando el modo sea `abstract`.

Tras `destroy c`, una creación posterior reactiva la misma identidad reservada $c$ y vuelve a construir sus declaraciones y, si es concreta, su estado inicial. La política de destrucción cuando existen descendientes permanece abierta.

## Evaluación de la sintaxis

La sintaxis nueva es preferible porque:

- Coloca primero la identidad que se activará.
- Hace opcional la especialización sin introducir un antecesor ficticio.
- Expresa `abstract` como modificador del resultado.
- Admite especialización múltiple.
- Distingue la operación que añade relaciones (`from`) de la consulta posterior (`is`).
- Mantiene posiciones gramaticales suficientes para que el parser la reconozca sin ambigüedad.

El uso de `from` en otros efectos no causa por sí solo ambigüedad: el parser conoce que se encuentra dentro de una producción iniciada por `create`.

## Consecuencias para `is`

Cada nombre de la lista `from` añade una arista directa. El operador `is` continúa consultando la clausura reflexiva y transitiva de la relación directa combinada.

Por ejemplo, tras:

```mud
create D from A, B {
}
```

son verdaderas:

```mud
D is D
D is A
D is B
```

y también cualquier relación obtenida transitivamente desde `A` o `B`.

## Consecuencias para el compilador y runtime

- El AST de `create` necesita una identidad reservada, un indicador abstracto, una lista posiblemente vacía de antecesores y un cuerpo declarativo completo.
- La resolución de nombres debe registrar la identidad aunque ninguna ejecución la haya activado todavía.
- Las referencias exactas a esa identidad pueden resolverse antes de su activación; las operaciones que exijan presencia deberán comprobarla.
- La lista de antecesores debe resolverse antes de publicar el nuevo estado.
- La fusión de esquemas debe validarse para todas las bases.
- Las declaraciones locales del cuerpo se fusionan con el esquema heredado y se validan antes de publicar el nuevo estado.
- Un constructo raíz exige registrar su existencia independientemente de las aristas.
- Un constructo abstracto creado entra en el grafo, pero no aporta posiciones de estado concreto.
- Un constructo concreto creado se inicializa después de resolver su esquema efectivo.

## Cuestiones abiertas

- Resultado de una acción solicitada que contiene `create A` cuando `A` ya está activa.
- Aplicabilidad de una regla o acción con varias creaciones cuando solo algunas identidades están ausentes.
- Compatibilidad entre varias apariciones declarativas de `create A` en el mismo programa.
- Tratamiento de antecesores repetidos en la lista `from`.
- Visibilidad entre varias creaciones dentro de una misma raíz atómica.
- Destrucción de un constructo que todavía tiene descendientes activos.

## Verificación futura

La suite deberá cubrir:

1. Creación concreta sin antecesores.
2. Creación abstracta sin antecesores.
3. Creación concreta con una y varias bases.
4. Creación abstracta con una y varias bases.
5. Rechazo de una base inexistente.
6. Rechazo de incompatibilidades de herencia múltiple.
7. Conservación de aciclicidad.
8. Derivación reflexiva y transitiva de `is`.
9. Resolución de una referencia exacta antes de que la identidad esté activa.
10. Ineficacia de `create A` mientras `A` está activa.
11. Reactivación de la misma identidad tras `destroy A`.
12. Declaración de propiedades locales dentro del cuerpo de `create`.
