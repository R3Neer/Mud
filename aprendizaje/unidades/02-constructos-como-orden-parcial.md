---
title: Unidad 02 — Constructos como orden parcial
aliases:
  - Constructos como orden parcial
unit: 2
status: en-curso
level: 0-a-1
concepts:
  - relaciones binarias
  - grafos dirigidos
  - clausura reflexiva y transitiva
  - relaciones acíclicas
  - órdenes parciales
  - especialización
spec-chapters:
  - "[[especificacion/03-notacion]]"
  - "[[especificacion/04-modelo-matematico]]"
  - "[[especificacion/README#11. Constructos, especialización e identidad]]"
decisions:
  - D-014
  - D-015
tags:
  - mud/aprendizaje
  - mud/unidad
---

# Unidad 02 — Constructos como orden parcial

> [!abstract]
> Esta unidad formaliza el grafo de especialización de MUD sin introducir clases ni instancias. Es material didáctico; las decisiones semánticas confirmadas proceden de [[notas/decisiones/ADR-014-ontologia-unificada-de-constructos|D-014]] y [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|D-015]].

## 1. Pregunta de MUD

Queremos dar un significado único a estas tres expresiones:

```mud
construct Egypt is Kingdom {
}

Egypt is Place
Egypt is Egypt
```

La primera declara especialización directa. La segunda depende de varios pasos de herencia. La tercera debe ser verdadera porque `is` es reflexivo.

La pregunta es:

> ¿Qué estructura matemática permite introducir relaciones directas, derivar especializaciones indirectas, aceptar reflexividad y rechazar ciclos?

## 2. Objetivos

Al terminar la unidad deberías poder:

1. Distinguir una función de una relación binaria.
2. Representar una jerarquía de especialización como grafo dirigido.
3. Distinguir especialización directa de `is` semántico.
4. Leer y calcular una clausura reflexiva y transitiva.
5. Explicar por qué un grafo directo acíclico produce un orden parcial.
6. Incorporar a la relación un constructo creado durante la ejecución.
7. Detectar un ciclo inválido y construir el contraejemplo que produciría.
8. Distinguir los dos usos sintácticos del token `is`.

## 3. Prerrequisitos

- Conjuntos.
- Pares ordenados.
- Producto cartesiano.
- Funciones parciales y dominio.
- Convenciones de [[especificacion/03-notacion|notación formal]].

La Unidad 01 introdujo esas herramientas. Su interpretación clase–instancia fue retirada, pero las técnicas matemáticas continúan siendo válidas.

## 4. Programa y mundo

Antes de formalizar `create`, necesitamos separar dos cosas que en el código fuente pueden parecer mezcladas:

- El **programa** $P$ contiene las declaraciones y leyes fijadas antes de comenzar una ejecución.
- El **mundo** $W$ contiene el estado semántico que puede cambiar durante esa ejecución.

En el fragmento actual, pertenecen a $P$:

- Las identidades de los constructos declarados estáticamente.
- Su carácter abstracto o concreto.
- Sus relaciones directas de especialización.
- Sus campos, restricciones, predeterminados, reglas y acciones declarados.

Pertenecen a $W$:

- Los constructos creados durante la ejecución y sus relaciones directas.
- El estado mutable actual de todos los constructos concretos existentes.
- Más adelante, las vinculaciones de reglas y otros componentes del estado runtime.

No son dos universos independientes. Es más preciso escribir:

$$
W\in\operatorname{Worlds}(P)
$$

porque solo podemos decidir si $W$ está bien formado conociendo el programa al que corresponde.

Un constructo concreto declarado estáticamente, como `Egypt`, tampoco se divide en una clase y un objeto. Su única identidad tiene:

- Un aspecto declarativo fijado por $P$: esquema, restricciones y relaciones.
- Un estado activo que forma parte de $W$: por ejemplo, el valor actual de `Egypt.treasury`.

El mundo inicial $W_0$ se construye a partir de $P$. Una ejecución produce después una secuencia:

$$
W_0\longrightarrow W_1\longrightarrow W_2\longrightarrow\cdots
$$

