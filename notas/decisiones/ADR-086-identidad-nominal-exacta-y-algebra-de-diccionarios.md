---
id: D-086
title: "Identidad nominal exacta, flechas exteriores y álgebra de diccionarios"
status: vigente
date: 2026-08-05
supersedes: []
superseded-by: []
questions: []
affects:
  - "operadores de tipo, narrowing nominal, diccionarios exactos y funcionales, cardinalidad, orden, unicidad, AST, IR, diagnósticos y ejemplos normativos"
---

# ADR-086 — Identidad nominal exacta, flechas exteriores y álgebra de diccionarios

- Modifica: [[ADR-038-familias-cerradas-de-valores|D-038]], [[ADR-039-colecciones-y-diccionarios|D-039]], [[ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]], [[ADR-057-gramatica-concreta-y-continuacion|D-057]], [[ADR-068-thing-universal-y-nombre-intrinseco|D-068]], [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]], [[ADR-074-uniones-nominales-y-estrechamiento|D-074]], [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]], [[ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|D-080]], [[ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]] y [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].
- Amplía: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]] y [[ADR-052-pipeline-materializadores-y-conformidad|D-052]].
- Documentos afectados: capítulos 02 y 04 a 09; futuros capítulos 10, 12, 15, 16, 19, 20, 34, 38, 40, 41, 44 y 47; gramática; CST; AST superficial; representación semántica posterior a tipado y elaboración; casos de conformidad.

## Contexto

D-085 introdujo tipos de diccionario exactos `A -> B` y diccionarios definidos mediante ramas `A --> B`, junto con productos anónimos, ausencia mediante `empty`, metadatos postfix y asociación derecha de flechas. La primera integración dejó tres asuntos incompletos:

1. La relación entre uniones y flechas no impedía de forma expresa que un diccionario apareciese como alternativa parcial de una unión, incluso después de resolver aliases.
2. `is` no permite distinguir pertenencia nominal transitiva de identidad nominal exacta, distinción necesaria al ordenar ramas que refinan aliases especializados.
3. Los operadores conjuntistas ya existentes carecían de una semántica específica para diccionarios exactos y para diccionarios definidos por ramas.

Además, la documentación numerada conservaba ejemplos y explicaciones incompatibles con D-085. Esta decisión fija la semántica nueva; la corrección de esos ejemplos forma parte de su integración documental, pero no crea decisiones adicionales.

## Terminología

La denominación pública canónica de `A --> B` pasa a ser **diccionario funcional**. La expresión **diccionario decisional** permanece como término histórico de D-085 y como descripción de su implementación por ramas, pero no es el nombre preferido en la especificación vigente.

Los identificadores mecánicos `DecisionDictionaryType`, `DecisionBranchExpr` y `DecisionApplyExpr` se conservan en la primera versión de los esquemas para no introducir una migración nominal sin valor semántico. Deben interpretarse como la representación de los diccionarios funcionales definidos por casos.

## Decisión

### Precedencia de `|`, `->` y `-->` en tipos

El operador de unión de tipos `|` tiene mayor precedencia que `->` y `-->`. Las dos flechas poseen la misma precedencia y son asociativas a la derecha.

```mud
A | B -> C | D
```

equivale a:

```mud
(A | B) -> (C | D)
```

```mud
A | B --> C | D
```

equivale a:

```mud
(A | B) --> (C | D)
```

```mud
A -> B -> C
```

equivale a:

```mud
A -> (B -> C)
```

Cada especificación de cardinalidad, orden, unicidad o capacidad pertenece exclusivamente a la flecha inmediatamente anterior:

```mud
A -> B [2] --> C [3 ordered]
```

se elabora como:

```mud
A -> (B --> C [3 ordered]) [2]
```

### La flecha como forma exterior completa

Una flecha debe constituir la forma exterior completa del tipo en el que aparece. Un diccionario exacto o funcional no puede ser una alternativa parcial de una unión. Los paréntesis no eluden esta restricción.

Son inválidos:

```mud
value: A | (B -> C)
value: (A -> B) | C
value: A | (B --> C) | D
value: (A -> B) | (C -> D)
```

