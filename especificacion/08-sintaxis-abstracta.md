---
title: Sintaxis abstracta superficial
aliases:
  - AST superficial
  - Surface AST
tags:
  - mud/especificacion
  - mud/sintaxis
status: propuesta
normative: true
depends-on:
  - 03-notacion
  - 05-texto-fuente
  - 06-lexico
  - 07-gramatica-concreta
  - sintaxis/cst-sin-perdidas
  - sintaxis/mud-surface-ast.asdl
questions:
  - Q-061
decisions:
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
---

# 08. Sintaxis abstracta superficial

## Estado y propósito

Este capítulo define el AST superficial normalizado de MUD 1.0. El AST conserva las distinciones sintácticas que afectan a fases posteriores y elimina puntuación, trivia, agrupaciones concretas y azúcares cuya interpretación no depende de resolución de nombres o tipos.

El esquema mecánico normativo es [[mud-surface-ast]]. Este capítulo explica sus invariantes y la frontera con otras representaciones.

El contrato semántico previo al IR vive en [[mud-resolved-ast]]. No es una instantánea tomada inmediatamente después de buscar nombres: se completa tras resolución nominal, tipado, elaboración y los análisis estáticos que alimentan su forma. Allí las referencias ya usan `AnchoredSymbol` o `LocalSymbol`, las uniones están elaboradas y las dependencias se expresan mediante aristas reconstruibles. La resolución nominal temprana puede construir símbolos y un grafo parcial sin introducir otro AST canónico intermedio.

## Cadena de representaciones

```text
texto fuente
→ tokens y trivia
→ CST sin pérdidas
→ validación sintáctica contextual
→ AST superficial normalizado
→ resolución nominal (símbolos + grafo parcial)
→ tipado, elaboración y análisis estático
→ AST semántico resuelto
→ IR
```

> [!rule] MUD-AST-001 — Responsabilidad superficial
> El AST superficial no contiene símbolos resueltos, anclas, tipos inferidos, efectos calculados ni decisiones que dependan de una declaración encontrada por nombre.

> [!rule] MUD-AST-002 — Normalización
> Dos formas concretas declaradas equivalentes por este capítulo producen la misma forma AST, salvo su procedencia.

## Relación con la CST

La CST conserva:

- Palabras clave.
- Delimitadores.
- Comas y terminadores.
- Paréntesis de agrupación.
- Comentarios y espacios.
- Escritura exacta de literales.
- Tokens ausentes o inesperados de recuperación.

El AST conserva:

- Categoría de declaración.
- Nombres escritos, todavía sin resolver.
- Orden fuente de listas semánticamente relevantes.
- Dominios, cardinalidades y permisos.
- Estructura de expresiones y efectos.
- Diferencias léxicas que tienen significado, como `and` frente a `&`.
- Procedencia suficiente para diagnósticos y transformaciones.

Un archivo con errores sintácticos puede tener CST sin producir un AST completo.

## Raíces

### `MudProject`

`MudProject` agrega los archivos que forman una compilación. No procede de una producción de un único archivo y no posee un `SourceSpan` único.

Sus archivos se serializan canónicamente por `relativePath` normalizada. Esa ordenación no modifica el orden interno de cada archivo ni atribuye significado semántico al orden físico de archivos.

### `MudFile`

Cada `MudFile` contiene:

- Metadatos físicos.
- Los defaults de metadatos de archivo en orden fuente.
- La lista de `using`.
- La lista de declaraciones de primer nivel.

Los metadatos de propietarios subordinados se almacenan directamente en sus constructores AST, no en una tabla lateral por `SourceSpan`. Los `using` se almacenan separados de las declaraciones porque la gramática exige que formen una cabecera. Ambos grupos conservan su orden fuente.

El path de MUD derivado de la ruta es metadato y no una declaración AST.

## Procedencia

Todos los nodos salvo `MudProject` poseen `SourceOrigin`:

```text
Written(span)
Synthetic(basis, reason)
```

`Written` indica una región concreta. `Synthetic` se usa para elementos realmente introducidos por normalización. Una cardinalidad omitida no se convierte en `[1..1]` en el AST superficial: conserva `OmittedCardinality` y la elaboración decide su forma según el propietario y el inicializador.

