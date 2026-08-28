---
title: Transformación de CST a AST superficial
aliases:
  - CST a AST
  - Normalización sintáctica
tags:
  - mud/especificacion
  - mud/sintaxis
status: propuesta
normative: true
depends-on:
  - cst-sin-perdidas
  - ../08-sintaxis-abstracta
  - mud-surface-ast.asdl
  - cobertura-sintactica.yaml
questions: []
decisions:
  - D-015
  - D-054
  - D-066
  - D-070
  - D-071
  - D-072
  - D-073
  - D-085
  - D-086
  - D-087
  - D-096
---

# Transformación de CST a AST superficial

## Estado y propósito

Este documento define la proyección normativa desde una CST validada al AST superficial normalizado. No define resolución de nombres, inferencia, evaluación estática ni semántica dinámica.

La matriz exhaustiva producción por producción está en `cobertura-sintactica.yaml`. Este documento define las reglas generales y las normalizaciones que requieren explicación.

## Precondición

La transformación recibe:

- Una `MudFileSyntax` completa.
- Tokens y nodos con spans coherentes.
- Ausencia de errores sintácticos bloqueantes en el subárbol transformado.
- Validación contextual de duplicados y combinaciones prohibidas.
- Metadatos físicos del archivo.

La existencia de tokens `MissingForRecovery`, `ErrorSyntax` o `SkippedTokensSyntax` dentro de una declaración impide producir el nodo normativo correspondiente, salvo que una implementación ofrezca además un AST tolerante a errores no normativo.

## Resultado

La transformación produce un `MudFile` con:

```text
metadata físico
metadataDefaults[]
usings[]
declarations[]
origin
```

Los metadatos de campos, componentes, participantes, unidades y demás propietarios estables se conservan directamente en el constructor del propietario. No existe una tabla lateral de `MetadataAttachment` por span.

El agregador de compilación construye después `MudProject` y ordena sus archivos por ruta normalizada para serialización canónica.

## Reglas comunes

### Trivia

Toda trivia se descarta. Los comentarios ordinarios no producen nodos AST.

### Puntuación

Se descartan:

- Comas.
- Dos puntos sintácticos.
- Llaves, corchetes y paréntesis.
- Terminadores.
- Palabras clave cuya presencia queda codificada por el constructor.

Una palabra clave que distingue operadores o variantes se convierte al enum correspondiente.

### Orden

Se conserva el orden fuente de todos los elementos que se convierten en secuencias AST. La transformación no ordena listas por significado.

### Procedencia

Un nodo directamente representado usa el span de la construcción CST completa, excluida la trivia inicial.

Un nodo sintetizado usa:

```text
Synthetic(anchorSpan, reason)
```

El `anchorSpan` es la posición concreta más estrecha que explica la síntesis.

## Archivo y `using`

```text
mud-file → MudFile
using-declaration → UsingDecl
```

El cuerpo concreto `using-file-body` o `declaration-file-body` desaparece. La transformación separa los defaults de metadatos de archivo, la cabecera `using` y las declaraciones. Los metadatos subordinados quedan en el constructor de su propietario, no en una tabla lateral.

```mud
using physics.*
```

produce:

```text
UsingDecl(path = [physics], recursive = Enabled)
```

La ausencia de `.*` produce `Disabled`.

## Nombres

Cada producción nominal genera su wrapper correspondiente. Los nombres cualificados conservan segmentos, no una string con puntos.

```mud
world.people.Person
```

produce conceptualmente:

```text
QualifiedName([world, people, Person])
```

Un camino de expresión formado únicamente por segmentos con punto produce `DottedPathExpr` hasta que la resolución determine su categoría.

## `thing`

```ebnf
thing-declaration
```

produce `ThingDecl`:

- `abstract` → `Enabled`; omisión → `Disabled`.
- Nombre → `NominalName`.
- Antecesores → secuencia de `TypeRef`.
- Declaraciones `~...` almacenadas o calculadas → secuencia de `metadata_assignment`, normalizada a `StoredMetadataAssignment` o `CalculatedMetadataAssignment`.
- Cuerpo → metadatos, campos e inicializadores concretos.

