---
title: Revisión 01 — Modelo mínimo de una puerta
unit: 1
status: completada-con-rectificacion
reviews:
  - "[[aprendizaje/respuestas/01-modelo-minimo-respuesta]]"
tags:
  - mud/aprendizaje
  - mud/revision
---

# Revisión 01 — Modelo mínimo de una puerta

> [!warning] Rectificación posterior
> Esta revisión corrigió adecuadamente la notación del ejercicio, pero aceptó una premisa semántica que después fue rechazada: MUD no divide los constructos en clases e instancias. En consecuencia, la función $\operatorname{kind}_W$ y la identidad didáctica `northGate#1` no son propuestas para el modelo normativo. La unidad queda completada como aprendizaje de funciones parciales, dominios, stores y redundancia representacional; su modelo concreto de constructos queda conservado únicamente como contramodelo.

## Resultado general

La respuesta demuestra que los conceptos básicos se han entendido:

- La clasificación entre constructo, identidad, campo y valor es correcta.
- Los conjuntos locales contienen los elementos esperados.
- Las funciones `kind` y `store` están aplicadas correctamente al ejemplo.
- La explicación de por qué un campo ajeno no debe tener valor es correcta.
- La pregunta posterior sobre $I_G$ detecta una redundancia real del modelo presentado.

La revisión también descubre una debilidad del propio ejercicio: con los conjuntos locales elegidos, la parcialidad del store no era necesaria para el mundo mínimo de una única puerta.

## 1. Corrección

### Clasificación

Correcta:

| Elemento | Clasificación |
| --- | --- |
| `Gate` | Constructo |
| `northGate#1` | Identidad runtime didáctica |
| `unlocked`, `open` | Campos |
| `true`, `false` | Valores |

### Conjuntos

La intención es correcta:

$$
C_G=\{\mathsf{Gate}\}
$$

