---
title: Nombres, paths y anclas
aliases:
  - Resolución de nombres de MUD
tags:
  - mud/especificacion
  - mud/nombres
status: propuesta
normative: true
depends-on:
  - "[[05-texto-fuente]]"
  - "[[08-sintaxis-abstracta]]"
questions:
  - Q-014
decisions:
  - D-035
  - D-065
  - D-072
  - D-078
  - D-085
  - D-086
  - D-087
  - D-088
  - D-090
---
# 09. Nombres, paths y anclas

## Estado y propósito

Este capítulo define qué nombres introduce un programa, cómo se resuelven y cuáles poseen identidad persistente. Un archivo y una declaración son entidades distintas: la ruta aporta contexto lógico, pero no forma parte de la sintaxis escrita del archivo.

## Paths de MUD

> [!definition] MUD-NAME-001 — Path de MUD
> El path de un archivo es la secuencia de segmentos `lowerCamel` derivada de su ruta relativa bajo la raíz del programa, excluyendo el nombre del archivo y su extensión.

No existe una declaración `namespace` ni una palabra reservada `path`. Un editor puede mostrar el path como cabecera virtual y ofrecer acciones para copiar nombres cualificados o anclas, pero esa presentación no pertenece al texto fuente.

Un nombre cualificado concatena path y nombre nominal mediante puntos:

```text
game.combat.Heal
```

Mover una declaración entre archivos del mismo path no cambia su nombre cualificado. Moverla entre paths sí.

## Símbolos y espacios de nombres

> [!rule] MUD-NAME-002 — Espacio nominal superior único
> Todas las declaraciones de primer nivel de un mismo path deben tener nombres distintos, con independencia de su categoría.

La categoría esperada no desambigua dos declaraciones superiores homónimas. Los campos y miembros anidados pertenecen al espacio de su propietario y pueden repetir nombres en propietarios distintos.

Participantes `for`, `on` y `given` son símbolos léxicos con ancla subordinada estable según D-087. Iteradores y vinculaciones locales ordinarias continúan sin ancla pública. Los nombres pueden repetirse en ámbitos independientes, pero no pueden sombrear un nombre ya visible.

> [!rule] MUD-NAME-003 — Convenciones obligatorias
> Declaraciones nominales y miembros de family usan `PascalCase`; campos, componentes, roles, `given`, variables y segmentos de path usan `lowerCamel`; los identificadores de unidad usan `lowerCamel`. Un incumplimiento es un error estático con arreglo mecánico cuando exista una única corrección segura.

## Entornos de resolución

Sea $Gamma$ un entorno y sea $n$ un nombre no cualificado. La resolución consulta estos niveles:

1. Símbolos del ámbito léxico.
2. Miembros del propietario o receptor implícito.
3. Declaraciones del path actual.
4. Declaraciones aportadas por `using` exactos.
5. Declaraciones aportadas por `using` recursivos.
6. Nombres incorporados.

> [!rule] MUD-NAME-004 — Primer nivel no vacío
> La resolución usa exclusivamente el primer nivel que produzca candidatos. Si ninguno de sus candidatos pertenece a la categoría exigida, la referencia es inválida; no continúa en niveles posteriores.

Candidatos que designan la misma ancla se deduplican. Dos anclas distintas en el mismo nivel producen ambigüedad. El orden textual de archivos y `using` no decide empates.

Un `using` exacto importa un path concreto y uno recursivo importa sus descendientes. Ninguno reexporta los `using` contenidos en los archivos alcanzados. Una referencia completamente cualificada evita la búsqueda por niveles.

`Prefix` participa en el último nivel como tipo incorporado. Los nombres SI `quecto`…`quetta` también se resuelven allí como constantes incorporadas de `Prefix`; no introducen declaraciones ni anclas propias.

Los accesos con puntos se elaboran por etapas: primero se resuelve la raíz nominal y después cada miembro con el tipo o propietario obtenido. Una ruta cualificada y una cadena de miembros pueden compartir escritura superficial sin compartir resolución interna.


## Ámbitos de iteración y bloques de expresión

Las vinculaciones de iteración y las declaraciones locales de `ExpressionBlock` son `LocalSymbol`: no reciben ancla pública y obedecen al primer nivel léxico de resolución.

