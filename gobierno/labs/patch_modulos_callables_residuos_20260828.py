from pathlib import Path

ROOT = Path.cwd()


def rewrite(rel: str, old: str, new: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"{rel}: bloque esperado no encontrado")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# Modelo matemático: activación modular y tests con cierre estático.
rewrite(
    "especificacion/04-modelo-matematico.md",
    "19. Una única declaración global `start with` determina por separado contribuciones finitas y no ordenadas de `thing` y reglas inicialmente activas mediante las secciones `things { ... }` y `rules { ... }`.\n20. Cada contribución es una expresión estática que produce una declaración o una colección plana de declaraciones de la categoría correspondiente; no admite instrucciones, efectos ni colecciones anidadas.\n21. Si se omite `start with`, ambas contribuciones están vacías. `Thing` continúa siempre efectiva y no forma parte de la colección activable ni del resultado de `all`.\n22. Cada test construye un mundo fresco y aislado cuyo `start with` local sustituye al global.\n23. Los tests no son declaraciones activables ni forman parte del mundo o de su API pública.",
    "19. Cada módulo puede aportar como máximo un `start with`; sus contribuciones finitas y no ordenadas reúnen en una sola superficie declaraciones activables `thing | rule`, y las contribuciones de todos los módulos se materializan conjuntamente antes de la estabilización inicial.\n20. Cada contribución es una expresión estática que produce una declaración activable o una colección plana de ellas; no admite instrucciones, efectos ni colecciones anidadas.\n21. Si un módulo omite `start with`, su contribución es vacía. `Thing` continúa siempre efectiva y no forma parte de la colección activable ni de la enumeración materializada por `all Thing`.\n22. Cada test construye un mundo fresco y aislado; antes del test raíz se calcula el cierre transitivo estático de tests alcanzables y se unen sus contribuciones `start with`.\n23. Los tests no son declaraciones activables ni forman parte del mundo o de la API pública del host; su visibilidad entre módulos existe únicamente en contexto de tests.",
)
rewrite(
    "especificacion/04-modelo-matematico.md",
    "start with {\n        Alexandria,\n        empty\n    }",
    "start with {\n    Alexandria,\n    empty\n}",
)

# Léxico: things/rules dejan de ser etiquetas contextuales y all también tiene forma prefija.
rewrite(
    "especificacion/06-lexico.md",
    "- `things` y `rules` como etiquetas obligatorias de sus secciones de `start with`.\n",
    "",
)
rewrite(
    "especificacion/06-lexico.md",
    "`all` es un literal contextual que requiere un dominio enumerable esperado. Su carácter reservado permite distinguirlo de una declaración ordinaria aun antes del tipado.",
    "`all` es una palabra reservada que sirve tanto como literal contextual sin operando, cuyo dominio enumerable se obtiene del contexto, como prefijo `all D` para materializar explícitamente un dominio enumerable. Su carácter reservado permite distinguir ambas formas de una declaración ordinaria aun antes del tipado.",
)
rewrite(
    "especificacion/gramatica/mud-lexico.ebnf",
    '    ::= "abstract" | "always" | "start"\n      | "things" | "rules" | "value"',
    '    ::= "abstract" | "always" | "start"\n      | "value"',
)

# Proyección CST/AST y caso de defaults: retirar semántica obsoleta sin perder cobertura.
rewrite(
    "especificacion/sintaxis/cst-a-ast-superficial.md",
    "9. `start with` produce `StartSet(things, rules)` sin mezclar contribuciones.",
    "9. `start with` produce `StartSet(contributions)` con una única secuencia de contribuciones; la categoría activable se comprueba durante elaboración.",
)
rewrite(
    "especificacion/sintaxis/casos/cst-ast.yaml",
    "- id: metadata-file-defaults\n  category: metadata\n  source: '~private = true\n\n\n    thing Cache {}\n\n    '\n  cst_root: MudFileSyntax\n  ast: MudFile(metadataDefaults=[private])\n  produces_ast: true",
    "- id: metadata-file-defaults\n  category: metadata\n  source: '~summary = \"internal cache\"\n\n\n    thing Cache {}\n\n    '\n  cst_root: MudFileSyntax\n  ast: MudFile(metadataDefaults=[summary])\n  produces_ast: true",
)