Las posiciones:

- Comienzan en cero.
- Usan offsets de bytes UTF-8.
- Tienen extremo final exclusivo.
- Cuentan columnas mediante valores escalares Unicode.

## Nombres

El AST usa wrappers distintos para evitar mezclar categorías antes de la resolución:

- `MudPath`.
- `QualifiedName`.
- `NominalName`.
- `FieldName`.
- `MemberName`.
- `RoleName`.
- `GivenName`.
- `ComponentName`.
- `VariableName`.
- `TypeRef`.
- `DeclarationRef`.

La capitalización se valida según el contexto, pero el texto original del identificador se conserva.

### Caminos con punto

Una secuencia de identificadores enlazados exclusivamente mediante `.` se representa como `DottedPathExpr`. La resolución posterior decidirá si sus segmentos denotan:

- Path de MUD y declaración.
- Declaración y miembro.
- Participante y campo.
- Una combinación de los anteriores.

Cuando la cadena contiene llamadas, índices u otros postfix, se usan `MemberAccessExpr`, `IndexExpr` y `CallExpr`.

## Flags

ASDL-MUD define:

```text
flag = Disabled | Enabled
```

Se usa para propiedades conceptualmente booleanas como:

- `isAbstract`.
- `isOrdered` de una `family`.
- Mutabilidad exterior.
- Capacidad sobre miembros.
- Unicidad.
- Ciclicidad de un intervalo.

No se representa mediante enteros ni strings.

## Metadatos en propietarios estables

Todo constructor superficial que represente directamente un propietario metadata-bearing conserva una secuencia `metadata_assignment* metadata`. Esto incluye declaraciones nominales admitidas por D-087, unidades, campos, componentes y participantes. Los cuerpos concretos solo delimitan el preámbulo; no se crea un `MetadataAttachment` lateral ni se usa el `SourceSpan` como identidad del propietario.

Una cabecera agrupada de participantes se normaliza a varios descriptores y copia la misma secuencia de metadatos a cada uno. `GlobalStartDecl` y el `start with` interno de un test no reciben secuencia propia.

## Declaraciones de `thing`

Una `ThingDecl` contiene:

- `isAbstract`.
- Nombre nominal fuente.
- Antecesores directos en orden fuente.
- Asignaciones de metadatos como `~name`.
- Campos.

El AST no ordena alfabéticamente los antecesores. Que su orden carezca de prioridad semántica no elimina su valor como procedencia, formato y diagnóstico.

El AST superficial conserva un `Thing` escrito explícitamente en `as`. La resolución posterior lo normaliza como redundancia de la raíz efectiva y el tooling ofrece retirarlo; el formatter no lo elimina silenciosamente.

El preámbulo contiene declaraciones de metadatos y el resto del cuerpo contiene campos. `metadata_assignment` distingue `StoredMetadataAssignment` y `CalculatedMetadataAssignment`; conserva únicamente información escrita o normalizada sintácticamente, sin fabricar propiedades intrínsecas. Los metadatos se resuelven y tipan por categoría de propietario y no se convierten en campos ordinarios.

## Campos

### Campo almacenado

```text
StoredFieldDecl(
    collectionMutable,
    name,
    shape,
    defaultValue?,
    metadata*
)
```

`ValueShape` contiene un `TypeExpr` normalizado con alternativas nominales, dominio opcional por alternativa y una única especificación de colección exterior.

### Campo calculado

```text
CalculatedFieldDecl(name, shape?, value, metadata*)
```

No contiene mutabilidad exterior. `shape` ausente delega tipo, dominio y colección a la inferencia. `ExplicitDerivedShape` conserva un `TypeExpr` completo; `InferredDerivedShape` conserva un dominio o colección escritos sin inventar un tipo superficial. La elaboración combina esas restricciones con el tipo inferido.

### Campos públicos

`PublicFieldDecl(name, shape?, value, metadata*)` comparte la forma calculada, pero conserva una categoría propia porque pertenece a la interfaz de `look` y `message`.

## Forma de valor

`ValueShape` es una estructura reutilizada por:

- Campos almacenados.
- Componentes de alias.
- Datos almacenados de `family`.
- Participantes `for`.