$$
I_G=\{\mathit{northGate\#1}\}
$$

$$
F_G=\{\mathsf{unlocked},\mathsf{open}\}
$$

$$
V_G=\{\mathsf{true},\mathsf{false}\}
$$

Las familias tipográficas `\mathsf` y `\mathit` no cambian la matemática; solo hacen explícita nuestra convención para nombres de lenguaje e identidades.

### `kind`

La función escrita es correcta para la versión original del ejercicio:

$$
\operatorname{kind}_{W_G}:I_G\to C_G
$$

$$
\operatorname{kind}_{W_G}
(\mathit{northGate\#1})
=
\mathsf{Gate}
$$

La observación del autor permite simplificar el modelo general. Si la función ya tiene dominio $I_G$, el conjunto se puede recuperar:

$$
I_G=\operatorname{dom}(\operatorname{kind}_{W_G})
$$

Por tanto, no necesitamos almacenar $I_G$ además de `kind`, salvo que queramos deliberadamente una estructura con conjunto portador explícito.

### Store

Las dos asociaciones son correctas:

$$
\operatorname{store}_{W_G}
(\mathit{northGate\#1},\mathsf{unlocked})
=
\mathsf{true}
$$

$$
\operatorname{store}_{W_G}
(\mathit{northGate\#1},\mathsf{open})
=
\mathsf{false}
$$

## 2. La objeción sobre $I_G$

La objeción es válida.

En la primera propuesta:

$$
W_G=
\left(
I_G,
\operatorname{kind}_{W_G},
\operatorname{store}_{W_G}
\right)
$$

`kind` ya contiene su dominio. Si además exigimos que:

$$
\operatorname{kind}_{W_G}:I_G\to C_G
$$

entonces:

$$
I_G=\operatorname{dom}(\operatorname{kind}_{W_G})
$$

Mantener $I_G$ separado presenta dos costes:

1. Repite información.
2. Permite construir representaciones incoherentes donde $I_G$ no coincide con el dominio de `kind`.

La propuesta revisada es:

$$
\operatorname{kind}_W:
\mathcal I\rightharpoonup\mathcal C_P
$$

$$
I_W:=
\operatorname{dom}(\operatorname{kind}_W)
$$

$$
W=
\left(
\operatorname{kind}_W,
\operatorname{store}_W
\right)
$$

Aquí:

- $\mathcal I$ es el universo de identidades posibles.
- $\mathcal C_P$ es el conjunto de constructos proporcionado por el programa resuelto $P$.
- Una identidad existe en $W$ si `kind` está definida para ella.
- $I_W$ es una abreviatura derivada, no estado almacenado por duplicado.

## 3. Por qué no incluimos $C_G$, $F_G$ y $V_G$ en el mundo

Los conjuntos de constructos, campos y tipos de valores proceden del programa $P$. Son contexto estático:

$$
\mathcal C_P,\qquad
\mathcal F_P,\qquad
\mathcal V_P
$$

El mundo cambia durante la ejecución; el programa respecto al que lo interpretamos no cambia dentro de una resolución.

Podemos escribir:

$$
W\in\operatorname{Worlds}(P)
$$

Esto indica que $W$ solo tiene sentido respecto a las declaraciones de $P$, sin copiar esas declaraciones dentro de cada estado.

Si en el futuro MUD admite modificar su propio programa durante una ejecución, esta separación tendría que revisarse. No es una capacidad prevista actualmente.

## 4. Debilidad del ejercicio: la parcialidad

La respuesta dice correctamente:

> Si el store fuera total, cada identidad tendría valor para todos los campos.

Pero el tipo concreto escrito era:

$$
\operatorname{store}_{W_G}:
I_G\times F_G
\rightharpoonup
V_G
$$

y se había definido:

$$
F_G=
\{\mathsf{unlocked},\mathsf{open}\}
$$

Como la única identidad es una puerta y ambos campos le pertenecen, en ese ejemplo también sería posible:

$$
\operatorname{store}_{W_G}:
I_G\times F_G
\to
V_G
$$

La función parcial se justifica al utilizar el conjunto de todos los campos del programa:

$$
\operatorname{store}_W:
I_W\times\mathcal F_P
\rightharpoonup
\mathcal V_P
$$

porque entonces existen pares no aplicables, por ejemplo:

$$
(\mathit{northGate\#1},\mathsf{treasury})
$$

Esta imprecisión estaba en el diseño del ejercicio, no en la respuesta del autor.

## 5. Precisión notacional

En la tupla final se escribió:

$$
W_G=
\left(
I_G,
kind_G,
store_G
\right)
$$

pero las funciones se habían definido como:

$$
\operatorname{kind}_{W_G}
\qquad
\operatorname{store}_{W_G}
$$

No es un error conceptual, pero sí una inconsistencia. En una especificación formal, cambiar un subíndice puede designar otro objeto.

Con el modelo revisado, la forma coherente sería:

$$
W_G=
\left(
\operatorname{kind}_{W_G},
\operatorname{store}_{W_G}
\right)
$$

## 6. Claridad

Las explicaciones son breves y correctas. Podrían ganar precisión sustituyendo:

> todos los campos existentes en el mundo

por:

> todos los campos declarados por el programa usados como segundo componente del dominio

La primera frase comunica la intuición; la segunda fija exactamente qué conjunto interviene.

## 7. Valoración por dimensiones

| Dimensión | Estado | Observación |
| --- | --- | --- |
| Corrección conceptual | Conseguida | Clasificación y asociaciones correctas |
| Precisión formal | En progreso | Conviene mantener subíndices y alfabetos tipográficos |
| Exhaustividad | Adecuada | Se respondieron todos los apartados |
| Consistencia notacional | En progreso | `kind_G` frente a `kind_{W_G}` |
| Capacidad crítica | Destacada | La pregunta sobre $I_G$ mejora el modelo |
| Escritura LaTeX | En aprendizaje | La estructura ya es correcta; falta fluidez mecánica |

## 8. Revisión solicitada al autor

No es necesario repetir todo el ejercicio. Modifica únicamente:

1. La tupla del apartado 5 para usar el modelo revisado.
2. La explicación del apartado 6 para referirte al conjunto global de campos del programa.
3. Si estás de acuerdo, añade una frase indicando que $I_{W_G}$ puede definirse como el dominio de `kind`.

Si prefieres conservar $I_W$ como conjunto portador explícito, defiéndelo: ambas representaciones son matemáticamente posibles, pero sus costes deben quedar claros.

## 9. Próximo paso tras la revisión

Completada la corrección mecánica y registrada la rectificación semántica:

1. La Unidad 01 se considera completada en sus objetivos matemáticos.
2. Se incorporarán a [[especificacion/03-notacion]] las convenciones ya asentadas.
3. No se promoverá el modelo $\operatorname{kind}_W$ a [[especificacion/04-modelo-matematico]].
4. Se resolverá primero la ontología de los constructos y la semántica de `is` y `create`.