# D-021: start with unificado.
rewrite(
    "notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension.md",
    "Las declaraciones presentes al comienzo se separan por categoría conforme a D-085:\n\n```mud\nstart with {\n    things {\n        Kingdom,\n        Place\n    }\n\n    rules {\n        CanEnter\n    }\n}\n```\n\nNo existe una forma plana que mezcle `thing` y reglas en un mismo conjunto.",
    "Las declaraciones presentes al comienzo se aportan mediante el `start with` unificado de D-096:\n\n```mud\nstart with {\n    Kingdom,\n    Place,\n    CanEnter\n}\n```\n\nLas contribuciones pueden mezclar declaraciones activables `thing | rule`; se deduplican y su orden no es semántico.",
)

# D-036 y D-063: on directo sobre things; on relacionado sobre fuente finita enumerable.
rewrite(
    "notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md",
    "Un rol `for` admite cualquier `declared-type`, incluidos tipos básicos, aliases, familias, diccionarios y `thing`, un dominio `in` y la especificación completa de colección. El dominio restringe los valores admisibles del rol y se escribe entre el tipo y la especificación de colección. La cardinalidad omitida equivale a `[1]` conforme a D-039. `on` continúa vinculando una sola `thing` por rol y no admite otros tipos, cardinalidad ni los modificadores de colección `unique` u `ordered`.",
    "Un rol `for` admite cualquier `declared-type`, incluidos tipos básicos, aliases, familias, diccionarios y `thing`, un dominio `in` y la especificación completa de colección. El dominio restringe los valores admisibles del rol y se escribe entre el tipo y la especificación de colección. La cardinalidad omitida equivale a `[1]` conforme a D-039. Un rol `on` vincula un único valor por vinculación y no admite cardinalidad ni los modificadores de colección `unique` u `ordered`: la forma directa sin `in` usa el universo implícito de `thing` concretas activas; la forma relacionada `nombre[: Tipo] in fuente` puede tomar miembros de una fuente finita enumerable conforme a D-096.",
)
rewrite(
    "notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md",
    "`on` continúa vinculando exclusivamente `thing` individuales. Para cada rol `r` cuyo tipo efectivo sea `T`, su universo es el conjunto finito de `thing` concretas y activas de la instantánea leída que satisfacen `is T`.\n\nSea `r_1,\\ldots,r_n` el orden textual de los roles y sean `U_1,\\ldots,U_n` sus universos. La cabecera denota el conjunto:",
    "`on` vincula un valor individual por rol. En una forma directa sin `in`, el universo del rol es el conjunto finito de `thing` concretas y activas de la instantánea leída que satisfacen su tipo efectivo. En una forma relacionada `nombre[: Tipo] in fuente`, el universo procede de los miembros de esa fuente finita enumerable y la anotación opcional actúa como refinamiento. Un tipo sin universo implícito finito, por ejemplo `Nat`, no puede usar la forma directa.\n\nSea `r_1,\\ldots,r_n` el orden textual de los roles y sean `U_1,\\ldots,U_n` sus universos así obtenidos. La cabecera denota el conjunto:",
)
rewrite(
    "notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md",
    "Una vinculación es una asignación total de roles. No se impone desigualdad implícita: dos roles pueden recibir la misma `thing` si satisfacen sus restricciones.\n\nLos roles también conservan orientación. Si una relación simétrica admite tanto `(Alice, Bob)` como `(Bob, Alice)`, ambas son vinculaciones distintas. MUD no deduplica parejas por simetría ni presupone que el cuerpo trate los roles de igual manera.\n\nSemánticamente, las vinculaciones de una onda forman un conjunto y su orden no decide los efectos. Para trazas, diagnósticos y serialización, se usa un orden técnico reproducible: orden textual de roles y orden lexicográfico de sus anclas resueltas. Este orden no concede comparación `<` o `>` a las `thing`.",
    "Una vinculación es una asignación total de roles. No se impone desigualdad implícita: dos roles pueden recibir el mismo valor si satisfacen sus restricciones.\n\nLos roles también conservan orientación. Si una relación simétrica admite tanto `(Alice, Bob)` como `(Bob, Alice)`, ambas son vinculaciones distintas. MUD no deduplica parejas por simetría ni presupone que el cuerpo trate los roles de igual manera.\n\nSemánticamente, las vinculaciones de una onda forman un conjunto y su orden no decide los efectos. Cuando todos los valores vinculados son `thing`, el orden técnico reproducible ya definido por anclas continúa disponible para trazas y diagnósticos; D-096 no convierte esa convención técnica en un orden semántico de los valores `on` generales.",
)

