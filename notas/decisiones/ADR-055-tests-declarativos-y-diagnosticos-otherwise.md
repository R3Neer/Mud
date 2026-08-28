---
id: D-055
title: "Tests declarativos y diagnósticos `otherwise`"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-059"
affects:
  - "[[notas/preguntas/README|Preguntas activas]], futuros capítulos 06 a 09, 25, 28, 30, 43, 46 y 49"
---
# ADR-055 — Tests declarativos y diagnósticos `otherwise`

- Relacionada con: [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|D-025]], [[notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas|D-035]], [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]]
- Abre: [[notas/preguntas/Q-059-observacion-de-resultados-de-accion-en-tests|Q-059]]
- Ampliada por: [[notas/decisiones/ADR-071-vinculaciones-locales-en-bloques-booleanos|D-071]]
- Ampliada además por: [[ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]]
- Documentos afectados: [[notas/preguntas/README|Preguntas activas]], futuros capítulos 06 a 09, 25, 28, 30, 43, 46 y 49

## Contexto

MUD necesita pruebas que puedan leer y escribir quienes modelan el mundo, sin obligarlos a abandonar el lenguaje para describir el escenario esperado. Una prueba comparte con una acción el uso de efectos, estabilización y poscondiciones, pero no forma parte de la API del mundo:

- No tiene un solicitante externo.
- No modifica un mundo persistente.
- No expresa una operación disponible para personajes o sistemas.
- Su resultado informa al ejecutor de pruebas.

Tratarla como una variante de `action` confundiría ambas fronteras y haría natural, aunque incorrecto, asignarle un ancla `action::*`.

## Decisión

### Declaración propia

`test` es una palabra reservada que introduce una categoría de declaración propia:

```mud
test CounterIncreases {
    start with Counter

    then Counter.value += 1

    after {
        Counter.value == 1 otherwise "The counter did not increase"
        old Counter.value == 0 otherwise "The counter did not start at zero"
    }
}
```

Un test:

- Tiene nombre nominal en `PascalCase`.
- No declara `for`, `given`, `if`, `when` ni participantes.
- Declara exactamente un `start with`, un `then` y un `after`.
- No es invocable como `action` ni consultable como regla; en contexto de pruebas puede invocarse como operación `test` desde el `then` de otro test visible conforme a D-096.
- No puede ser objetivo de `create` o `destroy`.
- No puede aparecer en un conjunto `start with`.

De manera esquemática:

```ebnf
test-declaration
    ::= "test" nominal-name "{"
        test-start-with
        then-clause
        test-after-clause
        "}"

test-start-with
    ::= start-with-declaration

test-after-clause
    ::= "after" test-assertion
      | "after" "{" test-assertion { terminator test-assertion } "}"

test-assertion
    ::= boolean-expression [ "otherwise" text-expression ]
```

`test` no es un modificador contextual de `action`. El AST contiene una forma propia:

```text
TestDecl(anchor, initialActivationSet, thenBody, assertions)
TestAssertion(condition, optionalDiagnostic)
```

### Mundo aislado y `start with`

Cada ejecución de un test comienza con un mundo vacío, fresco y aislado. El `start with` de un test es una contribución propia de activación y no incorpora por sí mismo el `start with` ordinario de los módulos.

La superficie es la misma forma unificada de D-096: una contribución directa o un bloque de expresiones que aportan cero, una o varias declaraciones activables `thing | rule`. El orden no es observable y las identidades repetidas se deduplican. No contiene instrucciones `create`, asignaciones ni otros efectos, y una colección anidada es inválida.

Antes de ejecutar el test raíz se calcula estáticamente el cierre transitivo de tests que puede llamar, respetando `uses`, y se unen las contribuciones `start with` de todos ellos. Una llamada posterior a un test ya incluido no vuelve a materializar su activación; un ciclo ejecutable entre tests es inválido. Las declaraciones resultantes se materializan conjuntamente con sus inicializadores canónicos y el mundo se estabiliza antes del `then` raíz.

Sea $C(t)$ el cierre transitivo estático de tests alcanzables desde el test raíz $t$, sea $I_u$ la contribución de activación de cada test $u$ y sea $I_t^*=\bigcup_{u\in C(t)} I_u$. El estado previo al escenario se obtiene mediante:

$$
W_t^0
=
\operatorname{stabilize}
\bigl(
\operatorname{materialize}(P,I_t^*)
\bigr)
$$

La activación inicial ordinaria de los módulos no interviene en esta construcción.

### `then` y estado del escenario

`then` utiliza la semántica ordinaria de consecuencias y forma la transición probada. Puede mezclar efectos, locales y llamadas permitidas, incluidas operaciones `test` visibles en contexto de pruebas. Las asignaciones y demás modificaciones escritas al comienzo de `then` no pertenecen al estado inicial: son efectos de la prueba. Invocar un test cuyo `start with` ya participó en el cierre inicial no vuelve a materializar esa contribución.

El estado observado por `old e` dentro de `after` es $W_t^0$, anterior al `then` completo. No existe una frontera implícita entre instrucciones de preparación y de ejercicio según su posición textual.

