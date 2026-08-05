---
id: D-085
title: "Diccionarios decisionales, metadatos y activación estructurada"
status: vigente
date: 2026-08-05
supersedes: []
superseded-by: []
questions: []
affects:
  - "acciones y subacciones, organización de archivos, operadores, tipos, diccionarios, productos, ausencia, cardinalidad, selección, activación inicial, Thing, Any, metadatos, magnitudes, texto, gramática, CST, AST, IR y diagnósticos"
---

# ADR-085 — Diccionarios decisionales, metadatos y activación estructurada

- Modifica: [[ADR-017-valor-predeterminado-de-todo-tipo|D-017]], [[ADR-035-organizacion-nombres-using-y-anclas|D-035]], [[ADR-037-campos-y-dominios-declarativos|D-037]], [[ADR-039-colecciones-y-diccionarios|D-039]], [[ADR-042-acciones-raiz-y-resultados|D-042]], [[ADR-047-cuantificadores-e-iteracion-finita|D-047]], [[ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]], [[ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]], [[ADR-061-resultados-fallidos-y-plantillas-text|D-061]], [[ADR-068-thing-universal-y-nombre-intrinseco|D-068]], [[ADR-074-uniones-nominales-y-estrechamiento|D-074]], [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]], [[ADR-083-magnitudes-base-sin-unidades|D-083]] y [[ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]].
- Amplía: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]], [[ADR-052-pipeline-materializadores-y-conformidad|D-052]] y [[ADR-053-operador-semantico-y-flujo-de-autoria|D-053]].
- Documentos afectados: capítulos 05 a 09, futuros capítulos 10 a 20, 24, 26, 32, 34 y 38, gramática, modelos sintácticos, diagnósticos y operaciones semánticas.

## Contexto

MUD ya dispone de colecciones, diccionarios exactos, acciones compuestas, nombres nominales, activación inicial y plantillas `Text`. Varias decisiones posteriores muestran cuatro necesidades relacionadas:

1. Expresar políticas puras definidas por casos sin introducir una categoría general de función.
2. Separar de manera uniforme el contenido del mundo de los metadatos nominales y de procedencia.
3. Permitir que ausencia y cardinalidad modelen consultas parciales sin convertir la falta de resultado en fallo inmediato.
4. Hacer explícitas las fronteras entre API pública, auxiliares internas y catálogos iniciales de `thing` y reglas.

Esta decisión consolida esas necesidades y reemplaza toda formulación anterior incompatible dentro de su alcance. Los ADR modificados conservan el historial de las reglas previas.

## Decisión

### Acciones auxiliares `subaction`

Una declaración `subaction` posee el mismo contrato de participantes, `given`, guardas, efectos, postcondiciones, atomicidad y anclaje que una `action`, con una diferencia de accesibilidad:

```mud
subaction RemoveMoney for account: Account [mut]
given amount: Money {
    then account.balance -= amount
}
```

- Una `subaction` solo puede invocarse desde el cuerpo de otra `action` o `subaction`.
- No puede constituir una solicitud externa, un comando raíz ni una entrada de la API pública.
- Una `action` ordinaria puede invocar acciones ordinarias y subacciones.
- Una `subaction` puede invocar acciones ordinarias y subacciones, sujeta al mismo análisis de aciclicidad.
- Toda la cadena participa en una única resolución atómica. Un resultado no aceptado o un fallo de cualquier llamada interna descarta también los efectos privados anteriores de sus llamadores.
- Su ancla conserva la categoría `action::*`; la clase pública o auxiliar forma parte del descriptor, no del prefijo de ancla.

El AST superficial conserva explícitamente la clase `PublicAction` o `Subaction`. La comprobación de accesibilidad se realiza después de resolver la llamada.

### Organización editorial de archivos

Los archivos deberían agrupar preferentemente conceptos, lugares, procesos o situaciones del mundo, no categorías sintácticas. Un archivo como `battle.mud` puede reunir `thing`, aliases, reglas, acciones, vistas y mensajes que describan conjuntamente la batalla.

Esta regla es informativa y no afecta a resolución, identidad, conformidad ni anclas. Una relación transversal puede ocupar un archivo propio cuando represente mejor el dominio.

### Operador `not in`

`not in` es la negación canónica de pertenencia. Se tokeniza como las dos palabras reservadas `not` e `in`, forma un único operador de comparación y tiene la misma precedencia y restricciones de encadenamiento que `in`.