Contiene la expresión de tipo completa, pero no predeterminado ni mutabilidad exterior. Esos aspectos pertenecen al contexto propietario.

`GivenDecl` reutiliza directamente `TypeExpr`. Su inmutabilidad es un invariante de construcción del AST: la validación previa recorre el tipo completo y rechaza cualquier `CollectionSpec` con `elementsMutable = Enabled`, incluso si aparece dentro de un producto o diccionario. Así un `given` puede usar toda la forma de tipos sin transportar capacidad de escritura.

## Tipos

### Uniones nominales

`TypeExpr` contiene una secuencia no vacía de `TypeAlternative` y una sola especificación de colección exterior. El AST superficial aplana agrupaciones, elimina duplicados idénticos y conserva el orden de la primera aparición para procedencia y formato. La unión elaborada es asociativa, conmutativa e idempotente, pero no elimina una alternativa por inclusión de dominio. Los paréntesis redundantes no sobreviven.

Cada `TypeAlternative` contiene un `DeclaredType` y un `DomainExpr` opcional. `SteppedDomain` conserva por separado intervalo y paso; los demás dominios superficiales usan `ExpressionDomain` hasta su elaboración semántica.

### Tipo nominal

```text
NamedType(TypeRef)
```

Incluye tanto tipos incorporados como tipos declarados por el programa. Que un nombre sea `Nat`, una `thing`, una `family`, un alias o una magnitud se decide después.

### Diccionario

```text
DictionaryType(keyType, valueTypeExpression)
```

El valor conserva su `TypeExpr`, por lo que puede contener dominio y colección propios. La colección escrita después del diccionario completo pertenece al `TypeExpr` exterior.

Los paréntesis exigidos por la gramática para un diccionario anidado no sobreviven al AST.

Las ramas de un diccionario funcional permanecen nodos de valor en el AST superficial y no reciben `AnchoredSymbol` ni ancla sintética. La resolución conserva su orden fuente y deriva una `decision_branch_key` local al diccionario a partir del selector normalizado; esa clave sirve para reconstrucción y dependencias internas, no para resolución nominal ni metadatos.

## Colecciones

La forma normalizada es:

```text
CollectionSpec(
    cardinality,
    isUnique,
    order,
    elementsMutable
)
```

El orden es una suma:

```text
Unordered
InsertionOrdered
OrderedBy(path)
```

No se usa una combinación de booleano más ruta opcional porque permitiría estados inválidos.

### Cardinalidad

`CollectionSpec` conserva la procedencia de la cardinalidad. Si no se escribe ninguna, `cardinalityOrigin = OmittedCardinality`: el AST superficial no sintetiza `[1..1]` ni infiere todavía una cardinalidad efectiva. La elaboración posterior la determina según el propietario y, cuando corresponda, su inicializador.

Las formas explícitas se normalizan así:

- `[a]` → `[a..a]`.
- `[*]` → `[*..*]`.
- `[a..b]` conserva ambos extremos.

Un extremo `*` escrito permanece como `EffectiveCardinality` en el AST superficial. La elaboración posterior aplica su valor efectivo según el lado y el contexto.

### Modificadores duplicados

La CST puede representar `unique unique`; la validación previa al AST lo rechaza. El AST solo contiene una propiedad `isUnique`.

## Aliases

`AliasDecl` contiene:

- Nombre nominal.
- Secuencia fuente de antecesores directos todavía no resueltos.
- Definición local opcional.
- Metadatos del alias en orden fuente.

La definición local es una de:

```text
AliasRepresentation(TypeExpr)
StructuralAlias(AliasMember*)
```

Los miembros estructurales pueden ser:

```text
AliasComponentDecl(AliasComponent)
AliasCalculatedFieldDecl(nombre, forma?, expresión)
AliasDefaultOverride(nombre, valor)
```

La ausencia de definición se conserva cuando existe `as`; la validación previa al AST rechaza `alias A` sin antecesores ni definición. Un cuerpo vacío explícito y la omisión de cuerpo son formas concretas distintas, pero ambos producen una secuencia local vacía.

Un componente estructural:

- No admite mutabilidad exterior.
- Puede contener capacidad interior `[mut]` en su colección.
- Puede tener dominio y predeterminado estático.

