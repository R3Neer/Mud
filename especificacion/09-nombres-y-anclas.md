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
  - D-101
  - D-035
  - D-065
  - D-072
  - D-078
  - D-085
  - D-086
  - D-087
  - D-088
  - D-090
  - D-091
  - D-093
  - D-094
  - D-096
  - D-097
  - D-100
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

Participantes `for`, `on` y `given` son símbolos léxicos con ancla subordinada estable según el modelo de descriptores. Iteradores y vinculaciones locales ordinarias continúan sin ancla pública. Los nombres pueden repetirse en ámbitos independientes, pero no pueden sombrear un nombre ya visible.

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


## Ámbitos locales, iteración y bloques

Las vinculaciones de iteración y todas las declaraciones locales son `LocalSymbol`: no reciben ancla pública y obedecen al primer nivel léxico de resolución. El `kind` del HIR distingue como mínimo iterador, local calculada y local almacenada; la mutabilidad es una capacidad comprobada posteriormente y no una categoría de ancla.

En `ExpressionBlock` y en los preámbulos compartidos de action/rule/message solo se introducen locales calculadas puras. Cada local es visible desde la declaración siguiente hasta el final del bloque propietario y no puede sombrear un nombre visible.

`ValueBlock` crea una frontera léxica propia. Sus declaraciones calculadas y almacenadas se introducen secuencialmente. Un `LocalForEach` resuelve `source` y `by` antes de introducir su binding; el binding es visible en el filtro y en `LocalStatementBlock`. Las locales creadas dentro de una iteración no sobreviven a la siguiente. Una mutación puede referirse a una local mutable de un ámbito envolvente del mismo `ValueBlock`; la comprobación de que el destino final no escape del bloque pertenece a tipado/elaboración.

En el `for each` ejecutable se mantienen las mismas reglas de introducción del binding, pero el cuerpo pertenece al `EffectBlock` y puede escribir lugares exteriores conforme a su autoridad. En una selección o cuantificador, la vinculación solo vive dentro de su `ExpressionBlock`.

En asociaciones `->` y ramas `-->`, el bloque izquierdo y el derecho crean scopes hermanos: las locales de clave/selector no son visibles en valor/resultado. Ambos ven el entorno exterior común y las ramas funcionales conservan además su binding contextual `value` cuando corresponda.

Las locales calculadas y almacenadas siguen sin ancla pública. Una local almacenada mutable puede satisfacer un participante `for mut`; la resolución nominal vincula el nombre al `LocalSymbol`, mientras tipado/elaboración comprueban que la ocurrencia usada como receptor designa un slot escribible. El HIR nominal no necesita una clase de referencia ni de símbolo adicional.

Ningún ámbito local permite referencias adelantadas, ciclos, redeclaración o sombreado de un nombre ya visible.

## Etapas

1. El AST superficial aporta nombres y procedencia.
2. La resolución nominal crea símbolos, scopes, bindings y anclas y los materializa en el HIR nominal de `nombres/mud-nominal-hir.asdl`.
3. El sistema de tipos consume AST superficial + HIR nominal y resuelve uniones, dominios y referencias dependientes del tipo.
4. La elaboración completa accesos, llamadas, abreviaturas contextuales y demás significado dependiente de tipos; su representación mecánica posterior todavía no está fijada.