`create` transforma un mundo en otro. No reescribe el archivo `.mud`, no altera $P$ durante esa ejecución y no crea por sí mismo un commit de Git.

> [!intuition]
> $P$ responde «¿qué leyes y declaraciones gobiernan esta ejecución?». $W$ responde «¿qué existe y cuál es su estado ahora, bajo esas leyes?».

> [!note]
> Que una creación pueda ampliar el grafo de constructos significa que $W$ contiene parte de la ontología activa. No significa que la creación pase a formar parte del texto estático de $P$.

## 5. Repaso: función frente a relación

Una función:

$$
f:A\to B
$$

asigna a cada elemento de $A$ exactamente un elemento de $B$.

Una relación binaria:

$$
R\subseteq A\times B
$$

es un conjunto de pares. Un mismo elemento de $A$ puede relacionarse con cero, uno o varios elementos de $B$.

Esto importa porque MUD admite especialización múltiple:

```mud
construct Warship is MilitaryUnit, NavalUnit {
}
```

No podemos representar todos los antecesores directos mediante una función:

$$
\operatorname{parent}:\mathcal C\to\mathcal C
$$

porque `Warship` tendría dos resultados. Una relación sí puede contener:

$$
(\mathsf{Warship},\mathsf{MilitaryUnit})
$$

$$
(\mathsf{Warship},\mathsf{NavalUnit})
$$

> [!intuition]
> Una función responde «¿cuál es su único resultado?». Una relación responde «¿con cuáles está relacionado?».

## 6. Ejemplo de trabajo

Considera:

```mud
abstract construct Place {
    name: Text
}

construct Kingdom is Place {
    mut treasury: Money = 0M
}

construct Egypt is Kingdom {
    name = "Egypt"
}
```

Durante la ejecución aparece además:

```mud
create France from Kingdom {
    name = "France"
}
```

No hay instancias de `Place`, `Kingdom` o `Egypt`. Los cuatro nombres designan constructos. `Place` es abstracto; los demás son concretos.

## 7. Constructos declarados

Sea $P$ el programa resuelto. Sus constructos declarados son:

$$
\mathcal C_P
=
\{
\mathsf{Place},
\mathsf{Kingdom},
\mathsf{Egypt}
\}
$$

Los abstractos forman:

$$
\mathcal A_P
=
\{
\mathsf{Place}
\}
$$

Los concretos declarados se derivan:

$$
\mathcal K_P
:=
\mathcal C_P\setminus\mathcal A_P
$$

Por tanto:

$$
\mathcal K_P
=
\{
\mathsf{Kingdom},
\mathsf{Egypt}
\}
$$

El conjunto de abstractos no constituye otro universo. Es un subconjunto que distingue qué constructos no poseen estado concreto propio.

## 8. Relación de especialización directa

Definimos:

$$
R_P^{\mathrm{dir}}
\subseteq
\mathcal C_P\times\mathcal C_P
$$

con la orientación:

$$
(c,a)\in R_P^{\mathrm{dir}}
$$

si $c$ declara directamente `is a`.

Para el ejemplo:

$$
R_P^{\mathrm{dir}}
=
\{
(\mathsf{Kingdom},\mathsf{Place}),
(\mathsf{Egypt},\mathsf{Kingdom})
\}
$$

La primera posición es el constructo más específico; la segunda, su antecesor directo.

```text
Egypt ──► Kingdom ──► Place
```

La flecha del dibujo representa especialización directa, no movimiento de datos ni propagación de estado.

## 9. Caminos y especialización indirecta

Existe un camino de `Egypt` a `Place`:

$$
\langle
\mathsf{Egypt},
\mathsf{Kingdom},
\mathsf{Place}
\rangle
$$

porque:

$$
(\mathsf{Egypt},\mathsf{Kingdom})
\in
R_P^{\mathrm{dir}}
$$

y:

$$
(\mathsf{Kingdom},\mathsf{Place})
\in
R_P^{\mathrm{dir}}
$$

Aunque el par:

$$
(\mathsf{Egypt},\mathsf{Place})
$$

no pertenezca a la relación directa, `Egypt is Place` debe ser verdadero.

