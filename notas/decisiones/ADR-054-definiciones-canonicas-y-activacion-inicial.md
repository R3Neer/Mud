# ADR-054 — Definiciones canónicas y activación inicial

- Estado: Vigente
- Fecha: 2026-07-28
- Relacionada con: [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]], [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]], [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|D-025]], [[notas/decisiones/ADR-035-organizacion-nombres-imports-y-anclas|D-035]], [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]]
- Cierra: [[notas/08-preguntas-abiertas#Q-044 — Identidad y referencias a `thing` futuras|Q-044]], [[notas/08-preguntas-abiertas#Q-045 — Contenido declarativo de `create`|Q-045]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[notas/03-semantica-de-ejecucion]], [[notas/08-preguntas-abiertas]], [[notas/12-destruccion-colecciones-y-grafo-activo]], [[especificacion/04-modelo-matematico]], futuros capítulos 06, 07, 08, 09, 11, 21 a 25 y 32

## Contexto

La sintaxis debe separar tres operaciones:

1. Definir qué es una declaración.
2. Decidir si participa en el mundo actual.
3. Modificar su estructura.

El modelo de uso adoptado es el de un juego con:

- Un catálogo estático de cosas y reglas posibles.
- Una selección de declaraciones presentes al comenzar.
- Operaciones runtime que retiran y vuelven a introducir las mismas identidades.

## Decisión

### Definición canónica única

Cada `thing` y cada regla tiene exactamente una definición completa de primer nivel en todo el programa.

```mud
abstract thing Vegetation {
}

thing Tree as Vegetation {
    age: Years
}

rule CanGrow on plant: Vegetation {
    ...
}
```

La definición fija:

- La categoría de la declaración.
- Su identidad y ancla.
- En una `thing`, su carácter abstracto o concreto.
- En una `thing`, sus antecesoras directas.
- Su cuerpo declarativo.

Las antecesoras directas de una `thing` no cambian durante la ejecución. `destroy` y `create` modifican su actividad, no su identidad ni su descriptor.

Dos definiciones completas con la misma ancla son un error estático aunque sus cuerpos sean iguales. El orden de archivos y declaraciones no resuelve la duplicidad.

### `create` solo activa

`create` es exclusivamente una instrucción runtime de activación:

```mud
create Tree
create CanGrow
```

Su objetivo debe resolver estáticamente a una única definición canónica de `thing` o regla. No admite categoría, modificador, lista de antecesoras ni cuerpo.

Una activación posterior a `destroy Tree` recupera la misma identidad `Tree`, con las mismas antecesoras y el mismo descriptor. Conforme a D-021, la carga almacenada se conserva.

Varias solicitudes concurrentes `create d` dirigidas a la misma declaración ausente se consolidan idempotentemente. Ya no existen fragmentos declarativos runtime ni fusión de cuerpos producida por `create`.

Una solicitud `create d` no modifica una declaración ya activa. La aplicabilidad de reglas y acciones que solicitan activaciones ya satisfechas continúa bajo Q-046.

### Conjunto inicial `start with`

Las definiciones de `thing` y reglas no quedan activas por el mero hecho de aparecer en el programa. Un programa puede contener una única declaración de primer nivel:

```mud
start with {
    Vegetation,
    Tree,
    CanGrow
}
```

Su contenido es un conjunto finito y no ordenado de referencias a definiciones canónicas activables. No es una secuencia de instrucciones ni una acción especial.

Por tanto:

- Solo admite referencias a `thing` y reglas.
- No admite `create`, `destroy`, `add`, `remove`, asignaciones, condiciones ni bloques `then`.
- El orden textual de las referencias no es observable.
- Las referencias se separan mediante comas.
- No se admite una coma después de la última referencia, conforme a la sintaxis general de colecciones de MUD.
- Una referencia repetida es un error estático de redundancia.
- Cada referencia debe resolverse de manera unívoca.
- El conjunto completo se materializa y valida atómicamente.
- Si la declaración se omite, ninguna `thing` ni regla está explícitamente activa al comienzo.

Sea $\mathcal L_P$ el conjunto de definiciones con ciclo de vida conocidas por el programa. La declaración determina:

$$
\operatorname{initiallyActive}_P
\subseteq
\mathcal L_P
$$

El estado inicial se construye materializando conjuntamente las declaraciones de $\operatorname{initiallyActive}_P$, validando sus dependencias y estabilizando las consecuencias iniciales antes de aceptar acciones externas.

Las acciones, aliases y magnitudes no pertenecen a $\operatorname{initiallyActive}_P$: no poseen este ciclo de vida. Una acción declarada forma parte de la API estática, aunque su invocabilidad efectiva pueda quedar suspendida por dependencias inactivas.

### Inicialización y reactivación

Los inicializadores de una definición se aplican cuando se materializa por primera vez su carga, ya sea mediante `start with` o mediante una instrucción `create`.

Después de `destroy d`, una nueva activación:

$$
\operatorname{stored}_{W'}(d)
=
\operatorname{stored}_{W}(d)
$$

No vuelve a ejecutar los inicializadores ni cambia el descriptor.

### Palabras reservadas y contextuales

`with` es una palabra reservada.

`start` es una palabra contextual: el parser la reconoce como introductor únicamente en la producción de primer nivel `start with`.

`abstract` también es contextual: el parser lo reconoce como modificador únicamente delante de `thing`. Fuera de esa posición puede usarse como identificador ordinario.

Las etiquetas reconocidas dentro de una declaración concreta, como `name` y `prefixes` en las declaraciones de unidades, son igualmente contextuales y no pertenecen por ello al catálogo de palabras reservadas.

No existe un token único ni una categoría léxica denominada «expresión reservada» para `start with`; es una producción gramatical formada por una palabra contextual y una palabra reservada.

## Sintaxis concreta

De manera esquemática:

```ebnf
thing-declaration
    ::= [ "abstract" ] "thing" nominal-name
        [ "as" nominal-name { "," nominal-name } ]
        body

create-instruction
    ::= "create" declaration-reference

start-with-declaration
    ::= "start" "with" "{"
        [ declaration-reference
          { "," declaration-reference }
        ]
        "}"
```

La escritura entre comillas en esta EBNF no implica por sí sola que `start` o `abstract` sean palabras reservadas; su clasificación léxica es la fijada en la sección anterior.

## Sintaxis abstracta

El AST debe distinguir, como mínimo:

```text
ThingDecl(anchor, mode, directAncestors, body)
RuleDecl(anchor, variant, body)
InitialActivationSet(references)
CreateReference(anchor)
DestroyReference(anchor)
```

`CreateReference` no contiene un descriptor. `InitialActivationSet` conserva procedencia textual para diagnósticos, pero su significado es un conjunto no ordenado.

## Consecuencias

- El programa determina un catálogo finito de identidades posibles; el mundo determina cuáles están activas.
- Un mismo nombre no designa encarnaciones runtime distintas.
- El grafo almacenado de especialización procede de definiciones estáticas, no de fragmentos acumulados durante la ejecución.
- El bypass de una antecesora inactiva continúa siendo temporal y restaura exactamente las aristas declaradas al reactivarla.
- Desaparecen los conflictos por fusión de cuerpos de `thing`.
- La modificación dinámica de propiedades, cuando esté permitida, debe expresarse mediante operaciones explícitas como `add` y `remove`.
- Crear cantidades no acotadas de individuos frescos exigiría una característica distinta; `create` no la introduce implícitamente.
- El LSP puede navegar desde toda activación hasta una única definición.
- El catálogo de palabras reservadas debe distinguir palabras duras de palabras contextuales.

## Alternativas descartadas

### Reutilizar un nombre para identidades sucesivas

Se descarta porque obliga a decidir si las referencias existentes siguen a la identidad antigua o se vuelven a enlazar al nuevo ocupante del nombre. La segunda opción puede invalidar dominios y cardinalidades almacenados; la primera conserva identidades ocultas que ya no coinciden con el nombre visible.

### Acumular antecesoras sin permitir retirarlas

Se descarta porque una nueva creación aparenta proporcionar una definición completa, pero conservaría silenciosamente todas las antecesoras anteriores. No resulta natural para lectores sin formación técnica y tampoco coincide con la expectativa habitual de herencia declarativa.

### Conservar la fusión fragmentaria de `thing`

Se descarta porque hace depender el descriptor de una identidad de qué reglas coinciden y en qué oleadas. Los cambios estructurales deben usar operaciones explícitas.

### Modelar `start with` como acción o `then`

Se descarta porque no tiene llamador, participantes, condiciones ni resultado operativo. Su contenido es un conjunto inicial, no una secuencia causal.

## Verificación futura

La suite deberá cubrir:

1. Una definición canónica por `thing` y regla.
2. Rechazo de dos definiciones con la misma ancla.
3. Rechazo de `create` con categoría, antecesoras o cuerpo.
4. Activación y destrucción de una `thing`.
5. Reactivación con conservación exacta de descriptor y carga.
6. Activación idempotente concurrente de una identidad ausente.
7. Un único `start with`.
8. Independencia respecto del orden de su lista.
9. Rechazo de coma final.
10. Rechazo de referencias duplicadas o no activables.
11. Estado inicial vacío cuando se omite la declaración.
12. Estabilización inicial antes de aceptar acciones externas.
13. Uso ordinario de `start` y `abstract` como identificadores fuera de sus contextos especiales.
14. Tratamiento contextual de `name`, `prefixes` y etiquetas equivalentes.
