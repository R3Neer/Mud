---
title: Unidad 01 — Programa, mundo y store mínimo
aliases:
  - Modelo mínimo actual de MUD
unit: 1
status: vigente
level: 0-a-1
depends-on: []
concepts:
  - programa resuelto
  - mundo
  - thing
  - identidad
  - posición de estado
  - función parcial
  - store
  - buena formación
spec-chapters:
  - "[[especificacion/03-notacion]]"
  - "[[especificacion/04-modelo-matematico]]"
decisions:
  - D-014
  - D-017
  - D-019
  - D-021
  - D-025
  - D-026
tags:
  - mud/aprendizaje
  - mud/unidad
---

# Unidad 01 — Programa, mundo y store mínimo

> [!abstract]
> Esta unidad construye el modelo matemático mínimo de MUD con la ontología actual. No hay clases ni instancias: `Gate`, `NorthGate` y cualquier identidad creada son `thing` del mismo dominio. La versión anterior de la unidad se conserva en [[aprendizaje/historico/01-modelo-clase-instancia/README|el archivo histórico]].

## 1. Pregunta de MUD

Partimos de:

```mud
abstract thing Gate {
    unlocked: Bool
    open: Bool
}

thing NorthGate as Gate {
    unlocked = true
    open = false
}
```

Queremos responder:

> ¿Qué información pertenece al programa y qué información pertenece al mundo para poder decir formalmente que `NorthGate` está activa, desbloqueada y cerrada?

La pregunta parece sencilla, pero obliga a separar:

- Identidades y declaraciones conocidas por el programa.
- Presencia efectiva en un mundo.
- Propiedades aplicables.
- Valores almacenados.
- Información retenida aunque una declaración se suspenda.

## 2. Objetivos

Al terminar deberías poder:

1. Distinguir programa resuelto y mundo.
2. Explicar por qué una `thing` no es una clase con instancias.
3. Leer conjuntos, pares ordenados y productos cartesianos.
4. Distinguir función total y parcial.
5. Modelar un store mediante posiciones `(thing, propiedad)`.
6. Explicar por qué el conjunto de identidades no necesita repetirse dentro del mundo.
7. Formular una condición sencilla de buena formación.
8. Distinguir información almacenada de proyección efectiva.

## 3. Prerrequisitos

- Notación elemental de conjuntos.
- Idea informal de función.
- Ningún conocimiento previo de semántica formal.

## 4. Una sola ontología de `thing`

> [!rule] Decisión de MUD — D-014
> Las `thing` declaradas inicialmente y las introducidas por `create` pertenecen al mismo dominio conceptual. Una `thing` concreta posee identidad y estado propio; no es una instancia de otra.

En el ejemplo:

- `Gate` es una `thing` abstracta.
- `NorthGate` es una `thing` concreta.
- `NorthGate as Gate` declara una arista de especialización.
- `NorthGate is Gate` será una consulta verdadera.

No existe una identidad adicional como `northGate#1`. `NorthGate` ya es la cosa.

Esto no impide que `NorthGate` sea a su vez antecesora de otras `thing`. MUD unifica deliberadamente «cosa concreta» y «posible categoría más específica».

## 5. Programa resuelto y mundo

Llamaremos $P$ al programa resuelto. Contiene información que no depende del estado momentáneo:

- Identidades reservadas.
- Descriptores de declaraciones.
- Propiedades declaradas.
- Tipos, cardinalidades y predeterminados.
- Relaciones directas introducidas por `as`.
- Cuerpos conocidos de `create`.

Llamaremos $W$ a un mundo. Contiene información que puede variar:

- Qué declaraciones están activas.
- Qué cargas han sido materializadas.
- Qué valores están almacenados.
- Memoria operacional necesaria para reglas y ondas.

> [!intuition]
> El programa dice qué piezas y reglas podría tener el juego. El mundo dice cuáles están ahora sobre el suelo y en qué estado se encuentran.

## 6. Conjuntos del fragmento

Para esta unidad usamos:

$$
\mathcal T_P
$$

conjunto finito de identidades de `thing` reservadas por $P$;

$$
\mathcal F_P
$$

conjunto de anclas de propiedades conocidas;

$$
\mathcal V_P
$$

universo de valores representables en el fragmento.

Para el ejemplo:

$$
\mathcal T_P
=
\{
\mathsf{Gate},
\mathsf{NorthGate}
\}
$$

$$
\mathcal F_P
=
\{
\mathsf{Gate::unlocked},
\mathsf{Gate::open}
\}
$$

No usamos un conjunto separado de «objetos». Hacerlo introduciría otra vez la ontología descartada.

## 7. Pares ordenados y posiciones

Un par ordenado:

$$
(t,f)
$$

puede leerse como «la posición de la propiedad $f$ en la `thing` $t$».

El producto cartesiano:

