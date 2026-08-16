from pathlib import Path

ROOT = Path('.')


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one occurrence, found {count}: {old!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')


def write_new(path: str, content: str) -> None:
    p = ROOT / path
    if p.exists():
        raise SystemExit(f'{path}: already exists')
    p.write_text(content, encoding='utf-8', newline='\n')


def append_cases(content: str) -> None:
    p = ROOT / 'especificacion/sintaxis/casos/cst-ast.yaml'
    text = p.read_text(encoding='utf-8')
    if 'id: metadata-signature-supported-absent' in text:
        raise SystemExit('metadata signature cases already present')
    if not text.endswith('\n'):
        text += '\n'
    p.write_text(text + content, encoding='utf-8', newline='\n')


# D-087: static capability gate, not universal optional properties.
replace_once(
    'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md',
    '- Precisada por: [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]].\n',
    '- Precisada por: [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]], [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]] y [[ADR-092-disponibilidad-estatica-de-propiedades-reflectivas|D-092]].\n',
)
replace_once(
    'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md',
    '''### Firmas y participantes\n\nLas declaraciones que posean las cláusulas correspondientes exponen:\n\n```text\n~for     : Participant [* unique ordered]\n~on      : Participant [* unique ordered]\n~given   : Participant [* unique ordered]\n~clauses : ClauseKind [* unique]\n```\n\nUna cláusula ausente produce `empty`. `~clauses` informa solo de presencia de clases, nunca expone el AST del cuerpo.\n''',
    '''### Firmas y participantes\n\nLa disponibilidad de una propiedad reflectiva depende de la categoría estática compatible del receptor. Que la gramática pueda reconocer `expression~name` no hace que ese nombre exista para todo receptor. D-092 fija esta frontera de lookup.\n\nLas propiedades de participantes tienen estas capacidades por subcategoría de declaración:\n\n| Subcategoría | `~for` | `~on` | `~given` |\n| --- | --- | --- | --- |\n| regla booleana | sí | no | sí |\n| regla reactiva | no | sí | no |\n| regla `always` | no | sí | no |\n| `action` | sí | no | sí |\n| `subaction` | sí | no | sí |\n| `look` | sí | no | no |\n| `message` | no | sí | no |\n| demás declaraciones | no | no | no |\n\nCuando una propiedad está soportada por la subcategoría pero la declaración concreta omite su cláusula opcional, el valor es `empty` con el tipo de colección correspondiente. Cuando la propiedad no está soportada por la subcategoría estática, el acceso es un error estático; no produce `empty` ni un valor predeterminado. Por ejemplo, `thing A` hace inválido `A~for`, mientras que una `action` sin cláusula `for` admite `ActionName~for` y devuelve `empty`.\n\n```text\n~for     : Participant [* unique ordered]\n~on      : Participant [* unique ordered]\n~given   : Participant [* unique ordered]\n~clauses : ClauseKind [* unique]\n```\n\n`~clauses` informa solo de presencia de clases, nunca expone el AST del cuerpo. Su disponibilidad sigue igualmente el contrato de propietario de la propiedad; la regla anterior sobre `empty` no convierte `~clauses` ni ninguna otra propiedad en universal.\n''',
)

# 07: make the owner column a capability matrix rather than an instance-presence condition.
replace_once(
    'especificacion/07-gramatica-concreta.md',
    '  - D-091\n',
    '  - D-091\n  - D-092\n',
)
replace_once(
    'especificacion/07-gramatica-concreta.md',
    '| `~for` | `Participant [* unique ordered]` | declaraciones con cláusula `for` | no, intrínseco |\n| `~on` | `Participant [* unique ordered]` | declaraciones con cláusula `on` | no, intrínseco |\n| `~given` | `Participant [* unique ordered]` | declaraciones con cláusula `given` | no, intrínseco |\n',
    '| `~for` | `Participant [* unique ordered]` | regla booleana, `action`, `subaction`, `look` | no, intrínseco |\n| `~on` | `Participant [* unique ordered]` | regla reactiva, regla `always`, `message` | no, intrínseco |\n| `~given` | `Participant [* unique ordered]` | regla booleana, `action`, `subaction` | no, intrínseco |\n',
)
replace_once(
    'especificacion/07-gramatica-concreta.md',
    '''La tabla resume las propiedades comunes y configurables que afectan a la sintaxis de este capítulo. D-087 define además las propiedades reflectivas específicas de cada descriptor, como relaciones de especialización, campos, componentes y propiedades estructurales de colecciones y diccionarios; no se duplican aquí como un segundo catálogo normativo.\n''',
    '''La columna «Propietarios» es una restricción semántica de disponibilidad, no una descripción de cuándo el resultado es no vacío. Tras resolver y tipar el receptor, un acceso a una propiedad no soportada por su categoría estática es error. En particular, `thing A` hace inválido `A~for`; una `action` sí soporta `~for` aunque omita la cláusula y en ese caso obtiene `empty`. La misma separación entre propiedad inexistente y valor vacío se aplica a `~on` y `~given`.\n\nLa producción `metadata-name ::= identifier | "for" | "on" | "given"` solo permite que esas keywords duras aparezcan sintácticamente después de `~`. El parser no puede decidir por el nombre textual del receptor si el acceso existe: construye la forma postfix y la resolución/tipado aplica la matriz de D-092.\n\nLa tabla resume las propiedades comunes y configurables que afectan a la sintaxis de este capítulo. D-087 define además las propiedades reflectivas específicas de cada descriptor, como relaciones de especialización, campos, componentes y propiedades estructurales de colecciones y diccionarios; no se duplican aquí como un segundo catálogo normativo.\n''',
)

# 08: preserve metadata access syntactically, never as an assignable suffix.
replace_once(
    'especificacion/08-sintaxis-abstracta.md',
    '  - D-091\n',
    '  - D-091\n  - D-092\n',
)
replace_once(
    'especificacion/08-sintaxis-abstracta.md',
    '`element~metadata` produce `MetadataAccessExpr` o `MetadataSuffix` en un destino asignable. Toda interpolación produce `ValueInterpolation`, incluida:\n',
    '`element~metadata` produce siempre `MetadataAccessExpr`. No existe `MetadataSuffix` asignable: `AssignableExpr` solo conserva `MemberSuffix` e `IndexSuffix`, de modo que ningún acceso `~` puede ser destino de un efecto. El AST superficial tampoco decide si la propiedad existe para el receptor; D-092 difiere esa comprobación hasta que la categoría estática del receptor ha sido resuelta. Toda interpolación produce `ValueInterpolation`, incluida:\n',
)

# New ADR records the accepted semantic clarification without changing parsing.
write_new(
    'notas/decisiones/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas.md',
    '''---\nid: D-092\ntitle: "Disponibilidad estática de propiedades reflectivas"\nstatus: vigente\ndate: 2026-08-16\nsupersedes: []\nsuperseded-by: []\nquestions: []\naffects:\n  - "reflexión, metadatos, participantes, resolución, tipado, AST resuelto, diagnósticos y tooling"\n---\n\n# ADR-092 — Disponibilidad estática de propiedades reflectivas\n\n- Precisa: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n- Amplía: [[ADR-074-uniones-nominales-y-estrechamiento|D-074]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].\n\n## Contexto\n\nLa sintaxis postfix `expression~property` debe poder reconocer nombres que son keywords duras, como `for`, `on` y `given`. La regla concreta `metadata-name ::= identifier | "for" | "on" | "given"` permite esa escritura, pero no puede determinar durante el parsing qué categoría denota una expresión receptora.\n\nD-087 decía además que una cláusula ausente produce `empty`. Leída sin la restricción de propietario, esa frase permite interpretar erróneamente que cualquier declaración tiene siempre `~for`, `~on` y `~given`. Eso haría válido, por ejemplo, `thing A; A~for`, aunque una `thing` no posee firma `for`.\n\n## Decisión\n\nLa existencia de una propiedad reflectiva se comprueba estáticamente después de resolver y tipar el receptor. Cada propiedad tiene un conjunto de categorías o descriptores propietarios. Si la categoría estática del receptor no garantiza pertenencia a ese conjunto, el acceso es un error estático.\n\nEl reconocimiento sintáctico del nombre después de `~` no concede la propiedad. No existe lookup dinámico por nombre, fallback a `empty` ni metadato de usuario implícito para una propiedad no soportada. Un narrowing que haga suficientemente precisa la categoría del receptor puede volver válido un acceso que antes no estaba garantizado.\n\nPara las propiedades de participantes, la matriz es:\n\n| Subcategoría resuelta | `~for` | `~on` | `~given` |\n| --- | --- | --- | --- |\n| `RuleKind.Boolean` | sí | no | sí |\n| `RuleKind.Reactive` | no | sí | no |\n| `RuleKind.Always` | no | sí | no |\n| `ActionKind.Action` | sí | no | sí |\n| `ActionKind.Subaction` | sí | no | sí |\n| `look` | sí | no | no |\n| `message` | no | sí | no |\n| cualquier otra declaración | no | no | no |\n\nLa matriz describe capacidad de la subcategoría, no presencia concreta de la cláusula. Cuando una propiedad está soportada y la cláusula opcional fue omitida en esa declaración, el acceso es válido y devuelve `empty` con tipo `Participant [* unique ordered]`. Cuando la cláusula está presente, devuelve sus descriptores en orden de firma.\n\nPor tanto:\n\n```mud\nthing A\n\n# error estático: Thing no soporta ~for\ncheck := A~for\n```\n\ny, conceptualmente:\n\n```mud\naction Ping {\n    then create A\n}\n\n# válido: Action soporta ~for; Ping omitió la cláusula\nparticipants := Ping~for  # empty\n```\n\nLa regla de disponibilidad se aplica también al resto de propiedades reflectivas conforme al conjunto de propietarios de su contrato. Una propiedad cuyo resultado admita ausencia o colección vacía sigue distinguiendo esa ausencia de la inexistencia de la propiedad.\n\n## Consecuencias por fase\n\n### Parser y CST\n\nNo cambian. Deben aceptar la forma postfix siempre que el nombre sea sintácticamente válido. En particular, `for`, `on` y `given` siguen admitiéndose tras `~` porque son keywords duras.\n\n### AST superficial\n\nConserva `MetadataAccessExpr(receiver, metadata)` aunque el acceso vaya a resultar semánticamente inválido. No posee información suficiente para aplicar la matriz.\n\n### Resolución y tipado\n\nDeterminan la categoría estática del receptor, aplican narrowing cuando exista y seleccionan el contrato de propiedad. Si ninguna propiedad compatible existe para todos los casos todavía posibles del receptor, emiten error estático. Solo los accesos válidos llegan al AST resuelto con tipo de resultado.\n\n### Ejecución\n\nNo realiza búsqueda dinámica para rescatar un acceso inválido. `empty` aparece únicamente como valor de un contrato válido que lo permita.\n\n## Casos frontera\n\n- `thing A; A~for` es inválido.\n- Una `action` sin `for` tiene `ActionName~for == empty`.\n- Una regla booleana sin `given` tiene `RuleName~given == empty`.\n- Una regla reactiva sin `on` tiene `RuleName~on == empty`.\n- `ActionName~on` es inválido aunque la acción no tenga participantes.\n- Un receptor estático demasiado amplio debe estrecharse antes de acceder a una propiedad que no esté garantizada por todas sus alternativas posibles.\n\n## Alternativas descartadas\n\n### Todas las propiedades de firma existen y las no aplicables devuelven `empty`\n\nDescartada porque borra la diferencia entre una categoría que admite una cláusula opcional y otra que carece de ese concepto.\n\n### Rechazo durante parsing según el texto del receptor\n\nDescartada porque el receptor es una expresión general y su categoría se conoce después de resolución; vincular la gramática al nombre textual rompería aliases, referencias cualificadas y narrowing.\n\n## Verificación\n\n1. La EBNF sigue aceptando `for`, `on` y `given` como `metadata-name`.\n2. `thing A; A~for` produce AST superficial y después error estático de propiedad no soportada.\n3. Una declaración de categoría compatible sin cláusula concreta devuelve `empty`.\n4. `AssignableExpr` no contiene ningún sufijo de metadata.\n5. El AST resuelto solo contiene `MetadataAccessExpr` para propiedades compatibles con la categoría estática resuelta.\n''',
)

append_cases(
    '''- id: metadata-signature-supported-absent\n  category: typing-after-ast\n  source: "thing Seed\\naction Spawn {\\n    then create Seed\\n}\\nrule EmptySignatureCheck {\\n    Spawn~for == empty and Spawn~given == empty\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: BooleanRuleDecl(condition=BinaryExpr(MetadataAccessExpr(Spawn, for) == empty, WordAnd, MetadataAccessExpr(Spawn, given) == empty))\n  semantic_expectations:\n  - action-without-for-yields-empty-for\n  - action-without-given-yields-empty-given\n  produces_ast: true\n- id: metadata-signature-unsupported-receiver\n  category: typing-after-ast\n  source: "thing Seed\\nrule InvalidSignatureReflection {\\n    Seed~for == empty\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: BooleanRuleDecl(condition=ComparisonChainExpr(MetadataAccessExpr(Seed, for), Equal, empty))\n  expected_diagnostics:\n  - metadata-property-not-supported-by-static-receiver\n  produces_ast: true\n'''
)

print('GLOBAL_COHERENCE_PHASE5_METADATA_CAPABILITIES_OK')
