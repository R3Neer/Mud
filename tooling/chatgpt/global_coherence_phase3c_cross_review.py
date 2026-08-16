from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one occurrence, found {count}: {old!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')


replace_once(
    'especificacion/07-gramatica-concreta.md',
    '  - D-088\n',
    '  - D-088\n  - D-090\n',
)
replace_once(
    'especificacion/07-gramatica-concreta.md',
    'Las ramas solo cambian mediante edición semántica dirigida a sus anclas. `CREATE` inserta antes de `_` por defecto; `UPDATE`, `REMOVE` y `MOVE` conservan la identidad estable de la rama.\n',
    'Las ramas solo cambian mediante edición del modelo sobre el diccionario propietario. Una edición estructural puede insertar antes de `_` por defecto y puede actualizar, retirar o mover una rama, pero ninguna de esas operaciones se dirige a una ancla de rama ni presupone identidad pública independiente; D-090 fija su clave local en la representación resuelta.\n',
)

print('GLOBAL_COHERENCE_PHASE3C_CROSS_REVIEW_OK')
