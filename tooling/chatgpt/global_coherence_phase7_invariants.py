from pathlib import Path

def r(p: str) -> str:
    return Path(p).read_text(encoding='utf-8')

checks = {
    'notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades.md': ['name = "meter"','plural = "meters"','abbreviation = "m"','prefixes = empty'],
    'notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos.md': ['    format ='],
    'notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas.md': ['anchor{...}','`name` es contextual dentro de un cuerpo de `thing`'],
    'notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md': ['puede omitirse','participante individual anónimo'],
    'notas/decisiones/ADR-037-campos-y-dominios-declarativos.md': ['omitir cardinalidad equivale a `[1]`','rechazo de `in` sobre un campo calculado','Rechazo de `mut` y de especificaciones de colección en campos calculados'],
    'notas/decisiones/ADR-039-colecciones-y-diccionarios.md': ['`unique` no se aplica porque','Leer una clave ausente produce el predeterminado'],
    'notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md': ['Vegetation,\n    Tree,\n    CanGrow','InitialActivationSet(references)','`name` y `prefixes`'],
    'notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md': ['[ declaration-reference','Es un conjunto finito y no ordenado.'],
    'notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text.md': ['anchor{','format = "{hour','La propiedad `format`'],
    'notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md': ['puede ser anónimo','Un rol anónimo'],
    'notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md': ['anchor{','name = "El Castillo Negro"','Egypt.name','propiedad intrínseca, pública, inmutable'],
    'notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md': ['objetivos asignables de metadato','ancla estable de cada rama','El AST resuelto o IR registra'],
}
for p, stales in checks.items():
    text = r(p)
    for s in stales:
        if s in text:
            raise SystemExit(f'{p}: stale positive semantics: {s!r}')

must = {
    'notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md': ['Todo participante `for`, `on` y `given` debe declarar un identificador'],
    'notas/decisiones/ADR-039-colecciones-y-diccionarios.md': ['Leer una clave ausente produce `empty`','`unique`, cuando se escribe, se aplica a los **valores asociados**'],
    'notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md': ['things {','rules {','InitialActivationSet(things, rules)'],
    'notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text.md': ['"Rule: {CanRecruit~anchor}"','metadato `~format`'],
    'notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md': ['### Metadato estándar `~name`','Un campo ordinario `name` puede coexistir con `~name`'],
    'notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md': ['ningún acceso `~` forma parte de los objetivos asignables','clave local canónica de cada rama'],
}
for p, needed in must.items():
    text = r(p)
    for s in needed:
        if s not in text:
            raise SystemExit(f'{p}: missing current semantics: {s!r}')

print('PHASE7_ADR_SWEEP_INVARIANTS_OK')
