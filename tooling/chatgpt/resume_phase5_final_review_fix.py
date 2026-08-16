from pathlib import Path

p = Path('notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md')
text = p.read_text(encoding='utf-8')
old = 'La forma especial `anchor{...}` dejó de existir con D-087.\n'
new = 'La forma especial `anchor{...}` dejó de existir con D-085.\n'
if text.count(old) != 1:
    raise SystemExit(f'D-068 attribution marker count={text.count(old)}')
p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')
print('PHASE5_FINAL_REVIEW_FIX_OK')
