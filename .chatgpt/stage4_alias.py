from pathlib import Path
import os

ROOT=Path(os.environ['MUD_TARGET']).resolve()
def rd(r): return (ROOT/r).read_text(encoding='utf-8')
def wr(r,t): (ROOT/r).write_text(t.rstrip('\n')+'\n',encoding='utf-8',newline='\n')
def one(t,a,b,label):
    n=t.count(a)
    if n!=1: raise SystemExit(f'{label}: expected 1, found {n}')
    return t.replace(a,b,1)

# D-032: modern phase terminology.
r='notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal.md'; t=rd(r)
t=one(t,'- El AST tipado conserva el alias nominal incluso cuando su representación coincide con otro tipo.','- El IR semántico conserva explícitamente la construcción contextual y el alias nominal incluso cuando su representación coincide con otro tipo.','D032 consequence')
if 'ContextualAliasConstructionExpr' not in t:
    t=one(t,'- La elaboración debe distinguir literales sin tipo fijado de expresiones ya tipadas.','- La elaboración debe distinguir literales sin tipo fijado de expresiones ya tipadas.\n- El IR usa `ContextualAliasConstructionExpr` para la construcción dirigida por tipo esperado y reserva `ConversionExpr` para un `to` explícito.','D032 IR consequence')
wr(r,t)

# 08: make the elaboration boundary explicit.
r='especificacion/08-sintaxis-abstracta.md'; t=rd(r)
if '  - D-032\n' not in t:
    marker='decisions:\n'; i=t.find(marker); j=i+len(marker)
    t=t[:j]+'  - D-032\n'+t[j:]
needle='''Los literales estructurales siguen siendo contextuales. `PositionalStructuralLiteralExpr` exige al menos dos valores y `NamedStructuralLiteralExpr` conserva uno o más componentes nombrados; no se selecciona todavía un alias concreto. Por tanto, los miembros del alias solo quedan disponibles después de elaboración contextual o de una conversión nominal explícita.\n'''
extra=needle+'''\nLa misma regla se aplica a literales básicos. Si el contexto espera un alias nominal cuya representación admite el literal, la elaboración construye directamente ese alias sin introducir una conversión implícita general. Por ejemplo, con `alias PlayerName := Text`, `name: PlayerName = "Ada"` es válido. En cambio, una expresión que ya posee tipo `Text`, como una variable `rawName`, no cambia silenciosamente a `PlayerName`; requiere `rawName to PlayerName`.\n\nEl IR semántico distingue ambas operaciones: `ContextualAliasConstructionExpr(literal, target_alias)` representa construcción dirigida por el tipo esperado y `ConversionExpr(value, target_type)` representa `to` escrito explícitamente. El AST superficial no añade un nodo de alias contextual porque todavía conserva el literal y el contexto que lo espera.\n'''
t=one(t,needle,extra,'08 alias contextual')
wr(r,t)

# Semantic IR gets a distinct elaborated node.
r='especificacion/ir/mud-semantic-ir.asdl'; t=rd(r)
t=one(t,'                  | ConversionExpr(semantic_expr value, anchor target_type)\n','                  | ContextualAliasConstructionExpr(semantic_expr literal, anchor target_alias)\n                  | ConversionExpr(semantic_expr value, anchor target_type)\n','semantic IR contextual alias')
wr(r,t)

# Conformance cases.
r='especificacion/sintaxis/casos/cst-ast.yaml'; t=rd(r)
if 'id: contextual-basic-alias-literal' not in t:
    t += r'''
- id: contextual-basic-alias-literal
  category: validation-after-resolution
  source: "alias PlayerName := Text\nthing Person {\n    name: PlayerName = \"Ada\"\n}\n"
  cst_root: MudFileSyntax
  semantic_expectations:
  - elaborate-basic-literal-as-expected-nominal-alias
  - semantic-ir-uses-contextual-alias-construction
  produces_ast: true
- id: typed-representation-does-not-implicitly-become-alias
  category: validation-after-resolution
  source: "alias PlayerName := Text\nthing Person {\n    rawName: Text = \"Ada\"\n    name: PlayerName = rawName\n}\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - explicit-nominal-conversion-required
  produces_ast: true
- id: explicit-representation-to-alias
  category: validation-after-resolution
  source: "alias PlayerName := Text\nthing Person {\n    rawName: Text = \"Ada\"\n    name: PlayerName = rawName to PlayerName\n}\n"
  cst_root: MudFileSyntax
  semantic_expectations:
  - semantic-ir-uses-explicit-conversion
  produces_ast: true
'''
wr(r,t)
print('STAGE4_OK')
