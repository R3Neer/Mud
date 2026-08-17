from pathlib import Path
import os

ROOT=Path(os.environ['MUD_TARGET']).resolve()
def text(p): return (ROOT/p).read_text(encoding='utf-8')
hir=text('especificacion/ir/mud-nominal-hir.asdl')
for x in ['module MUDNominalHIR','NominalHIR(','NominalSymbol(','NominalScope(','ResolvedReference(','Owns(','Specializes(','RefersTo(']:
    if x not in hir: raise SystemExit(f'HIR missing {x}')
for x in ['semantic_type','effective_domain','collection_shape','effective_cardinality','termination_evidence','ConversionExpr']:
    if x in hir: raise SystemExit(f'HIR leaks elaboration: {x}')
if (ROOT/'especificacion/sintaxis/mud-resolved-ast.asdl').exists(): raise SystemExit('retired resolved AST reappeared')
d93=text('notas/decisiones/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado.md')
for x in ['HIR nominal','no puede contener','mud-nominal-hir.asdl','IR semántico']:
    if x not in d93: raise SystemExit(f'D093 missing {x}')
checks={
 'especificacion/08-sintaxis-abstracta.md':['HIR nominal','mud-nominal-hir.asdl'],
 'especificacion/09-nombres-y-anclas.md':['HIR nominal','mud-nominal-hir.asdl'],
 'especificacion/ir/README.md':['mud-nominal-hir.asdl','mud-semantic-ir.asdl'],
}
for p, required in checks.items():
    txt=text(p)
    for x in required:
        if x not in txt: raise SystemExit(f'{p} missing {x}')
print('STAGE2_AUDIT_OK')