# D-041: la rule reactiva sí puede llamar actions/subactions dentro de su then.
rewrite(
    "notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla.md",
    "Declara vinculaciones automáticas mediante `on`, no admite `given`, exige `when`, admite `if` y produce efectos mediante `then`. No ejecuta acciones reales. Puede consultar reglas booleanas y usar `allowed` si el grafo resultante sigue siendo acíclico.",
    "Declara vinculaciones automáticas mediante `on`, no admite `given`, exige `when`, admite `if` y produce consecuencias mediante `then`. Ese `then` puede mezclar efectos, locales y llamadas a `action` o `subaction` dentro de la resolución causal activa conforme a D-096. Puede consultar reglas booleanas y usar `allowed` si el grafo resultante sigue siendo admisible.",
)
rewrite(
    "notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla.md",
    "- Solo las reglas booleanas forman llamadas con resultado.\n- Solo las reactivas forman consecuencias causales.\n- Solo `always` convierte una falsedad en fallo de invariante.",
    "- Solo las reglas booleanas son callables con resultado booleano.\n- Entre las reglas, solo las reactivas poseen `then` y producen consecuencias que pueden modificar el mundo.\n- Reglas reactivas y `always` pueden además actuar como fuentes declarativas de trigger conforme a D-096.\n- Solo `always` convierte una falsedad en fallo de invariante.",
)

# D-042: retirar elemental/compuesta y conservar Q-023 solo para análisis dinámico pendiente.
rewrite(
    "notas/decisiones/ADR-042-acciones-raiz-y-resultados.md",
    "### Acciones elementales\n\nSu `then` contiene efectos. Las instrucciones del bloque son secuenciales dentro de su delta privado y la acción es atómica para cualquier observador exterior.\n\n### Acciones compuestas\n\nSu `then` contiene exclusivamente llamadas a acciones. No se mezclan llamadas y efectos directos en el mismo `then`.\n\nTodas las hojas de una composición:\n\n1. leen el mismo estado estable inicial;\n2. evalúan participantes, `given`, dominios e `if` sobre ese estado;\n3. generan una raíz simultánea consolidada;\n4. comprueban sus `after` después de estabilizar la resolución completa.\n\nEl grafo estático de llamadas entre acciones debe ser acíclico. La selección dinámica de acciones permanece abierta en Q-023.",
    "### Secuencia unificada de `then`\n\nNo existe una clasificación semántica entre actions elementales y compuestas. Un `then` es una secuencia ordenada de consecuencias y puede mezclar vinculaciones locales, efectos directos, llamadas a `action` o `subaction` y recorridos `for each`.\n\nCada sentencia lee el delta privado visible en su posición textual. Una llamada interna se valida y ejecuta en ese punto, observa los efectos privados anteriores, aporta sus propios efectos a la misma resolución atómica y deja esos efectos visibles para las sentencias posteriores. No abre una transacción independiente.\n\nLos `after` de todas las actions/subactions ejecutadas se comprueban contra el estado estable tentativo final de la resolución completa. El análisis de llamadas debe impedir ciclos ejecutables; Q-023 conserva abierta la demostración de aciclicidad e impacto cuando la selección del descriptor callable es dinámica, no la posibilidad de invocarlo.",
)
rewrite(
    "notas/decisiones/ADR-042-acciones-raiz-y-resultados.md",
    "3. Acción elemental y compuesta válidas.\n4. Rechazo de un `then` mixto y de un ciclo de llamadas.",
    "3. `then` mixto con efectos, locales y llamadas en orden textual.\n4. Propagación del delta privado a través de llamadas internas y rechazo de un ciclo ejecutable de llamadas.",
)

