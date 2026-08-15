from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
rel = 'especificacion/sintaxis/cst-sin-perdidas.md'
p = root / rel
text = p.read_text(encoding='utf-8')

# Add D-088 to the chapter's normative decision set.
front_anchor = '  - D-086\n'
if '  - D-088\n' not in text:
    if text.count(front_anchor) != 1:
        raise SystemExit(f'cst frontmatter anchor: expected 1, found {text.count(front_anchor)}')
    text = text.replace(front_anchor, front_anchor + '  - D-088\n', 1)

old = ('Entre las categorías concretas inventariadas se encuentra `BooleanBlockSyntax`, '
       'que conserva en orden las declaraciones locales iniciales y la expresión booleana final. '
       'La CST no amplía por sí sola su ámbito hasta `otherwise`; esa relación se establece al proyectar '
       'y resolver la construcción propietaria.')
new = ('Entre las categorías concretas inventariadas se encuentra `ExpressionBlockSyntax`, '
       'que conserva en orden las declaraciones locales iniciales y la expresión final. '
       'La categoría no fija por sí sola el contrato de esa expresión: el propietario decide si debe ser '
       'booleana, temporal, agregable u ordenable. La CST no amplía por sí sola su ámbito hasta `otherwise`; '
       'esa relación se establece al proyectar y resolver la construcción propietaria.')
if text.count(old) != 1:
    raise SystemExit(f'cst block paragraph: expected 1, found {text.count(old)}')
text = text.replace(old, new, 1)

# The independent D-087 cleanup must stay inherited from main.
if '- `ANCHOR_INTERPOLATION_START`.' in text:
    raise SystemExit('stale positive ANCHOR_INTERPOLATION_START returned')
if 'No existe `ANCHOR_INTERPOLATION_START`' not in text:
    raise SystemExit('D-087 negative anchor-token statement missing')
if 'BooleanBlockSyntax' in text:
    raise SystemExit('stale BooleanBlockSyntax remains in CST chapter')

p.write_text(text.rstrip('\n') + '\n', encoding='utf-8', newline='\n')
print('D088_CST_FIX_OK')
