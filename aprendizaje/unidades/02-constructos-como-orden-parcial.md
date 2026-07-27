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
  - D-016
  - D-018
tags:
  - mud/aprendizaje
  - mud/unidad
---

# Unidad 02 — Constructos como orden parcial

> [!abstract]
> Esta unidad formaliza el grafo de especialización de MUD sin introducir clases ni instancias. Es material didáctico; las decisiones semánticas confirmadas proceden de [[notas/decisiones/ADR-014-ontologia-unificada-de-constructos|D-014]], [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|D-015]], [[notas/decisiones/ADR-016-creacion-generalizada-de-constructos|D-016]] y [[notas/decisiones/ADR-018-from-declara-is-consulta|D-018]].

## 1. Pregunta de MUD

Queremos dar un significado único a estas tres expresiones:

```mud
construct Egypt from Kingdom {
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
8. Distinguir la declaración directa con `from` de la consulta derivada con `is`.

## 3. Prerrequisitos

- Conjuntos.
- Pares ordenados.
- Producto cartesiano.
- Funciones parciales y dominio.
- Convenciones de [[especificacion/03-notacion|notación formal]].

La Unidad 01 introdujo esas herramientas. Su interpretación clase–instancia fue retirada, pero las técnicas matemáticas continúan siendo válidas.

## 4. Programa y mundo

Antes de formalizar `create`, necesitamos separar dos cosas que en el código fuente pueden parecer mezcladas:

- El **programa** $P$ es el texto resuelto que describe cómo construir el mundo inicial y qué transiciones están permitidas.
- El **mundo** $W$ contiene las identidades activas, sus declaraciones activas y su estado semántico actual.

El programa contiene sintácticamente:

- Las declaraciones iniciales de constructos.
- Las declaraciones reservadas dentro de `create`.
- Las reglas, acciones y demás leyes de transición.

Al resolverlo obtenemos, conceptualmente:

$$
\llbracket P\rrbracket
=
(W_0,\longrightarrow_P)
$$

donde $W_0$ es el mundo inicial y $\longrightarrow_P$ es la relación de transición permitida por el programa. Una declaración:

```mud
construct Egypt from Kingdom {
}
```

activa `Egypt` en $W_0$. Una creación lo haría en un mundo posterior. La identidad semántica activa pertenece al mundo en ambos casos; el texto que permite activarla pertenece al programa.

Esto no introduce clases e instancias. `Egypt` sigue siendo una única identidad. Distinguimos:

- La reserva y descripción de esa identidad en el programa resuelto.
- Su presencia o ausencia y, cuando sea concreta, su estado activo en el mundo.

Una ejecución produce una secuencia:

$$
W_0\longrightarrow W_1\longrightarrow W_2\longrightarrow\cdots
$$

`create` activa una identidad reservada que estaba ausente. `destroy` puede volver a retirarla del conjunto activo; una creación posterior reactiva la misma identidad. Ninguna de esas operaciones reescribe el archivo `.mud`, altera $P$ durante la ejecución ni crea por sí misma un commit de Git.

> [!intuition]
> $P$ responde «¿cómo nace el mundo y qué cambios se permiten?». $W$ responde «¿qué está activo y cuál es su estado ahora?».

> [!note]
> El subíndice $P$ que aparece más adelante identifica datos extraídos del programa para este fragmento sin destrucción. No afirma que esas identidades deban permanecer activas para siempre. La unidad de ciclo de vida introducirá un conjunto explícito de identidades activas.

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
construct Warship from MilitaryUnit, NavalUnit {
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

construct Kingdom from Place {
    mut treasury: Money = 0M
}

construct Egypt from Kingdom {
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
construct A from B {
}

construct B from A {
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

El programa resuelto reserva las identidades que aparecen como resultado de `create`:

$$
\mathcal R_P^{\mathsf{create}}
\subseteq
\mathcal C
$$

Para no adelantar el estudio del cuerpo completo, proyectamos cada declaración reservada sobre su modo y sus antecesores:

$$
\operatorname{shape}_P:
\mathcal R_P^{\mathsf{create}}
\to
\left(
\mathcal M
\times
\mathcal P_{\mathrm{fin}}(\mathcal C)
\right)
$$

Aquí, $\mathcal P_{\mathrm{fin}}(\mathcal C)$ es el conjunto de todos los subconjuntos finitos de $\mathcal C$. El resultado es un par formado por un modo y un conjunto, no por un único antecesor.

Las proyecciones extraen los dos componentes del par:

$$
\pi_1(m,S)=m
$$

$$
\pi_2(m,S)=S
$$

Las sentencias:

```mud
create Monument {
}

create abstract PoliticalUnion from Place {
}

create France from Kingdom {
}

