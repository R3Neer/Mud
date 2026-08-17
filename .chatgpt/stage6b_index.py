from pathlib import Path
import os
root=Path(os.environ['MUD_TARGET']).resolve()
p=root/'especificacion/README.md'
t=p.read_text(encoding='utf-8')
old='- Formación y unicidad de anclas, incluidas anclas estables de ramas decisionales.'
new='- Formación y unicidad de anclas públicas; las ramas funcionales de diccionarios decisionales usan claves locales y no reciben ancla pública conforme a D-090.'
if t.count(old)!=1:
    raise SystemExit(f'expected one stale branch-anchor line, found {t.count(old)}')
p.write_text(t.replace(old,new,1).rstrip('\n')+'\n',encoding='utf-8',newline='\n')
print('STAGE6B_OK')
