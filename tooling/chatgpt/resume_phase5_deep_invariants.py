from pathlib import Path


def r(path: str) -> str:
    return Path(path).read_text(encoding='utf-8')


d36=r('notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md')
for stale in ('puede omitirse. Los accesos no cualificados dentro del cuerpo se resuelven contra esos participantes anónimos','un rol básico anónimo','Participante individual anónimo','participantes individuales anónimos','La omisión del nombre de participante individual','`on World` o `for World`','`on Thing` enumera'):
    assert stale not in d36, stale
assert d36.count('`on world: World` o `for world: World`') == 2
assert 'un rol `on` de tipo `Thing` enumera' in d36

spec=r('especificacion/07-gramatica-concreta.md')
assert '`on World` y un rol `for World`' not in spec
assert 'Los participantes `on world: World` y `for world: World`' in spec

d63=r('notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md')
assert 'puede ser anónimo' not in d63 and 'Un rol anónimo solo admite' not in d63
assert 'Todo rol `for` posee identificador fuente explícito conforme a D-087' in d63

d68=r('notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md')
assert 'title: "`Thing` universal, identificador y presentación reflectiva"' in d68
assert '# ADR-068 — `Thing` universal, identificador y presentación reflectiva' in d68
for stale in ('`on Thing`','anchor{Thing}','anchor{value}','### Propiedad intrínseca `name`','thing BlackCastle {\n    name =','`Egypt.name`','`value.name` vale','Los campos ordinarios llamados `name` dejan de ser válidos'):
    assert stale not in d68, stale
assert '~identifier : Name' in d68 and '~name       : Name' in d68
assert '`Thing~anchor` devuelve ese valor reflectivo' in d68
assert 'Un campo ordinario llamado `name`' in d68

d15=r('notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente.md')
assert 'La propiedad intrínseca `name` tampoco se hereda.' not in d15
assert '`~identifier` pertenece al descriptor local de cada identidad' in d15
assert 'La presentación configurable `~name` tampoco se hereda' in d15
assert 'ADR-087-metadatos-reflectivos' in d15

d28=r('notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades.md')
for stale in ('        name = "meter"','        plural = "meters"','        abbreviation = "m"','    name = "minute"','    plural = "minutes"','    abbreviation = "min"','        name = "fastie"','        plural = "fasties"','        abbreviation = "fst"','`prefixes = empty`','`prefixes = all`','`prefixes = [p1, p2, ...]`','nombre intrínseco y el ancla'):
    assert stale not in d28, stale
for current in ('~name = "meter"','~plural = "meters"','~abbreviation = "m"','~prefixes = empty','~prefixes = all','`~identifier`'):
    assert current in d28, current
assert 'ADR-087-metadatos-reflectivos' in d28

d35=r('notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas.md')
assert 'D-061 añade `anchor{...}` como forma contextual exclusiva' not in d35
assert 'D-085 retira la forma contextual `anchor{...}`' in d35
assert '`~anchor`' in d35 and '"{value~anchor}"' in d35

d61=r('notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text.md')
for stale in ('- `anchor{d}` inserta el ancla canónica','`anchor` es contextual únicamente dentro de una plantilla','El valor de su propiedad intrínseca `name`','El nombre nominal del miembro','Su `format`, si existe','Una magnitud de punto sin `format`','omite su `format`','unidades escritas en `format`','Dentro del `format`','La propiedad `format` de una magnitud','no el `format`','`anchor{...}` es una forma contextual de plantilla','huecos de ancla','`anchor{...}` conserva la identidad canónica','mediante `anchor{...}`','Rechazo de `anchor{...}` sobre valores'):
    assert stale not in d61, stale
assert 'un ancla se interpola mediante la expresión ordinaria `{e~anchor}`' in d61
assert 'No existe un hueco especial `anchor{...}`' in d61
assert '| `thing` | Su presentación `~name` efectiva |' in d61
assert '| Miembro de `family` | Su presentación `~name` efectiva |' in d61
assert '| Magnitud de punto | Su `~format`, si está configurado;' in d61
assert '`~abbreviation`' in d61 and '`~plural`' in d61
assert '"Rule: {CanRecruit~anchor}"' in d61
assert 'Obtención de anclas mediante la propiedad reflectiva `~anchor`' in d61
assert 'ADR-087-metadatos-reflectivos' in d61

d70=r('notas/decisiones/ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado.md')
assert 'integra el `name` intrínseco' not in d70
assert 'integra la separación entre `~identifier`, `~name` y campos ordinarios' in d70

cov=r('especificacion/sintaxis/cobertura-sintactica.yaml')
assert 'alternativa integrada en ThingDecl como nombre intrínseco o campo' not in cov
assert 'alternativa integrada en ThingDecl como campo' in cov

d72=r('notas/decisiones/ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas.md')
assert 'Roles, `given`, variables de iteración y vinculaciones locales son símbolos léxicos sin ancla.' not in d72
assert 'participantes `for`, `on` y `given` son símbolos léxicos con ancla pública subordinada' in d72

d78=r('notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial.md')
assert 'Roles, `given`, iteradores, vinculaciones locales y valores globales no nominales solo reciben identidad interna efímera.' not in d78
assert 'participantes `for`/`on`/`given`' in d78

d38=r('notas/decisiones/ADR-038-familias-cerradas-de-valores.md')
assert '`name: Text` intrínseco' not in d38
assert '`~identifier: Name`' in d38 and '`~name: Name`' in d38

d85=r('notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md')
assert 'objetivos asignables de metadato' not in d85
assert 'ancla estable de cada rama' not in d85
assert '`decision_branch_key` local de cada rama' in d85
assert 'D-087 prohíbe usar cualquier acceso `~` como destino runtime' in d85

readme=r('especificacion/README.md')
assert 'anclas estables de ramas decisionales' not in readme
assert 'El grafo registra anclas de rama' not in readme

cases=r('especificacion/sintaxis/casos/cst-ast.yaml')
for stale in ('update-branch-by-stable-anchor','remove-branch-by-stable-anchor','move-branch-preserves-anchor-and-changes-first-match-order'):
    assert stale not in cases, stale
assert 'legacy-anchor-interpolation-rejected' in cases
assert 'no-public-branch-anchor' in cases

d87=r('notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md')
for rel in ('ADR-015-especializacion-aciclica-y-estado-independiente','ADR-028-sistema-de-magnitudes-y-unidades','ADR-038-familias-cerradas-de-valores','ADR-061-resultados-fallidos-y-plantillas-text','ADR-063-firmas-given-y-vinculaciones-on-conjuntas','ADR-068-thing-universal-y-nombre-intrinseco','ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas'):
    assert rel in d87, rel

idx=r('notas/decisiones/README.md')
assert '| D-068 | vigente | 2026-08-02 | [[notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco|`Thing` universal, identificador y presentación reflectiva]] |' in idx
print('PHASE5_DEEP_INVARIANTS_OK')
