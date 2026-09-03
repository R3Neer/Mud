---
id: D-087
title: "Metadatos reflectivos, descriptores estables y visibilidad exterior"
status: current
date: 2026-08-15
supersedes: []
superseded-by: []
questions: []
affects:
  - "metadatos postfix, reflexión, anclas subordinadas, participantes, campos y componentes, documentación, visibilidad exterior, defaults de archivo, gramática, CST, AST, IR, diagnósticos y tooling"
---

# ADR-087 — Metadatos reflectivos, descriptores estables y visibilidad exterior

- Modificada por: [[ADR-101-bloques-de-valor-variables-locales-almacenadas-and-extremos-por-testigos|D-101]].

- Modifica: [[ADR-036-participants-recipients-and-calls|D-036]], [[ADR-037-fields-and-declarative-domains|D-037]], [[ADR-076-named-units-prefixes-and-adjacent-notation|D-076]] y [[ADR-085-diccionarios-funcionales-metadatos-and-activacion-estructurada|D-085]].
- Amplía: [[ADR-035-organisation-names-using-and-anchors|D-035]], [[ADR-051-graph-future-semantics-and-reconstructable-information|D-051]], [[ADR-070-lossless-cst-and-normalised-surface-ast|D-070]] y [[ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]].
- Precisada por: [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]], [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]], [[ADR-092-disponibilidad-estatica-de-propiedades-reflectivas|D-092]] y [[ADR-094-anclas-terminales-de-metadatos-configurados|D-094]].

## Contexto

D-085 introdujo los metadatos postfix `~name`, `~path`, `~anchor` y `~file`, pero no fijó un sistema general de reflexión ni una regla uniforme para metadatos definidos por el autor. También conservó escrituras runtime de `~name` y participantes individuales anónimos. La ampliación actual necesita descriptores estables para declaraciones y elementos subordinados, documentación estructurada, defaults de archivo y una frontera explícita entre estado del mundo y metadatos del modelo.

## Decisión

### Operador postfix `~`

La única forma de acceso es:

```mud
expression~property
```

`expression.~property` y `~~` no pertenecen a MUD. El espacio `~` es distinto del espacio de campos ordinarios.

Todo acceso `~` es de solo lectura durante la ejecución. Ninguna propiedad `~` puede aparecer como destino de una asignación o actualización runtime. Esto sustituye la autorización anterior de D-085 para escribir `~name` durante una action. Los metadatos configurables cambian mediante edición del modelo y nueva elaboración, no mediante efectos del mundo.

`mut` es inválido en una declaración de metadato. Un metadato puede ser almacenado mediante `=` o calculado mediante `:=`. El calculado puede depender de valores que cambien y reevaluarse con ellos, pero continúa sin ser asignable.

Los metadatos no forman parte del payload de alias, igualdad de valores, construcción de valores, campos ordinarios, cardinalidad exterior ni store ordinario de una `thing`. Existen aunque el propietario esté inactivo. `create` y `destroy` no crean ni eliminan metadatos.

### Preámbulo del propietario

Los metadatos configurables y de usuario se escriben al comienzo del cuerpo del propietario, antes de campos, componentes, miembros, participantes, cláusulas o contenido ordinario:

```mud
thing Nora as Person {
    ~name = "Nora"
    ~summary = "Persona principal del ejemplo"
    ~author: Text = "Samuel"

    mut health: Nat = 100
}
```

Una declaración `~...` que aparezca después del primer contenido ordinario del mismo cuerpo es inválida. Los metadatos intrínsecos no se declaran.

### Principio de admisión

Un elemento puede poseer metadatos propios únicamente cuando satisface conjuntamente:

1. existe como entidad semántica estable después de resolución;
2. posee descriptor tipado propio;
3. posee ancla pública estable;
4. el metadato describe al elemento completo y no una ocurrencia sintáctica accidental;
5. su existencia no depende de una ejecución concreta.

