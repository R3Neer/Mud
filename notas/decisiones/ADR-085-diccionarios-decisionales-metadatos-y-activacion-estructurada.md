---
id: D-085
title: "Diccionarios decisionales, metadatos y activación estructurada"
status: vigente
date: 2026-08-05
supersedes: []
superseded-by: []
questions:
  - "Q-061"
affects:
  - "acciones y subacciones, organización de archivos, operadores, tipos, diccionarios, productos, ausencia, cardinalidad, selección, activación inicial, Thing, Any, metadatos, magnitudes, texto, gramática, CST, AST, IR y diagnósticos"
---

# ADR-085 — Diccionarios decisionales, metadatos y activación estructurada

- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]
- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]] y [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]]
- Modificada por: [[ADR-096-modulos-callables-look-message-y-activacion|D-096]].

- Modifica: [[ADR-017-valor-predeterminado-de-todo-tipo|D-017]], [[ADR-035-organizacion-nombres-using-y-anclas|D-035]], [[ADR-037-campos-y-dominios-declarativos|D-037]], [[ADR-039-colecciones-y-diccionarios|D-039]], [[ADR-042-acciones-raiz-y-resultados|D-042]], [[ADR-047-cuantificadores-e-iteracion-finita|D-047]], [[ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]], [[ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]], [[ADR-061-resultados-fallidos-y-plantillas-text|D-061]], [[ADR-068-thing-universal-y-nombre-intrinseco|D-068]], [[ADR-074-uniones-nominales-y-estrechamiento|D-074]], [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]], [[ADR-083-magnitudes-base-sin-unidades|D-083]] y [[ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]].
- Amplía: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]], [[ADR-052-pipeline-materializadores-y-conformidad|D-052]] y [[ADR-053-operador-semantico-y-flujo-de-autoria|D-053]].
- Documentos afectados: capítulos 05 a 09, futuros capítulos 10 a 20, 24, 26, 32, 34 y 38, gramática, modelos sintácticos, diagnósticos y operaciones semánticas.

## Contexto

MUD ya dispone de colecciones, diccionarios exactos, composición secuencial mediante llamadas dentro de `then`, nombres nominales, activación inicial y plantillas `Text`. Varias decisiones posteriores muestran cuatro necesidades relacionadas:

1. Expresar políticas puras definidas por casos sin introducir una categoría general de función.
2. Separar de manera uniforme el contenido del mundo de los metadatos nominales y de procedencia.
3. Permitir que ausencia y cardinalidad modelen consultas parciales sin convertir la falta de resultado en fallo inmediato.
4. Hacer explícitas las fronteras entre API pública, auxiliares internas y catálogos iniciales de `thing` y reglas.

Esta decisión consolida esas necesidades y reemplaza toda formulación anterior incompatible dentro de su alcance. Los ADR modificados conservan el historial de las reglas previas.

## Decisión

### Acciones auxiliares `subaction`

Una declaración `subaction` posee el mismo contrato de participantes, `given`, guardas, efectos, postcondiciones, atomicidad y anclaje que una `action`, con una diferencia de accesibilidad:

```mud
subaction RemoveMoney for account: Account [mut]
given amount: Money {
    then account.balance -= amount
}
```

- Una `subaction` puede invocarse desde cualquier contexto semántico `then`, incluido el de una rule reactiva.
- No puede constituir una solicitud externa, un comando raíz ni una entrada de la API pública.
- Una `action` o `subaction` puede invocar actions ordinarias y subactions dentro de la misma resolución, sujeta al análisis de ciclos ejecutables.
- Toda la cadena participa en una única resolución atómica. Un resultado no aceptado o un fallo de cualquier llamada interna descarta también los efectos privados anteriores de sus llamadores.
- Su ancla conserva la categoría `action::*`; la clase pública o auxiliar forma parte del descriptor, no del prefijo de ancla.

El AST superficial conserva explícitamente la clase `PublicAction` o `Subaction`. La comprobación de accesibilidad se realiza después de resolver la llamada.

