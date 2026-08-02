---
title: Notación matemática y metalenguaje
aliases:
  - Notación formal de MUD
tags:
  - mud/especificacion
  - mud/normativa
status: borrador
normative: true
depends-on:
  - "[[00-convenciones-editoriales]]"
  - "[[01-alcance-y-conformidad]]"
  - "[[02-terminologia]]"
questions: []
decisions:
  - D-070
---

# 03. Notación matemática y metalenguaje

## Estado y propósito

Este capítulo fija el metalenguaje empleado para definir MUD. Su función es evitar que una misma construcción matemática cambie de significado entre capítulos y distinguir con claridad:

- La sintaxis que una persona escribe en un archivo `.mud`.
- Las estructuras matemáticas utilizadas para describirla.
- Los juicios con los que la especificación formula sus propiedades.

Las fórmulas de este capítulo pertenecen a la especificación, no a la sintaxis de MUD. Una implementación no está obligada a representar internamente los objetos mediante estas mismas estructuras, pero su comportamiento observable deberá respetar las definiciones que se construyan con ellas.

Este capítulo es un borrador. Las convenciones aquí definidas pueden utilizarse en otros borradores, pero no adquieren estado vigente hasta completar el ciclo de revisión.

## Dependencias

- [[00-convenciones-editoriales|Convenciones editoriales de la especificación MUD]].
- [[01-alcance-y-conformidad|Alcance, conformidad y versiones]].
- [[02-terminologia|Terminología]].

## 1. Convenciones tipográficas

La tipografía aporta información, pero nunca será la única forma de distinguir dos categorías semánticas.

| Forma | Uso principal | Ejemplos |
| --- | --- | --- |
| $\mathcal A,\mathcal C,\mathcal V$ | Universos y conjuntos destacados | Universo de anclas |
| $A,B,R,W$ | Conjuntos, relaciones y estructuras concretas | Estado de mundo |
| $a,c,v,w$ | Elementos y valores | Un ancla o un valor |
| $\Gamma,\Sigma,\rho$ | Entornos y asignaciones | Entorno de nombres |
| $\tau,\sigma$ | Tipos | Tipo de una expresión |
| $\mathsf{accepted}$ | Categorías formales y nombres literales del metalenguaje | Resultado de una solicitud |
| $\operatorname{dom}(f)$ | Operaciones con nombre | Dominio de una función |

Los nombres concretos utilizados en ejemplos matemáticos pueden escribirse en sans serif:

$$
\mathsf{Gate}
\qquad
\mathsf{open}
$$

Una metavariable se introduce en prosa o mediante un cuantificador antes de utilizarse. El subíndice identifica el objeto respecto al cual se interpreta una cantidad:

$$
R_W
$$

se lee «la relación $R$ correspondiente a $W$». Cambiar el subíndice puede cambiar el objeto designado.

## 2. Igualdad, definición y lógica

La igualdad matemática se escribe:

$$
x=y
$$

La desigualdad se escribe:

$$
x\neq y
$$

El símbolo `:=` introduce una definición en el metalenguaje:

$$
A:=\{x\in B\mid P(x)\}
$$

La fórmula se lee «$A$ se define como el conjunto de elementos $x$ de $B$ que satisfacen $P$». `:=` no es el operador `:=` que pueda aparecer en la sintaxis concreta de MUD; el contexto matemático y el bloque de código los distinguen.

Se emplean los conectores habituales:

| Notación | Lectura |
| --- | --- |
| $\neg P$ | no $P$ |
| $P\land Q$ | $P$ y $Q$ |
| $P\lor Q$ | $P$ o $Q$ |
| $P\Rightarrow Q$ | si $P$, entonces $Q$ |
| $P\Leftrightarrow Q$ | $P$ si y solo si $Q$ |
| $\forall x\in A.\ P(x)$ | para todo $x$ de $A$, se cumple $P(x)$ |
| $\exists x\in A.\ P(x)$ | existe algún $x$ de $A$ que satisface $P(x)$ |
| $\exists!x\in A.\ P(x)$ | existe un único $x$ de $A$ que satisface $P(x)$ |

Los puntos que siguen al dominio de un cuantificador son separadores, no operadores de MUD.

## 3. Conjuntos

La pertenencia y la no pertenencia se escriben:

$$
x\in A
\qquad
x\notin A
$$

El conjunto vacío es $\varnothing$. Las inclusiones se escriben:

