# ADR-016 — Creación generalizada de `thing`

- Estado: Vigente
- Fecha: 2026-07-27
- Actualizada: 2026-07-28 para usar el vocabulario de D-025
- Modificada por: [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]]
- Preguntas resueltas: [[notas/08-preguntas-abiertas#Q-044 — Identidad y referencias a `thing` futuras|Q-044]], [[notas/08-preguntas-abiertas#Q-045 — Contenido declarativo de `create`|Q-045]]
- Pregunta abierta relacionada: [[notas/08-preguntas-abiertas#Q-046 — Creación inefectiva dentro de una raíz|Q-046]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[especificacion/04-modelo-matematico]], futuro `24-acciones.md`, futuro `32-ciclo-de-vida-runtime.md`

## Contexto

La sintaxis inicial:

```mud
create EgyptianArmy AirForce {
}
```

presuponía una única base y no hacía evidente cuál de los dos nombres designaba la nueva `thing`. Tampoco podía expresar con naturalidad una raíz, una `thing` abstracta o especialización múltiple.

## Decisión

`create` admite las siguientes familias:

```mud
create thing A {
}
```

activa una `thing` concreta sin antecesoras directas;

```mud
create abstract thing B as A {
}
```

activa una `thing` abstracta cuya antecesora directa es `A`; y:

```mud
create thing D as A, B, C {
}
```

activa una `thing` concreta con las tres antecesoras directas indicadas.

Las variantes se combinan de manera uniforme:

```text
create [abstract] thing nombre [as lista-de-antecesoras] bloque
```

El nombre reservado aparece antes de `as`. La lista posterior a `as` denota un conjunto finito de antecesoras directas y no establece prioridad por orden. El bloque es una declaración completa: puede contener las propiedades admitidas por una declaración ordinaria de `thing`, no solo asignaciones de inicialización.

La creación modifica el mundo runtime. No añade texto al programa `.mud`, no modifica el historial Git y no convierte la `thing` creada en una categoría ontológica distinta.

## Efecto semántico

Sea $\mathcal T$ el universo de identidades posibles de `thing`. El análisis del programa reserva un conjunto:

$$
\mathcal R_P^{\mathsf{create}}
\subseteq
\mathcal T
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

Sea $\mathcal S_P^{\mathsf{create}}$ el conjunto finito de apariciones de creación de `thing`. Cada aparición tiene un objetivo y un fragmento resueltos:

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
\mathcal P_{\mathrm{fin}}(\mathcal T)
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
\mathcal P_{\mathrm{fin}}(\mathcal T)
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

Sea $\mathcal E_W\subseteq\mathcal T$ el conjunto de identidades activas. La vista efectiva de las `thing` creadas es:

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

Las dos primeras proyecciones recuperan el modo y las antecesoras; la tercera recupera el cuerpo declarativo combinado. Una `thing` raíz continúa perteneciendo a $\operatorname{dom}(\operatorname{created}_W)$ aunque no contribuya ninguna arista a $R_W^{\mathrm{dir}}$.

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
- Existencia de todas las antecesoras indicadas en `as`.
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
- Distingue la operación que añade relaciones (`as`) de la consulta posterior (`is`).
- Mantiene posiciones gramaticales suficientes para que el parser la reconozca sin ambigüedad.

El uso independiente de `from` en operaciones como `remove x from collection` no causa ambigüedad: `from` ya no introduce especialización.

## Consecuencias para `is`

Cada nombre de la lista `as` añade una arista directa. El operador `is` continúa consultando la clausura reflexiva y transitiva de la relación directa combinada.

Por ejemplo, tras:

```mud
create thing D as A, B {
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

- El AST de `create` necesita una identidad reservada, un indicador abstracto, una lista posiblemente vacía de antecesoras y un cuerpo declarativo completo.
- La resolución de nombres debe registrar la identidad aunque ninguna ejecución la haya activado todavía.
- Las referencias exactas a esa identidad pueden resolverse antes de su activación; las operaciones que exijan presencia deberán comprobarla.
- La lista de antecesoras debe resolverse antes de publicar el nuevo estado.
- La fusión de esquemas debe validarse para todas las antecesoras.
- Las declaraciones locales del cuerpo se fusionan con el esquema heredado y se validan antes de publicar el nuevo estado.
- Una `thing` raíz exige registrar su existencia independientemente de las aristas.
- Una `thing` abstracta creada entra en el grafo, pero no aporta posiciones de estado concreto.
- Una `thing` concreta creada se inicializa después de resolver su esquema efectivo.

## Cuestiones abiertas

- Resultado de una acción solicitada que contiene `create A` cuando `A` ya está activa.
- Aplicabilidad de una regla o acción con varias creaciones cuando solo algunas identidades están ausentes.
- Compatibilidad entre varias apariciones declarativas de `create A` en el mismo programa.
- Tratamiento de antecesoras repetidas en la lista `as`.
- Visibilidad entre varias creaciones dentro de una misma raíz atómica.
- Combinación entre reactivación y nuevos fragmentos declarativos.

## Verificación futura

La suite deberá cubrir:

1. Creación concreta sin antecesoras.
2. Creación abstracta sin antecesoras.
3. Creación concreta con una y varias antecesoras.
4. Creación abstracta con una y varias antecesoras.
5. Rechazo de una antecesora inexistente.
6. Rechazo de incompatibilidades de especialización múltiple.
7. Conservación de aciclicidad.
8. Derivación reflexiva y transitiva de `is`.
9. Resolución de una referencia exacta antes de que la identidad esté activa.
10. Ineficacia de `create A` mientras `A` está activa.
11. Reactivación de la misma identidad y restauración de su carga tras `destroy A`.
12. Declaración de propiedades locales dentro del cuerpo de `create`.