`thing-body` y `thing-body-declaration` no generan nodos AST independientes. `metadata-assignment` sí produce un nodo propio y no se convierte en campo. Cada `field-declaration` alimenta la secuencia `fields`; cada `thing-initializer`, tanto en una `thing` concreta como abstracta, produce `ThingInitializer(fieldName, value)` en la secuencia `initializers`, sin plegarse dentro de `StoredFieldDecl.defaultValue`. Si una misma definición declara localmente un campo y contiene un `thing-initializer` con el mismo nombre, se rechaza durante la validación previa al AST. La omisión del cuerpo y un cuerpo explícito vacío producen las mismas secuencias vacías; el terminador se descarta como layout.

Una forma `name = valor` no recibe un rechazo sintáctico especial. Se proyecta como cualquier otro `ThingInitializer`; la resolución posterior decide si `name` designa realmente un campo almacenado heredado del esquema efectivo. Si la misma `thing` declara localmente un campo ordinario `name`, la combinación se rechaza por la regla general que impide declarar e inicializar por separado el mismo campo. El metadato de presentación continúa escribiéndose `~name = valor`.

Un antecesor explícito `Thing` permanece en esa secuencia superficial. No bloquea la transformación: la resolución posterior emite la redundancia, normaliza la raíz efectiva y puede ofrecer una acción de código que retire el elemento escrito.

## Campos

### Almacenado

```mud
mut population: Population in [0..*] [1] = 10 people
```

se proyecta a:

```text
StoredFieldDecl(
    collectionMutable = Enabled,
    name = population,
    shape = ValueShape(
        type = NamedType(Population),
        domain = [0..*],
        collection = CollectionSpec([1..1], ...)
    ),
    defaultValue = 10 people
)
```

El dominio de la forma de valor y la especificación de colección son nodos normalizados, no fragmentos de texto.

### Calculado y público

La anotación de tipo ausente permanece ausente. No se inserta el tipo inferido.

## Normalización de colecciones

### Cardinalidad omitida

```mud
value: Nat
values: Nat = [1, 2, 3]
```

ambas formas producen un `CollectionSpec` con `OmittedCardinality`. El AST superficial no fabrica `[1]` ni infiere `[3]`. La elaboración posterior usa el propietario y el inicializador: un escalar ordinario sin evidencia conserva `[1]`; un campo almacenado inmutable con inicializador finito puede obtener una cardinalidad exacta con procedencia `InferredFromInitializer`.

### Cardinalidad exacta

```mud
values: Nat [5]
```

produce:

```text
[5..5]
```

### Estrella exacta

```mud
values: Nat [*]
```

produce:

```text
[EffectiveCardinality..EffectiveCardinality]
```

No se sustituye todavía el extremo izquierdo por cero.

### Modificadores

Las dos formas concretas:

```mud
[0..* unique ordered mut]
[0..*, unique, ordered, mut]
```

producen el mismo `CollectionSpec`.

La omisión de modificadores produce:

```text
isUnique = Disabled
order = Unordered
elementsMutable = Disabled
```

`ordered` produce `InsertionOrdered`. `ordered by a.b` produce `OrderedBy([a,b])`.

La validación previa rechaza:

- Repetición de `unique`.
- Repetición de `mut`.
- Más de un `ordered`.
- `ordered` y `ordered by` simultáneos.

### `given`

`given-declaration` proyecta su anotación mediante el mismo `TypeExpr` superficial que los demás contextos de tipo. Esto permite conservar tipos diccionario completos sin introducir una segunda jerarquía de tipos de solo lectura. La presencia de capacidad `mut` puede quedar representada en el AST superficial, pero D-063 la rechaza estáticamente para `given` antes de producir IR semántico.

## Tipos

### Nominal

Todo `type-reference` produce `NamedType(TypeRef(...))`. El AST no clasifica aún el nombre.

### Productos y diccionarios

```mud
Name -> Coordinate -> Piece [*]
A -> B [2] --> C [3 ordered]
```