### Organización editorial de archivos

Los archivos deberían agrupar preferentemente conceptos, lugares, procesos o situaciones del mundo, no categorías sintácticas. Un archivo como `battle.mud` puede reunir `thing`, aliases, reglas, acciones, vistas y mensajes que describan conjuntamente la batalla.

Esta regla es informativa y no afecta a resolución, identidad, conformidad ni anclas. Una relación transversal puede ocupar un archivo propio cuando represente mejor el dominio.

### Operador `not in`

`not in` es la negación canónica de pertenencia. Se tokeniza como las dos palabras reservadas `not` e `in`, forma un único operador de comparación y tiene la misma precedencia y restricciones de encadenamiento que `in`.

No equivale a aplicar el prefijo `not` a una expresión incompleta. El AST conserva `NotMembership` como operador propio.

### Diccionarios exactos

El tipo ordinario conserva la forma:

```mud
A -> B
```

Una asociación se escribe `a -> b` y es un valor operativo. Puede aparecer en un literal de diccionario o añadirse de forma explícita:

```mud
add (a -> b) to dictionary
```

Los paréntesis pueden omitirse cuando la precedencia no resulte ambigua.

La aplicación por clave exacta es parcial:

- una clave presente produce su valor asociado;
- una clave ausente produce `empty` con la forma de salida declarada;
- la ausencia no produce `failed` por sí misma;
- el fallo aparece únicamente cuando el resultado vacío no pertenece al tipo, dominio o cardinalidad exigidos por el contexto.

Los diccionarios exactos:

- conservan mutabilidad exterior;
- continúan siendo enumerables por claves o asociaciones;
- admiten `ordered` con su semántica ordinaria;
- admiten `unique`, que exige unicidad global de valores asociados.

Una inserción o sustitución que haría aparecer el mismo valor bajo más de una clave en un diccionario exacto `unique` es una no-op completa. No modifica ninguna asociación y no produce `failed`.

### Diccionarios decisionales

El tipo:

```mud
A --> B
```

representa una política pura definida por ramas. Una rama se escribe:

```mud
selector --> result
```

Dentro del selector y del resultado, `value` es una palabra contextual vinculada a la entrada de tipo `A`.

Todo selector ordinario debe elaborar directamente a `Bool`. MUD no inserta implícitamente `value`, `==`, `is` ni `in`: deben escribirse de forma expresa `value == expresión`, `value in dominio`, `value is Tipo` o cualquier otra condición booleana pura. Una expresión desnuda que no produzca `Bool` es inválida. `_` es el fallback y solo se considera cuando ninguna rama ordinaria aplicable ha producido resultado.

Los resultados y selectores pueden leer estado externo. Cada lectura debe quedar registrada como dependencia de la rama y del diccionario. Todas las llamadas transitivas de una aplicación observan la misma instantánea estable del mundo.

Las ramas son estáticas durante la ejecución ordinaria y no admiten efectos, llamadas a acciones, asignaciones, `create`, `destroy` ni mutación. La edición del modelo puede crear, actualizar, retirar o mover ramas dentro del diccionario propietario, pero una rama no posee ancla pública ni descriptor metadata-bearing propio. El modelo resuelto usa una clave local de rama: el selector normalizado es la clave de una rama ordinaria y no puede repetirse dentro del mismo diccionario; `_` usa una clave de fallback propia y única. Cambiar solo el resultado conserva la clave; cambiar el selector retira estructuralmente la clave anterior y crea la nueva. Una rama nueva se inserta antes de `_` de forma predeterminada; en un decisional ordenado puede declararse una posición concreta.

Un diccionario decisional:

- no admite mutabilidad exterior;
- no admite capacidad interior `[mut]`;
- rechaza estáticamente cualquier `mut` aplicado a su tipo o lugar;
- no es una fuente de `for each`;
- puede referenciar directa o indirectamente otros diccionarios decisionales.

