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
  - Q-054
  - Q-059
decisions:
  - D-025
  - D-027
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
---

# 07. Gramática concreta

## Estado y propósito

[[gramatica/mud.ebnf]] define la sintaxis completa de MUD 1.0. Este capítulo fija cómo leerla, cómo resolver las construcciones contextuales y cómo agrupar expresiones. Las cuestiones listadas en el frontmatter afectan semántica posterior, no impiden reconocer la forma fuente.

## Producto del parsing

El resultado normativo del parsing es una CST sin pérdidas por archivo, definida en [[sintaxis/cst-sin-perdidas]]. La EBNF determina agrupación y orden de tokens significativos; la CST conserva además puntuación, terminadores y trivia.

La existencia de una CST no afirma que el archivo sea válido. La recuperación puede representar tokens ausentes o inesperados sin descartarlos.

## Validación anterior al AST

Después de construir la CST se comprueban restricciones sintácticas contextuales necesarias para producir un AST normalizado, entre ellas:

- Modificadores de colección duplicados.
- Propiedades de unidad duplicadas o requeridas ausentes.
- Un argumento posicional posterior a uno nombrado.
- Combinaciones concretas prohibidas por este capítulo.

La resolución de nombres, tipos, dominios y efectos no pertenece a esta validación.

## Transformación abstracta

La proyección a AST está en [[sintaxis/cst-a-ast-superficial]]. Las producciones se cubren mecánicamente en `sintaxis/cobertura-sintactica.yaml`.

## Programa

Un archivo contiene una cabecera de declaraciones `using` seguida por las declaraciones de primer nivel:

```mud
using world.people
using physics.*
```

No existe una declaración `namespace`; se deriva de la ruta. `using`, no `import`, es la única construcción de visibilidad entre namespaces.

Todos los `using` deben aparecer antes de la primera declaración de primer nivel. Intercalarlos es un error y nunca crea alcance local o secuencial. El orden entre varios `using` no decide ambigüedades.

Las categorías de primer nivel son:

- `thing`
- `alias`
- `family`
- `magnitude`
- Las tres formas de `rule`
- `action`
- `look`
- `message`
- `test`
- `start with

## `thing`

```mud
thing World {}

abstract thing Place {}

