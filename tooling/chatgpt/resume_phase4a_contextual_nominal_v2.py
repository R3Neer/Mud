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
# Clarify the representation boundary first. D-052 keeps the conceptual
# phases separate; this merely states when the existing resolved schema is
# complete. No extra canonical AST snapshot is invented after name lookup.
# ---------------------------------------------------------------------
path = "especificacion/sintaxis/README.md"
replace_once(
    path,
    """archivo .mud\n→ scanner completo\n→ tokens significativos + trivia\n→ CST sin pérdidas\n→ validación sintáctica contextual\n→ AST superficial normalizado\n→ resolución\n→ AST resuelto\n→ tipado/elaboración\n→ IR\n""",
    """archivo .mud\n→ scanner completo\n→ tokens significativos + trivia\n→ CST sin pérdidas\n→ validación sintáctica contextual\n→ AST superficial normalizado\n→ resolución nominal (símbolos + grafo parcial)\n→ tipado, elaboración y análisis estático\n→ AST semántico resuelto\n→ IR\n""",
)
replace_once(
    path,
    """| `mud-resolved-ast.asdl` | Normativo mecánico | Contrato del AST resuelto, tipos unión, símbolos, anclas y dependencias. |""",
    """| `mud-resolved-ast.asdl` | Normativo mecánico | Contrato del AST semántico resuelto previo al IR: símbolos y anclas ya resueltos, tipos elaborados y dependencias semánticas. |""",
)

path = "especificacion/08-sintaxis-abstracta.md"
replace_once(
    path,
    """El contrato de la fase posterior vive en [[mud-resolved-ast]]. Allí las referencias se sustituyen por `AnchoredSymbol` o `LocalSymbol`, las uniones quedan normalizadas y el grafo nominal se expresa mediante aristas reconstruibles.\n""",
    """El contrato semántico previo al IR vive en [[mud-resolved-ast]]. No es una instantánea tomada inmediatamente después de buscar nombres: se completa tras resolución nominal, tipado, elaboración y los análisis estáticos que alimentan su forma. Allí las referencias ya usan `AnchoredSymbol` o `LocalSymbol`, las uniones están elaboradas y las dependencias se expresan mediante aristas reconstruibles. La resolución nominal temprana puede construir símbolos y un grafo parcial sin introducir otro AST canónico intermedio.\n""",
)
replace_once(
    path,
    """texto fuente\n→ tokens y trivia\n→ CST sin pérdidas\n→ validación sintáctica contextual\n→ AST superficial normalizado\n→ resolución de nombres\n→ AST resuelto\n→ tipado y elaboración\n→ IR\n""",
    """texto fuente\n→ tokens y trivia\n→ CST sin pérdidas\n→ validación sintáctica contextual\n→ AST superficial normalizado\n→ resolución nominal (símbolos + grafo parcial)\n→ tipado, elaboración y análisis estático\n→ AST semántico resuelto\n→ IR\n""",
)
old = """Los literales estructurales siguen siendo contextuales. `PositionalStructuralLiteralExpr` exige al menos dos valores y `NamedStructuralLiteralExpr` conserva uno o más componentes nombrados; no se selecciona todavía un alias concreto. Por tanto, los miembros del alias solo quedan disponibles después de elaboración contextual o de una conversión nominal explícita.\n"""
new = old + """\nCuando la elaboración recibe un tipo esperado que selecciona un único alias compatible, el AST semántico resuelto conserva una `ContextualNominalConstructionExpr` alrededor del literal. Esta forma no equivale a `ConversionExpr`: esta última representa `to` escrito sobre un valor que ya tenía tipo. La construcción contextual solo puede materializar un literal cuya identidad nominal dependía todavía del contexto; no convierte silenciosamente variables, accesos, llamadas ni otras expresiones ya tipadas.\n"""
replace_once(path, old, new)

