from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
p = root / 'especificacion/sintaxis/casos/cst-ast.yaml'
t = p.read_text(encoding='utf-8')
old1 = 'source: "action Price given prices: Product -> Money {\\n    then total += 1\\n}\\n"'
new1 = 'source: "rule HasPrice given prices: Product -> Money {\\n    true\\n}\\n"'
old2 = 'source: "action Price given prices: Product -> Money [mut] {\\n    then total += 1\\n}\\n"'
new2 = 'source: "rule BadPrices given prices: Product -> Money [mut] {\\n    true\\n}\\n"'
for old, new in ((old1, new1), (old2, new2)):
    if t.count(old) != 1:
        raise SystemExit(f'expected one case source: {old}')
    t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8', newline='\n')
print('GIVEN_CASES_FIXED')