Las cadenas de flechas se pliegan por la derecha. La primera forma produce un `ExactDictionaryType(Name, ExactDictionaryType(Coordinate, Piece, [*]), ...)`; la segunda produce un exacto cuyo valor es un `DecisionDictionaryType(B, C, FirstMatch, [3])`, y `[2]` pertenece a la flecha exterior.

`(A, B)` y `(name: A, value: B)` producen respectivamente `PositionalProductType` y `NamedProductType`. Los paréntesis que forman el producto sobreviven mediante el constructor; los paréntesis puramente agrupadores se descartan.

La CST puede reconocer una flecha parentizada dentro de una alternativa, pero la validación contextual o la resolución rechaza que una flecha sea una alternativa parcial de `|`, incluso cuando la forma exterior procede de un alias.

## Aliases

La lista escrita después de `as` se conserva como `direct_ancestors`. La alternativa `:= type-expression` produce `AliasRepresentation`; su combinación con antecesores se rechaza antes del AST. La ausencia de definición produce `definition = None` y solo es válida si existe al menos una antecesora. Un cuerpo metadata-only posterior a `:= type-expression` alimenta `AliasDecl.metadata` y no crea miembros estructurales.

`type-expression` normaliza una o más `type-alternative` separadas por `|` en un único `TypeExpr`. Se eliminan agrupaciones redundantes, se deduplican alternativas idénticas y se conserva cada alternativa nominal aunque su dominio esté contenido en el de otra. La especificación de colección exterior se asocia al `TypeExpr` completo.

`derived-value-shape` con `: type-expression` produce `ExplicitDerivedShape`. Las formas sin tipo, `in domain [collection]` y `collection`, producen `InferredDerivedShape`; una colección omitida se normaliza a la cardinalidad escalar y el tipo no se inventa hasta la fase de inferencia.

Una restricción `interval-expression by constant-expression` produce `SteppedDomain`; las demás restricciones producen `ExpressionDomain`. Los paréntesis que no cambian la agrupación no llegan al AST superficial.

El cuerpo estructural produce `StructuralAlias` con `AliasMember` en orden fuente. Un `component-declaration` produce `AliasComponentDecl`; un `calculated-field-declaration`, `AliasCalculatedFieldDecl`; y `inherited-default-override`, `AliasDefaultOverride`.

Un componente no puede producir mutabilidad exterior. Su colección general sí puede producir `elementsMutable = Enabled`. Un campo derivado puede declarar igualmente `elementsMutable = Enabled`; esa capacidad pertenece a la colección derivada y no se infiere de las fuentes de su expresión.

## Familias

La palabra `ordered` produce `isOrdered = Enabled`.

Las declaraciones de datos se separan en almacenadas y calculadas. Cada declaración puede llevar un cuerpo inmediato formado exclusivamente por `metadata-assignment`; esa secuencia se conserva en `StoredFamilyDataDecl.metadata` o `CalculatedFamilyDataDecl.metadata`. El dato calculado conserva provisionalmente `derived_value_shape? shape`, porque Q-061 mantiene abierta la contradicción entre la EBNF actual y la restricción más estrecha escrita en D-038. Esta transformación no inventa una normalización que resuelva esa cuestión.

En el preámbulo de un miembro, cualquier `metadata-assignment` produce `StoredMetadataAssignment` o `CalculatedMetadataAssignment` del descriptor del miembro; las asignaciones ordinarias posteriores se conservan como `FamilyDataAssignment`. Estas asignaciones sustituyen el valor de un dato almacenado para ese miembro, pero no crean descriptor, ancla ni metadata-body propios. Un cuerpo de miembro metadata-only produce `assignments = []` y conserva su secuencia `metadata`.

La coma entre miembros desaparece. La ausencia de coma final ya ha sido validada por la gramática.

## Magnitudes

### Representación

La anotación opcional usa `DeclaredType`. La comprobación de representación numérica se difiere.

### Base

El cuerpo se divide en:

- Unidad raíz opcional.
- Unidades alternativas posteriores.

### Derivada

La expresión dimensional se pliega de izquierda a derecha en `DimensionProduct` y `DimensionLink` conservando multiplicación y división.

### Punto