Por ello pueden ser metadata-bearing las declaraciones nominales ancladas, miembros de `family`, unidades, campos almacenados/calculados/públicos, datos asociados almacenados/calculados de una `family`, componentes de alias y participantes `for`/`on`/`given`.

No lo son expresiones, sentencias, operandos, condiciones, cuerpos de cláusula, tokens, nodos arbitrarios del AST ni ramas funcionales sin descriptor estable. Una rama de diccionario funcional tampoco posee ancla pública: su identidad estructural local pertenece al diccionario propietario y sirve para reconstrucción y análisis posteriores, sin convertirse en ancla ni símbolo. `when`, `if`, `then`, `after` y `otherwise` pueden reflejarse como clases presentes mediante `~clauses`, pero sus cuerpos no se convierten en objetos metadata-bearing.

Un valor `Metadata` configurado sí posee descriptor y ancla propios para reflexión y tooling, pero es **terminal**: no puede poseer metadata propia y no expone `~metadata`. D-094 fija esta excepción deliberada al principio de admisión.

La declaración global `start with` continúa sin nombre y sin ancla pública, por lo que no admite metadatos. El `start with` local de un `test` es parte del descriptor del test, no una declaración independiente, y tampoco admite metadatos.

### Propiedades intrínsecas comunes

Según la categoría estática del receptor se exponen, cuando tengan sentido:

```text
~identifier : Name
~anchor     : Anchor
~path       : MudPath
~file       : MudFile
~kind       : family reflectiva específica
```

`~identifier` es el identificador fuente. `~name` es presentación humana configurable y no participa en resolución, igualdad ni formación de anclas.

`~file` puede leerse en expresiones. Si una lectura de `~file` influye en una condición, cálculo o efecto que altere comportamiento del mundo, se conserva el warning de fragilidad física fijado por D-085.

### Reflexión de declaraciones

Las declaraciones ancladas exponen, según categoría:

```text
~metadata           : Metadata [* unique]
~creatable          : Bool
~destroyable        : Bool
~active             : Bool
~abstract           : Bool
~parents            : Declaration [* unique]
~ancestors          : Declaration [* unique]
~children           : Declaration [* unique]
~descendants        : Declaration [* unique]
~fields              : Field [* unique]
~declaredFields      : Field [* unique]
~components          : Component [* unique]
~declaredComponents  : Component [* unique]
```

`~parents` devuelve solo padres directos; `~ancestors`, el cierre transitivo estricto y nunca al receptor. `~children` y `~descendants` son las relaciones inversas. Los metadatos estándar o de usuario no aparecen en `~fields`.

`~metadata` materializa únicamente metadatos estándar configurados y metadatos de usuario del receptor. Las propiedades intrínsecas no aparecen como valores `Metadata`.

### Familias reflectivas

Se incorporan las familias conceptuales:

```mud
family DeclarationKind {
    Thing, Alias, Family, FamilyMember, Magnitude, Unit,
    Rule, Action, Subaction, Look, Message, Test, Start
}

family RuleKind { Boolean, Reactive, Always }
family ActionKind { Action, Subaction }
family FieldKind { Stored, Calculated, Public }
family ClauseKind { When, If, Then, After, Otherwise }
family ParticipantClause { For, On, Given }
family MetadataKind { Standard, User }
```

`Start` puede describir la categoría de la declaración global en tooling/reflexión de proyecto, pero no implica que esa construcción posea ancla o `~metadata`.

Las keywords duras de categoría ya presentes en la gramática pueden aparecer desnudas en posición de expresión como valores de `DeclarationKind`: `thing`, `alias`, `family`, `magnitude`, `rule`, `action`, `subaction`, `look`, `message` y `test`. La forma superficial se conserva como un valor categorial, no como una referencia nominal. Los miembros de `DeclarationKind` que no poseen keyword dura propia no reciben por esta decisión una grafía literal nueva.