path = "especificacion/09-nombres-y-anclas.md"
needle = """4. La resolución de miembros completa accesos, llamadas y abreviaturas contextuales.\n\nLa norma se expresa mediante entornos y conjuntos de candidatos. Una implementación puede usar scope graphs si reproduce exactamente prioridades, candidatos, ambigüedades y rechazos.\n"""
replacement = """4. La resolución de miembros completa accesos, llamadas y abreviaturas contextuales.\n\nEstas etapas no obligan a materializar un AST canónico distinto al terminar cada una. La resolución nominal temprana produce la tabla de símbolos y permite construir el grafo nominal parcial; `mud-resolved-ast.asdl` describe la forma semántica acumulada una vez completados también tipado, elaboración y los análisis estáticos que preceden al IR.\n\nLa norma se expresa mediante entornos y conjuntos de candidatos. Una implementación puede usar scope graphs si reproduce exactamente prioridades, candidatos, ambigüedades y rechazos.\n"""
replace_once(path, needle, replacement)
replace_once(
    path,
    """El esquema mecánico [[mud-resolved-ast]] representa esta frontera: una declaración persistente y todo participante declarado usan `AnchoredSymbol`; los locales e iteradores ordinarios usan `LocalSymbol` subordinado a su propietario. Las ramas funcionales no son símbolos: sus dependencias se reconstruyen mediante el ancla del diccionario propietario y una `decision_branch_key` local.\n""",
    """Esta frontera nominal temprana se representa mediante símbolos y el grafo parcial, no mediante una segunda instantánea canónica del AST. El esquema mecánico [[mud-resolved-ast]] representa el resultado semántico posterior ya elaborado: una declaración persistente y todo participante declarado usan `AnchoredSymbol`; los locales e iteradores ordinarios usan `LocalSymbol` subordinado a su propietario. Las ramas funcionales no son símbolos: sus dependencias se reconstruyen mediante el ancla del diccionario propietario y una `decision_branch_key` local.\n""",
)

path = "especificacion/sintaxis/mud-resolved-ast.asdl"
replace_once(
    path,
    """-- MUD 1.0 — Contrato del AST resuelto\n--\n-- Complementa mud-surface-ast.asdl. Conserva procedencia y forma semántica,\n-- pero sustituye referencias nominales por símbolos y anclas resueltas.\n""",
    """-- MUD 1.0 — Contrato del AST semántico resuelto\n--\n-- Complementa mud-surface-ast.asdl. Esta forma se completa después de la\n-- resolución nominal, el tipado, la elaboración y los análisis estáticos\n-- que preceden al IR; no representa la instantánea temprana de name lookup.\n-- Conserva procedencia y significado resuelto mediante símbolos, anclas,\n-- tipos elaborados y dependencias semánticas.\n""",
)
replace_once(
    path,
    """                  | NamedProductExpr(named_expr_component first,\n                                     named_expr_component* remaining)\n                  | ExactAssociationExpr(resolved_expr key, resolved_expr value)\n""",
    """                  | NamedProductExpr(named_expr_component first,\n                                     named_expr_component* remaining)\n                  | ContextualNominalConstructionExpr(resolved_expr literal,\n                                                      anchor target_type)\n                  | ExactAssociationExpr(resolved_expr key, resolved_expr value)\n""",
)

# ---------------------------------------------------------------------
# D-032 already decides contextual construction. Preserve its distinction
# explicitly in the semantic representation.
# ---------------------------------------------------------------------
path = "notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal.md"
old = """Esta construcción contextual no requiere `to`. En cambio, una expresión ya tipada conserva su tipo y necesita conversión explícita:\n\n```mud\nrawName: Text = \"Ada\"\nplayerName: PlayerName =\n    rawName to PlayerName\n```\n"""
new = old + """\nLa representación semántica conserva la diferencia: un literal todavía contextual que adquiere un alias por tipo esperado produce `ContextualNominalConstructionExpr(literal, target_type)`; una conversión escrita con `to` produce `ConversionExpr(value, target_type)`. La primera forma solo construye literales cuya identidad nominal aún depende del contexto y nunca convierte silenciosamente variables, accesos, llamadas u otras expresiones ya tipadas.\n"""
replace_once(path, old, new)

# Conformance examples retain the surface node and state the later expectation.
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

print("PHASE4A_V2_OK")
