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
questions: []
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
---

# 08. Sintaxis abstracta superficial

## Estado y propósito

Este capítulo define el AST superficial normalizado de MUD 1.0. El AST conserva las distinciones sintácticas que afectan a fases posteriores y elimina puntuación, trivia, agrupaciones concretas y azúcares cuya interpretación no depende de resolución de nombres o tipos.

El esquema mecánico normativo es [[mud-surface-ast]]. Este capítulo explica sus invariantes y la frontera con otras representaciones.

El contrato de la fase posterior vive en [[mud-resolved-ast]]. Allí las referencias se sustituyen por `AnchoredSymbol` o `LocalSymbol`, las uniones quedan normalizadas y el grafo nominal se expresa mediante aristas reconstruibles.

## Cadena de representaciones

```text
texto fuente
→ tokens y trivia
→ CST sin pérdidas
→ validación sintáctica contextual
→ AST superficial normalizado
→ resolución de nombres
→ AST resuelto
→ tipado y elaboración
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
- La lista de `using`.
- La lista de declaraciones de primer nivel.

Los `using` se almacenan separados de las declaraciones porque la gramática exige que formen una cabecera. Ambos grupos conservan su orden fuente.

El path de MUD derivado de la ruta es metadato y no una declaración AST.

## Procedencia

Todos los nodos salvo `MudProject` poseen `SourceOrigin`:

```text
Written(span)
Synthetic(basis, reason)
```

`Written` indica una región concreta. `Synthetic` se usa para elementos introducidos por normalización, como una cardinalidad omitida que se convierte en `[1..1]`.

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

## Declaraciones de `thing`

Una `ThingDecl` contiene:

- `isAbstract`.
- Nombre.
- Antecesores directos en orden fuente.
- Sobrescritura opcional del `name` intrínseco, ya decodificada.
- Campos.

El AST no ordena alfabéticamente los antecesores. Que su orden carezca de prioridad semántica no elimina su valor como procedencia, formato y diagnóstico.

El AST superficial conserva un `Thing` escrito explícitamente en `as`. La resolución posterior lo normaliza como redundancia de la raíz efectiva y el tooling ofrece retirarlo; el formatter no lo elimina silenciosamente.

El cuerpo contiene como máximo una sobrescritura `name = "literal"` y los campos. El `name` intrínseco no se convierte en campo, no se hereda y no forma parte del store.

## Campos

### Campo almacenado

```text
StoredFieldDecl(
    collectionMutable,
    name,
    shape,
    defaultValue?
)
```

`ValueShape` contiene un `TypeExpr` normalizado con alternativas nominales, dominio opcional por alternativa y una única especificación de colección exterior.

### Campo calculado

```text
CalculatedFieldDecl(name, shape?, value)
```

No contiene mutabilidad exterior. `shape` ausente delega tipo, dominio y colección a la inferencia. `ExplicitDerivedShape` conserva un `TypeExpr` completo; `InferredDerivedShape` conserva un dominio o colección escritos sin inventar un tipo superficial. La elaboración combina esas restricciones con el tipo inferido.

### Campos públicos

`PublicFieldDecl` comparte la forma calculada, pero conserva una categoría propia porque pertenece a la interfaz de `look` y `message`.

## Forma de valor

`ValueShape` es una estructura reutilizada por:

- Campos almacenados.
- Componentes de alias.
- Datos almacenados de `family`.
- Participantes `for`.

Contiene la expresión de tipo completa, pero no predeterminado ni mutabilidad exterior. Esos aspectos pertenecen al contexto propietario.

`GivenDecl` usa `ReadonlyValueShape`, que no puede representar capacidad interior `mut`.

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

Toda colección posee una cardinalidad explícita en el AST:

- Omisión → `[1..1]` sintético.
- `[a]` → `[a..a]`.
- `[*]` → `[*..*]`.
- `[a..b]` conserva ambos extremos.

Un extremo `*` permanece como `EffectiveCardinality` en el AST superficial. La elaboración posterior aplica su valor efectivo según el lado y el contexto.

### Modificadores duplicados

La CST puede representar `unique unique`; la validación previa al AST lo rechaza. El AST solo contiene una propiedad `isUnique`.

## Aliases

`AliasDecl` tiene dos cuerpos:

```text
AliasOf(TypeExpr)
StructuralAlias(AliasComponent*)
```

Un componente estructural:

- No admite mutabilidad exterior.
- Puede contener capacidad interior `[mut]` en su colección.
- Puede tener dominio y predeterminado estático.
- No puede ser calculado.

Los literales estructurales siguen siendo contextuales. `PositionalStructuralLiteralExpr` exige al menos dos valores y `NamedStructuralLiteralExpr` conserva uno o más componentes nombrados; no se selecciona todavía un alias concreto.

## Familias

`FamilyDecl` contiene:

- Flag de orden por declaración.
- Datos almacenados o calculados.
- Miembros.

Los datos asociados no admiten mutabilidad exterior. Su colección puede conceder capacidad interior sobre `thing` contenidas.

Cada `FamilyMember` conserva una sobrescritura opcional del `name` intrínseco y asignaciones a datos almacenados. Un bloque omitido produce sobrescritura ausente y secuencia vacía.

## Magnitudes

Existen constructores separados:

- `BaseMagnitudeDecl`.
- `DerivedMagnitudeDecl`.
- `PointMagnitudeDecl`.

La representación numérica opcional se almacena mediante `DeclaredType`, no mediante una enumeración cerrada. Una regla estática posterior exige que el tipo resuelto sea una representación numérica permitida.

### Dimensiones

Las expresiones dimensionales usan nodos propios y no expresiones aritméticas generales:

```text
DimensionProduct(first, links)
DimensionLink(MultiplyDimension | DivideDimension, term)
```

### Unidades

Una unidad raíz y una alternativa son variantes diferentes porque la segunda posee equivalencia cuantitativa.

Las propiedades se normalizan a una estructura fija:

- Identificador `lowerCamel` obligatorio en la declaración.
- `name` opcional.
- `plural` opcional.
- `abbreviation` opcional.
- Política de prefijos.

La ausencia de `plural` se conserva; no se sintetiza en el AST superficial.

La política de prefijos es:

- Propiedad omitida → `NoPrefixes`.
- `prefixes = empty` → `NoPrefixes`.
- `prefixes = all` → `AllPrefixes`.
- `prefixes = [p1, ...]` → `SelectedPrefixes`.

Las propiedades duplicadas se rechazan antes de construir el AST. Un cuerpo vacío es válido y produce metadatos ausentes con `NoPrefixes`.

## Participantes

### `for`

`ForParticipant` contiene:

- Mutabilidad exterior.
- Nombre opcional.
- `ValueShape` completo.

No admite predeterminado.

### `on`

Hay dos variantes:

```text
DirectOnParticipant(name?, type, elementsMutable)
RelatedOnParticipant(name, refinement?, source, elementsMutable)
```

Las referencias entre participantes, incluidas referencias adelantadas y ciclos, se conservan como expresiones. Su resolución conjunta no pertenece al AST superficial.

### `given`

`GivenDecl` contiene:

- Nombre obligatorio.
- Forma de valor de solo lectura.
- Predeterminado opcional.

No puede representar mutabilidad exterior ni interior.

### Cláusulas

`ForClause`, `OnClause` y `GivenClause` son nodos propios. Una cláusula omitida es ausencia, no una cláusula sintética vacía.

## Reglas

Las tres clases tienen constructores distintos:

- `BooleanRuleDecl`.
- `ReactiveRuleDecl`.
- `AlwaysRuleDecl`.

Una regla reactiva almacena:

- Activador `when` como bloque booleano.
- Guardia `if` opcional como bloque booleano.
- Bloque de efectos.

`changes` es un nodo de expresión, no una variante separada de cláusula `when`.

En una regla `always`, `InvariantBodySyntax` produce exclusivamente el `BooleanBlock`; el `DiagnosticTailSyntax` posterior a la llave de cierre produce el campo `diagnostic` de `AlwaysRuleDecl`. La regla puede omitirlo y el AST conserva `diagnostic = absent`. El warning y el diagnóstico predeterminado pertenecen a validación y elaboración.

## Bloques booleanos

Las condiciones de reglas booleanas, `when`, `if`, `always` y `after` se normalizan como:

```text
BooleanBlock(locals, result)
```

`locals` conserva en orden las declaraciones con `:=`; `result` es la única expresión final. Debe satisfacer el contrato booleano del propietario o, en `when`, el contrato temporal de activador. La forma breve posee una secuencia local vacía. El `otherwise` asociado no forma parte de `BooleanBlock`, pero su expresión puede resolver los nombres locales declarados por este.

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

`binding in source: predicate` posee `SelectionExpr`. Conserva la vinculación, la fuente y el predicado sin materializar la colección resultante. La vinculación solo introduce nombres dentro del predicado.

`take amount from source` posee `TakeExpr`. El AST superficial no decide si la fuente es ordenada, texto, diccionario, dominio enumerable o una colección sin orden; esa resolución determina después si se toma un prefijo canónico o una muestra reproducible.

La composición de ambas formas es estructural. `take n from player in players: condition` contiene un `SelectionExpr` como fuente de `TakeExpr`; `player in take m from players: condition` contiene un `TakeExpr` como fuente de `SelectionExpr`.

### `all`

El literal contextual `all` produce `AllLiteral`. Su dominio y carácter estático o dinámico se determinan durante el tipado; el AST superficial no enumera sus valores.

### Cuantificadores

`exists`, `forall`, `count`, `sum`, `min` y `max` comparten `QuantifierExpr` con un enum propio.

### Operadores de colección

`--` produce `CollectionDifference`, distinto de `Subtract`. Las actualizaciones `|=`, `&=`, `^=` y `--=` producen respectivamente `UnionAssign`, `IntersectionAssign`, `SymmetricDifferenceAssign` y `DifferenceAssign`; no se reducen a `Assign` porque la clase de actualización participa en la consolidación concurrente.

## Plantillas `Text`

Una plantilla es una secuencia ordenada de:

- `TextFragment` con texto decodificado.
- `ValueInterpolation`.
- `AnchorInterpolation`.

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
Interval(lower, lowerBoundary, upper, upperBoundary, sharedUnit?, cyclic)
EmptyInterval(sharedUnit?)
```

Normalizaciones:

- `a..b` → intervalo cerrado.
- `[a]` → intervalo cerrado con ambos extremos iguales.
- Formas con unidad compartida → unidad en `sharedUnit`.
- `[] unit` → `EmptyInterval(unit)`.
- `[a..b cycle)` → intervalo cíclico con límites declarados.

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
- Unidad con propiedades duplicadas.
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