El HIR nominal no contiene tipos efectivos, dominios efectivos, cardinalidades ni pruebas de terminación. Es el contrato entre resolución de nombres y tipado, no una copia resuelta del AST superficial.

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
family::game.world.Terrain::movementCost
magnitude::physics.Length
unit::physics.Length::meter
action::game.combat.Heal
type::Nat
type::Prefix
thing::game.people.Person::friends~summary
```

La forma canónica es `<categoría>::<nombre-cualificado>` y, para una declaración anidada, añade `::<miembro>` por cada propietario. Un metadato configurado añade `~<identificador-metadata>` a la ancla de su propietario. Los identificadores de MUD no contienen `::` y `~` pertenece al espacio postfix reservado, de modo que ambas separaciones son inequívocas. El catálogo de categorías de MUD 1.0 es:

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

Los participantes `for`, `on` y `given` no introducen una categoría superior nueva: su ancla es subordinada a la del propietario y deriva además de la clase de cláusula y del identificador, conforme al modelo de descriptores. La posición nunca forma parte de esa identidad.

`start with` de módulo no introduce nombre y, por tanto, no posee ancla. La categoría describe la declaración propietaria: un campo de `look` conserva una ancla como `look::game.Status::score`, no una categoría adicional `field`.

Poseen ancla:

- declaraciones nominales de primer nivel;
- campos, componentes y datos asociados declarados por una `family`;
- miembros de family;
- unidades declaradas;
- participantes `for`, `on` y `given`;
- metadatos configurados y de usuario materializados como `Metadata`;
- tipos incorporados.

No poseen ancla pública:

- variables locales o de iteración;
- vinculaciones temporales que no sean participantes declarados;
- resultados intermedios;
- unidades creadas estructuralmente por prefijos;
- los valores incorporados `Prefix`, que se elaboran como constantes y no como declaraciones;
- las ramas de diccionarios funcionales, que se identifican solo de forma local dentro de su diccionario propietario;
- las propiedades reflectivas intrínsecas, que no materializan objetos `Metadata`.

Un dato asociado declarado por una `family` posee un ancla subordinada estable formada con la categoría `family`, el nombre cualificado de la familia y el identificador del dato. Esa ancla identifica el descriptor del esquema uniforme, no cada valor obtenido al consultar un miembro. Una asignación dentro del cuerpo de un miembro no introduce ancla y no cambia la del dato declarado.

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

Después de la resolución nominal se construye un grafo parcial sobre símbolos resueltos. El HIR nominal conserva exactamente estas familias de aristas:

- `Owns`: propiedad o contención nominal;
- `Specializes`: especialización nominal entre declaraciones;
- `RefersTo`: referencia nominal cuyo origen y destino ya son símbolos resueltos.

Tipos y dominios efectivos, inicialización elaborada, cálculos, lecturas, escrituras, efectos, magnitudes derivadas y demás relaciones dependientes de tipos no pertenecen a esta fase. Se determinan, cuando corresponda, durante tipado y elaboración posteriores.

El grafo parcial no sustituye al AST ni constituye una fuente de verdad. Su finalidad es materializar exclusivamente las conclusiones de resolución nominal que deben sobrevivir como contrato entre el AST superficial y el sistema de tipos.

## Conformidad

Una implementación conforme debe producir los mismos candidatos y anclas, rechazar el sombreado y las colisiones indicadas, conservar la procedencia y permitir reconstruir el grafo nominal desde el programa fuente.

## Especialización de aliases

Las declaraciones `alias` pueden aportar aristas de especialización. El grafo nominal conserva las antecesoras directas escritas y la clausura `is` se calcula durante elaboración. Los miembros heredados mantienen el ancla de su origen. La resolución nominal conserva las contribuciones independientes; su posible fusión por equivalencia o su resolución explícita dependen de tipado y elaboración, no del orden nominal de `as`.


## Metadatos, descriptores y anclas subordinadas

El acceso reflectivo `~` distingue propiedades intrínsecas y metadatos configurados: `~identifier` es el identificador fuente, `~name` es presentación configurable y todo acceso `~` es runtime-readonly. Solo poseen metadatos propios entidades semánticas estables con descriptor tipado y ancla pública: declaraciones nominales, miembros de `family`, unidades, campos, componentes y participantes. Se excluyen expresiones, cuerpos de cláusula y ambos `start with` como propietarios; el de módulo continúa sin ancla.

Todo participante `for`, `on` y `given` tiene nombre y ancla subordinada basada en propietario, clase de cláusula e identificador. La posición no forma parte de la identidad. Los participantes son símbolos anclados; los locales ordinarios continúan como `LocalSymbol`. Los miembros heredados conservan descriptor, ancla y metadatos de su declaración original. `~metadata` enumera solo metadatos configurados, nunca propiedades intrínsecas.

Cada valor `Metadata` configurado posee a su vez una ancla terminal formada añadiendo `~<identificador-metadata>` a la ancla del propietario, por ejemplo `thing::game.Person::health~description`. Esa ancla sirve para reflexión y tooling; no convierte a `Metadata` en propietario de otros metadatos.

`Metadata` expone `~anchor`, `~path` y `~file`. Su `~path` es el path lógico de la entidad propietaria y su `~file` procede del archivo físico donde se declaró esa configuración de metadata. Entrar en `~<identificador-metadata>` cambia la identidad terminal, no el namespace lógico. Estas propiedades son intrínsecas del descriptor y no aparecen en la colección `~metadata`. `Metadata~metadata` no forma parte del contrato.

## Claves locales de ramas funcionales

> [!rule] MUD-NAME-006 — Sin ancla pública de rama
> Una rama de diccionario funcional no introduce símbolo anclado, nombre público ni propietario de metadatos. Su identidad persistente es la del diccionario que la contiene.

Cada rama funcional posee una `decision_branch_key` estructural local al diccionario para las fases que necesiten reconstrucción o dependencias posteriores. Para una rama ordinaria, la clave es la forma canónica del selector resuelto. Dos ramas ordinarias con la misma forma canónica dentro del mismo diccionario son inválidas: compartirían la misma clave estructural local. `_` usa una clave `FallbackBranchKey` distinta y única. Esa clave no es un símbolo, no pertenece al HIR nominal y su representación mecánica posterior no se fija todavía. El ordinal fuente se conserva por separado porque participa en `FirstMatch`, pero tampoco se convierte en ancla.

Las operaciones de tooling que requieran una referencia persistente deben dirigirse al diccionario propietario y expresar después la edición estructural de su conjunto o secuencia de ramas. `CREATE`, `UPDATE`, `REMOVE` y `MOVE` no pueden tratar una rama como entidad global independiente.

Las operaciones conjuntistas de funcionales no crean ni fusionan claves globales de rama: el nodo compuesto conserva referencias a ambos operandos y su grafo de dependencias es la unión transitiva de los dos.

## Pertenencia de paths

Sobre `MudPath`, la pertenencia usa `q has p`: es reflexiva y compara segmentos completos. La forma negativa usa `q has not p`:

```mud
world.combat has world.combat                  # true
world.combat has world.combat.melee            # true
world.combat has world.combatant                # false
world.combat has not world.trade                # true
```

## Identidad nominal exacta

`is` consulta la clausura de especialización; `iis` compara el tipo nominal efectivo exacto. El narrowing de `iis not` elimina una única posibilidad nominal y no elimina sus especializaciones. Esta distinción no crea anclas nuevas ni sustituye la igualdad de identidades singleton mediante `==`.

## Módulos, `uses` y anclas

La pertenencia a módulo es una dimensión de visibilidad y dependencia, no un componente adicional del ancla nominal. `uses` autoriza el conocimiento del contrato de otro módulo; un `using` no concede esa autorización. La resolución cruzada solo puede alcanzar operaciones y tipos pertenecientes al cierre visible del contrato modular.