$$
A\subset B
\qquad
A\subseteq B
$$

En esta especificación, $A\subset B$ exige que $A$ sea un subconjunto estricto de $B$. La forma $A\subseteq B$ permite que ambos conjuntos sean iguales. Esta convención se mantendrá incluso cuando una fuente matemática externa utilice $\subset$ con un sentido no estricto.

Las operaciones de conjuntos son:

| Notación | Operación |
| --- | --- |
| $A\cup B$ | Unión |
| $A\cap B$ | Intersección |
| $A\setminus B$ | Diferencia |
| $\mathcal P(A)$ | Conjunto potencia |
| $\mathcal P_{\mathrm{fin}}(A)$ | Subconjuntos finitos de $A$ |
| $\lvert A\rvert$ | Cardinalidad de $A$ |

La comprensión:

$$
\{x\in A\mid P(x)\}
$$

denota el subconjunto de $A$ cuyos elementos satisfacen $P$. La notación:

$$
\{e(x)\mid x\in A\land P(x)\}
$$

denota las imágenes $e(x)$ obtenidas de los elementos que satisfacen la condición. Las repeticiones no producen elementos adicionales.

Un conjunto parametrizado por un objeto utiliza un subíndice. Por ejemplo, $\mathcal A_P$ puede designar el conjunto de anclas proporcionado por un programa $P$, siempre que el capítulo correspondiente lo defina.

## 4. Tuplas y productos cartesianos

Una tupla ordenada se escribe:

$$
(x_1,\ldots,x_n)
$$

El orden y la posición de sus componentes forman parte de su significado. Los paréntesis de una tupla no denotan un conjunto.

El producto cartesiano es:

$$
A\times B
:=
\{(a,b)\mid a\in A\land b\in B\}
$$

Para una estructura matemática puede utilizarse:

$$
S=(A,R,f)
$$

La igualdad entre dos estructuras de esta forma exige la igualdad componente a componente, salvo que el capítulo que las define establezca explícitamente otra noción de equivalencia.

Los corchetes angulares:

$$
\langle X,e\rangle
$$

se reservan preferentemente para configuraciones de evaluación o transición. Siguen siendo una agrupación ordenada; su forma tipográfica ayuda a distinguir una configuración operacional de una tupla de datos.

## 5. Funciones totales y parciales

Una función total se declara:

$$
f:A\to B
$$

y debe asignar a cada $a\in A$ un único valor $f(a)\in B$.

Una función parcial se declara:

$$
f:A\rightharpoonup B
$$

y puede no estar definida para algunos elementos de $A$. Su dominio efectivo y su imagen son:

$$
\operatorname{dom}(f)
:=
\{a\in A\mid f(a)\text{ está definida}\}
$$

$$
\operatorname{im}(f)
:=
\{f(a)\mid a\in\operatorname{dom}(f)\}
$$

Que la aplicación esté definida se abrevia:

$$
f(a)\downarrow
\quad\Leftrightarrow\quad
a\in\operatorname{dom}(f)
$$

La ausencia de resultado se abrevia:

$$
f(a)\uparrow
\quad\Leftrightarrow\quad
a\notin\operatorname{dom}(f)
$$

En estas fórmulas, $\downarrow$ y $\uparrow$ solo afirman si la aplicación está definida. No significan por sí mismos aceptación, rechazo, fallo ni terminación de una ejecución.

Una función parcial es finita cuando su dominio efectivo es finito:

$$
f:A\rightharpoonup B
\qquad
\lvert\operatorname{dom}(f)\rvert<\infty
$$

Un mapa finito puede mostrarse por extensión:

$$
f=
\{
a_1\mapsto b_1,
\ldots,
a_n\mapsto b_n
\}
$$

La flecha $\mapsto$ se lee «se asocia con». Cada clave debe aparecer como máximo una vez.

Dos funciones parciales son iguales cuando tienen el mismo dominio efectivo y coinciden en todas sus entradas:

$$
f=g
\quad\Leftrightarrow\quad
\operatorname{dom}(f)=\operatorname{dom}(g)
\land
\forall x\in\operatorname{dom}(f).\ f(x)=g(x)
$$

## 6. Relaciones

Una relación binaria entre $A$ y $B$ es un subconjunto:

$$
R\subseteq A\times B
$$

Las expresiones:

$$
(a,b)\in R
\qquad
a\,R\,b
$$

son equivalentes cuando la segunda resulte legible.

