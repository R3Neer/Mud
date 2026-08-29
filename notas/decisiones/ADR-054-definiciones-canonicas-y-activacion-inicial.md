---
id: D-054
title: "Definiciones canónicas y activación inicial"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-044"
  - "Q-045"
affects:
  - "[[notas/preguntas/README|Preguntas activas]], [[especificacion/04-modelo-matematico]], futuros capítulos 06, 07, 08, 09, 11, 21 a 25 y 32"
---
# ADR-054 — Definiciones canónicas y activación inicial

- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]
- Relacionada con: [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]], [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]], [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|D-025]], [[notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas|D-035]], [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]], [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]]
- Modificada por: [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]]
- Modificada por: [[notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco|D-068]]
- Modificada por: [[ADR-099-materializaciones-frescas-tras-destroy-create|D-099]]
- Cierra: [[notas/preguntas/Q-044-identidad-y-referencias-a-thing-futuras|Q-044]], [[notas/preguntas/Q-045-contenido-declarativo-de-create|Q-045]]
- Documentos afectados: [[notas/preguntas/README|Preguntas activas]], [[especificacion/04-modelo-matematico]], futuros capítulos 06, 07, 08, 09, 11, 21 a 25 y 32

## Contexto

La sintaxis debe separar tres operaciones:

1. Definir qué es una declaración.
2. Decidir si participa en el mundo actual y, para una `thing` concreta, si existe una materialización runtime activa.
3. Modificar la estructura de una materialización activa.

El modelo de uso adoptado es el de un juego con:

- Un catálogo estático de cosas y reglas posibles.
- Una selección de declaraciones presentes al comenzar.
- Operaciones runtime que retiran y vuelven a introducir las mismas identidades canónicas.
- Materializaciones runtime de `thing` concretas que pueden terminar con `destroy` y reconstruirse de forma fresca mediante un `create` posterior.

## Decisión

### Definición canónica única

Cada `thing` declarable y cada regla tiene exactamente una definición completa de primer nivel en todo el programa. La raíz incorporada `Thing` es la única `thing` sin definición fuente: su descriptor canónico pertenece al lenguaje, es abstracto y siempre efectivo. No puede redefinirse ni aparecer como objetivo de `create` o `destroy`.

```mud
abstract thing Vegetation {}

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

Las antecesoras directas de una `thing` no cambian durante la ejecución. `destroy` y `create` modifican su actividad y, para una `thing` concreta, terminan o construyen su materialización runtime; no cambian su identidad ni su descriptor canónico.

Dos definiciones completas con la misma ancla son un error estático aunque sus cuerpos sean iguales. El orden de archivos y declaraciones no resuelve la duplicidad.

### `create` activa una identidad canónica y materializa cuando corresponde

`create` es una instrucción runtime dirigida a una identidad canónica:

```mud
create Tree
create CanGrow
```

Su objetivo debe resolver estáticamente a una única definición canónica de `thing` o regla. No admite categoría, modificador, lista de antecesoras ni cuerpo.

Una activación posterior a `destroy Tree` recupera la misma identidad `Tree`, con las mismas antecesoras y el mismo descriptor. Conforme a D-099, si `Tree` es una `thing` concreta cuya materialización anterior terminó, `create Tree` construye una materialización fresca desde la definición canónica; no recupera la carga ni las modificaciones estructurales propias de la materialización destruida.

Varias solicitudes concurrentes `create d` dirigidas a la misma declaración ausente se consolidan idempotentemente. Ya no existen fragmentos declarativos runtime ni fusión de cuerpos producida por `create`.

Una solicitud `create d` no modifica una declaración ya activa. La aplicabilidad de reglas y acciones que solicitan activaciones ya satisfechas continúa bajo Q-046.

### Conjunto inicial `start with`

Las definiciones de `thing` y reglas no quedan activas por aparecer. Cada módulo puede aportar como máximo un `start with` unificado:

```mud
start with {
    Vegetation,
    Tree,
    CanGrow
}
```

Una contribución directa o cada expresión del bloque aporta cero, una o varias declaraciones activables `thing | rule`: una referencia aporta una, `empty` aporta cero y una colección aporta sus miembros. Para materializar un dominio enumerable explícito se usa `all D`; una colección de colecciones es inválida. Las identidades repetidas se deduplican y el orden no es observable.

Las expresiones solo pueden depender de información disponible antes de existir mundo runtime. Las contribuciones de todos los módulos se combinan, materializan y validan atómicamente y se estabilizan antes de aceptar acciones externas. Cada módulo solo puede activar declaraciones con ciclo de vida del mismo módulo.

Actions, aliases y magnitudes no son declaraciones activables. Cada test declara su propia contribución `start with`; para un test raíz se unen las contribuciones del cierre transitivo estático de tests alcanzables conforme a D-096.

### Inicialización y rematerialización

Los predeterminados e inicializadores de una `thing` concreta se aplican cuando se construye una materialización desde su definición canónica, tanto en la materialización inicial mediante `start with` o `create` como en una rematerialización posterior a `destroy`.

Después de un `destroy d` confirmado sobre una `thing` concreta, la carga propia y las modificaciones estructurales runtime de la materialización destruida se descartan. Un `create d` posterior:

- conserva la identidad, el descriptor y las antecesoras canónicas de `d`;
- reconstruye la estructura desde la definición canónica;
- vuelve a aplicar predeterminados e inicializadores;
- no recupera valores ni modificaciones estructurales de la materialización terminada.

Una `thing` abstracta no posee carga concreta propia que reinicializar. Para rules, D-099 fija que la memoria runtime de una activación explícitamente destruida tampoco atraviesa la nueva activación.

La suspensión de una declaración porque una dependencia dura está inactiva no equivale a `destroy`: esa suspensión puede conservar la carga que pertenece a la declaración suspendida.

### Palabras reservadas y contextuales

`with` es una palabra reservada.

`start` es una palabra contextual: el parser la reconoce como introductor de una contribución modular `start with` de primer nivel o del `start with` contenido en un test.

`abstract` también es contextual: el parser lo reconoce como modificador únicamente delante de `thing`. Fuera de esa posición puede usarse como identificador ordinario.

`always` es contextual delante de `rule`. D-055 introduce `test` y `otherwise` como palabras reservadas.

Los metadatos estándar como `~name` y `~prefixes` usan la gramática general postfix `~`; `name` y `prefixes` no son etiquetas contextuales especiales por esa razón.

No existe un token único ni una categoría léxica denominada «expresión reservada» para `start with`; es una producción gramatical formada por una palabra contextual y una palabra reservada.

## Sintaxis concreta

De manera esquemática:

```ebnf
thing-declaration
    ::= [ "abstract" ] "thing" nominal-name
        [ "as" nominal-name { "," nominal-name } ]
        [ body ]

