from pathlib import Path

ROOT = Path('.')


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one occurrence, found {count}: {old!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')


def append_case(content: str) -> None:
    p = ROOT / 'especificacion/sintaxis/casos/cst-ast.yaml'
    text = p.read_text(encoding='utf-8')
    if 'id: family-data-metadata' in text:
        raise SystemExit('family cases already present')
    if not text.endswith('\n'):
        text += '\n'
    p.write_text(text + content, encoding='utf-8', newline='\n')


def write_new(path: str, content: str) -> None:
    p = ROOT / path
    if p.exists():
        raise SystemExit(f'{path}: already exists')
    p.write_text(content, encoding='utf-8', newline='\n')


# ------------------------------------------------------------------
# EBNF: metadata-body inmediato en declaraciones de datos de family.
# El calculado vuelve además al contrato vigente de D-038: solo tipo opcional.
# ------------------------------------------------------------------
replace_once(
    'especificacion/gramatica/mud.ebnf',
    '''stored-family-data-declaration\n    ::= field-name , ":" , type-expression\n        , [ "=" , constant-expression ]\n        ;\n\ncalculated-family-data-declaration\n    ::= field-name , [ derived-value-shape ] , ":=" , value-expression\n        ;\n''',
    '''stored-family-data-declaration\n    ::= field-name , ":" , type-expression\n        , [ "=" , constant-expression ]\n        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]\n        ;\n\ncalculated-family-data-declaration\n    ::= field-name , [ ":" , type-expression ] , ":=" , value-expression\n        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]\n        ;\n''',
)

# CST catalog mirrors the new RHS exactly.
replace_once(
    'especificacion/sintaxis/mud-syntax-kinds.yaml',
    '''  stored-family-data-declaration:\n    kind: StoredFamilyDataDeclarationSyntax\n    rhs: "field-name , \\":\\" , type-expression\\n        , [ \\"=\\" , constant-expression ]"\n    references:\n    - field-name\n    - type-expression\n    - constant-expression\n  calculated-family-data-declaration:\n    kind: CalculatedFamilyDataDeclarationSyntax\n    rhs: field-name , [ derived-value-shape ] , ":=" , value-expression\n    references:\n    - field-name\n    - derived-value-shape\n    - value-expression\n''',
    '''  stored-family-data-declaration:\n    kind: StoredFamilyDataDeclarationSyntax\n    rhs: "field-name , \\":\\" , type-expression\\n        , [ \\"=\\" , constant-expression ]\\n        , [ \\"{\\" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , \\"}\\" ]"\n    references:\n    - field-name\n    - type-expression\n    - constant-expression\n    - declaration-layout\n    - metadata-assignment\n    - required-separation\n  calculated-family-data-declaration:\n    kind: CalculatedFamilyDataDeclarationSyntax\n    rhs: "field-name , [ \\":\\" , type-expression ] , \\":=\\" , value-expression\\n        , [ \\"{\\" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , \\"}\\" ]"\n    references:\n    - field-name\n    - type-expression\n    - value-expression\n    - declaration-layout\n    - metadata-assignment\n    - required-separation\n''',
)

# Coverage remains constructor-to-constructor, but records the new preserved payload.
replace_once(
    'especificacion/sintaxis/cobertura-sintactica.yaml',
    '''  stored-family-data-declaration:\n    cst: StoredFamilyDataDeclarationSyntax\n    ast:\n      disposition: constructor\n      target: StoredFamilyDataDecl\n  calculated-family-data-declaration:\n    cst: CalculatedFamilyDataDeclarationSyntax\n    ast:\n      disposition: constructor\n      target: CalculatedFamilyDataDecl\n''',
    '''  stored-family-data-declaration:\n    cst: StoredFamilyDataDeclarationSyntax\n    ast:\n      disposition: constructor\n      target: StoredFamilyDataDecl\n      reason: conserva el metadata-body del descriptor de dato almacenado\n  calculated-family-data-declaration:\n    cst: CalculatedFamilyDataDeclarationSyntax\n    ast:\n      disposition: constructor\n      target: CalculatedFamilyDataDecl\n      reason: conserva tipo opcional, expresión y metadata-body del descriptor calculado\n''',
)

# Surface AST: metadata lives on the schema declaration, never on member overrides.
replace_once(
    'especificacion/sintaxis/mud-surface-ast.asdl',
    '''    family_data_decl = StoredFamilyDataDecl(field_name name,\n                                            value_shape shape,\n                                            expr? default_value)\n                     | CalculatedFamilyDataDecl(field_name name,\n                                                derived_value_shape? shape,\n                                                expr value)\n        attributes (source_origin origin)\n''',
    '''    family_data_decl = StoredFamilyDataDecl(field_name name,\n                                            value_shape shape,\n                                            expr? default_value,\n                                            metadata_assignment* metadata)\n                     | CalculatedFamilyDataDecl(field_name name,\n                                                type_expr? type,\n                                                expr value,\n                                                metadata_assignment* metadata)\n        attributes (source_origin origin)\n''',
)

# Concrete-to-AST contract.
replace_once(
    'especificacion/sintaxis/cst-a-ast-superficial.md',
    '''Las declaraciones de datos se separan en almacenadas y calculadas. En el preámbulo de un miembro, cualquier `metadata-assignment` produce `StoredMetadataAssignment` o `CalculatedMetadataAssignment`; las asignaciones ordinarias posteriores se conservan como datos almacenados. Un cuerpo metadata-only produce `assignments = []` y conserva su secuencia `metadata`.\n''',
    '''Las declaraciones de datos se separan en almacenadas y calculadas. Cada declaración puede llevar un cuerpo inmediato formado exclusivamente por `metadata-assignment`; esa secuencia se conserva en `StoredFamilyDataDecl.metadata` o `CalculatedFamilyDataDecl.metadata`. En un dato calculado, la anotación superficial conservada es únicamente `type_expr?`: `in domain` y las especificaciones de colección no pertenecen a esta producción.\n\nEn el preámbulo de un miembro, cualquier `metadata-assignment` produce `StoredMetadataAssignment` o `CalculatedMetadataAssignment` del descriptor del miembro; las asignaciones ordinarias posteriores se conservan como `FamilyDataAssignment`. Estas asignaciones sustituyen el valor de un dato almacenado para ese miembro, pero no crean descriptor, ancla ni metadata-body propios. Un cuerpo de miembro metadata-only produce `assignments = []` y conserva su secuencia `metadata`.\n''',
)

# 07: normative syntax and examples.
replace_once(
    'especificacion/07-gramatica-concreta.md',
    '  - D-090\n',
    '  - D-090\n  - D-091\n',
)
replace_once(
    'especificacion/07-gramatica-concreta.md',
    '''Los datos aparecen antes del primer miembro y pueden ser almacenados o calculados mediante `nombre [: Tipo] := expresión`. El tipo calculado es opcional si se puede inferir de forma unívoca. Su expresión se evalúa estáticamente para cada miembro después de resolver los datos almacenados, puede consultar otros datos asociados mediante nombres no cualificados y debe tener dependencias acíclicas. El bloque de un miembro solo puede asignar datos almacenados.\n\nLos miembros se separan por comas y no admiten coma final. `ordered family` hace comparables sus miembros en orden de declaración y permite usar rutas de datos asociados, incluidos los calculados estables, como claves de `ordered by` en colecciones.\n''',
    '''Los datos aparecen antes del primer miembro. Un dato almacenado puede llevar, después de su predeterminado opcional, un cuerpo inmediato que contenga solo declaraciones `~...`. Un dato calculado se escribe exclusivamente como `nombre [: Tipo] := expresión` y puede llevar el mismo metadata-body inmediato; no admite `in`, especificación de colección, predeterminado ni `mut`. El tipo calculado es opcional si se puede inferir de forma unívoca.\n\nEl metadata-body describe el descriptor uniforme del dato de la `family`, no el valor concreto proyectado por cada miembro. Por ejemplo:\n\n```mud\nfamily Terrain {\n    movementCost: Nat = 1 {\n        ~summary = "Coste base de movimiento"\n    }\n    costly := movementCost >= 3 {\n        ~summary = "Indica terreno costoso"\n    }\n\n    Plain,\n    Mountain {\n        movementCost = 4\n    }\n}\n```\n\nLa asignación `movementCost = 4` del miembro es solo una sobrescritura de valor del dato almacenado. No admite metadata-body, no introduce otra ancla y no modifica los metadatos del descriptor `movementCost`. La expresión de un dato calculado se evalúa estáticamente para cada miembro después de resolver los datos almacenados, puede consultar otros datos asociados mediante nombres no cualificados y debe tener dependencias acíclicas. El bloque de un miembro solo puede asignar datos almacenados.\n\nLos miembros se separan por comas y no admiten coma final. `ordered family` hace comparables sus miembros en orden de declaración y permite usar rutas de datos asociados, incluidos los calculados estables, como claves de `ordered by` en colecciones.\n''',
)

# 08: descriptors and surface representation.
replace_once(
    'especificacion/08-sintaxis-abstracta.md',
    '  - D-090\n',
    '  - D-090\n  - D-091\n',
)
replace_once(
    'especificacion/08-sintaxis-abstracta.md',
    '''Los datos asociados no admiten mutabilidad exterior. Su colección puede conceder capacidad interior sobre `thing` contenidas.\n\nCada `FamilyMember` conserva asignaciones de metadatos, como `~name`, y asignaciones a datos almacenados. Un bloque omitido produce ambas secuencias vacías. Los metadatos no se confunden con datos de la familia.\n''',
    '''Los datos asociados no admiten mutabilidad exterior. El dato almacenado conserva `metadata_assignment* metadata` junto a su forma y predeterminado. El dato calculado conserva únicamente `type_expr? type`, su expresión y `metadata_assignment* metadata`: una forma `in ...` o una especificación de colección sería inválida antes del AST.\n\nCada declaración de dato asociado es un propietario metadata-bearing estable y se elabora como descriptor `Field` subordinado a la `family`, con `FieldKind.Stored` o `FieldKind.Calculated`. La proyección `member.data` es un valor, no una copia del descriptor. Por tanto, los metadatos pertenecen al dato declarado una sola vez y no se duplican por miembro.\n\nCada `FamilyMember` conserva asignaciones de metadatos, como `~name`, y asignaciones a datos almacenados. `FamilyDataAssignment` permanece deliberadamente sin campo `metadata`: una sobrescritura de miembro solo selecciona el valor efectivo del slot almacenado y no crea un propietario metadata-bearing. Un bloque omitido produce ambas secuencias vacías.\n''',
)

# 09: make the already-implied family-data anchors explicit and separate them from values.
replace_once(
    'especificacion/09-nombres-y-anclas.md',
    '  - D-090\n',
    '  - D-090\n  - D-091\n',
)
replace_once(
    'especificacion/09-nombres-y-anclas.md',
    'family::game.rules.Severity::Critical\n',
    'family::game.rules.Severity::Critical\nfamily::game.world.Terrain::movementCost\n',
)
replace_once(
    'especificacion/09-nombres-y-anclas.md',
    '- campos y componentes;\n- miembros de family;\n',
    '- campos, componentes y datos asociados declarados por una `family`;\n- miembros de family;\n',
)
replace_once(
    'especificacion/09-nombres-y-anclas.md',
    '''Un miembro heredado conserva el ancla del propietario que lo declaró. En `thing` esto no comparte estado; en aliases identifica el origen usado para deduplicar diamantes. Una sobrescritura de predeterminado no introduce un miembro ni un ancla nuevos.\n''',
    '''Un dato asociado declarado por una `family` posee un ancla subordinada estable formada con la categoría `family`, el nombre cualificado de la familia y el identificador del dato. Esa ancla identifica el descriptor del esquema uniforme, no cada valor obtenido al consultar un miembro. Una asignación dentro del cuerpo de un miembro no introduce ancla y no cambia la del dato declarado.\n\nUn miembro heredado conserva el ancla del propietario que lo declaró. En `thing` esto no comparte estado; en aliases identifica el origen usado para deduplicar diamantes. Una sobrescritura de predeterminado no introduce un miembro ni un ancla nuevos.\n''',
)

# D-038: distinguish runtime value identity from declaration identity and record metadata.
replace_once(
    'notas/decisiones/ADR-038-familias-cerradas-de-valores.md',
    '- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]\n',
    '- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]]\n',
)
replace_once(
    'notas/decisiones/ADR-038-familias-cerradas-de-valores.md',
    '''El dato calculado reutiliza la forma general definida por D-037:\n\n```text\nnombre [: tipo] := expresión\n```\n\nLa anotación de tipo de un dato calculado es opcional. Si se omite, el compilador debe inferir un único tipo estático; si no puede hacerlo, la declaración es inválida. Un dato calculado no admite `mut`, `in`, especificación de colección, predeterminado ni almacenamiento propio: su forma y su valor proceden de la expresión.\n''',
    '''El dato calculado reutiliza la forma de cálculo con tipo opcional definida por D-037:\n\n```text\nnombre [: tipo] := expresión [metadata-body]\n```\n\nLa anotación de tipo de un dato calculado es opcional. Si se omite, el compilador debe inferir un único tipo estático; si no puede hacerlo, la declaración es inválida. Un dato calculado no admite `mut`, `in`, especificación de colección, predeterminado ni almacenamiento propio: su forma y su valor proceden de la expresión. Tanto un dato almacenado como uno calculado pueden llevar un cuerpo inmediato formado exclusivamente por declaraciones de metadatos `~...`; D-091 fija que ese cuerpo pertenece al descriptor uniforme del dato.\n''',
)
replace_once(
    'notas/decisiones/ADR-038-familias-cerradas-de-valores.md',
    '''Los datos asociados, almacenados o calculados:\n\n- Son inmutables.\n- No poseen identidad ni ciclo de vida propios.\n- Se consultan como propiedades del valor de familia, por ejemplo `terrain.movementCost`.\n- No alteran la identidad ni la igualdad del miembro: siguen dependiendo de la familia nominal y el nombre del miembro.\n''',
    '''Los valores asociados obtenidos para un miembro, almacenados o calculados:\n\n- Son inmutables.\n- No poseen identidad ni ciclo de vida runtime propios.\n- Se consultan como propiedades del valor de familia, por ejemplo `terrain.movementCost`.\n- No alteran la identidad ni la igualdad del miembro: siguen dependiendo de la familia nominal y el nombre del miembro.\n\nLa declaración del dato sí es una entidad semántica estable del esquema de la `family`: posee descriptor `Field`, ancla subordinada y metadatos propios conforme a D-091. Una asignación de miembro solo sustituye el valor efectivo de un dato almacenado y no crea una segunda entidad.\n''',
)

# D-087: include family data explicitly in the Field contract, without inventing a new descriptor kind.
replace_once(
    'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md',
    '- Precisada por: [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]].\n',
    '- Precisada por: [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]].\n',
)
replace_once(
    'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md',
    'Por ello pueden ser metadata-bearing las declaraciones nominales ancladas, miembros de `family`, unidades, campos almacenados/calculados/públicos, componentes de alias y participantes `for`/`on`/`given`.\n',
    'Por ello pueden ser metadata-bearing las declaraciones nominales ancladas, miembros de `family`, unidades, campos almacenados/calculados/públicos, datos asociados almacenados/calculados de una `family`, componentes de alias y participantes `for`/`on`/`given`.\n',
)
replace_once(
    'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md',
    '''`~kind` usa `FieldKind`. Los componentes de alias exponen el mismo contrato estructural salvo que `~mutable` es siempre `false`; esta decisión no crea una `ComponentKind` nueva.\n''',
    '''`~kind` usa `FieldKind`. Los datos asociados declarados por una `family` reutilizan `Field`: un dato almacenado usa `FieldKind.Stored` y uno calculado `FieldKind.Calculated`. No se crea `FamilyDataKind`. Su ancla es subordinada a la `family`; el valor proyectado por cada miembro no obtiene descriptor ni metadatos propios. Los componentes de alias exponen el mismo contrato estructural salvo que `~mutable` es siempre `false`; esta decisión no crea una `ComponentKind` nueva.\n''',
)
replace_once(
    'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md',
    '''Campos y componentes pueden llevar inmediatamente un cuerpo que contenga solo declaraciones `~...`. El cuerpo pertenece al descriptor, no al valor del campo o componente. Un campo añadido dinámicamente por un efecto no puede adquirir metadatos persistentes porque no satisface el principio de admisión.\n''',
    '''Campos, componentes y datos asociados declarados por una `family` pueden llevar inmediatamente un cuerpo que contenga solo declaraciones `~...`. El cuerpo pertenece al descriptor, no al valor proyectado. Una asignación de dato dentro de un miembro de `family` no admite ese cuerpo porque no declara un descriptor nuevo. Un campo añadido dinámicamente por un efecto no puede adquirir metadatos persistentes porque no satisface el principio de admisión.\n''',
)

# Dedicated ADR for the clarified identity boundary.
write_new(
    'notas/decisiones/ADR-091-datos-de-family-como-descriptores-anclados.md',
    '''---\nid: D-091\ntitle: "Datos de family como descriptores anclados"\nstatus: vigente\ndate: 2026-08-16\nsupersedes: []\nsuperseded-by: []\nquestions: []\naffects:\n  - "family, datos asociados, metadatos, anclas, gramática, CST, AST superficial, AST resuelto, reflexión y tooling"\n---\n\n# ADR-091 — Datos de family como descriptores anclados\n\n- Modifica: [[ADR-038-familias-cerradas-de-valores|D-038]].\n- Precisa: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n- Amplía: [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].\n\n## Contexto\n\nD-038 definió datos asociados uniformes para una `family` y afirmó que no poseían identidad propia, hablando de los valores proyectados por cada miembro. D-087 estableció después que los elementos metadata-bearing necesitan descriptor tipado y ancla pública estable. La especificación de anclas ya clasificaba los datos de `family` bajo la categoría `family`, pero la gramática y el AST superficial no permitían adjuntarles metadatos.\n\nAdemás, la EBNF había ampliado accidentalmente el dato calculado mediante `derived-value-shape`, aunque D-038 prohíbe `in` y especificaciones de colección en esa declaración.\n\n## Decisión\n\nLa declaración de un dato asociado almacenado o calculado es una entidad semántica estable del esquema uniforme de la `family`. Posee:\n\n- descriptor reflectivo `Field`;\n- `FieldKind.Stored` o `FieldKind.Calculated`;\n- ancla subordinada `family::<nombre-cualificado>::<dato>`;\n- secuencia propia de metadatos.\n\nNo se introduce `FamilyDataKind` ni una categoría de ancla nueva.\n\nUn dato puede llevar inmediatamente un cuerpo formado exclusivamente por declaraciones `~...`:\n\n```mud\nfamily Terrain {\n    movementCost: Nat = 1 {\n        ~summary = "Coste base de movimiento"\n    }\n    costly := movementCost >= 3 {\n        ~summary = "Indica terreno costoso"\n    }\n\n    Plain,\n    Mountain {\n        movementCost = 4\n    }\n}\n```\n\nEl metadata-body pertenece al descriptor `movementCost` o `costly`, no al valor obtenido para `Plain`, `Mountain` u otro miembro. Consultar `Mountain.movementCost` produce el valor asociado; no crea un descriptor nuevo por miembro.\n\nUna `family-data-assignment` dentro del cuerpo de un miembro es únicamente una sobrescritura del valor efectivo de un dato almacenado. No posee ancla, no admite metadata-body y no puede modificar los metadatos del dato declarado.\n\nEl dato calculado conserva la sintaxis estricta de D-038:\n\n```text\nnombre [: tipo] := expresión [metadata-body]\n```\n\nNo admite `mut`, `in`, especificación de colección, predeterminado ni almacenamiento propio. La EBNF y el AST superficial no deben representar esas formas prohibidas.\n\n`~private` continúa sin ser válido en datos asociados de `family`: D-087 lo restringe a declaraciones de primer nivel compatibles y a campos pertenecientes a una `thing`.\n\n## Consecuencias\n\n- Renombrar un dato asociado cambia el ancla de su descriptor.\n- Cambiar el valor de un miembro no cambia anclas ni metadatos.\n- Los descriptores de datos participan en `~fields` y `~declaredFields` de la `family` como `Field`.\n- `StoredFamilyDataDecl` y `CalculatedFamilyDataDecl` conservan `metadata_assignment* metadata`.\n- `CalculatedFamilyDataDecl` conserva `type_expr?`, no `derived_value_shape?`.\n- `FamilyDataAssignment` permanece sin metadatos.\n\n## Alternativas descartadas\n\n### Descriptor independiente por miembro y dato\n\nDescartado porque multiplicaría artificialmente entidades que comparten un único esquema y haría que una sobrescritura de valor pareciese una declaración.\n\n### Nueva categoría reflectiva `FamilyData`\n\nDescartada porque el contrato ya coincide con `Field` y `FieldKind`; añadir otra familia reflectiva no aporta una diferencia semántica.\n\n### Permitir metadata-body en una sobrescritura de miembro\n\nDescartado porque los metadatos describen el slot declarado, no una ocurrencia de su valor.\n\n## Verificación\n\n1. La EBNF admite metadata-body en ambos datos declarados y no lo admite en `family-data-assignment`.\n2. El dato calculado solo conserva tipo opcional antes de `:=`.\n3. CST, cobertura y proyección AST conservan el metadata-body en el descriptor.\n4. El AST superficial almacena metadatos en ambos constructores de datos y no en `FamilyDataAssignment`.\n5. La especificación de anclas identifica el descriptor bajo la categoría `family`.\n6. D-038 distingue la identidad del descriptor de la ausencia de identidad runtime del valor proyectado.\n''',
)

# Mechanical cases: positive descriptor metadata and negative metadata on override.
append_case(
    '''- id: family-data-metadata\n  category: family\n  source: "family Terrain {\\n    movementCost: Nat = 1 {\\n        ~summary = \\\"Coste base\\\"\\n    }\\n    costly: Bool := movementCost >= 3 {\\n        ~summary = \\\"Costoso\\\"\\n    }\\n\\n    Plain,\\n    Mountain {\\n        movementCost = 4\\n    }\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: FamilyDecl(data=[StoredFamilyDataDecl(movementCost, metadata=[StoredMetadataAssignment(summary)]), CalculatedFamilyDataDecl(costly, type=Bool, metadata=[StoredMetadataAssignment(summary)])])\n  normalizations:\n  - family-data-metadata-belongs-to-schema-descriptor\n  produces_ast: true\n- id: family-data-override-metadata-rejected\n  category: validation-before-ast\n  source: "family Terrain {\\n    movementCost: Nat = 1\\n\\n    Plain,\\n    Mountain {\\n        movementCost = 4 {\\n            ~summary = \\\"solo aquí\\\"\\n        }\\n    }\\n}\\n"\n  cst_root: MudFileSyntax\n  expected_diagnostics:\n  - family-data-assignment-cannot-have-metadata\n  produces_ast: false\n'''
)

print('GLOBAL_COHERENCE_PHASE4_FAMILY_METADATA_OK')