Todo componente recursivo del grafo de llamadas debe disponer de una medida bien fundada que disminuya estrictamente en cada arista que continúe el ciclo. El compilador debe demostrar la terminación mediante descenso numérico, reducción de cardinalidad, subestructuras estrictamente menores u otra prueba equivalente. La ausencia de prueba es un error estático.

#### Modo `ordered`

```mud
A --> B [ordered]
```

- Las ramas ordinarias se prueban en orden fuente.
- Gana la primera coincidencia.
- Los selectores pueden solaparse y el orden forma parte del valor.
- `_` debe ser la última rama efectiva; toda rama posterior es inalcanzable.
- Sin coincidencia ni fallback, la aplicación tiene cardinalidad derivada `[0..1]` y produce `empty` cuando no hay resultado.
- Con fallback, la cardinalidad derivada es `[1]`.
- `unique` es válido pero redundante; produce una sugerencia de eliminación.

El modo elaborado se denomina `FirstMatch`.

#### Modo no ordenado

```mud
A --> B
```

- Se evalúan todas las ramas ordinarias.
- Cada rama coincidente aporta un resultado.
- Los selectores pueden solaparse.
- El orden fuente no es semántico.
- Sin coincidencias se obtiene la colección vacía.
- `_` aporta exactamente un resultado solo cuando ninguna rama ordinaria coincide.
- La cardinalidad derivada es `[0..n]`, donde `n` es la cota máxima demostrable de ramas ordinarias coincidentes; con fallback la cota inferior pasa a `1`.
- `unique` deduplica resultados producidos por ramas distintas.

El modo elaborado se denomina `AllMatches`.

### Flechas, composición y productos

`->` y `-->` aceptan expresiones de tipo completas a ambos lados. Las cadenas son asociativas a la derecha:

```mud
A -> B -> C
```

se elabora como `A -> (B -> C)`. Lo mismo se aplica a cadenas mixtas. Cada cardinalidad o modificador pertenece exclusivamente a la flecha inmediatamente anterior:

```mud
A -> B [2] -> C [3]
```

se elabora como `A -> (B -> C [3]) [2]`.

Los paréntesis continúan siendo obligatorios para cambiar esa agrupación, para usar un diccionario completo como clave o para aplicar una colección exterior al valor diccionario completo.

No se introduce una categoría separada de función. La composición se expresa aplicando el resultado de un diccionario como entrada de otro; la aplicación encadenada `table[a][b]` consume diccionarios anidados.

Se añaden productos estructurales anónimos:

```mud
(A, B)
(a: A, b: B)
```

Sus valores se escriben respectivamente `(x, y)` y `(a = x, b = y)`. Son estructurales y se comparan componente a componente. Los nombres de variables que ocupan un producto posicional no crean nombres de componente. Los aliases declarados continúan siendo nominales aunque su representación coincida con un producto anónimo.

Los productos pueden actuar como claves exactas o entradas decisionales.

### `empty`, consultas parciales y cardinalidad

`empty` representa ausencia o colección vacía y no es un fallo por sí mismo. Toda operación parcial debe producir `empty` cuando no existe resultado. La comprobación posterior contra el tipo, dominio y cardinalidad esperados decide si esa ausencia es válida o causa `failed`.

Una consulta exacta ausente conserva la forma de salida `B`. Una consulta decisional `FirstMatch` sin coincidencia produce `empty`; una consulta `AllMatches` sin coincidencias produce una colección vacía válida.

### Cardinalidad omitida de campos almacenados

La omisión de cardinalidad ya no se normaliza universalmente a `[1]` antes de conocer el contexto del campo.

- En un campo almacenado sin mutabilidad exterior y con inicializador, se infiere la cardinalidad exterior exacta del valor inicial.
- Un valor unitario infiere `[1]`, una colección literal de tres miembros infiere `[3]` y `empty` infiere `[0]`.
- El contenido interno de un diccionario no altera la cardinalidad exterior: un diccionario es un valor aunque contenga varias asociaciones o ramas.
- En un campo con mutabilidad exterior, la omisión conserva `[1]`.
- Un campo almacenado sin inicializador usa la regla ordinaria del tipo y de su predeterminado, salvo las excepciones explícitas como `Any`.
- Los campos calculados `:=` conservan la forma inferida de su expresión o la forma declarada.

