from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one match, found {count}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")


replace_once(
    "especificacion/08-sintaxis-abstracta.md",
    """### Cardinalidad\n\nToda colección posee una cardinalidad explícita en el AST:\n\n- Omisión → `[1..1]` sintético.\n- `[a]` → `[a..a]`.\n- `[*]` → `[*..*]`.\n- `[a..b]` conserva ambos extremos.\n\nUn extremo `*` permanece como `EffectiveCardinality` en el AST superficial. La elaboración posterior aplica su valor efectivo según el lado y el contexto.\n""",
    """### Cardinalidad\n\n`CollectionSpec` conserva la procedencia de la cardinalidad. Si no se escribe ninguna, `cardinalityOrigin = OmittedCardinality`: el AST superficial no sintetiza `[1..1]` ni infiere todavía una cardinalidad efectiva. La elaboración posterior la determina según el propietario y, cuando corresponda, su inicializador.\n\nLas formas explícitas se normalizan así:\n\n- `[a]` → `[a..a]`.\n- `[*]` → `[*..*]`.\n- `[a..b]` conserva ambos extremos.\n\nUn extremo `*` escrito permanece como `EffectiveCardinality` en el AST superficial. La elaboración posterior aplica su valor efectivo según el lado y el contexto.\n""",
)

replace_once(
    "especificacion/sintaxis/casos/cst-ast.yaml",
    """- id: cardinality-omitted\n  category: collection\n  source: \"thing Counter {\\n    value: Nat\\n}\\n\"\n  cst_root: MudFileSyntax\n  ast: StoredFieldDecl(value, cardinality=[1..1])\n  normalizations:\n  - omitted-cardinality-to-one\n  produces_ast: true\n""",
    """- id: cardinality-omitted\n  category: collection\n  source: \"thing Counter {\\n    value: Nat\\n}\\n\"\n  cst_root: MudFileSyntax\n  ast: StoredFieldDecl(value, cardinalityOrigin=OmittedCardinality)\n  normalizations:\n  - preserve-omitted-cardinality\n  produces_ast: true\n""",
)
