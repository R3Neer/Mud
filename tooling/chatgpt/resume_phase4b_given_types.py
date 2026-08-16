from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one match, got {count}: {old!r}")
    write(path, text.replace(old, new, 1))


# ---------------------------------------------------------------------
# Grammar: a given accepts the same complete type-expression as any value.
# Mutability is a semantic/syntactic-context restriction over the whole type
# tree, rather than a parallel grammar that only protects the outer level.
# ---------------------------------------------------------------------
path = "especificacion/gramatica/mud.ebnf"
old = '''given-declaration
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
      ;
'''
new = '''given-declaration
    ::= given-name , { "," , given-name } , ":" , type-expression , [ "=" , constant-expression ]
        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]
        ;
'''
replace_once(path, old, new)

# CST inventory mirrors the grammar and removes the obsolete parallel subset.
path = "especificacion/sintaxis/mud-syntax-kinds.yaml"
old = '''  given-declaration:
    kind: GivenDeclarationSyntax
    rhs: "given-name , { \",\" , given-name } , \":\" , union-type-expression , [ given-collection-specification ] , [ \"=\" , constant-expression ]\\n        , [ \"{\" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , \"}\" ]"
    references:
    - given-name
    - union-type-expression
    - given-collection-specification
    - constant-expression
    - declaration-layout
    - metadata-assignment
    - required-separation
  given-collection-specification:
    kind: GivenCollectionSpecificationSyntax
    rhs: "\"[\"\\n        , ( cardinality\\n            , [ optional-comma , given-collection-modifier\\n                , { optional-comma , given-collection-modifier }\\n              ]\\n          | given-collection-modifier\\n            , { optional-comma , given-collection-modifier }\\n          )\\n        , \"]\""
    references:
    - cardinality
    - optional-comma
    - given-collection-modifier
  given-collection-modifier:
    kind: GivenCollectionModifierSyntax
    rhs: "\"unique\"\\n      | \"ordered\" , [ \"by\" , order-key-path ]"
    references:
    - order-key-path
'''
new = '''  given-declaration:
    kind: GivenDeclarationSyntax
    rhs: "given-name , { \",\" , given-name } , \":\" , type-expression , [ \"=\" , constant-expression ]\\n        , [ \"{\" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , \"}\" ]"
    references:
    - given-name
    - type-expression
    - constant-expression
    - declaration-layout
    - metadata-assignment
    - required-separation
'''
replace_once(path, old, new)

# Coverage drops productions that no longer exist.
path = "especificacion/sintaxis/cobertura-sintactica.yaml"
old = '''  given-declaration:
    cst: GivenDeclarationSyntax
    ast:
      disposition: constructor
      target: GivenDecl
  given-collection-specification:
    cst: GivenCollectionSpecificationSyntax
    ast:
      disposition: wrapper
      target: readonly_collection_spec
  given-collection-modifier:
    cst: GivenCollectionModifierSyntax
    ast:
      disposition: enum-or-property
      target: readonly_collection_spec
'''
new = '''  given-declaration:
    cst: GivenDeclarationSyntax
    ast:
      disposition: constructor
      target: GivenDecl
'''
replace_once(path, old, new)

# Surface AST reuses TypeExpr. Readonly is an invariant on GivenDecl, not a
# second incomplete type algebra.
path = "especificacion/sintaxis/mud-surface-ast.asdl"
replace_once(
    path,
    '''    readonly_value_shape = (type_alternative first,
                            type_alternative* remaining,
                            readonly_collection_spec collection)
        attributes (source_origin origin)

''',
    '',
)
replace_once(
    path,
    '''    readonly_collection_spec = (cardinality cardinality,
                                cardinality_origin origin,
                                flag is_unique,
                                collection_order order)
        attributes (source_origin origin)

''',
    '',
)
replace_once(
    path,
    '''    given_decl = GivenDecl(given_name name,
                           readonly_value_shape shape,
                           expr? default_value,
                           metadata_assignment* metadata)
''',
    '''    given_decl = GivenDecl(given_name name,
                           type_expr type,
                           expr? default_value,
                           metadata_assignment* metadata)
''',
)

# Normative prose and transformation contract.
path = "especificacion/sintaxis/cst-a-ast-superficial.md"
replace_once(
    path,
    '''### `given`

`given-collection-specification` produce `ReadonlyCollectionSpec`; no existe campo para `elementsMutable`.
''',
    '''### `given`

`given-declaration` reutiliza `TypeExpr` completo, incluidos productos y diccionarios. Antes de construir `GivenDecl`, la validación contextual recorre todo el árbol de tipo y rechaza cualquier `collection-specification` que contenga `mut`, también dentro de productos, diccionarios o agrupaciones anidadas. No existe un segundo álgebra de tipos exclusivo de `given`.
''',
)

