from pathlib import Path
import os,re,yaml,sys
try: sys.stdout.reconfigure(encoding='utf-8',errors='backslashreplace')
except Exception: pass
ROOT=Path(os.environ['MUD_TARGET']).resolve()

def text(name): return (ROOT/'notas/decisiones'/name).read_text(encoding='utf-8')
def forbid(name, pattern, label):
    t=text(name)
    if re.search(pattern,t,re.M|re.S): raise SystemExit(f'{name}: stale {label}')
def need(name, needle):
    if needle not in text(name): raise SystemExit(f'{name}: missing {needle}')

forbid('ADR-021-ciclo-de-vida-logico-y-suspension.md',r'start with \{\s*Kingdom', 'flat start with')
need('ADR-021-ciclo-de-vida-logico-y-suspension.md','things {')
need('ADR-021-ciclo-de-vida-logico-y-suspension.md','rules {')
for name in ['ADR-028-sistema-de-magnitudes-y-unidades.md']:
    for old in [r'^\s*name\s*=',r'^\s*plural\s*=',r'^\s*abbreviation\s*=',r'^\s*prefixes\s*=']:
        forbid(name,old,'old unit property syntax')
forbid('ADR-029-intervalos-estrellas-y-ciclos.md',r'^\s*format\s*=','old format property')
need('ADR-029-intervalos-estrellas-y-ciclos.md','~format')
forbid('ADR-036-participantes-receptores-y-llamadas.md',r'participante individual an[oó]nimo|rol básico anónimo','anonymous participant')
need('ADR-036-participantes-receptores-y-llamadas.md','Todo participante `for`, `on` y `given` debe declarar un identificador')
forbid('ADR-054-definiciones-canonicas-y-activacion-inicial.md',r'start with \{\s*(?:[A-Z][A-Za-z0-9_]*\s*,)','flat start with')
need('ADR-054-definiciones-canonicas-y-activacion-inicial.md','things {')
forbid('ADR-055-tests-declarativos-y-diagnosticos-otherwise.md',r'start with \{\s*(?:[A-Z][A-Za-z0-9_]*\s*,)','flat local start with')
for name in ['ADR-035-organizacion-nombres-using-y-anclas.md','ADR-061-resultados-fallidos-y-plantillas-text.md','ADR-068-thing-universal-y-nombre-intrinseco.md']:
    # Historical explanation may mention the removed spelling only when explicitly negated/retired.
    for m in re.finditer(r'anchor\{', text(name)):
        context=text(name)[max(0,m.start()-100):m.start()+120].lower()
        if not any(x in context for x in ['retira','no existe','ya no','elimina','sustitu']):
            raise SystemExit(f'{name}: active anchor interpolation remains')
need('ADR-038-familias-cerradas-de-valores.md','metadato estándar `~name: Name`')
need('ADR-038-familias-cerradas-de-valores.md','descriptor `Field`, ancla subordinada y metadatos propios')
forbid('ADR-038-familias-cerradas-de-valores.md',r'Cada miembro posee un `name: Text`','old family member name')
need('ADR-037-campos-y-dominios-declarativos.md','D-075')
need('ADR-039-colecciones-y-diccionarios.md','D-085')
need('ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md','identificador')
print('ADR_SWEEP_ASSERTIONS_OK')
