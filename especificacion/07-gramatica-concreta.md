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
  - Q-055
  - Q-059
decisions:
  - D-025
  - D-027
  - D-028
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
---

# 07. Gramática concreta

## Estado y propósito

[[gramatica/mud.ebnf]] define la sintaxis completa de MUD 1.0. Este capítulo fija cómo leerla, cómo resolver las construcciones contextuales y cómo agrupar expresiones. Las cuestiones listadas en el frontmatter afectan semántica posterior, no impiden reconocer la forma fuente.

## Programa

Un archivo contiene declaraciones `using` y declaraciones de primer nivel:

```mud
using world.people
using physics.*
```

No existe una declaración `namespace`; se deriva de la ruta. `using`, no `import`, es la única construcción de visibilidad entre namespaces.

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
- `start with`

## `thing`

```mud
thing World {
}

abstract thing Place {
}

thing Alexandria as City, Place {
    name: Text = "Alexandria"
}
```

La lista posterior a `as` no expresa prioridad. `create` no acepta aquí ni en ningún otro lugar un cuerpo:

```mud
create Alexandria
destroy Alexandria
```

## Campos

Forma almacenada:

```text
[mut] name: Type [in domain] [collection-specification] [= value]
```

Forma calculada:

```text
name [: Type] := expression
```

La anotación de tipo es opcional. Si se omite, el tipo debe poder inferirse unívocamente de la expresión, sin prioridades predeterminadas entre representaciones o formas contextuales compatibles. Si hay más de una solución, el tipo debe escribirse. Un campo calculado no admite `mut`, dominio ni especificación de colección adicionales.

El `mut` exterior se escribe antes del nombre porque califica el lugar almacenado, no el tipo de sus miembros. `name: mut Type` no pertenece a la sintaxis.

```mud
mut population: Population in [0..*] [1] = 10 people
density := population / area
displayDensity: Density := density
```

Si el compilador puede demostrar que un campo calculado conservaría exactamente el mismo valor observable como campo almacenado inmutable, debe sugerir esa forma más directa. No es un error ni una reescritura automática, y la sugerencia no aparece si el cálculo depende de estado cambiante.

## Colecciones y diccionarios

La cardinalidad, cuando aparece, ocupa el inicio de los corchetes. Los modificadores pueden separarse por espacio o por coma:

```mud
citizens: Person [0..* unique ordered mut]
citizens: Person [0..*, unique, ordered, mut]
```

No se permite coma final. La omisión de cardinalidad equivale a `[1]`.

Las colecciones compatibles admiten `|`, `&`, `-` y `^`. Operan sobre multiplicidades, no concatenan:

```mud
leftChars: Char [1..5] = ['a']
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

`ordered by expression` pertenece a colecciones cuyo tipo admita una clave semántica. En una colección de `ordered family`, la expresión puede consultar los datos asociados del miembro mediante nombres no cualificados; el orden de declaración desempata claves iguales:

```mud
route: Terrain [* ordered by movementCost]
```

La clave debe poseer orden semántico total. Se prohíbe `ordered by` para `Char`; su orden es Unicode. `Text` no acepta especificaciones de colección.

## Aliases

```mud
alias PlayerName := Text

alias Board :=
    Square -> Piece [0..32 ordered]

alias Square {
    file: File
    rank: Rank
}

