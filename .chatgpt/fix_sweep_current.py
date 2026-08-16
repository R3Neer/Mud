from pathlib import Path
import sys

ROOT=Path(sys.argv[1]).resolve()

def read(rel): return (ROOT/rel).read_text(encoding='utf-8')
def write(rel,text): (ROOT/rel).write_text(text.rstrip('\n')+'\n',encoding='utf-8',newline='\n')
def exact(text,old,new,label):
    n=text.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1, found {n}')
    return text.replace(old,new,1)

# D-072 no estuvo cubierto por el sweep histórico: D-087 ancló participantes declarados.
rel='notas/decisiones/ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas.md'
t=read(rel)
t=exact(t,
'''Roles, `given`, variables de iteración y vinculaciones locales son símbolos léxicos sin ancla. Pueden repetir nombre en declaraciones o bloques independientes, pero no dentro de un mismo ámbito ni mediante sombreado de un nombre visible.''',
'''Los participantes declarados `for`, `on` y `given` son símbolos anclados subordinados a su propietario conforme a D-087. Las variables de iteración y vinculaciones locales ordinarias son símbolos léxicos sin ancla. Los nombres locales pueden repetirse en declaraciones o bloques independientes, pero no dentro de un mismo ámbito ni mediante sombreado de un nombre visible.''',
'D072 participants anchors')
t=exact(t,
'''3. Ausencia de ancla para roles, `given`, iteradores y locales.''',
'''3. Anclas subordinadas para participantes `for`, `on` y `given`, y ausencia de ancla para iteradores y locales ordinarios.''',
'D072 verification anchors')
if 'D-087' not in t.split('## Contexto',1)[0]:
    marker='- Ampliada por: [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]]\n'
    if t.count(marker)!=1: raise SystemExit('D072 relation marker')
    t=t.replace(marker, marker+'- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n',1)
write(rel,t)
print('SWEEP_CURRENT_FIX_OK')