No equivale a aplicar el prefijo `not` a una expresión incompleta. El AST conserva `NotMembership` como operador propio.

### Diccionarios exactos

El tipo ordinario conserva la forma:

```mud
A -> B
```

Una asociación se escribe `a -> b` y es un valor operativo. Puede aparecer en un literal de diccionario o añadirse de forma explícita:

```mud
add (a -> b) to dictionary
```

Los paréntesis pueden omitirse cuando la precedencia no resulte ambigua.

La aplicación por clave exacta es parcial:

- una clave presente produce su valor asociado;
- una clave ausente produce `empty` con la forma de salida declarada;
- la ausencia no produce `failed` por sí misma;
- el fallo aparece únicamente cuando el resultado vacío no pertenece al tipo, dominio o cardinalidad exigidos por el contexto.

Los diccionarios exactos:

- conservan mutabilidad exterior;
- continúan siendo enumerables por claves o asociaciones;
- admiten `ordered` con su semántica ordinaria;
- admiten `unique`, que exige unicidad global de valores asociados.

Una inserción o sustitución que haría aparecer el mismo valor bajo más de una clave en un diccionario exacto `unique` es una no-op completa. No modifica ninguna asociación y no produce `failed`.

### Diccionarios decisionales

El tipo:

```mud
A --> B
```

representa una política pura definida por ramas. Una rama se escribe:

```mud
selector --> result
```

Dentro del selector y del resultado, `value` es una palabra contextual vinculada a la entrada de tipo `A`.

El selector se elabora así:

- un valor suelto equivale a `value == selector`;
- un intervalo equivale a `value in selector`;
- una expresión booleana explícita puede usar `value` y cualquier operación pura admitida;
- `_` es el fallback y solo se considera cuando ninguna rama ordinaria aplicable ha producido resultado.

Los resultados y selectores pueden leer estado externo. Cada lectura debe quedar registrada como dependencia de la rama y del diccionario. Todas las llamadas transitivas de una aplicación observan la misma instantánea estable del mundo.

Las ramas son estáticas durante la ejecución ordinaria y no admiten efectos, llamadas a acciones, asignaciones, `create`, `destroy` ni mutación. El operador semántico o la edición del modelo pueden crear, actualizar, retirar o mover ramas mediante sus anclas propias. Una rama nueva se inserta antes de `_` de forma predeterminada; en un decisional ordenado puede declararse una posición concreta.

Un diccionario decisional:

- no admite mutabilidad exterior;
- no admite capacidad interior `[mut]`;
- rechaza estáticamente cualquier `mut` aplicado a su tipo o lugar;
- no es una fuente de `for each`;
- puede referenciar directa o indirectamente otros diccionarios decisionales.

Todo componente recursivo del grafo de llamadas debe disponer de una medida bien fundada que disminuya estrictamente en cada arista que continúe el ciclo. El compilador debe demostrar la terminación mediante descenso numérico, reducción de cardinalidad, subestructuras estrictamente menores u otra prueba equivalente. La ausencia de prueba es un error estático.

#### Modo `ordered`

```mud
A --> B [ordered]
```

- Las ramas ordinarias se prueban en orden fuente.
- Gana la primera coincidencia.
- Los selectores pueden solaparse y el orden forma parte del valor.
- `_` debe ser la última rama efectiva; toda rama posterior es inalcanzable.
- Sin coincidencia ni fallback, la aplicación tiene cardinalidad derivada `[0..1]` y produce `empty` cuando no hay resultado.
- Con fallback, la cardinalidad derivada es `[1]`.
- `unique` es válido pero redundante; produce una sugerencia de eliminación.

El modo elaborado se denomina `FirstMatch`.

#### Modo no ordenado

```mud
A --> B
```

- Se evalúan todas las ramas ordinarias.
- Cada rama coincidente aporta un resultado.
- Los selectores pueden solaparse.
- El orden fuente no es semántico.
- Sin coincidencias se obtiene la colección vacía.
- `_` aporta exactamente un resultado solo cuando ninguna rama ordinaria coincide.
- La cardinalidad derivada es `[0..n]`, donde `n` es la cota máxima demostrable de ramas ordinarias coincidentes; con fallback la cota inferior pasa a `1`.
- `unique` deduplica resultados producidos por ramas distintas.

El modo elaborado se denomina `AllMatches`.

### Flechas, composición y productos