Un campo derivado no posee carga asignable, puede declarar forma y capacidad interior y se recalcula desde su expresión. Una sobrescritura local solo puede dirigirse a un componente almacenado heredado y solo reemplaza su predeterminado.

Los literales estructurales siguen siendo contextuales. `PositionalStructuralLiteralExpr` exige al menos dos valores y `NamedStructuralLiteralExpr` conserva uno o más componentes nombrados; no se selecciona todavía un alias concreto. Por tanto, los miembros del alias solo quedan disponibles después de elaboración contextual o de una conversión nominal explícita.

Cuando la elaboración recibe un tipo esperado que selecciona un único alias compatible, el AST semántico resuelto conserva una `ContextualNominalConstructionExpr` alrededor del literal. Esta forma no equivale a `ConversionExpr`: esta última representa `to` escrito sobre un valor que ya tenía tipo. La construcción contextual solo puede materializar un literal cuya identidad nominal dependía todavía del contexto; no convierte silenciosamente variables, accesos, llamadas ni otras expresiones ya tipadas.

## Familias

`FamilyDecl` contiene:

- Flag de orden por declaración.
- Metadatos de la family en orden fuente.
- Datos almacenados o calculados.
- Miembros.

Los datos asociados no admiten mutabilidad exterior. El dato almacenado conserva `metadata_assignment* metadata` junto a su forma y predeterminado. El dato calculado conserva provisionalmente `derived_value_shape? shape`, su expresión y `metadata_assignment* metadata`; Q-061 decidirá si esa forma debe restringirse al tipo opcional descrito por D-038.

Cada declaración de dato asociado es un propietario metadata-bearing estable y se elabora como descriptor `Field` subordinado a la `family`, con `FieldKind.Stored` o `FieldKind.Calculated`. La proyección `member.data` es un valor, no una copia del descriptor. Por tanto, los metadatos pertenecen al dato declarado una sola vez y no se duplican por miembro.

Cada `FamilyMember` conserva asignaciones de metadatos, como `~name`, y asignaciones a datos almacenados. `FamilyDataAssignment` permanece deliberadamente sin campo `metadata`: una sobrescritura de miembro solo selecciona el valor efectivo del slot almacenado y no crea un propietario metadata-bearing. Un bloque omitido produce ambas secuencias vacías.

## Magnitudes

Existen constructores separados:

- `BaseMagnitudeDecl`.
- `DerivedMagnitudeDecl`.
- `PointMagnitudeDecl`.

La representación numérica opcional se almacena mediante `DeclaredType`, no mediante una enumeración cerrada. Una regla estática posterior exige que el tipo resuelto sea una representación numérica permitida.

En `BaseMagnitudeDecl`, `root_unit` ausente representa deliberadamente una magnitud base sin unidades; no es un nodo incompleto ni solicita una unidad sintética posterior. En ese caso `units` debe estar vacío. La dimensión nominal se incorpora durante la elaboración y no se deduce de la presencia de una forma de unidad.

### Dimensiones

Las expresiones dimensionales usan nodos propios y no expresiones aritméticas generales:

```text
DimensionProduct(first, links)
DimensionLink(MultiplyDimension | DivideDimension, term)
```

### Unidades

Una unidad raíz y una alternativa son variantes diferentes porque la segunda posee equivalencia cuantitativa:

```text
RootUnitDecl(name, metadata*)
AlternativeUnitDecl(name, equivalence, metadata*)
```

No existe `UnitProperties` ni `PrefixPolicy` en el AST superficial. El cuerpo de unidad es un preámbulo general de `metadata_assignment` y cada declaración se conserva sin convertirla a una estructura paralela.

`~prefixes` es metadata almacenada de tipo `Prefix [* unique]` cuyo default de lenguaje es `empty`. `empty`, `all` y `[kilo, milli]` permanecen expresiones MUD ordinarias en el AST; la resolución posterior identifica `kilo`, `milli`, etc. como valores incorporados de `Prefix`. La ausencia de `~plural` o `~abbreviation` también se conserva, sin sintetizar presentación en esta fase.

## Participantes

### `for`

`ForParticipant` contiene:

- Mutabilidad exterior.
- Nombre obligatorio.
- `ValueShape` completo.
- Metadatos del descriptor en orden fuente.

