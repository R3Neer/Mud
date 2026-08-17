from pathlib import Path
import os

ROOT=Path(os.environ['MUD_TARGET']).resolve()

def rd(r): return (ROOT/r).read_text(encoding='utf-8')
def wr(r,t): (ROOT/r).write_text(t.rstrip('\n')+'\n',encoding='utf-8',newline='\n')
def one(t,a,b,label):
    n=t.count(a)
    if n!=1: raise SystemExit(f'{label}: expected 1, found {n}')
    return t.replace(a,b,1)

# 08
r='especificacion/08-sintaxis-abstracta.md'; t=rd(r)
if '  - D-093\n' not in t:
    t=one(t,'  - D-092\n---','  - D-092\n  - D-093\n---','08 D093')
t=one(t,'La resolución nominal opera sobre este AST sin fabricar un segundo árbol normativo: produce símbolos, bindings, anclas y un grafo nominal parcial. Tras tipado y elaboración, el contrato semántico vive en `ir/mud-semantic-ir.asdl`, donde aparecen tipos efectivos, dominios, cardinalidades, dependencias y otras formas elaboradas.','La resolución nominal opera sobre este AST y produce el HIR normativo `ir/mud-nominal-hir.asdl`, que materializa símbolos, scopes, bindings, anclas y un grafo nominal parcial sin duplicar la sintaxis de fuente. Tras tipado y elaboración, el contrato semántico vive en `ir/mud-semantic-ir.asdl`, donde aparecen tipos efectivos, dominios, cardinalidades, dependencias y otras formas elaboradas.','08 boundary')
t=one(t,'→ AST superficial normalizado\n→ resolución nominal: símbolos + bindings + grafo parcial\n→ tipado y elaboración\n→ IR semántico','→ AST superficial normalizado\n→ resolución nominal\n→ HIR nominal: símbolos + scopes + bindings + anclas + grafo parcial\n→ tipado y elaboración\n→ IR semántico tipado/elaborado','08 pipeline')
marker='> [!rule] MUD-AST-002 — Normalización'
block='''> [!rule] MUD-AST-003 — Frontera del HIR nominal
> El HIR nominal puede añadir identidad y resolución, pero no significado de tipos: contiene símbolos, scopes, bindings, anclas y aristas nominales. Tipos efectivos, dominios efectivos, cardinalidades, conversiones elaboradas y evidencia de terminación están prohibidos hasta el IR semántico.

'''
if 'MUD-AST-003 — Frontera del HIR nominal' not in t:
    i=t.find(marker)
    if i<0: raise SystemExit('08 MUD-AST-002 missing')
    t=t[:i]+block+t[i:]
wr(r,t)

# 09
r='especificacion/09-nombres-y-anclas.md'; t=rd(r)
t=one(t,'## Etapas\n\n1. El AST superficial aporta nombres y procedencia.\n2. La resolución nominal crea símbolos y resuelve declaraciones cuya categoría ya es conocida.\n3. El sistema de tipos resuelve uniones, dominios y referencias dependientes del tipo.\n4. La resolución de miembros completa accesos, llamadas y abreviaturas contextuales.','''## Etapas

1. El AST superficial aporta nombres y procedencia.
2. La resolución nominal crea símbolos, scopes, bindings y anclas y los materializa en el HIR nominal de `ir/mud-nominal-hir.asdl`.
3. El sistema de tipos consume AST superficial + HIR nominal y resuelve uniones, dominios y referencias dependientes del tipo.
4. La elaboración completa accesos, llamadas, abreviaturas contextuales y demás significado dependiente de tipos en el IR semántico.

El HIR nominal no contiene tipos efectivos, dominios efectivos, cardinalidades ni pruebas de terminación. Es el contrato entre resolución de nombres y tipado, no una copia resuelta del AST superficial.''','09 stages')
wr(r,t)

