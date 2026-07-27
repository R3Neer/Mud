---
title: Unidad 01 — Modelo mínimo de un mundo
aliases:
  - Modelo mínimo de un mundo
unit: 1
status: en-curso
level: 0-a-1
concepts:
  - conjuntos
  - producto cartesiano
  - funciones
  - funciones parciales
  - estado
  - identidad
spec-chapters:
  - "[[especificacion/03-notacion]]"
  - "[[especificacion/04-modelo-matematico]]"
tags:
  - mud/aprendizaje
  - mud/unidad
---

# Unidad 01 — Modelo mínimo de un mundo

> [!abstract]
> Esta unidad construye una primera representación matemática de un mundo MUD. Es material didáctico y una propuesta de trabajo: no forma parte todavía de la especificación normativa.

## 1. Pregunta de MUD

Queremos poder afirmar:

> Si una acción resulta `rejected`, el mundo observable después de la solicitud es exactamente el mismo que antes.

La frase parece clara, pero contiene una pregunta previa:

> ¿Qué es exactamente un mundo y qué significa que dos mundos sean “el mismo”?

No podemos demostrar atomicidad ni rollback mientras “mundo” siga siendo una intuición.

## 2. Objetivos

Al terminar esta unidad deberías poder:

1. Distinguir un conjunto, un par ordenado, una función y una función parcial.
2. Explicar por qué la definición de un constructo no es el estado de una instancia.
3. Distinguir tipo, identidad, campo y valor.
4. Leer la propuesta:

   $$
   W=(\operatorname{kind}_W,\operatorname{store}_W)
   $$

5. Explicar por qué el store se modela inicialmente como una función parcial.
6. Formalizar un segundo mundo siguiendo el mismo patrón.

## 3. Prerrequisitos

No se presupone teoría de conjuntos más allá de haber visto alguna vez llaves como $\{1,2,3\}$. Toda notación nueva se introduce aquí.

## 4. Escenario

Partimos de este fragmento:

```mud
construct Kingdom {
    name: Text
    mut treasury: Money
    mut soldiers: Natural
}
```

Y de una instancia concreta, que por ahora describimos informalmente:

```text
identidad: egypt#1
tipo runtime: Kingdom
name: "Egypt"
treasury: 10_000M
soldiers: 2_000
```

> [!warning]
> `egypt#1` es una notación didáctica para una identidad runtime. No estamos decidiendo todavía su sintaxis, serialización ni relación definitiva con un constructo estático como `Egypt`.

## 5. Conjuntos

Un **conjunto** es una colección matemática en la que:

- El orden no forma parte del significado.
- Un elemento pertenece o no pertenece.
- Repetir un elemento no crea una segunda aparición.

Se escribe:

$$
A=\{a_1,a_2,\ldots,a_n\}
$$

Y la pertenencia se escribe:

$$
a\in A
$$

Para nuestro ejemplo introducimos varios universos:

$$
\mathcal C
$$

es el conjunto de constructos;

$$
\mathcal I
$$

es el conjunto de identidades runtime;

$$
\mathcal F
$$

es el conjunto de campos;

$$
\mathcal V
$$

es el universo de valores.

La letra caligráfica no cambia la naturaleza del conjunto. Es una convención visual para reconocer universos o conjuntos importantes.

Para el ejemplo podemos tomar subconjuntos pequeños:

$$
C_0=\{\mathsf{Kingdom}\}
$$