No admite predeterminado.

### `on`

Hay dos variantes:

```text
DirectOnParticipant(name, type, elementsMutable, metadata*)
RelatedOnParticipant(name, refinement?, source, elementsMutable, metadata*)
```

Las referencias entre participantes, incluidas referencias adelantadas y ciclos, se conservan como expresiones. Su resolución conjunta no pertenece al AST superficial.

### `given`

`GivenDecl` contiene:

- Nombre obligatorio.
- Forma de valor de solo lectura.
- Predeterminado opcional.
- Metadatos del descriptor en orden fuente.

No puede representar mutabilidad exterior ni interior.

### Cláusulas

`ForClause`, `OnClause` y `GivenClause` son nodos propios. Una cláusula omitida es ausencia, no una cláusula sintética vacía.

## Reglas

Las tres clases tienen constructores distintos:

- `BooleanRuleDecl`.
- `ReactiveRuleDecl`.
- `AlwaysRuleDecl`.

Una regla reactiva almacena:

- Activador `when` como `ExpressionBlock` con contrato temporal.
- Guardia `if` opcional como `ExpressionBlock` con contrato booleano.
- Bloque de efectos.

`changes` es un nodo de expresión, no una variante separada de cláusula `when`.

En una regla `always`, `InvariantBodySyntax` produce exclusivamente el `ExpressionBlock`; el `DiagnosticTailSyntax` posterior a la llave de cierre produce el campo `diagnostic` de `AlwaysRuleDecl`. La regla puede omitirlo y el AST conserva `diagnostic = absent`. El warning y el diagnóstico predeterminado pertenecen a validación y elaboración.

## Bloques de expresión

La estructura común es `ExpressionBlock(locals, result)`. `locals` conserva las declaraciones `:=` y `result` la única expresión final. El nodo no fija el tipo del resultado: el propietario aplica su contrato booleano, temporal, agregable u ordenable. La forma breve normaliza a `ExpressionBlock([], expression)`. Las locales son puras, inmutables, secuenciales y sin referencias adelantadas, ciclos, redeclaración ni sombreado. El `otherwise` asociado no forma parte del bloque.

## Acciones

El AST superficial usa un único `ActionDecl`.

La clasificación como elemental o compuesta requiere resolver los `ActionCallCandidateEffect`; por ello pertenece al AST resuelto. La forma superficial no inventa una clasificación basada únicamente en la apariencia de un `postfix-expression`.

Una acción contiene:

- Participantes `for` opcionales.
- `given` opcionales.
- Guardia booleana opcional y diagnóstico.
- Bloque de efectos.
- Postcondición booleana `after` opcional y diagnóstico.

## `look` y `message`

`LookDecl` conserva participantes `for` y propiedades públicas.

`MessageDecl` conserva participantes `on`, activador booleano, guardia booleana opcional y propiedades públicas.

No se reducen a reglas o acciones genéricas porque sus contratos posteriores son distintos.

## Tests

`TestDecl` contiene:

- Conjunto inicial local.
- Bloque de efectos.
- Un `TestAfterBlock` con declaraciones locales iniciales y una secuencia no vacía de aserciones.

La forma `after expr` produce un bloque sin locales y una aserción. En la forma `after { ... }`, todas las declaraciones locales preceden a la primera aserción.

`start with` global y local comparten `StartSet`, pero solo el primero está envuelto en `GlobalStartDecl`.

## Bloques de efectos

Un `then` con un único efecto se normaliza a `EffectBlock` con `leadingLocals` vacío, ese efecto como `firstEffect`, `remainingStatements` vacío y diagnóstico de fallo opcional.

El bloque conserva por separado las declaraciones locales anteriores al primer efecto, el primer efecto obligatorio y las sentencias restantes. Estas últimas pueden ser `EffectStatement` o `LocalValueStatement`.

El AST no presupone ejecución secuencial o simultánea distinta de la definida por capítulos posteriores; solo conserva la estructura declarada.

## Efectos

Hay nodos propios para:

- Asignación.
- Adición de valor.
- Adición de campo.
- Eliminación.
- Creación.
- Destrucción.
- Candidato a llamada de acción.
- Iteración `for each`.

### Valores separados por comas

