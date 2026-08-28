---
title: Gramática concreta
aliases:
  - Sintaxis concreta de MUD
tags:
  - mud/especificacion
  - mud/gramatica
status: propuesta
normative: true
depends-on:
  - "[[05-texto-fuente]]"
  - "[[06-lexico]]"
questions:
  - Q-022
  - Q-059
  - Q-061
  - Q-062
  - Q-063
decisions:
  - D-015
  - D-025
  - D-028
  - D-029
  - D-031
  - D-035
  - D-036
  - D-037
  - D-038
  - D-039
  - D-041
  - D-042
  - D-044
  - D-047
  - D-048
  - D-049
  - D-050
  - D-054
  - D-055
  - D-056
  - D-057
  - D-058
  - D-059
  - D-061
  - D-062
  - D-063
  - D-064
  - D-065
  - D-066
  - D-067
  - D-068
  - D-069
  - D-070
  - D-071
  - D-072
  - D-073
  - D-074
  - D-075
  - D-076
  - D-077
  - D-079
  - D-080
  - D-081
  - D-082
  - D-084
  - D-085
  - D-086
  - D-087
  - D-088
  - D-090
  - D-091
  - D-092
  - D-096
---

# 07. Gramática concreta

## Estado y propósito

[[gramatica/mud.ebnf]] define la sintaxis completa de los archivos fuente ordinarios `.mud` de MUD 1.0. La superficie física adicional de `mud.module` se documenta por separado y su gramática completa permanece abierta en Q-062. Este capítulo fija cómo leerla, cómo resolver las construcciones contextuales y cómo agrupar expresiones. Las cuestiones listadas en el frontmatter afectan semántica posterior, no impiden reconocer la forma fuente.

## Producto del parsing

El resultado normativo del parsing es una CST sin pérdidas por archivo, definida en [[sintaxis/cst-sin-perdidas]]. La EBNF determina agrupación y orden de tokens significativos; la CST conserva además puntuación, terminadores y trivia.

La existencia de una CST no afirma que el archivo sea válido. La recuperación puede representar tokens ausentes o inesperados sin descartarlos.

## Validación anterior al AST

Después de construir la CST se comprueban restricciones sintácticas contextuales necesarias para producir un AST normalizado, entre ellas:

- Modificadores de colección duplicados.
- Declaraciones duplicadas del mismo metadato en un propietario, incluidas las unidades.
- Un argumento posicional posterior a uno nombrado.
- Combinaciones concretas prohibidas por este capítulo.

La resolución de nombres, tipos, dominios y efectos no pertenece a esta validación.

Un `given` reutiliza la expresión general de tipo, incluidos los diccionarios:

```mud
given prices: Product -> Money
```

La gramática puede conservar un modificador `mut` escrito dentro de esa expresión para diagnóstico, pero esa capacidad es estáticamente inválida: `given` nunca concede capacidad de escritura.

## Transformación abstracta

La proyección a AST está en [[sintaxis/cst-a-ast-superficial]]. Las producciones se cubren mecánicamente en `sintaxis/cobertura-sintactica.yaml`.

## Programa

Un archivo contiene una cabecera de declaraciones `using` seguida por las declaraciones de primer nivel:

```mud
using world.people
using physics.*
```

No existe una declaración de path; se deriva de la ruta. `using`, no `import`, es la única construcción de visibilidad entre paths de MUD.

Todos los `using` deben aparecer antes de la primera declaración de primer nivel. Intercalarlos es un error y nunca crea alcance local o secuencial. El orden entre varios `using` no decide ambigüedades.

Las categorías de primer nivel son:

- `thing`
- `alias`
- `family`
- `magnitude`
- Las tres formas de `rule`
- `action`
- `subaction`
- `look`
- `message`
- `test`
- `start with`

## `thing`

```mud
thing World

abstract thing Place

thing Alexandria as City, Place {
    ~name = "Alejandría"
}
```

`Thing` es la `thing` abstracta incorporada que actúa como tipo superior. Toda `thing` satisface `is Thing`. Una raíz sin `as` conserva cero antecesoras declaradas, pero recibe una arista semántica implícita hacia `Thing`. Es válido escribir `as Thing`, pero es redundante: una implementación conforme debe emitir un diagnóstico no bloqueante y ofrecer eliminarlo. `Thing` no puede declararse, crearse ni destruirse:

```mud
create Thing   # error estático
destroy Thing  # error estático
```

`Thing` está siempre efectiva sin aparecer en `start with`, y `all Thing` enumera únicamente las `thing` concretas efectivas, nunca el incorporado abstracto.

Toda `thing` expone propiedades y metadatos postfix separados de sus campos. `~identifier` conserva el identificador fuente y `~name` es presentación configurable. Todo acceso `~` es de solo lectura durante ejecución; ningún metadato es destino asignable. Los metadatos no son campos ordinarios.

La lista posterior a `as` no expresa prioridad. `create` no acepta aquí ni en ningún otro lugar un cuerpo:

```mud
create Alexandria
destroy Alexandria
```

### Inicializadores de `thing`

Una `thing`, concreta o abstracta, puede inicializar un campo almacenado ya aportado por su esquema heredado mediante una asignación sin redeclarar el campo:

```text
fieldName = static-expression
```

El objetivo se conserva como nombre de campo hasta la resolución. No declara un campo nuevo, no sustituye su predeterminado heredable y no puede dirigirse a un campo calculado. Debe resolver a un campo heredado: una misma `thing` no puede declarar localmente `fieldName` y además contener una instrucción separada `fieldName = ...`. La forma `fieldName: Type = value` es una sola declaración con predeterminado y sigue siendo válida. El valor del inicializador usa `constant-expression`, por lo que debe ser una expresión estática cerrada.

En una `abstract thing`, el inicializador no materializa carga propia; se conserva como contribución heredada para la primera materialización de descendientes concretos. En una `thing` concreta, el inicializador local se aplica a su propia primera materialización y no se hereda por sus descendientes. Un inicializador más específico sustituye a uno heredado menos específico. La especialización múltiple no obtiene prioridad del orden de `as`: el mismo origen se deduplica y contribuciones independientes e incomparables sobre el mismo campo entran en conflicto.

```mud
thing Kingdom {
    mut treasury: Money = 0
}

thing France as Kingdom {
    treasury = 20
}
```

En `France`, `20` inicializa únicamente la carga propia de `France.treasury` en su primera materialización. No se convierte en el predeterminado ni en un inicializador heredable para descendientes de `France`, y una reactivación posterior a `destroy France` conserva la carga almacenada en vez de ejecutar de nuevo el inicializador. Esta distinción conserva separados el predeterminado heredable y la contribución de primera materialización.

```mud
abstract thing RichKingdom as Kingdom {
    treasury = 20
}

thing Lydia as RichKingdom
```

`RichKingdom` no posee una carga concreta de `treasury`, pero su inicializador participa en la primera materialización de `Lydia`.

Es inválido mezclar declaración e inicializador separado del mismo campo en una definición:

```mud
thing Broken as Kingdom {
    treasury: Money = 10
    treasury = 20
}
```

`name = valor` no posee un significado intrínseco especial: si `name` es un campo almacenado heredado del esquema efectivo, usa esta misma forma; `~name` continúa siendo el metadato de presentación.

## Campos

Forma almacenada:

```text
[mut] fieldName: Type [in domain] [collection-specification] [= static-expression]
```

Forma calculada:

```text
fieldName [derived-value-shape] := value-expression
```

`derived-value-shape` puede ser `: Type`, `in domain` con colección opcional, o una especificación de colección sola. Por tanto son válidos tanto `area: Num in 0..* := width * height` como `area in 0..* := width * height`. Si se omite el tipo, debe poder inferirse unívocamente de la expresión, sin prioridades predeterminadas entre representaciones o formas contextuales compatibles. Si hay más de una solución, el tipo debe escribirse. Un campo calculado no admite `mut` exterior. Su forma puede declarar dominio, especificación de colección y capacidad interior `[mut]`.

El `mut` exterior se escribe antes del nombre porque califica el lugar almacenado, no el tipo de sus miembros. `fieldName: mut Type` no pertenece a la sintaxis. Los nombres de campo y los nombres de metadato ocupan espacios sintácticos distintos: `name: Text` declara un campo, mientras `~name = expresión` declara o modifica el metadato de presentación.

El valor de `=` es una expresión estática cerrada: se evalúa por completo al compilar, no lee estado, participantes, `given`, locales ni actividad del mundo y puede combinar literales, valores nominales y operaciones constantes. Por ejemplo:

```mud
allowed: Int Interval = 1..2 | 3..4
duration: Time = 1 hour + 30 minutes
```

La primera forma produce directamente un intervalo discontinuo normalizado.

```mud
mut population: Population in [0..*] [1] = 10 people
density := population / area
displayDensity: Density := density
```

Si la expresión de un campo calculado es además estática cerrada, el compilador debe sugerir la forma almacenada inmutable. No es un error ni una reescritura automática, y la sugerencia no aparece cuando el cálculo depende de estado runtime.

Una lista separada por comas construye una colección calculada e infiere tipo y cardinalidad cuando sean demostrables:

```mud
numbers := a * b, d, c / a
```

El dominio de un cálculo actúa como contrato. Una posible salida exterior produce warning y comprobación de transición; una salida necesariamente exterior produce error.

## Uniones de tipos y flechas exteriores

`|` une alternativas no flecha y tiene mayor precedencia que `->` y `-->`. Las dos flechas poseen la misma precedencia y se agrupan por la derecha:

```mud
A | B -> C | D       # (A | B) -> (C | D)
A | B --> C | D      # (A | B) --> (C | D)
A -> B -> C           # A -> (B -> C)
```

