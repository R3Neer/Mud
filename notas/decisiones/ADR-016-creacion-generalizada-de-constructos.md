# ADR-016 — Creación generalizada de constructos

- Estado: Vigente
- Fecha: 2026-07-27
- Preguntas relacionadas: [[notas/08-preguntas-abiertas#Q-044 — Identidad y referencias a constructos futuros|Q-044]], [[notas/08-preguntas-abiertas#Q-045 — Contenido declarativo de create|Q-045]]
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
create A
```

crea un constructo concreto sin antecesores directos;

```mud
create abstract B from A
```

crea un constructo abstracto cuyo antecesor directo es `A`; y:

```mud
create D from A, B, C
```

crea un constructo concreto con los tres antecesores directos indicados.

Las variantes se combinan de manera uniforme:

```text
create [abstract] nombre [from lista-de-antecesores] [bloque]
```

El nombre nuevo aparece antes de `from`. La lista posterior a `from` denota un conjunto finito de antecesores directos y no establece prioridad por orden.

La creación modifica el mundo runtime. No añade texto al programa `.mud`, no modifica el historial Git y no convierte el constructo creado en una categoría ontológica distinta.

## Efecto semántico

Sea $\mathcal C$ un universo de identidades posibles de constructo y sea:

$$
\mathcal M
:=
\{
\mathsf{abstract},
\mathsf{concrete}
\}
$$

Una representación candidata del registro dinámico es:

$$
\operatorname{created}_W:
\mathcal C
\rightharpoonup
\left(
\mathcal M
\times
\mathcal P_{\mathrm{fin}}(\mathcal C)
\right)
$$

Su dominio:

$$
\mathcal D_W
:=
\operatorname{dom}(\operatorname{created}_W)
$$

es el conjunto de constructos creados y actualmente existentes.

Ejemplos:

$$
\operatorname{created}_W(\mathsf{A})
=
(\mathsf{concrete},\varnothing)
$$

$$
\operatorname{created}_W(\mathsf{B})
=
(\mathsf{abstract},\{\mathsf{A}\})
$$

$$
\operatorname{created}_W(\mathsf{D})
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
p\in\pi_2(\operatorname{created}_W(c))
\}
$$

El modo abstracto se deriva mediante la primera proyección. Un constructo raíz continúa perteneciendo a $\mathcal D_W$ aunque no contribuya ninguna arista a $R_W^{\mathrm{dir}}$.

Esta representación sustituye la candidata $\operatorname{base}_W$, que no podía representar raíces ni varias bases.

## Buena formación mínima

Una creación válida debe preservar:

- Frescura de la identidad creada respecto a los constructos existentes.
- Existencia de todos los antecesores indicados en `from`.
- Aciclicidad de la relación directa combinada.
- Compatibilidad de los esquemas heredados.
- Ausencia de estado concreto propio cuando el modo sea `abstract`.

La disponibilidad temporal de los nombres y el contenido permitido en el bloque permanecen abiertos en Q-044 y Q-045.

## Evaluación de la sintaxis

La sintaxis nueva es preferible porque:

- Coloca primero la identidad creada.
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
create D from A, B
```

son verdaderas:

```mud
D is D
D is A
D is B
```

y también cualquier relación obtenida transitivamente desde `A` o `B`.

## Consecuencias para el compilador y runtime

- El AST de `create` necesita un nombre nuevo, un indicador abstracto, una lista posiblemente vacía de antecesores y un bloque pendiente de precisar.
- La lista de antecesores debe resolverse antes de publicar el nuevo estado.
- La fusión de esquemas debe validarse para todas las bases.
- Un constructo raíz exige registrar su existencia independientemente de las aristas.
- Un constructo abstracto creado entra en el grafo, pero no aporta posiciones de estado concreto.
- Un constructo concreto creado se inicializa después de resolver su esquema efectivo.

## Cuestiones abiertas

- Si el nombre escrito por `create` designa una identidad global predecible o una vinculación local a una identidad fresca.
- Si una misma sentencia de creación puede ejecutarse varias veces.
- Si una regla estática puede mencionar exactamente un nombre aún no creado.
- Si el bloque puede declarar campos o predeterminados, o solo inicializar estado.
- Tratamiento de antecesores repetidos en la lista `from`.
- Visibilidad entre varias creaciones dentro de una misma raíz atómica.

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