El dominio ordinario produce `OrdinaryPointDomain`; la presencia de `cycle` después de la expresión intervalo produce `CyclicPointDomain`. El token no se incorpora al intervalo como un delimitador ni como parte de sus extremos.

`~format` ausente permanece ausente.

## Unidades

Las unidades no tienen una normalización `UnitProperties` separada. `unit-body` se descarta como envoltorio concreto y cada `metadata-assignment` se conserva en la secuencia `metadata` de `RootUnitDecl` o `AlternativeUnitDecl`.

`~prefixes = empty`, `~prefixes = all` y `~prefixes = [kilo, milli]` siguen la transformación ordinaria de expresiones. El AST superficial no fabrica `NoPrefixes`, `AllPrefixes` ni `SelectedPrefixes`; la elaboración posterior aplica el tipo esperado `Prefix [* unique]` y el default `empty`.

Una unidad raíz produce `RootUnitDecl(name, metadata)` y una alternativa `AlternativeUnitDecl(name, equivalence, metadata)`. Los metadatos de presentación omitidos permanecen ausentes en esta fase.

## Participantes

### `for`

Cada participante tiene nombre obligatorio. Se convierten `mut` exterior, `ValueShape` y la secuencia de metadatos del descriptor. Una cabecera agrupada produce un `ForParticipant` por identificador y copia a cada uno el mismo metadata-body.

### `on`

La variante directa produce `DirectOnParticipant(name, type, elementsMutable, metadata)`. La variante relacionada produce `RelatedOnParticipant(name, refinement?, source, elementsMutable, metadata)`. Las referencias cruzadas continúan sin resolver en esta fase.

### `given`

Se convierten nombre, `TypeExpr`, predeterminado y metadatos. Un tipo diccionario se conserva mediante los constructores ordinarios `ExactDictionaryType` o `DecisionDictionaryType`. El predeterminado continúa siendo `expr`; su carácter constante y la prohibición de cualquier capacidad `mut` del `given` se comprueban después.

## Reglas y acciones

El preámbulo metadata-bearing de cada regla, action, subaction, look, message y test se conserva en el campo `metadata` del constructor superior correspondiente. `start with` no obtiene metadata propia.

### Regla booleana

El cuerpo se convierte en `ExpressionBlock(locals, result)`. La forma sin declaraciones locales produce `locals = []`.

### Regla reactiva

`when` produce un `ExpressionBlock` en `activator`; `if` produce otro en `guard?`; `then` produce `EffectBlock`.

### Regla `always`

`InvariantBodySyntax`, encerrado entre llaves, produce un `ExpressionBlock`. El `DiagnosticTailSyntax` exterior produce el diagnóstico de `AlwaysRuleDecl`; si está ausente se conserva `diagnostic = absent`. No se inserta aquí el texto predeterminado del warning.

### Acción

`if` produce `ActionGuard` con un `ExpressionBlock`; `after` produce `ActionPostcondition` con otro.

No se clasifica la acción como elemental o compuesta.

### `look` y `message`

Las propiedades públicas se convierten a `PublicFieldDecl` y conservan su orden.

## Bloques de expresión y tests

Los terminadores opcionales escritos después de `:` en `for each`, selección y cuantificadores son separación concreta: no producen nodos ni cambian `ExpressionBlock`/`EffectBlock`.

Una forma breve como `if ready` produce `ExpressionBlock([], ready)`. Una forma entre llaves recoge todas las declaraciones locales `:=` iniciales y exige una única expresión final. El `otherwise` asociado queda fuera del bloque AST, pero la resolución posterior extiende hasta él el entorno de esos locales.

En tests, `after expr` produce `TestAfterBlock([], [TestAssertion(expr)])`. La forma entre llaves produce `TestAfterBlock(locals, assertions)`; los locales solo pueden aparecer antes de la primera aserción.

## `then` y bloques

```mud
then effect
```

y:

```mud
then {
    effect
}
```

producen ambos `EffectBlock`, con una sentencia en los casos equivalentes.

Las declaraciones locales anteriores al primer efecto se almacenan en `leadingLocals`; el primer efecto ocupa `firstEffect`; las declaraciones locales y efectos posteriores forman `remainingStatements`.

