from pathlib import Path
import sys

ROOT=Path(sys.argv[1]).resolve()

def read(rel): return (ROOT/rel).read_text(encoding='utf-8')
def write(rel,text): (ROOT/rel).write_text(text.rstrip('\n')+'\n',encoding='utf-8',newline='\n')
def exact(text,old,new,label):
    n=text.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1, found {n}')
    return text.replace(old,new,1)

# D-072 se toma del sweep histórico porque ya corrige participantes y diagnósticos.
# Se adapta a la frontera AST/IR de D-093 sin perder D-087.
rel='notas/decisiones/ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas.md'
t=read(rel)
if '- Ajustada a la frontera de fases de [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].' not in t:
    marker='- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]\n'
    if t.count(marker)!=1: raise SystemExit('D072 D087 relation marker mismatch')
    t=t.replace(marker, marker+'- Ajustada a la frontera de fases de [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].\n',1)
t=exact(t,
'''La separación entre CST, AST superficial y AST resuelto exige fijar cómo se representan ámbitos y candidatos. También debe distinguirse qué nombres poseen identidad semántica persistente y qué nombres solo vinculan valores dentro de una declaración.''',
'''La separación entre CST, AST superficial, resultados de resolución nominal e IR semántico exige fijar cómo se representan ámbitos y candidatos. También debe distinguirse qué nombres poseen identidad semántica persistente y qué nombres solo vinculan valores dentro de una declaración.''',
'D072 phase wording')
write(rel,t)
print('SWEEP_CURRENT_FIX_OK')