Son válidos:

```mud
value: (A | B) -> C
value: A -> (B | C)
value: (A | B) --> (C | D)
value: A -> (B -> C)
```

La restricción se comprueba después de resolver aliases. Si la forma exterior efectiva de un alias es una flecha, tampoco puede emplearse como alternativa de una unión:

```mud
alias Lookup := B -> C

value: A | Lookup       # inválido
value: A -> Lookup      # válido
```

La EBNF puede conservar agrupaciones parentizadas para producir una CST útil; la validación posterior a la resolución rechaza las formas exteriores prohibidas.

### Operador nominal exacto `iis`

`iis` es un operador infijo no encadenable cuyo resultado es `Bool`. El operando izquierdo es un valor y el derecho debe resolver a un tipo nominal.

```mud
value iis PersonId
```

es verdadero solo cuando el tipo nominal efectivo del valor es exactamente `PersonId`.

`is` y `iis` son distintos:

```mud
value is T
```

comprueba pertenencia a `T`, incluidas sus especializaciones.

```mud
value iis T
```

comprueba identidad nominal exacta.

Sean:

```mud
alias Identifier := Nat
alias PersonId as Identifier
alias EmployeeId as PersonId
```

Para un valor cuyo tipo exacto es `EmployeeId`:

```mud
value is Identifier    # true
value is PersonId      # true
value is EmployeeId    # true

value iis Identifier   # false
value iis PersonId     # false
value iis EmployeeId   # true
```

La misma regla se aplica con especialización múltiple. Para `alias C as A, B`, un valor exacto `C` satisface `is A`, `is B` e `is C`, pero solo `iis C`.

### Negación exacta `iis not`

`iis not` es la forma derivada directa de la negación del test exacto:

```mud
value iis not PersonId
```

equivale a:

```mud
not (value iis PersonId)
```

No se añade `not iis`. El parser conserva si se escribió `iis` o `iis not` mediante la polaridad del nodo exacto; el formateador puede preservar la forma fuente.

### Narrowing

- `value is T` conserva `T` y sus especializaciones posibles.
- `value iis T` conserva únicamente la posibilidad nominal exacta `T`.
- `not (value is T)` elimina `T` y todas sus especializaciones.
- `not (value iis T)` y `value iis not T` eliminan solo la posibilidad exacta `T`; las especializaciones continúan siendo posibles.

El análisis de flujo debe aplicar estas reglas a uniones nominales y a especialización múltiple.

`iis` no sustituye a `==`. La igualdad compara valores conforme a su tipo y contenido; `iis` solo inspecciona el tipo nominal efectivo del operando izquierdo.

La identidad exacta de una `thing` singleton continúa comprobándose mediante `==`:

```mud
place == Madrid
```

La pertenencia de una `thing` a una categoría se comprueba mediante `is`:

```mud
place is City
```

El operando derecho de `iis` no puede ser un producto anónimo, una unión estructural, un diccionario, una expresión de tipo no nominal ni una identidad singleton como `Madrid`.

### `iis` en diccionarios funcionales

`iis` puede seleccionar una rama y estrecha `value` dentro de su resultado:

```mud
describe: Identifier --> Text [ordered] =
    value iis EmployeeId --> "Employee {value}",
    value iis PersonId --> "Person {value}",
    value is Identifier --> "Identifier {value}"
```

El orden es significativo porque un `EmployeeId` también satisface `value is PersonId`.

## Álgebra de diccionarios exactos

Los operadores `|`, `&`, `--` y `^` actúan sobre el dominio de claves de dos diccionarios exactos compatibles. Cuando una operación conserva una clave presente en ambos operandos, prevalece la asociación del operando izquierdo.

Sean:

```mud
left: Key -> Value =
    a -> 1,
    b -> 2

right: Key -> Value =
    b -> 9,
    c -> 3
```

### Unión exacta `|`

```mud
left | right
```

produce:

```mud
a -> 1,
b -> 2,
c -> 3
```

Formalmente:

```text
domain(L | R) = domain(L) ∪ domain(R)
(L | R)[k] = L[k] si k ∈ domain(L); R[k] en otro caso
```

No es necesariamente conmutativa como valor de diccionario.

### Intersección exacta `&`

```mud
left & right
```

produce:

```mud
b -> 2
```

Formalmente:

```text
domain(L & R) = domain(L) ∩ domain(R)
(L & R)[k] = L[k]
```

Tiene el mismo conjunto de claves que `R & L`, pero no necesariamente las mismas asociaciones.

### Diferencia exacta `--`

```mud
left -- right
```

produce:

```mud
a -> 1
```

Conserva las asociaciones izquierdas cuyas claves no aparecen a la derecha.

### Diferencia simétrica exacta `^`

```mud
left ^ right
```

produce:

```mud
a -> 1,
c -> 3
```

Solo conserva las claves presentes en exactamente un operando. `^` está admitido sobre diccionarios exactos aunque sus claves ya sean inherentemente únicas, porque opera sobre la pertenencia de claves y no exige reinterpretar la unicidad de los valores.

### Propiedades y orden

- `|` y `&` son asociativos y conmutativos respecto al conjunto de claves, pero no necesariamente como valores de diccionario por la precedencia izquierda.
- `--` no es asociativo ni conmutativo.
- `^` es asociativo y conmutativo.
- `L | R` conserva primero las asociaciones de `L` y añade después las claves nuevas de `R`.
- `L & R` y `L -- R` filtran `L` sin reordenarlo.
- `L ^ R` conserva primero las asociaciones exclusivas de `L` y después las exclusivas de `R`.
- Un criterio `ordered by` normaliza el contenido después de calcularlo.

### Interacción con `unique`

En un diccionario exacto `[unique]`, ningún valor puede quedar asociado a dos claves distintas. La operación incorpora primero las asociaciones izquierdas y después las derechas que correspondan. Una asociación derecha que violaría `unique` se omite como no-op y no produce `failed`.

```mud
left: Person -> Room [unique] =
    Ana -> BlueRoom

right: Person -> Room [unique] =
    Luis -> BlueRoom,
    Marta -> RedRoom
```

`left | right` produce `Ana -> BlueRoom, Marta -> RedRoom`.

Los tipos de clave y valor de ambos operandos deben ser compatibles. El resultado conserva los tipos comunes, la unicidad exigida, el orden demostrable y una cardinalidad derivada conservadoramente.

## Álgebra de diccionarios funcionales

Los operadores conjuntistas no comparan ni fusionan ramas, selectores, fallbacks u órdenes fuente. Su semántica es extensional y punto a punto sobre el resultado de aplicar ambos diccionarios a una misma entrada.

Para cualquier operador `op` entre `|`, `&`, `--` y `^`:

```text
(F op G)[x] = F[x] op G[x]
```

La operación de la derecha es el operador ordinario de colecciones. `F[x]` y `G[x]` se calculan sobre la misma entrada y la misma instantánea del mundo antes de combinarlos.

### Unión funcional `|`

```text
(F | G)[x] = F[x] | G[x]
```

Incluye los resultados producidos por cualquiera de los operandos. No existe precedencia izquierda entre resultados funcionales.

### Intersección funcional `&`

```text
(F & G)[x] = F[x] & G[x]
```

Conserva los resultados producidos por ambos.

### Diferencia funcional `--`

```text
(F -- G)[x] = F[x] -- G[x]
```

Retira de los resultados de `F` las multiplicidades producidas por `G`.

### Diferencia simétrica funcional `^`

```text
(F ^ G)[x] = F[x] ^ G[x]
```

Conserva los resultados producidos por exactamente uno de los dos operandos y mantiene las restricciones ordinarias de unicidad de la diferencia simétrica de colecciones.

### Orden y cardinalidad

Dos funcionales `ordered` producen individualmente como máximo un resultado. Su combinación conserva `ordered` solo cuando la cardinalidad máxima por aplicación continúa siendo `[0..1]`.