Cuando la cardinalidad inferida de un campo inmutable sea distinta de `[1]`, el compilador emite una sugerencia no bloqueante con una corrección que materializa la cardinalidad exacta en el texto fuente.

El AST superficial conserva que la cardinalidad fue omitida; tipado y elaboración determinan la cardinalidad efectiva y deben conservar suficiente procedencia para distinguir `InferredFromInitializer`, `OrdinaryScalarDefault` y `Explicit`. La codificación mecánica posterior todavía no está fijada.

### Selección

La expresión:

```mud
binding in source: predicate
```

es exclusivamente un filtro. El cuerpo posterior a `:` debe ser booleano. La expresión devuelve directamente los miembros originales aceptados, sin proyección, envoltura adicional ni aplanamiento.

Conserva multiplicidad, `unique`, orden, criterio de orden y la inferencia conservadora de cardinalidad de la fuente. Sobre un diccionario exacto, una vinculación por pareja produce otro diccionario con las asociaciones aceptadas.

### Activación inicial estructurada

D-096 sustituye la separación por categorías por una superficie única. Cada módulo puede aportar como máximo un `start with`, en forma directa o como bloque:

```mud
start with {
    Kingdom,
    CanGrow,
    all ActivableDeclarations
}
```

Cada expresión aporta cero, una o varias declaraciones activables `thing | rule`: una referencia individual aporta una, `empty` aporta cero, una colección aporta directamente sus miembros y `all D` materializa explícitamente un dominio enumerable. Una colección de colecciones es inválida.

Las identidades repetidas se deduplican y el orden no es observable. Las expresiones se evalúan solo con información disponible antes del mundo runtime y cada módulo solo puede activar declaraciones con ciclo de vida del mismo módulo. Las contribuciones de todos los módulos se materializan conjuntamente antes de la estabilización inicial.

El AST conserva una única secuencia `StartSet(contributions)`; la elaboración comprueba categoría activable, profundidad y evaluabilidad estática.

### `Thing` y `Any`

`Thing` continúa siendo la raíz incorporada de todas las `thing`. Está siempre efectiva, no aparece en `start with`, no puede declararse, crearse ni destruirse y queda excluida del catálogo producido por `all` en una sección `things`.

`Any` es el tipo superior de todos los valores MUD. Su dominio abierto incluye tipos básicos —incluido `Money`—, identidades `thing`, aliases, miembros de family, magnitudes, intervalos, colecciones, diccionarios, productos estructurales y descriptores first-class de declaraciones y tipos conforme a D-096. Los nodos sintácticos de implementación no son valores MUD por ese mero hecho.

`Any`:

- no es enumerable y rechaza `all Any`;
- no posee un orden total universal;
- compara igualdad solo entre tipos efectivos compatibles y delega en su igualdad;
- exige estrechamiento antes de una operación específica;
- conserva el estrechamiento dentro de la rama decisional donde se demostró;
- no posee predeterminado universal.

`Any` es una excepción explícita a D-017. Todo campo almacenado de tipo `Any` requiere inicializador explícito.

### Metadatos postfix

El acceso a metadatos usa el operador postfix `~` sin punto:

```mud
value~name
value~path
value~anchor
value~file
```

`value.~name` es inválido. El operador distingue metadatos nominales o de procedencia de campos ordinarios del mundo y tiene la misma precedencia postfix que `.`, `[]` y llamadas.

Los tipos incorporados iniciales son:

- `Name` para `~name`;
- `MudPath` para `~path`;
- `Anchor` para `~anchor`;
- `MudFile` para `~file`.

Son tipos nominales, no aliases implícitos de `Text`. Pueden declarar conversiones explícitas a `Text`. Las plantillas pueden renderizarlos contextualmente sin introducir compatibilidad nominal general.