# D-045: ocurrencias causales y trigger algebra por matches.
rewrite(
    "notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola.md",
    "Para una vinculación con memoria, los disparos comparan valores en las instantáneas de inicio de dos ondas consecutivas conforme a D-041 y D-058. Un `when e` puramente booleano detecta únicamente $\\mathsf{false}\\rightarrow\\mathsf{true}$; `e changes` compara directamente ambos valores y puede pulsar en ondas consecutivas. `and` y `or` componen pulsos de cambio y transiciones booleanas sin convertirlos en estado persistente.",
    "Para una vinculación con memoria, los activadores temporales comparan valores en las instantáneas de inicio de dos ondas consecutivas conforme a D-041 y D-058. Un `when e` puramente booleano detecta únicamente $\\mathsf{false}\\rightarrow\\mathsf{true}$ y `e changes` compara directamente ambos valores. D-096 generaliza el resultado de un trigger a cero o más matches causales: `and` realiza natural join de matches compatibles y `or` su unión, conservando bindings, testigos e identidades de ocurrencia.",
)
rewrite(
    "notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola.md",
    "Una resolución termina cuando una onda no produce efectos ni nuevas consecuencias pendientes. Un ciclo u oscilación detectados producen `failed`; un límite de recursos es una salvaguarda técnica distinguible, no una definición alternativa de estabilización.",
    "Una resolución termina cuando una onda no produce efectos ni deja nuevas consecuencias u ocurrencias causales pendientes para la siguiente. Un ciclo u oscilación detectados producen `failed`; un límite de recursos es una salvaguarda técnica distinguible, no una definición alternativa de estabilización.",
)
rewrite(
    "notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola.md",
    "Los `message` detectados se conservan como ocurrencias tentativas. Sus propiedades se calculan sobre el estado final y solo se publican al confirmar; una reversión no entrega ninguna.",
    "Cada `message` ocurrido se conserva como una ocurrencia causal tentativa con identidad, declaración, bindings y vista de nacimiento. Su payload interno se proyecta sobre esa vista causal y la misma ocurrencia queda disponible como trigger en la onda siguiente; hacia el host, tras confirmar, el payload se proyecta sobre el estado estable final. Una reversión cancela toda entrega exterior.",
)
rewrite(
    "notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola.md",
    "- La multiplicidad, orden y deduplicación de mensajes siguen en Q-052.",
    "- La multiplicidad de ocurrencias causalmente distintas se conserva y no se deduplica por payload. Q-067 mantiene abierto qué ocurre si un participante ya no existe o no es evaluable en la proyección exterior final.",
)

# D-054: activación modular unificada y sintaxis esquemática coherente.
rewrite(
    "notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md",
    "Las definiciones de `thing` y reglas no quedan activas por aparecer. El único `start with` global separa obligatoriamente ambos universos:\n\n```mud\nstart with {\n    things {\n        Vegetation,\n        Tree\n    }\n\n    rules {\n        CanGrow\n    }\n}\n```\n\nNo existe la forma plana o mezclada. Cada sección recibe expresiones estáticas que aportan cero, una o varias identidades de su categoría: una referencia aporta una, `empty` aporta cero, una colección aporta sus miembros y `all` denota el catálogo estático correspondiente. Una colección de colecciones es inválida. Las identidades repetidas se deduplican y el orden no es observable.\n\nLas expresiones solo pueden depender de información disponible antes de existir mundo runtime. El resultado completo se materializa y valida atómicamente y se estabiliza antes de aceptar acciones externas.\n\nLas acciones, aliases y magnitudes no pertenecen a ninguno de esos conjuntos. Cada test declara un `start with` local con las mismas secciones `things` y `rules`; durante ese test sustituye por completo al global.",
    "Las definiciones de `thing` y reglas no quedan activas por aparecer. Cada módulo puede aportar como máximo un `start with` unificado:\n\n```mud\nstart with {\n    Vegetation,\n    Tree,\n    CanGrow\n}\n```\n\nUna contribución directa o cada expresión del bloque aporta cero, una o varias declaraciones activables `thing | rule`: una referencia aporta una, `empty` aporta cero y una colección aporta sus miembros. Para materializar un dominio enumerable explícito se usa `all D`; una colección de colecciones es inválida. Las identidades repetidas se deduplican y el orden no es observable.\n\nLas expresiones solo pueden depender de información disponible antes de existir mundo runtime. Las contribuciones de todos los módulos se combinan, materializan y validan atómicamente y se estabilizan antes de aceptar acciones externas. Cada módulo solo puede activar declaraciones con ciclo de vida del mismo módulo.\n\nActions, aliases y magnitudes no son declaraciones activables. Cada test declara su propia contribución `start with`; para un test raíz se unen las contribuciones del cierre transitivo estático de tests alcanzables conforme a D-096.",
)
rewrite(
    "notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md",
    'start-with-declaration\n    ::= "start" "with" "{"\n        [ declaration-reference\n          { "," declaration-reference }\n        ]\n        "}"',
    'start-with-declaration\n    ::= "start" "with"\n        ( expression\n        | "{" [ expression { "," expression } [ "," ] ] "}"\n        )',
)

