from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve()

def r(path):
    return (ROOT / path).read_text(encoding='utf-8')

def need(path, text):
    if text not in r(path):
        raise SystemExit(f'MISSING {text!r} in {path}')

def forbid(path, text):
    if text in r(path):
        raise SystemExit(f'STALE {text!r} in {path}')

forbid('especificacion/sintaxis/mud-resolved-ast.asdl', 'duplicate_index')
need('especificacion/sintaxis/mud-resolved-ast.asdl', 'SelectorBranchKey(string canonical_selector)')
need('notas/decisiones/ADR-090-ramas-funcionales-sin-ancla-publica.md', 'no pueden existir dos ramas ordinarias con el mismo selector canónico')
forbid('notas/decisiones/ADR-090-ramas-funcionales-sin-ancla-publica.md', 'Dos selectores canónicamente iguales siguen siendo representables')
need('especificacion/09-nombres-y-anclas.md', 'compartirían la misma clave estructural local')
need('especificacion/sintaxis/casos/cst-ast.yaml', 'duplicate-decision-branch-key')
print('BRANCH_KEY_AUDIT_OK')