## Efectos

### Asignación

El operador concreto se convierte a:

- `Assign`.
- `AddAssign`.
- `SubtractAssign`.
- `MultiplyAssign`.
- `DivideAssign`.
- `UnionAssign`.
- `IntersectionAssign`.
- `SymmetricDifferenceAssign`.
- `DifferenceAssign`.

### `add`

La alternativa con expresión produce `AddValueEffect`.

La alternativa con declaración de campo produce `AddFieldEffect`. La declaración anidada se transforma como campo almacenado.

### Candidato a llamada

`action-call-effect` produce `ActionCallCandidateEffect(expr)`. La resolución posterior debe confirmar que la expresión termina en una llamada a acción válida.

### Iteración

La vinculación simple produce `ValueIterationBinding`. La pareja entre paréntesis produce `DictionaryIterationBinding`. `for each` conserva `by` como `step?`, normaliza `if` a `ExpressionBlock` y convierte tanto el efecto breve como el bloque tras `:` en `EffectBlock`. Dirección, compatibilidad y paso cero pertenecen a fases posteriores.

## Expresiones

### Plegado de precedencia

Las producciones por niveles se pliegan conforme a [[07-gramatica-concreta]]:

- Operadores repetitivos ordinarios: izquierda.
- Implicación: derecha.
- Comparaciones encadenables: `ComparisonChainExpr`.

### Operadores de palabra y símbolo

Se conservan enums distintos:

| Concreto | AST |
|---|---|
| `and` | `WordAnd` |
| `&` | `SymbolAnd` |
| `or` | `WordOr` |
| `|` | `SymbolOr` |
| `xor` | `WordXor` |
| `^` | `SymbolXor` |
| `--` | `CollectionDifference` |

### `changes`

La presencia del sufijo produce `ChangesExpr(operand)`.

### Selección y `take`

`binding in source [by step]: predicate` produce `SelectionExpr(binding, source, step?, predicate)`. La vinculación simple o de diccionario reutiliza `ValueIterationBinding` o `DictionaryIterationBinding`; su alcance queda limitado al predicado. La forma breve y `{ locales*; resultado }` convergen en `ExpressionBlock`.

Los cuantificadores/agregadores producen `QuantifierExpr(kind, variable, source, step?, body)`, con `body` como `ExpressionBlock`. La transformación no decide contrato de tipo ni admisibilidad de la progresión.

`take amount from source` produce `TakeExpr(amount, source)`. La forma del nodo no decide si la selección será un prefijo ordenado o una muestra reproducible: esa distinción depende del tipo y del orden resueltos de `source`.

Ambas construcciones contienen expresiones completas. Por tanto, la composición se conserva por anidamiento explícito del AST:

```text
take n from player in players: player.score == 2
→ TakeExpr(n, SelectionExpr(player, players, ...))

player in take m from players: player.score == 2
→ SelectionExpr(player, TakeExpr(m, players), ...)
```

### Conversiones

`to T` produce `TypeConversion`. `in u` produce `UnitConversion`.

### Postfix

Los sufijos se aplican en orden:

```text
base.a[i](x)
```

produce:

```text
CallExpr(
  IndexExpr(
    MemberAccessExpr(base, a),
    [i]
  ),
  [x]
)
```

### Argumentos

Los argumentos sin etiqueta forman el prefijo `positionalArguments`. Los argumentos con `name =` forman el sufijo de `NamedCallArgument`.

La validación sintáctica contextual rechaza un posicional posterior al primer nombrado, por lo que `CallExpr` no necesita representar ese estado inválido.

### Ambigüedad de receptores

`receiver-tuple` y `structural-literal` convergen en una de dos formas: `PositionalStructuralLiteralExpr` o `NamedStructuralLiteralExpr`. El `MemberAccessExpr` y `CallExpr` posteriores conservan la forma completa. La resolución de firma selecciona después entre receptor único estructural y receptores múltiples.

### Caminos

Un `qualified-name` usado como expresión produce `DottedPathExpr`, no una referencia resuelta.

## Literales

### Exactos y `Rum`