## 10. Clausura transitiva y reflexiva

La clausura transitiva:

$$
\left(R_P^{\mathrm{dir}}\right)^+
$$

contiene los pares conectados por uno o más pasos.

En el ejemplo:

$$
\left(R_P^{\mathrm{dir}}\right)^+
=
\{
(\mathsf{Kingdom},\mathsf{Place}),
(\mathsf{Egypt},\mathsf{Kingdom}),
(\mathsf{Egypt},\mathsf{Place})
\}
$$

La clausura reflexiva y transitiva:

$$
\left(R_P^{\mathrm{dir}}\right)^*
$$

añade los caminos de longitud cero:

$$
(\mathsf{Place},\mathsf{Place})
$$

$$
(\mathsf{Kingdom},\mathsf{Kingdom})
$$

$$
(\mathsf{Egypt},\mathsf{Egypt})
$$

Definimos provisionalmente el significado de `is`:

$$
R_P^{\mathsf{is}}
:=
\operatorname{Id}_{\mathcal C_P}
\cup
\left(R_P^{\mathrm{dir}}\right)^+
=
\left(R_P^{\mathrm{dir}}\right)^*
$$

La estrella se interpreta aquí respecto al conjunto portador $\mathcal C_P$. Escribir explícitamente la relación identidad evita olvidar constructos aislados que no participan en ninguna arista.

Y abreviamos:

$$
c\preceq_P a
\quad\Leftrightarrow\quad
(c,a)\in R_P^{\mathsf{is}}
$$

Se lee:

> $c$ es el mismo constructo que $a$ o una especialización suya.

Por tanto:

$$
\mathsf{Egypt}\preceq_P\mathsf{Place}
$$

y:

$$
\mathsf{Egypt}\preceq_P\mathsf{Egypt}
$$

## 11. Aciclicidad

La relación directa es acíclica si no existe un camino no vacío que salga de un constructo y regrese a él.

Este programa sería inválido:

```mud
construct A is B {
}

construct B is A {
}
```

Produciría:

```text
A ──► B
▲     │
└─────┘
```

No debe confundirse este ciclo con la reflexividad de `is`:

- $(A,A)\notin R^{\mathrm{dir}}$.
- $(A,A)\in R^{\mathsf{is}}$.

La primera sería una arista directa reflexiva inválida. La segunda es un resultado derivado y obligatorio.

## 12. Orden parcial

Una relación $\preceq$ sobre un conjunto $C$ es un orden parcial cuando es:

1. **Reflexiva**:

   $$
   \forall c\in C.\ c\preceq c
   $$

2. **Transitiva**:

   $$
   \forall a,b,c\in C.\
   a\preceq b
   \land
   b\preceq c
   \Rightarrow
   a\preceq c
   $$

3. **Antisimétrica**:

   $$
   \forall a,b\in C.\
   a\preceq b
   \land
   b\preceq a
   \Rightarrow
   a=b
   $$

Antisimetría no significa que solo pueda existir una dirección entre dos elementos. Significa que, si existen las dos, ambos elementos deben ser el mismo.

## 13. Primera demostración resuelta

> [!proof] Proposición — La clausura de una especialización acíclica es un orden parcial
> Sea $R\subseteq C\times C$ una relación acíclica. Sea $R^*:=\operatorname{Id}_C\cup R^+$. Entonces $R^*$ es un orden parcial sobre $C$.

### Reflexividad

$R^*$ contiene por definición todos los caminos de longitud cero. Para cada $c\in C$ existe el camino:

$$
\langle c\rangle
$$

Por tanto:

$$
(c,c)\in R^*
$$

y $R^*$ es reflexiva.

### Transitividad

Supongamos:

$$
(a,b)\in R^*
$$

y:

$$
(b,c)\in R^*
$$

Existe un camino de $a$ a $b$ y otro de $b$ a $c$. Al concatenarlos obtenemos un camino de $a$ a $c$. Por tanto:

$$
(a,c)\in R^*
$$

y $R^*$ es transitiva.

### Antisimetría

Supongamos:

$$
(a,b)\in R^*
$$