- `F | G` puede producir dos resultados distintos y pierde `ordered` en general.
- `F & G` produce como máximo uno y puede conservar `ordered`.
- `F -- G` produce como máximo el resultado de `F` y puede conservar `ordered`.
- `F ^ G` puede producir dos y pierde `ordered` en general.

Si uno o ambos operandos no son `ordered`, el compilador puede conservarlo únicamente cuando demuestre la misma cota máxima.

Para:

```text
F[x] : B [fmin..fmax]
G[x] : B [gmin..gmax]
```

se admiten inicialmente las aproximaciones conservadoras:

```text
F | G  : B [max(fmin, gmin)..fmax + gmax]
F & G  : B [0..min(fmax, gmax)]
F -- G : B [0..fmax]
F ^ G  : B [0..fmax + gmax]
```

El análisis puede estrecharlas con `unique`, dominios finitos o información de solapamiento demostrable.

### `unique`, fallback y dependencias

`unique` deduplica la colección producida por cada aplicación. Puede ser relevante al combinar dos funcionales `ordered`, aunque fuera redundante en cada operando aislado.

Los fallbacks pertenecen a cada operando. Se evalúan primero `F[x]` y `G[x]` con sus propias ramas y `_`; después se combinan los resultados. No se crea ni fusiona un fallback conjunto.

Las dependencias externas del compuesto son la unión de las dependencias transitivas de ambos operandos:

```text
dependencies(F op G) = dependencies(F) ∪ dependencies(G)
```

La operación continúa siendo pura y determinista respecto a la instantánea común.

### Igualdad

Definir la aritmética de forma extensional no convierte la igualdad general de funcionales en una prueba de equivalencia para todas las entradas. `F == G` continúa sujeto a las reglas nominales o estructurales que se definan separadamente.

## Restricciones comunes

- Solo se combinan diccionarios de la misma clase: exacto con exacto y funcional con funcional.
- No se combina directamente `->` con `-->`.
- Los tipos de entrada y salida deben ser compatibles.
- Los operadores son puros y no producen efectos.
- La evaluación conserva la instantánea y la atomicidad ordinarias.
- No se introduce un operador que seleccione el izquierdo si produce algo y el derecho en caso contrario.

## Representación sintáctica y semántica

El AST superficial conserva `iis` mediante:

```text
ExactTypeTestExpr(valueExpression, nominalTypeReference, negated)
```

- `negated = false` para `iis`.
- `negated = true` para `iis not`.

El operador derecho se resuelve durante la elaboración. Los tipos estructurales y las identidades singleton se rechazan durante tipado/elaboración antes de producir la forma correspondiente dla futura representación semántica posterior a tipado y elaboración.

Las operaciones conjuntistas pueden conservarse como `BinaryExpr` en el AST superficial porque su clase depende de los tipos resueltos. La futura representación semántica posterior a tipado y elaboración distingue:

```text
ExactDictionarySetOperationExpr(operator, left, right, resultType)
FunctionalDictionarySetOperationExpr(operator, left, right, resultType)
```

La aplicación del segundo nodo equivale a aplicar ambos operandos en la misma instantánea y ejecutar después la operación de colección. Nunca se materializa una lista fusionada de ramas ni se intenta demostrar equivalencia lógica entre selectores.

La futura representación semántica posterior a tipado y elaboración diferencia también:

```text
TypeTestExpr                # pertenencia transitiva de is
ExactNominalTypeTestExpr    # identidad nominal exacta de iis
```

## Diagnósticos requeridos

Una implementación debe diagnosticar, como mínimo:

- flecha usada como alternativa parcial de unión;
- alias cuya forma exterior efectiva es una flecha dentro de una unión;
- operando derecho no nominal de `iis`;
- identidad singleton a la derecha de `iis`;
- encadenamiento de `iis` o `iis not`;
- combinación de diccionario exacto y funcional;
- tipos de entrada incompatibles;
- tipos de salida incompatibles;
- pérdida demostrada de `ordered` cuando una forma declarada lo exige;
- uso de `^` cuando el tipo de colección resultante no satisface sus requisitos de unicidad.

