from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve()

def r(p): return (ROOT / p).read_text(encoding='utf-8')
def need(p, s):
    if s not in r(p): raise SystemExit(f'MISSING {s!r} in {p}')
def forbid(p, s):
    if (ROOT / p).exists() and s in r(p): raise SystemExit(f'STALE {s!r} in {p}')

if (ROOT / 'especificacion/sintaxis/mud-resolved-ast.asdl').exists():
    raise SystemExit('retired mud-resolved-ast.asdl still exists')
need('especificacion/ir/mud-semantic-ir.asdl', 'module MUDSemanticIR')
need('especificacion/ir/mud-semantic-ir.asdl', 'termination_evidence')
need('especificacion/ir/mud-semantic-ir.asdl', 'semantic_type')
need('especificacion/sintaxis/README.md', 'AST superficial normalizado')
forbid('especificacion/sintaxis/README.md', '→ AST resuelto')
need('notas/decisiones/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado.md', 'MUD posee un único AST normativo')
need('notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles.md', 'El AST normativo es el AST superficial')
need('notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial.md', 'D-093 retira la idea de materializar un segundo AST normativo')
forbid('notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial.md', 'Roles, `given`, iteradores, vinculaciones locales y valores globales no nominales solo reciben identidad interna efímera')
need('especificacion/09-nombres-y-anclas.md', 'Esta frontera no introduce un segundo AST normativo')
need('especificacion/sintaxis/validate_syntax_model.py', 'semantic_ir_path')
print('AST_IR_AUDIT_OK')