# D-055: tests usan la superficie unificada y cierre transitivo de contribuciones.
rewrite(
    "notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md",
    "test CounterIncreases {\n    start with {\n        things { Counter }\n        rules { empty }\n    }",
    "test CounterIncreases {\n    start with Counter",
)
rewrite(
    "notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md",
    "Cada ejecución de un test comienza con un mundo vacío, fresco y aislado. Su `start with` sustituye por completo al `start with` global del programa.\n\nEl bloque local conserva la misma estructura declarativa que el global de D-085: contiene obligatoriamente las secciones `things { ... }` y `rules { ... }`. Cada una admite contribuciones estáticas de cero, una o varias identidades de su propia categoría mediante referencias, `empty`, colecciones de un nivel o `all` contextual. El orden no es observable y las identidades repetidas se deduplican.\n\nNo contiene instrucciones `create`, asignaciones ni otros efectos, y una contribución de categoría incorrecta o una colección anidada es inválida.\n\nLas declaraciones referenciadas se materializan conjuntamente con sus inicializadores canónicos. El mundo se valida y estabiliza antes de ejecutar el `then`.\n\nSea $\\mathcal L_P$ el conjunto de declaraciones activables del programa $P$ y sea $I_t\\subseteq\\mathcal L_P$ el conjunto local del test $t$. El estado previo al escenario se obtiene mediante:\n\n$$\nW_t^0\n=\n\\operatorname{stabilize}\n\\bigl(\n\\operatorname{materialize}(P,I_t)\n\\bigr)\n$$\n\nEl conjunto inicial global del programa no interviene en esta construcción.",
    "Cada ejecución de un test comienza con un mundo vacío, fresco y aislado. El `start with` de un test es una contribución propia de activación y no incorpora por sí mismo el `start with` ordinario de los módulos.\n\nLa superficie es la misma forma unificada de D-096: una contribución directa o un bloque de expresiones que aportan cero, una o varias declaraciones activables `thing | rule`. El orden no es observable y las identidades repetidas se deduplican. No contiene instrucciones `create`, asignaciones ni otros efectos, y una colección anidada es inválida.\n\nAntes de ejecutar el test raíz se calcula estáticamente el cierre transitivo de tests que puede llamar, respetando `uses`, y se unen las contribuciones `start with` de todos ellos. Una llamada posterior a un test ya incluido no vuelve a materializar su activación; un ciclo ejecutable entre tests es inválido. Las declaraciones resultantes se materializan conjuntamente con sus inicializadores canónicos y el mundo se estabiliza antes del `then` raíz.\n\nSea $C(t)$ el cierre transitivo estático de tests alcanzables desde el test raíz $t$, sea $I_u$ la contribución de activación de cada test $u$ y sea $I_t^*=\\bigcup_{u\\in C(t)} I_u$. El estado previo al escenario se obtiene mediante:\n\n$$\nW_t^0\n=\n\\operatorname{stabilize}\n\\bigl(\n\\operatorname{materialize}(P,I_t^*)\n\\bigr)\n$$\n\nLa activación inicial ordinaria de los módulos no interviene en esta construcción.",
)

