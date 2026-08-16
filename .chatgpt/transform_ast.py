from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1]).resolve()


def path(rel):
    return ROOT / rel


def read(rel):
    return path(rel).read_text(encoding='utf-8')


def write(rel, text):
    p = path(rel)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.rstrip('\n') + '\n', encoding='utf-8', newline='\n')


def exact(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {n}')
    return text.replace(old, new, 1)


def add_decision_frontmatter(text, decision):
    if f'  - {decision}\n' in text:
        return text
    marker = 'decisions:\n'
    i = text.find(marker)
    if i < 0:
        raise SystemExit(f'missing decisions frontmatter for {decision}')
    j = i + len(marker)
    while text.startswith('  - ', j):
        j = text.find('\n', j) + 1
    return text[:j] + f'  - {decision}\n' + text[j:]


# -----------------------------------------------------------------------------
# D-093: un único AST normativo (superficial) y un IR semántico elaborado.
# -----------------------------------------------------------------------------
adr = '''---
id: D-093
title: "AST superficial único e IR semántico elaborado"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "pipeline, AST superficial, resolución nominal, tabla de símbolos, grafo nominal, tipado, elaboración, IR y validadores"
---

# ADR-093 — AST superficial único e IR semántico elaborado

- Modifica: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].
- Precisa: [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]], [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]], [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]].

## Contexto

El pipeline vigente ya separa CST, AST superficial, resolución nominal y tipado/elaboración, pero `mud-resolved-ast.asdl` mezclaba en un artefacto denominado «AST resuelto» referencias nominales con tipos efectivos, dominios elaborados, cardinalidades inferidas y pruebas de terminación. Esa mezcla hacía imposible interpretar el archivo como salida exclusiva de resolución de nombres y duplicaba innecesariamente el árbol abstracto de fuente.

## Decisión

MUD posee un único AST normativo: el **AST superficial** producido a partir del CST sin pérdidas. Conserva la forma abstracta escrita, procedencia y las distinciones sintácticas que necesitan diagnósticos y tooling, sin anticipar tipado ni elaboración.

La resolución nominal no construye un segundo AST normativo. Produce sobre el AST superficial:

- tabla de símbolos y bindings de referencias;
- anclas y propietarios resueltos;
- ámbitos léxicos;
- claves estructurales locales como `decision_branch_key`;
- un grafo nominal parcial de propiedad, especialización y dependencias cuyos extremos ya puedan identificarse.

El tipado y la elaboración consumen el AST superficial junto con esos resultados de resolución y producen el **IR semántico**. El IR contiene el significado elaborado necesario para análisis posteriores y ejecución, incluidos cuando proceda:

- tipos efectivos y narrowing;
- dominios y formas de colección;
- cardinalidades efectivas y su procedencia;
- modos y formas de aplicación de diccionarios;
- conversiones ya resueltas;
- dependencias semánticas;
- pruebas o evidencias de terminación.

El esquema mecánico del IR vive en `especificacion/ir/mud-semantic-ir.asdl`. No es una segunda fuente de verdad: conforme a D-051 se reconstruye a partir del programa, el AST superficial y las decisiones de versión.

## Pipeline

```text
texto fuente
→ scanner y clasificación contextual
→ CST sin pérdidas
→ AST superficial
→ resolución nominal: símbolos + bindings + grafo nominal parcial
→ tipado y elaboración
→ IR semántico
→ análisis posteriores / ejecución
```

Una implementación puede materializar internamente un HIR intermedio si le resulta útil, pero ese artefacto no es normativo ni puede introducir significado que no aparezca en el AST superficial, las reglas de resolución o la elaboración.

## Consecuencias

- Se retira `especificacion/sintaxis/mud-resolved-ast.asdl` como contrato normativo.
- Los contratos semánticos que allí vivían se trasladan al IR y dejan de llamarse «AST resuelto».
- `mud-surface-ast.asdl` continúa siendo el único esquema AST.
- D-078 describe exclusivamente resolución nominal, símbolos, anclas y grafo inicial; no promete tipos o dominios ya elaborados.
- Los validadores deben comprobar que el IR semántico sea ASDL autoconsistente y que el antiguo archivo no reaparezca.

## Verificación

1. El directorio de sintaxis contiene un único esquema AST: `mud-surface-ast.asdl`.
2. El flujo documental no sitúa un «AST resuelto» entre resolución y tipado.
3. El IR semántico conserva tipos, dominios, cardinalidades y terminación que antes estaban mezclados en el AST resuelto.
4. D-051 y D-078 describen la misma frontera de fases.
5. El validador rechaza tipos ASDL desconocidos en el esquema del IR y la reaparición del contrato retirado.
'''
write('notas/decisiones/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado.md', adr)

# Mover mecánicamente el antiguo esquema a IR y renombrar su vocabulario.
old_rel = 'especificacion/sintaxis/mud-resolved-ast.asdl'
old = read(old_rel)
if 'module MUDResolved' not in old or 'termination_evidence' not in old:
    raise SystemExit('unexpected old resolved AST shape')
semantic = old
semantic = semantic.replace('-- MUD 1.0 — Contrato del AST resuelto', '-- MUD 1.0 — Contrato del IR semántico elaborado', 1)
semantic = semantic.replace('-- Complementa mud-surface-ast.asdl. Conserva procedencia y forma semántica,\n-- pero sustituye referencias nominales por símbolos y anclas resueltas.', '-- Se reconstruye desde el AST superficial después de resolución nominal, tipado y elaboración.\n-- Conserva significado semántico, símbolos/anclas resueltos y procedencia de fuente.', 1)
semantic = semantic.replace('module MUDResolved', 'module MUDSemanticIR', 1)
semantic = re.sub(r'\bresolved_', 'semantic_', semantic)
semantic = re.sub(r'\bResolved', 'Semantic', semantic)
write('especificacion/ir/mud-semantic-ir.asdl', semantic)
path(old_rel).unlink()

ir_readme = '''# IR semántico de MUD

Este directorio contiene contratos mecánicos posteriores a resolución nominal, tipado y elaboración. No contiene CST ni AST de fuente.

## `mud-semantic-ir.asdl`

Es el esquema normativo del significado elaborado reconstruible de un programa. Puede contener tipos efectivos, dominios, cardinalidades, narrowing, dependencias y evidencias de terminación porque se produce después de esas fases.

El IR no es fuente independiente de verdad. Debe poder descartarse y reconstruirse desde los archivos `.mud`, el AST superficial y las decisiones/versiones aplicables.

El AST normativo de fuente continúa siendo `especificacion/sintaxis/mud-surface-ast.asdl`.
'''
write('especificacion/ir/README.md', ir_readme)

# README de sintaxis.
p = 'especificacion/sintaxis/README.md'
t = read(p)
t = exact(t,
'| `mud-resolved-ast.asdl` | Normativo mecánico | Contrato del AST resuelto, tipos unión, símbolos, anclas y dependencias. |\n',
'', 'syntax README resolved row')
t = exact(t,
'''→ AST superficial normalizado\n→ resolución\n→ AST resuelto\n→ tipado/elaboración\n→ IR''',
'''→ AST superficial normalizado\n→ resolución nominal: símbolos + bindings + grafo parcial\n→ tipado/elaboración\n→ IR semántico (`../ir/mud-semantic-ir.asdl`)''',
'syntax README pipeline')
t = exact(t,
'''Este directorio no define:\n\n- Resolución de nombres y anclas.\n- Subtipado.\n- Inferencia de tipos.\n- Evaluación estática.\n- Semántica de efectos.\n- Ondas causales.\n- Forma canónica del IR.''',
'''Este directorio no define:\n\n- Resolución de nombres y anclas.\n- Subtipado.\n- Inferencia de tipos.\n- Evaluación estática.\n- Semántica de efectos.\n- Ondas causales.\n- Forma canónica del IR, cuyo esquema mecánico vive en `../ir/`.''',
'syntax README limits')
write(p, t)

# Capítulo de nombres.
p = 'especificacion/09-nombres-y-anclas.md'
t = add_decision_frontmatter(read(p), 'D-093')
t = exact(t,
'''Ninguno de estos ámbitos permite referencias adelantadas, ciclos, redeclaración o sombreado de un nombre ya visible. El AST resuelto usa la variante genérica `LocalSymbol(owner, kind, name, ordinal)`; D-088 no introduce una clase de símbolo ni una categoría de ancla nuevas.''',
'''Ninguno de estos ámbitos permite referencias adelantadas, ciclos, redeclaración o sombreado de un nombre ya visible. La resolución nominal registra estas vinculaciones como símbolos locales subordinados a su propietario; el IR semántico usa la variante genérica `LocalSymbol(owner, kind, name, ordinal)`. D-088 no introduce una clase de símbolo ni una categoría de ancla nuevas.''',
'09 local symbols')
t = exact(t,
'''El esquema mecánico [[mud-resolved-ast]] representa esta frontera: una declaración persistente y todo participante declarado usan `AnchoredSymbol`; los locales e iteradores ordinarios usan `LocalSymbol` subordinado a su propietario. Las ramas funcionales no son símbolos: sus dependencias se reconstruyen mediante el ancla del diccionario propietario y una `decision_branch_key` local.''',
'''Esta frontera no introduce un segundo AST normativo. La resolución nominal produce tabla de símbolos, bindings y el grafo parcial sobre el AST superficial. En el IR semántico una declaración persistente y todo participante declarado usan `AnchoredSymbol`; los locales e iteradores ordinarios usan `LocalSymbol` subordinado a su propietario. Las ramas funcionales no son símbolos: sus dependencias se reconstruyen mediante el ancla del diccionario propietario y una `decision_branch_key` local.''',
'09 resolved schema')
t = t.replace('El AST resuelto conserva para cada rama una `decision_branch_key`', 'El IR semántico conserva para cada rama una `decision_branch_key`')
write(p, t)

# D-078 queda literalmente vigente y limitado a resolución nominal.
p = 'notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial.md'
t = read(p)
t = exact(t,
'- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]',
'- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]] y [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]]',
'D078 modifier')
t = exact(t,
'''Poseen ancla las declaraciones globales, campos en su propietario original, componentes, miembros de family, unidades declaradas y tipos incorporados. Un campo heredado conserva el ancla declarativa del antecesor aunque su estado sea independiente en cada `thing`. Roles, `given`, iteradores, vinculaciones locales y valores globales no nominales solo reciben identidad interna efímera.''',
'''Poseen ancla las declaraciones globales, campos en su propietario original, componentes, datos asociados declarados por una `family`, miembros de `family`, unidades declaradas, participantes `for`/`on`/`given` y tipos incorporados. Un campo heredado conserva el ancla declarativa del antecesor aunque su estado sea independiente en cada `thing`. Iteradores, vinculaciones locales ordinarias y valores globales no nominales solo reciben identidad interna efímera.''',
'D078 anchors')
t = exact(t,
'''La resolución se ejecuta por etapas: primero símbolos nominales, después tipos y dominios, y finalmente miembros dependientes del tipo. La norma usa entornos y conjuntos de candidatos; un scope graph es una implementación posible, no autoridad.''',
'''La resolución nominal crea símbolos, anclas y bindings de referencias cuya categoría ya puede determinarse. Los nombres de tipos se vinculan nominalmente a sus símbolos, pero la comprobación de compatibilidad, uniones, dominios, cardinalidades y miembros dependientes del tipo pertenece al tipado y la elaboración. La norma usa entornos y conjuntos de candidatos; un scope graph es una implementación posible, no autoridad. D-093 retira la idea de materializar un segundo AST normativo como salida de esta fase.''',
'D078 stages')
t = exact(t,
'''6. Símbolos locales sin ancla pública.\n7. Grafo nominal construible antes del tipado completo.''',
'''6. Participantes declarados con ancla pública y símbolos locales ordinarios sin ella.\n7. Grafo nominal construible antes del tipado completo sin requerir un segundo AST.''',
'D078 verification')
write(p, t)

# D-051: AST escrito, IR significado elaborado.
p = 'notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles.md'
t = read(p)
insert = '- Modificada por: [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]]\n'
if insert not in t:
    marker = '- Ampliada por: [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]]\n'
    t = exact(t, marker, marker + insert, 'D051 modifier')
t = exact(t,
'''El AST conserva forma escrita y procedencia. El IR conserva significado resuelto y debe:''',
'''El AST normativo es el AST superficial y conserva forma escrita y procedencia. La resolución nominal produce símbolos, bindings y un grafo parcial sin crear otro AST normativo. Tras tipado y elaboración, el IR semántico conserva el significado resuelto y debe:''',
'D051 AST IR boundary')
write(p, t)

# Referencias en decisiones directamente afectadas.
p = 'notas/decisiones/ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios.md'
t = read(p).replace('gramática; CST; AST superficial y resuelto; casos de conformidad.', 'gramática; CST; AST superficial; IR semántico; casos de conformidad.')
write(p, t)

p = 'notas/decisiones/ADR-090-ramas-funcionales-sin-ancla-publica.md'
t = read(p)
t = t.replace('AST resuelto', 'IR semántico')
t = t.replace('`mud-resolved-ast.asdl`', '`especificacion/ir/mud-semantic-ir.asdl`')
write(p, t)

p = 'notas/decisiones/ADR-091-datos-de-family-como-descriptores-anclados.md'
t = read(p).replace('AST superficial, AST resuelto, reflexión y tooling', 'AST superficial, IR semántico, reflexión y tooling')
write(p, t)

p = 'notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md'
t = read(p)
t = t.replace('La AST superficial conserva que la cardinalidad fue omitida; la elaboración resuelta registra la cardinalidad efectiva y su procedencia', 'El AST superficial conserva que la cardinalidad fue omitida; el IR semántico elaborado registra la cardinalidad efectiva y su procedencia')
write(p, t)

# Validador: el IR semántico sustituye al antiguo contrato resuelto.
p = 'especificacion/sintaxis/validate_syntax_model.py'
t = read(p)
t = exact(t,
'''    asdl_path = root / "especificacion/sintaxis/mud-surface-ast.asdl"''',
'''    asdl_path = root / "especificacion/sintaxis/mud-surface-ast.asdl"\n    semantic_ir_path = root / "especificacion/ir/mud-semantic-ir.asdl"\n    retired_resolved_ast_path = root / "especificacion/sintaxis/mud-resolved-ast.asdl"''',
'validator paths')
t = exact(t,
'''    asdl_defined, asdl_used = asdl_types_and_uses(asdl_path)''',
'''    asdl_defined, asdl_used = asdl_types_and_uses(asdl_path)\n    if retired_resolved_ast_path.exists():\n        problems.append(Problem(str(retired_resolved_ast_path), "contrato retirado: solo existe AST superficial; use IR semántico"))\n    if not semantic_ir_path.exists():\n        problems.append(Problem(str(semantic_ir_path), "falta el contrato del IR semántico"))\n        semantic_ir_defined, semantic_ir_used = set(), set()\n    else:\n        semantic_ir_defined, semantic_ir_used = asdl_types_and_uses(semantic_ir_path)''',
'validator semantic types')
t = exact(t,
'''    for unknown in sorted(asdl_used - asdl_defined - {"int", "string", "identifier"}):\n        problems.append(Problem(str(asdl_path), f"tipo ASDL no definido: {unknown}"))''',
'''    for unknown in sorted(asdl_used - asdl_defined - {"int", "string", "identifier"}):\n        problems.append(Problem(str(asdl_path), f"tipo ASDL no definido: {unknown}"))\n    for unknown in sorted(semantic_ir_used - semantic_ir_defined - {"int", "string", "identifier"}):\n        problems.append(Problem(str(semantic_ir_path), f"tipo ASDL no definido: {unknown}"))\n    if semantic_ir_path.exists() and "module MUDSemanticIR" not in semantic_ir_path.read_text(encoding="utf-8"):\n        problems.append(Problem(str(semantic_ir_path), "falta module MUDSemanticIR"))''',
'validator semantic unknowns')
t = t.replace('root / "especificacion/sintaxis/mud-resolved-ast.asdl": [', 'root / "especificacion/ir/mud-semantic-ir.asdl": [')
write(p, t)

print('AST_IR_TRANSFORM_OK')
