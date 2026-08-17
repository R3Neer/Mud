from __future__ import annotations

from pathlib import Path
import os
import re
import yaml

ROOT = Path(os.environ['MUD_TARGET']).resolve()


def text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding='utf-8')


def require(rel: str, *needles: str) -> None:
    s = text(rel)
    for needle in needles:
        if needle not in s:
            raise SystemExit(f'{rel}: missing {needle!r}')


def forbid(rel: str, *needles: str) -> None:
    s = text(rel)
    for needle in needles:
        if needle in s:
            raise SystemExit(f'{rel}: stale/forbidden {needle!r}')


def frontmatter(rel: str) -> dict:
    s = text(rel)
    if not s.startswith('---\n'):
        raise SystemExit(f'{rel}: missing frontmatter')
    end = s.find('\n---\n', 4)
    if end < 0:
        raise SystemExit(f'{rel}: malformed frontmatter')
    return yaml.safe_load(s[4:end]) or {}


def case_ids() -> set[str]:
    data = yaml.safe_load(text('especificacion/sintaxis/casos/cst-ast.yaml')) or {}
    return {c.get('id') for c in data.get('cases', []) if c.get('id')}


# 1. Unit source forms: configurable display forms, spaces, alphabetic content,
# keyword exclusion, and uniqueness after allowed-prefix closure.
require(
    'especificacion/06-lexico.md',
    'MUD-LEX-016',
    'MUD-LEX-017',
    '`~name`, `~plural` y `~abbreviation`',
    'palabra clave de MUD',
)
require(
    'notas/decisiones/ADR-089-clasificacion-contextual-de-formas-fuente.md',
    'al menos un carácter alfabético',
    'todas las combinaciones con prefijos permitidos',
)
ids = case_ids()
required_unit_cases = {
    'unit-form-multispace-name',
    'unit-form-all-digits-rejected',
    'unit-form-all-symbols-rejected',
    'unit-form-keyword-rejected',
    'unit-form-prefixed-collision-rejected',
}
missing = required_unit_cases - ids
if missing:
    raise SystemExit(f'item 1: missing unit cases {sorted(missing)}')

# 2. Functional decision branches have local structural identity, not public anchors.
require(
    'notas/decisiones/ADR-090-ramas-funcionales-sin-ancla-publica.md',
    'no es una declaración pública',
    'decision_branch_key',
    'no materializa un `BranchSymbol`',
    'no expone una ancla pública',
)
require(
    'especificacion/README.md',
    'no reciben ancla pública conforme a D-090',
)

# 3. Surface AST -> nominal HIR -> typed/elaborated semantic IR.
hir_path = ROOT / 'especificacion/ir/mud-nominal-hir.asdl'
if not hir_path.exists():
    raise SystemExit('item 3: missing mud-nominal-hir.asdl')
hir = hir_path.read_text(encoding='utf-8')
for needle in [
    'module MUDNominalHIR',
    'NominalHIR(',
    'NominalSymbol(',
    'NominalScope(',
    'ResolvedReference(',
    'Owns(',
    'Specializes(',
    'RefersTo(',
]:
    if needle not in hir:
        raise SystemExit(f'item 3: HIR missing {needle!r}')
for forbidden in [
    'semantic_type',
    'effective_domain',
    'collection_shape',
    'effective_cardinality',
    'termination_evidence',
    'ConversionExpr',
]:
    if forbidden in hir:
        raise SystemExit(f'item 3: nominal HIR leaks elaboration via {forbidden!r}')
if (ROOT / 'especificacion/sintaxis/mud-resolved-ast.asdl').exists():
    raise SystemExit('item 3: retired mud-resolved-ast.asdl reappeared')
require(
    'notas/decisiones/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado.md',
    'mud-nominal-hir.asdl',
    'HIR nominal',
    'no puede contener',
)
require(
    'especificacion/08-sintaxis-abstracta.md',
    'HIR nominal',
    'IR semántico',
)

# 4. Vigente ADR sweep: assert the corrected contracts and reject the exact old
# active statements that were found by the independent sweep. Historical/negative
# mentions remain allowed where they document a withdrawal.
require('notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension.md', 'things {', 'rules {')
require('notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades.md', '~name =', '~plural =', '~abbreviation =')
forbid('notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades.md', '\n        abbreviation =', '\n        prefixes =')
require('notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos.md', '~format =')
forbid('notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos.md', '\n    format =')
require('notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas.md', 'D-087 retira `anchor{...}`', 'expression~anchor')
forbid('notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas.md', 'D-061 añade `anchor{...}` como forma contextual exclusiva')
require('notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md', 'debe declarar un identificador fuente explícito')
forbid('notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md', 'El nombre de un participante `on`, o de un participante `for` cuya cardinalidad efectiva sea exactamente `[1]`, puede omitirse.')
require('notas/decisiones/ADR-037-campos-y-dominios-declarativos.md', 'campo ordinario llamado `name`')
forbid('notas/decisiones/ADR-037-campos-y-dominios-declarativos.md', 'omitir cardinalidad equivale a `[1]`')
require('notas/decisiones/ADR-038-familias-miembros-y-datos-asociados.md', '~name: Name', '~name =')
require('notas/decisiones/ADR-039-colecciones-y-diccionarios.md', '`unique`, cuando se escribe, se aplica a los **valores asociados**', 'Leer una clave ausente produce `empty`')
require('notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md', 'No existe la forma plana o mezclada')
require('notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md', 'things { Counter }', 'test-start-with\n    ::= start-with-declaration')
require('notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text.md', 'No existe una interpolación especial `anchor{...}`', '~format =', 'expression~anchor')
forbid('notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text.md', '- `anchor{d}` inserta')
require('notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md', 'Todo rol `for` tiene identificador fuente explícito')
forbid('notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md', 'puede ser anónimo')
require('notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md', '### Metadato estándar `~name`', 'Thing~anchor')
forbid('notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md', 'anchor{Thing} produce')
require('notas/decisiones/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas.md', '`~anchor`, `~path` y `~file`')

