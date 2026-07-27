# Semántica de ejecución

Este documento describe cómo una acción transforma un estado estable en otro. Es la parte que diferencia MUD de un DSL de datos.

## Modelo de estado

El mundo solo expone estados estables y confirmados. Una resolución crea estados tentativos internos, pero nunca publica una raíz o una onda parcial.

La transición general es:

```text
estado estable anterior
→ validación de solicitud
→ raíz tentativa
→ onda 1
→ onda 2
→ ...
→ estado estable tentativo
→ comprobación final
→ confirmar o revertir
```

`old` observa el estado estable anterior a la acción exterior completa.

## Inicio de una acción

Al comenzar la acción:

1. Se vinculan los participantes.
2. Se evalúan los valores `given`.
3. Se validan sus dominios.
4. Se evalúa `if`.
5. Se calcula la raíz.

Los `given` fuera de dominio rechazan la acción antes de evaluar `if`. Una precondición falsa también la rechaza. Ninguno de los dos casos produce efectos.

## Raíz y acciones compuestas

Una acción elemental declara efectos. Una acción compuesta declara llamadas a otras acciones. La especificación exige que las hojas de una composición:

- Lean el mismo estado inicial.
- Evalúen sus condiciones sobre ese estado.
- Formen una raíz simultánea.
- Comprueben sus `after` al final.

Las llamadas entre acciones deben ser acíclicas.

Hay una tensión que requiere formalización: las instrucciones de un `then` elemental se describen como secuenciales, mientras las hojas de una composición forman una raíz simultánea. La semántica deberá precisar qué lecturas observan efectos anteriores y cómo se detectan conflictos.

## Ondas causales

Después de la raíz:

1. Se construyen las vinculaciones `for` de la onda.
2. Todas las reglas de esa onda leen la misma instantánea.
3. `when` detecta transiciones por vinculación.
4. `changes` produce pulsos por cambios netos confirmados.
5. Los efectos se calculan de forma independiente.
6. Los efectos compatibles se combinan.
7. Los conflictos fallan la resolución.
8. El nuevo estado alimenta la siguiente onda.

Las vinculaciones se fijan al inicio de cada onda. Los cambios de pertenencia solo alteran la onda siguiente.

## Disparo reactivo

`when condition` se activa en una transición `false → true`. Esto implica que el runtime mantiene memoria del valor anterior por vinculación.

Queda por definir:

- Estado inicial de una vinculación recién creada.
- Qué ocurre al destruir y recrear una vinculación equivalente.
- Identidad de una vinculación con varios participantes.
- Cuándo se descarta su memoria.
- Interacción exacta entre `when`, `changes` y una raíz.

Estas preguntas son requisitos del runtime, no detalles de optimización.

## Invariantes y poscondiciones

Las reglas `always` se comprueban automáticamente sobre estados tentativos publicables. `after` se evalúa después de todas las ondas, respecto al resultado estable tentativo, y puede consultar `old`.

Orden propuesto de validación final:

1. Dominios, tipos y cardinalidades durante cada aplicación de efectos.
2. Reglas `always` al cerrar raíz y ondas según exija la semántica.
3. Estabilización.
4. `after`.
5. Confirmación.

La especificación afirma varios puntos de control, pero falta una definición operacional única que elimine cualquier duda sobre el momento exacto.

## Resultados

| Resultado | Significado |
| --- | --- |
| `accepted` | La solicitud, raíz, ondas, invariantes y poscondiciones son válidas |
| `rejected` | La solicitud es semánticamente válida, pero no admisible en este estado |
| `failed` | La evaluación encontró un error, conflicto o estado inválido |

Casos de `rejected`:

- `given` fuera de dominio.
- `if` falso.
- `after` falso.

Casos de `failed`:

- Conflicto de efectos.
- Ciclo u oscilación.
- Dominio, cardinalidad o referencia inválida.
- `always` incumplida.
- Fallo técnico o semántico propagado.

Toda salida distinta de `accepted` deja el mundo exactamente como estaba. Esta consecuencia está fuertemente implicada por la atomicidad y debe escribirse como regla normativa explícita.

## Conflictos

La especificación menciona asignaciones idénticas, asignaciones distintas, combinaciones aditivas y multiplicativas y operaciones de colección. Falta una tabla normativa que, para cada par de efectos concurrentes, determine:

- Si son compatibles.
- En qué orden se normalizan.
- Qué resultado producen.
- Qué diagnóstico emiten si colisionan.

Sin esa tabla, el resultado puede depender accidentalmente de la implementación.

## Terminación

Toda acción debe alcanzar un estado estable o fallar. No basta con imponer un número arbitrario de ondas y llamarlo semántica.

El runtime necesita:

- Detección de repetición de estados o configuraciones.
- Límite de recursos como salvaguarda técnica distinguible de un fallo semántico.
- Diagnóstico con el ciclo de anclas y campos implicados.
- Política para dominios infinitos o estado no comparable.

MUD no debe afirmar que no es Turing completo sin una prueba. La propiedad operativa relevante es la estabilización obligatoria de cada resolución.

## `allowed`

`allowed` ejecuta una acción en una copia especulativa:

- No modifica el mundo real.
- Devuelve verdadero para `accepted`.
- Devuelve falso para `rejected`.
- Propaga `failed`.
- Usa una rama aleatoria reproducible.

El grafo de consultas de admisibilidad debe ser acíclico. La implementación debería reutilizar el mismo motor transaccional que las acciones reales, cambiando únicamente el destino de la confirmación.

## `eventually`

`eventually` pregunta si existe una secuencia finita de acciones aceptadas que alcanza una condición. Solo es admisible cuando el compilador demuestra:

- Espacio de estado relevante finito y comparable.
- Acciones y `given` enumerables.
- Transiciones terminantes.
- Creación acotada.

Es una función avanzada de análisis de modelos, no un requisito para el núcleo inicial.

## Determinismo y azar

El comportamiento no puede depender del orden de archivos, estructuras de datos, hilos ni tiempo de máquina. Toda aleatoriedad debe derivarse de semillas y subsemillas reproducibles.

Antes de implementar azar deben decidirse:

- Identidad de cada punto aleatorio.
- Derivación de subsemillas.
- Momento de muestreo.
- Caché dentro de una instantánea.
- Comportamiento en especulación y reintentos.

