# ADR-061 — Resultados fallidos y plantillas `Text`

- Estado: Vigente
- Fecha: 2026-07-29
- Modifica: [[notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos|D-029]], [[notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas|D-035]], [[notas/decisiones/ADR-038-familias-cerradas-de-valores|D-038]], [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-048-azar-reproducible-y-fallos|D-048]], [[notas/decisiones/ADR-050-comentarios-terminadores-y-separadores-numericos|D-050]] y [[notas/decisiones/ADR-056-char-texto-y-orden-unicode|D-056]]
- Relacionada con: [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]]
- Preguntas relacionadas: Q-007, Q-059
- Documentos afectados: resultados de acción, reglas `always`, léxico, gramática, evaluación de `Text`, diagnósticos y frontera externa

## Contexto

El resultado público de una acción ya distingue `accepted`, `rejected` y `failed`, pero `failed` no transportaba todavía una explicación obligatoria. Las reglas `always` podían provocar ese resultado sin declarar el diagnóstico propio de la invariante.

Al mismo tiempo, los literales `Text` necesitan incorporar valores sin recurrir a concatenaciones manuales ni confundir una declaración con el valor que una expresión produce.

## Decisión

### Resultado externo de una acción

Una solicitud de acción devuelve al invocador externo un objeto con una de estas formas:

```text
{ state: accepted }
{ state: rejected }
{ state: failed, reason: Text }
```

El campo `reason` es obligatorio exactamente cuando `state` es `failed`. Todo caso normativo capaz de producir un `failed` semántico debe definir un diagnóstico humano de tipo `Text` que explique su causa. La implementación puede conservar además código estable, ancla, procedencia, onda, traza y causas estructuradas, pero ninguna de esas propiedades sustituye al `reason`.

Cuando concurren varias causas, el objeto continúa exponiendo un único `reason` que las representa. Q-007 debe fijar la estructura y el orden canónicos de esa agregación, además de la frontera externa de límites de recursos y defectos del runtime.

Los errores estáticos y los fallos técnicos no se convierten por ello en resultados de acción. Toda superficie que los publique debe acompañarlos también de un texto humano, pero conserva su categoría propia.

El resultado externo no es todavía un valor ordinario de MUD. En particular, una acción no puede invocarse dentro de una expresión ni de una interpolación. Q-059 conserva abierta su observación explícita desde tests.

### Diagnóstico obligatorio de `always`

Toda regla `always` declara una condición pura y un diagnóstico `Text` obligatorio mediante `otherwise`:

```mud
always rule ValidPopulation on kingdom: Kingdom {
    kingdom.population >= 0
    otherwise "Population cannot be negative in {kingdom}"
}
```

El diagnóstico se evalúa de forma perezosa, solo cuando la condición es falsa, con las mismas vinculaciones y sobre el mismo estado tentativo que infringe la invariante. Su valor se incorpora como causa del `failed`. No puede producir efectos.

Si la evaluación del propio diagnóstico falla, la infracción original no desaparece ni se transforma en `rejected`: el runtime produce el diagnóstico canónico correspondiente al fallo de explicación y conserva la causa original en su información estructurada.

### Plantillas `Text`

Los literales ordinarios y multilínea de `Text` son plantillas. Dentro de ellos:

- `{e}` evalúa la expresión MUD `e` e inserta la representación textual de su valor;
- `anchor{d}` inserta el ancla canónica de la entidad designada por `d`;
- `\{` y `\}` insertan llaves literales;
- una llave sin escapar que no forme un hueco válido es un error;
- `\u{...}` continúa siendo un escape Unicode indivisible y no abre un hueco.

`anchor` es contextual únicamente dentro de una plantilla y no se convierte en palabra reservada general. Fuera de ella puede seguir siendo un identificador ordinario.

El scanner usa una pila de modos: el contenido de `{...}` vuelve al léxico ordinario de expresiones y sus delimitadores se equilibran normalmente. Un literal `Text` anidado dentro de esa expresión abre a su vez su propio modo de plantilla. El salto o fin de archivo solo puede cerrar implícitamente un texto ordinario cuando no queda ningún hueco abierto.

### Valores renderizables

La representación de un hueco depende del valor evaluado, no del nombre escrito:

| Valor | Representación |
| --- | --- |
| `Text` | Sus caracteres, sin comillas |
| `Char` | El escalar que contiene |
| `Bool` | `true` o `false` |
| Número básico | Su representación numérica canónica o el formato explícito |
| `thing` | El nombre nominal de la `thing` almacenada |
| Miembro de `family` | El nombre nominal del miembro |
| Intervalo | Su forma canónica normalizada |
| Colección | Sus elementos separados por `, `, sin los corchetes exteriores |