`value-expression` con varios elementos se normaliza a:

```text
CollectionLiteralExpr(elements)
```

La forma de un solo elemento permanece como esa expresión, no como una colección sintética.

### Asignables

`AssignableExpr` conserva una base y sufijos de miembro o índice. La comprobación de que la base designa un lugar escribible pertenece a resolución, tipos y efectos.

### Iteración `for each`

`ForEachEffect(binding, source, step?, filter?, body)` conserva la expresión `by`, el filtro como `ExpressionBlock` y normaliza efecto breve/bloque posterior a `:` a `EffectBlock`. Dirección, paso predeterminado, compatibilidad, orden del filtro y paso cero pertenecen a elaboración.

## Expresiones

### Operadores

El AST conserva operadores léxicamente distintos cuando MUD les atribuye contratos diferentes:

- `WordAnd` frente a `SymbolAnd`.
- `WordOr` frente a `SymbolOr`.
- `WordXor` frente a `SymbolXor`.

Esto permite que `when` distinga composición temporal mediante palabras de booleanos ordinarios mediante símbolos.

### Comparaciones

Una cadena como:

```mud
0 <= x < 10
```

se representa mediante `ComparisonChainExpr`, no como asociaciones binarias arbitrarias.

Las comparaciones no encadenables producen una única arista en la cadena o un nodo equivalente validado.

`is not` produce `IsNotRelation`; no se pierde como un `not` exterior porque el estrechamiento nominal necesita reconocer directamente la prueba negativa.

### Selección y cuantificadores

`SelectionExpr(binding, source, step?, predicate)` conserva `step?` y normaliza el predicado a `ExpressionBlock`. `QuantifierExpr(kind, variable, source, step?, body)` hace lo mismo para los seis cuantificadores/agregadores. El AST no decide el contrato de tipo de `body`.

### Conversiones

`to Type` y `in unit` producen `ConversionExpr` con destinos distintos. La barrera postfix de la gramática ya ha decidido su agrupación, pero no la compatibilidad.

### Postfix y llamadas

`MemberAccessExpr`, `IndexExpr` y `CallExpr` se construyen de izquierda a derecha.

`CallExpr` conserva:

- La expresión llamada.
- El prefijo de argumentos posicionales.
- El sufijo de argumentos nombrados.

La separación impide representar un posicional posterior a un nombrado.

La posible interpretación de:

```mud
(attacker, defender).CanAttack()
```

como varios receptores o como un único valor estructural queda pendiente de resolución de firma. El AST superficial conserva la forma estructural y el encadenamiento postfix.

### `Rand`

`Rand(expr)` posee `RandomExpr`; no es un tipo ni una llamada ordinaria.

### Selección y `take`

`binding in source [by step]: predicate` posee `SelectionExpr`. Conserva la vinculación, la fuente, el paso opcional y el predicado como `ExpressionBlock` sin materializar la colección resultante. La vinculación solo introduce nombres dentro del predicado.

`take amount from source` posee `TakeExpr`. El AST superficial no decide si la fuente es ordenada, texto, diccionario, dominio enumerable o una colección sin orden; esa resolución determina después si se toma un prefijo canónico o una muestra reproducible.

La composición de ambas formas es estructural. `take n from player in players: condition` contiene un `SelectionExpr` como fuente de `TakeExpr`; `player in take m from players: condition` contiene un `TakeExpr` como fuente de `SelectionExpr`.

### `all`

El literal contextual `all` produce `AllLiteral`. Su dominio y carácter estático o dinámico se determinan durante el tipado; el AST superficial no enumera sus valores.

### Cuantificadores

`exists`, `forall`, `count`, `sum`, `min` y `max` comparten `QuantifierExpr` con un enum propio, un `step?` opcional y un `ExpressionBlock` como cuerpo.

### Operadores de colección

`--` produce `CollectionDifference`, distinto de `Subtract`. Las actualizaciones `|=`, `&=`, `^=` y `--=` producen respectivamente `UnionAssign`, `IntersectionAssign`, `SymmetricDifferenceAssign` y `DifferenceAssign`; no se reducen a `Assign` porque la clase de actualización participa en la consolidación concurrente.

## Plantillas `Text`

Una plantilla es una secuencia ordenada de:

- `TextFragment` con texto decodificado.
- `ValueInterpolation`.

El AST no conserva:

- Comilla final explícita o implícita.
- Margen físico del literal multilínea.
- Escapes usados para obtener el mismo carácter.

La CST sí los conserva.

La escritura ordinaria entre comillas dobles siempre llega al AST superficial como `TextTemplateExpr`. La elaboración posterior puede convertirla en un valor `Char` cuando el contexto exige `Char`, no contiene interpolaciones y su valor decodificado es exactamente un escalar Unicode. Por ello el AST superficial no posee un constructor léxico separado `CharLiteral`.

`NumericTextFormat` representa anchuras enteras y fraccionarias opcionales sin conservar los dos puntos concretos.

Dentro del `format` de una magnitud de punto, `unidad from contenedor` produce `ContextualPointComponentExpr`; no se inventa un receptor explícito que no aparece en la fuente.

## Intervalos

Todas las formas se normalizan a:

```text
Interval(lower, lowerBoundary, upper, upperBoundary, sharedUnit?)
EmptyInterval(sharedUnit?)
```

Normalizaciones:

- `a..b` → intervalo cerrado.
- `[a]` → intervalo cerrado con ambos extremos iguales.
- Formas con unidad compartida → unidad en `sharedUnit`.
- `[] unit` → `EmptyInterval(unit)`.
- `[a..b) cycle` → `CyclicPointDomain` sobre el intervalo semiabierto declarado.

Los paréntesis y corchetes solo sobreviven como `OpenBoundary` o `ClosedBoundary`.

Los extremos `*` permanecen como `EffectiveIntervalBound` hasta elaboración.

## Cantidades y unidades

`QuantityValueExpr` contiene un literal numérico y una `UnitProduct`.

La expresión de unidad y la de dimensión poseen árboles separados aunque ambas usen `*`, `/` y paréntesis en la sintaxis concreta.

Una forma `UNIT_FORM` se conserva como texto fuente contextual. Su resolución contra el catálogo pertenece a fases posteriores.

La ausencia de espacio entre número y unidad no altera el AST. `3m` y `3 m` producen la misma cantidad; la forma fuente exacta permanece disponible en la CST y el formateador emite la segunda.

## Literales numéricos

El AST conserva una escritura canónica del valor, no necesariamente el lexema exacto. Por ejemplo:

```mud
1_000
1000
```

pueden producir el mismo `ExactNumberLiteral("1000")`.

La exactitud matemática de `Num` y la interpretación binary64 de `Rum` se elaboran después.

## Orden preservado y orden canónico

Se conserva el orden fuente de:

- Declaraciones dentro de un archivo.
- Antecesores.
- Campos y componentes.
- Datos y miembros de familias.
- Participantes y `given`.
- Argumentos.
- Efectos y aserciones.

Solo `MudProject` define una serialización canónica de archivos por ruta. Ninguna otra lista se ordena automáticamente en el AST superficial salvo que una normalización concreta lo declare.

## Estados inválidos excluidos

Un AST superficial conforme no puede contener:

- Cardinalidad ausente.
- Dos modificadores `unique`.
- Dos órdenes de colección.
- `given` mutable.
- Declaraciones de metadatos duplicadas en una misma unidad.
- Acción ya clasificada elemental o compuesta sin resolución.
- Símbolo o ancla resueltos.
- Tipo inferido insertado como si se hubiera escrito.
- Comentarios ordinarios.
- Tokens de recuperación.

## Serialización estructural

La serialización canónica de AST:

1. Ordena archivos por ruta normalizada.
2. Conserva el orden de las secuencias internas.
3. Usa los nombres de constructores ASDL.
4. Omite trivia y puntuación.
5. Incluye `SourceOrigin` salvo en vistas de comparación que lo excluyan expresamente.
6. Serializa enums por su nombre canónico.

Esta serialización sirve para snapshots, caché y tooling. No es código MUD y no sustituye al pretty-printer.

## Cobertura

Toda producción de [[mud]] debe aparecer en:

- `mud-syntax-kinds.yaml`.
- `cobertura-sintactica.yaml`.

La cobertura declara si la producción:

- Construye un nodo.
- Se normaliza.
- Se pliega en el padre.
- Se descarta como layout.
- Queda contextual hasta resolución.