# D-081: collection-producing operations require explicit all D.
rewrite(
    "notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones.md",
    "La fuente se captura al comenzar la evaluación. Debe ser finita y enumerable; si esa propiedad no puede demostrarse, la expresión es inválida.",
    "La fuente se captura al comenzar la evaluación. Debe ser una colección finita y enumerable; si la fuente conceptual es un dominio, se materializa explícitamente como `all D` antes de seleccionar. Si la finitud o enumerabilidad no puede demostrarse, la expresión es inválida.",
)
rewrite(
    "notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones.md",
    "`take` se aplica además a:\n\n- dominios finitos enumerables, produciendo una colección de sus primeros valores canónicos;\n- diccionarios, conservando asociaciones completas;\n- `Text`, produciendo el prefijo de hasta `n` valores `Char` como otro `Text`.",
    "`take` se aplica además a:\n\n- materializaciones `all D` de dominios finitos enumerables, tomando sus primeros valores canónicos;\n- diccionarios, conservando asociaciones completas;\n- `Text`, produciendo el prefijo de hasta `n` valores `Char` como otro `Text`.\n\nUn dominio desnudo no es fuente directa de `take`: al producir una colección, la materialización debe quedar explícita en el programa.",
)

# D-085: subaction callable desde cualquier then; start with unificado; Any incluye descriptores.
rewrite(
    "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md",
    "- Una `subaction` solo puede invocarse desde el cuerpo de otra `action` o `subaction`.\n- No puede constituir una solicitud externa, un comando raíz ni una entrada de la API pública.\n- Una `action` ordinaria puede invocar acciones ordinarias y subacciones.\n- Una `subaction` puede invocar acciones ordinarias y subacciones, sujeta al mismo análisis de aciclicidad.",
    "- Una `subaction` puede invocarse desde cualquier contexto semántico `then`, incluido el de una rule reactiva.\n- No puede constituir una solicitud externa, un comando raíz ni una entrada de la API pública.\n- Una `action` o `subaction` puede invocar actions ordinarias y subactions dentro de la misma resolución, sujeta al análisis de ciclos ejecutables.",
)
rewrite(
    "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md",
    "### Activación inicial estructurada\n\nLa única forma de `start with` contiene dos secciones obligatorias y separadas:\n\n```mud\nstart with {\n    things {\n        ...\n    }\n\n    rules {\n        ...\n    }\n}\n```\n\nNo existe la forma mezclada ni azúcar equivalente. Cada expresión de una sección aporta cero, una o varias identidades del universo correspondiente:\n\n- una referencia individual aporta una;\n- `empty` aporta cero;\n- una colección aporta directamente sus miembros;\n- una colección de colecciones es inválida: solo se incorpora un nivel de contribuciones.\n\nLas identidades repetidas se deduplican y el orden no es observable. En `things`, `all` denota el catálogo estático de declaraciones `thing` activables. En `rules`, `all` denota el catálogo estático de reglas activables. Las expresiones se evalúan solo con metadatos y propiedades disponibles estáticamente; no pueden leer estado runtime todavía inexistente.\n\nEl AST conserva `things` y `rules` como conjuntos separados de expresiones de contribución. La elaboración comprueba categoría, profundidad y evaluabilidad estática.",
    "### Activación inicial estructurada\n\nD-096 sustituye la separación por categorías por una superficie única. Cada módulo puede aportar como máximo un `start with`, en forma directa o como bloque:\n\n```mud\nstart with {\n    Kingdom,\n    CanGrow,\n    all ActivableDeclarations\n}\n```\n\nCada expresión aporta cero, una o varias declaraciones activables `thing | rule`: una referencia individual aporta una, `empty` aporta cero, una colección aporta directamente sus miembros y `all D` materializa explícitamente un dominio enumerable. Una colección de colecciones es inválida.\n\nLas identidades repetidas se deduplican y el orden no es observable. Las expresiones se evalúan solo con información disponible antes del mundo runtime y cada módulo solo puede activar declaraciones con ciclo de vida del mismo módulo. Las contribuciones de todos los módulos se materializan conjuntamente antes de la estabilización inicial.\n\nEl AST conserva una única secuencia `StartSet(contributions)`; la elaboración comprueba categoría activable, profundidad y evaluabilidad estática.",
)
rewrite(
    "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md",
    "Se incorpora el tipo superior `Any` para todos los valores MUD del proyecto. Su dominio abierto incluye tipos básicos —incluido `Money`—, identidades `thing`, aliases, miembros de familia, magnitudes, intervalos, colecciones, diccionarios y productos estructurales. No incluye acciones, reglas, tests, declaraciones ni nodos sintácticos como valores ordinarios.",
    "`Any` es el tipo superior de todos los valores MUD. Su dominio abierto incluye tipos básicos —incluido `Money`—, identidades `thing`, aliases, miembros de family, magnitudes, intervalos, colecciones, diccionarios, productos estructurales y descriptores first-class de declaraciones y tipos conforme a D-096. Los nodos sintácticos de implementación no son valores MUD por ese mero hecho.",
)

