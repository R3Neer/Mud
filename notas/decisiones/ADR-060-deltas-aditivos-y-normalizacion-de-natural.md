---
id: D-060
title: "Deltas aditivos y normalización de `Natural`"
status: vigente
date: 2026-07-29
supersedes: []
superseded-by: []
questions:
  - "Q-002"
  - "Q-006"
  - "Q-019"
affects:
  - "futuros capítulos `10-sistema-de-tipos.md`, `25-efectos.md`, `28-resolucion-de-acciones.md` y `29-ondas.md`"
---
# ADR-060 — Deltas aditivos y normalización de `Natural`

- Modifica: [[notas/decisiones/ADR-040-semantica-numerica-basica-restante|D-040]], [[notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola|D-045]] y [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]]
- Relacionada con: [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]]
- Preguntas relacionadas: Q-002, Q-006, Q-019
- Documentos afectados: futuros capítulos `10-sistema-de-tipos.md`, `25-efectos.md`, `28-resolucion-de-acciones.md` y `29-ondas.md`

## Contexto

D-040 establecía que la aritmética de `Natural` satura en cero. D-046 establecía a la vez que las actualizaciones aditivas compatibles se consolidan sumando deltas. Sin precisar el punto de saturación, estas reglas admitían dos resultados distintos:

```mud
# counter vale 0
counter -= 2
counter += 3
```

Saturar cada actualización produciría `3`; sumar primero los deltas y saturar una sola vez produciría `1`. La primera alternativa depende del orden y contradice el propósito conmutativo de los efectos aditivos.

## Decisión

### Valores y deltas

Un valor de tipo `Natural` nunca es negativo. Los estados almacenados, las instantáneas de onda y toda lectura de una expresión `Natural` pertenecen a:

$$
\mathbb N=\{0,1,2,\ldots\}.
$$

Un delta aditivo dirigido a un `Natural` no es a su vez un valor `Natural`. El IR lo representa como un entero con signo:

$$
\delta\in\mathbb Z.
$$

Por tanto, `counter -= 2` aporta el delta $-2$ y no almacena el valor $-2$.

### Aritmética pura

La resta ordinaria de valores `Natural` conserva la saturación inmediata de D-040:

$$
a-_{\mathsf N}b=\max(0,a-b).
$$

Una expresión pura siempre produce un valor de su tipo. En particular:

```mud
result: Natural := 0 - 2
```

produce `0`.

### Efectos acumulativos

Las instrucciones acumulativas no son azúcar de asignación:

```mud
target += amount
target -= amount
```

producen respectivamente deltas aditivos positivos y negativos. No se elaboran como:

```mud
target = target + amount
target = target - amount
```

Sean $n\in\mathbb N$ el valor del destino en la instantánea común y $\delta_1,\ldots,\delta_k\in\mathbb Z$ todos los deltas aditivos compatibles dirigidos a él durante un mismo lote causal. El valor que alimenta la instantánea siguiente es:

$$
n'=
\max\left(
0,\;
n+\sum_{i=1}^{k}\delta_i
\right).
$$

La suma de deltas ocurre antes de la normalización. Esta regla se aplica al consolidar la raíz y al cerrar cada onda, antes de construir la instantánea que podrá leer el lote siguiente.

En el ejemplo inicial:

$$
\max(0,0-2+3)=1.
$$

El resultado es el mismo para cualquier permutación de los deltas.

### Overlay secuencial de un `then`

Cada `then` conserva su orden textual para evaluar los operandos de efectos posteriores. Sea $\Delta_j$ la suma firmada de los deltas que ese mismo `then` ya ha emitido sobre un destino `Natural` después de sus primeras $j$ instrucciones.

Una lectura posterior del destino dentro del mismo delta privado observa:

$$
\operatorname{read}_{j}(n)=\max(0,n+\Delta_j).
$$

La proyección no sustituye ni recorta $\Delta_j$. El delta interno puede seguir siendo negativo aunque la lectura visible sea cero:

```mud
# counter vale 0
counter -= 2
snapshot = counter
counter += 3
```

La lectura de `counter` para calcular `snapshot` produce `0`, pero el delta acumulado final es $-2+3=1$ y el siguiente estado contiene `counter == 1`.

Un `then` nunca observa deltas privados de otros `then`. Todos ellos parten de la misma instantánea común y solo sus deltas finales se consolidan.

### Dominios y observación

Tras normalizar el resultado al tipo `Natural`, se comprueba el dominio refinado del destino conforme a D-037. Si el dominio excluye el valor normalizado, el estado tentativo es inválido y la resolución produce `failed`.

Ninguna regla reactiva, mensaje, `look`, `old` ni `changes` observa deltas negativos o valores intermedios de un `then`. Las ondas solo comparan instantáneas ya consolidadas y normalizadas.

### Alcance

D-060 fija únicamente las actualizaciones aditivas homogéneas. Permanecen vigentes:

- el conflicto entre asignación y actualización aritmética;
- el conflicto entre actualización aditiva y multiplicativa;
- la composición por producto de actualizaciones multiplicativas compatibles;
- las preguntas abiertas de D-046 sobre efectos estructurales y destinos parcialmente solapados.

## Consecuencias

- La saturación de `Natural` no rompe la conmutatividad de los deltas aditivos.
- El IR distingue valores naturales de deltas enteros firmados.
- El orden físico de reglas o hilos no altera el resultado consolidado.
- La secuencialidad privada afecta a las lecturas usadas para calcular efectos posteriores, no al punto global de normalización.
- `+=` y `-=` no pueden reescribirse mediante una asignación ordinaria.
- Los límites inferiores de dominios refinados se comprueban después de normalizar al tipo básico.

## Alternativas descartadas

### Saturar cada actualización

Para un valor inicial cero, aplicar `-2` y `+3` produciría `3` o `1` según el orden. Esto haría que efectos declarados compatibles dejaran de ser conmutativos.

### Exponer el acumulador negativo

Permitiría que una expresión de tipo `Natural` produjera temporalmente un entero negativo y filtraría detalles del IR a la semántica observable.

### Recortar también el delta privado

Si una lectura proyectada a cero reemplazara el delta $-2$ por cero, se perdería la compensación posterior con $+3$ y reaparecería la saturación por instrucción.

### Equiparar `-=` con asignación

Confundiría el efecto acumulativo con el cálculo puro saturado y haría imposible consolidar actualizaciones procedentes de reglas distintas mediante suma de deltas.

## Verificación

1. `Natural` nunca contiene ni expone un valor negativo.
2. La resta pura `0 - 2` produce `0`.
3. Sobre valor inicial `0`, los deltas `-2` y `+3` producen `1`.
4. Toda permutación de deltas aditivos produce el mismo resultado.
5. Un total todavía negativo se normaliza a `0`.
6. Una lectura privada tras un delta negativo observa `0` sin recortar el delta pendiente.
7. Una lectura privada posterior a varios deltas observa la proyección de su suma acumulada.
8. Un `then` no observa deltas de otro `then`.
9. Raíz y ondas entregan a la instantánea siguiente únicamente valores normalizados.
10. Un dominio refinado se comprueba después de la normalización básica.
11. Rechazo de la expansión de `+=` o `-=` a una asignación.
12. Conservación de los conflictos entre familias de efectos incompatibles.