`->` y `-->` aceptan expresiones de tipo completas a ambos lados. Las cadenas son asociativas a la derecha:

```mud
A -> B -> C
```

se elabora como `A -> (B -> C)`. Lo mismo se aplica a cadenas mixtas. Cada cardinalidad o modificador pertenece exclusivamente a la flecha inmediatamente anterior:

```mud
A -> B [2] -> C [3]
```

se elabora como `A -> (B -> C [3]) [2]`.

Los paréntesis continúan siendo obligatorios para cambiar esa agrupación, para usar un diccionario completo como clave o para aplicar una colección exterior al valor diccionario completo.

No se introduce una categoría separada de función. La composición se expresa aplicando el resultado de un diccionario como entrada de otro; la aplicación encadenada `table[a][b]` consume diccionarios anidados.

Se añaden productos estructurales anónimos:

```mud
(A, B)
(a: A, b: B)
```

Sus valores se escriben respectivamente `(x, y)` y `(a = x, b = y)`. Son estructurales y se comparan componente a componente. Los nombres de variables que ocupan un producto posicional no crean nombres de componente. Los aliases declarados continúan siendo nominales aunque su representación coincida con un producto anónimo.

Los productos pueden actuar como claves exactas o entradas decisionales.

### `empty`, consultas parciales y cardinalidad

`empty` representa ausencia o colección vacía y no es un fallo por sí mismo. Toda operación parcial debe producir `empty` cuando no existe resultado. La comprobación posterior contra el tipo, dominio y cardinalidad esperados decide si esa ausencia es válida o causa `failed`.

Una consulta exacta ausente conserva la forma de salida `B`. Una consulta decisional `FirstMatch` sin coincidencia produce `empty`; una consulta `AllMatches` sin coincidencias produce una colección vacía válida.

### Cardinalidad omitida de campos almacenados

La omisión de cardinalidad ya no se normaliza universalmente a `[1]` antes de conocer el contexto del campo.

- En un campo almacenado sin mutabilidad exterior y con inicializador, se infiere la cardinalidad exterior exacta del valor inicial.
- Un valor unitario infiere `[1]`, una colección literal de tres miembros infiere `[3]` y `empty` infiere `[0]`.
- El contenido interno de un diccionario no altera la cardinalidad exterior: un diccionario es un valor aunque contenga varias asociaciones o ramas.
- En un campo con mutabilidad exterior, la omisión conserva `[1]`.
- Un campo almacenado sin inicializador usa la regla ordinaria del tipo y de su predeterminado, salvo las excepciones explícitas como `Any`.
- Los campos calculados `:=` conservan la forma inferida de su expresión o la forma declarada.

Cuando la cardinalidad inferida de un campo inmutable sea distinta de `[1]`, el compilador emite una sugerencia no bloqueante con una corrección que materializa la cardinalidad exacta en el texto fuente.

La AST superficial conserva que la cardinalidad fue omitida; la elaboración resuelta registra la cardinalidad efectiva y su procedencia `InferredFromInitializer`, `OrdinaryScalarDefault` o `Explicit`.

### Selección

La expresión:

```mud
binding in source: predicate
```

es exclusivamente un filtro. El cuerpo posterior a `:` debe ser booleano. La expresión devuelve directamente los miembros originales aceptados, sin proyección, envoltura adicional ni aplanamiento.

Conserva multiplicidad, `unique`, orden, criterio de orden y la inferencia conservadora de cardinalidad de la fuente. Sobre un diccionario exacto, una vinculación por pareja produce otro diccionario con las asociaciones aceptadas.

### Activación inicial estructurada

La única forma de `start with` contiene dos secciones obligatorias y separadas:

```mud
start with {
    things {
        ...
    }

    rules {
        ...
    }
}
```

No existe la forma mezclada ni azúcar equivalente. Cada expresión de una sección aporta cero, una o varias identidades del universo correspondiente:

- una referencia individual aporta una;
- `empty` aporta cero;
- una colección aporta directamente sus miembros;
- una colección de colecciones es inválida: solo se incorpora un nivel de contribuciones.

Las identidades repetidas se deduplican y el orden no es observable. En `things`, `all` denota el catálogo estático de declaraciones `thing` activables. En `rules`, `all` denota el catálogo estático de reglas activables. Las expresiones se evalúan solo con metadatos y propiedades disponibles estáticamente; no pueden leer estado runtime todavía inexistente.

