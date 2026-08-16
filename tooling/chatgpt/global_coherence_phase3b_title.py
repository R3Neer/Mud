from pathlib import Path
p=Path('notas/decisiones/ADR-091-identidad-de-datos-family-y-anclas-de-metadatos.md')
t=p.read_text(encoding='utf-8')
old='title: "Identidad de datos de family y anclas de metadatos"'
new='title: "Identidad de datos de `family` y anclas de metadatos"'
if old not in t: raise SystemExit('D-091 title not found')
p.write_text(t.replace(old,new,1),encoding='utf-8',newline='\n')
print('D091_TITLE_OK')