path = "especificacion/08-sintaxis-abstracta.md"
replace_once(
    path,
    '''`GivenDecl` usa `ReadonlyValueShape`, que no puede representar capacidad interior `mut`.
''',
    '''`GivenDecl` reutiliza directamente `TypeExpr`. Su inmutabilidad es un invariante de construcción del AST: la validación previa recorre el tipo completo y rechaza cualquier `CollectionSpec` con `elementsMutable = Enabled`, incluso si aparece dentro de un producto o diccionario. Así un `given` puede usar toda la forma de tipos sin transportar capacidad de escritura.
''',
)

path = "especificacion/07-gramatica-concreta.md"
old = '''Ningún `given` admite mutabilidad exterior ni interior: su especificación de colección puede declarar cardinalidad, `unique` y `ordered`, pero su producción excluye `mut`.
'''
new = '''Ningún `given` admite mutabilidad exterior ni interior. Su anotación usa la `type-expression` completa, por lo que puede ser un tipo básico, nominal, producto, colección o diccionario exacto/funcional. La validación previa al AST rechaza `mut` en cualquier `collection-specification` contenida en ese tipo, no solo en la colección exterior; cardinalidad, `unique` y `ordered` continúan disponibles donde la forma de tipo los admita.
'''
replace_once(path, old, new)

# Keep vigente ADRs literally current in the part affected by this fix.
path = "notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md"
old = '''Un `given` no admite mutabilidad exterior ni capacidad interior `mut`. Si una acción necesita escribir la colección suministrada o el estado de una `thing` recibida, ese valor constituye un sujeto de la operación y debe declararse mediante `for`.
'''
new = old + '''\nEl tipo de un `given` usa la forma general `type-expression`, incluidos productos y diccionarios exactos o funcionales. La prohibición de capacidad interior se aplica recursivamente a todo el tipo: cualquier modificador de colección `mut` dentro de un producto, valor de diccionario, colección anidada u otra subforma hace inválida la declaración. No se mantiene una gramática paralela de tipos readonly.
'''
replace_once(path, old, new)

path = "notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md"
old = '''Todo `given` tiene nombre obligatorio, es de solo lectura y no admite mutabilidad exterior ni capacidad interior. Puede declarar un predeterminado estático cerrado conforme a D-063.
'''
new = old + ''' Su tipo usa la forma general de tipos, incluidos productos y diccionarios; la ausencia de capacidad de escritura se valida sobre todo el árbol de tipo, no mediante una subgramática reducida.\n'''
replace_once(path, old, new)

# Conformance cases.
path = "especificacion/sintaxis/casos/cst-ast.yaml"
text = read(path)
old = '''- id: given-readonly
  category: participant
  source: "rule HasEnough for owner: Person\\ngiven amount: Money [1 ordered] = 1 {\\n    owner.balance >= amount\\n}\\n"
  cst_root: MudFileSyntax
  ast: GivenDecl(amount, ReadonlyCollectionSpec([1..1], ordered))
  produces_ast: true
'''
new = '''- id: given-readonly
  category: participant
  source: "rule HasEnough for owner: Person\\ngiven amount: Money [1 ordered] = 1 {\\n    owner.balance >= amount\\n}\\n"
  cst_root: MudFileSyntax
  ast: GivenDecl(amount, type=TypeExpr(Money [1..1 ordered]))
  normalizations:
  - validate-given-type-readonly-recursively
  produces_ast: true
'''
if text.count(old) != 1:
    raise SystemExit(f"given-readonly case count={text.count(old)}")
text = text.replace(old, new, 1)
if "id: given-exact-dictionary" in text:
    raise SystemExit("given dictionary cases already exist")
addition = r'''- id: given-exact-dictionary
  category: participant
  source: "rule AcceptsLookup given lookup: Key -> Value [*] {\n    true\n}\n"
  cst_root: MudFileSyntax
  ast: GivenDecl(lookup, type=TypeExpr(ExactDictionaryType(Key, Value, [*])))
  normalizations:
  - given-reuses-complete-type-expression
  semantic_expectations:
  - given-is-readonly-dictionary-value
  produces_ast: true
- id: given-functional-dictionary
  category: participant
  source: "rule AcceptsPolicy given policy: Input --> Output [ordered] {\n    true\n}\n"
  cst_root: MudFileSyntax
  ast: GivenDecl(policy, type=TypeExpr(DecisionDictionaryType(Input, Output, FirstMatch)))
  normalizations:
  - given-reuses-complete-type-expression
  semantic_expectations:
  - given-is-readonly-dictionary-value
  produces_ast: true
- id: given-nested-mut-invalid
  category: validation-before-ast
  source: "rule RejectsCapability given payload: (Nat [mut], Text) {\n    true\n}\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - given-type-carries-mut-capability
  semantic_expectations:
  - mut-rejection-recurses-through-product-type
  produces_ast: false
'''
if not text.endswith("\n"):
    text += "\n"
write(path, text + addition)

print("PHASE4B_GIVEN_TYPES_OK")