Se eliminan `_` y se normaliza el exponente y la mantisa a una escritura canónica. No se pierde la procedencia al lexema CST.

### `Char` y `Text`

Todo literal ordinario entre comillas dobles produce inicialmente `TextTemplateExpr`. La elaboración contextual posterior lo convierte en `Char` cuando el tipo esperado lo exige y el texto decodificado contiene exactamente un escalar Unicode. Las comillas simples no producen ningún token literal.

### Booleanos

`true` → `BoolLiteral(Enabled)`.

`false` → `BoolLiteral(Disabled)`.

### `empty`

Produce `EmptyLiteral`.

### `POINT_LITERAL`

Conserva su forma fuente en `PointLiteral`; su magnitud esperada no se resuelve aún.

## Plantillas

`TEXT_FRAGMENT` se decodifica después de escapes y normalización de margen.

La diferencia entre cierre explícito e implícito desaparece.

Toda interpolación produce `ValueInterpolation`; `anchor{...}` no pertenece al lenguaje.

Dentro del `format` de una magnitud de punto, `unidad from contenedor` produce `ContextualPointComponentExpr`; no se inventa un receptor que no estaba escrito.

## Literales estructurales

La forma posicional produce `PositionalStructuralLiteralExpr` con dos elementos obligatorios y los restantes.

La forma nombrada produce `NamedStructuralLiteralExpr` con uno o más `NamedStructuralElement`.

La selección de alias, la completitud posicional y los predeterminados de componentes pertenecen a validación/resolución posterior según necesiten tipo esperado.

## Valores separados por comas

La producción:

```ebnf
value-expression ::= expression , [ "," , expression , { "," , expression } ] ;
```

se transforma así:

- Sin coma: expresión original.
- Con una o más comas: `CollectionLiteralExpr` de todas las expresiones.

## Intervalos

### Cerrado abreviado

```mud
a..b
```

produce límites cerrados.

### Singleton

```mud
[a]
```

produce `lower = a`, `upper = a`, ambos cerrados.

### Vacío con unidad

```mud
[] meters
```

produce `EmptyInterval(UnitProduct(...))`.

### Unidad compartida

La unidad final se mueve al campo `sharedUnit`; no se duplica en cada extremo.

### Cíclico

El `cycle` posterior del `PointDomainSyntax` selecciona `CyclicPointDomain`; no modifica el `Interval` contenido. La validación anterior al AST exige que el intervalo precedente sea finito, no vacío, cerrado a la izquierda y abierto a la derecha.

### Estrellas

`*` produce `EffectiveIntervalBound`, sin convertirlo todavía a infinito o a un extremo dependiente del dominio.

## Cantidades y unidades

Un literal numérico seguido por unidad produce `QuantityValueExpr(Quantity(...))`.

Las expresiones de unidad y dimensión eliminan paréntesis de agrupación, pero conservan el árbol impuesto por multiplicación y división.

## `start with` y tests

Las referencias de un `start with` producen `StartSet`.

La declaración global añade `GlobalStartDecl`. Dentro de un test, el mismo `StartSet` es un campo de `TestDecl`.

`after assertion` y `after { assertion... }` producen un `TestAfterBlock` uniforme.

## Elementos que no se normalizan todavía

Permanecen pendientes de fases posteriores:

- Nombre cualificado frente a acceso semántico.
- Alias concreto de un literal estructural.
- Receptores múltiples frente a receptor estructural.
- Llamada ordinaria frente a llamada de regla o acción.
- Tipo de un literal contextual.
- Constancia de una expresión declarada estática.
- Compatibilidad de dominios y cardinalidades.
- Resolución de unidades y prefijos.

## Diagnósticos de transformación

La transformación puede emitir diagnósticos propios únicamente cuando:

- La CST viola una invariante contextual requerida para normalizar.
- Falta una propiedad necesaria para construir un producto AST.
- Dos formas concretas intentan escribir el mismo campo normalizado.
- Una producción cubierta no posee regla de transformación.

Un fallo de nombres o tipos no es un diagnóstico de esta fase.

## Tabla mecánica

`cobertura-sintactica.yaml` es exhaustivo. Cada producción declara:

- `cst`: categoría concreta.
- `ast.disposition`.
- `ast.target` o razón de descarte/pliegue.

Las disposiciones son:

- `constructor`.
- `wrapper`.
- `normalized`.
- `enum-or-property`.
- `folded`.
- `inlined`.
- `discarded`.

## Pruebas mínimas

Cada regla de normalización debe contar con al menos:

- Forma mínima válida.
- Variante equivalente.
- Caso límite.
- Caso inválido previo al AST cuando proceda.

El corpus inicial está en `casos/cst-ast.yaml`.


## Revisión de transformación por D-085

Estas reglas sustituyen las normalizaciones anteriores incompatibles:

1. Una declaración `~...` produce `StoredMetadataAssignment` o `CalculatedMetadataAssignment` y se conserva en la secuencia `metadata` de su propietario.
2. La omisión de cardinalidad produce `OmittedCardinality`. La inferencia exacta de un campo almacenado inmutable pertenece a la elaboración y no se simula con `[1]` sintético.
3. Una cadena `A -> B [m] --> C [n]` se pliega de derecha a izquierda. Cada enlace produce `ExactDictionaryType` o `DecisionDictionaryType` y conserva sus modificadores.
4. Los productos de tipo producen `PositionalProductType` o `NamedProductType`; los literales estructurales existentes conservan sus nodos de valor.
5. `a -> b` produce `ExactAssociationExpr`; `selector --> resultado`, `DecisionBranchExpr`; `_`, `FallbackLiteral`.
6. `element~metadata` produce `MetadataAccessExpr`; ningún acceso `~` forma parte de un objetivo asignable runtime.
7. `not in` produce `NotMembership`.
8. `action` y `subaction` producen `ActionDecl` con `PublicAction` o `Subaction`.
9. `start with` produce `StartSet(contributions)` con una única secuencia de contribuciones; la categoría activable se comprueba durante elaboración.
10. Toda interpolación es `ValueInterpolation`; no existe `AnchorInterpolation`.
11. `e iis T` produce `ExactTypeTestExpr(e, T, Disabled)` y `e iis not T`, `ExactTypeTestExpr(e, T, Enabled)`.
12. `|`, `&`, `--` y `^` conservan inicialmente `BinaryExpr`; la elaboración los especializa según sean colecciones, diccionarios exactos o diccionarios funcionales.
13. Una operación funcional conserva ambos operandos y nunca se transforma en una lista fusionada de ramas.

## Proyección D-087

`MudFile` conserva defaults de archivo y cada propietario estable conserva directamente su secuencia `metadata`. Los grupos de participantes producen un nodo por identificador y copian a cada descriptor las mismas declaraciones con procedencia `NormalizedSugar`. `start with` y los cuerpos de cláusula no reciben metadata propia.

Las unidades usan exactamente la misma proyección: `unit-body` es solo un contenedor de `metadata-assignment`. `~prefixes` permanece una expresión ordinaria cuyo tipo esperado es `Prefix [* unique]`; no existe `UnitProperties`, `PrefixPolicy` ni `MetadataAttachment` lateral.

## D-096 — tipos callable, `look`, locales, `all D` y `start with`

- `callable-type` produce `CallableType(kind, receivers, givens)` conservando literalmente categoría y tipos escritos; la compatibilidad/varianza se difiere a Q-063.
- `reflected-type` produce `ReflectedType(value)` y la elaboración posterior exige que ese valor termine en `~type` y denote estáticamente `Type`; el IR semántico sustituye esa forma por el tipo representado.
- `look-declaration` proyecta su `given-clause` opcional a `LookDecl.givens`.
- Las `local-value-declaration` situadas entre metadatos y cláusulas de action/rule reactiva/message se proyectan a `leading_locals` de su declaración, no al `EffectBlock` posterior.
- El prefijo `all D` se normaliza como `PrefixExpr(EnumerateAll, D)`; el literal contextual sin operando conserva `AllLiteral`.
- `start-with-declaration` normaliza tanto la forma de una expresión como el bloque de expresiones a un único `StartSet(contributions)` y conserva el orden fuente solo como procedencia, no como semántica de activación.
