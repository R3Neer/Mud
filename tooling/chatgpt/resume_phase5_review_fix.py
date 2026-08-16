from pathlib import Path

p = Path('notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md')
text = p.read_text(encoding='utf-8')
old = '10. Diferencia entre la referencia exacta `World` y un participante `on World` o `for World`.\n'
new = '10. Diferencia entre la referencia exacta `World` y un participante nombrado `on world: World` o `for world: World`.\n'
if text.count(old) != 1:
    raise SystemExit(f'D-036 verification marker count={text.count(old)}')
p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')
print('PHASE5_REVIEW_FIX_OK')
