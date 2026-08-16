from pathlib import Path
import sys

ROOT=Path(sys.argv[1]).resolve()
def r(path): return (ROOT/path).read_text(encoding='utf-8')

def fail(msg, errors): errors.append(msg)

stale={
'notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades.md':['name = "meter"','plural = "meters"','abbreviation = "m"','prefixes = empty'],
'notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos.md':['    format ='],
'notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas.md':['anchor{...}','`name` es contextual dentro de un cuerpo de `thing`'],
'notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md':['puede omitirse','participante individual anónimo'],
'notas/decisiones/ADR-037-campos-y-dominios-declarativos.md':['omitir cardinalidad equivale a `[1]`','rechazo de `in` sobre un campo calculado','Rechazo de `mut` y de especificaciones de colección en campos calculados'],
'notas/decisiones/ADR-039-colecciones-y-diccionarios.md':['`unique` no se aplica porque','Leer una clave ausente produce el predeterminado'],
'notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md':['Vegetation,\n    Tree,\n    CanGrow','InitialActivationSet(references)','`name` y `prefixes`'],
'notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md':['[ declaration-reference','Es un conjunto finito y no ordenado.'],
'notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text.md':['anchor{','format = "{hour','La propiedad `format`'],
'notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md':['puede ser anónimo','Un rol anónimo'],
'notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md':['anchor{','name = "El Castillo Negro"','Egypt.name','propiedad intrínseca, pública, inmutable'],
'notas/decisiones/ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas.md':['Roles, `given`, variables de iteración y vinculaciones locales son símbolos léxicos sin ancla.','Ausencia de ancla para roles, `given`, iteradores y locales.'],
'notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md':['objetivos asignables de metadato','ancla estable de cada rama','El AST resuelto o IR registra'],
}
required={
'notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md':['Todo participante `for`, `on` y `given` debe declarar un identificador'],
'notas/decisiones/ADR-039-colecciones-y-diccionarios.md':['Leer una clave ausente produce `empty`','`unique`, cuando se escribe, se aplica a los **valores asociados**'],
'notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md':['things {','rules {','InitialActivationSet(things, rules)'],
'notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text.md':['"Rule: {CanRecruit~anchor}"','metadato `~format`'],
'notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md':['### Metadato estándar `~name`','Un campo ordinario `name` puede coexistir con `~name`'],
'notas/decisiones/ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas.md':['Los participantes declarados `for`, `on` y `given` son símbolos anclados subordinados a su propietario'],
'notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md':['ningún acceso `~` forma parte de los objetivos asignables','clave local canónica de cada rama'],
'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md':['no puede poseer metadata propia y no expone `~metadata`'],
'notas/decisiones/ADR-090-ramas-funcionales-sin-ancla-publica.md':['no pueden existir dos ramas ordinarias con el mismo selector canónico'],
'notas/decisiones/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado.md':['MUD posee un único AST normativo'],
'notas/decisiones/ADR-094-anclas-terminales-de-metadatos-configurados.md':['<ancla-del-propietario>~<identificador-metadata>'],
'notas/decisiones/ADR-095-extremos-vacios-como-ausencia-ordinaria.md':['`min` y `max` sobre una fuente finita y enumerable sin candidatos producen `empty`'],
}
errors=[]
for path,vals in stale.items():
    text=r(path)
    for val in vals:
        if val in text: fail(f'STALE {path}: {val!r}',errors)
for path,vals in required.items():
    text=r(path)
    for val in vals:
        if val not in text: fail(f'MISSING {path}: {val!r}',errors)

# Retired architecture names: only D-093 may narrate them; validator may guard the retired path.
for top in ('especificacion','notas'):
    for p in (ROOT/top).rglob('*'):
        if not p.is_file() or p.suffix not in {'.md','.yaml','.yml','.asdl','.py'}: continue
        rel=p.relative_to(ROOT).as_posix()
        for n,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
            if 'AST resuelto' not in line and 'mud-resolved-ast' not in line: continue
            if rel=='notas/decisiones/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado.md': continue
            if rel=='especificacion/sintaxis/validate_syntax_model.py' and 'retired_resolved_ast_path' in line: continue
            fail(f'RETIRED_ARCH {rel}:{n}:{line}',errors)

if (ROOT/'--repo').exists(): fail('accidental root file --repo exists',errors)
if 'duplicate_index' in r('especificacion/ir/mud-semantic-ir.asdl'): fail('decision branch duplicate_index survives',errors)
q60=r('notas/preguntas/Q-060-catalogo-reflectivo-de-typekind.md')
if 'resolved: false' not in q60: fail('Q-060 is not unresolved',errors)
policy=r('gobierno/POLITICA-DE-PREGUNTAS.md').lower()
for needle in ('criterio de cierre','evidencia de cierre'):
    if needle not in policy: fail(f'question policy missing {needle}',errors)

if errors:
    print(('\n'.join(errors)).encode('ascii','backslashreplace').decode('ascii'))
    raise SystemExit(f'POST_SWEEP_HAS_{len(errors)}_ISSUES')
print('POST_SWEEP_AUDIT_OK')