El narrowing categorial admite formas como `declaration is rule`, `declaration is action`, `declaration is subaction` y `declaration is thing`. `~type` no sustituye esta clasificación.

El catálogo completo de miembros de `TypeKind` pertenece a la especificación del sistema de tipos; esta decisión no inventa dicho catálogo.

### Firmas y participantes

La disponibilidad de una propiedad reflectiva depende de la categoría estática compatible del receptor. Que la gramática pueda reconocer `expression~name` no hace que ese nombre exista para todo receptor. D-092 fija esta frontera de lookup.

Las propiedades de participantes tienen estas capacidades por subcategoría de declaración:

| Subcategoría | `~for` | `~on` | `~given` |
| --- | --- | --- | --- |
| regla booleana | sí | no | sí |
| regla reactiva | no | sí | no |
| regla `always` | no | sí | no |
| `action` | sí | no | sí |
| `subaction` | sí | no | sí |
| `look` | sí | no | sí |
| `message` | no | sí | no |
| demás declaraciones | no | no | no |

Cuando una propiedad está soportada por la subcategoría pero la declaración concreta omite su cláusula opcional, el valor es `empty` con el tipo de colección correspondiente. Cuando la propiedad no está soportada por la subcategoría estática, el acceso es un error estático; no produce `empty` ni un valor predeterminado. Por ejemplo, `thing A` hace inválido `A~for`, mientras que una `action` sin cláusula `for` admite `ActionName~for` y devuelve `empty`.

```text
~for     : Participant [* unique ordered]
~on      : Participant [* unique ordered]
~given   : Participant [* unique ordered]
~clauses : ClauseKind [* unique]
```

`~clauses` informa solo de presencia de clases, nunca expone el AST del cuerpo. Su disponibilidad sigue igualmente el contrato de propietario de la propiedad; la regla anterior sobre `empty` no convierte `~clauses` ni ninguna otra propiedad en universal.

Todo participante `for`, `on` y `given` debe tener identificador fuente explícito. Queda retirada la forma anónima admitida por D-036. El orden continúa formando parte de la firma, pero no de la identidad persistente.

Cada participante posee ancla pública derivada de:

```text
ancla-del-propietario + clase-de-cláusula + identifier
```

La posición nunca se usa como identidad. Reordenar participantes no cambia sus anclas. Dos participantes homónimos en cláusulas distintas siguen siendo distintos porque la clase `For`, `On` o `Given` forma parte de la derivación.

`Participant` expone:

```text
~identifier       : Name
~anchor           : Anchor
~path             : MudPath
~file             : MudFile
~owner            : Declaration
~clause           : ParticipantClause
~position         : Nat
~type             : Type
~domain           : Domain
~cardinality      : Cardinality
~mutable          : Bool
~elementsMutable  : Bool
~hasDefault       : Bool
~default          : Any [0..1]
~metadata         : Metadata [* unique]
```

Un `metadata-body` unido a un participante describe el slot de la firma, no el valor recibido.

Una cabecera puede agrupar varios identificadores con un tipo y un único `metadata-body`:

```mud
for attacker, target: Fighter {
    ~category: ParticipantCategory = Combatant
}
```

El cuerpo se copia semánticamente a cada descriptor. El grupo no introduce descriptor ni ancla adicional. Participantes con metadatos distintos se escriben como elementos separados de la misma cláusula, separados por coma.

### Campos y componentes

Los descriptores `Field` exponen:

```text
~identifier ~anchor ~kind ~type ~domain ~cardinality
~mutable ~elementsMutable ~hasDefault ~default
~inherited ~declaredBy ~metadata
```

`~kind` usa `FieldKind`. Los datos asociados declarados por una `family` reutilizan `Field`: un dato almacenado usa `FieldKind.Stored` y uno calculado `FieldKind.Calculated`. No se crea `FamilyDataKind`. Su ancla es subordinada a la `family`; el valor proyectado por cada miembro no obtiene descriptor ni metadatos propios. Los componentes de alias exponen el mismo contrato estructural salvo que `~mutable` es siempre `false`; esta decisión no crea una `ComponentKind` nueva.