$$
\mathcal T_P\times\mathcal F_P
$$

contiene todas las combinaciones posibles, incluidas muchas sin sentido. Por ejemplo, una propiedad puede no pertenecer al esquema efectivo de una `thing`.

Definimos provisionalmente:

$$
\operatorname{fields}_P(t)
$$

como el conjunto de propiedades efectivas de $t$. La Unidad 03 explicará cómo se deriva mediante herencia y fusión.

Las posiciones almacenables son:

$$
\operatorname{Pos}_P
=
\{
(t,f)
\mid
t\in\mathcal T_P
\land
f\in\operatorname{fields}_P(t)
\land
\operatorname{stored}_P(f)
\}
$$

La barra vertical se lee «tal que».

## 8. Funciones y funciones parciales

Una función total:

$$
g:A\to B
$$

asocia a cada elemento de $A$ exactamente un elemento de $B$.

Una función parcial:

$$
g:A\rightharpoonup B
$$

puede no estar definida para algunos elementos de $A$.

El store puede escribirse de dos formas equivalentes si se eligen bien los dominios:

$$
\operatorname{store}_W:
\mathcal T_P\times\mathcal F_P
\rightharpoonup
\mathcal V_P
$$

o:

$$
\operatorname{store}_W:
\operatorname{Pos}^{\mathsf{mat}}_{P,W}
\to
\mathcal V_P
$$

La primera usa un dominio grande y parcialidad. La segunda usa únicamente las posiciones materializadas y es total sobre ellas.

> [!intuition]
> «Parcial» no significa incompleto ni defectuoso. Significa que preguntas como «¿cuál es el tesoro de una puerta?» no tienen por qué recibir un valor inventado.

## 9. Dominio de una función

El dominio efectivo de una función parcial $g$ es:

$$
\operatorname{dom}(g)
=
\{
x
\mid
g(x)\downarrow
\}
$$

El símbolo $\downarrow$ se lee «está definido».

Para el ejemplo:

$$
\operatorname{dom}(\operatorname{store}_W)
=
\{
(\mathsf{NorthGate},\mathsf{Gate::unlocked}),
(\mathsf{NorthGate},\mathsf{Gate::open})
\}
$$

y:

$$
\operatorname{store}_W
(\mathsf{NorthGate},\mathsf{Gate::unlocked})
=
\operatorname{singleton}(\mathsf{true})
$$

$$
\operatorname{store}_W
(\mathsf{NorthGate},\mathsf{Gate::open})
=
\operatorname{singleton}(\mathsf{false})
$$

Usamos `singleton` porque todo campo MUD denota una colección. Omitir `[1]` es azúcar de cardinalidad, no convierte el campo en un escalar distinto.

## 10. Actividad, materialización y suspensión

D-021 obliga a distinguir tres ideas:

1. Una identidad está reservada porque aparece en el programa.
2. Su carga puede haber sido materializada y permanecer almacenada.
3. La declaración puede estar activa o suspendida.

Sea:

$$
\mathcal M_W\subseteq\mathcal T_P
$$

el conjunto de `thing` concretas cuya carga ya se materializó, y:

$$
\mathcal A_W\subseteq\mathcal T_P
$$

el conjunto de declaraciones activas.

No exigimos:

$$
\mathcal A_W=\mathcal M_W
$$

porque `destroy NorthGate` puede retirar `NorthGate` de la proyección efectiva sin borrar sus valores almacenados. Una reactivación posterior recupera la carga.

En el mundo inicial del ejemplo:

$$
\mathsf{NorthGate}
\in
\mathcal A_W\cap\mathcal M_W
$$

## 11. Modelo mínimo del mundo

Para el fragmento estudiado:

$$
W
=
\left(
\mathcal A_W,
\mathcal M_W,
\operatorname{store}_W
\right)
$$

No incluimos $\mathcal T_P$, $\mathcal F_P$ ni las relaciones declaradas porque ya pertenecen a $P$.

> [!warning]
> Esta terna no pretende ser todavía el modelo completo del runtime. Faltan reglas, aliases, vinculaciones, memoria de `when`, azar y trazas. Es un corte matemático suficiente para estudiar identidad, actividad y estado almacenado sin afirmar más.

## 12. Buena formación

Escribiremos:

$$
P\vdash W\ \mathsf{wf}
$$

para decir «$W$ está bien formado respecto de $P$».

En este fragmento exigimos:

1. $\mathcal A_W\subseteq\mathcal T_P$.
2. $\mathcal M_W\subseteq\mathcal T_P$.
3. Toda `thing` concreta activa está materializada:

   $$
   \mathcal A_W\cap\mathcal T_P^{\mathsf{concrete}}
   \subseteq
   \mathcal M_W
   $$

4. Toda posición del store es aplicable y almacenada.
5. Todo valor pertenece al tipo y dominio de la propiedad.
6. Toda posición almacenada obligatoria de una carga materializada tiene valor.