y:

$$
(b,a)\in R^*
$$

Si $a\neq b$, ambos caminos tienen conjuntamente longitud positiva. Concatenarlos produciría un camino no vacío que sale de $a$ y vuelve a $a$: un ciclo.

Eso contradice que $R$ sea acíclica. Por tanto:

$$
a=b
$$

y $R^*$ es antisimétrica.

### Conclusión

Como $R^*$ es reflexiva, transitiva y antisimétrica:

$$
(C,R^*)
$$

es un conjunto parcialmente ordenado.

> [!intuition]
> La reflexividad procede de permitir no moverse; la transitividad, de concatenar caminos; la antisimetría, de haber prohibido regresar mediante un ciclo.

## 14. Incorporación de `create`

Sea $\mathcal C$ un universo ambiente de identidades posibles de constructo y sea:

$$
\mathcal M
:=
\{
\mathsf{abstract},
\mathsf{concrete}
\}
$$

El mundo registra cada constructo creado junto con su modo y su conjunto finito de antecesores directos:

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

Aquí, $\mathcal P_{\mathrm{fin}}(\mathcal C)$ es el conjunto de todos los subconjuntos finitos de $\mathcal C$. Esta es una función parcial porque no toda identidad posible existe como creación en el mundo actual. Su resultado es un par formado por un modo y un conjunto, no por un único antecesor.

Las proyecciones extraen los dos componentes del par:

$$
\pi_1(m,S)=m
$$

$$
\pi_2(m,S)=S
$$

Las ejecuciones:

```mud
create Monument
create abstract PoliticalUnion from Place
create France from Kingdom
create EuropeanRealm from Kingdom, PoliticalUnion
```

producen, esquemáticamente:

$$
\operatorname{created}_W(\mathsf{Monument})
=
(\mathsf{concrete},\varnothing)
$$

$$
\operatorname{created}_W(\mathsf{PoliticalUnion})
=
(\mathsf{abstract},\{\mathsf{Place}\})
$$

$$
\operatorname{created}_W(\mathsf{France})
=
(\mathsf{concrete},\{\mathsf{Kingdom}\})
$$

$$
\operatorname{created}_W(\mathsf{EuropeanRealm})
=
\left(
\mathsf{concrete},
\{\mathsf{Kingdom},\mathsf{PoliticalUnion}\}
\right)
$$

En particular, `create abstract PoliticalUnion from Place` produce en el mundo activo el mismo modo y la misma arista que habría aportado una declaración estática vacía `abstract construct PoliticalUnion is Place {}`. No convierte por ello la sentencia ejecutada en texto nuevo de $P$: coinciden sus consecuencias relevantes para el grafo, pero difieren el momento y el lugar donde nacen.

Los constructos creados y existentes se derivan del dominio:

$$
\mathcal D_W
:=
\operatorname{dom}(\operatorname{created}_W)
$$

Los abstractos creados pueden derivarse mediante la primera proyección:

$$
\mathcal A_W
:=
\{
c\in\mathcal D_W
\mid
\pi_1(\operatorname{created}_W(c))
=
\mathsf{abstract}
\}
$$

El conjunto de constructos existentes respecto a $P$ y $W$ es:

$$
\mathcal C_{P,W}
:=
\mathcal C_P\cup\mathcal D_W
$$

La relación directa aportada por el mundo se obtiene de la segunda proyección:

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

Por tanto:

$$
R_{P,W}^{\mathrm{dir}}
:=
R_P^{\mathrm{dir}}
\cup
R_W^{\mathrm{dir}}
$$

El tipo de $\operatorname{created}_W$ no basta para garantizar que represente un mundo válido. Exigimos al menos:

$$
\mathcal D_W\cap\mathcal C_P
=
\varnothing
$$

para que las identidades creadas sean nuevas respecto al programa;

$$
\bigcup_{c\in\mathcal D_W}
\pi_2(\operatorname{created}_W(c))
\subseteq
\mathcal C_{P,W}
$$

para que todo antecesor exista; además, la relación directa combinada debe ser acíclica y los esquemas heredados deben ser compatibles.

