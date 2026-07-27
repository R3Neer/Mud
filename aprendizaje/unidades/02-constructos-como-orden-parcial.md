---
title: Unidad 02 — `Thing` como orden parcial
aliases:
  - Orden parcial de things
unit: 2
status: en-curso
level: 0-a-1
depends-on:
  - "[[aprendizaje/unidades/01-modelo-minimo-de-un-mundo]]"
concepts:
  - relación binaria
  - grafo dirigido
  - camino
  - clausura reflexiva y transitiva
  - orden parcial
  - grafo almacenado
  - grafo efectivo
  - identidad reservada
  - actividad
spec-chapters:
  - "[[especificacion/03-notacion]]"
  - "[[especificacion/04-modelo-matematico]]"
  - "[[especificacion/README#11. `Thing`, especialización e identidad]]"
decisions:
  - D-014
  - D-015
  - D-016
  - D-021
  - D-023
  - D-025
  - D-026
tags:
  - mud/aprendizaje
  - mud/unidad
---

# Unidad 02 — `Thing` como orden parcial

> [!abstract]
> Esta unidad formaliza la especialización actual de MUD. `as` declara aristas directas; `is` consulta una relación reflexiva y transitiva. Las `thing` concretas siguen siendo cosas con identidad y estado propio: no aparecen clases ni instancias.

## 1. Pregunta de MUD

Considera:

```mud
abstract thing Place {
}

thing Kingdom as Place {
}

thing Egypt as Kingdom {
}
```

Queremos justificar:

```mud
Egypt is Kingdom
Egypt is Place
Egypt is Egypt
```

y rechazar un ciclo como:

```mud
thing Place as Egypt {
}
```

La pregunta central es:

> ¿Qué estructura matemática permite declarar especialización múltiple, consultar antecesores indirectos y conservar un significado coherente cuando una `thing` se suspende?

## 2. Objetivos

Al terminar deberías poder:

1. Distinguir función y relación.
2. Representar especialización directa mediante pares ordenados.
3. Leer un camino en un grafo dirigido.
4. Calcular clausuras transitivas y reflexivas.
5. Demostrar que `is` forma un orden parcial bajo aciclicidad.
6. Incorporar `create` sin inventar identidades frescas.
7. Distinguir grafo almacenado y grafo efectivo.
8. Explicar el bypass de antecesores inactivos.
9. Distinguir reflexividad de `is` y membresía estricta de colecciones.
10. Distinguir `as` declarativo de `is` consultivo.

## 3. Prerrequisitos

De la Unidad 01:

- $\mathcal T_P$: identidades de `thing` reservadas.
- $\mathcal A_W$: declaraciones activas.
- Separación entre programa $P$ y mundo $W$.
- Pares ordenados, productos cartesianos y funciones parciales.

## 4. Función frente a relación

Una relación binaria entre $A$ y $B$ es un subconjunto:

$$
R\subseteq A\times B
$$

Una función:

$$
f:A\to B
$$

es una relación especial que asocia cada elemento de $A$ con exactamente un elemento de $B$.

La especialización no es, en general, una función porque MUD admite varios antecesores:

```mud
thing AmphibiousForce as LandForce, NavalForce {
}
```

Por tanto:

$$
(\mathsf{AmphibiousForce},\mathsf{LandForce})
\in R
$$

y:

$$
(\mathsf{AmphibiousForce},\mathsf{NavalForce})
\in R
$$

La orientación adoptada es:

$$
(\text{más específica},\text{antecesora})
$$

## 5. `as` declara la relación directa

Sea:

$$
R^{\mathsf{stored}}_{P,W}
\subseteq
\mathcal T_P\times\mathcal T_P
$$

la relación directa almacenada.

Una cabecera:

```mud
thing Egypt as Kingdom, Place {
}
```

aporta:

$$
(\mathsf{Egypt},\mathsf{Kingdom})
$$

$$
(\mathsf{Egypt},\mathsf{Place})
$$

`as` no pregunta si la relación es verdadera: introduce aristas en un descriptor conocido por el programa.

> [!rule] Decisión de MUD — D-025
> `thing` es la palabra reservada de la entidad y `as` introduce sus antecesores directos. `construct` y `from` son sintaxis histórica.

## 6. Caminos

Un camino no vacío desde $x$ hasta $y$ en $R$ es una secuencia:

$$
\langle v_0,v_1,\ldots,v_n\rangle
$$

tal que:

$$
v_0=x
$$

$$
v_n=y
$$

y, para todo $i<n$:

$$
(v_i,v_{i+1})\in R
$$

Con:

```mud
thing Kingdom as Place {
}

thing Egypt as Kingdom {
}
```

existe el camino:

$$
\langle
\mathsf{Egypt},
\mathsf{Kingdom},
\mathsf{Place}
\rangle
$$

## 7. Clausuras

La clausura transitiva $R^+$ contiene los pares unidos por uno o más pasos.

La clausura reflexiva y transitiva $R^*$ añade además la identidad:

$$
\operatorname{Id}_A
=
\{
(a,a)
\mid
a\in A
\}
$$

$$
R^*
=
\operatorname{Id}_A\cup R^+
$$