Un miembro heredado conserva el ancla, descriptor y metadatos del elemento que lo declaró. No se fabrican copias metadata-bearing por cada descendiente.

Campos, componentes y datos asociados declarados por una `family` pueden llevar metadata propia. Con un valor breve conservan el cuerpo inmediato exclusivamente de `~...`; cuando usan `ValueBlock`, esas declaraciones pueden integrarse como preámbulo contiguo al principio del mismo cuerpo. En ambos casos pertenecen al descriptor y no al valor ni a las sentencias del `ValueBlock`. Una declaración no combina simultáneamente ambos lugares de metadata. Una asignación de dato dentro de un miembro de `family` no admite ese cuerpo porque no declara un descriptor nuevo. Un campo añadido dinámicamente por un efecto no puede adquirir metadatos persistentes porque no satisface el principio de admisión.

### Descriptor `Metadata`

Un valor `Metadata` expone al menos:

```text
~identifier  : Name
~anchor      : Anchor
~path        : MudPath
~file        : MudFile
~type        : Type
~domain      : Domain
~cardinality : Cardinality
~kind        : MetadataKind
~owner       : Declaration | Field | Component | Participant | FamilyMember | Unit
~calculated  : Bool
```

Las propiedades intrínsecas no se convierten en `Metadata` y no reciben ancla de metadata. Los nombres intrínsecos y estándar reservados no pueden ser ocultados por un metadato de usuario. La ancla de un metadato configurado se deriva como `<ancla-propietario>~<identificador-metadata>`; cambiar su valor no cambia identidad.

Para un descriptor `Metadata`, `~path` conserva el `MudPath` lógico de su propietario y `~file` se deriva de la procedencia física de la declaración de metadata. Ninguna de estas propiedades materializa metadata adicional. `Metadata` continúa siendo terminal y no expone `~metadata`.

### Colecciones y diccionarios

Las colecciones exponen:

```text
~count       : Nat
~domain      : Domain
~cardinality : Cardinality
~unique      : Bool
~ordered     : Bool
~order       : Order [0..1]
```

Los diccionarios exactos añaden `~keyDomain` y `~valueDomain`. Los funcionales exponen `~inputDomain`, `~outputDomain`, `~resultCardinality`, `~recursive` y `~count`, donde `~count` cuenta ramas.

Todo valor MUD expone `~type: Type`. Los descriptores `Type` exponen `~kind`, `~domain` y `~cardinality`; el catálogo concreto de `TypeKind` se fija con el sistema de tipos.

### Metadatos estándar configurables

Se conservan los metadatos estándar de presentación y configuración con estos contratos principales:

```text
~name         : Name
~plural       : Text
~abbreviation : Text
~prefixes     : Prefix [* unique] = empty
~format       : Text
~summary      : Text = ""
~description  : Text = ""
~deprecated   : Text [0..1] = empty
```

`Prefix` es un tipo nominal incorporado. El catálogo SI fijado por D-076 proporciona valores incorporados de `Prefix` desde `quecto` hasta `quetta`. Sus nombres son identificadores ordinarios que se resuelven en el nivel de incorporados. Por ello `~prefixes = [kilo, milli]` es una colección MUD ordinaria, `all` enumera el dominio incorporado de `Prefix` y `empty` representa la colección vacía. Las unidades no mantienen `unit-property`, `prefix-selection` ni otra subgramática paralela: su cuerpo contiene exclusivamente declaraciones generales de metadatos.

`~name`, `~summary`, `~description` y `~deprecated` están disponibles en todo elemento metadata-bearing compatible. `~name` toma por defecto una presentación derivada de `~identifier`. `~summary` es una descripción breve; `~description` admite Markdown de presentación; `~deprecated` no vacío activa diagnóstico de obsolescencia pero no invalida el uso.

### Metadatos de usuario

