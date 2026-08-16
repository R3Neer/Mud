from pathlib import Path
import re, sys

root = Path(sys.argv[1]).resolve()

def rd(rel):
    return (root / rel).read_text(encoding='utf-8')

def wr(rel, text):
    (root / rel).write_text(text.rstrip('\n') + '\n', encoding='utf-8', newline='\n')

def exact(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    return text.replace(old, new, 1)

def yaml_block(text, key, replacement=None):
    pat = re.compile(rf'(?ms)^  {re.escape(key)}:\n.*?(?=^  [A-Za-z0-9_-]+:\n|\Z)')
    ms = list(pat.finditer(text))
    if len(ms) != 1:
        raise SystemExit(f'yaml {key}: expected 1 block, found {len(ms)}')
    repl = '' if replacement is None else replacement.rstrip() + '\n'
    return text[:ms[0].start()] + repl + text[ms[0].end():]

# EBNF: given accepts the general type-expression. Read-only is a static
# contract of given, not a separate syntactic type universe.
p = 'especificacion/gramatica/mud.ebnf'
t = rd(p)
t = exact(t,
'''given-declaration
    ::= given-name , { "," , given-name } , ":" , union-type-expression , [ given-collection-specification ] , [ "=" , constant-expression ]
        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]
        ;

given-collection-specification
    ::= "["
        , ( cardinality
            , [ optional-comma , given-collection-modifier
                , { optional-comma , given-collection-modifier }
              ]
          | given-collection-modifier
            , { optional-comma , given-collection-modifier }
          )
        , "]"
        ;

given-collection-modifier
    ::= "unique"
      | "ordered" , [ "by" , order-key-path ]
      ;''',
'''given-declaration
    ::= given-name , { "," , given-name } , ":" , type-expression , [ "=" , constant-expression ]
        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]
        ;''', 'grammar given')
wr(p, t)

# CST inventory mirrors the EBNF.
p = 'especificacion/sintaxis/mud-syntax-kinds.yaml'
t = rd(p)
t = yaml_block(t, 'given-declaration', '''  given-declaration:
    kind: GivenDeclarationSyntax
    rhs: "given-name , { \",\" , given-name } , \":\" , type-expression , [ \"=\" , constant-expression ]\\n        , [ \"{\" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , \"}\" ]"
    references:
    - given-name
    - type-expression
    - constant-expression
    - declaration-layout
    - metadata-assignment
    - required-separation''')
t = yaml_block(t, 'given-collection-specification', None)
t = yaml_block(t, 'given-collection-modifier', None)
wr(p, t)

# Coverage drops the retired concrete-only wrappers.
p = 'especificacion/sintaxis/cobertura-sintactica.yaml'
t = rd(p)
t = yaml_block(t, 'given-collection-specification', None)
t = yaml_block(t, 'given-collection-modifier', None)
wr(p, t)

# Surface AST uses the ordinary TypeExpr. Invalid mut capabilities remain
# representable and are rejected by the static contract of given.
p = 'especificacion/sintaxis/mud-surface-ast.asdl'
t = rd(p)
t = exact(t,
'''    readonly_value_shape = (type_alternative first,
                            type_alternative* remaining,
                            readonly_collection_spec collection)
        attributes (source_origin origin)

''', '', 'delete readonly_value_shape')
t = exact(t,
'''    readonly_collection_spec = (cardinality cardinality,
                                cardinality_origin origin,
                                flag is_unique,
                                collection_order order)
        attributes (source_origin origin)

''', '', 'delete readonly_collection_spec')
t = exact(t,
'''    given_decl = GivenDecl(given_name name,
                           readonly_value_shape shape,
                           expr? default_value,
                           metadata_assignment* metadata)''',
'''    given_decl = GivenDecl(given_name name,
                           type_expr shape,
                           expr? default_value,
                           metadata_assignment* metadata)''', 'GivenDecl shape')
wr(p, t)

# Transformation prose.
p = 'especificacion/sintaxis/cst-a-ast-superficial.md'
t = rd(p)
t = exact(t,
'''### `given`

`given-collection-specification` produce `ReadonlyCollectionSpec`; no existe campo para `elementsMutable`.
''',
'''### `given`

`given-declaration` proyecta su anotación mediante el mismo `TypeExpr` superficial que los demás contextos de tipo. Esto permite conservar tipos diccionario completos sin introducir una segunda jerarquía de tipos de solo lectura. La presencia de capacidad `mut` puede quedar representada en el AST superficial, pero D-063 la rechaza estáticamente para `given` antes de producir IR semántico.
''', 'projection collection given')
t = exact(t,
'''### `given`

Se convierten nombre, tipo, dominio, colección de solo lectura, predeterminado y metadatos. El predeterminado continúa siendo `expr`; su carácter constante se comprueba después.
''',
'''### `given`

Se convierten nombre, `TypeExpr`, predeterminado y metadatos. Un tipo diccionario se conserva mediante los constructores ordinarios `ExactDictionaryType` o `DecisionDictionaryType`. El predeterminado continúa siendo `expr`; su carácter constante y la prohibición de cualquier capacidad `mut` del `given` se comprueban después.
''', 'projection participants given')
wr(p, t)

# AST prose.
p = 'especificacion/08-sintaxis-abstracta.md'
t = rd(p)
t = exact(t,
'`GivenDecl` usa `ReadonlyValueShape`, que no puede representar capacidad interior `mut`.',
'`GivenDecl` usa el mismo `TypeExpr` superficial que los demás contextos de tipo, por lo que puede representar diccionarios exactos o decisionales. D-063 mantiene `given` como parámetro de solo lectura: cualquier `mut` que aparezca en esa forma se conserva únicamente para diagnóstico y se rechaza estáticamente antes del IR semántico.', '08 GivenDecl')
wr(p, t)

# Concrete prose: add explicit valid form near dictionaries/given contract.
p = 'especificacion/07-gramatica-concreta.md'
t = rd(p)
anchor = 'La resolución de nombres, tipos, dominios y efectos no pertenece a esta validación.\n'
addition = anchor + '''\nUn `given` reutiliza la expresión general de tipo, incluidos los diccionarios:\n\n```mud\ngiven prices: Product -> Money\n```\n\nLa gramática puede conservar un modificador `mut` escrito dentro de esa expresión para diagnóstico, pero D-063 lo hace estáticamente inválido: `given` nunca concede capacidad de escritura.\n'''
t = exact(t, anchor, addition, '07 given dictionaries')
wr(p, t)

# Keep the governing ADR literally current.
p = 'notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md'
t = rd(p)
anchor = 'Un `given` no admite mutabilidad exterior ni capacidad interior `mut`. Si una acción necesita escribir la colección suministrada o el estado de una `thing` recibida, ese valor constituye un sujeto de la operación y debe declararse mediante `for`.\n'
addition = anchor + '''\nLa anotación de un `given` admite la expresión general de tipo, incluidos tipos diccionario exactos y decisionales. Por ejemplo, `given prices: Product -> Money` es válido. La posibilidad de escribir un diccionario no concede capacidad: todas sus colecciones y valores siguen sometidos a la prohibición anterior de `mut` en `given`.\n'''
t = exact(t, anchor, addition, 'D063 given dictionaries')
wr(p, t)

# Conformance cases.
p = 'especificacion/sintaxis/casos/cst-ast.yaml'
t = rd(p)
if 'id: given-dictionary-type' in t:
    raise SystemExit('cases already present')
t += '''\n- id: given-dictionary-type\n  category: participant\n  source: "action Price given prices: Product -> Money {\\n    then total += 1\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: GivenDecl(prices, TypeExpr(ExactDictionaryType(Product, Money, ...)), defaultValue=None, metadata=[])\n  semantic_expectations:\n  - given-is-readonly\n  produces_ast: true\n- id: given-dictionary-mut-rejected\n  category: validation-after-ast\n  source: "action Price given prices: Product -> Money [mut] {\\n    then total += 1\\n}\\n"\n  cst_root: MudFileSyntax\n  expected_diagnostics:\n  - given-mutability-forbidden\n  produces_ast: true\n'''
wr(p, t)

# Guard against stale parallel type hierarchy.
for rel in [
    'especificacion/gramatica/mud.ebnf',
    'especificacion/sintaxis/mud-syntax-kinds.yaml',
    'especificacion/sintaxis/cobertura-sintactica.yaml',
    'especificacion/sintaxis/mud-surface-ast.asdl',
]:
    s = rd(rel)
    for stale in ('given-collection-specification', 'given-collection-modifier', 'readonly_value_shape', 'readonly_collection_spec'):
        if stale in s:
            raise SystemExit(f'{rel}: stale {stale}')

print('GIVEN_DICTIONARY_TRANSFORM_OK')