# IR README
wr('especificacion/ir/README.md','''# Representaciones intermedias de MUD

Este directorio contiene contratos mecánicos derivados del AST superficial. No contiene CST ni una segunda sintaxis fuente.

## `mud-nominal-hir.asdl`

Es el contrato normativo producido por resolución de nombres. Contiene símbolos, scopes, bindings, anclas y aristas nominales parciales. No puede contener tipos efectivos, dominios efectivos, cardinalidades, conversiones elaboradas ni evidencia de terminación.

## `mud-semantic-ir.asdl`

Es el esquema normativo posterior a tipado y elaboración. Puede contener tipos efectivos, dominios, cardinalidades, narrowing, dependencias y evidencias de terminación porque se produce después de esas fases.

Ninguna representación intermedia es fuente independiente de verdad. Ambas deben poder descartarse y reconstruirse desde los archivos `.mud`, el AST superficial y las decisiones/versiones aplicables.

El único AST normativo de fuente continúa siendo `especificacion/sintaxis/mud-surface-ast.asdl`.
''')

# Validator
r='especificacion/sintaxis/validate_syntax_model.py'; t=rd(r)
t=one(t,'    semantic_ir_path = root / "especificacion/ir/mud-semantic-ir.asdl"\n    retired_resolved_ast_path = root / "especificacion/sintaxis/mud-resolved-ast.asdl"','    nominal_hir_path = root / "especificacion/ir/mud-nominal-hir.asdl"\n    semantic_ir_path = root / "especificacion/ir/mud-semantic-ir.asdl"\n    retired_resolved_ast_path = root / "especificacion/sintaxis/mud-resolved-ast.asdl"','validator paths')
t=one(t,'    if retired_resolved_ast_path.exists():\n        problems.append(Problem(str(retired_resolved_ast_path), "contrato retirado: solo existe AST superficial; use IR semántico"))\n    if not semantic_ir_path.exists():','''    if retired_resolved_ast_path.exists():
        problems.append(Problem(str(retired_resolved_ast_path), "contrato retirado: use HIR nominal + IR semántico"))
    if not nominal_hir_path.exists():
        problems.append(Problem(str(nominal_hir_path), "falta el contrato del HIR nominal"))
        nominal_hir_defined, nominal_hir_used = set(), set()
    else:
        nominal_hir_defined, nominal_hir_used = asdl_types_and_uses(nominal_hir_path)
    if not semantic_ir_path.exists():''','validator load')
t=one(t,'    for unknown in sorted(semantic_ir_used - semantic_ir_defined - {"int", "string", "identifier"}):\n        problems.append(Problem(str(semantic_ir_path), f"tipo ASDL no definido: {unknown}"))\n    if semantic_ir_path.exists() and "module MUDSemanticIR" not in semantic_ir_path.read_text(encoding="utf-8"):\n        problems.append(Problem(str(semantic_ir_path), "falta module MUDSemanticIR"))','''    for unknown in sorted(nominal_hir_used - nominal_hir_defined - {"int", "string", "identifier"}):
        problems.append(Problem(str(nominal_hir_path), f"tipo ASDL no definido: {unknown}"))
    if nominal_hir_path.exists():
        hir_text = nominal_hir_path.read_text(encoding="utf-8")
        if "module MUDNominalHIR" not in hir_text:
            problems.append(Problem(str(nominal_hir_path), "falta module MUDNominalHIR"))
        for fragment in ["semantic_type", "effective_domain", "collection_shape", "effective_cardinality", "termination_evidence", "ConversionExpr"]:
            if fragment in hir_text:
                problems.append(Problem(str(nominal_hir_path), f"el HIR nominal contiene elaboración prohibida: {fragment}"))
    for unknown in sorted(semantic_ir_used - semantic_ir_defined - {"int", "string", "identifier"}):
        problems.append(Problem(str(semantic_ir_path), f"tipo ASDL no definido: {unknown}"))
    if semantic_ir_path.exists() and "module MUDSemanticIR" not in semantic_ir_path.read_text(encoding="utf-8"):
        problems.append(Problem(str(semantic_ir_path), "falta module MUDSemanticIR"))''','validator checks')
wr(r,t)
print('STAGE2_FINISH_OK')