create EuropeanRealm from Kingdom, PoliticalUnion {
}
```

reservan al resolver $P$ y, cuando son efectivas, activan las identidades correspondientes. Su proyección estructural es:

$$
\operatorname{shape}_P(\mathsf{Monument})
=
(\mathsf{concrete},\varnothing)
$$

$$
\operatorname{shape}_P(\mathsf{PoliticalUnion})
=
(\mathsf{abstract},\{\mathsf{Place}\})
$$

$$
\operatorname{shape}_P(\mathsf{France})
=
(\mathsf{concrete},\{\mathsf{Kingdom}\})
$$

$$
\operatorname{shape}_P(\mathsf{EuropeanRealm})
=
\left(
\mathsf{concrete},
\{\mathsf{Kingdom},\mathsf{PoliticalUnion}\}
\right)
$$

En particular, `create abstract PoliticalUnion from Place {}` produce en el mundo activo el mismo modo y la misma arista que habría aportado una declaración inicial vacía `abstract construct PoliticalUnion from Place {}`. No convierte por ello la sentencia ejecutada en una activación inicial: coinciden sus consecuencias relevantes para el grafo, pero difiere el momento en que la identidad pasa a estar activa.

El cuerpo de `create` es declarativamente completo. Puede declarar propiedades locales, restricciones, reglas o acciones igual que el cuerpo de un constructo ordinario. En esta unidad usamos únicamente su proyección sobre modo y antecesores; la Unidad 03 estudiará el esquema que ahora estamos omitiendo deliberadamente.

Sea $\mathcal E_W\subseteq\mathcal C$ el conjunto de todas las identidades activas del mundo. Las identidades reservadas mediante `create` que están activas son:

$$
\mathcal D_W
:=
\mathcal E_W
\cap
\mathcal R_P^{\mathsf{create}}
$$

La vista activa de los descriptores es la restricción:

$$
\operatorname{created}_W
:=
\left.
\operatorname{shape}_P
\right|_{\mathcal D_W}
$$

De modo que:

$$
\operatorname{dom}(\operatorname{created}_W)
=
\mathcal D_W
$$

`destroy A` retira $A$ de $\mathcal E_W$ y, por tanto, de $\mathcal D_W$, sin liberar su reserva. Una ejecución posterior de `create A` puede volver a incluir la misma identidad $A$.

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

> [!warning]
> Esta igualdad pertenece al fragmento de la unidad, en el que todavía no se ejecuta `destroy` sobre constructos iniciales. En el modelo completo, la existencia se obtendrá de un conjunto activo explícito y no de una unión que obligue a conservar para siempre $\mathcal C_P$.

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

El tipo de $\operatorname{created}_W$ no basta para garantizar que represente un mundo válido. La identidad debe estar reservada, ausente de $\mathcal E_W$ antes de una creación efectiva y activa después de ella. Exigimos además:

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

### Primera clase, reserva y presencia activa

Que un constructo creado sea de primera clase significa que puede participar en relaciones, expresiones, acciones o vinculaciones como cualquier otro constructo. Además, MUD reserva su identidad al resolver el programa, por lo que una aparición textual exacta puede resolverse antes de que esté activa.

Hay dos casos diferentes:

1. Una regla puede hablar de un antecesor ya declarado, como `Place`, y aplicarse en el futuro a constructos creados que satisfagan `is Place`.
2. Una regla puede intentar mencionar exactamente `FutureCity` antes de que una ejecución cree algo con ese nombre.

El primer caso no necesita una identidad exacta futura. En el segundo, el nombre se resuelve a la identidad reservada, pero toda operación que requiera presencia debe comprobar que está activa.

Para una vinculación `for` exacta, antes de la creación no hay todavía una vinculación asociada a ese constructo. La creación podría hacerla nacer; entonces habrá que definir su valor previo y el instante preciso de activación. Una regla `for` no se «llama»: se mantiene una vinculación de la regla para cada participante aplicable.

Para un participante `on` exacto, no habría receptor disponible antes de la creación. En cambio, una acción cuyo participante admita un antecesor ya existente podría aceptar después cualquier descendiente creado compatible.

> [!note]
> [[notas/08-preguntas-abiertas#Q-044 — Identidad y referencias a constructos futuros|Q-044]] está cerrada: destruir y recrear `FutureCity` conserva su identidad. Si una regla con `create FutureCity` la encuentra activa, la regla completa no se ejecuta. [[notas/08-preguntas-abiertas#Q-046 — Creación inefectiva dentro de una raíz|Q-046]] conserva los casos de acciones y varias creaciones.

## 16. Declarar con `from`, consultar con `is`

En:

```mud
construct Egypt from Kingdom {
}
```

`from` forma parte de una cabecera y añade un par a la relación directa.

En:

```mud
Egypt is Place
```

`is` forma una expresión booleana y consulta la relación derivada.

El lexer y el parser distinguen dos palabras y dos nodos:

```text
ConstructDecl(Egypt, parents = {Kingdom})
IsExpression(Egypt, Place)
```

Ambos remiten a la misma estructura en niveles distintos: `from` aporta aristas y `is` consulta su clausura.

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
- `create` activa una identidad reservada raíz, abstracta o concreta con cero o varios antecesores.
- La sintaxis sitúa la identidad reservada antes de la cláusula opcional `from`.
- `from` declara aristas directas; `is` solo consulta la relación derivada.
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