Una flecha debe ser la forma exterior completa del tipo. Un diccionario no puede aparecer como alternativa parcial de una unión, ni siquiera mediante paréntesis o a través de un alias cuya forma efectiva sea una flecha.


### Tipos callable y tipos obtenidos por reflexión

Los tipos callable se escriben a partir de los tipos de receptor/participantes y de la parte `given` de la firma:

```mud
Dragon.action(Volume)
(Attacker, Defender).action(Amount)
Dragon.rule(Limit)
Dragon.look(Detail)
```

La categoría forma parte de la construcción de tipo. Esta superficie no decide por sí sola la varianza ni todas las reglas de compatibilidad entre firmas: Q-063 mantiene abierto ese problema. La capacidad de raíz exterior de `action` tampoco se deduce únicamente del subtyping reflectivo.

Una expresión postfix terminada en `~type` puede ocupar una posición de tipo cuando la elaboración demuestra estáticamente que produce `Type`. Por ejemplo `alias Stats := MyDragon.Stats()~type` es válido; la llamada `MyDragon.Stats()` sin `~type` sigue siendo un valor y no una expresión de tipo. Un tipo callable como `Dragon.look(Detail)` ya denota `Type` y no necesita `~type`.
Son inválidos:

```mud
value: A | (B -> C)
value: (A -> B) | C
value: A | (B --> C) | D

alias Lookup := B -> C
value: A | Lookup
```

Son válidos:

```mud
value: (A | B) -> C
value: A -> (B | C)
value: (A | B) --> (C | D)
value: A -> Lookup
```

La restricción de aliases se comprueba después de la resolución nominal. Cada alternativa no flecha puede declarar dominio y una única especificación de colección final pertenece a la unión completa:

```mud
values: Nat in 0..10 | Int in -10..-1 [1..*] = [2 to Nat]
```

No se permiten cardinalidades por alternativa. Si una expresión contextual encaja en varias alternativas debe seleccionar una mediante `to`.

## Colecciones y diccionarios

La cardinalidad, cuando aparece, ocupa el inicio de los corchetes. Los modificadores pueden separarse por espacio o por coma:

```mud
citizens: Person [0..* unique ordered mut]
citizens: Person [0..*, unique, ordered, mut]
```

No se permite coma final. En un campo almacenado inmutable con inicializador, una cardinalidad omitida se conserva como omitida en el AST y se infiere como la cardinalidad exterior exacta del valor inicial:

```mud
one: Nat = 1                 # [1]
three: Nat = [1, 2, 3]      # [3]
none: Nat = empty            # [0]
table: A -> B = AValue -> BValue # [1]: el diccionario completo es un valor
```

Un campo con `mut` exterior conserva `[1]` cuando la omite. Los campos calculados `:=` conservan la forma inferida de su expresión. Una cardinalidad inmutable inferida distinta de `[1]` produce una sugerencia para escribirla explícitamente.

Las colecciones compatibles admiten `|`, `&` y `--`. `^` exige que el resultado cumpla las reglas de unicidad. Operan sobre multiplicidades o pertenencia, no concatenan:

```mud
leftChars: Char [1..5] = ["a"]
rightChars: Char [0..2] = empty
combinedChars := leftChars | rightChars
```

`empty` no es un fallo por sí mismo. Una consulta parcial produce `empty`; el fallo aparece únicamente cuando la forma exterior exigida no admite cardinalidad cero.

### Diccionarios exactos `->`

Un diccionario exacto consulta por igualdad de clave, es enumerable y admite mutabilidad exterior. Las asociaciones se escriben con la misma flecha:

```mud
capitalOf: Country -> City [2 ordered] =
    Spain -> Madrid,
    France -> Paris
```

Una clave ausente produce `empty`. Una asociación completa puede insertarse como valor operativo:

```mud
then add (Portugal -> Lisbon) to capitalOf
```

`unique` exige unicidad global de los valores asociados. Una inserción o sustitución que duplicaría un valor bajo dos claves es una no-op completa: no modifica ninguna asociación y no produce `failed`.

Añadir una asociación cuya clave ya existe sustituye atómicamente la asociación anterior cuando el resultado respeta el contrato:

```mud
then add (Spain -> Barcelona) to capitalOf
```

Los diccionarios exactos son enumerables. Una vinculación simple recorre claves y una vinculación por pareja recorre asociaciones:

```mud
action CollectCapitalData
for capitalOf: Country -> City [*],
    mut visitedCountries: Country [* unique],
    mut visitedCapitals: City [* unique] {
    then {
        for each country in capitalOf: {
            add country to visitedCountries
        }

        for each (country, capital) in capitalOf: {
            add country to visitedCountries
            add capital to visitedCapitals
        }
    }
}
```

Una consulta ausente conserva la forma de salida opcional:

```mud
capitalOf[Italy] # City [0..1], produce empty si Italy no está
```

Las claves pueden ser productos estructurales:

```mud
distance: (City, City) -> Length =
    (Madrid, Toledo) -> 74 km,
    (Madrid, Segovia) -> 91 km
```

Los operadores conjuntistas de exactos actúan sobre claves. Para una clave común, `|` y `&` conservan el valor izquierdo:

```mud
left: Key -> Nat = AKey -> 1, BKey -> 2
right: Key -> Nat = BKey -> 9, CKey -> 3

left | right   # AKey -> 1, BKey -> 2, CKey -> 3
left & right   # BKey -> 2
left -- right  # AKey -> 1
left ^ right   # AKey -> 1, CKey -> 3
```

`|` y `&` no son necesariamente conmutativos como diccionarios. El orden de inserción conserva primero el contenido izquierdo; `ordered by` normaliza después de calcular el contenido.

### Diccionarios funcionales `-->`

Un diccionario funcional es una política pura definida por casos. `value` designa la entrada dentro del selector y el resultado; `_` es el fallback:

```mud
dangerOf: Creature --> Danger [ordered] =
    value is Dragon --> Extreme,
    value is Predator --> High,
    _ --> Low
```

`ordered` significa `FirstMatch`: gana la primera rama aplicable y la aplicación produce `[0..1]`, o `[1]` con fallback. Sin `ordered` se evalúan todas las ramas ordinarias y se obtiene un resultado por coincidencia; `unique` deduplica resultados:

```mud
traitsOf: Creature --> Trait [unique] =
    value is Flying --> Aerial,
    value is Aquatic --> Aquatic,
    value is Magical --> Magical
```

Los selectores se escriben de forma explícita. No existe una abreviatura que inserte implícitamente `value`, `==`, `is` o `in`:

```mud
seasonName: Month --> Text [ordered] =
    value == January --> "winter",
    value in [March..May] --> "spring",
    value == June or value == July --> "summer",
    _ --> "other"
```

Por tanto, `January --> "winter"`, `[March..May] --> "spring"`, `Dragon --> Extreme` y `shop.discounted --> DiscountedPrice` no adquieren automáticamente significado de selector. Debe escribirse la comparación o pertenencia completa.

Aplicabilidad y producción de resultado se registran por separado. Una rama cuyo selector es aplicable puede producir `empty`; el fallback `_` solo aporta resultado cuando ninguna rama ordinaria aplicable ha producido uno. En `FirstMatch` se conserva el orden de prueba; en `AllMatches` se recogen todos los resultados realmente producidos.

Los selectores y resultados pueden leer estado externo puro:

```mud
priceOf: Product --> Money [ordered] =
    value in shop.discounted --> value.basePrice * shop.discount,
    _ --> value.basePrice
```

Esas lecturas crean dependencias explícitas hacia `shop.discounted`, `shop.discount` y `basePrice`. Todas las llamadas transitivas observan la misma instantánea.

No admite `mut` exterior ni `[mut]`, no se recorre directamente mediante `for each` y toda recursión debe poseer una medida bien fundada demostrable. Son pruebas válidas el descenso numérico, la reducción estricta de cardinalidad o el paso a una subestructura estrictamente menor; un ciclo sin evidencia demostrable es error.

Para recorrer resultados se recorre un dominio de entradas y se aplica el diccionario:

```mud
action CollectPrices
for products: Product [*], pricing: Product --> Money,
    mut prices: Money [*] {
    then for each product in products: {
        price := pricing[product]
        add price to prices
    }
}
```

Las ramas solo cambian mediante edición del modelo sobre el diccionario propietario. Una edición estructural puede insertar antes de `_` por defecto y puede actualizar, retirar o mover una rama, pero ninguna de esas operaciones se dirige a una ancla de rama ni presupone identidad pública independiente; su clave local se fija en la representación resuelta.

La aritmética de funcionales es extensional; no fusiona ramas:

```text
(F op G)[x] = F[x] op G[x]
```

`F | G`, `F & G`, `F -- G` y `F ^ G` combinan las colecciones obtenidas al aplicar ambos operandos a `x`. Sus fallbacks se evalúan de forma independiente. La unión y la diferencia simétrica de dos funcionales `ordered` pueden producir dos resultados y pierden `ordered` en general; intersección y diferencia pueden conservarlo.

No se permite combinar directamente un exacto con un funcional.

### `FirstMatch`, `AllMatches`, fallback y cardinalidad

En un funcional `[ordered]`, `unique` es válido pero redundante y produce una sugerencia de eliminación. Sin fallback, la aplicación tiene `[0..1]`; con fallback, `[1]`.

En un funcional no ordenado, cada rama ordinaria coincidente aporta como máximo un resultado. Con `n` ramas potencialmente coincidentes, la forma conservadora es `[0..n]`; un fallback eleva la cota inferior a `1`. `unique` deduplica resultados iguales de ramas distintas sin cambiar qué ramas fueron aplicables.