alias Pagination {
    page: Natural = 1
    size: Natural = 20
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

## Familias

```mud
family Terrain {
    movementCost: Natural = 1
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

Los miembros se separan por comas y no admiten coma final. `ordered family` hace comparables sus miembros en orden de declaración y permite usar sus datos asociados, incluidos los calculados, como claves de `ordered by` en colecciones.

## Magnitudes

Magnitud base:

```mud
magnitude Probability: Number in [0..1] {
}
```

Magnitud derivada:

```mud
magnitude Speed: Number in [0..*] :=
    Length / Time
{
    unit := 1 m/s {
        name = "fastie"
        plural = "fasties"
        abbreviation = "fst"
    }
}
```

Magnitud de punto:

```mud
magnitude TimeOfDay point over Time in [0..86_400 cycle) {
    format = "{hour:2}:{minute:2}:{second:2}"
}
```

Una magnitud base puede tener una `root unit`; una derivada solo unidades nominales alternativas; una magnitud de punto no declara unidades. La gramática de la cadena `format` queda separada del lenguaje MUD general y continúa en Q-055.

Las formas producidas por ese minilenguaje ocupan el token contextual `POINT_LITERAL`; por ejemplo, el objetivo es que un formato horario pueda reconocer `12:30:00`. Q-055 debe cerrarse antes de declarar conforme esa familia de literales.

## Participantes

`for` vincula roles suministrados de cualquier tipo de valor declarado. Un rol puede ser individual o colectivo y admite la especificación completa de colección. `on` construye vinculaciones automáticas exclusivamente individuales cuyo tipo debe ser una `thing`.

```mud
rule CanAttack for attacker: Army, defender: Army
given maximumDistance: Length {
    distance <= maximumDistance
}

rule AllAdults for people: Person [1..*, unique] {
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

El tipo se infiere en un participante relacionado: se escribe `kingdom in world.kingdoms`, no `kingdom: Kingdom in ...`.

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

La declaración anterior puede cambiar la membresía u orden de la colección almacenada recibida y modificar sus miembros. `mut patients: Person [*]` concede solo la primera capacidad; `patients: Person [*, mut]`, solo la segunda. La capacidad interior `mut` solo es válida cuando el tipo efectivo de miembro es una `thing`; los valores básicos, aliases y miembros de `family` son inmutables.

La mutabilidad exterior sí puede aplicarse a una colección de cualquier tipo:

```mud
action Record for mut observations: Number [*]
given value: Number {
    then add value to observations
}
```

Reglas booleanas y `look`, por ser puros, no admiten `mut` exterior.

Una referencia ordinaria a `World` designa la identidad exacta. `on World` y un rol `for World` seleccionan reflexivamente las `thing` concretas activas que satisfacen `is World`, incluida la propia `World` si es concreta. Esta selección solo se aplica cuando el tipo del rol es una `thing`.

La vinculación depende de la categoría del rol:

- una `thing` se vincula por identidad;
- un básico, alias, miembro de `family`, diccionario u otro valor inmutable se vincula por valor;
- un rol con `mut` exterior se vincula por identidad del lugar almacenado y conserva además su valor actual.

## Reglas

### Booleana

El cuerpo contiene directamente una expresión `Bool`:

```mud
rule IsAdult for person: Person {
    person.age >= 18
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

`changes` es postfix:

```mud
when day changes

when {
    calendar.day
} changes
```

### `always`

```mud
always rule ValidPopulation on kingdom: Kingdom {
    kingdom.population >= 0 people
}
```

El cuerpo contiene directamente la condición, sin `if`.

## Acciones

```mud
action Recruit for kingdom: Kingdom [mut]
given amount: Natural in 1..100 {
    if kingdom.treasury >= amount * recruitmentCost
    then {
        kingdom.treasury -= amount * recruitmentCost
        kingdom.soldiers += amount
    }
    after kingdom.soldiers >= old kingdom.soldiers
}
```

`then` contiene efectos o llamadas a acciones conforme a la distinción estática entre acciones elementales y compuestas.

## Frontera de salida

```mud
look RealmSummary for kingdom: Kingdom {
    name := kingdom.name
    population: Population := kingdom.population
}

message KingChanged on kingdom: Kingdom {
    when kingdom.king changes
    if kingdom.visible

    kingdomName := kingdom.name
    kingName: Text := kingdom.king.name
}
```

`look` y `message` se declaran en MUD pero no se llaman desde MUD. El exterior consulta un `look`; el runtime detecta y publica un `message`.

## Cláusulas y llaves

`when`, `if`, `then` y `after` siempre pueden usar llaves. Pueden omitirlas cuando contienen un único elemento. Un `then` con más de un efecto y un `after` de test con más de una aserción deben usarlas.

```mud
if ready

if {
    ready
}
```

Las llaves no suprimen los terminadores entre elementos de un bloque.

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

Las etiquetas de `given` no reordenan:

```mud
game.Search(origin, depth = 3, true)
```

Pueden mezclarse argumentos etiquetados y desnudos, pero cada etiqueta debe coincidir con la posición declarada.

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

add mut morale: Natural in 0..100 = 50 to Army
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

## Precedencia y agrupación

De mayor a menor:

| Nivel | Formas | Agrupación |
| ---: | --- | --- |
| 1 | acceso `.`, índice `[]`, llamada `()` | izquierda |
| 2 | prefijos `old`, `allowed`, `not`, signo | derecha |
| 3 | `*`, `/`, `%` | izquierda |
| 4 | `+`, `-` | izquierda |
| 5 | sufijos `to Type`, `in unit` | acumulativa |
| 6 | `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, pertenencia `in` | restringida |
| 7 | `and`, `&` | izquierda |
| 8 | `or`, `|` | izquierda |
| 9 | `xor`, `^` | izquierda |
| 10 | `=>` | derecha |
| 11 | `<=>` | cadena adyacente |
| 12 | `eventually ... through ...` | exterior |

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

No se admiten `&`, `^` ni `-` sobre `Text`. `xor` es exclusivamente lógico. Los aliases nominales de `Text` no adquieren concatenación implícita.

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

Si nombres, tipos y restricciones de la expresión no determinan una única interpretación válida, el programa es inválido y debe aportar el tipo que falte. No se aplica una preferencia implícita. Por ejemplo, una derivación sin contexto suficiente no puede elegir arbitrariamente si `[3]` es una colección o el intervalo `[3..3]`.

## Recuperación de errores

Una implementación puede sincronizar después de un error en:

- `TERMINATOR`
- `}`
- Inicio inequívoco de una declaración superior

La recuperación solo mejora diagnósticos. No puede insertar silenciosamente semántica ni aceptar una forma fuera de la gramática.
