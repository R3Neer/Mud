from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one occurrence, found {count}: {old!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')


replace_once(
    'especificacion/sintaxis/mud-resolved-ast.asdl',
    '                                                       int source_ordinal,\n                                                       string is_fallback,\n                                                       resolved_expr selector,\n',
    '                                                       int source_ordinal,\n                                                       resolved_expr selector,\n',
)

replace_once(
    'notas/decisiones/ADR-090-ramas-funcionales-sin-ancla-publica.md',
    'El `source_ordinal` continúa conservándose por separado. En `FirstMatch` forma parte del valor funcional porque decide prioridad; en `AllMatches` conserva procedencia y diagnóstico, pero no se convierte en identidad persistente.\n',
    'La variante de `decision_branch_key` determina por sí sola si la rama es ordinaria o fallback; el AST resuelto no conserva un segundo flag `is_fallback` que pudiera contradecirla. El `source_ordinal` continúa conservándose por separado. En `FirstMatch` forma parte del valor funcional porque decide prioridad; en `AllMatches` conserva procedencia y diagnóstico, pero no se convierte en identidad persistente.\n',
)
replace_once(
    'notas/decisiones/ADR-090-ramas-funcionales-sin-ancla-publica.md',
    '2. `DecisionDependsOn` conserva el ancla del diccionario y una clave local de rama.\n',
    '2. `ResolvedDecisionBranch` no duplica la condición de fallback mediante un flag separado.\n3. `DecisionDependsOn` conserva el ancla del diccionario y una clave local de rama.\n',
)
replace_once(
    'notas/decisiones/ADR-090-ramas-funcionales-sin-ancla-publica.md',
    '3. El catálogo de anclas no enumera ramas funcionales como entidades públicas.\n4. D-085 ya no promete `CREATE`, `UPDATE`, `REMOVE` o `MOVE` dirigidos a una ancla de rama.\n5. D-087 mantiene las ramas fuera de la superficie metadata-bearing.\n',
    '4. El catálogo de anclas no enumera ramas funcionales como entidades públicas.\n5. D-085 ya no promete `CREATE`, `UPDATE`, `REMOVE` o `MOVE` dirigidos a una ancla de rama.\n6. D-087 mantiene las ramas fuera de la superficie metadata-bearing.\n',
)

print('GLOBAL_COHERENCE_PHASE3B_REVIEW_OK')