```mud
tagsOf: Creature --> Tag [unique] =
    value is Dragon --> Magical,
    value is FireCreature --> Magical,
    value is Flying --> Aerial,
    _ --> Ordinary
```

Para un dragón de fuego, `Magical` aparece una sola vez. La unión o diferencia simétrica de dos funcionales `ordered` pierde `ordered` cuando puede producir dos resultados distintos; intersección y diferencia lo conservan cuando mantienen la cota `[0..1]`.

### Encadenamiento de tipos de diccionario

Las flechas aceptan tipos completos y son asociativas a la derecha:

```mud
board: Square -> Piece [0..32 ordered]
nested: Name -> Coordinate -> Piece [*]
policyByMode: Mode -> Product --> Money [2..4 ordered]
```

El segundo ejemplo equivale a `Name -> (Coordinate -> Piece [*])`. Cada especificación de colección pertenece a la flecha inmediatamente anterior. Los paréntesis solo son necesarios para cambiar la agrupación natural o para delimitar otra construcción completa.

La aplicación encadenada consume cada nivel sucesivamente:

```mud
piece := boardByGame[game][coordinate]
```

La composición no introduce una categoría abstracta de función. Se expresa aplicando el resultado de un diccionario como entrada de otro:

```mud
weather := weatherOf[capitalOf[country]]
```

### Productos estructurales anónimos

Los tipos `(A, B)` y `(a: A, b: B)` son productos estructurales. Sus literales son `(x, y)` y `(a = x, b = y)`. Se comparan componente a componente y pueden actuar como claves exactas o entradas funcionales:

```mud
distance: (City, City) -> Length
label: (name: Text, count: Nat)
routePolicy: (origin: City, destination: City) --> Route
```

Los nombres de variables no crean nombres de componentes: `(x, y)` continúa siendo posicional aunque las variables se llamen `x` e `y`. Un alias declarado sigue siendo nominal aunque su payload tenga la misma forma:

```mud
alias Coordinate {
    x: Num
    y: Num
}

raw: (Num, Num) = (1, 2)
nominal: Coordinate = (x = 1, y = 2)
```

`raw` y `nominal` no son intercambiables sin una conversión nominal explícita. La compatibilidad de productos anónimos exige misma aridad, nombres de componente compatibles cuando existen y tipos componente a componente.

`ordered by ruta` pertenece a colecciones cuyos miembros ofrecen una ruta estable de campos, componentes o datos asociados. Cada acceso intermedio debe ser singular y el valor final debe poseer orden semántico total:

```mud
route: Terrain [* ordered by movementCost]
teams: Team [* ordered by captain.age]
```

Una `thing` no posee por sí misma orden total y no puede ser la clave final. Toda la ruta debe ser transitivamente estable: se rechazan campos almacenados mutables, cálculos con dependencias mutables y accesos intermedios cuyo estado posterior pueda alterar la clave. Una ruta opcional también se rechaza mientras no exista una posición definida para `empty`.

Si el miembro es una unión, la ruta debe existir sobre todas las alternativas alcanzables. Cada segmento conserva singularidad y estabilidad y las claves finales deben elaborar hacia un único tipo común totalmente ordenado. Una ampliación implícita única es válida; dos aliases meramente representacionales no se unifican. Cuando haga falta adaptar alternativas se declara primero un campo calculado común.

`ordered by` no admite expresiones arbitrarias. Si el criterio necesita una fórmula, se declara como campo o dato calculado y se ordena por su nombre. Las claves iguales conservan el orden relativo de inserción; no se desempatan por ancla, identidad ni orden de declaración de una `family`.

Se prohíbe `ordered by` para `Char`; su orden es Unicode. `Text` no acepta especificaciones de colección.

## Aliases

```mud
alias PlayerName := Text
alias UserName as PlayerName

alias Board := Square -> Piece [0..32 ordered]

alias Square {
    file: File
    rank: Rank
    label: Text := "{file}{rank}"
}

alias Coordinate {
    x: Num
    y: Num
}

alias PositionedCoordinate as Coordinate

alias Pagination {
    page: Nat = 1
    size: Nat = 20
}

alias LargePagination as Pagination {
    size = 100
}
```

Una declaración de alias puede escribir una lista no ordenada de antecesores con `as`. La definición local es opcional cuando los antecesores determinan una forma efectiva completa. Por ello son válidas tanto `alias UserName as PlayerName` como `alias PositionedCoordinate as Coordinate`. `alias A` sin antecesores ni definición es un error estático.

`:= tipo` solo introduce la representación de un alias nominal raíz. Un alias nominal con antecesores hereda la representación efectiva y no puede volver a declararla. En especial, `alias UserName as PlayerName := Text` es inválido.

Una representación `:= tipo` puede ir seguida por un cuerpo inmediato que contiene solo metadatos del alias. Así un alias representacional puede documentarse o configurarse sin adquirir componentes estructurales.

El cuerpo estructural puede contener componentes almacenados, campos derivados y sobrescrituras de predeterminados heredados. Una sobrescritura `nombre = valor` solo cambia el predeterminado efectivo: no puede alterar tipo, dominio, cardinalidad, orden, unicidad ni capacidad interior.

Los literales estructurales son contextuales:

```mud
(E, Four)
(file = E, rank = Four)
(size = 30)
```

La forma posicional debe proporcionar todos los componentes. Si se omite alguno, la forma debe ser completamente nombrada: los omitidos toman su predeterminado explícito o el predeterminado de su tipo. Los componentes nombrados pueden saltar componentes anteriores o intermedios, pero los presentes conservan el orden relativo de declaración. No se permite mezclar posiciones y nombres:

```mud
pagination: Pagination = (2, 30) # válido
pagination: Pagination = (2)     # inválido: posición parcial
pagination: Pagination = (size = 30) # válido: page conserva 1
```

Un componente no admite `mut` exterior porque el valor de alias y cada uno de sus componentes son inmutables. Sí puede escribir `[mut]` en su especificación de colección para conceder capacidad interior sobre las `thing` contenidas directamente; esa capacidad no permite reemplazar la colección.

Un campo derivado de alias usa la misma sintaxis que los demás campos calculados, incluida una forma declarada opcional:

```mud
alias Squad {
    members: Soldier [*]

    wounded [* mut] :=
        soldier in members:
            soldier.health < MaximumHealth
}
```

La colección derivada no es una subcolección almacenada de `members`: posee contrato propio. `[mut]` concede capacidad interior aunque la fuente no la conceda. La selección se fija para la instantánea en evaluación; después de consolidar los efectos se recalcula sobre el nuevo estado, por lo que los miembros pueden entrar o salir automáticamente. Una colección almacenada nunca se autopoda por esta razón.

## Familias

```mud
family Terrain {
    movementCost: Nat = 1
    passable: Bool = true
    costly := movementCost >= 3

    Plain,
    Forest {
        movementCost = 2
    },
    Water {
        movementCost = 0
        passable = false
    }
}
```

Los datos aparecen antes del primer miembro. Un dato almacenado puede llevar, después de su predeterminado opcional, un cuerpo inmediato que contenga solo declaraciones `~...`. Un dato calculado puede llevar el mismo metadata-body inmediato. Q-061 mantiene abierta si esta producción debe conservar `derived-value-shape` o restringirse a la forma `nombre [: Tipo] := expresión`; hasta resolverla, la EBNF conserva la forma más amplia.

El metadata-body describe el descriptor uniforme del dato de la `family`, no el valor concreto proyectado por cada miembro. Por ejemplo:

```mud
family Terrain {
    movementCost: Nat = 1 {
        ~summary = "Coste base de movimiento"
    }
    costly := movementCost >= 3 {
        ~summary = "Indica terreno costoso"
    }

    Plain,
    Mountain {
        movementCost = 4
    }
}
```

La asignación `movementCost = 4` del miembro es solo una sobrescritura de valor del dato almacenado. No admite metadata-body, no introduce otra ancla y no modifica los metadatos del descriptor `movementCost`. La expresión de un dato calculado se evalúa estáticamente para cada miembro después de resolver los datos almacenados, puede consultar otros datos asociados mediante nombres no cualificados y debe tener dependencias acíclicas. El bloque de un miembro solo puede asignar datos almacenados.

Los miembros se separan por comas y no admiten coma final. `ordered family` hace comparables sus miembros en orden de declaración y permite usar rutas de datos asociados, incluidos los calculados estables, como claves de `ordered by` en colecciones.

## Magnitudes

Magnitud base:

```mud
magnitude Probability: Num in [0..1] {}

magnitude Length: Num in [0..*] {
    root unit meter {
        ~plural = "meters"
        ~abbreviation = "m"
        ~prefixes = all
    }
}
```

Magnitud derivada:

```mud
magnitude Speed: Num in [0..*] := Length / Time {
    unit fastie := 1 m/s {
        ~plural = "fasties"
        ~abbreviation = "fst"
    }
}
```

Magnitud de punto:

```mud
magnitude RawInstant point over Time {}

magnitude Timestamp point over Time {
    ~format = "{day}:{hour:2}:{minute:2}"
}

magnitude WorkdayTime point over Time in [0..28_800] {
    ~format = "{hour:2}:{minute:2}"
}

magnitude TimeOfDay point over Time in [0..86_400) cycle {
    ~format = "{hour:2}:{minute:2}:{second:2}"
}
```

Una magnitud base tiene una de dos formas: un cuerpo vacío sin unidades, o exactamente una `root unit nombre` seguida de cero o más unidades alternativas. No puede declarar una alternativa sin raíz. La ausencia de raíz es una elección semántica completa: la magnitud conserva una dimensión nominal independiente, pero sus valores no escriben unidad. No equivale a su representación numérica, a otra magnitud sin unidades ni al elemento neutro dimensional.

```mud
chance: Probability = 0.75
explicitChance := ratio to Probability
```