> [!intuition]
> Una signatura indica qué forma tienen los datos. La buena formación descarta datos de esa forma que no representan un estado admisible.

El operador se interpreta mediante:

$$
R_{P,W}^{\mathsf{is}}
:=
\operatorname{Id}_{\mathcal C_{P,W}}
\cup
\left(R_{P,W}^{\mathrm{dir}}\right)^+
=
\left(R_{P,W}^{\mathrm{dir}}\right)^*
$$

De ahí:

$$
\mathsf{France}\preceq_{P,W}\mathsf{Kingdom}
$$

$$
\mathsf{France}\preceq_{P,W}\mathsf{Place}
$$

$$
\mathsf{France}\preceq_{P,W}\mathsf{France}
$$

## 15. Por qué la relación no registra por sí sola todas las creaciones

Podríamos intentar almacenar únicamente $R_W^{\mathrm{dir}}$, pero perderíamos `Monument`:

$$
\pi_2(\operatorname{created}_W(\mathsf{Monument}))
=
\varnothing
$$

Al no tener antecesores, no produce ningún par en la relación. Sin embargo, `Monument` existe, pertenece a $\mathcal D_W$ y hace verdadera la consulta reflexiva `Monument is Monument`.

Por eso conservamos dos niveles:

- $\operatorname{created}_W$: descriptor de existencia, modo y antecesores de cada creación.
- $R_W^{\mathrm{dir}}$: relación dinámica derivada del descriptor.
- $R_{P,W}^{\mathrm{dir}}$: relación directa estática y dinámica combinada.
- $R_{P,W}^{\mathsf{is}}$: cierre reflexivo y transitivo consultado por el operador.

> [!note]
> El descriptor no duplica accidentalmente la relación: contiene información que una relación sin aristas no puede expresar.

### Primera clase no significa nombre futuro

Que un constructo creado sea de primera clase significa que, una vez disponible su identidad, puede participar en relaciones, expresiones, acciones o vinculaciones como cualquier otro constructo. No determina si una aparición textual de su nombre puede resolverse antes de la creación.

Hay dos casos diferentes:

1. Una regla puede hablar de un antecesor ya declarado, como `Place`, y aplicarse en el futuro a constructos creados que satisfagan `is Place`.
2. Una regla puede intentar mencionar exactamente `FutureCity` antes de que una ejecución cree algo con ese nombre.

El primer caso no necesita referencias futuras. El segundo sí exige decidir qué significa ese nombre antes de existir.

Para una vinculación `for` exacta, antes de la creación no hay todavía una vinculación asociada a ese constructo. La creación podría hacerla nacer; entonces habrá que definir su valor previo y el instante preciso de activación. Una regla `for` no se «llama»: se mantiene una vinculación de la regla para cada participante aplicable.

Para un participante `on` exacto, no habría receptor disponible antes de la creación. En cambio, una acción cuyo participante admita un antecesor ya existente podría aceptar después cualquier descendiente creado compatible.