La relación identidad sobre $A$ es:

$$
\operatorname{Id}_A
:=
\{(a,a)\mid a\in A\}
$$

Si $R\subseteq A\times B$ y $S\subseteq B\times C$, su composición es:

$$
S\circ R
:=
\{
(a,c)\in A\times C
\mid
\exists b\in B.\ a\,R\,b\land b\,S\,c
\}
$$

Para una relación $R\subseteq A\times A$:

- $R^+$ denota su clausura transitiva.
- $R^*$ denota su clausura reflexiva y transitiva.

Estas clausuras no presuponen que una relación concreta de MUD sea herencia, pertenencia o subtipo. Cada capítulo deberá declarar el significado de su propia relación.

## 7. Secuencias y multiconjuntos

$A^*$ denota el conjunto de secuencias finitas de elementos de $A$. La secuencia vacía se escribe $\epsilon$ y una secuencia concreta:

$$
\langle a_1,\ldots,a_n\rangle
$$

La longitud de una secuencia $s$ se escribe $\lvert s\rvert$. La concatenación se escribe $s\mathbin{\cdot}t$. Salvo indicación contraria, los índices de una secuencia comienzan en $1$.

El superíndice $*$ está sobrecargado de manera convencional: en $A^*$ forma secuencias finitas y en $R^*$ forma la clausura reflexiva y transitiva de una relación. El tipo de la base deberá hacer inequívoca cada aparición.

Un multiconjunto finito sobre $A$ se modela como una función:

$$
m:A\to\mathbb{N}
$$

con soporte finito, donde $m(a)$ es la multiplicidad de $a$ y:

$$
\operatorname{supp}(m)
:=
\{a\in A\mid m(a)>0\}
$$

es finito. Esta representación distingue un multiconjunto de un conjunto sin imponerle un orden.

## 8. Grafos y caminos

Un grafo dirigido es una pareja:

$$
G=(N,E)
$$

donde $N$ es el conjunto de nodos y $E\subseteq N\times N$ es la relación de aristas.

Un camino finito de $n_0$ a $n_k$ es una secuencia:

$$
\langle n_0,\ldots,n_k\rangle
$$

tal que:

$$
\forall j\in\{1,\ldots,k\}.\ (n_{j-1},n_j)\in E
$$

Un camino de longitud cero contiene un único nodo. Los capítulos que necesiten caminos simples, ciclos o grafos etiquetados introducirán esas restricciones explícitamente.

## 9. Juicios

Un juicio expresa una afirmación definida por la especificación. Su forma y sus parámetros deben declararse antes de utilizarlo.

Por ejemplo:

$$
\Gamma\vdash e:\tau
$$

puede leerse «en el entorno $\Gamma$, la expresión $e$ tiene tipo $\tau$», si el capítulo del sistema de tipos lo define así.

El símbolo $\vdash$ separa el contexto de la afirmación juzgada. No implica por sí solo tipado: también puede emplearse para resolución de nombres, validez estática u otras relaciones derivables.

El símbolo:

$$
M\models P
$$

se reserva para indicar que una estructura $M$ satisface una propiedad semántica $P$, cuando el capítulo correspondiente defina esa relación de satisfacción.

Los contextos múltiples se separan mediante punto y coma:

$$
\Gamma;\Sigma\vdash e:\tau
$$

El punto y coma forma parte del metalenguaje del juicio, no de la sintaxis de MUD.

## 10. Reglas de inferencia y derivaciones

Una regla de inferencia tiene la forma:

$$
\frac{
J_1
\qquad
\cdots
\qquad
J_n
}{
J
}
\;\mathsf{Nombre\text{-}De\text{-}Regla}
$$

$J_1,\ldots,J_n$ son las premisas y $J$ es la conclusión. Una regla sin premisas es un axioma:

$$
\frac{\ }{J}
\;\mathsf{Nombre\text{-}De\text{-}Axioma}
$$

Los nombres de regla son únicos dentro de la especificación y se escriben con `\mathsf`. Una derivación es un árbol finito cuyas hojas son axiomas o hipótesis admitidas y cuya raíz es el juicio demostrado.

Las condiciones laterales que no sean juicios se escriben junto a las premisas y se explican en prosa. Ninguna premisa necesaria quedará implícita por el ejemplo que acompaña a la regla.

## 11. Semántica operacional

Una evaluación completa puede representarse mediante un juicio de paso grande:

$$
\langle X,e\rangle
\Downarrow
\langle X',r\rangle
$$

La flecha $\Downarrow$ indica que la configuración de la izquierda produce el resultado completo de la derecha conforme a las reglas que definan ese juicio.

Un paso elemental puede representarse:

$$
K\to K'
$$

o, cuando el paso tenga una etiqueta observable:

$$
K\xrightarrow{\ell}K'
$$

La clausura reflexiva y transitiva de la transición se escribe:

$$
K\to^*K'
$$

Estas flechas no garantizan terminación, determinismo ni ausencia de fallos. Cada sistema de transición deberá definir sus configuraciones, etiquetas y estados terminales.

## 12. EBNF

La gramática concreta utilizará el siguiente dialecto EBNF:

| Forma | Significado |
| --- | --- |
| `"token"` | Terminal literal |
| `nombre` | Referencia a una producción no terminal |
| `a, b` | Concatenación |
| `a \| b` | Alternativa |
| `[ a ]` | Aparición opcional |
| `{ a }` | Cero o más apariciones |
| `( a )` | Agrupación |
| `nombre = a ;` | Definición de una producción |

Una o más apariciones de `a` se escribirán:

```ebnf
a, { a }
```

Los símbolos EBNF pertenecen al metalenguaje. Cuando uno de ellos sea también un token de MUD aparecerá entre comillas.

La ausencia de ambigüedad no se presume por haber escrito una EBNF. El capítulo de gramática deberá fijar además precedencia, asociatividad y cualquier restricción contextual necesaria.

## 13. ASDL-MUD

El AST superficial se describe mediante un dialecto ASDL explícito.

| Forma | Significado |
|---|---|
| `t = C(a x) \| D` | Tipo suma con constructores. |
| `t = (a x, b y)` | Tipo producto. |
| `T?` | Cero o un valor. |
| `T*` | Secuencia finita ordenada. |
| `attributes (...)` | Atributos comunes de todos los constructores del tipo. |

Escalares incorporados:

- `identifier`: texto ya validado como identificador léxico.
- `string`: cadena Unicode.
- `int`: entero matemático no acotado en el esquema.

MUD añade el tipo declarado:

```asdl
flag = Disabled | Enabled
```

ASDL describe distinciones normativas, no una disposición concreta de memoria. Una implementación puede usar índices, referencias, interning o estructuras compactas si conserva el mismo contenido observable.

## 14. Notación de CST

El catálogo CST usa las nociones:

```text
SyntaxNode(kind, children, span, fullSpan)
SyntaxToken(kind, text, leadingTrivia, span, fullSpan, origin)
SyntaxTrivia(kind, text, span)
```

Una categoría terminada en `Syntax` corresponde a una producción o a un nodo especial de recuperación. La CST conserva tokens y trivia; el AST no.

`SourceSpan` usa posiciones basadas en cero, offsets en bytes UTF-8 y extremo final exclusivo. La columna cuenta valores escalares Unicode.

## 15. Ausencia, indefinición y resultados

La especificación distinguirá siempre:

- La ausencia de un elemento en un conjunto.
- Una función parcial no definida para una entrada.
- Un valor de dominio que represente ausencia, si MUD llegase a definirlo.
- Un cálculo que no termina.
- Un resultado semántico como $\mathsf{rejected}$ o $\mathsf{failed}$.
- Un error de una implementación.

Ninguna de estas situaciones se identificará con otra sin una regla explícita.

## 16. Disciplina de uso

Todo capítulo deberá:

1. Introducir sus universos y metavariables antes de usarlos.
2. Indicar el dominio de cada cuantificador.
3. Distinguir funciones totales de parciales.
4. Definir el significado de cada juicio y flecha.
5. Mantener los subíndices de forma consistente.
6. Separar igualdad, equivalencia observacional e identidad cuando no coincidan.
7. Declarar si una colección es conjunto, secuencia o multiconjunto.
8. Explicar cualquier sobrecarga de notación.

## 17. Notación pendiente de introducción

Los órdenes parciales, puntos fijos, medidas de probabilidad y variables aleatorias se definirán cuando un capítulo normativo los necesite por primera vez. Hasta entonces no se fija una notación propia para ellos.

## Cuestiones abiertas

No hay cuestiones abiertas que bloqueen el núcleo de notación definido en este borrador. Su suficiencia deberá revisarse al redactar cada capítulo que lo utilice.