El AST conserva `things` y `rules` como conjuntos separados de expresiones de contribución. La elaboración comprueba categoría, profundidad y evaluabilidad estática.

### `Thing` y `Any`

`Thing` continúa siendo la raíz incorporada de todas las `thing`. Está siempre efectiva, no aparece en `start with`, no puede declararse, crearse ni destruirse y queda excluida del catálogo producido por `all` en una sección `things`.

Se incorpora el tipo superior `Any` para todos los valores MUD del proyecto. Su dominio abierto incluye tipos básicos —incluido `Money`—, identidades `thing`, aliases, miembros de familia, magnitudes, intervalos, colecciones, diccionarios y productos estructurales. No incluye acciones, reglas, tests, declaraciones ni nodos sintácticos como valores ordinarios.

`Any`:

- no es enumerable y rechaza `all Any`;
- no posee un orden total universal;
- compara igualdad solo entre tipos efectivos compatibles y delega en su igualdad;
- exige estrechamiento antes de una operación específica;
- conserva el estrechamiento dentro de la rama decisional donde se demostró;
- no posee predeterminado universal.

`Any` es una excepción explícita a D-017. Todo campo almacenado de tipo `Any` requiere inicializador explícito.

### Metadatos postfix

El acceso a metadatos usa el operador postfix `~` sin punto:

```mud
value~name
value~path
value~anchor
value~file
```

`value.~name` es inválido. El operador distingue metadatos nominales o de procedencia de campos ordinarios del mundo y tiene la misma precedencia postfix que `.`, `[]` y llamadas.

Los tipos incorporados iniciales son:

- `Name` para `~name`;
- `MudPath` para `~path`;
- `Anchor` para `~anchor`;
- `MudFile` para `~file`.

Son tipos nominales, no aliases implícitos de `Text`. Pueden declarar conversiones explícitas a `Text`. Las plantillas pueden renderizarlos contextualmente sin introducir compatibilidad nominal general.

#### `~name`

Se elimina la propiedad intrínseca `.name` y la forma especial `name = ...`. El metadato de presentación se declara o sobrescribe como:

```mud
~name = "El Castillo Negro"
```

Si se omite, su valor inicial deriva del nombre nominal no cualificado. `~name` no modifica identificador fuente, igualdad, orden nominal, `~anchor`, `~path` ni `~file`.

`~name` es mutable para `thing`, declaraciones alias y miembros de `family`. Una escritura runtime usa el objetivo postfix:

```mud
Nora~name = "Nora la Roja"
```

La escritura exige la capacidad correspondiente y participa en la atomicidad y conflictos como una escritura de estado del propietario. En aliases y miembros de familia se almacena separada del payload inmutable; cambiarla no cambia igualdad estructural ni datos asociados.

La interpolación ordinaria de esos valores usa su `~name` efectivo.

#### Identidad y procedencia

`~anchor`, `~path` y `~file` son inmutables y no asignables. `~anchor` produce el ancla pública canónica; `~path`, el path MUD; `~file`, la procedencia física.

`~file` puede participar en cualquier expresión válida, pero el compilador emite un aviso cuando escapa de presentación o logging, o cuando su dependencia puede alterar comportamiento del mundo. El uso continúa siendo válido.

Sobre valores `MudPath`, `in` es reflexivo y compara segmentos completos: `p in q` es cierto si `p == q` o si `p` es descendiente de `q`.

#### Magnitudes y unidades

Las propiedades especiales de magnitudes y unidades usan la misma familia de metadatos:

```mud
~name = "metro"
~plural = "metros"
~abbreviation = "m"
~prefixes = all
~format = "{hour:2}:{minute:2}:{second:2}"
```

Cada metadato conserva su tipo, mutabilidad y restricciones propias. El prefijo `~` no implica mutabilidad.

### Plantillas y anclas

Se elimina `anchor{expression}`. El ancla se interpola mediante una expresión ordinaria:

```mud
"{expression~anchor}"
```

`~anchor` es además un valor tipado utilizable fuera de plantillas. El AST de plantilla conserva solo fragmentos e interpolaciones de valor; desaparece `AnchorInterpolation` y el token especial correspondiente.

## Modelo sintáctico y semántico

La gramática y los modelos deben distinguir como mínimo:

- `ActionDecl(PublicAction | Subaction, ...)`;
- `ExactDictionaryType` y `DecisionDictionaryType`;
- asociaciones exactas y ramas decisionales;
- productos posicionales y nombrados;
- `MetadataAccessExpr` y objetivos asignables de metadato;
- `NotMembership`;
- conjuntos separados de activación de `thing` y reglas;
- cardinalidad omitida frente a explícita;
- ausencia del antiguo nombre intrínseco y de la interpolación especial de ancla.

El AST resuelto o IR registra para cada decisional:

- modo `FirstMatch` o `AllMatches`;
- orden semántico;
- fallback;
- unicidad de resultados;
- cardinalidad derivada de aplicación;
- dependencias externas de selectores y resultados;
- ancla estable de cada rama;
- evidencia de terminación de cada componente recursivo.

Los diagnósticos mínimos nuevos son:

1. solicitud externa de una `subaction`;
2. llamada a `subaction` fuera de acción o subacción;
3. `mut` exterior o interior en `-->`;
4. `_` no final o ramas inalcanzables en `FirstMatch`;
5. `unique` redundante en `FirstMatch`;
6. intento de iterar un decisional;
7. ciclo decisional sin prueba de descenso;
8. cardinalidad inmutable inferida distinta de `[1]`;
9. `all Any` o enumeración de `Any`;
10. campo `Any` sin inicializador;
11. asignación a metadato inmutable;
12. uso semánticamente frágil de `~file`;
13. forma retirada `.name`, `name =` o `anchor{...}`;
14. forma mezclada retirada de `start with`.

## Consecuencias

- MUD obtiene políticas puras por casos sin introducir funciones generales.
- La ausencia se conserva hasta que un contrato exterior exige presencia.
- La API externa distingue acciones públicas de auxiliares atómicas.
- La activación inicial no mezcla categorías y admite selecciones estáticas composables.
- Identidad, presentación y procedencia quedan separadas y tipadas.
- Las flechas y productos permiten claves y políticas estructurales sin debilitar la nominalidad de aliases.
- `Any` sirve como frontera universal de valores sin inventar enumeración, orden ni predeterminado universales.

## Alternativas descartadas

### Hacer fallar inmediatamente una consulta parcial

Se descarta porque duplica en el operador una restricción que ya expresa la cardinalidad esperada y rompe la composición con filtros, fallbacks y tipos opcionales.

### Introducir una categoría general de función

Se descarta porque las políticas requeridas son valores declarativos, inspeccionables y editables por ramas. Los diccionarios decisionales conservan esa estructura explícita.

### Conservar `.name` y `anchor{...}` como excepciones

Se descarta porque obliga a mantener dos mecanismos paralelos para información que pertenece a una misma dimensión de metadatos.

### Hacer `Any` enumerable o darle un predeterminado arbitrario

Se descarta porque el dominio depende del proyecto, mezcla categorías sin un orden universal y no contiene un valor distinguido estable.

## Verificación

La suite debe cubrir al menos:

1. Accesibilidad externa e interna de `action` y `subaction`, ancla compartida y rollback completo.
2. Tokenización maximal-munch de `-->`, `--` y `->`, y parseo de `not in`.
3. Consulta ausente exacta, asociación operativa y `unique` de valores como no-op.
4. Modos decisionales, solapamiento, fallback, cardinalidad derivada, deduplicación y prohibición de mutación o iteración.
5. Terminación aceptada y rechazada de ciclos decisionales y lectura de una sola instantánea.
6. Cadenas de flechas puras y mixtas con modificadores ligados a su flecha.
7. Productos posicionales y nombrados, igualdad estructural y uso como clave o entrada.
8. Inferencia `[0]`, `[1]` y `[n]` de campos almacenados inmutables, sugerencia de explicitación y excepción mutable.
9. Selección sin envoltura, proyección ni flatten, incluida la pareja de diccionario.
10. `start with` por secciones, `empty`, colecciones de un nivel, deduplicación, `all` contextual y rechazo de colecciones anidadas.
11. Efectividad permanente y exclusión catalográfica de `Thing`.
12. `Any`, estrechamiento, igualdad compatible, rechazo de enumeración y exigencia de inicializador.
13. Lectura, escritura y tipos de metadatos; inmutabilidad de identidad y aviso de `~file`.
14. Pertenencia reflexiva y segmentada de `MudPath`.
15. Metadatos de unidades y magnitudes.
16. Retirada de `.name`, `name =` y `anchor{...}` y sustitución por `~name` y `~anchor`.