`validate_syntax_model.py` comprueba esa correspondencia.

## Conformidad

Una implementación conforme del AST superficial debe:

1. Producir constructores equivalentes a `mud-surface-ast.asdl`.
2. Aplicar todas las normalizaciones de [[cst-a-ast-superficial]].
3. Rechazar antes del AST los estados excluidos.
4. Conservar procedencia.
5. No anticipar resolución, tipado o IR.
6. Mantener las diferencias de operadores exigidas.
7. Permitir generar una forma estructural estable para pruebas.

## Normalización de cuerpos vacíos de `thing`

`thing A`, `thing A;` y `thing A {}` producen el mismo `ThingDecl` con cero campos y sin sobrescritura intrínseca. La CST conserva el cuerpo y el terminador escritos; el AST no fabrica un nodo de cuerpo vacío.


## Ejemplos fuente → AST

```mud
A -> B -> C
```

se normaliza como `ExactDictionaryType(A, ExactDictionaryType(B, C))`.

```mud
value iis not PersonId
```

produce `ExactTypeTestExpr(value, PersonId, Enabled)`.

```mud
"{value~anchor}"
```

produce `TextTemplateExpr([ValueInterpolation(MetadataAccessExpr(value, anchor))])`.

```mud
values: Nat = [1, 2, 3]
```

conserva `OmittedCardinality` en el AST superficial y adquiere `[3]` únicamente durante la elaboración del campo.

```mud
start with { things { all } rules { empty } }
```

produce `StartSet(things=[AllLiteral], rules=[EmptyLiteral])`.

## Tipos producto y tipos de diccionario

`PositionalProductType` y `NamedProductType` conservan los componentes de los productos estructurales anónimos. `ExactDictionaryType` y `DecisionDictionaryType` representan respectivamente los diccionarios exactos y los diccionarios funcionales definidos por ramas. El nombre mecánico `Decision` se conserva por estabilidad del esquema.

Una cadena se pliega por la derecha:

```text
A -> B [2] --> C [3 ordered]
```

produce conceptualmente:

```text
ExactDictionaryType(
    A,
    DecisionDictionaryType(B, C, FirstMatch, [3]),
    [2]
)
```

La validación posterior a la resolución rechaza una flecha como alternativa parcial de una unión, incluso cuando aparece a través de un alias.

## Cardinalidad omitida

`CollectionSpec` conserva `WrittenCardinality` u `OmittedCardinality`. Para:

```mud
values: Nat = [1, 2, 3]
```

el AST superficial conserva la omisión. La elaboración de un campo almacenado inmutable infiere después `[3]` y registra `InferredFromInitializer`; no fabrica esa información durante el parsing.

## Comparaciones nominales

`is` continúa representándose mediante la comparación nominal transitiva. `iis` produce un nodo propio porque su narrowing es distinto:

```text
ExactTypeTestExpr(value, PersonId, negated=Disabled)
ExactTypeTestExpr(value, PersonId, negated=Enabled)
```

La segunda forma corresponde a `value iis not PersonId`. La resolución exige que el operando derecho sea un tipo nominal.

## Operaciones conjuntistas de diccionarios

El AST superficial conserva `|`, `&`, `--` y `^` como `BinaryExpr`, porque la categoría exacta depende de los tipos resueltos. La elaboración los especializa como operación de diccionario exacto o funcional. Una operación funcional conserva sus operandos; no crea una lista nueva de ramas.

## Metadatos, texto y activación

`element~metadata` produce siempre `MetadataAccessExpr`. No existe `MetadataSuffix` asignable: `AssignableExpr` solo conserva `MemberSuffix` e `IndexSuffix`, de modo que ningún acceso `~` puede ser destino de un efecto. El AST superficial tampoco decide si la propiedad existe para el receptor; D-092 difiere esa comprobación hasta que la categoría estática del receptor ha sido resuelta. Toda interpolación produce `ValueInterpolation`, incluida:

```mud
"{value~anchor}"
```

No existe `AnchorInterpolation`. `start with` produce `StartSet(things, rules)` y mantiene ambas contribuciones separadas. `ActionDecl` conserva `PublicAction` o `Subaction`.