# D-087/D-092: look refleja givens y ~private queda retirado, también en defaults y verificación.
for rel in (
    "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md",
    "notas/decisiones/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas.md",
):
    rewrite(rel, "| `look` | sí | no | no |", "| `look` | sí | no | sí |")
rewrite(
    "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md",
    "~deprecated   : Text [0..1] = empty\n~private      : Bool = false",
    "~deprecated   : Text [0..1] = empty",
)
rewrite(
    "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md",
    "`~private` solo es válido en declaraciones de primer nivel `thing`, `alias`, `family`, `magnitude` y `rule`, y en campos almacenados/calculados/públicos pertenecientes a una `thing`. No es válido en `action`, `subaction`, `message`, `look`, `unit`, participantes, componentes, miembros de `family`, metadatos ni sintaxis arbitraria.\n\n`~private` controla exposición automática al host: bindings, esquemas, documentación, editores, serializadores generales e interfaces de inspección exterior deben omitir por defecto los elementos privados. No cambia resolución interna, tipos, herencia, reglas, actions, `create`, `destroy`, `start with`, reflexión interna ni materialización. No constituye una frontera de seguridad.",
    "`~private` queda retirado por D-096 y cualquier intento de declararlo como metadato estándar es inválido. La exposición exterior se deriva de la frontera de módulo, la categoría operacional y el cierre de tipos requerido por el contrato; no se expresa mediante un booleano metadata-bearing.",
)
rewrite(
    "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md",
    "```mud\n~private = true\n~stability: Stability = Experimental\n~summary = \"Subsistema interno\"\n\nusing world.shared\n```",
    "```mud\n~stability: Stability = Experimental\n~summary = \"Subsistema interno\"\n\nusing world.shared\n```",
)
rewrite(
    "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md",
    "Un default de archivo no admite `:=`, lecturas runtime ni propiedades intrínsecas. `~private`, `~summary`, `~description` y `~deprecated` pueden usarse como defaults. `~name`, `~plural`, `~abbreviation`, `~prefixes` y `~format` no pueden usarse como defaults de archivo por ser inherentemente individuales. Los metadatos de usuario son admitidos como defaults salvo restricción futura explícita de su definición.",
    "Un default de archivo no admite `:=`, lecturas runtime ni propiedades intrínsecas. `~summary`, `~description` y `~deprecated` pueden usarse como defaults. `~name`, `~plural`, `~abbreviation`, `~prefixes` y `~format` no pueden usarse como defaults de archivo por ser inherentemente individuales. `~private` no existe. Los metadatos de usuario son admitidos como defaults salvo restricción futura explícita de su definición.",
)
rewrite(
    "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md",
    "11. `~private` en categorías permitidas y rechazo en las demás.",
    "11. Rechazo de `~private` como nombre estándar retirado y ausencia de ese default de archivo.",
)

print("D-096 residue corrections applied")
