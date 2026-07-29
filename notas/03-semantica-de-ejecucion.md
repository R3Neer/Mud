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

En el `after` de acciones y tests, `old` observa el estado estable anterior a la acción exterior completa. En el `when` o `if` de una regla reactiva, observa la instantánea de inicio de la onda anterior.

## Construcción del mundo inicial

Las definiciones canónicas de `thing` y reglas pertenecen al programa y no están activas por defecto. La declaración global única `start with` determina un conjunto inicial no ordenado de activaciones.

El runtime:

1. Resuelve todas sus referencias contra definiciones canónicas.
2. Materializa conjuntamente las cargas que todavía no existan.
3. Activa todo el conjunto sin observar el orden textual de la lista.
4. Valida dependencias, tipos, dominios, cardinalidades y reglas `always` efectivas.
5. Resuelve las consecuencias iniciales hasta alcanzar un primer estado estable.

Solo después puede aceptar acciones externas. Un fallo en este proceso significa que el programa no produce un mundo inicial válido; no es `rejected`, porque no existe una solicitud exterior. Las vinculaciones presentes en la primera instantánea materializada usan la inicialización reactiva descrita más adelante; Q-005 conserva abiertas únicamente su identidad canónica y la retirada o conservación posterior de memoria.

## Inicio de una acción

Al comenzar la acción:

1. Se vinculan los roles `for`: por identidad para `thing`, por valor para valores inmutables y por lugar para `mut` exterior.
2. Se validan tipos, cardinalidades y capacidades de los roles.
3. Para cada rol con mutabilidad exterior se conserva el lugar almacenado receptor.
4. Se evalúan los valores `given`.
5. Se validan sus dominios.
6. Se evalúa `if`.
7. Se calcula la raíz.

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

1. Se construyen las vinculaciones `on` de la onda.
2. Todas las reglas de esa onda leen la misma instantánea.
3. `when` evalúa activadores temporales por vinculación.
4. Los efectos se calculan de forma independiente.
5. Los efectos compatibles se combinan.
6. Los conflictos fallan la resolución.
7. El nuevo estado alimenta la siguiente onda.

Las vinculaciones se fijan al inicio de cada onda. Los cambios de pertenencia solo alteran la onda siguiente.

La activación o suspensión de una regla durante una onda tampoco modifica el conjunto de bindings ya fijado para esa onda. La proyección efectiva resultante se utiliza al construir la onda siguiente.

Cada `then` conserva su secuencialidad mediante un delta privado sobre la instantánea común. Los bloques no observan deltas parciales ajenos. Al consolidarlos, las activaciones mediante `create` preceden a las adiciones y las retiradas preceden a las destrucciones. Varias activaciones de una misma definición canónica ausente se consolidan idempotentemente; `create` no aporta cuerpos ni fragmentos declarativos. Los aliases no participan en efectos de ciclo de vida. Véanse [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]], [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]] y [[notas/decisiones/ADR-031-aliases-nominales-e-inmutables|D-031]].

Para un destino `Natural`, `+=` y `-=` aportan deltas enteros firmados. Una lectura posterior dentro del mismo `then` proyecta a cero el valor inicial más el delta privado acumulado, pero no recorta ese delta. Al consolidar la raíz o una onda, se suman primero todos los deltas compatibles y se aplica `max(0, ...)` una sola vez antes de validar dominios y formar la instantánea siguiente. Véase [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]].

La cardinalidad no se comprueba tras cada instrucción del delta privado. El compilador debe demostrar que el resultado final de cada `then` respeta todos los límites y que la consolidación de bloques potencialmente concurrentes también los conserva. Un bloque no puede depender de otro para reparar su cardinalidad. Si la prueba estática no es posible, el programa se rechaza, conforme a [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]].

## Disparo reactivo

Sea $v_n(b,e)$ el valor de `e` para la vinculación $b$ en la instantánea de inicio de la onda $n$. Un `when e` puramente booleano se activa exactamente cuando $v_{n-1}(b,e)$ es falso y $v_n(b,e)$ es verdadero.