create-instruction
    ::= "create" declaration-reference

start-with-declaration
    ::= "start" "with"
        ( expression
        | "{" [ expression { "," expression } [ "," ] ] "}"
        )
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

`CreateReference` no contiene un descriptor ni una nueva definición. `InitialActivationSet` conserva procedencia textual para diagnósticos, pero su significado es un conjunto no ordenado.

## Consecuencias

- El programa determina un catálogo finito de identidades posibles; el mundo determina cuáles están activas y qué materializaciones concretas existen.
- `destroy` + `create` no introduce una identidad nueva, aunque sí puede terminar una materialización y construir otra de la misma identidad canónica.
- El grafo declarativo de especialización procede de definiciones estáticas, no de fragmentos acumulados durante la ejecución.
- El bypass de una antecesora inactiva continúa siendo temporal y restaura las aristas declaradas al reactivarla.
- Desaparecen los conflictos por fusión de cuerpos de `thing`.
- La modificación dinámica de propiedades, cuando esté permitida, debe expresarse mediante operaciones explícitas como `add` y `remove` y pertenece a la materialización activa correspondiente.
- Crear cantidades no acotadas de individuos frescos exigiría una característica distinta; `create` no la introduce implícitamente.
- El LSP puede navegar desde toda activación o materialización hasta una única definición canónica.
- El catálogo de palabras reservadas debe distinguir palabras duras de palabras contextuales.

## Alternativas descartadas

### Reutilizar un nombre para identidades sucesivas

Se descarta porque obliga a decidir si las referencias existentes siguen a la identidad antigua o se vuelven a enlazar al nuevo ocupante del nombre. La segunda opción puede invalidar dominios y cardinalidades almacenados; la primera conserva identidades ocultas que ya no coinciden con el nombre visible.

### Hibernar la carga propia tras `destroy`

Se descarta conforme a D-099. Conservar la materialización propia haría que `destroy` se comportase como una mera desactivación y evitaría que una nueva materialización partiera del estado declarado.

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
5. Rematerialización de una `thing` concreta con conservación exacta de identidad y descriptor, pero reconstrucción de carga desde predeterminados e inicializadores.
6. Activación idempotente concurrente de una identidad ausente.
7. Como máximo un `start with` por módulo y ausencia válida de contribución en un módulo.
8. Independencia del orden y deduplicación dentro del conjunto unificado de contribuciones.
9. Admisión de contribución directa, bloque unificado y coma final opcional.
10. Rechazo de declaraciones no activables, activación de otro módulo y colecciones anidadas.
11. Proyecto cuyos módulos omiten `start with`, equivalente a una contribución inicial vacía.
12. Materialización conjunta de las contribuciones de todos los módulos y estabilización previa a acciones externas.
13. `Thing` siempre efectiva y no activable.
14. Descarte de carga y modificaciones estructurales propias tras `destroy`, sin borrar carga ajena meramente suspendida por dependencia.
15. Unión de contribuciones `start with` del cierre transitivo estático de tests alcanzables.
16. Disparo durante la estabilización inicial de un `when` cuya condición comienza verdadera.
17. Navegación LSP desde cada activación a una única definición.

## Modificación sintáctica por D-084

El cuerpo de una `thing` puede omitirse cuando no contiene miembros. `thing A`, `thing A {}` y `thing A;` fijan la misma definición canónica; solo su CST difiere.

## Modificación vigente por D-096

La activación inicial pasa a ser modular. Cada módulo puede contribuir como máximo un `start with`; todas las contribuciones se combinan y materializan conjuntamente antes de la estabilización. `start with` ya no separa `things` y `rules`, no establece orden y solo puede activar declaraciones con ciclo de vida del mismo módulo.