En `for each`, la fuente y el `by` opcional se resuelven antes de introducir la vinculación. La variable simple o ambas variables de una pareja de diccionario pasan a estar visibles en el filtro `if` y en el cuerpo ejecutable. Una local declarada dentro del `ExpressionBlock` del filtro solo amplía el entorno de las locales posteriores y de la expresión final del filtro; no permanece visible en el cuerpo de efectos.

En una selección o un cuantificador/agregador, `source` y `by` se resuelven igualmente en el entorno exterior. Después se introduce la vinculación y se resuelve el `ExpressionBlock`: cada local ve las vinculaciones exteriores y las locales anteriores; el resultado final ve todas las locales del bloque. La vinculación y esas locales dejan de existir al terminar la expresión propietaria.

Ninguno de estos ámbitos permite referencias adelantadas, ciclos, redeclaración o sombreado de un nombre ya visible. El AST resuelto usa la variante genérica `LocalSymbol(owner, kind, name, ordinal)`; D-088 no introduce una clase de símbolo ni una categoría de ancla nuevas.

## Etapas

1. El AST superficial aporta nombres y procedencia.
2. La resolución nominal crea símbolos y resuelve declaraciones cuya categoría ya es conocida.
3. El sistema de tipos resuelve uniones, dominios y referencias dependientes del tipo.
4. La resolución de miembros completa accesos, llamadas y abreviaturas contextuales.

La norma se expresa mediante entornos y conjuntos de candidatos. Una implementación puede usar scope graphs si reproduce exactamente prioridades, candidatos, ambigüedades y rechazos.

## Anclas

> [!definition] MUD-NAME-005 — Ancla pública
> Una ancla es la identidad legible, global y sensible a mayúsculas de una entidad semántica persistente a la que la especificación asigna identidad pública.

Formas representativas:

```text
thing::game.people.Person
thing::game.people.Person::friends
alias::game.ids.UserId
family::game.rules.Severity
family::game.rules.Severity::Critical
magnitude::physics.Length
unit::physics.Length::meter
action::game.combat.Heal
type::Nat
type::Prefix
```

La forma canónica es `<categoría>::<nombre-cualificado>` y, para una declaración anidada, añade `::<miembro>` por cada propietario. Los identificadores de MUD no contienen `::`, de modo que la separación es inequívoca. El catálogo de categorías de MUD 1.0 es:

| Declaración | Categoría de ancla |
|---|---|
| `thing` y sus campos | `thing` |
| alias, sus componentes y sus campos derivados | `alias` |
| family, datos y miembros | `family` |
| magnitude | `magnitude` |
| unidad declarada | `unit` |
| cualquiera de las tres clases de rule | `rule` |
| action | `action` |
| look | `look` |
| message | `message` |
| test | `test` |
| tipo incorporado | `type` |

Los participantes `for`, `on` y `given` no introducen una categoría superior nueva: su ancla es subordinada a la del propietario y deriva además de la clase de cláusula y del identificador, conforme a D-087. La posición nunca forma parte de esa identidad.

`start with` global no introduce nombre y, por tanto, no posee ancla. La categoría describe la declaración propietaria: un campo de `look` conserva una ancla como `look::game.Status::score`, no una categoría adicional `field`.

Poseen ancla:

- declaraciones globales;
- campos y componentes;
- miembros de family;
- unidades declaradas;
- participantes `for`, `on` y `given`;
- tipos incorporados.

No poseen ancla pública:

- variables locales o de iteración;
- vinculaciones temporales que no sean participantes declarados;
- resultados intermedios;
- unidades creadas estructuralmente por prefijos;
- los valores incorporados `Prefix`, que se elaboran como constantes y no como declaraciones.

Un miembro heredado conserva el ancla del propietario que lo declaró. En `thing` esto no comparte estado; en aliases identifica el origen usado para deduplicar diamantes. Una sobrescritura de predeterminado no introduce un miembro ni un ancla nuevos.

Un diagnóstico puede describir un símbolo local mediante el ancla de su propietario:

```text
action::game.combat.Heal - given amount
```

La descripción completa no constituye una ancla nueva.

## Nombres contextuales de valores

Un miembro de family puede abreviarse cuando el tipo esperado determina la family:

