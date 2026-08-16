from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve()

def read(path):
    return (ROOT / path).read_text(encoding='utf-8')

def write(path, text):
    (ROOT / path).write_text(text.rstrip('\n') + '\n', encoding='utf-8', newline='\n')

def exact(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {n}')
    return text.replace(old, new, 1)

# D-090: la clave local es exclusivamente el selector canónico.
p = 'notas/decisiones/ADR-090-ramas-funcionales-sin-ancla-publica.md'
t = read(p)
t = exact(t,
'''SelectorBranchKey(canonical_selector, duplicate_index)\nFallbackBranchKey''',
'''SelectorBranchKey(canonical_selector)\nFallbackBranchKey''',
'D090 key shape')
t = exact(t,
'''`canonical_selector` es la forma canónica del selector después de resolución y normalización semántica suficiente para reconstruir la rama. Si varias ramas tienen el mismo selector canónico, `duplicate_index` las distingue solo dentro de la representación resuelta actual. Ese índice no es una ancla, no participa en resolución nominal y no promete estabilidad entre ediciones. El fallback `_` usa una variante propia y única por diccionario.''',
'''`canonical_selector` es la forma canónica del selector después de resolución y normalización semántica suficiente para reconstruir la rama. Dentro de un mismo diccionario no pueden existir dos ramas ordinarias con el mismo selector canónico: la parte izquierda actúa como clave estructural local. El fallback `_` usa una variante propia y única por diccionario.''',
'D090 canonical key semantics')
t = exact(t,
'''- Dos selectores canónicamente iguales siguen siendo representables; el índice de colisión evita introducir una prohibición nueva.''',
'''- Dos selectores canónicamente iguales dentro del mismo diccionario son inválidos porque representarían la misma clave estructural local.''',
'D090 duplicate consequence')
t = exact(t,
'''### Prohibir selectores duplicados para obtener una clave única\n\nDescartada en esta decisión porque convertiría una necesidad de representación en una restricción semántica nueva.''',
'''### Permitir selectores canónicamente duplicados mediante un índice local\n\nDescartada porque la rama ya posee una clave estructural natural: su selector canónico. Introducir un índice permitiría dos entradas con la misma clave y haría depender las operaciones editoriales de una distinción que no existe en el modelo del diccionario.''',
'D090 rejected alternative')
t = exact(t,
'''3. `DecisionDependsOn` conserva el ancla del diccionario y una clave local de rama.''',
'''3. `DecisionDependsOn` conserva el ancla del diccionario y una clave local de rama sin índice de colisión.''',
'D090 verification')
write(p, t)

# D-085 debe quedar literalmente vigente según la política actual.
p = 'notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md'
t = read(p)
t = exact(t,
'''Las ramas son estáticas durante la ejecución ordinaria y no admiten efectos, llamadas a acciones, asignaciones, `create`, `destroy` ni mutación. La edición del modelo puede crear, actualizar, retirar o mover ramas dentro del diccionario propietario, pero una rama no posee ancla pública ni descriptor metadata-bearing propio. El modelo resuelto usa una clave local de rama: el selector normalizado es su discriminante principal y las colisiones entre selectores iguales se distinguen mediante un índice local sin garantía de persistencia; `_` usa una clave de fallback propia. Una rama nueva se inserta antes de `_` de forma predeterminada; en un decisional ordenado puede declararse una posición concreta.''',
'''Las ramas son estáticas durante la ejecución ordinaria y no admiten efectos, llamadas a acciones, asignaciones, `create`, `destroy` ni mutación. La edición del modelo puede crear, actualizar, retirar o mover ramas dentro del diccionario propietario, pero una rama no posee ancla pública ni descriptor metadata-bearing propio. El modelo resuelto usa una clave local de rama: el selector normalizado es la clave de una rama ordinaria y no puede repetirse dentro del mismo diccionario; `_` usa una clave de fallback propia y única. Cambiar solo el resultado conserva la clave; cambiar el selector retira estructuralmente la clave anterior y crea la nueva. Una rama nueva se inserta antes de `_` de forma predeterminada; en un decisional ordenado puede declararse una posición concreta.''',
'D085 branch key')
write(p, t)

# Norma de nombres/anclas.
p = 'especificacion/09-nombres-y-anclas.md'
t = read(p)
t = exact(t,
'''El AST resuelto conserva para cada rama una `decision_branch_key` local al diccionario. Para una rama ordinaria, la clave contiene la forma canónica del selector resuelto y un índice de colisión entre ramas con el mismo selector canónico. El índice solo garantiza unicidad dentro de esa representación resuelta y no constituye identidad persistente. `_` usa una clave `FallbackBranchKey` distinta. El ordinal fuente se conserva por separado porque participa en `FirstMatch`, pero tampoco se convierte en ancla.''',
'''El AST resuelto conserva para cada rama una `decision_branch_key` local al diccionario. Para una rama ordinaria, la clave es la forma canónica del selector resuelto. Dos ramas ordinarias con la misma forma canónica dentro del mismo diccionario son inválidas: compartirían la misma clave estructural local. `_` usa una clave `FallbackBranchKey` distinta y única. El ordinal fuente se conserva por separado porque participa en `FirstMatch`, pero tampoco se convierte en ancla.''',
'09 branch key')
write(p, t)

# AST resuelto.
p = 'especificacion/sintaxis/mud-resolved-ast.asdl'
t = read(p)
t = exact(t,
'''    decision_branch_key = SelectorBranchKey(string canonical_selector, int duplicate_index)\n                        | FallbackBranchKey''',
'''    decision_branch_key = SelectorBranchKey(string canonical_selector)\n                        | FallbackBranchKey''',
'resolved AST branch key')
write(p, t)

# Caso de conformidad: el AST puede construirse superficialmente, pero resolución rechaza clave duplicada.
p = 'especificacion/sintaxis/casos/cst-ast.yaml'
t = read(p)
marker = '- id: duplicate-decision-branch-canonical-selector\n'
if marker not in t:
    t = t.rstrip() + '''\n- id: duplicate-decision-branch-canonical-selector\n  category: resolution-after-ast\n  source: "thing PolicyHolder {\\n    policy: Nat --> Text = value < 10 --> \\\"low\\\", value < 10 --> \\\"alsoLow\\\"\\n}\\n"\n  cst_root: MudFileSyntax\n  expected_diagnostics:\n  - duplicate-decision-branch-key\n  produces_ast: true\n''' 
write(p, t)

print('BRANCH_KEY_TRANSFORM_OK')