thing Alexandria as City, Place {
    name = "Alejandría"
}
```

`Thing` es la `thing` abstracta incorporada que actúa como tipo superior. Toda `thing` satisface `is Thing`. Una raíz sin `as` conserva cero antecesoras declaradas, pero recibe una arista semántica implícita hacia `Thing`. Es válido escribir `as Thing`, pero es redundante: una implementación conforme debe emitir un diagnóstico no bloqueante y ofrecer eliminarlo. `Thing` no puede declararse, crearse ni destruirse.

Toda `thing` expone la propiedad intrínseca e inmutable `name: Text`. Su valor predeterminado es su nombre nominal no cualificado. Puede sobrescribirse una sola vez con `name =` y un literal `Text` sin interpolaciones, como en `Alexandria`. No es un campo almacenado o calculado, no ocupa el store y no se hereda: una descendiente sin sobrescritura usa siempre su propio nombre nominal.

La lista posterior a `as` no expresa prioridad. `create` no acepta aquí ni en ningún otro lugar un cuerpo:

```mud
create Alexandria
destroy Alexandria
```

## Campos

Forma almacenada:

```text
[mut] fieldName: Type [in domain] [collection-specification] [= static-expression]
```

Forma calculada:

```text
fieldName [: Type] := expression
```

La anotación de tipo es opcional. Si se omite, el tipo debe poder inferirse unívocamente de la expresión, sin prioridades predeterminadas entre representaciones o formas contextuales compatibles. Si hay más de una solución, el tipo debe escribirse. Un campo calculado no admite `mut`, dominio ni especificación de colección adicionales.

El `mut` exterior se escribe antes del nombre porque califica el lugar almacenado, no el tipo de sus miembros. `fieldName: mut Type` no pertenece a la sintaxis. El identificador `name` está ocupado por la propiedad intrínseca dentro de una `thing` y no puede redeclararse mediante ninguna de estas formas.

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

## Colecciones y diccionarios

La cardinalidad, cuando aparece, ocupa el inicio de los corchetes. Los modificadores pueden separarse por espacio o por coma:

```mud
citizens: Person [0..* unique ordered mut]
citizens: Person [0..*, unique, ordered, mut]
```

No se permite coma final. La omisión de cardinalidad equivale a `[1]`.

Las colecciones compatibles admiten `|`, `&`, `-` y `^`. Operan sobre multiplicidades, no concatenan:

```mud
leftChars: Char [1..5] = ["a"]
rightChars: Char [0..2] = empty
combinedChars := leftChars | rightChars # Char [1..7]
```

`unique`, `ordered` y el `mut` interior se propagan con la misma regla: unión y diferencia simétrica los conservan solo si aparecen en ambos operandos; intersección, si aparecen en cualquiera; diferencia, si aparecen en el izquierdo. El `mut` exterior nunca se infiere para un resultado calculado.

Un resultado con orden canónico se normaliza por ese orden. Con orden de inserción, se conserva estable el orden izquierdo y se incorporan después las ocurrencias adicionales derechas cuando la operación lo requiere.

`unique` se prohíbe estáticamente en diccionarios: sus claves ya son únicas y el modificador no se reinterpreta como unicidad de valores.

```mud
board: Square -> Piece [0..32 ordered]
nested: Name -> (Coordinate -> Piece [*]) [*]
```

Los paréntesis son obligatorios para anidar un diccionario como valor.

`ordered by ruta` pertenece a colecciones cuyos miembros ofrecen una ruta estable de campos, componentes o datos asociados. Cada acceso intermedio debe ser singular y el valor final debe poseer orden semántico total:

```mud
route: Terrain [* ordered by movementCost]
teams: Team [* ordered by captain.age]
```

Una `thing` no posee por sí misma orden total y no puede ser la clave final. Toda la ruta debe ser transitivamente estable: se rechazan campos almacenados mutables, cálculos con dependencias mutables y accesos intermedios cuyo estado posterior pueda alterar la clave. Una ruta opcional también se rechaza mientras no exista una posición definida para `empty`.

`ordered by` no admite expresiones arbitrarias. Si el criterio necesita una fórmula, se declara como campo o dato calculado y se ordena por su nombre. Las claves iguales conservan el orden relativo de inserción; no se desempatan por ancla, identidad ni orden de declaración de una `family`.

Se prohíbe `ordered by` para `Char`; su orden es Unicode. `Text` no acepta especificaciones de colección.

## Aliases

```mud
alias PlayerName := Text

alias Board := Square -> Piece [0..32 ordered]

alias Square {
    file: File
    rank: Rank
}

alias Pagination {
    page: Nat = 1
    size: Nat = 20
}
```

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

Un componente no admite `mut` exterior porque el valor de alias y cada uno de sus componentes son inmutables. Sí puede escribir `[mut]` en su especificación de colección para conceder capacidad interior sobre las `thing` contenidas directamente; esa capacidad no permite reemplazar la colección ni atraviesa aliases o contenedores anidados de manera implícita.

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

Los datos aparecen antes del primer miembro y pueden ser almacenados o calculados mediante `nombre [: Tipo] := expresión`. El tipo calculado es opcional si se puede inferir de forma unívoca. Su expresión se evalúa estáticamente para cada miembro después de resolver los datos almacenados, puede consultar otros datos asociados mediante nombres no cualificados y debe tener dependencias acíclicas. El bloque de un miembro solo puede asignar datos almacenados.

Los miembros se separan por comas y no admiten coma final. `ordered family` hace comparables sus miembros en orden de declaración y permite usar rutas de datos asociados, incluidos los calculados estables, como claves de `ordered by` en colecciones.

## Magnitudes

Magnitud base:

```mud
magnitude Probability: Num in [0..1] {}
```

Magnitud derivada:

```mud
magnitude Speed: Num in [0..*] := Length / Time {
    unit := 1 m/s {
        name = "fastie"
        plural = "fasties"
        abbreviation = "fst"
    }
}
```

Magnitud de punto:

```mud
magnitude RawInstant point over Time {}

magnitude Timestamp point over Time {
    format = "{day}:{hour:2}:{minute:2}"
}

magnitude WorkdayTime point over Time in [0..28_800] {
    format = "{hour:2}:{minute:2}"
}