# 5. Family data declarations are anchored descriptors; per-member values are payload.
require(
    'notas/decisiones/ADR-091-datos-de-family-como-descriptores-anclados.md',
    'declaración de descriptor',
    'family::game.Status::score',
    'no introduce otra declaración ni otra ancla',
)
require(
    'notas/decisiones/ADR-038-familias-miembros-y-datos-asociados.md',
    'no introduce una declaración independiente',
)

# 6. Metadata descriptors expose path/file but remain terminal.
require(
    'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md',
    '~anchor',
    '~path',
    '~file',
)
require(
    'notas/decisiones/ADR-094-anclas-terminales-de-metadatos-configurados.md',
    '`~path: MudPath`',
    '`~file: MudFile`',
    'descriptor terminal',
)
required_metadata_cases = {'metadata-descriptor-path-file', 'metadata-descriptor-remains-terminal'}
missing = required_metadata_cases - ids
if missing:
    raise SystemExit(f'item 6: missing metadata cases {sorted(missing)}')

# 7. Contextual nominal alias construction is explicit in the modern phase contract.
require('notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal.md', 'ContextualAliasConstructionExpr')
require('especificacion/08-sintaxis-abstracta.md', '### Construcción contextual de aliases', 'ContextualAliasConstructionExpr(literal, target_alias)', 'ConversionExpr')
require('especificacion/ir/mud-semantic-ir.asdl', 'ContextualAliasConstructionExpr(', 'ConversionExpr(')
required_alias_cases = {
    'contextual-basic-alias-literal',
    'contextual-alias-comparison-literal',
    'typed-representation-does-not-implicitly-become-alias',
    'explicit-representation-to-alias',
}
missing = required_alias_cases - ids
if missing:
    raise SystemExit(f'item 7: missing alias cases {sorted(missing)}')
require('especificacion/sintaxis/validate_syntax_model.py', 'ContextualAliasConstructionExpr(', *sorted(required_alias_cases))

# 8. Given uses the full TypeExpr and therefore supports collection/dictionary shapes.
surface = text('especificacion/sintaxis/mud-surface-ast.asdl')
if not re.search(r'given_decl\s*=\s*GivenDecl\(identifier name,\s*\n\s*type_expr type,', surface):
    raise SystemExit('item 8: GivenDecl does not carry type_expr')
for needle in ['dictionary_shape = DictionaryShape(', 'collection_spec', 'type_expr']:
    if needle not in surface:
        raise SystemExit(f'item 8: surface AST missing {needle!r}')
require('especificacion/gramatica/mud.ebnf', 'given-parameter', 'type-expression')

# 9. Empty extrema are ordinary absence with conservative [0..1] result.
d95 = frontmatter('notas/decisiones/ADR-095-extremos-vacios-como-ausencia-ordinaria.md')
if d95.get('status') != 'vigente':
    raise SystemExit('item 9: D-095 is not vigente')
require(
    'notas/decisiones/ADR-095-extremos-vacios-como-ausencia-ordinaria.md',
    'producen `empty`',
    'min : T [0..1]',
    'max : T [0..1]',
    'no introduce por sí misma `failed`',
)

# 10. TypeKind intentionally remains open; do not freeze an invented catalog.
q60 = frontmatter('notas/preguntas/Q-060-catalogo-reflectivo-de-typekind.md')
if q60.get('resolved') is not False or q60.get('closed') not in (None, ''):
    raise SystemExit('item 10: Q-060 was accidentally closed')
require(
    'notas/preguntas/Q-060-catalogo-reflectivo-de-typekind.md',
    'catálogo normativo completo para MUD 1.0',
    '## Resolución\n\nPendiente.',
)
active_questions = text('notas/preguntas/README.md')
if 'Q-060 — Catálogo reflectivo de `TypeKind`' not in active_questions:
    raise SystemExit('item 10: Q-060 missing from active question index')

# 11. Question governance is explicit; Q-054/Q-055 are closed with criterion evidence.
require(
    'gobierno/POLITICA-DE-PREGUNTAS.md',
    'El campo `resolved` es la única fuente de verdad',
    'Una pregunta `resolved: true` contiene además `## Evidencia de cierre`',
    'un ADR enlazado por sí solo no constituye cierre',
)
for rel in [
    'notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos.md',
    'notas/preguntas/Q-055-literales-de-magnitudes-de-punto.md',
]:
    data = frontmatter(rel)
    if data.get('resolved') is not True or not data.get('closed'):
        raise SystemExit(f'item 11: {rel} is not properly closed')
    require(rel, '## Criterio de cierre', '## Evidencia de cierre', '- C1:')
    if data.get('id') in active_questions:
        raise SystemExit(f'item 11: closed {data.get("id")} remains active')

# 12. Authority/readability: normative surface and editorial maturity are orthogonal.
require(
    'gobierno/CICLO-DOCUMENTAL.md',
    '### Autoridad durante la preparación',
    '`normative: true`',
    '`status`',
    'no existe una precedencia silenciosa',
)
require(
    'especificacion/00-convenciones-editoriales.md',
    '`normative: true`',
    'estado editorial',
)
require(
    'especificacion/README.md',
    'Carácter normativo y estado editorial',
    'no reciben ancla pública conforme a D-090',
)
forbid('especificacion/README.md', 'anclas estables de ramas decisionales')

print('FINAL_CHECKLIST_AUDIT_OK items=12 head_expected=84142accf22f4c71d52954a6e56945e789621ea2')
