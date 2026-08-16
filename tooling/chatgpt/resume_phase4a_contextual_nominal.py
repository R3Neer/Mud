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


# D-032 already decides contextual construction. Make the representation distinction explicit.
path = "notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal.md"
old = """Esta construcción contextual no requiere `to`. En cambio, una expresión ya tipada conserva su tipo y necesita conversión explícita:\n\n```mud\nrawName: Text = \"Ada\"\nplayerName: PlayerName =\n    rawName to PlayerName\n```\n"""
new = """Esta construcción contextual no requiere `to`. En cambio, una expresión ya tipada conserva su tipo y necesita conversión explícita:\n\n```mud\nrawName: Text = \"Ada\"\nplayerName: PlayerName =\n    rawName to PlayerName\n```\n\nLa representación elaborada conserva esta diferencia. Un literal todavía contextual que adquiere un alias por tipo esperado produce `ContextualNominalConstructionExpr(literal, target_type)`; una conversión escrita con `to` produce `ConversionExpr(value, target_type)`. La primera forma solo construye literales cuyo tipo o identidad nominal aún dependen del contexto y nunca convierte silenciosamente variables, accesos, llamadas u otras expresiones ya tipadas.\n"""
replace_once(path, old, new)

# Surface AST remains contextual; later elaboration must not collapse construction into an explicit cast.
path = "especificacion/08-sintaxis-abstracta.md"
old = """Los literales estructurales siguen siendo contextuales. `PositionalStructuralLiteralExpr` exige al menos dos valores y `NamedStructuralLiteralExpr` conserva uno o más componentes nombrados; no se selecciona todavía un alias concreto. Por tanto, los miembros del alias solo quedan disponibles después de elaboración contextual o de una conversión nominal explícita.\n"""
new = old + """\nCuando el tipado/elaboración recibe un tipo esperado que selecciona un único alias compatible, la forma posterior conserva una `ContextualNominalConstructionExpr` alrededor del literal. Esta forma no equivale a una `ConversionExpr`: esta última representa `to` escrito sobre un valor que ya tenía tipo. La construcción contextual no se aplica a variables, accesos, llamadas ni otras expresiones ya tipadas.\n"""
replace_once(path, old, new)

# Resolved/elaborated expression vocabulary must preserve the semantic distinction.
path = "especificacion/sintaxis/mud-resolved-ast.asdl"
old = """                  | NamedProductExpr(named_expr_component first,\n                                     named_expr_component* remaining)\n                  | ExactAssociationExpr(resolved_expr key, resolved_expr value)\n"""
new = """                  | NamedProductExpr(named_expr_component first,\n                                     named_expr_component* remaining)\n                  | ContextualNominalConstructionExpr(resolved_expr literal,\n                                                      anchor target_type)\n                  | ExactAssociationExpr(resolved_expr key, resolved_expr value)\n"""
replace_once(path, old, new)

# Conformance examples: same surface literal, distinct later semantic form from explicit `to`.
path = "especificacion/sintaxis/casos/cst-ast.yaml"
text = read(path)
if "id: contextual-nominal-basic" in text:
    raise SystemExit("contextual nominal cases already exist")
addition = r'''- id: contextual-nominal-basic
  category: typing-after-ast
  source: "alias PlayerName := Text\nthing Person {\n    nickname: PlayerName = \"Ada\"\n}\n"
  cst_root: MudFileSyntax
  ast: StoredFieldDecl(nickname, defaultValue=TextTemplateExpr([TextFragment(Ada)]))
  normalizations:
  - preserve-literal-untyped-until-contextual-elaboration
  semantic_expectations:
  - contextual-nominal-construction-target-PlayerName
  - no-synthetic-explicit-conversion
  produces_ast: true
- id: contextual-nominal-structural
  category: typing-after-ast
  source: "alias Coordinate {\n    x: Num\n    y: Num\n}\nthing Marker {\n    position: Coordinate = (x = 1, y = 2)\n}\n"
  cst_root: MudFileSyntax
  ast: StoredFieldDecl(position, defaultValue=NamedStructuralLiteralExpr([x=1,y=2]))
  normalizations:
  - preserve-structural-literal-untyped-until-contextual-elaboration
  semantic_expectations:
  - contextual-nominal-construction-target-Coordinate
  - components-available-after-nominal-construction
  produces_ast: true
- id: explicit-nominal-cast-distinct-from-context
  category: typing-after-ast
  source: "alias PlayerName := Text\nrule IsAda given raw: Text {\n    raw to PlayerName == \"Ada\"\n}\n"
  cst_root: MudFileSyntax
  ast: ComparisonChainExpr(ConversionExpr(raw, PlayerName), EqualRelation, TextTemplateExpr([TextFragment(Ada)]))
  semantic_expectations:
  - written-to-produces-conversion-expr
  - right-literal-contextually-constructs-PlayerName
  produces_ast: true
'''
if not text.endswith("\n"):
    text += "\n"
write(path, text + addition)

print("PHASE4A_CONTEXTUAL_NOMINAL_OK")