magnitude TimeOfDay point over Time in [0..86_400 cycle) {
    format = "{hour:2}:{minute:2}:{second:2}"
}
```

Una magnitud base puede tener una `root unit`; una derivada solo unidades nominales alternativas; una magnitud de punto no declara unidades. En esta última, `in` y el dominio son opcionales: sin ellos se usa el dominio completo de la coordenada subyacente, un intervalo ordinario la acota sin envolver y `[a..b cycle)` añade normalización cíclica. Solo una magnitud de punto admite `cycle`.

En una unidad, omitir la propiedad `prefixes` habilita todos los prefijos del catálogo incorporado. `prefixes = empty` no habilita ninguno y `prefixes = [p1, p2, ...]` selecciona únicamente los enumerados. No existe una forma desnuda `prefixes`.

`format` es opcional y usa la sintaxis general de plantilla `Text`: los huecos son código y `:2` fija aquí dos posiciones a la izquierda del punto. Sin él no existe una representación especial de punto: se aplica exactamente la representación textual ordinaria de una magnitud, con la coordenada en la unidad raíz y la abreviatura o nombre de esa unidad. Con él, el primer componente es la coordenada en esa unidad —reducida por el ciclo, si existe— y cada componente siguiente se extrae dentro del anterior. Un contenedor no obvio se hace explícito, por ejemplo `format = "{week from year:2}"`.

Fuera de `format`, la extracción exige el punto:

```mud
minute from hour in time
picosecond from second in time
week from year in date
```

La forma es una sola construcción sintáctica. El receptor debe ser una magnitud de punto; ambas unidades pertenecen a su magnitud subyacente; la unidad extraída no supera a la contenedora; el resultado es `Nat`. Se usa el origen canónico y el resto euclídeo, con un posible último componente parcial cuando las unidades no dividen exactamente. La extracción no depende del `format`.

Las formas producidas por `format` ocupan el token contextual `POINT_LITERAL`. El tipo esperado selecciona una única magnitud de punto y el literal debe reproducir exactamente su forma canónica. Un formato que no pueda invertirse unívocamente es inválido. Los componentes más finos que el último representado toman valor cero.

Sin `format`, el literal se escribe como una cantidad ordinaria con unidad compatible. Todo literal debe pertenecer al dominio antes de aplicar normalización cíclica; por ejemplo, `26:00:00` es inválido para `TimeOfDay`.

## Participantes

`for` vincula roles suministrados de cualquier tipo de valor declarado. Un rol puede ser individual o colectivo, restringir sus valores mediante `in dominio` y admitir la especificación completa de colección. El dominio se escribe después del tipo y antes de la colección. `on` construye vinculaciones automáticas exclusivamente individuales cuyo tipo debe ser una `thing`.

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
    then ...
}
```

Todos los nombres de una cabecera `on` son visibles en la cabecera completa. Sus tipos y restricciones se resuelven conjuntamente, de modo que se admiten referencias adelantadas y ciclos cuando existe una solución nominal única. Cada rol parte de las `thing` concretas y activas de su tipo efectivo; las vinculaciones son el join finito que satisface todas las pertenencias sobre una misma instantánea. No se impone que roles distintos reciban identidades distintas y dos orientaciones simétricas constituyen vinculaciones diferentes.

El nombre de un participante puede omitirse cuando su cardinalidad efectiva es exactamente `[1]` y no declara mutabilidad exterior:

```mud
rule IsDestroyed for Army {
    soldiers == 0
}
```

La omisión es válida solo si cada acceso no cualificado se resuelve unívocamente. Un rol `for` con cardinalidad distinta de `[1]` debe tener nombre, porque los accesos a miembros de una colección requieren cuantificación, agregación o iteración explícitas. Los nombres de `given` nunca se omiten.

En una action, `mut` antes del nombre de cualquier rol `for`, incluida la cardinalidad `[1]`, concede mutabilidad exterior sobre la colección suministrada. El receptor correspondiente debe ser un lugar almacenado con esa capacidad; un literal o una colección calculada no satisfacen el contrato. El `mut` de la especificación de colección continúa concediendo capacidad interior sobre las `thing` miembro:

```mud
action Treat for
    mut patients: Person [1..10, unique, mut]
{
    then for each patient in patients {
        patient.health += 10
    }
}
```

La declaración anterior puede cambiar la membresía u orden de la colección almacenada recibida y modificar sus miembros. `mut patients: Person [*]` concede solo la primera capacidad; `patients: Person [*, mut]`, solo la segunda.

