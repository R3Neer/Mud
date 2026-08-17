from pathlib import Path
import re, subprocess, sys
ROOT = Path.cwd()

def text(path):
    return (ROOT / path).read_text(encoding='utf-8')

def require(path, *needles):
    data = text(path)
    for needle in needles:
        if needle not in data:
            raise SystemExit(f'{path}: missing {needle!r}')

def forbid(path, *needles):
    data = text(path)
    for needle in needles:
        if needle in data:
            raise SystemExit(f'{path}: forbidden residue {needle!r}')

# 1. Formas fuente de unidades.
require('especificacion/06-lexico.md', 'MUD-LEX-016', 'MUD-LEX-017')
require('notas/decisiones/ADR-089-clasificacion-contextual-de-formas-fuente.md', '~name', '~plural', '~abbreviation', 'palabra clave de MUD', 'combinaciones con prefijos permitidos')
cases = text('especificacion/sintaxis/casos/cst-ast.yaml')
for case_id in [
    'unit-form-multispace-name', 'unit-form-all-digits-rejected',
    'unit-form-all-symbols-rejected', 'unit-form-keyword-rejected',
    'unit-form-prefixed-collision-rejected',
]:
    if f'- id: {case_id}' not in cases:
        raise SystemExit(f'cst-ast.yaml: missing case {case_id}')

# 2. Frontera Surface AST -> HIR nominal -> IR semántico.
hir_path = ROOT / 'especificacion/ir/mud-nominal-hir.asdl'
if not hir_path.exists():
    raise SystemExit('missing mud-nominal-hir.asdl')
hir = hir_path.read_text(encoding='utf-8')
for needle in ['module MUDNominalHIR', 'NominalHIR(', 'NominalSymbol(', 'NominalScope(', 'ResolvedReference(', 'Owns(', 'Specializes(', 'RefersTo(']:
    if needle not in hir:
        raise SystemExit(f'HIR: missing {needle}')
for leak in ['semantic_type', 'effective_domain', 'collection_shape', 'effective_cardinality', 'termination_evidence', 'ConversionExpr']:
    if leak in hir:
        raise SystemExit(f'HIR leaks elaboration: {leak}')
if (ROOT / 'especificacion/sintaxis/mud-resolved-ast.asdl').exists():
    raise SystemExit('retired mud-resolved-ast.asdl reappeared')
require('notas/decisiones/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado.md', 'HIR nominal', 'mud-nominal-hir.asdl', 'IR semántico')

# 3. Metadata terminal y capacidades de procedencia.
require('notas/decisiones/ADR-094-anclas-terminales-de-metadatos-configurados.md', 'Metadata', '~anchor', '~path', '~file', 'terminal')
require('notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md', '~path', '~file')
for stale in ['Esta decisión no añade por simetría `~path` ni `~file`', 'no expone `~path` ni `~file`']:
    for path in ['notas/decisiones/ADR-094-anclas-terminales-de-metadatos-configurados.md', 'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md']:
        forbid(path, stale)

# 4. Construcción contextual de aliases.
require('notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal.md', 'PlayerName', 'construcción contextual', 'expresión ya tipada', 'ContextualAliasConstructionExpr')
for case_id in [
    'contextual-basic-alias-literal',
    'typed-representation-does-not-implicitly-become-alias',
    'explicit-representation-to-alias',
    'contextual-alias-comparison-literal',
]:
    if f'- id: {case_id}' not in cases:
        raise SystemExit(f'cst-ast.yaml: missing alias case {case_id}')

# 5. Autoridad documental.
require('especificacion/README.md', '**Capítulo vigente**: su texto normativo es autoridad consolidada', 'no equivale por sí solo a aprobación')
require('especificacion/00-convenciones-editoriales.md', 'Solo `status: vigente` concede autoridad consolidada al capítulo como unidad')
require('gobierno/CICLO-DOCUMENTAL.md', '### Autoridad durante la promoción', 'no es el mecanismo que hace vigentes retroactivamente las decisiones')

# 6. Residuos activos de contratos retirados en superficies normativas principales.
for path in ['especificacion/06-lexico.md', 'especificacion/07-gramatica-concreta.md', 'especificacion/08-sintaxis-abstracta.md', 'especificacion/09-nombres-y-anclas.md']:
    forbid(path, 'anchor{')
for path in ['especificacion/08-sintaxis-abstracta.md', 'especificacion/09-nombres-y-anclas.md']:
    forbid(path, 'AST resuelto')

print('FINAL_CHECKLIST_AUDIT_OK')