Si un elemento de una colección es a su vez una colección, esa colección interior conserva sus corchetes. La regla se aplica recursivamente:

```mud
"{[1, 2, 3]}"          # 1, 2, 3
"{[[1, 2], [3, 4]]}"   # [1, 2], [3, 4]
```

Una colección vacía aporta el texto vacío. `ordered`, `unique`, `mut` y la cardinalidad pertenecen al tipo o forma de colección y no se imprimen. Una colección ordenada usa su orden; una no ordenada usa su enumeración canónica.

Una llamada a regla booleana es renderizable porque produce `Bool`. El nombre desnudo de una declaración no es un valor. Acciones, reglas reactivas, reglas `always`, `look`, `message` y `test` no producen valores interpolables. Los tipos, familias como declaraciones y cualquier otra categoría sin representación decidida producen error estático en `{...}`.

### Formato numérico

Un hueco numérico admite:

```text
{e:izquierda}
{e::derecha}
{e:izquierda:derecha}
```

`izquierda` y `derecha` son enteros naturales escritos en decimal:

- `izquierda` fija el mínimo de cifras a la izquierda del punto y rellena con ceros; el signo no cuenta y nunca se eliminan cifras si el valor excede ese mínimo;
- `derecha` fija exactamente las cifras a la derecha del punto, añade ceros o redondea al más cercano con empates al par conforme a D-034;
- si `derecha` es cero, no se escribe punto decimal.

La precisión izquierda se admite para todos los tipos numéricos básicos. La precisión derecha solo se admite para los tipos que pueden mostrar parte fraccionaria: `Number`, `Rumber` y `Money`. El formato modifica exclusivamente el `Text` producido, nunca el valor ni su tipo.

```mud
count: Natural = 12
ratio: Number = 12.3

"{count:4}"     # 0012
"{ratio::2}"    # 12.30
"{ratio:4:2}"   # 0012.30
```

Aplicar un formato numérico a otro tipo o escribir una especificación incompleta es un error estático.

La propiedad `format` de una magnitud `point over` usa esta misma sintaxis, no un segundo lenguaje de llaves. Sus nombres como `hour`, `minute` o `second` se resuelven en el entorno contextual pendiente de Q-055; `{hour:2}` solicita dos posiciones a la izquierda.

### Interpolación de anclas

`anchor{...}` es una forma contextual de plantilla, no una función general ni una conversión a `Text`. Admite una referencia a una entidad semántica con ancla o una expresión cuyo valor tenga identidad nominal anclada. Por ejemplo:

```mud
"Rule: anchor{CanRecruit}"
"Kingdom: {kingdom}; identity: anchor{kingdom}"
```

Esto permite mencionar acciones, reglas, `look`, `message`, tests y tipos sin convertir sus declaraciones en valores ordinarios. Una expresión cuyo resultado carezca de ancla produce error estático.

## Consecuencias

- El AST distingue fragmentos literales, huecos de valor, especificaciones numéricas y huecos de ancla.
- El IR conserva la expresión, el formato y la procedencia de cada fragmento.
- El lexer necesita modos anidados para texto y código.
- `otherwise` continúa siendo opcional en aserciones de test, pero es obligatorio en reglas `always`.
- El catálogo de fallos debe proporcionar una razón humana para cada `failed`.
- La renderización contextual no introduce una conversión implícita general a `Text`.

## Verificación

1. Resultado externo `failed` con `reason` obligatorio y ausencia del campo en los otros dos estados.
2. Rechazo de una regla `always` sin `otherwise` o con diagnóstico que no sea `Text`.
3. Evaluación perezosa del diagnóstico sobre el estado tentativo infractor.
4. Interpolación ordinaria y multilínea con expresiones anidadas.
5. Escapes `\{`, `\}`, `\"`, `\'` y `\u{...}`.
6. Renderización de `thing`, miembros de `family`, reglas booleanas, intervalos y colecciones anidadas.
7. Rechazo de declaraciones y constructos sin valor dentro de `{...}`.
8. Formatos `{n:4}`, `{n::2}` y `{n:4:2}`, incluidos cero, signo, relleno, exceso de cifras y redondeo al par.
9. Obtención de anclas de declaraciones y valores nominales mediante `anchor{...}`.
10. Rechazo de `anchor{...}` sobre valores sin identidad anclada.