Escribir capacidad interior sobre valores inmutables es legal, pero el compilador sugiere retirarla cuando puede demostrar que nunca será ejercitable. La sugerencia conserva el significado y no constituye un aviso. En diccionarios, el `mut` exterior cambia asociaciones y `[mut]` solo concede capacidad sobre valores `thing` materialmente asociados; nunca sobre claves, aliases, niveles anidados o el predeterminado leído para una clave ausente.

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
    calendar.day changes
    or alarm.enabled
}
```

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

Las vinculaciones presentes en la primera instantánea materializada por `start with` comparan `old` y el valor actual contra la misma instantánea: `changes` no pulsa. Las ramas booleanas elevadas conservan, en cambio, el anterior virtual falso y pueden disparar si ya son verdaderas. Toda vinculación nacida después toma su primera onda activa como línea base completa, sin disparar, y comienza a comparar en la siguiente.

### `always`

```mud
always rule ValidPopulation on kingdom: Kingdom {
    population := kingdom.population
    population >= 0 people
    otherwise "Population cannot be negative: {population}"
}
```

El cuerpo contiene directamente la condición, sin `if`, y puede añadir `otherwise` con una expresión `Text`. El diagnóstico solo se evalúa si la condición es falsa, sobre el mismo estado tentativo y con las mismas vinculaciones que incumplieron la regla. Su valor pasa a ser la razón del resultado `failed`. Omitirlo es legal, pero produce un aviso y una razón predeterminada.

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

`then` contiene efectos o llamadas a acciones conforme a la distinción estática entre acciones elementales y compuestas. El `otherwise` opcional de `if` o `after` explica un `rejected`; omitirlo produce una sugerencia y una razón generada. No captura errores de evaluación ni envuelve resultados.

## Frontera de salida

```mud
look RealmSummary for kingdom: Kingdom {
    name := kingdom.name
    population: Population := kingdom.population in people
}

message KingChanged on kingdom: Kingdom {
    when kingdom.king changes
    if kingdom.visible

    kingdomName := kingdom.name
    kingName: Text := kingdom.king.name
    time := kingdom.clock in second
    timeText := "{kingdom.clock}"
}
```

`look` y `message` se declaran en MUD pero no se llaman desde MUD. El exterior consulta un `look`; el runtime detecta y publica un `message`.

Un campo público cuyo valor directo es una magnitud debe seleccionar preferentemente su unidad con `in`. Omitirla es legal y usa la unidad raíz o combinación canónica, pero produce un aviso por dejar implícita una decisión de la API. Una magnitud de punto directa publica su coordenada en la unidad elegida y no su `format`; para publicar el formato se construye un campo `Text`.

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

La forma `name [: Type] := expression` declara un valor local inmutable. El tipo se infiere si existe una solución única; en otro caso debe escribirse. No admite `mut`, `in` ni especificación de colección propia.

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

add value to collection
remove value from collection

add mut morale: Nat in 0..100 = 50 to Army
remove morale from Army

create Declaration
destroy Declaration
```

La forma `remove name from Owner` se distingue de retirar un valor mediante resolución y tipos. En ambos casos el parser conserva la misma procedencia; el AST elaborado debe producir la variante correcta o un diagnóstico.

## `for each` y cuantificadores

```mud
for each person in kingdom.people if person.hungry {
    person.health -= 1
}

for each value in 0..100 by 5 {
    ...
}
```

`by` precede a `if`. Un diccionario puede vincular `(key, value)`.

Cuantificadores y agregaciones:

```mud
exists person in kingdom.people: person.hungry
forall person in kingdom.people: person.alive
count person in kingdom.people: person.hungry
sum city in kingdom.cities: city.population
min city in kingdom.cities: city.population
max city in kingdom.cities: city.population
```

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

`a..b` equivale a `[a..b]`; `[a]`, a `[a..a]`. Un extremo `*` debe estar cerrado en su lado. La forma cíclica exclusiva de magnitudes de punto es `[a..b cycle)`.

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

Los dominios declarados en la cabecera de una magnitud conservan los límites numéricos desnudos interpretados en su unidad canónica. La forma `[a..b cycle)` también conserva esa restricción y exige un periodo estrictamente positivo.

## Precedencia y agrupación

De mayor a menor:

| Nivel | Formas | Agrupación |
| ---: | --- | --- |
| 1 | acceso `.`, índice `[]`, llamada `()` y `unit from container in point` | izquierda o forma completa |
| 2 | prefijos `old`, `allowed`, `not`, signo | derecha |
| 3 | `*`, `/`, `%` | izquierda |
| 4 | `+`, `-` | izquierda |
| 5 | sufijos `to Type`, `in unit` | acumulativa |
| 6 | `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, pertenencia `in` | restringida |
| 7 | sufijo temporal `changes` | no asociativa |
| 8 | `and`, `&` | izquierda |
| 9 | `or`, `|` | izquierda |
| 10 | `xor`, `^` | izquierda |
| 11 | `=>` | derecha |
| 12 | `<=>` | cadena adyacente |
| 13 | `eventually ... through ...` | exterior |

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
- `is`
- pertenencia `in`
- `=>`

No se mezclan operadores distintos dentro de una misma cadena sin conjunciones explícitas.

## `Text` y operadores

`|` concatena `Text`:

```mud
"Hello, " | name
```

No se admiten `&`, `^` ni `-` sobre `Text`. `xor` es exclusivamente lógico y `^` exclusivamente conjuntista. Los aliases nominales de `Text` no adquieren concatenación implícita.

Todo literal `Text`, ordinario o multilínea, es una plantilla. `{e}` evalúa `e` e inserta la representación de su valor; `anchor{d}` inserta el ancla canónica de la entidad designada:

```mud
"Kingdom: {kingdom}"
"Population: {kingdom.population:6}"
"Rule: anchor{CanRecruit}"
"Literal braces: \{example\}"
```

`anchor` es contextual dentro de la plantilla. `anchor{...}` no forma una llamada ni una conversión general a `Text`.

Son renderizables directamente `Text`, `Char`, `Bool`, los números básicos, los valores `thing`, los miembros de `family`, los intervalos, las colecciones y las magnitudes. Una llamada a regla booleana también lo es porque produce `Bool`. El nombre desnudo de una declaración no es un valor; acciones, reglas reactivas, reglas `always`, `look`, `message`, tests, tipos y declaraciones `family` producen error estático dentro de `{...}`.

Una `thing` se representa mediante el valor de su propiedad intrínseca `name`; `anchor{...}` continúa representando su ancla canónica. Un miembro de `family` se representa mediante el nombre del miembro. Un intervalo usa su forma canónica normalizada. Una colección omite solo sus corchetes exteriores y separa elementos mediante `, `; toda colección que aparezca como elemento conserva sus propios corchetes:

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

Una magnitud lineal sin `in` se representa en su unidad raíz o combinación canónica. Una magnitud de punto usa su `format` si lo tiene y, si no, sigue esa misma regla ordinaria, incluida la escritura de la unidad. `{magnitude in unit}` selecciona la unidad y, para un punto, evita el `format` y representa la coordenada completa. Se escribe la abreviatura de la unidad si existe; en otro caso, el nombre singular para `1` y `-1`, y el plural para los demás valores.

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
4. Después de `:`, `:=`, `->` o `.` cuando falta su operando o miembro.
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

Si nombres, tipos y restricciones de la expresión no determinan una única interpretación válida, el programa es inválido y debe aportar el tipo que falte. No se aplica una preferencia implícita. Por ejemplo, una derivación sin contexto suficiente no puede elegir arbitrariamente si `[3]` es una colección o el intervalo `[3..3]`. D-059 sí fija expresamente `1..5 m` como la forma de unidad común `(1..5) m`; no queda a elección del parser.

## Recuperación de errores

Una implementación puede sincronizar después de un error en:

- `TERMINATOR`
- `}`
- Inicio inequívoco de una declaración superior

La recuperación solo mejora diagnósticos. No puede insertar silenciosamente semántica ni aceptar una forma fuera de la gramática.

## Construcciones contextuales conservadas

El parser no decide cuestiones que requieren resolución:

- Si un camino con puntos atraviesa namespaces, declaraciones o miembros.
- Si un literal estructural usado antes de una llamada representa un receptor único o varios receptores.
- Si un `postfix-expression` de un efecto es una llamada de acción.
- Si una acción es elemental o compuesta.
- Qué tipo contextual selecciona un literal estructural, de unidad, de punto o textual de un único escalar.

La CST conserva la forma concreta y el AST superficial una forma no resuelta. Las fases posteriores realizan la clasificación.

## Representación de magnitudes

La anotación opcional de una magnitud usa la sintaxis general `declared-type`. Una regla estática posterior exige que el tipo resuelto sea una representación numérica permitida. La gramática no mantiene una lista cerrada duplicada de tipos numéricos.
