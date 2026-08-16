from pathlib import Path

p = Path('notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md')
text = p.read_text(encoding='utf-8')
replacements = {
    '10. Diferencia entre la referencia exacta `World` y un participante `on World` o `for World`.\n':
        '10. Diferencia entre la referencia exacta `World` y un participante nombrado `on world: World` o `for world: World`.\n',
    'El tipo incorporado `Thing` admite cualquier `thing`. Por tanto, un rol `for` de tipo `Thing` acepta cualquier identidad concreta compatible y `on Thing` enumera todas las `thing` concretas y activas; la raíz abstracta no produce una vinculación propia.\n':
        'El tipo incorporado `Thing` admite cualquier `thing`. Por tanto, un rol `for` de tipo `Thing` acepta cualquier identidad concreta compatible y un rol `on` de tipo `Thing` enumera todas las `thing` concretas y activas; la raíz abstracta no produce una vinculación propia.\n',
}
for old, new in replacements.items():
    if text.count(old) != 1:
        raise SystemExit(f'D-036 review marker count={text.count(old)} for {old!r}')
    text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8', newline='\n')
print('PHASE5_REVIEW_FIX_OK')