Por eso `Egypt is Egypt` puede ser verdadero sin almacenar un bucle:

$$
(\mathsf{Egypt},\mathsf{Egypt})
\notin
R^{\mathsf{stored}}_{P,W}
$$

pero:

$$
(\mathsf{Egypt},\mathsf{Egypt})
\in
\left(R^{\mathsf{stored}}_{P,W}\right)^*
$$

## 8. Aciclicidad

La relación directa es acíclica si no existe un camino no vacío que empiece y termine en la misma identidad.

El programa:

```mud
thing A as B {
}

thing B as A {
}
```

es inválido porque contiene:

$$
\langle\mathsf A,\mathsf B,\mathsf A\rangle
$$

La reflexividad de `is` no contradice esta regla:

- La relación directa no contiene $(A,A)$.
- Su clausura reflexiva sí lo contiene.

## 9. `is` como orden parcial

Sobre un conjunto portador $X$, una relación $\preceq$ es un orden parcial si es:

1. Reflexiva.
2. Transitiva.
3. Antisimétrica.

Definimos provisionalmente:

$$
x\preceq_{P,W}y
\iff
(x,y)
\in
\left(R^{\mathsf{eff}}_{P,W}\right)^*
$$

### Reflexividad

Por definición de clausura reflexiva:

$$
\forall x\in X.\ x\preceq_{P,W}x
$$

### Transitividad

Si existe un camino de $x$ a $y$ y otro de $y$ a $z$, su concatenación es un camino de $x$ a $z$.

### Antisimetría

Si $x\preceq y$ e $y\preceq x$ con $x\neq y$, los dos caminos formarían un ciclo no vacío. Como los ciclos se rechazan:

$$
x\preceq y
\land
y\preceq x
\implies
x=y
$$

> [!proof] Proposición
> Si la relación directa efectiva es acíclica, su clausura reflexiva y transitiva es un orden parcial.

## 10. Reserva, `create` y actividad

Una aparición:

```mud
create thing Memphis as Settlement {
}
```

no fabrica un nombre fresco cada vez. Al resolver $P$, `Memphis` ya pertenece a un conjunto de identidades reservadas:

$$
\mathcal R_P^{\mathsf{create}}
\subseteq
\mathcal T_P
$$

Cuando la creación es efectiva:

- `Memphis` entra en $\mathcal A_W$.
- Se materializa su carga si es la primera activación concreta.
- Sus fragmentos declarativos conocidos aportan aristas y esquema.

Después de `destroy Memphis`, el nombre, los fragmentos y la carga permanecen almacenados. Otro `create` reactiva la misma identidad.

Varias creaciones compatibles de una misma `thing` pueden aportar fragmentos fusionables. Esto no convierte la identidad en varias cosas.

## 11. Grafo almacenado y grafo efectivo

D-021 impide identificar sin más «arista almacenada» y «relación actualmente observable».

### Grafo almacenado

$$
R^{\mathsf{stored}}_{P,W}
$$

conserva las aristas declaradas aunque alguno de sus extremos esté suspendido.

### Portador efectivo

Para esta unidad:

$$
\mathcal T^{\mathsf{eff}}_{P,W}
=
\mathcal A_W\cap\mathcal T_P
$$

incluye las `thing` activas, abstractas o concretas.

### Bypass

La relación directa efectiva conecta dos identidades activas cuando el camino almacenado entre ellas no contiene otra identidad activa en medio:

$$
(x,y)\in R^{\mathsf{eff}}_{P,W}
$$

si y solo si existe:

$$
\langle
x=v_0,v_1,\ldots,v_n=y
\rangle
$$

en $R^{\mathsf{stored}}_{P,W}$, con $n\geq 1$, tal que:

$$
x,y\in\mathcal T^{\mathsf{eff}}_{P,W}
$$

y:

$$
\forall i\in\{1,\ldots,n-1\}.\,
v_i\notin\mathcal T^{\mathsf{eff}}_{P,W}
$$

Es decir: los nodos internos del camino están inactivos.

### Ejemplo

Antes:

```text
Egypt → Kingdom → Place
```

Si `Kingdom` se suspende:

```text
Egypt ─────────→ Place
        bypass
```

Las aristas almacenadas no se reescriben. La conexión `Egypt → Place` pertenece solo a la proyección efectiva y desaparece al reactivar `Kingdom`.

> [!intuition]
> El niño dice: «por ahora no jugamos con reinos, pero Egipto sigue siendo un lugar». No necesita borrar y reconstruir todo el árbol del juego.

## 12. Por qué el bypass conserva el orden

El bypass no inventa alcanzabilidad: cada arista efectiva corresponde a un camino almacenado.

Por tanto:

- No puede crear un ciclo que no existiera ya en el grafo almacenado.
- Conserva la orientación de más específico a antecesor.
- Su clausura sigue siendo reflexiva y transitiva.
- La aciclicidad almacenada permite conservar antisimetría.

La implementación puede comprimir caminos para consultar, pero la semántica se define mediante la relación, no mediante una optimización concreta.

## 13. `as` e `is` viven en niveles distintos