`e changes` pulsa cuando $v_{n-1}(b,e)\ne v_n(b,e)$. El pulso se calcula para esa onda: no es estado almacenado, no se restablece a falso y puede producirse en ondas consecutivas. Los cambios transitorios que desaparecen antes de formar la instantánea siguiente no cuentan.

Las palabras `and` y `or` componen activadores. Un operando booleano ordinario se eleva a su transición `false` → `true`, de modo que puede combinarse con `changes` sin convertir el pulso en un nivel sostenido. `old e`, admitido en `when` e `if` pero no en `then`, evalúa `e` sobre la instantánea anterior y permite expresar magnitudes de cambio sin un operador `changes by`.

Una vinculación presente en la primera instantánea materializada por `start with` usa un anterior virtual falso para cada rama booleana elevada, pero compara esa instantánea consigo misma para `changes` y `old`. Una vinculación nacida después entra en la primera onda posterior en que está activa, memoriza allí toda su línea base sin disparar y empieza a comparar en la onda siguiente.

Queda por definir:

- Qué ocurre al destruir y recrear una vinculación equivalente.
- Identidad de una vinculación con varios participantes.
- Cuándo se descarta su memoria.

Estas preguntas son requisitos del runtime, no detalles de optimización.

## Invariantes y poscondiciones

Las reglas `always` se comprueban automáticamente sobre estados tentativos publicables. `after` se evalúa después de todas las ondas, respecto al resultado estable tentativo, y puede consultar `old`.

Puntos de validación confirmados y pendientes:

1. Las cardinalidades finales de cada `then` y de toda consolidación posible se demuestran estáticamente.
2. Los estados intermedios privados entre instrucciones de un mismo `then` pueden incumplir temporalmente la cardinalidad.
3. Los tipos, dominios y demás invariantes locales todavía necesitan un punto de comprobación normativo único.
4. Las reglas `always` se comprobarán al cerrar raíz y ondas según exija la semántica definitiva.
5. Tras la estabilización se evalúa `after`.
6. Solo entonces se confirma.

La especificación afirma varios puntos de control, pero falta una definición operacional única que elimine cualquier duda sobre el momento exacto.

Una regla `always` suspendida explícitamente o por una dependencia inactiva deja temporalmente de imponer su condición. Cuando vuelve a ser efectiva, el estado tentativo deberá satisfacerla antes de poder publicarse.

Una regla booleana inactiva no produce un booleano fijo. Su llamada se marca como fragmento borrado después de elaborar la expresión a la forma booleana núcleo. `not`, `and` y `or` propagan o eliminan ese hueco; si toda la expresión desaparece, se cierra con verdadero. La definición y sus límites se encuentran en [[notas/decisiones/ADR-022-borrado-de-reglas-booleanas-inactivas|D-022]].

## Estado almacenado y estado efectivo

Una resolución opera sobre una proyección efectiva derivada de información almacenada. `destroy` modifica la actividad lógica y puede suspender propiedades, reglas o acciones dependientes sin eliminar sus cargas. `create` puede restaurarlas. `remove` sobre una propiedad sí elimina su declaración y contenido almacenados.

Esta separación evita que la destrucción tenga que podar colecciones o reparar cardinalidades. Los detalles y las cuestiones restantes se encuentran en [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]] y [[notas/12-destruccion-colecciones-y-grafo-activo]].

## Observaciones y mensajes

Un `look` evalúa todas sus propiedades públicas sobre una misma instantánea estable y no produce efectos.

Un `message` puede detectar su condición durante las ondas de una acción, pero difiere la evaluación de sus propiedades públicas hasta el estado estable tentativo final. El runtime conserva para ello una ocurrencia pendiente y las vinculaciones necesarias. La multiplicidad, el orden, la guarda y el destino de las ocurrencias cuando la acción no se acepta permanecen abiertos en Q-052; ningún transporte externo debe observar un mensaje antes de que la resolución pueda confirmarse.

## Resultados