Un literal numérico desnudo puede tomar el tipo de una magnitud sin unidades cuando el contexto esperado la determina unívocamente. Una expresión numérica general exige `to` para materializarla. La aritmética conserva el factor nominal aunque este no tenga forma de unidad; la proyección visible de unidades puede coincidir entre dimensiones estáticamente distintas. Una cantidad que sí escribe unidad solo aporta los factores determinados por ella: el contexto no añade factores invisibles.

Una magnitud derivada solo declara unidades nominales alternativas `unit nombre := equivalencia`; una magnitud de punto no declara unidades. En esta última, `in` y el dominio son opcionales: sin ellos se usa el dominio completo de la coordenada subyacente, un intervalo ordinario la acota sin envolver y `[a..b) cycle` añade normalización cíclica. `cycle` modifica el dominio completo, no forma parte de la expresión intervalo, y solo una magnitud de punto lo admite.

El cuerpo de una unidad contiene exclusivamente declaraciones generales `~...`; no existe `unit-property`. `~prefixes: Prefix [* unique] = empty` usa el tipo incorporado `Prefix`: omitirlo o escribir `empty` no habilita ninguno, `all` habilita el catálogo SI decimal completo y una colección como `[kilo, milli]` selecciona esos valores incorporados. `~name`, `~plural` y `~abbreviation` usan el mismo sistema general de metadatos y todo acceso runtime mediante `~` es de solo lectura.

Una cantidad puede omitir el espacio antes de su unidad, pero el formateador lo inserta: `3m` y `3 m` tienen el mismo AST y la segunda es canónica.

`~format` es opcional y usa la sintaxis general de plantilla `Text`: los huecos son código y `:2` fija aquí dos posiciones a la izquierda del punto. Sin él no existe una representación especial de punto: se aplica exactamente la representación textual ordinaria de una magnitud, con la coordenada en la unidad raíz y la abreviatura o nombre de esa unidad. Con él, el primer componente es la coordenada en esa unidad —reducida por el ciclo, si existe— y cada componente siguiente se extrae dentro del anterior. Un contenedor no obvio se hace explícito, por ejemplo `~format = "{week from year:2}"`.

Fuera de `~format`, la extracción exige el punto:

```mud
minute from hour in time
picosecond from second in time
week from year in date
```

La forma es una sola construcción sintáctica. El receptor debe ser una magnitud de punto; ambas unidades pertenecen a su magnitud subyacente; la unidad extraída no supera a la contenedora; el resultado es `Nat`. Se usa el origen canónico y el resto euclídeo, con un posible último componente parcial cuando las unidades no dividen exactamente. La extracción no depende de `~format`.

Las formas producidas por `~format` ocupan el token contextual `POINT_LITERAL`. El tipo esperado selecciona una única magnitud de punto y el literal debe reproducir exactamente su forma canónica. Un formato que no pueda invertirse unívocamente es inválido. Los componentes más finos que el último representado toman valor cero.

Sin `~format`, el literal se escribe como una cantidad ordinaria con unidad compatible. Todo literal debe pertenecer al dominio antes de aplicar normalización cíclica; por ejemplo, `26:00:00` es inválido para `TimeOfDay`.

## Activación inicial `start with`

Cada módulo puede declarar como máximo un `start with`. No es un `main`, no invoca módulos y no establece un orden de inicialización. La ausencia de `start with` en un módulo equivale a una contribución vacía.

La declaración acepta una contribución directa o un bloque unificado:

```mud
start with Kingdom
```

```mud
start with {
    Kingdom,
    Place,
    CanEnter,
    empty
}
```

Cada expresión debe ser estática y puede aportar cero, una o varias declaraciones activables `thing | rule`. Una colección aporta directamente sus miembros; no se admiten colecciones anidadas. Las identidades repetidas se deduplican y el orden fuente se conserva solo como procedencia, no como prioridad semántica.

Un `start with` solo puede activar declaraciones con ciclo de vida del mismo módulo. Las contribuciones de todos los módulos se materializan conjuntamente antes de la estabilización inicial. `Thing` permanece siempre efectiva y no forma parte de la colección activable.

`all D` puede materializar un dominio enumerable cuando una contribución necesita una colección explícita; `all` sin operando conserva su significado contextual.

## Participantes

`for` vincula roles suministrados de cualquier tipo de valor declarado. Un rol puede ser individual o colectivo, restringir sus valores mediante `in dominio` y admitir la especificación completa de colección. El dominio se escribe después del tipo y antes de la colección. `on nombre: Tipo` usa el universo implícito de `thing` concretas y activas compatibles con ese tipo; en cambio `on nombre[: Tipo] in fuente` vincula desde una fuente finita enumerable y puede por ello relacionar otros valores. La forma relacionada puede escribir el tipo para refinar nominalmente los miembros de la fuente.

```mud
rule CanAttack for attacker: Army, defender: Army
given maximumDistance: Length {
    distance <= maximumDistance
}

rule AllAdults for people: Person in EligibleCitizens [1..*, unique] {
    forall person in people: person.age >= 18
}

rule IsWeekend for day: Day {
    day == Saturday or day == Sunday
}

rule Starve on
    world: World,
    kingdom in world.kingdoms [mut]
{
    when kingdom.food == empty
    then kingdom.population -= 1
}
```

El tipo puede inferirse en un participante relacionado: normalmente basta `kingdom in world.kingdoms`.

También puede escribirse el tipo para refinar nominalmente los miembros de la colección, no para repetir necesariamente su tipo declarado:

```mud
rule MutualFriends on
    alice: Person in bob.friends,
    bob in alice.friends
{
    when alice.mood changes or bob.mood changes
    then create FriendshipChanged
}
```

Todos los nombres de una cabecera `on` son visibles en la cabecera completa. Sus tipos y restricciones se resuelven conjuntamente, de modo que se admiten referencias adelantadas y ciclos cuando existe una solución nominal única. Cada rol parte de las `thing` concretas y activas de su tipo efectivo; las vinculaciones son el join finito que satisface todas las pertenencias sobre una misma instantánea. No se impone que roles distintos reciban identidades distintas y dos orientaciones simétricas constituyen vinculaciones diferentes.

Todo participante `for`, `on` y `given` tiene identificador explícito. No existe participante anónimo, tampoco con cardinalidad efectiva `[1]`. Una cabecera puede agrupar identificadores que comparten tipo y metadata-body, por ejemplo `for attacker, target: Fighter { ... }`; el grupo es azúcar y cada descriptor conserva su propia ancla.

En una action, `mut` antes del nombre de cualquier rol `for`, incluida la cardinalidad `[1]`, concede mutabilidad exterior sobre la colección suministrada. El receptor correspondiente debe ser un lugar almacenado con esa capacidad; un literal o una colección calculada no satisfacen el contrato. El `mut` de la especificación de colección continúa concediendo capacidad interior sobre las `thing` miembro:

```mud
action Treat for
    mut patients: Person [1..10, unique, mut]
{
    then for each patient in patients: {
        patient.health += 10
    }
}
```

La declaración anterior puede cambiar la membresía u orden de la colección almacenada recibida y modificar sus miembros. `mut patients: Person [*]` concede solo la primera capacidad; `patients: Person [*, mut]`, solo la segunda.

Escribir capacidad interior sobre valores inmutables es legal, pero el compilador sugiere retirarla cuando puede demostrar que nunca será ejercitable. La sugerencia conserva el significado y no constituye un aviso. En un diccionario exacto, el `mut` exterior cambia asociaciones y `[mut]` solo concede capacidad sobre valores `thing` materialmente asociados; nunca sobre claves, aliases, niveles anidados o el valor ausente. Un diccionario funcional prohíbe ambas formas de `mut`.

La mutabilidad exterior sí puede aplicarse a una colección de cualquier tipo:

```mud
action Record for mut observations: Num [*]
given value: Num {
    then add value to observations
}
```

Reglas booleanas y `look`, por ser puros, no admiten `mut` exterior. Ningún `given` admite mutabilidad exterior ni interior: su especificación de colección puede declarar cardinalidad, `unique` y `ordered`, pero su producción excluye `mut`.

Una referencia ordinaria a `World` designa la identidad exacta. `on World` y un rol `for World` seleccionan reflexivamente las `thing` concretas activas que satisfacen `is World`, incluida la propia `World` si es concreta. Esta selección solo se aplica cuando el tipo del rol es una `thing`.

La vinculación depende de la categoría del rol:

- una `thing` se vincula por identidad;
- un básico, alias, miembro de `family`, diccionario u otro valor inmutable se vincula por valor;
- un rol con `mut` exterior se vincula por identidad del lugar almacenado y conserva además su valor actual.

## Reglas

### Booleana

El cuerpo termina en una única expresión `Bool` y puede declarar antes vinculaciones locales inmutables:

```mud
rule IsAdult for person: Person {
    person.age >= 18
}

rule CanAfford for person: Person given price: Money {
    available := person.money
    available >= price
}
```

No lleva `if`.

### Reactiva

```mud
rule OpenGate on gate: Gate [mut] {
    when gate.unlocked
    if not gate.open
    then gate.open = true
}
```

`changes` es un sufijo temporal de expresiones:

```mud
when position + offset changes

when {
    calendar.day changes or
        alarm.enabled
}
```

En cambio, comenzar la segunda línea con `or` es inválido:

```mud
when {
    calendar.day changes
    or alarm.enabled
}
```

El salto posterior a `changes` termina una expresión completa; las llaves no suprimen terminadores y el `or` queda sin operando izquierdo. Para colocar el operador al principio de la segunda línea habría que mantener abierta la expresión con paréntesis.

Tiene menos precedencia que la aritmética, las conversiones y las comparaciones, pero más que `and` y `or`. Por tanto:

```text
position + offset changes  ≡  (position + offset) changes
temperature > limit changes  ≡  (temperature > limit) changes
position changes or ready  ≡  (position changes) or ready
```

Dentro de `when`, cada `e changes` produce un activador temporal que pulsa cuando `e` tiene valores distintos en las dos instantáneas de inicio consecutivas. Los operandos booleanos ordinarios de `and` y `or` se elevan a su transición `false` → `true`; así pueden combinarse cambios y condiciones que pasan a ser verdaderas sin perder pulsos consecutivos. Solo las palabras `and` y `or` componen activadores temporales; sus variantes simbólicas y los demás operadores lógicos conservan su significado ordinario sobre valores.

Un `when e` puramente booleano detecta la transición `false` → `true` de la expresión completa. `old e` puede aparecer en `when` y en `if` de una regla reactiva cuando `e` es pura y evaluable en ambas instantáneas; lee la anterior. No se admite en su `then`. Para medir una variación se escribe una condición explícita, por ejemplo `position - old position >= 10 meters`; no existe `changes by`.

```mud
when position changes and velocity changes

when price changes or outOfStock
if price > old price and stock < old stock

when position - old position >= 10 meters
```


`when` admite además fuentes declarativas. Una ocurrencia de `message`, el disparo efectivo de una rule reactiva y la evaluación de una rule `always` para una vinculación pueden actuar como trigger. Actions, subactions, `look`, reglas booleanas y tests no son fuentes declarativas de trigger.

Una referencia declarativa usada como trigger no lleva paréntesis: `when Damaged`, `when Dragon.Damaged` o una local que contenga ese descriptor. Los receptores restringen sus bindings `on`; no convierten el trigger en una llamada ordinaria.

Un trigger produce cero o más matches causales. Cada match conserva bindings/testigos e identidades de ocurrencia. `and` realiza natural join de matches compatibles y, cuando no comparten bindings, producto cartesiano; `or` realiza unión. Dos ocurrencias causalmente distintas no se deduplican por compartir payload. El caso puramente booleano anterior es la elevación temporal que produce esos matches cuando aparece el flanco correspondiente.
Las vinculaciones presentes en la primera instantánea materializada por `start with` comparan `old` y el valor actual contra la misma instantánea: `changes` no pulsa. Las ramas booleanas elevadas conservan, en cambio, el anterior virtual falso y pueden disparar si ya son verdaderas. Toda vinculación nacida después toma su primera onda activa como línea base completa, sin disparar, y comienza a comparar en la siguiente.

### `always`

```mud
always rule ValidPopulation on kingdom: Kingdom {
    population := kingdom.population
    population >= 0 people
}
otherwise "Population cannot be negative: {population}"
```

El cuerpo contiene directamente la condición, sin `if`. El `otherwise` opcional se escribe después de la llave de cierre, pertenece a la regla completa y admite una expresión `Text`. El diagnóstico solo se evalúa si la condición es falsa, sobre el mismo estado tentativo y con las mismas vinculaciones que incumplieron la regla. Su valor pasa a ser la razón del resultado `failed`. Omitirlo es legal, pero produce un aviso y una razón predeterminada. Escribirlo dentro de las llaves es un error.

## Acciones

```mud
action Recruit for kingdom: Kingdom [mut]
given amount: Nat in 1..100 {
    if kingdom.treasury >= amount * recruitmentCost
    otherwise "The kingdom cannot afford {amount} recruits"
    then {
        kingdom.treasury -= amount * recruitmentCost
        kingdom.soldiers += amount
    }
    after kingdom.soldiers >= old kingdom.soldiers
    otherwise "Recruitment did not increase the army"
}
```

No existe una clasificación semántica de actions elementales frente a compuestas. Un `then` es una secuencia ordenada de consecuencias y puede mezclar vinculaciones locales `:=`, efectos directos, llamadas a `action` o `subaction` y recorridos `for each`. Una llamada interna se ejecuta en su posición textual sobre el delta privado de la resolución: observa los efectos anteriores visibles, incorpora sus propios efectos a la misma resolución y las sentencias posteriores los observan.

Una `action` puede ser raíz exterior. Una `subaction` nunca puede serlo, pero ambas son callables y pueden invocarse desde cualquier contexto semántico `then`, incluido el `then` de una rule reactiva o de un test cuando ese contexto lo permita. La llamada interna no abre una transacción ni una resolución raíz independiente.

Los `after` de todas las actions/subactions ejecutadas se comprueban contra el estado estable tentativo final de la resolución completa. Un `failed` anidado revierte toda la resolución; un `rejected` interno también la aborta y revierte, conservando la categoría `rejected`. El `otherwise` opcional de `if` o `after` explica el rechazo y el asociado al `then` explica el `failed` de la transición completa.

```mud
subaction RemoveMoney for account: Account [mut]
given amount: Money {
    then account.balance -= amount
}

action Transfer
for source: Account [mut], destination: Account [mut]
given amount: Money {
    then {
        source.RemoveMoney(amount)
        destination.AddMoney(amount)
    }
}
```

La capacidad exterior y el subtyping reflectivo son propiedades distintas: `subaction <: action`, pero ampliar un descriptor no convierte una alternativa `subaction` en raíz exterior segura.

## Frontera de salida

```mud
look RealmSummary for kingdom: Kingdom
given locale: Locale {
    name := kingdom~name
    population: Population := kingdom.population in people
}

message KingChanged on kingdom: Kingdom {
    when kingdom.king changes
    if kingdom.visible

    kingdomName := kingdom~name
    kingName: Text := kingdom.king~name
    time := kingdom.clock in second
    timeText := "{kingdom.clock}"
}
```

`look` es un callable puro. Puede consultarlo el host, otro módulo cuyo contrato lo haga visible y código MUD en contextos compatibles con lectura, incluido un `then`. Sus campos leen una única vista coherente heredada del llamador: estado estable desde el host, snapshot desde una rule y delta privado visible en el punto textual desde un `then`. Admite `for` y `given` y devuelve exactamente un valor del tipo anónimo formado por sus campos públicos.

Un `message` no se llama. Cada coincidencia de su `when` que supera `if` crea una ocurrencia causal con identidad, declaración, bindings `on` y vista de nacimiento. Esa misma ocurrencia puede alimentar triggers en la onda siguiente. Dentro de MUD su payload se proyecta sobre la vista causal; hacia el host se proyecta, tras commit, sobre el estado estable final. Un rollback cancela la entrega exterior.

La envoltura exterior mantiene separados los bindings `on` que identifican a los participantes y el payload público; no aplana ambos espacios de nombres. Las ocurrencias confirmadas conservan el orden causal entre ondas y, dentro de una misma onda, un orden técnico estable y reproducible que no introduce prioridad semántica entre ellas.

Un campo público cuyo valor directo es una magnitud que admite unidades debe seleccionar preferentemente su presentación con `in`. Omitirla es legal y usa la proyección canónica de unidades, pero produce un aviso por dejar implícita una decisión de la API. Una magnitud sin unidades publica directamente su representación numérica y no produce ese aviso. Una magnitud de punto directa publica su coordenada en la unidad elegida y no su `~format`; para publicar el formato se construye un campo `Text`.

## Cláusulas y llaves

`when`, `if`, `then` y `after` siempre pueden usar llaves. Pueden omitirlas cuando contienen un único elemento. Un `then` con más de un efecto y un `after` de test con más de una aserción deben usarlas.

```mud
if ready

if {
    available := player.money
    available >= price
}
otherwise "Available: {available}"
```

Las llaves no suprimen los terminadores entre elementos de un bloque.

### Valores locales en condiciones

Los bloques de reglas booleanas, `when`, `if`, reglas `always` y `after` de acciones pueden contener cero o más vinculaciones locales seguidas por exactamente una expresión final:

```mud
when {
    wasOpen := old door.open
    isOpen := door.open
    wasOpen != isOpen
}
```

Las vinculaciones usan `nombre [: Tipo] := expresión`, son puras, inmutables y secuenciales, y no admiten referencias adelantadas, ciclos, redeclaración ni sombreado. Se recalculan en cada evaluación de la cláusula y no almacenan estado entre ondas.

Su ámbito alcanza el `otherwise` asociado, pero no `then` ni otra cláusula. En un `when`, `changes` y `old` evalúan la expresión definitoria de una local en cada instantánea necesaria.

Una expresión sin estructura de declaración debe ser la última. Debe elaborar a `Bool`, salvo en `when`, donde debe elaborar a un activador admitido por su contrato temporal. Un bloque vacío, un bloque compuesto solo por locales o una segunda expresión no declarativa son inválidos.

El bloque `after` de un test conserva una o más aserciones. Puede comenzar con locales comunes, visibles en todas las aserciones y sus `otherwise`; después de la primera aserción no puede declararse otra local:

```mud
after {
    expected := before + amount
    kingdom.soldiers == expected
    kingdom.treasury >= 0
}
```

### Valores locales en `then`

Un bloque `then`, incluido el de una iteración, puede intercalar efectos con vinculaciones locales calculadas:

```mud
then {
    cost := amount * price
    remaining: Money := kingdom.money - cost
    kingdom.money -= cost
}
```

La forma `name [derived-value-shape] := value-expression` declara un valor local inmutable. La forma derivada admite `: Type`, `in domain` con colección opcional, o una colección sola. El tipo y la cardinalidad se infieren cuando existe una solución única; en otro caso deben escribirse. No admite `mut` exterior.

La expresión es pura y se evalúa una sola vez cuando la ejecución alcanza la declaración. Lee los efectos secuenciales anteriores del mismo delta privado y conserva su valor aunque instrucciones posteriores cambien sus dependencias.

