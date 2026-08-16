from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
p=root/'especificacion/08-sintaxis-abstracta.md'
t=p.read_text(encoding='utf-8')
old='La clasificación como elemental o compuesta requiere resolver los `ActionCallCandidateEffect`; por ello pertenece al AST resuelto. La forma superficial no inventa una clasificación basada únicamente en la apariencia de un `postfix-expression`.'
new='La clasificación como elemental o compuesta requiere resolver los `ActionCallCandidateEffect`; por ello pertenece al IR semántico después de resolución y elaboración. La forma superficial no inventa una clasificación basada únicamente en la apariencia de un `postfix-expression`.'
if t.count(old)!=1: raise SystemExit(f'08 action classification: expected 1, found {t.count(old)}')
p.write_text(t.replace(old,new,1).rstrip('\n')+'\n',encoding='utf-8',newline='\n')
print('ARCH_RESIDUE_FIX_OK')
