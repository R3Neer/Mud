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
  - D-070
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
metadata
usings[]
declarations[]
origin
```

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

El cuerpo concreto `using-file-body` o `declaration-file-body` desaparece. La transformación separa la cabecera `using` de las declaraciones.

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
- `name = "literal"` → texto decodificado en `intrinsic_name_override`.
- Cuerpo → campos.

`thing-body`, `thing-body-declaration` e `intrinsic-name-override` no generan nodos AST independientes. La validación anterior al AST exige como máximo una sobrescritura, sin interpolaciones, y la integra en `ThingDecl` sin convertirla en campo.

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
```

produce una colección sintética:

```text
Cardinality(FiniteCardinality(1), FiniteCardinality(1))
```

con razón `OmittedDefault`.

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

`given-collection-specification` produce `ReadonlyCollectionSpec`; no existe campo para `elementsMutable`.

## Tipos

### Nominal

Todo `type-reference` produce `NamedType(TypeRef(...))`. El AST no clasifica aún el nombre.

### Diccionario

```mud
Name -> (Coordinate -> Piece [*]) [*]
```

se proyecta de dentro hacia fuera:

```text
TypeExpr(
  DictionaryType(
    Name,
    TypeExpr(
      DictionaryType(Coordinate, TypeExpr(Piece, ..., [*])),
      ...
    )
  ),
  ...,
  [*]
)
```

Los paréntesis concretos se descartan.

## Aliases

La alternativa `:= type-expression` produce `AliasOf`.

El cuerpo estructural produce `StructuralAlias` con `AliasComponent` en orden fuente.

Un componente no puede producir mutabilidad exterior. Su colección general sí puede producir `elementsMutable = Enabled`.

## Familias

La palabra `ordered` produce `isOrdered = Enabled`.

Las declaraciones de datos se separan en almacenadas y calculadas. Los miembros conservan sus asignaciones; el cuerpo omitido genera una secuencia vacía.

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

El dominio ordinario produce `OrdinaryPointDomain`; la forma con `cycle` produce `CyclicPointDomain`.

`format` ausente permanece ausente.

## Unidades

La lista concreta de propiedades se convierte en una estructura fija después de validar unicidad y obligatoriedad.

| Forma concreta | AST |
|---|---|
| `name = e` | `name = e` |
| `plural = e` | `plural = e` |
| `abbreviation = e` | `abbreviation = e` |
| propiedad `prefixes` omitida | `AllPrefixes` |
| `prefixes = empty` | `NoPrefixes` |
| `prefixes = [a, b]` | `SelectedPrefixes([a,b])` |

No se sintetiza plural.

Una unidad raíz produce `RootUnitDecl`. Una alternativa produce `AlternativeUnitDecl(equivalence, properties)`.

## Participantes

### `for`

Se convierte `mut` exterior, nombre opcional y `ValueShape`.

La omisión de nombre sigue siendo ausencia; no se inventa uno a partir del tipo.

### `on`

La primera alternativa gramatical produce `DirectOnParticipant`.

La alternativa con `in expression` produce `RelatedOnParticipant`.

`[mut]` produce `elementsMutable = Enabled`.

Las referencias entre participantes permanecen como expresiones no resueltas.

### `given`

Se convierten nombre, tipo, dominio, colección de solo lectura y predeterminado. El predeterminado continúa siendo `expr`; su carácter constante se comprueba después.

## Reglas y acciones

### Regla booleana

El cuerpo de una única expresión se almacena directamente como condición.

### Regla reactiva

`when` produce `activator`; `if` produce `guard?`; `then` produce `EffectBlock`.

### Regla `always`

`otherwise` ausente produce `diagnostic = absent`. No se inserta aquí el texto predeterminado del warning.

### Acción

`if` produce `ActionGuard`; `after` produce `ActionPostcondition`.

No se clasifica la acción como elemental o compuesta.

### `look` y `message`

Las propiedades públicas se convierten a `PublicFieldDecl` y conservan su orden.

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

### `add`

La alternativa con expresión produce `AddValueEffect`.

La alternativa con declaración de campo produce `AddFieldEffect`. La declaración anidada se transforma como campo almacenado.

### Candidato a llamada

`action-call-effect` produce `ActionCallCandidateEffect(expr)`. La resolución posterior debe confirmar que la expresión termina en una llamada a acción válida.

### Iteración

La vinculación simple produce `ValueIterationBinding`. La pareja entre paréntesis produce `DictionaryIterationBinding`.

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

### `changes`

La presencia del sufijo produce `ChangesExpr(operand)`.

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

Una interpolación de valor produce `ValueInterpolation`; `anchor{...}` produce `AnchorInterpolation`.

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

`cycle` produce `cyclic = Enabled` y conserva el extremo superior abierto exigido por la sintaxis.

### Estrellas

`*` produce `EffectiveIntervalBound`, sin convertirlo todavía a infinito o a un extremo dependiente del dominio.

## Cantidades y unidades

Un literal numérico seguido por unidad produce `QuantityValueExpr(Quantity(...))`.

Las expresiones de unidad y dimensión eliminan paréntesis de agrupación, pero conservan el árbol impuesto por multiplicación y división.

## `start with` y tests

Las referencias de un `start with` producen `StartSet`.

La declaración global añade `GlobalStartDecl`. Dentro de un test, el mismo `StartSet` es un campo de `TestDecl`.

`after assertion` y `after { assertion... }` producen una secuencia uniforme.

## Elementos que no se normalizan todavía

Permanecen pendientes de fases posteriores:

- Nombre cualificado frente a acceso semántico.
- Alias concreto de un literal estructural.
- Receptores múltiples frente a receptor estructural.
- Llamada ordinaria frente a llamada de regla o acción.
- Acción elemental frente a compuesta.
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
