from pathlib import Path

p = Path('notas/decisiones/ADR-093-extremos-vacios-como-ausencia-tipada.md')
text = p.read_text(encoding='utf-8')
old = '- Alinea con: [[ADR-039-colecciones-y-diccionarios|D-039]] y [[ADR-075-dominios-enumerables-all-y-valores-derivados|D-075]].\n\n'
if text.count(old) != 1:
    raise SystemExit('D-093 relation marker mismatch')
text = text.replace(old, '', 1)
p.write_text(text, encoding='utf-8', newline='\n')
print('PHASE4C_RELATION_FIX_OK')