La pérdida inferida de `ordered` no es un fallo por sí misma si el contexto permite el tipo no ordenado; sí debe explicarse en el diagnóstico de incompatibilidad cuando una anotación exterior exige conservarlo.

## Cierre de cobertura de D-085

Esta versión incorpora como parte de la misma unidad normativa las brechas documentales y mecánicas que habían quedado fuera de la primera integración de D-085. En particular, la conformidad debe cubrir también:

- llamada interna, inaccesibilidad raíz y rollback atómico de `subaction`;
- `not in` sobre `MudPath` y rechazo de encadenamientos;
- consulta, sustitución, iteración por claves y asociaciones, claves producto y no-op de `unique` en exactos;
- selectores explícitos de igualdad, pertenencia y condiciones booleanas; rechazo de selectores implícitos; fallback, lectura externa, aplicación sobre dominios y terminación de funcionales;
- cardinalidades y deduplicación de `FirstMatch` y `AllMatches`;
- aplicación encadenada y composición de diccionarios;
- compatibilidad estructural de productos y separación frente a aliases nominales;
- selección como filtro directo que no proyecta, aplana ni envuelve y que conserva asociaciones de exactos;
- errores `create Thing`, `destroy Thing` y `all Any`;
- catálogo, tipado, mutabilidad y advertencias de los metadatos postfix;
- inferencia de cardinalidad `[0]`, `[1]` y cardinalidades mayores, incluidos diccionarios como un único valor exterior;
- `iis` con especialización múltiple y narrowing exacto.

Los ejemplos normativos correspondientes pertenecen a los capítulos numerados 05 a 09. Los capítulos futuros enumerados en el índice deberán conservarlos o refinarlos al redactarse, pero no pueden remitir únicamente a este ADR.

## Consecuencias

- Las flechas mantienen una lectura uniforme y no pueden ocultarse dentro de uniones mediante aliases.
- `iis` permite ordenar ramas desde casos nominales exactos hasta pertenencias más generales sin confundir igualdad de valores.
- El álgebra exacta sigue la identidad de claves y conserva precedencia izquierda.
- El álgebra funcional compone políticas sin inspeccionar su implementación por ramas.
- La inferencia de orden y cardinalidad forma parte del tipo elaborado del resultado.
- Los ejemplos normativos de los capítulos numerados deben mostrar casos positivos, combinados e inválidos.

## Alternativas rechazadas

### Interpretar `F | G` como preferencia izquierda

Rechazada porque confundiría unión con una operación de fallback. La unión funcional combina colecciones de resultados.

### Fusionar ramas funcionales

Rechazada porque exigiría equivalencia lógica de selectores, tratamiento especial de `_` y normalización de órdenes fuente.

### Representar `iis` como `==` sobre descriptores de tipo expuestos

Rechazada porque filtraría una representación de implementación y perdería reglas de narrowing propias.

### Permitir flechas parentizadas dentro de uniones

Rechazada porque haría depender la consultabilidad de un diccionario de agrupaciones difíciles de elaborar y permitiría eludir la restricción mediante aliases.

## Verificación

La suite debe cubrir:

1. precedencia y asociación de flechas;
2. rechazo superficial y tras resolución de aliases;
3. `is`, `iis`, `iis not` y `==` sobre cadenas y diamantes de especialización;
4. narrowing positivo y negativo exacto;
5. las cuatro operaciones sobre diccionarios exactos con colisiones;
6. orden e interacción con `unique`;
7. las cuatro operaciones funcionales sobre resultados con y sin solapamiento;
8. pérdida y conservación de `ordered`;
9. unión de dependencias y misma instantánea;
10. rechazo de mezcla exacto/funcional;
11. AST e IR esperados sin fusión de ramas;
12. ausencia de las construcciones retiradas por D-085 en ejemplos válidos y esquemas;
13. llamada y rollback de `subaction`;
14. selectores, fallback, dependencias y terminación funcional;
15. selección directa, `Any`, metadatos y matriz de cardinalidad omitida;
16. casos positivos y negativos enumerados por el validador de cobertura D-086 v4.
