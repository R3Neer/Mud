from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
p = root / 'notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial.md'
t = p.read_text(encoding='utf-8')
old = '  - "capítulo 09, resolución, AST resuelto, anclas, diagnósticos, LSP y grafo"'
new = '  - "capítulo 09, AST superficial, resolución nominal, tabla de símbolos, anclas, diagnósticos, LSP, grafo nominal e IR semántico"'
if t.count(old) != 1:
    raise SystemExit(f'D078 affects: expected 1, found {t.count(old)}')
p.write_text(t.replace(old, new, 1).rstrip('\n') + '\n', encoding='utf-8', newline='\n')
print('AST_REVIEW_FIX_OK')