$$
I_0=\{\mathit{egypt\#1}\}
$$

$$
F_0=
\{
\mathsf{name},
\mathsf{treasury},
\mathsf{soldiers}
\}
$$

$$
V_0=
\{
\text{"Egypt"},
10\,000M,
2\,000
\}
$$

> [!intuition]
> Los conjuntos anteriores no dicen todavía qué valor corresponde a cada campo. Solo enumeran qué objetos estamos considerando.

## 6. Pares ordenados y producto cartesiano

Un par ordenado:

$$
(a,b)
$$

no es lo mismo que un conjunto $\{a,b\}$. En el par, la primera y la segunda posición tienen significado:

$$
(a,b)\neq(b,a)
$$

en general.

El **producto cartesiano** de dos conjuntos $A$ y $B$ es el conjunto de todos los pares posibles:

$$
A\times B
=
\{(a,b)\mid a\in A\land b\in B\}
$$

En MUD nos interesa:

$$
\mathcal I\times\mathcal F
$$

porque cada posición del estado puede identificarse mediante:

1. La identidad de una instancia.
2. El campo que queremos consultar.

Por ejemplo:

$$
(\mathit{egypt\#1},\mathsf{treasury})
\in
\mathcal I\times\mathcal F
$$

Este par funciona como una dirección semántica: “el campo `treasury` de la instancia `egypt#1`”.

## 7. Funciones

Una función total:

$$
f:A\to B
$$

asigna a **cada** elemento de $A$ exactamente un elemento de $B$.

Las dos palabras importantes son:

- Cada entrada tiene resultado.
- Cada entrada tiene un único resultado.

Por ejemplo:

$$
\operatorname{double}:\mathbb N\to\mathbb N
$$

$$
\operatorname{double}(n)=2n
$$

está definida para todos los naturales.

En cambio, la operación “predecesor natural” no tiene resultado natural para $0$, salvo que inventemos una convención. Podemos representarla como función parcial:

$$
\operatorname{pred}:\mathbb N\rightharpoonup\mathbb N
$$

El símbolo:

$$
\rightharpoonup
$$

indica que algunas entradas pueden no tener resultado.

## 8. Por qué el store es parcial

Podríamos intentar:

$$
\operatorname{store}_W:
\mathcal I\times\mathcal F
\to
\mathcal V
$$

Esto obligaría a que toda identidad tuviera un valor para todo campo existente.

Si el mundo contiene un `Kingdom` y un `Gate`, exigiría absurdos como:

$$
\operatorname{store}_W
(\mathit{egypt\#1},\mathsf{open})
$$

aunque `open` solo pertenezca a `Gate`.

Por eso comenzamos con:

$$
\operatorname{store}_W:
\mathcal I\times\mathcal F
\rightharpoonup
\mathcal V
$$

Ahora el store puede estar definido únicamente en combinaciones con sentido.

Para el ejemplo:

$$
\operatorname{store}_W
(\mathit{egypt\#1},\mathsf{name})
=
\text{"Egypt"}
$$

$$
\operatorname{store}_W
(\mathit{egypt\#1},\mathsf{treasury})
=
10\,000M
$$

$$
\operatorname{store}_W
(\mathit{egypt\#1},\mathsf{soldiers})
=
2\,000
$$

En cambio:

$$
\operatorname{store}_W
(\mathit{egypt\#1},\mathsf{open})
$$

no está definido.

## 9. Dominio de una función

El dominio efectivo de una función parcial $f$ se escribe:

$$
\operatorname{dom}(f)
$$

Es el conjunto de entradas para las que sí existe resultado.

En nuestro ejemplo:

$$
\operatorname{dom}(\operatorname{store}_W)
=
\{
(\mathit{egypt\#1},\mathsf{name}),
(\mathit{egypt\#1},\mathsf{treasury}),
(\mathit{egypt\#1},\mathsf{soldiers})
\}
$$

Y se cumple:

$$
(\mathit{egypt\#1},\mathsf{open})
\notin
\operatorname{dom}(\operatorname{store}_W)
$$

## 10. Tipo runtime de una identidad

El store indica valores, pero todavía no indica qué constructo describe cada instancia.

Una primera posibilidad sería declarar explícitamente el conjunto $I_W$ de identidades existentes y después una función total:

$$
\operatorname{kind}_W:I_W\to\mathcal C
$$

Pero una función incluye su dominio como parte de su definición. Por tanto, si conocemos $\operatorname{kind}_W$, podemos recuperar $I_W$:

$$
I_W=\operatorname{dom}(\operatorname{kind}_W)
$$

Mantener ambos como componentes independientes introduciría redundancia y nos obligaría a imponer:

$$
I_W=\operatorname{dom}(\operatorname{kind}_W)
$$

en toda buena formación.

Una representación más pequeña consiste en hacer parcial `kind` sobre el universo de identidades:

$$
\operatorname{kind}_W:
\mathcal I
\rightharpoonup
\mathcal C
$$

Una identidad existe en $W$ exactamente cuando `kind` está definida para ella:

$$
i\in I_W
\iff
i\in\operatorname{dom}(\operatorname{kind}_W)
$$

Así, $I_W$ sigue siendo una abreviatura útil, pero es una noción derivada y no un componente independiente del mundo.

En el ejemplo:

$$
I_W=\{\mathit{egypt\#1}\}
$$

$$
\operatorname{kind}_W(\mathit{egypt\#1})
=
\mathsf{Kingdom}
$$

Aquí usamos una función total porque toda identidad existente debe tener algún constructo runtime. Esto es una **propuesta semántica razonable**, no todavía una norma aprobada.

## 11. Primera propuesta de mundo

Ya podemos agrupar las piezas dinámicas:

$$
W=
\left(
\operatorname{kind}_W,
\operatorname{store}_W
\right)
$$

Se lee:

> Un mundo $W$ está formado, como mínimo, por la clasificación runtime parcial de identidades y el store parcial de sus campos.

El programa resuelto $P$ proporciona el contexto estático: constructos, campos, tipos y demás declaraciones. Esos conjuntos no cambian durante la ejecución y no se repiten como componentes de cada mundo:

$$
\mathcal C_P,\qquad
\mathcal F_P,\qquad
\mathcal V_P
$$

El mundo se interpreta siempre respecto a un programa:

$$
W\in\operatorname{Worlds}(P)
$$

Para nuestro mundo:

$$
\operatorname{kind}_W
=
\{
\mathit{egypt\#1}\mapsto\mathsf{Kingdom}
\}
$$

$$
\operatorname{store}_W
=
\left\{
\begin{aligned}
(\mathit{egypt\#1},\mathsf{name})
&\mapsto \text{"Egypt"}\\
(\mathit{egypt\#1},\mathsf{treasury})
&\mapsto 10\,000M\\
(\mathit{egypt\#1},\mathsf{soldiers})
&\mapsto 2\,000
\end{aligned}
\right\}
$$

La flecha $\mapsto$ se lee “se asocia con”.

## 12. Esquema frente a estado

La declaración:

```mud
construct Kingdom {
    name: Text
    mut treasury: Money
    mut soldiers: Natural
}
```

no afirma que exista `egypt#1`, ni que tenga 10 000 unidades monetarias.

La declaración pertenece al **esquema semántico** del programa. Describe, entre otras cosas:

- Qué campos declara `Kingdom`.
- Qué tipo tiene cada campo.
- Qué campos son mutables.

El mundo $W$ pertenece al **estado runtime**. Describe:

- Qué identidades existen.
- Qué constructo runtime tiene cada una.
- Qué valores poseen sus campos.

> [!important]
> Confundir esquema y estado impediría expresar correctamente creación, destrucción, varias instancias del mismo constructo y rollback.

## 13. Buena formación

Nuestra pareja de funciones permite escribir mundos absurdos:

$$
\operatorname{store}_W
(\mathit{egypt\#1},\mathsf{treasury})
=
\text{"mucho"}
$$

La estructura matemática existe, pero no representa un estado válido de MUD.

Necesitamos un predicado:

$$
\operatorname{WellFormed}(P,W)
$$

que se lee:

> El mundo $W$ está bien formado respecto al programa resuelto $P$.

Más adelante tendrá que exigir, al menos:

1. Toda identidad existente pertenece al dominio de `kind`, y cada entrada de ese dominio tiene un único resultado.
2. Todo campo almacenado pertenece al constructo correspondiente o a sus ancestros.
3. Todo valor pertenece al tipo declarado del campo.
4. Se respetan cardinalidades.
5. Se respetan dominios.
6. No existen referencias colgantes.

No formalizamos todavía cada condición porque necesitamos antes el sistema de tipos, herencia, cardinalidades y dominios.

Esta es una técnica profesional importante: podemos definir el nombre y la responsabilidad de una noción antes de expandir todos sus casos, siempre que la marquemos como incompleta.

## 14. Igualdad de mundos

Con esta propuesta revisada:

$$
W_1=W_2
$$

si y solo si coinciden sus dos componentes:

$$
\operatorname{kind}_{W_1}
=
\operatorname{kind}_{W_2}
$$

$$
\operatorname{store}_{W_1}
=
\operatorname{store}_{W_2}
$$

Esto nos permite expresar la atomicidad de una acción rechazada:

$$
\frac{
\langle W,q\rangle
\Downarrow
\langle W',\mathsf{rejected},T\rangle
}{
W'=W
}
\;\mathsf{Rejected\text{-}Unchanged}
$$

Todavía no afirmamos que sea un teorema. Por ahora es la forma de una propiedad que queremos exigir o demostrar cuando definamos la semántica de acciones.

## 15. Alternativas consideradas

### 15.1 Conjunto portador explícito

También podríamos conservar:

$$
W=
(I_W,\operatorname{kind}_W,\operatorname{store}_W)
$$

Esta forma se parece a una estructura algebraica con conjuntos portadores explícitos y puede resultar cómoda al definir operaciones. Sin embargo, si `kind` es total sobre $I_W$, el conjunto puede recuperarse como su dominio.

Conservar ambos exige una condición de coherencia adicional. La propuesta revisada prefiere definir:

$$
I_W:=\operatorname{dom}(\operatorname{kind}_W)
$$

### 15.2 Un mapa por instancia

Podríamos representar:

$$
\operatorname{store}_W:
\mathcal I
\rightharpoonup
(\mathcal F\rightharpoonup\mathcal V)
$$

Es decir: cada identidad se asocia con otro mapa de campos a valores.

Esta representación es intuitiva y cercana a un objeto o registro. La representación plana:

$$
(\mathcal I\times\mathcal F)\rightharpoonup\mathcal V
$$

facilita hablar de posiciones individuales, conjuntos de lectura y conjuntos de escritura.

Las dos pueden contener esencialmente la misma información. Elegir una para la especificación es una convención de modelado, no una verdad matemática inevitable.

### 15.3 Un registro fijo

Podríamos definir un registro diferente para cada constructo. Funciona bien para lenguajes pequeños, pero complica:

- Herencia.
- Colecciones heterogéneas.
- Acceso uniforme mediante anclas.
- Creación dinámica.
- Grafos de dependencia.

### 15.4 Una secuencia de asignaciones

Una lista como:

```text
name = "Egypt"
treasury = 10_000M
soldiers = 2_000
```

conserva un orden que, según los principios de MUD, no debería cambiar el significado del estado. Introducir orden sin necesidad nos obligaría después a demostrar que es irrelevante.

## 16. Qué es estándar y qué es de MUD

### Matemática estándar

- Conjuntos y subconjuntos.
- Producto cartesiano.
- Funciones totales y parciales.
- Dominio de una función.
- Igualdad estructural de productos y funciones.

### Convenciones provisionales de la especificación

- $\mathcal C$, $\mathcal I$, $\mathcal F$ y $\mathcal V$ como letras.
- `kind` como nombre de la clasificación runtime.
- Store plano sobre pares identidad-campo.
- $I_W$ como abreviatura de $\operatorname{dom}(\operatorname{kind}_W)$.

### Decisiones semánticas de MUD que deberán aprobarse

- Toda identidad existente tiene un único constructo runtime.
- La identidad forma parte del estado observable.
- Dos mundos son iguales exactamente cuando coinciden estos componentes.
- El store contiene solo campos almacenados o también materializa otros datos.
- Relación entre constructos estáticos e identidades runtime.

## 17. Errores frecuentes

### Usar un conjunto para asociaciones

Esto enumera valores:

$$
\{10\,000M,2\,000\}
$$

pero no indica cuál es tesoro y cuál soldados.

### Confundir campo con valor

$\mathsf{treasury}$ identifica una propiedad. $10\,000M$ es un valor que puede ocuparla en un estado.

### Confundir nombre con identidad

`"Egypt"` puede cambiar o repetirse. Una identidad runtime debe seguir identificando la misma instancia aunque cambie `name`.

### Hacer total el store sin explicar valores imposibles

Una función total exige valores para todos los pares de su dominio declarado. No puede ignorarse esa obligación.

### Llamar teorema a una intención

`Rejected-Unchanged` todavía no está demostrado porque aún no existe una semántica formal completa de acciones.

## 18. Lectura de comprobación

Deberías poder leer:

$$
\operatorname{store}_W:
I_W\times\mathcal F
\rightharpoonup
\mathcal V
$$

como:

> En el mundo $W$, el store es una función parcial que, para algunos pares formados por una identidad existente y un campo, produce un valor.

Y:

$$
(\mathit{egypt\#1},\mathsf{open})
\notin
\operatorname{dom}(\operatorname{store}_W)
$$

como:

> El store de $W$ no define un valor para el campo `open` de `egypt#1`.

## 19. Tu turno

El ejercicio reutilizable está en [[aprendizaje/ejercicios/01-modelo-minimo-ejercicio]].

La primera respuesta del autor y su revisión se conservan como caso de aprendizaje:

- [[aprendizaje/respuestas/01-modelo-minimo-respuesta]]
- [[aprendizaje/revisiones/01-modelo-minimo-revision]]

> [!exercise] Entregable
> Modela un mundo con una puerta concreta siguiendo la misma estructura. Después explica con tus palabras por qué el store es parcial.

> [!hint]- Pista 1 — Clasifica antes de formalizar
> Separa constructo, identidad, campos y valores antes de escribir funciones.

> [!hint]- Pista 2 — Forma del mundo
> Conserva la forma $W_G=(\operatorname{kind}_{W_G},\operatorname{store}_{W_G})$ y sustituye únicamente su contenido.

> [!hint]- Pista 3 — Dominio del store
> El dominio debe contener dos pares: uno para `unlocked` y otro para `open`.

No hay solución completa en esta unidad. Se añadirá o enlazará después de tu intento.

## 20. Incorporación futura a la especificación

Tras revisar el ejercicio y las alternativas:

1. Fijaremos las convenciones necesarias en `03-notacion.md`.
2. Redactaremos una propuesta profesional de `04-modelo-matematico.md`.
3. Registraremos las decisiones todavía abiertas.
4. Buscaremos un contraejemplo que obligue a ampliar o corregir la representación $W$.

## 21. Repaso

En la siguiente unidad reaparecerán:

- Funciones parciales al definir campos y nombres.
- Productos cartesianos al formalizar anclas de miembros.
- Predicados de buena formación al introducir tipos.

Dos o tres unidades después tendrás que detectar por tu cuenta cuándo una función supuestamente total debería ser parcial.
