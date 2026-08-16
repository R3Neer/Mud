from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
p = root / 'especificacion/sintaxis/casos/cst-ast.yaml'
t = p.read_text(encoding='utf-8')
old_min='''- id: min-empty-is-empty
  category: quantifier-semantics
  source: "min x in empty: x"
  cst_root: ExpressionSyntax
  ast: QuantifierExpr(Min, source=empty)
  semantic_expectations:
  - result-cardinality-0-or-1
  - empty-source-produces-empty
  produces_ast: true
'''
new_min='''- id: min-empty-is-empty
  category: quantifier-semantics
  source: "thing Sample {\\n    values: Nat [*] = empty\\n    minimum := min x in values: x\\n}\\n"
  cst_root: MudFileSyntax
  ast: CalculatedFieldDecl(minimum, value=QuantifierExpr(Min, source=values, body=ExpressionBlock([], x)))
  semantic_expectations:
  - result-type-Nat
  - result-cardinality-0-or-1
  - empty-source-produces-empty
  produces_ast: true
'''
old_max='''- id: max-empty-is-empty
  category: quantifier-semantics
  source: "max x in empty: x"
  cst_root: ExpressionSyntax
  ast: QuantifierExpr(Max, source=empty)
  semantic_expectations:
  - result-cardinality-0-or-1
  - empty-source-produces-empty
  produces_ast: true
'''
new_max='''- id: max-empty-is-empty
  category: quantifier-semantics
  source: "thing Sample {\\n    values: Nat [*] = empty\\n    maximum := max x in values: x\\n}\\n"
  cst_root: MudFileSyntax
  ast: CalculatedFieldDecl(maximum, value=QuantifierExpr(Max, source=values, body=ExpressionBlock([], x)))
  semantic_expectations:
  - result-type-Nat
  - result-cardinality-0-or-1
  - empty-source-produces-empty
  produces_ast: true
'''
for old,new in ((old_min,new_min),(old_max,new_max)):
    if t.count(old)!=1:
        raise SystemExit('expected exactly one extrema case to replace')
    t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8',newline='\n')
print('EXTREMA_CASES_FIXED')