Un nombre no reservado puede declarar metadatos almacenados o calculados:

```mud
~author: Text = "Samuel"
~important := Nora~path in world.main
```

Pueden declarar tipo, dominio, cardinalidad y modificadores compatibles con valores de solo lectura. No admiten `mut`, no se heredan y no alteran la forma del valor descrito.

### Defaults de archivo

Un archivo puede comenzar, antes de cualquier `using`, con defaults de metadatos almacenados y constantes:

```mud
~stability: Stability = Experimental
~summary = "Subsistema interno"

using world.shared
```

Estas líneas no son metadatos de `MudFile`; son azúcar aplicado a declaraciones de primer nivel escritas directamente en ese archivo y compatibles con el metadato.

No se propagan a campos, componentes, participantes, miembros de familia, declaraciones importadas ni descendientes de otros archivos. La precedencia es:

```text
valor explícito del elemento > default de archivo > default del lenguaje
```

Un default de archivo no admite `:=`, `ValueBlock`, lecturas runtime ni propiedades intrínsecas. Su forma se mantiene separada de la asignación ordinaria de metadata de un propietario. `~summary`, `~description` y `~deprecated` pueden usarse como defaults. `~name`, `~plural`, `~abbreviation`, `~prefixes` y `~format` no pueden usarse como defaults de archivo por ser inherentemente individuales. Los metadatos de usuario son admitidos como defaults salvo restricción futura explícita de su definición.

### Texto y tooling

Las plantillas `Text` interpolan una expresión ordinaria y usan la conversión textual canónica de su valor. No existe una interpolación especial `anchor{...}`.

El LSP y el tooling oficial presentan preferentemente, cuando existan:

1. `~name` o `~identifier`;
2. firma estructural;
3. `~summary`;
4. `~description`;
5. advertencia de `~deprecated`.

## Consecuencias

- Los participantes anónimos dejan de ser sintaxis válida.
- Los participantes, campos y componentes anclados pasan a formar parte del grafo nominal como descriptores persistentes.
- El AST superficial conserva declaraciones y cuerpos de metadatos; tipado y elaboración distinguen propiedades intrínsecas de valores `Metadata` configurados. La codificación mecánica posterior de esa distinción todavía no está fijada.
- Las escrituras runtime a cualquier acceso `~` son errores estáticos.
- La visibilidad exterior se deriva del módulo propietario, su contrato `uses`, la categoría operacional y el cierre de tipos; el tooling presenta esa frontera, no la inventa.
- Las contribuciones `start with` de módulos y tests permanecen fuera de la superficie metadata-bearing.

## Verificación futura

1. Lectura postfix sin punto y rechazo de escritura runtime.
2. Preámbulo antes de contenido ordinario y rechazo de metadatos tardíos.
3. Metadatos almacenados y calculados de usuario.
4. Reflexión de `~metadata` sin propiedades intrínsecas.
5. Nombres obligatorios y anclas estables de `for`, `on` y `given` ante reordenación.
6. Metadata-body de campos, componentes y participantes, incluido grupo copiado.
7. Herencia de campos sin copia de descriptor ni metadatos.
8. Ausencia de metadatos en `start with`, cláusulas y cuerpos.
9. Defaults de archivo y precedencia explícito > archivo > lenguaje.
10. Rechazo de defaults calculados o individuales.
11. `~summary`, `~description` y `~deprecated` en elementos subordinados.
12. Colecciones y diccionarios con propiedades intrínsecas tipadas.
13. Narrowing categorial de declaraciones.
14. Eliminación completa de `anchor{...}`.

## Modificación vigente por D-096

La visibilidad exterior se deriva de módulo, categoría operacional y cierre de tipos. La reflexión cruzada de módulo solo es válida si su contrato garantiza que no puede devolver entidades invisibles; no se permite filtrar silenciosamente una colección reflectiva para ocultarlas. Tooling completo y reflexión disponible al código MUD siguen siendo superficies distintas.
