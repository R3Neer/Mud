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

## 4. Repaso: función frente a relación

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

## 5. Ejemplo de trabajo

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
create Kingdom France {
    name = "France"
}
```

No hay instancias de `Place`, `Kingdom` o `Egypt`. Los cuatro nombres designan constructos. `Place` es abstracto; los demás son concretos.

## 6. Constructos declarados

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

## 7. Relación de especialización directa

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

## 8. Caminos y especialización indirecta

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

## 9. Clausura transitiva y reflexiva

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

## 10. Aciclicidad

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

## 11. Orden parcial

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

## 12. Primera demostración resuelta

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

## 13. Incorporación de `create`

Para el fragmento actual, modelamos el antecesor inmediato de cada constructo creado mediante:

Sea $\mathcal C$ un universo ambiente de identidades posibles de constructo. Definimos:

$$
\operatorname{base}_W:
\mathcal C
\rightharpoonup
\mathcal C
$$

La ejecución:

```mud
create Kingdom France {
    name = "France"
}
```

añade:

$$
\operatorname{base}_W(\mathsf{France})
=
\mathsf{Kingdom}
$$

Los constructos creados se derivan:

$$
\mathcal D_W
:=
\operatorname{dom}(\operatorname{base}_W)
$$

En el ejemplo:

$$
\mathcal D_W
=
\{
\mathsf{France}
\}
$$

Los constructos existentes respecto a $P$ y $W$ son:

$$
\mathcal C_{P,W}
:=
\mathcal C_P\cup\mathcal D_W
$$

El tipo de $\operatorname{base}_W$ no basta para garantizar que represente un mundo válido. Exigimos al menos:

$$
\mathcal D_W\cap\mathcal C_P
=
\varnothing
$$

para que toda identidad creada sea fresca;

$$
\operatorname{im}(\operatorname{base}_W)
\subseteq
\mathcal C_{P,W}
$$

para que toda base exista; y que la relación directa combinada siga siendo acíclica.

> [!intuition]
> Una signatura indica qué forma tienen los datos. La buena formación descarta datos de esa forma que no representan un estado admisible.

La relación directa completa es:

$$
R_{P,W}^{\mathrm{dir}}
:=
R_P^{\mathrm{dir}}
\cup
\{
(c,\operatorname{base}_W(c))
\mid
c\in\mathcal D_W
\}
$$

Y el operador se interpreta mediante:

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

> [!warning]
> $\operatorname{base}_W$ es un candidato para el fragmento actual porque `create C N` declara una base. La forma definitiva deberá revisarse si `create` llega a admitir varias bases o cambios de antecesores.

## 14. Por qué `base` no sustituye a la relación

La función `base` resulta suficiente para registrar el único antecesor introducido por cada `create` actual. No sirve como representación general de la especialización declarada, porque MUD permite herencia múltiple.

La separación es:

- $R_P^{\mathrm{dir}}$: relación estática, potencialmente múltiple.
- $\operatorname{base}_W$: función parcial para creaciones runtime con una base.
- $R_{P,W}^{\mathrm{dir}}$: relación combinada y derivada.
- $R_{P,W}^{\mathsf{is}}$: cierre reflexivo y transitivo consultado por el operador.

## 15. Los dos usos sintácticos de `is`

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

## 16. Qué es estándar y qué es de MUD

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
- $\operatorname{base}_W$ para el antecesor de una creación.

### Decisiones semánticas de MUD

- Un solo dominio de constructos.
- `create` produce otro constructo.
- `is` es reflexivo y transitivo.
- Se rechazan ciclos.
- Los constructos concretos pueden ser cosas y antecesores.
- Los abstractos participan en el orden, pero no poseen estado concreto propio.

## 17. Errores frecuentes

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

## 18. Lectura comentada

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

## 19. Tu turno

El entregable está en [[aprendizaje/ejercicios/02-orden-parcial-de-constructos-ejercicio]].

La plantilla que debes completar está en [[aprendizaje/respuestas/02-orden-parcial-de-constructos-respuesta]].

> [!exercise] Entregable
> Formaliza una jerarquía distinta, incorpora un constructo creado, calcula varios casos de `is` y detecta un ciclo inválido.

> [!hint]- Pista 1 — Empieza por los pares escritos
> Construye primero $R_P^{\mathrm{dir}}$ usando únicamente las cabeceras.

> [!hint]- Pista 2 — Separa cierre y grafo
> Añade después caminos indirectos y pares reflexivos; no los mezcles con las aristas.

> [!hint]- Pista 3 — Usa el dominio
> El conjunto de constructos creados puede derivarse de $\operatorname{dom}(\operatorname{base}_W)$.

La solución completa no está incluida. Se añadirá tras el intento y la revisión.

## 20. Criterios de revisión

La revisión comprobará por separado:

- Orientación de los pares.
- Exhaustividad de la relación directa.
- Cálculo de clausura.
- Uso correcto de reflexividad.
- Detección y justificación del ciclo.
- Diferencia entre función y relación.
- Consistencia de subíndices.
- Claridad de la explicación.

## 21. Incorporación a la especificación

Después de revisar el ejercicio:

1. Ajustaremos la notación si aparece alguna ambigüedad.
2. Redactaremos el fragmento profesional del grafo de constructos.
3. Lo someteremos a ejemplos de herencia múltiple y creación.
4. Decidiremos qué parte pertenece a `04-modelo-matematico` y cuál al futuro `11-constructos.md`.
5. Activaremos la Unidad 03.

## 22. Repaso

En la Unidad 03 reaparecerán:

- Relaciones, al calcular campos heredados.
- Clausuras, al recorrer antecesores.
- Funciones parciales, al resolver predeterminados.
- Conjuntos derivados, al definir posiciones válidas del estado.

Dos unidades después se pedirá detectar sin ayuda si una relación propuesta debería ser una función o una relación múltiple.