```mud
thing Egypt as Kingdom {
}
```

produce un nodo de declaración, conceptualmente:

```text
ThingDecl(
    name = Egypt,
    directAncestors = {Kingdom}
)
```

```mud
Egypt is Place
```

produce una expresión:

```text
IsExpression(Egypt, Place)
```

`as` modifica el descriptor directo. `is` consulta la clausura sobre la proyección efectiva aplicable.

## 14. Reflexividad no significa membresía exacta

`is` es reflexivo:

$$
\mathsf{Person}\ \mathsf{is}\ \mathsf{Person}
$$

pero una colección:

```mud
people: Person[*]
```

no puede contener el ancla exacta `Person`.

D-026 exige para cada miembro $c$:

$$
c\neq\mathsf{Person}
\land
c\ \mathsf{is}\ \mathsf{Person}
$$

Puede contener `Alice` si `Alice is Person`, incluso si la propiedad pertenece a `Alice`. La desigualdad se compara con el tipo escrito `Person`, no con la `thing` propietaria.

No existe `[reflexive]`.

## 15. Abstractas y concretas

Las abstractas y concretas pertenecen al mismo grafo.

- Una `thing` abstracta posee identidad y puede ser antecesora.
- No denota directamente una cosa concreta con carga de estado propia.
- Una `thing` concreta posee estado independiente.
- Ser antecesora no provoca propagación del estado mutable.

Si `Egypt is Kingdom`, modificar `Kingdom.treasury` no modifica `Egypt.treasury`. `is` afecta esquema y sustituibilidad, no es un canal de sincronización.

## 16. Relación con reglas y acciones

Con la sintaxis actual:

- Una regla de cambio que observa `Person` declara su vinculación mediante `on`.
- Una regla booleana, acción o `look` que recibe `Person` declara el participante mediante `for`.

En ambos casos, una identidad creada puede empezar a satisfacer el patrón cuando se activa. La identidad estaba reservada antes; lo que cambia es su presencia efectiva.

## 17. Qué es estándar y qué es de MUD

### Matemática estándar

- Relaciones binarias.
- Grafos dirigidos y caminos.
- Clausuras.
- Aciclicidad.
- Órdenes parciales.

### Convenciones de notación

- Aristas orientadas de específica a antecesora.
- $R^{\mathsf{stored}}$ para el grafo conservado.
- $R^{\mathsf{eff}}$ para la proyección activa con bypass.

### Decisiones de MUD

- Un único dominio de `thing`.
- Especialización múltiple.
- `as` declara y `is` consulta.
- Rechazo de ciclos.
- Identidades de `create` reservadas globalmente.
- `destroy` suspende sin borrar.
- Membresía de colecciones siempre estricta respecto del tipo.

## 18. Errores frecuentes

### Modelar un único padre

Una función `parent` no representa especialización múltiple.

### Meter reflexividad en el grafo directo

Los pares $(t,t)$ pertenecen a la clausura, no a las aristas declaradas.

### Confundir `is` con igualdad

`Egypt is Place` no implica `Egypt = Place`.

### Confundir suspensión con borrado

`destroy Kingdom` no elimina las aristas almacenadas ni la carga.

### Inferir membresía exacta desde reflexividad

Aunque `Person is Person`, `Person` no puede ser miembro de `Person[*]`.

### Propagar estado por especialización

El estado de cada `thing` concreta es independiente.

## 19. Lectura comentada

Lee:

$$
x\preceq_{P,W}y
$$

como:

> En la proyección efectiva del programa $P$ y el mundo $W$, $x$ es la misma `thing` que $y$ o existe un camino de especialización desde $x$ hasta $y$.

Lee:

$$
R^{\mathsf{eff}}_{P,W}
\subseteq
\left(R^{\mathsf{stored}}_{P,W}\right)^+
$$

como:

> Toda arista efectiva resume uno o más pasos realmente almacenados.

## 20. Tu turno

El ejercicio está en [[aprendizaje/ejercicios/02-orden-parcial-de-constructos-ejercicio]].

> [!exercise] Objetivo
> Construir los grafos almacenado y efectivo antes y después de suspender un antecesor, calcular consultas `is` y aplicar la membresía estricta.

> [!hint]- Pista 1
> No borres ninguna arista al ejecutar `destroy`.

> [!hint]- Pista 2
> Para cada bypass busca un camino cuyos nodos internos estén inactivos.

## 21. Incorporación a la especificación

Podrán promoverse:

- El universo de identidades reservadas.
- Las relaciones almacenada y efectiva.
- La definición formal del bypass.
- La clausura consultada por `is`.
- La prueba de orden parcial.
- La interacción con membresía estricta.

Antes de publicar habrá que cerrar el comportamiento diagnóstico de una consulta `is` cuyos operandos estén inactivos.

## 22. Repaso

Comprueba que puedes:

1. Explicar por qué especialización es relación y no función.
2. Construir $R^*$ sin introducir bucles directos.
3. Demostrar antisimetría mediante aciclicidad.
4. Explicar reserva frente a actividad.
5. Calcular un bypass.
6. Explicar por qué `is` reflexivo no permite almacenar el tipo exacto.