#### `~name`

Se elimina la propiedad intrínseca `.name` y la forma especial `name = ...`. El metadato de presentación se declara o sobrescribe como:

```mud
~name = "El Castillo Negro"
```

Si se omite, su valor inicial deriva del nombre nominal no cualificado. `~name` no modifica identificador fuente, igualdad, orden nominal, `~anchor`, `~path` ni `~file`.

D-087 sustituye la mutabilidad runtime que esta decisión había introducido para `~name`. `~name` es un metadato configurable del modelo, pero todo acceso postfix `~` es de solo lectura durante la ejecución. Ninguna propiedad `~` puede aparecer como destino de una asignación o actualización runtime; los cambios configurables se realizan mediante edición del modelo y nueva elaboración. En aliases y miembros de `family`, los metadatos continúan separados del payload inmutable y no alteran igualdad estructural ni datos asociados.

La interpolación ordinaria de esos valores usa su `~name` efectivo.

#### Identidad y procedencia

Todo acceso `~` es runtime-readonly. `~anchor`, `~path` y `~file` son además propiedades intrínsecas, no configurables ni declarables: `~anchor` produce el ancla pública canónica; `~path`, el path MUD; `~file`, la procedencia física.

`~file` puede participar en cualquier expresión válida, pero el compilador emite un aviso cuando escapa de presentación o logging, o cuando su dependencia puede alterar comportamiento del mundo. El uso continúa siendo válido.

Sobre valores `MudPath`, `in` es reflexivo y compara segmentos completos: `p in q` es cierto si `p == q` o si `p` es descendiente de `q`.

#### Magnitudes y unidades

Las propiedades especiales de magnitudes y unidades usan la misma familia de metadatos:

```mud
~name = "metro"
~plural = "metros"
~abbreviation = "m"
~prefixes = all
~format = "{hour:2}:{minute:2}:{second:2}"
```

Cada metadato conserva su tipo, su modo almacenado o calculado y sus restricciones propias. El prefijo `~` no implica asignabilidad runtime.

### Plantillas y anclas

Se elimina `anchor{expression}`. El ancla se interpola mediante una expresión ordinaria:

```mud
"{expression~anchor}"
```

`~anchor` es además un valor tipado utilizable fuera de plantillas. El AST de plantilla conserva solo fragmentos e interpolaciones de valor; desaparece `AnchorInterpolation` y el token especial correspondiente.

## Modelo sintáctico y semántico

La gramática y los modelos deben distinguir como mínimo:

- `ActionDecl(PublicAction | Subaction, ...)`;
- `ExactDictionaryType` y `DecisionDictionaryType`;
- asociaciones exactas y ramas decisionales;
- productos posicionales y nombrados;
- `MetadataAccessExpr` y ausencia de objetivos asignables de metadato;
- `NotMembership`;
- un único `StartSet(contributions)` para activación unificada;
- cardinalidad omitida frente a explícita;
- ausencia del antiguo nombre intrínseco y de la interpolación especial de ancla.

La elaboración debe determinar para cada diccionario decisional, y cualquier representación posterior debe conservar o permitir reconstruir:

- modo `FirstMatch` o `AllMatches`;
- orden semántico;
- fallback;
- unicidad de resultados;
- cardinalidad derivada de aplicación;
- dependencias externas de selectores y resultados;
- clave local estable de cada rama, sin ancla pública;
- evidencia de terminación de cada componente recursivo.

Los diagnósticos mínimos nuevos son:

1. solicitud externa de una `subaction`;
2. uso de `subaction` como raíz exterior o fuera de un contexto semántico `then`;
3. `mut` exterior o interior en `-->`;
4. `_` no final o ramas inalcanzables en `FirstMatch`;
5. `unique` redundante en `FirstMatch`;
6. intento de iterar un decisional;
7. ciclo decisional sin prueba de descenso;
8. cardinalidad inmutable inferida distinta de `[1]`;
9. `all Any` o enumeración de `Any`;
10. campo `Any` sin inicializador;
11. intento de asignación o actualización runtime sobre cualquier acceso `~`;
12. uso semánticamente frágil de `~file`;
13. forma retirada `.name`, `name =` o `anchor{...}`;
14. uso de las secciones retiradas `things`/`rules` dentro de `start with`.

