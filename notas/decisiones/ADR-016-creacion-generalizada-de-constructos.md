# ADR-016 — Creación generalizada de constructos

- Estado: Vigente
- Fecha: 2026-07-27
- Modificada por: [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]]
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
create construct A {
}
```

activa un constructo concreto sin antecesores directos;

```mud
create abstract construct B from A {
}
```

activa un constructo abstracto cuyo antecesor directo es `A`; y:

```mud
create construct D from A, B, C {
}
```

activa un constructo concreto con los tres antecesores directos indicados.

Las variantes se combinan de manera uniforme:

```text
create [abstract] construct nombre [from lista-de-antecesores] bloque
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

Sea $\mathcal S_P^{\mathsf{create}}$ el conjunto finito de apariciones de creación de constructo. Cada aparición tiene un objetivo y un fragmento resueltos:

$$
\operatorname{createTarget}_P:
\mathcal S_P^{\mathsf{create}}
\to
\mathcal R_P^{\mathsf{create}}
$$

$$
\operatorname{createFragment}_P:
\mathcal S_P^{\mathsf{create}}
\to
\left(
\mathcal M
\times
\mathcal P_{\mathrm{fin}}(\mathcal C)
\times
\mathcal B
\right)
$$

D-023 permite que varias apariciones dirigidas a la misma identidad aporten fragmentos compatibles en una oleada. Su combinación parcial se escribe $\sqcup$. Por tanto, el descriptor materializado no es una función fija del programa para cada identidad, sino estado almacenado del mundo:

$$
\operatorname{storedCreate}_W:
\mathcal R_P^{\mathsf{create}}
\rightharpoonup
\left(
\mathcal M
\times
\mathcal P_{\mathrm{fin}}(\mathcal C)
\times
\mathcal B
\right)
$$

Cuando una oleada solicita por primera vez las apariciones $S_c\subseteq\mathcal S_P^{\mathsf{create}}$ cuyo objetivo común es $c$, se exige que:

$$
\bigsqcup_{s\in S_c}
\operatorname{createFragment}_P(s)
$$

esté definida. El resultado se almacena en $\operatorname{storedCreate}_{W'}(c)$.

Sea $\mathcal E_W\subseteq\mathcal C$ el conjunto de identidades activas. La vista efectiva de los constructos creados es:

$$
\operatorname{created}_W
:=
\left.
\operatorname{storedCreate}_W
\right|_{
\mathcal E_W
\cap
\operatorname{dom}(\operatorname{storedCreate}_W)
}
$$

La reserva y los fragmentos pertenecen al programa resuelto; el descriptor combinado almacenado y su presencia efectiva pertenecen al mundo. No son una clase y una instancia, sino aspectos del ciclo de vida de la misma identidad semántica.

$$
\operatorname{shape}_W(c)
:=
\left(
\pi_1(\operatorname{storedCreate}_W(c)),
\pi_2(\operatorname{storedCreate}_W(c))
\right)
$$

La relación directa añadida por el mundo se deriva:

$$
R_W^{\mathrm{dir}}
:=
\{
(c,p)
\mid
c\in\operatorname{dom}(\operatorname{created}_W)
\land
p\in\pi_2(\operatorname{shape}_W(c))
\}
$$

Las dos primeras proyecciones recuperan el modo y los antecesores; la tercera recupera el cuerpo declarativo combinado. Un constructo raíz continúa perteneciendo a $\operatorname{dom}(\operatorname{created}_W)$ aunque no contribuya ninguna arista a $R_W^{\mathrm{dir}}$.

Esta representación sustituye tanto la candidata $\operatorname{base}_W$, que no podía representar raíces ni varias bases, como la función única $\operatorname{createDecl}_P$, que no podía representar la fusión dinámica de fragmentos decidida posteriormente.

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

Tras `destroy c`, una creación posterior reactiva la misma identidad reservada $c$. Conforme a D-021, la estructura y el estado almacenados no se reinicializan: vuelven a la proyección efectiva. La política de fusión con nuevos fragmentos declarativos permanece abierta.

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
create construct D from A, B {
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
- Combinación entre reactivación y nuevos fragmentos declarativos.

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
11. Reactivación de la misma identidad y restauración de su carga tras `destroy A`.
12. Declaración de propiedades locales dentro del cuerpo de `create`.