El nombre solo está disponible desde su declaración hasta el final del bloque. Puede usarse en declaraciones posteriores, pero no antes de aparecer; no existen referencias adelantadas, ciclos, redeclaración ni sombreado. Cada iteración crea un ámbito nuevo. Un `then` debe conservar al menos un efecto o llamada: un bloque compuesto únicamente por valores locales es inválido.

## Llamadas

Los participantes ocupan el receptor; los `given`, los paréntesis:

```mud
army.IsDestroyed()
(attacker, defender).CanAttack()
(
    attacker = leftArmy,
    defender = rightArmy
).CanAttack()
```

Los receptores nombrados pueden reordenar roles si son exactos y exhaustivos.

Una expresión de colección ocupa una sola posición de receptor cuando el rol correspondiente es colectivo; no se descompone en varios roles. Si el rol declara `mut` exterior, esa expresión debe ser además un lugar mutable compatible.

Que un tipo pueda aparecer en `for` no obliga a tratar todos los argumentos de ese tipo como roles. `for` identifica los sujetos semánticos de la operación; `given`, sus parámetros auxiliares.

Los `given` tienen nombre obligatorio, son de solo lectura y pueden declarar un predeterminado estático cerrado:

```mud
given origin: Square = Capital,
      depth: Nat,
      exhaustive: Bool = false
```

Los argumentos pueden ser posicionales, nombrados o un prefijo posicional seguido por nombres. Después del primer argumento nombrado no puede aparecer uno posicional. Posicionalmente solo puede omitirse un sufijo completo con predeterminado; los nombres permiten omitir predeterminados intermedios y reordenar:

```mud
game.Search(Capital, 3)
game.Search(depth = 3)
game.Search(exhaustive = true, depth = 3)
```

La última forma es válida, pero el compilador sugiere escribir `depth` antes de `exhaustive` para seguir el orden de declaración. Un nombre no puede repetirse ni ser desconocido y todo `given` sin predeterminado debe quedar vinculado.

Los receptores multiparte completamente nombrados también pueden reordenar roles y reciben la misma sugerencia de orden canónico. Continúan siendo exactos, exhaustivos y no se mezclan con receptores posicionales.

## Efectos

La gramática reconoce:

```mud
target = value
target += amount
target -= amount
target *= factor
target /= divisor
target |= values
target &= values
target ^= uniqueValues
target --= values

add value to collection
remove value from collection

add mut morale: Nat to Army
remove morale from Army

create Declaration
destroy Declaration
```

La forma `remove name from Owner` se distingue de retirar un valor mediante resolución y tipos. En ambos casos el parser conserva la misma procedencia; el AST elaborado debe producir la variante correcta o un diagnóstico.

`|=`, `&=`, `^=` y `--=` conservan en el AST su clase de actualización. Exigen un destino exteriormente mutable y un resultado asignable. `^=` solo admite colecciones `unique`. Sobre colecciones, las actualizaciones homogéneas se consolidan por unión, intersección, paridad o suma de multiplicidades retiradas; mezclar clases distintas es conflicto salvo regla posterior expresa. Sobre `Text`, `|=` concatena y varias actualizaciones concurrentes requieren un orden total determinado.

## `for each`, progresiones, selección y cuantificadores

`for each` acepta cualquier fuente finita y enumerable: colecciones, diccionarios exactos, intervalos enumerables, dominios finitos enumerables y cualquier otro valor con enumeración canónica. Un intervalo no se convierte en colección por poder recorrerse.

```mud
for each person in kingdom.people if person.hungry:
    person.health -= 1

for each value in [0..100] by 5: {
    doubled := value * 2
    total += doubled
}
```

El `:` es obligatorio. Las llaves pertenecen al cuerpo posterior y no sustituyen el separador. El cuerpo puede comenzar en la misma línea o después de uno o más terminadores; esa separación física no cambia su estructura abstracta. El cuerpo breve debe ser un efecto o llamada a acción; el bloque comparte el contrato de `then`.

### Filtro de iteración

`by` precede a `if`. El filtro puede ser una expresión o un bloque de expresión con locales. Es puro y no estocástico. Con orden semántico se evalúa justo antes de cada iteración y observa efectos secuenciales anteriores; sin orden semántico todos los filtros leen la instantánea inicial y los deltas aceptados se consolidan simultáneamente. Un diccionario exacto puede vincular `(key, value)`.

### Progresión `by`

`by` recibe una diferencia firmada compatible y se evalúa una vez antes del recorrido runtime. Positivo ancla en el límite inferior y negativo en el superior. Un límite inicial abierto avanza una vez antes del primer candidato. La progresión termina antes del primer candidato exterior y no necesita alcanzar el extremo opuesto. Los extremos invertidos siguen produciendo `empty`.

```text
[1..8] by 2   -> 1, 3, 5, 7
[1..8] by -3  -> 8, 5, 2
(1..8] by 2   -> 3, 5, 7
[1..8) by -2  -> 6, 4, 2
```

Un paso runtime demostrablemente cero es error estático; si puede variar y finalmente vale cero, produce el fallo de evaluación `progression-step-zero`. En una acción real ese fallo termina como `failed` y rollback; en una expresión pura se propaga como fallo de evaluación y nunca se convierte en `false`. En un dominio escalonado cero siempre es error estático. La compatibilidad usa la operación de avance y conversiones implícitas exactas, no identidad nominal: `Nat` puede avanzar por `Int`, `Num` por diferencias exactas compatibles y las magnitudes por unidades compatibles. En una magnitud de punto el paso es una diferencia lineal.

`by` no es stride sobre colecciones arbitrarias. `ordered by ruta` conserva otra semántica.

### Pasos predeterminados y números

Una fuente con enumeración propia no necesita `by`. Cuando la enumeración depende de una progresión, `Nat` e `Int` usan por defecto `1` y `Money`, `0.01`; omitir `by` elige siempre esa diferencia positiva. Otros tipos de progresión exacta requieren paso explícito salvo sucesor canónico definido. `Num` admite paso exacto explícito y un intervalo general de `Num` sin paso es inválido. Los intervalos de `Rum` nunca admiten progresión `by`, ni en iteración ni en dominios escalonados; una colección explícita de valores `Rum` sí es enumerable sin `by`.

### Dominios escalonados

`interval by step` usa la misma progresión para definir pertenencia y el paso estático puede ser negativo. El signo puede cambiar los miembros, pero el orden no forma parte del tipo. `all` materializa en orden canónico; `Nat in [1..8] by -2 = all` produce `2, 4, 6, 8`. En intervalos discontinuos el paso se reinicia por segmento; positivo recorre segmentos de menor a mayor y negativo al revés. Un dominio cíclico de punto recorre como máximo un periodo fundamental.

### Selección y cuantificadores

Selección y `exists`, `forall`, `count`, `sum`, `min`, `max` aceptan `by` cuando la fuente define progresión y mantienen `:` aunque el cuerpo tenga llaves. El bloque contiene locales `:=` seguidas de una expresión final. Selección, `exists`, `forall` y `count` exigen contrato booleano; `sum`, valor agregable; `min`/`max`, valor ordenable.

Una selección produce una colección y por ello no consume directamente un dominio desnudo: si la fuente conceptual es un dominio `D`, debe escribirse `all D`. Los recorridos y cuantificadores que no producen una colección sí pueden consumir directamente un dominio finito enumerable.

```mud
selected := x in source by step: {
    threshold := limit
    x < threshold
}

sum x in source by step: {
    adjusted := x.amount - x.exempt
    adjusted
}
```

Una selección devuelve directamente las ocurrencias aceptadas y conserva multiplicidad, unicidad y orden demostrables. Su predicado sigue siendo puro y determinista.

### `take` e indexación

`take amount from source` conserva su semántica existente. Como produce una colección, un dominio `D` no puede aparecer desnudo como `source`: debe materializarse explícitamente como `all D`. Sobre una colección ordenada o una materialización con enumeración canónica toma el prefijo; sobre colección/diccionario no ordenado con elección real muestrea reproduciblemente sin reemplazo. La indexación posicional sigue exigiendo orden observable.

## Tipo superior `Any`

`Any` es el tipo superior abierto de los valores MUD del proyecto. Incluye básicos, valores incorporados como los miembros de `Prefix`, identidades `thing`, aliases, miembros de `family`, magnitudes, intervalos, colecciones, diccionarios, productos estructurales y descriptores first-class de declaraciones y tipos. Los nodos de AST no son valores MUD por el mero hecho de existir como representación del compilador.

`Any` no es enumerable, no posee orden total universal ni predeterminado. Son inválidos:

```mud
all Any
unknown: Any
```

Un campo almacenado `Any` debe escribir inicializador. La igualdad exige tipos efectivos compatibles y delega en la igualdad del tipo efectivo. Cualquier operación específica requiere narrowing:

```mud
rule Positive given value: Any {
    value is Nat and value > 0
}
```

Dentro de una rama funcional, `is` e `iis` conservan el narrowing en el resultado:

```mud
describeAny: Any --> Text [ordered] =
    value iis PersonId --> "Person id {value}",
    value is Nat --> "Natural {value}",
    _ --> "Other"
```

`Money` continúa siendo un básico incorporado por sus reglas de materialización, no una excepción a la apertura de `Any`.

## Valores contextuales

Las colecciones pueden escribirse entre corchetes. En posiciones donde una coma no compita con otra construcción, la forma contextual puede omitirlos:

```mud
[A, B, C]
```

Los corchetes son obligatorios para anidamiento y para usar la colección como un único argumento. `empty` necesita un tipo esperado; comparar `empty == empty` sin contexto es inválido.

Un diccionario con clave alias estructural admite:

```mud
board[(E, Four)]
board[E, Four]
```