```mud
severity: Severity = Critical
```

`Severity.Critical` continúa disponible. Las unidades aplican la misma regla con magnitud, identificador, `name`, plural y abreviatura. Si dos magnitudes continúan siendo posibles, se exige cualificación.

## Migración

Renombrar, cambiar de categoría o mover entre paths cambia el ancla. El tooling registra una correspondencia dirigida desde la anterior hacia la vigente. Esa correspondencia puede migrar referencias persistentes e historial, pero nunca convierte el nombre antiguo en alias admitido por el compilador.

El formato externo y ciclo completo del registro siguen abiertos en [[notas/preguntas/Q-014-migracion-de-anclas|Q-014]].

## Grafo nominal inicial

Después de la resolución nominal puede construirse un grafo parcial con nodos anclados y aristas de:

- propiedad y contención;
- especialización;
- referencia nominal;
- tipo y dominio escritos;
- inicialización y cálculo;
- lectura, escritura y efectos;
- magnitud, unidad y equivalencia.

El tipado completa o rechaza aristas cuya validez dependa de una unión, una inferencia o un miembro contextual. El grafo parcial no sustituye al AST ni constituye fuente de verdad.

El esquema mecánico [[mud-resolved-ast]] representa esta frontera: una declaración persistente y todo participante declarado usan `AnchoredSymbol`; los locales e iteradores ordinarios usan `LocalSymbol` subordinado a su propietario.

## Conformidad

Una implementación conforme debe producir los mismos candidatos y anclas, rechazar el sombreado y las colisiones indicadas, conservar la procedencia y permitir reconstruir el grafo nominal desde el programa fuente.

## Especialización de aliases

Las declaraciones `alias` pueden aportar aristas de especialización. El grafo nominal conserva las antecesoras directas escritas y la clausura `is` se calcula durante elaboración. Los miembros heredados mantienen el ancla de su origen; dos miembros independientes con el mismo nombre no se fusionan.


## Metadatos, descriptores y anclas subordinadas

D-087 generaliza `~`: `~identifier` es el identificador fuente, `~name` es presentación configurable y todo acceso `~` es runtime-readonly. Solo poseen metadatos propios entidades semánticas estables con descriptor tipado y ancla pública: declaraciones nominales, miembros de `family`, unidades, campos, componentes y participantes. Se excluyen expresiones, cuerpos de cláusula y ambos `start with` como propietarios; el global continúa sin ancla.

Todo participante `for`, `on` y `given` tiene nombre y ancla subordinada basada en propietario, clase de cláusula e identificador. La posición no forma parte de la identidad. Los participantes son símbolos anclados; los locales ordinarios continúan como `LocalSymbol`. Los miembros heredados conservan descriptor, ancla y metadatos de su declaración original. `~metadata` enumera solo metadatos configurados, nunca propiedades intrínsecas.

## Claves locales de entradas de diccionario

Las asociaciones exactas y las ramas decisionales no poseen ancla pública propia. Son entradas estructurales del valor diccionario y se direccionan dentro de su contenedor mediante una clave local conforme a D-090.

En un diccionario exacto se usa la clave ordinaria. En un decisional se usa la forma canónica del selector; el resultado y la posición no participan en esa clave y `_` es la clave especial del fallback. `CREATE`, `UPDATE`, `REMOVE` y `MOVE` pueden usar el par `(diccionario, clave-local)` sin convertirlo en `AnchoredSymbol` ni someterlo a migración de anclas.

Las operaciones conjuntistas de funcionales no crean ni fusionan identidades de rama: el nodo compuesto conserva referencias a ambos operandos y su grafo de dependencias es la unión transitiva de los dos.

## Pertenencia de paths

Sobre `MudPath`, `p in q` es reflexivo y compara segmentos completos:

```mud
world.combat in world.combat                  # true
world.combat.melee in world.combat            # true
world.combatant in world.combat                # false
world.trade not in world.combat                # true
```

## Identidad nominal exacta

`is` consulta la clausura de especialización; `iis` compara el tipo nominal efectivo exacto. El narrowing de `iis not` elimina una única posibilidad nominal y no elimina sus especializaciones. Esta distinción no crea anclas nuevas ni sustituye la igualdad de identidades singleton mediante `==`.