La cardinalidad exacta y los dominios se formalizarán después. D-026 ya fija que una modificación aceptable debe demostrar la cardinalidad final de cada `then` y de su consolidación.

## 13. Información redundante

Podríamos añadir un conjunto:

$$
\mathcal I_W
=
\{
t\mid\exists f.\,(t,f)\in
\operatorname{dom}(\operatorname{store}_W)
\}
$$

pero sería derivable del store y además no distinguiría bien una `thing` activa sin propiedades almacenadas.

La lección general es:

> [!definition]
> Una estructura formal no debe incluir como componente independiente información que puede derivarse sin pérdida de los demás componentes, salvo que exista una razón operacional explícita.

Aquí $\mathcal A_W$ sí merece ser explícito: no se deriva del store, porque una declaración suspendida conserva carga y una declaración activa puede no tener propiedades.

## 14. Igualdad de mundos en el fragmento

Para este corte:

$$
W_1=W_2
$$

si y solo si:

$$
\mathcal A_{W_1}=\mathcal A_{W_2}
\land
\mathcal M_{W_1}=\mathcal M_{W_2}
\land
\operatorname{store}_{W_1}
=
\operatorname{store}_{W_2}
$$

El modelo completo podría añadir componentes semánticamente observables. No deben añadirse a escondidas cuando llegue el runtime.

## 15. Qué es estándar y qué es de MUD

### Matemática estándar

- Conjuntos y subconjuntos.
- Pares ordenados y productos cartesianos.
- Funciones totales y parciales.
- Dominio de una función.
- Igualdad componente a componente.

### Convenciones de esta formalización

- $\mathcal T_P$ para identidades de `thing`.
- $\mathcal F_P$ para propiedades.
- $\mathcal A_W$ para actividad.
- $\mathcal M_W$ para cargas materializadas.
- $\operatorname{store}_W$ para valores almacenados.

### Decisiones de MUD

- Un único dominio de `thing`, sin clases e instancias.
- Identidades globales reservadas.
- Campos interpretados como colecciones.
- Valores predeterminados para todo tipo bien formado.
- Suspensión lógica distinta de eliminación.

## 16. Errores frecuentes

### Volver a introducir instancias

Es incorrecto inventar `northGate#1` como objeto de tipo `Gate`. `NorthGate` ya es la identidad concreta.

### Confundir programa y mundo

Una propiedad declarada pertenece a $P$. Su valor actual pertenece a $W$.

### Hacer total el store sobre combinaciones imposibles

Una función total sobre $\mathcal T_P\times\mathcal F_P$ obligaría a fabricar valores para propiedades no aplicables.

### Derivar actividad desde el store

No funciona: una `thing` destruida conserva carga y una `thing` sin propiedades puede estar activa.

### Confundir sintaxis omitida con semántica distinta

`Bool` y `Bool[1]` tienen la misma cardinalidad. La omisión solo es azúcar.

## 17. Lectura comentada

Lee:

$$
\operatorname{store}_W:
\operatorname{Pos}^{\mathsf{mat}}_{P,W}
\to
\mathcal V_P
$$

como:

> En el mundo $W$, el store asigna exactamente un valor MUD a cada posición almacenada materializada.

Lee:

$$
\mathcal A_W\subseteq\mathcal T_P
$$

como:

> Todo lo activo en el mundo debe haber sido reservado por el programa.

## 18. Tu turno

El ejercicio actualizado está en [[aprendizaje/ejercicios/01-modelo-minimo-ejercicio]].

> [!exercise] Objetivo
> Modelar un mundo con `NorthGate` activa y `SouthGate` materializada pero suspendida, sin introducir instancias ni repetir dentro de $W$ la información estática de $P$.

> [!hint]- Pista 1
> Separa primero $\mathcal T_P$, $\mathcal A_W$ y $\mathcal M_W$.

> [!hint]- Pista 2
> Pregúntate qué pares deben pertenecer al dominio del store aunque su `thing` no sea efectiva.

## 19. Incorporación a la especificación

De esta unidad podrán promoverse:

- La separación entre $P$ y $W$.
- El dominio único de identidades de `thing`.
- La distinción entre reserva, materialización y actividad.
- La forma general del store.
- Las primeras condiciones de buena formación.

Antes de publicar habrá que integrar formalmente esquema heredado, aliases, reglas, vinculaciones y proyección efectiva.

## 20. Repaso

Comprueba que puedes explicar:

1. Por qué `NorthGate` no es una instancia de `Gate`.
2. Por qué el store puede verse como función parcial.
3. Por qué actividad y materialización son conjuntos distintos.
4. Por qué $\mathcal T_P$ pertenece al programa y no se repite en el mundo.
5. Qué significa $P\vdash W\ \mathsf{wf}$.