## Intervalos

La forma concreta de un tipo de intervalo escribe primero el tipo de sus límites y después la palabra contextual `Interval`:

```mud
Nat Interval
Int Interval
Num Interval
Rum Interval
Money Interval
```

La gramática conserva cualquier `type-reference` en esa posición; la fase estática exige que resuelva a una representación numérica admitida. `Interval` no es una declaración nominal consultada mediante resolución de nombres en esta construcción.

Formas:

```mud
[a..b]
(a..b)
[a..b)
(a..b]
a..b
[a]
```

`a..b` equivale a `[a..b]`; `[a]`, a `[a..a]`. Un extremo `*` debe estar cerrado en su lado. La forma cíclica exclusiva de magnitudes de punto es un intervalo completo seguido por el modificador: `[a..b) cycle`.

Los extremos finitos son expresiones completas y deben elaborar al mismo tipo ordenado. En un intervalo de magnitud pueden llevar unidades locales, incluso distintas, que se normalizan antes de comparar:

```mud
[1 m..5 km]
[minimumDistance..5 m]
[1 km..maximumDistance]
[minimumDistance..maximumDistance]
```

Un literal situado junto a un campo de magnitud debe llevar su propia unidad. Por tanto, `[minimumDistance..5] m` es inválido y se escribe `[minimumDistance..5 m]`.

Cuando todos los extremos finitos son literales numéricos sin unidad, una sola unidad puede seguir al intervalo:

```mud
[1..5] m
1..5 m
[1..5) km
[*..5] m
[1] m
[] m
```

`1..5 m` se agrupa como `(1..5) m`. La unidad exterior no se distribuye sobre campos ni sobre cantidades que ya tengan unidad. `[1..5 m]` es inválido porque enfrenta `Num` con una magnitud, y `[1 m..5 m] m` añade una segunda unidad exterior inválida.

La serialización canónica de literales que comparten unidad usa `[1..5] m`, aunque `[1 m..5 m]` también es válida. Si las unidades difieren o un extremo es una expresión ya tipada, se usan unidades locales.

Después de evaluar y normalizar los extremos efectivos de un intervalo lineal:

- un límite inferior menor que el superior conserva los lados escritos;
- dos límites iguales forman un unitario solo si ambos lados son cerrados y producen `empty` en otro caso;
- un límite inferior mayor que el superior produce `empty`.

La inversión no implica recorrido descendente ni ciclo. Construir ese intervalo vacío no falla una resolución por sí mismo; solo producen `failed` las restricciones que vuelvan inválido el estado tentativo, como un valor almacenado que quede fuera de su dominio o una regla `always` incumplida. Un `given` fuera de dominio y un `if` o `after` falsos conservan su resultado `rejected`.

Los dominios declarados en la cabecera de una magnitud conservan los límites numéricos desnudos interpretados en su representación canónica: en la unidad raíz cuando existe y directamente en la representación numérica cuando no hay unidades. La forma `[a..b) cycle` también conserva esa restricción y exige un periodo estrictamente positivo. Otros lados, infinitos o intervalos vacíos son inválidos con `cycle`.

## Precedencia y agrupación

De mayor a menor:

| Nivel | Formas | Agrupación |
| ---: | --- | --- |
| 1 | acceso `.`, metadato `~`, índice `[]`, llamada `()` y `unit from container in point` | izquierda o forma completa |
| 2 | prefijos `old`, `allowed`, `not`, signo | derecha |
| 3 | `*`, `/`, `%` | izquierda |
| 4 | `+`, `-`, `--` | izquierda |
| 5 | sufijos `to Type`, `in unit` | acumulativa |
| 6 | `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `is not`, `iis`, `iis not`, `in`, `not in` | restringida |
| 7 | sufijo temporal `changes` | no asociativa |
| 8 | `and`, `&` | izquierda |
| 9 | `or`, `|` | izquierda |
| 10 | `xor`, `^` | izquierda |
| 11 | `=>` | derecha |
| 12 | `<=>` | cadena adyacente |
| 13 | `eventually ... through ...` | exterior |

Las formas `take amount from source`, `binding in source: predicate` y los cuantificadores contienen expresiones completas en sus posiciones delimitadas. El primer `from` no anidado que puede cerrar la cantidad de `take` separa cantidad y fuente; los dos puntos no anidados separan fuente y predicado. Los `from` o `:` encerrados entre paréntesis o dentro de otra construcción completa pertenecen a esa construcción. Esta regla de delimitación contextual evita que el `from` de extracción de componentes absorba accidentalmente el separador de `take`. Por ello:

```mud
take n from player in players: player.ready
```

se agrupa como `take n from (player in players: player.ready)` sin paréntesis.

`to` y el `in` de unidad transforman el valor completo acumulado a su izquierda. El parser continúa después con el resultado:

```mud
population / regions to Population
distance + offset in km
value to A to B
```

se agrupan:

```text
(population / regions) to Population
(distance + offset) in km
(value to A) to B
```

Si aparece después otro operador, usa el resultado ya convertido. Esta regla se implementa naturalmente con un parser Pratt que permita un postfix de menor precedencia seguido de operadores nuevos.

`in` de unidad consume la expresión de unidad completa, incluidos productos, cocientes y paréntesis:

```mud
speed in km/h
acceleration in m/(s*s)
```

Como `to` pertenece a cada operando cuantitativo antes de comparar, `3 m == 3 m to Length` se agrupa como `3 m == (3 m to Length)`, no como una conversión del resultado booleano.

## Encadenamientos

Las cadenas homogéneas de orden:

```mud
a < b < c
```

se elaboran como:

```mud
a < b and b < c
```

La igualdad encadenada usa la misma regla. `<=>` produce conjunciones de pares adyacentes. No se encadenan:

- `!=`
- `is` e `is not`
- `iis` e `iis not`
- pertenencia `in` y `not in`
- `=>`

No se mezclan operadores distintos dentro de una misma cadena sin conjunciones explícitas.

`iis` comprueba el tipo nominal efectivo exacto; `is` incluye especializaciones. Para:

```mud
alias Identifier := Nat
alias PersonId as Identifier
alias EmployeeId as PersonId
```

un `EmployeeId` satisface `value is PersonId`, pero no `value iis PersonId`. `value iis not PersonId` elimina únicamente la posibilidad exacta `PersonId` durante el narrowing. El operando derecho de `iis` debe ser un tipo nominal; productos, diccionarios y la identidad singleton `Madrid` son inválidos.

Sobre `MudPath`, `p in q` es reflexivo y compara segmentos completos:

```mud
world.combat in world.combat          # true
world.combat.melee in world.combat    # true
world.combatant in world.combat       # false
```

## Metadatos postfix

El acceso se escribe `owner~metadata`, nunca `owner.~metadata`. Todo acceso `~` es runtime-readonly; la escritura solo existe como declaración del modelo dentro del preámbulo metadata-bearing correspondiente.

| Metadato | Tipo | Propietarios principales | Declarable |
| --- | --- | --- | --- |
| `~identifier` | `Name` | elementos anclados | no, intrínseco |
| `~name` | `Name` | elementos metadata-bearing compatibles | sí |
| `~path` | `MudPath` | declaraciones y elementos anclados | no, intrínseco |
| `~anchor` | `Anchor` | declaraciones y elementos anclados | no, intrínseco |
| `~file` | `MudFile` | elementos con procedencia física | no, intrínseco |
| `~kind` | familia reflectiva según receptor | declaraciones y descriptores compatibles | no, intrínseco |
| `~type` | `Type` | todo valor MUD | no, intrínseco |
| `~metadata` | `Metadata [* unique]` | elementos metadata-bearing | no, intrínseco |
| `~for` | `Participant [* unique ordered]` | regla booleana, `action`, `subaction`, `look` | no, intrínseco |
| `~on` | `Participant [* unique ordered]` | regla reactiva, regla `always`, `message` | no, intrínseco |
| `~given` | `Participant [* unique ordered]` | regla booleana, `action`, `subaction`, `look` | no, intrínseco |
| `~clauses` | `ClauseKind [* unique]` | declaraciones con cláusulas | no, intrínseco |
| `~plural` | `Text` | unidades | sí |
| `~abbreviation` | `Text` | unidades | sí |
| `~prefixes` | `Prefix [* unique]` | unidades | sí; default `empty` |
| `~format` | `Text` | magnitudes de punto | sí |
| `~summary` | `Text` | elementos metadata-bearing compatibles | sí; default `""` |
| `~description` | `Text` | elementos metadata-bearing compatibles | sí; default `""` |
| `~deprecated` | `Text [0..1]` | elementos metadata-bearing compatibles | sí; default `empty` |

La columna «Propietarios» es una restricción semántica de disponibilidad, no una descripción de cuándo el resultado es no vacío. Tras resolver y tipar el receptor, un acceso a una propiedad no soportada por su categoría estática es error. En particular, `thing A` hace inválido `A~for`; una `action` sí soporta `~for` aunque omita la cláusula y en ese caso obtiene `empty`. La misma separación entre propiedad inexistente y valor vacío se aplica a `~on` y `~given`.

La producción `metadata-name ::= identifier | "for" | "on" | "given"` solo permite que esas keywords duras aparezcan sintácticamente después de `~`. El parser no puede decidir por el nombre textual del receptor si el acceso existe: construye la forma postfix y la resolución y el tipado aplican la matriz anterior.

La tabla resume las propiedades comunes y configurables que afectan a la sintaxis de este capítulo. El sistema reflectivo define además las propiedades específicas de cada descriptor, como relaciones de especialización, campos, componentes y propiedades estructurales de colecciones y diccionarios; no se duplican aquí como un segundo catálogo normativo.

`Prefix` es un tipo incorporado. Sus valores SI se escriben como identificadores ordinarios (`kilo`, `milli`, ...), por lo que `~prefixes = [kilo, milli]` no necesita gramática especial.

Las conversiones generales son explícitas cuando existen:

```mud
pathText: Text = Alexandria~path to Text
```

Las plantillas pueden renderizar los tipos de metadatos directamente sin crear compatibilidad nominal general con `Text`. `~file` es válido en cualquier expresión, pero produce advertencia cuando escapa de texto o de una salida pública meramente informativa y su valor puede alterar el comportamiento:

```mud
look SourceInfo {
    source := "Loaded from {Alexandria~file}"
}

