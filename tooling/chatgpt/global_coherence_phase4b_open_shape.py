from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one occurrence, found {count}: {old!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')


def write_new(path: str, content: str) -> None:
    p = Path(path)
    if p.exists():
        raise SystemExit(f'{path}: already exists')
    p.write_text(content, encoding='utf-8', newline='\n')


# Do not resolve the pre-existing D-038 / EBNF contradiction here.
replace_once(
    'especificacion/gramatica/mud.ebnf',
    '''calculated-family-data-declaration\n    ::= field-name , [ ":" , type-expression ] , ":=" , value-expression\n        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]\n        ;\n''',
    '''calculated-family-data-declaration\n    ::= field-name , [ derived-value-shape ] , ":=" , value-expression\n        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]\n        ;\n''',
)
replace_once(
    'especificacion/sintaxis/mud-syntax-kinds.yaml',
    '''  calculated-family-data-declaration:\n    kind: CalculatedFamilyDataDeclarationSyntax\n    rhs: "field-name , [ \\":\\" , type-expression ] , \\":=\\" , value-expression\\n        , [ \\"{\\" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , \\"}\\" ]"\n    references:\n    - field-name\n    - type-expression\n    - value-expression\n    - declaration-layout\n    - metadata-assignment\n    - required-separation\n''',
    '''  calculated-family-data-declaration:\n    kind: CalculatedFamilyDataDeclarationSyntax\n    rhs: "field-name , [ derived-value-shape ] , \\":=\\" , value-expression\\n        , [ \\"{\\" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , \\"}\\" ]"\n    references:\n    - field-name\n    - derived-value-shape\n    - value-expression\n    - declaration-layout\n    - metadata-assignment\n    - required-separation\n''',
)
replace_once(
    'especificacion/sintaxis/mud-surface-ast.asdl',
    '''                     | CalculatedFamilyDataDecl(field_name name,\n                                                type_expr? type,\n                                                expr value,\n                                                metadata_assignment* metadata)\n''',
    '''                     | CalculatedFamilyDataDecl(field_name name,\n                                                derived_value_shape? shape,\n                                                expr value,\n                                                metadata_assignment* metadata)\n''',
)
replace_once(
    'especificacion/sintaxis/cobertura-sintactica.yaml',
    '      reason: conserva tipo opcional, expresión y metadata-body del descriptor calculado\n',
    '      reason: conserva la forma derivada vigente, la expresión y el metadata-body del descriptor calculado; Q-061 mantiene abierta su restricción exacta\n',
)
replace_once(
    'especificacion/sintaxis/cst-a-ast-superficial.md',
    '''Las declaraciones de datos se separan en almacenadas y calculadas. Cada declaración puede llevar un cuerpo inmediato formado exclusivamente por `metadata-assignment`; esa secuencia se conserva en `StoredFamilyDataDecl.metadata` o `CalculatedFamilyDataDecl.metadata`. En un dato calculado, la anotación superficial conservada es únicamente `type_expr?`: `in domain` y las especificaciones de colección no pertenecen a esta producción.\n''',
    '''Las declaraciones de datos se separan en almacenadas y calculadas. Cada declaración puede llevar un cuerpo inmediato formado exclusivamente por `metadata-assignment`; esa secuencia se conserva en `StoredFamilyDataDecl.metadata` o `CalculatedFamilyDataDecl.metadata`. El dato calculado conserva provisionalmente `derived_value_shape? shape`, porque Q-061 mantiene abierta la contradicción entre la EBNF actual y la restricción más estrecha escrita en D-038. Esta transformación no inventa una normalización que resuelva esa cuestión.\n''',
)

# Keep 07 descriptive of parsing while making the unresolved static boundary explicit.
replace_once(
    'especificacion/07-gramatica-concreta.md',
    'questions:\n  - Q-022\n  - Q-059\n',
    'questions:\n  - Q-022\n  - Q-059\n  - Q-061\n',
)
replace_once(
    'especificacion/07-gramatica-concreta.md',
    '''Los datos aparecen antes del primer miembro. Un dato almacenado puede llevar, después de su predeterminado opcional, un cuerpo inmediato que contenga solo declaraciones `~...`. Un dato calculado se escribe exclusivamente como `nombre [: Tipo] := expresión` y puede llevar el mismo metadata-body inmediato; no admite `in`, especificación de colección, predeterminado ni `mut`. El tipo calculado es opcional si se puede inferir de forma unívoca.\n''',
    '''Los datos aparecen antes del primer miembro. Un dato almacenado puede llevar, después de su predeterminado opcional, un cuerpo inmediato que contenga solo declaraciones `~...`. Un dato calculado puede llevar el mismo metadata-body inmediato. La EBNF conserva por ahora `derived-value-shape` en esta producción, mientras D-038 describe una forma más estrecha `nombre [: Tipo] := expresión`; Q-061 mantiene abierta esa discrepancia y esta decisión no la resuelve.\n''',
)

# 08 likewise preserves the unresolved surface shape.
replace_once(
    'especificacion/08-sintaxis-abstracta.md',
    'questions: []\n',
    'questions:\n  - Q-061\n',
)
replace_once(
    'especificacion/08-sintaxis-abstracta.md',
    '''Los datos asociados no admiten mutabilidad exterior. El dato almacenado conserva `metadata_assignment* metadata` junto a su forma y predeterminado. El dato calculado conserva únicamente `type_expr? type`, su expresión y `metadata_assignment* metadata`: una forma `in ...` o una especificación de colección sería inválida antes del AST.\n''',
    '''Los datos asociados no admiten mutabilidad exterior. El dato almacenado conserva `metadata_assignment* metadata` junto a su forma y predeterminado. El dato calculado conserva provisionalmente `derived_value_shape? shape`, su expresión y `metadata_assignment* metadata`; Q-061 decidirá si esa forma debe restringirse al tipo opcional descrito por D-038.\n''',
)

# D-038: add metadata without pretending this ADR contradiction has been resolved.
replace_once(
    'notas/decisiones/ADR-038-familias-cerradas-de-valores.md',
    '''El dato calculado reutiliza la forma de cálculo con tipo opcional definida por D-037:\n\n```text\nnombre [: tipo] := expresión [metadata-body]\n```\n\nLa anotación de tipo de un dato calculado es opcional. Si se omite, el compilador debe inferir un único tipo estático; si no puede hacerlo, la declaración es inválida. Un dato calculado no admite `mut`, `in`, especificación de colección, predeterminado ni almacenamiento propio: su forma y su valor proceden de la expresión. Tanto un dato almacenado como uno calculado pueden llevar un cuerpo inmediato formado exclusivamente por declaraciones de metadatos `~...`; D-091 fija que ese cuerpo pertenece al descriptor uniforme del dato.\n''',
    '''El dato calculado se describe aquí mediante la forma estrecha:\n\n```text\nnombre [: tipo] := expresión\n```\n\nLa anotación de tipo de un dato calculado es opcional. Si se omite, el compilador debe inferir un único tipo estático; si no puede hacerlo, la declaración es inválida. Este ADR afirma que el dato calculado no admite `mut`, `in`, especificación de colección, predeterminado ni almacenamiento propio, mientras la EBNF vigente conserva `derived-value-shape`; Q-061 registra explícitamente esa contradicción pendiente sin elegir una versión. Independientemente de su forma final, D-091 permite que tanto un dato almacenado como uno calculado lleven un cuerpo inmediato formado exclusivamente por declaraciones de metadatos `~...`, perteneciente al descriptor uniforme del dato.\n''',
)

# D-091 becomes strictly about descriptor identity and metadata.
p = Path('notas/decisiones/ADR-091-datos-de-family-como-descriptores-anclados.md')
text = p.read_text(encoding='utf-8')
text = text.replace(
    'Además, la EBNF había ampliado accidentalmente el dato calculado mediante `derived-value-shape`, aunque D-038 prohíbe `in` y especificaciones de colección en esa declaración.\n\n',
    'Existe además una contradicción previa entre D-038 y la EBNF sobre la forma exacta del dato calculado. D-091 no la resuelve; queda aislada en Q-061.\n\n',
)
text = text.replace(
    '''El dato calculado conserva la sintaxis estricta de D-038:\n\n```text\nnombre [: tipo] := expresión [metadata-body]\n```\n\nNo admite `mut`, `in`, especificación de colección, predeterminado ni almacenamiento propio. La EBNF y el AST superficial no deben representar esas formas prohibidas.\n\n''',
    '''El metadata-body se añade después de la forma de declaración del dato calculado que resulte vigente. Esta decisión no determina si dicha forma debe admitir todo `derived-value-shape` o limitarse al tipo opcional descrito por D-038; Q-061 conserva esa elección abierta.\n\n''',
)
text = text.replace(
    '- `CalculatedFamilyDataDecl` conserva `type_expr?`, no `derived_value_shape?`.\n',
    '- `CalculatedFamilyDataDecl` conserva provisionalmente `derived_value_shape?` hasta resolver Q-061.\n',
)
text = text.replace(
    '2. El dato calculado solo conserva tipo opcional antes de `:=`.\n3. CST, cobertura y proyección AST conservan el metadata-body en el descriptor.\n4. El AST superficial almacena metadatos en ambos constructores de datos y no en `FamilyDataAssignment`.\n5. La especificación de anclas identifica el descriptor bajo la categoría `family`.\n6. D-038 distingue la identidad del descriptor de la ausencia de identidad runtime del valor proyectado.\n',
    '2. CST, cobertura y proyección AST conservan el metadata-body en el descriptor sin cerrar Q-061.\n3. El AST superficial almacena metadatos en ambos constructores de datos y no en `FamilyDataAssignment`.\n4. La especificación de anclas identifica el descriptor bajo la categoría `family`.\n5. D-038 distingue la identidad del descriptor de la ausencia de identidad runtime del valor proyectado.\n',
)
text += '\n## Cuestión abierta relacionada\n\n[[notas/preguntas/Q-061-forma-de-datos-calculados-de-family|Q-061]] debe reconciliar la forma estrecha de D-038 con el `derived-value-shape` que hoy reconoce la EBNF. Nada en D-091 prejuzga esa resolución.\n'
p.write_text(text, encoding='utf-8', newline='\n')

write_new(
    'notas/preguntas/Q-061-forma-de-datos-calculados-de-family.md',
    '''---\nid: Q-061\ntitle: Forma declarable de datos calculados de family\npriority: P1\nopened: 2026-08-16\nresolved: false\nclosed:\ndecisions:\n  - D-037\n  - D-038\n  - D-091\naffects:\n  - especificacion/07-gramatica-concreta.md\n  - especificacion/08-sintaxis-abstracta.md\n  - especificacion/gramatica/mud.ebnf\n  - especificacion/sintaxis/mud-surface-ast.asdl\nsuperseded-by: []\n---\n\n# Q-061 — Forma declarable de datos calculados de `family`\n\n## Pregunta\n\n¿Qué forma puede declarar un dato calculado de `family`: solo un tipo opcional antes de `:=`, como afirma D-038, o el `derived-value-shape` más amplio que reconoce actualmente la EBNF?\n\n## Contexto\n\nD-038 escribe `nombre [: tipo] := expresión` y excluye `in` y especificaciones de colección. La EBNF vigente, en cambio, usa `[ derived-value-shape ]`, que también reconoce dominio y forma colectiva. El AST superficial conserva esa forma amplia. D-091 añade identidad de descriptor y metadata-body a los datos asociados, pero no necesita elegir entre ambas variantes y por tanto deja esta contradicción abierta.\n\n## Ya decidido\n\n- Un dato calculado es inmutable y se evalúa estáticamente por miembro.\n- Su tipo puede inferirse cuando la expresión determina uno de forma unívoca.\n- La declaración del dato posee descriptor `Field`, ancla subordinada y metadatos propios conforme a D-091.\n- Una asignación de miembro no puede dirigirse a un dato calculado.\n\n## Pendiente\n\n- C1: decidir si el contrato declarable es `[: tipo]` o todo `derived-value-shape`.\n- C2: si se elige la forma estrecha, fijar qué construcciones cuentan como `tipo` sin reintroducir por dentro dominio o especificación de colección.\n- C3: alinear EBNF, catálogo CST, AST superficial y ejemplos con una única respuesta.\n\n## Criterio de cierre\n\n- C1: existe una única forma normativa no contradictoria.\n- C2: la gramática expresa esa forma sin aceptar por otra ruta lo que la semántica prohíba.\n- C3: `CalculatedFamilyDataDecl` conserva exactamente las distinciones que sobrevivan al parsing y ninguna forma declarada válida se pierde.\n\n## Resolución\n\nPendiente.\n''',
)

print('GLOBAL_COHERENCE_PHASE4B_OPEN_SHAPE_OK')