La resolución del `then` incluye su raíz, sus ondas causales, las reglas `always` y la estabilización. El mundo resultante nunca se publica y se descarta al finalizar el test.

### Aserciones y `otherwise`

El `after` de un test contiene una o más aserciones ordenadas. Cada aserción consta de:

1. Una expresión pura de tipo `Bool`.
2. Un diagnóstico opcional introducido por la palabra reservada `otherwise`.

El diagnóstico debe ser una expresión pura de tipo `Text` y solo se evalúa cuando la condición asociada es falsa. Si se omite, el compilador ofrece una sugerencia y el ejecutor produce un diagnóstico predeterminado a partir de la condición y su procedencia.

```mud
after condition

after condition
    otherwise "Explanation"

after {
    firstCondition
    secondCondition otherwise "Second condition failed"
}
```

Todas las condiciones se evalúan sobre el mismo estado final estable y en orden textual. El ejecutor puede informar conjuntamente de todas las condiciones falsas. Una aserción no produce efectos.

`after` no devuelve la unión `Bool | Text`: la condición conserva tipo `Bool` y el diagnóstico conserva tipo `Text`.

### Resultado y descarte

La ejecución de un test produce exactamente uno de estos resultados para el ejecutor:

| Resultado | Causa |
| --- | --- |
| `passed` | El mundo inicial y el `then` se estabilizan y todas las aserciones son verdaderas |
| `failed` | Al menos una aserción es falsa y ninguna fase produce un error |
| `error` | No puede construirse el mundo inicial, falla la resolución del `then` o falla la evaluación de una aserción o diagnóstico |

`passed`, `failed` y `error` no son valores ordinarios del mundo ni sustituyen a `accepted`, `rejected` y `failed` de las acciones.

El estado aislado, los mensajes y cualquier otra salida producida durante el test se descartan siempre. El ejecutor puede conservar únicamente el resultado, los diagnósticos y la traza necesaria para explicarlos.

### Palabras y anclas

`test` y `otherwise` son palabras reservadas.

`abstract` continúa siendo contextual delante de `thing` y `always` es contextual delante de `rule`. Los modificadores y variantes no cambian la categoría del ancla:

```text
thing::world.Vegetation
rule::world.ValidWorld
test::world.CounterIncreases
```

Una `abstract thing` usa `thing::*`. Una regla `always` usa `rule::*`. Un test usa `test::*` porque constituye una categoría declarativa distinta.

## Consecuencias

- Los tests forman parte del lenguaje fuente, pero no del mundo ejecutado ni de su API pública.
- El compilador puede excluir `TestDecl` de una compilación de producción después de validarlo.
- El ejecutor de tests reutiliza el motor transaccional y causal sin publicar sus efectos.
- La selección por anclas `test::*` permite ejecutar un test, un path de MUD o un conjunto filtrado.
- No se infiere una fase de preparación a partir de las primeras instrucciones de `then`.
- La comprobación explícita del resultado `accepted`, `rejected` o `failed` de una acción invocada queda abierta en Q-059.

## Alternativas descartadas

### `test action`

Se descarta porque presenta el test como una variante de la API de escritura y haría incoherente asignarle una categoría de ancla distinta.

### `if` como precondición del test

Se descarta porque permitiría omitir silenciosamente una prueba cuando el mundo no cumpla la condición. El test construye deliberadamente su mundo mediante `start with`.

### Estado mutable dentro de `start with`

Se descarta porque mezclaría activación inicial y efectos. Los valores específicos del escenario se establecen en `then`.

### `after` de tipo `Bool | Text`

Se descarta porque mezcla comprobación y diagnóstico. `otherwise` conserva ambos tipos separados y permite mensajes distintos para varias condiciones.

## Verificación futura

1. Reconocimiento de `test` y `otherwise` como palabras reservadas.
2. Ancla `test::*` independiente de `action::*`.
3. Rechazo de `for`, `given`, `if` y `when` en un test.
4. Unión de `start with` del cierre transitivo estático de tests alcanzables, sin aplicar la activación ordinaria de los módulos.
5. Rechazo de instrucciones y asignaciones dentro de una contribución `start with` de test.
6. Materialización y estabilización antes del `then` raíz, llamada posterior sin reactivación y rechazo de ciclos ejecutables entre tests.
7. Lectura de `old` sobre el estado anterior al `then` completo.
8. Una y varias aserciones con diagnósticos opcionales.
9. Evaluación perezosa del diagnóstico `otherwise`.
10. Distinción entre `passed`, `failed` y `error`.
11. Descarte incondicional del mundo y de sus salidas.
12. Anclas `thing::*` para abstractas y `rule::*` para reglas `always`.

## Modificación vigente por D-096

El `start with` de test usa la superficie unificada de D-096. Para un test raíz se calcula estáticamente el cierre transitivo de tests que puede llamar y se unen sus contribuciones de activación antes de ejecutar el cuerpo. Los tests pueden cruzar módulos solo en contexto de pruebas, mediante operaciones de test visibles y dependencias `uses`; una llamada posterior no vuelve a ejecutar el `start with` del test alcanzado.
