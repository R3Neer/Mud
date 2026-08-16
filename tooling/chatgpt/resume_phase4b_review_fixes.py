from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')

replace_once(
    'notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md',
    '\n Su tipo usa la forma general de tipos, incluidos productos y diccionarios; la ausencia de capacidad de escritura se valida sobre todo el árbol de tipo, no mediante una subgramática reducida.\n',
    '\n\nSu tipo usa la forma general de tipos, incluidos productos y diccionarios; la ausencia de capacidad de escritura se valida sobre todo el árbol de tipo, no mediante una subgramática reducida.\n',
)
replace_once(
    'especificacion/sintaxis/casos/cst-ast.yaml',
    'source: "rule AcceptsPolicy given policy: Input --> Output [ordered] {\\n    true\\n}\\n"',
    'source: "rule AcceptsPolicy given policy: Input --> Output {\\n    true\\n}\\n"',
)
replace_once(
    'especificacion/sintaxis/casos/cst-ast.yaml',
    'ast: GivenDecl(policy, type=TypeExpr(DecisionDictionaryType(Input, Output, FirstMatch)))',
    'ast: GivenDecl(policy, type=TypeExpr(DecisionDictionaryType(Input, Output, AllMatches)))',
)
print('PHASE4B_REVIEW_FIXES_OK')