| Resultado | Significado |
| --- | --- |
| `accepted` | La solicitud, raíz, ondas, invariantes y poscondiciones son válidas |
| `rejected` | La solicitud es semánticamente válida, pero no admisible en este estado |
| `failed` | La evaluación encontró un error, conflicto o estado inválido |

El invocador externo recibe un objeto con el campo `state`. Si su valor es `failed`, el objeto contiene además `reason: Text`; este campo es obligatorio y explica la causa humana del fallo. Códigos, anclas, trazas y causas estructuradas pueden acompañarlo, pero no reemplazarlo.

Casos de `rejected`:

- `given` fuera de dominio.
- `if` falso.
- `after` falso.

Casos de `failed`:

- Conflicto de efectos.
- Ciclo u oscilación.
- Dominio, cardinalidad o referencia inválida.
- `always` incumplida.
- Fallo semántico propagado.

Todo caso normativo de `failed` debe asociarse a un diagnóstico `Text`. Una regla `always` obtiene el suyo del `otherwise` obligatorio, evaluado perezosamente sobre el estado tentativo infractor. La agregación estable de varias causas y la separación externa respecto de límites técnicos continúan bajo Q-007.

Un intervalo lineal con extremos invertidos se normaliza válidamente a `empty` y no añade por sí solo un caso de `failed`. Si ese vacío deja un `given` fuera de dominio o hace falso un `if` o `after`, se aplican los casos ordinarios de `rejected`. Si deja un valor almacenado fuera de dominio o incumple una regla `always`, el estado tentativo es inválido y se obtiene `failed`, conforme a [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]].

Toda salida distinta de `accepted` deja el mundo exactamente como estaba. Esta consecuencia está fuertemente implicada por la atomicidad y debe escribirse como regla normativa explícita.

Esta consecuencia ya es normativa en [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]]. Los contratos de reglas, especulación, alcanzabilidad, ondas, conflictos, iteración y azar se consolidan respectivamente en [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notas/decisiones/ADR-043-consulta-especulativa-allowed|D-043]], [[notas/decisiones/ADR-044-alcanzabilidad-eventually|D-044]], [[notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola|D-045]], [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]], [[notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita|D-047]] y [[notas/decisiones/ADR-048-azar-reproducible-y-fallos|D-048]].

## Ejecución de tests

Cada test se ejecuta sobre un mundo fresco y aislado. Su `start with` local sustituye al global, materializa únicamente las definiciones canónicas referenciadas y estabiliza el mundo antes de ejecutar `then`.

El `then` forma una única transición de prueba. Las asignaciones situadas al comienzo del bloque son efectos ordinarios; no crean una frontera implícita de preparación. Por ello, `old` dentro del `after` del test observa el estado estable producido por el `start with` local y anterior al `then` completo.

Después de estabilizar la transición, todas las aserciones `after` se evalúan sobre el mismo estado final y en orden textual. Una condición falsa produce su diagnóstico `otherwise`, si existe, y el ejecutor puede acumular varias condiciones falsas.

El resultado del test es:

- `passed` si todas las fases terminan correctamente y todas las aserciones son verdaderas;
- `failed` si existe al menos una aserción falsa y no se produce un error;
- `error` si falla la construcción inicial, la transición o la evaluación de una aserción o diagnóstico.

El mundo, los mensajes y las demás salidas se descartan siempre. Estos resultados pertenecen al ejecutor de tests y no son los resultados de acción `accepted`, `rejected` y `failed`. La semántica completa pertenece a [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]].

## Conflictos

La especificación menciona asignaciones idénticas, asignaciones distintas, combinaciones aditivas y multiplicativas y operaciones de colección. Falta una tabla normativa que, para cada par de efectos concurrentes, determine:

- Si son compatibles.
- En qué orden se normalizan.
- Qué resultado producen.
- Qué diagnóstico emiten si colisionan.

Sin esa tabla, el resultado puede depender accidentalmente de la implementación.

D-023 cierra únicamente la parte estructural necesaria para `create`, `destroy`, `add` y `remove`. No sustituye la futura matriz de asignaciones y actualizaciones aritméticas.

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