rule Fragile given expected: MudFile {
    Alexandria~file == expected # válido con advertencia
}
```

`~name` y cualquier otro metadato configurable se cambian editando el modelo y reelaborándolo; nunca mediante un efecto runtime. Esta edición no cambia payload, igualdad, path ni ancla salvo que se modifique el identificador fuente por otro mecanismo.

## `Text` y operadores

`|` concatena `Text`:

```mud
"Hello, " | name
```

No se admiten `&`, `^` ni `-` sobre `Text`. `xor` es exclusivamente lógico y `^` exclusivamente conjuntista. Los aliases nominales de `Text` no adquieren concatenación implícita.

Todo literal `Text`, ordinario o multilínea, es una plantilla. `{e}` evalúa `e` e inserta la representación textual canónica del valor. Los metadatos son expresiones ordinarias:

```mud
"Kingdom: {kingdom}"
"Population: {kingdom.population:6}"
"Rule: {CanRecruit~anchor}"
"Path: {CanRecruit~path}"
"Literal braces: \{example\}"
```

`anchor{...}` no pertenece al lenguaje. Renderizar `Name`, `MudPath`, `Anchor` o `MudFile` en una plantilla no los convierte implícitamente a `Text` fuera de ese contexto.

Son renderizables directamente `Text`, `Char`, `Bool`, los números básicos, los valores `thing`, los miembros de `family`, los intervalos, las colecciones y las magnitudes. Una llamada a regla booleana también lo es porque produce `Bool`. Los descriptores de declaraciones y tipos son valores MUD first-class, pero esa condición no les concede una representación textual implícita. Actions, reglas reactivas, reglas `always`, `look`, `message`, tests, tipos y declaraciones `family` producen error estático dentro de `{...}` mientras no exista una conversión o proyección textual explícita aplicable.

Una `thing`, un alias nominal y un miembro de `family` se representan mediante su `~name` efectivo. Su ancla canónica se obtiene mediante `~anchor`; modificar `~name` no cambia igualdad, path ni ancla. Un miembro de `family` sin sobrescritura usa inicialmente su nombre nominal. Un intervalo usa su forma canónica normalizada. Una colección omite solo sus corchetes exteriores y separa elementos mediante `, `; toda colección que aparezca como elemento conserva sus propios corchetes:

```mud
"{[1, 2, 3]}"          # 1, 2, 3
"{[[1, 2], [3, 4]]}"   # [1, 2], [3, 4]
```

Un hueco numérico admite `{e:izquierda}`, `{e::derecha}` y `{e:izquierda:derecha}`. La precisión izquierda es el mínimo de cifras anteriores al punto y rellena con ceros sin contar el signo ni truncar. La derecha fija exactamente las cifras posteriores, añade ceros o redondea al más cercano con empates al par:

```mud
"{count:4}"     # 0012
"{ratio::2}"    # 12.30
"{ratio:4:2}"   # 0012.30
```

La precisión izquierda se admite para todos los tipos numéricos básicos. La derecha se admite para los tipos que pueden mostrar parte fraccionaria: `Num`, `Rum` y `Money`. Cualquier formato numérico sobre otro tipo es un error estático.

Una magnitud lineal sin `in` representa el número seguido por la proyección canónica de unidades de su dimensión. Si esa proyección es vacía, representa únicamente el número. Los factores nominales sin unidad no se imprimen, pero permanecen en el tipo. Una magnitud de punto usa su `~format` si lo tiene y, si no, sigue la regla ordinaria de su magnitud subyacente. `{magnitude in unit}` selecciona una presentación disponible y, para un punto, evita el `~format` y representa la coordenada completa. Es inválido aplicar `in` a una magnitud base sin unidades. Cuando hay unidad, se escribe su abreviatura si existe; en otro caso, el nombre singular para `1` y `-1`, y el plural para los demás valores.

`time in picosecond` expresa la coordenada total; `picosecond from second in time` extrae la parte dentro del segundo. La segunda forma es válida aunque el formato visible no incluya picosegundos.

## `eventually`, `allowed` y azar

```mud
allowed game.Move(origin, destination)

eventually game.Checkmate(White)
    through game.Move, game.Pass

eventually game.Checkmate(White)
    through [game.Move, game.Pass]

Rand([1..6])
```

Las entradas de `through` son referencias a acciones, no llamadas concretas. La lista con o sin corchetes representa la misma colección contextual. MUD 1.0 solo admite `Rand(source)`; no introduce todavía sintaxis de pesos o distribuciones.

## Terminadores y prefijos abiertos

`TERMINATOR` procede de `;` o de `NEWLINE`. Un salto continúa cuando aparece:

1. Dentro de `()` o `[]`.
2. Después de `,`.
3. Después de un operador binario o asignación incompletos.
4. Después de `:`, `:=`, `->`, `-->`, `.` o `~` cuando falta su operando o miembro.
5. Después de `using`, `as`, `for`, `on`, `given`, `when`, `if`, `then`, `after`, `otherwise`, `to`, `in`, `through`, `by`, `from`, `over`, `root` o `point` cuando la producción exige contenido.
6. Dentro de una cabecera que, según la EBNF, no puede terminar todavía.
7. Dentro de un literal o comentario multilínea.

Un salto después de una unidad ya completa termina esa unidad. La sangría nunca decide.

> [!example]
> En `value = first` el salto termina la asignación. En `value = first +` no la termina porque falta el operando derecho.

## Distinciones contextuales

El parser o la elaboración posterior deben resolver sin elección arbitraria:

| Superficie | Distinción |
| --- | --- |
| `in` | dominio, participante relacionado, pertenencia o unidad |
| `call()` | regla booleana o acción |
| `remove x from y` | valor de colección o propiedad dinámica |
| `UNIT_FORM` | unidad habilitada o nombre inválido |
| operadores compartidos | operación lógica, aritmética, textual o conjuntista |
| literal estructural | alias esperado |
| `[expression]` | colección unitaria o intervalo unitario |
| `1..5 unit` | unidad común del intervalo o extremo derecho de una derivación inválida |

Si nombres, tipos y restricciones de la expresión no determinan una única interpretación válida, el programa es inválido y debe aportar el tipo que falte. No se aplica una preferencia implícita. Por ejemplo, una derivación sin contexto suficiente no puede elegir arbitrariamente si `[3]` es una colección o el intervalo `[3..3]`. La gramática fija expresamente `1..5 m` como la forma de unidad común `(1..5) m`; no queda a elección del parser.

## Recuperación de errores

Una implementación puede sincronizar después de un error en:

- `TERMINATOR`
- `}`
- Inicio inequívoco de una declaración superior

La recuperación solo mejora diagnósticos. No puede insertar silenciosamente semántica ni aceptar una forma fuera de la gramática.

## Construcciones contextuales conservadas

El parser no decide cuestiones que requieren resolución:

- Si un camino con puntos atraviesa paths de MUD, declaraciones o miembros.
- Si un literal estructural usado antes de una llamada representa un receptor único o varios receptores.
- Si un `postfix-expression` de un efecto es una llamada de acción.
- Qué tipo contextual selecciona un literal estructural, de unidad, de punto o textual de un único escalar.

La CST conserva la forma concreta y el AST superficial una forma no resuelta. Las fases posteriores realizan la clasificación.

## Representación de magnitudes

La anotación opcional de una magnitud usa la sintaxis general `declared-type`. Una regla estática posterior exige que el tipo resuelto sea una representación numérica permitida. La gramática no mantiene una lista cerrada duplicada de tipos numéricos.

## Cuerpos vacíos omitidos

El cuerpo de una `thing` es opcional. Estas formas producen el mismo AST e IR, aunque la CST conserva la escritura:

```mud
thing A
thing A {}
thing A;
abstract thing Root
thing B as Root
```

El punto y coma no añade una regla nueva: ya es un `TERMINATOR` explícito y permite, por ejemplo, `thing A; thing B; thing C as A`.

## Acceso nominal a miembros de alias

Los componentes y campos derivados pertenecen al tipo nominal del alias. Una estructura desnuda no adquiere miembros por coincidencia de forma:

```mud
(1, 2).derived                    # inválido
((1, 2) to CosoAlias).derived     # válido
```

El contexto de tipo también puede construir el alias sin `to`. El compilador no busca aliases candidatos a partir del nombre del miembro.

## Metadatos reflectivos

Los `~...` configurables preceden al contenido ordinario. Campos, componentes y participantes pueden llevar un bloque inmediato metadata-only. Todo `for`, `on` y `given` tiene nombre obligatorio; una cabecera agrupada comparte tipo y metadata-body entre sus identificadores. Los defaults de archivo preceden a `using`. `start with` y los cuerpos de `when`/`if`/`then`/`after`/`otherwise` no son propietarios metadata-bearing.


### Metadata de usuario llamada `private`

`private` no es un metadato estándar ni controla visibilidad. Como `metadata-name` admite identificadores ordinarios, `~private` puede declararse y consultarse como metadata de usuario cuando el propietario admita metadata configurable. Se comporta como cualquier otra metadata de extensión y no recibe tratamiento especial.