> [!question] Diseño pendiente
> [[notas/08-preguntas-abiertas#Q-044 — Identidad y referencias a constructos futuros|Q-044]] decidirá si el nombre de `create` es una identidad global reservable, una vinculación local a una identidad fresca o si hace falta una declaración prospectiva explícita. Hasta resolverlo, no debemos asumir que los nombres futuros son válidos.

## 16. Los dos usos sintácticos de `is`

En:

```mud
construct Egypt is Kingdom {
}
```

`is` forma parte de una cabecera y añade un par a la relación directa.

En:

```mud
Egypt is Place
```

`is` forma una expresión booleana y consulta la relación derivada.

El lexer puede producir el mismo token. El parser y el AST deben distinguir:

```text
DirectSpecialization(Egypt, Kingdom)
IsExpression(Egypt, Place)
```

No existe ambigüedad semántica si ambos nodos remiten a la misma relación en niveles distintos.

## 17. Qué es estándar y qué es de MUD

### Matemática estándar

- Relaciones binarias.
- Grafos dirigidos.
- Caminos.
- Clausuras transitiva y reflexiva-transitiva.
- Aciclicidad.
- Órdenes parciales.

### Convenciones de notación

- La orientación de específico a general.
- $R^{\mathrm{dir}}$ para la relación directa.
- $\preceq$ para la relación semántica.
- $\operatorname{created}_W$ para el descriptor parcial de las creaciones existentes.

### Decisiones semánticas de MUD

- Un solo dominio de constructos.
- `create` produce un constructo raíz, abstracto o concreto con cero o varios antecesores.
- La sintaxis sitúa la identidad nueva antes de la cláusula opcional `from`.
- `is` es reflexivo y transitivo.
- Se rechazan ciclos.
- Los constructos concretos pueden ser cosas y antecesores.
- Los abstractos participan en el orden, pero no poseen estado concreto propio.

## 18. Errores frecuentes

### Tratar la especialización múltiple como función

Una función solo permite un resultado por entrada. La relación directa puede contener varios antecesores.

### Introducir los pares reflexivos en la relación directa

La reflexividad pertenece a $R^*$, no al grafo declarado.

### Confundir aristas con todos los pares verdaderos

`Egypt is Place` puede ser verdadero aunque no exista una arista directa entre ambos.

### Invertir la orientación

En esta unidad:

$$
(c,a)
$$

significa que $c$ es más específico que $a$.

### Pensar que `is` propaga estado

La relación determina especialización y sustituibilidad. [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|D-015]] prohíbe heredar estado activo.

## 19. Lectura comentada

La expresión:

$$
c\preceq_{P,W}a
$$

se lee:

> En el programa $P$ y el mundo $W$, el constructo $c$ es idéntico a $a$ o existe un camino de especialización directa desde $c$ hasta $a$.

La expresión:

$$
R_{P,W}^{\mathsf{is}}
=
\left(R_{P,W}^{\mathrm{dir}}\right)^*
$$

no afirma que almacenemos toda la clausura. Define su significado. Una implementación puede calcularla, indexarla o responder mediante búsqueda siempre que obtenga el mismo resultado.

## 20. Tu turno

El entregable está en [[aprendizaje/ejercicios/02-orden-parcial-de-constructos-ejercicio]].

La plantilla que debes completar está en [[aprendizaje/respuestas/02-orden-parcial-de-constructos-respuesta]].

> [!exercise] Entregable
> Formaliza una jerarquía distinta, incorpora un constructo creado, calcula varios casos de `is` y detecta un ciclo inválido.

> [!hint]- Pista 1 — Empieza por los pares escritos
> Construye primero $R_P^{\mathrm{dir}}$ usando únicamente las cabeceras.

> [!hint]- Pista 2 — Separa cierre y grafo
> Añade después caminos indirectos y pares reflexivos; no los mezcles con las aristas.

> [!hint]- Pista 3 — Usa el dominio
> El conjunto de constructos creados puede derivarse de $\operatorname{dom}(\operatorname{created}_W)$.

La solución completa no está incluida. Se añadirá tras el intento y la revisión.

## 21. Criterios de revisión

La revisión comprobará por separado:

- Orientación de los pares.
- Exhaustividad de la relación directa.
- Cálculo de clausura.
- Uso correcto de reflexividad.
- Detección y justificación del ciclo.
- Diferencia entre función y relación.
- Consistencia de subíndices.
- Claridad de la explicación.

## 22. Incorporación a la especificación

Después de revisar el ejercicio:

1. Ajustaremos la notación si aparece alguna ambigüedad.
2. Redactaremos el fragmento profesional del grafo de constructos.
3. Lo someteremos a ejemplos de herencia múltiple y creación.
4. Decidiremos qué parte pertenece a `04-modelo-matematico` y cuál al futuro `11-constructos.md`.
5. Activaremos la Unidad 03.

## 23. Repaso

En la Unidad 03 reaparecerán:

- Relaciones, al calcular campos heredados.
- Clausuras, al recorrer antecesores.
- Funciones parciales, al resolver predeterminados.
- Conjuntos derivados, al definir posiciones válidas del estado.

Dos unidades después se pedirá detectar sin ayuda si una relación propuesta debería ser una función o una relación múltiple.