## Consecuencias

- MUD obtiene políticas puras por casos sin introducir funciones generales.
- La ausencia se conserva hasta que un contrato exterior exige presencia.
- La API externa distingue acciones públicas de auxiliares atómicas.
- La activación inicial reúne declaraciones activables `thing | rule` por módulo en un conjunto unificado, deduplicado y sin orden semántico.
- Identidad, presentación y procedencia quedan separadas y tipadas.
- Las flechas y productos permiten claves y políticas estructurales sin debilitar la nominalidad de aliases.
- `Any` sirve como frontera universal de valores sin inventar enumeración, orden ni predeterminado universales.

## Alternativas descartadas

### Hacer fallar inmediatamente una consulta parcial

Se descarta porque duplica en el operador una restricción que ya expresa la cardinalidad esperada y rompe la composición con filtros, fallbacks y tipos opcionales.

### Introducir una categoría general de función

Se descarta porque las políticas requeridas son valores declarativos, inspeccionables y editables por ramas. Los diccionarios decisionales conservan esa estructura explícita.

### Conservar `.name` y `anchor{...}` como excepciones

Se descarta porque obliga a mantener dos mecanismos paralelos para información que pertenece a una misma dimensión de metadatos.

### Hacer `Any` enumerable o darle un predeterminado arbitrario

Se descarta porque el dominio depende del proyecto, mezcla categorías sin un orden universal y no contiene un valor distinguido estable.

## Verificación

La suite debe cubrir al menos:

1. Capacidad exterior exclusiva de `action`, invocación de `action`/`subaction` desde contextos `then`, ancla compartida y rollback completo.
2. Tokenización maximal-munch de `-->`, `--` y `->`, y parseo de `not in`.
3. Consulta ausente exacta, asociación operativa y `unique` de valores como no-op.
4. Modos decisionales, solapamiento, fallback, cardinalidad derivada, deduplicación y prohibición de mutación o iteración.
5. Terminación aceptada y rechazada de ciclos decisionales y lectura de una sola instantánea.
6. Cadenas de flechas puras y mixtas con modificadores ligados a su flecha.
7. Productos posicionales y nombrados, igualdad estructural y uso como clave o entrada.
8. Inferencia `[0]`, `[1]` y `[n]` de campos almacenados inmutables, sugerencia de explicitación y excepción mutable.
9. Selección sin envoltura, proyección ni flatten, incluida la pareja de diccionario.
10. `start with` unificado por módulo, forma directa y de bloque, `empty`, colecciones de un nivel, deduplicación, `all D` cuando se materializa un dominio y rechazo de colecciones anidadas.
11. Efectividad permanente y exclusión catalográfica de `Thing`.
12. `Any`, estrechamiento, igualdad compatible, rechazo de enumeración y exigencia de inicializador.
13. Lectura y tipos de metadatos; solo lectura runtime de todo acceso `~`, separación de identidad y aviso de `~file`.
14. Pertenencia reflexiva y segmentada de `MudPath`.
15. Metadatos de unidades y magnitudes.
16. Retirada de `.name`, `name =` y `anchor{...}` y sustitución por `~name` y `~anchor`.

## Modificación vigente por D-096

Se sustituye la sección de activación estructurada que exigía bloques separados `things` y `rules`. `start with` acepta una contribución directa o un bloque unificado de expresiones que aportan declaraciones activables `thing | rule`; las identidades se deduplican y el orden no es semántico. La activación se agrega por módulo.

También se amplía `subaction`: puede invocarse desde cualquier contexto `then`, no solo desde otra action/subaction, sin adquirir capacidad de raíz exterior.
