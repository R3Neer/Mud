from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()


def read(rel):
    return (root / rel).read_text(encoding="utf-8")


def write(rel, text):
    (root / rel).write_text(text.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def exact(text, old, new, label, count=1):
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"{label}: expected {count}, found {actual}")
    return text.replace(old, new, count)


def case_block(text, case_id):
    marker = f"- id: {case_id}\n"
    if text.count(marker) != 1:
        raise SystemExit(f"case {case_id}: marker expected once, found {text.count(marker)}")
    start = text.index(marker)
    end = text.find("\n- id: ", start + len(marker))
    if end < 0:
        end = len(text)
    return start, end, text[start:end]


def replace_in_case(text, case_id, old, new, label):
    start, end, block = case_block(text, case_id)
    actual = block.count(old)
    if actual != 1:
        raise SystemExit(f"{label}: expected once in {case_id}, found {actual}")
    block = block.replace(old, new, 1)
    return text[:start] + block + text[end:]


# -----------------------------------------------------------------------------
# D-088: repair the progression/default-step antecedent and make the lexical
# scope consequences explicit.
# -----------------------------------------------------------------------------
rel = "notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md"
t = read(rel)
t = exact(
    t,
    '  - "for each, filtros, cuantificadores, selección, dominios escalonados, intervalos, magnitudes, bloques de expresión, gramática, CST y AST"',
    '  - "for each, filtros, cuantificadores, selección, dominios escalonados, intervalos, magnitudes, bloques de expresión, resolución de nombres, gramática, CST y AST"',
    "D088 affects resolution",
)
t = exact(
    t,
    "Una fuente que ya posee enumeración propia —por ejemplo una colección ordenada, un diccionario exacto o un dominio nominal finito— no necesita `by` para recorrerse. Los pasos predeterminados solo intervienen cuando la enumeración se construye como progresión. En esas fuentes puede omitirse `by` únicamente cuando el tipo recorrido define una diferencia sucesora canónica. MUD fija `Nat -> 1`, `Int -> 1` y `Money -> 0.01`; omitir `by` selecciona siempre esa diferencia positiva. Otros tipos de progresión exacta requieren paso explícito salvo decisión que defina un sucesor canónico.",
    "Una fuente que ya posee enumeración propia —por ejemplo una colección, un diccionario exacto o un dominio nominal finito— no necesita `by` para recorrerse. Los pasos predeterminados solo intervienen cuando la enumeración se construye como progresión. En una fuente cuya enumeración se construye como progresión puede omitirse `by` únicamente cuando el tipo recorrido define una diferencia sucesora canónica. MUD fija `Nat -> 1`, `Int -> 1` y `Money -> 0.01`; omitir `by` selecciona siempre esa diferencia positiva. Otros tipos de progresión exacta requieren paso explícito salvo decisión que defina un sucesor canónico.",
    "D088 default-step antecedent",
)
anchor = "Las locales son puras, inmutables, secuenciales y no admiten referencias adelantadas, ciclos, redeclaración ni sombreado.\n"
addition = """

## Ámbitos de iteración y bloques de expresión

`source` y el `by` opcional se resuelven en el entorno exterior, antes de introducir la vinculación de iteración. Por tanto, la variable iterada —o la pareja `(key, value)`— no es visible dentro de `source` ni de `by`.

En `for each`, la vinculación de iteración sí es visible en el filtro `if` y en el cuerpo ejecutable. Si el filtro usa un `ExpressionBlock`, sus locales son visibles únicamente en las locales posteriores y en la expresión final del propio filtro; desaparecen antes de entrar en el cuerpo de efectos.

En selección y cuantificadores/agregadores, la vinculación introducida es visible en las locales y en la expresión final de su `ExpressionBlock`, pero no fuera de él. Cada local se vuelve visible después de su propia declaración, de modo que puede ser usada por locales posteriores y por el resultado final, nunca por su inicializador ni por declaraciones anteriores.
"""
if addition.strip() in t:
    raise SystemExit("D088 scope section already present")
if t.count(anchor) != 1:
    raise SystemExit(f"D088 scope anchor expected once, found {t.count(anchor)}")
t = t.replace(anchor, anchor + addition, 1)
write(rel, t)


# -----------------------------------------------------------------------------
# 09-nombres-y-anclas: the generic LocalSymbol representation already suffices,
# but the normative scope rules must cover the new owners introduced by D-088.
# -----------------------------------------------------------------------------
rel = "especificacion/09-nombres-y-anclas.md"
t = read(rel)
t = exact(
    t,
    "  - D-087\n",
    "  - D-087\n  - D-088\n",
    "09 frontmatter D088",
)
anchor = "Los accesos con puntos se elaboran por etapas: primero se resuelve la raíz nominal y después cada miembro con el tipo o propietario obtenido. Una ruta cualificada y una cadena de miembros pueden compartir escritura superficial sin compartir resolución interna.\n"
section = """

## Ámbitos de iteración y bloques de expresión

Las vinculaciones de iteración y las declaraciones locales de `ExpressionBlock` son `LocalSymbol`: no reciben ancla pública y obedecen al primer nivel léxico de resolución.

En `for each`, la fuente y el `by` opcional se resuelven antes de introducir la vinculación. La variable simple o ambas variables de una pareja de diccionario pasan a estar visibles en el filtro `if` y en el cuerpo ejecutable. Una local declarada dentro del `ExpressionBlock` del filtro solo amplía el entorno de las locales posteriores y de la expresión final del filtro; no permanece visible en el cuerpo de efectos.

En una selección o un cuantificador/agregador, `source` y `by` se resuelven igualmente en el entorno exterior. Después se introduce la vinculación y se resuelve el `ExpressionBlock`: cada local ve las vinculaciones exteriores y las locales anteriores; el resultado final ve todas las locales del bloque. La vinculación y esas locales dejan de existir al terminar la expresión propietaria.

Ninguno de estos ámbitos permite referencias adelantadas, ciclos, redeclaración o sombreado de un nombre ya visible. El AST resuelto usa la variante genérica `LocalSymbol(owner, kind, name, ordinal)`; D-088 no introduce una clase de símbolo ni una categoría de ancla nuevas.
"""
if section.strip() in t:
    raise SystemExit("09 D088 scope section already present")
if t.count(anchor) != 1:
    raise SystemExit(f"09 scope anchor expected once, found {t.count(anchor)}")
t = t.replace(anchor, anchor + section, 1)
write(rel, t)


# -----------------------------------------------------------------------------
# Conformance corpus: align textual AST expectations with the corrected sources
# and distinguish runtime evaluation failure from compile-time diagnostics.
# -----------------------------------------------------------------------------
rel = "especificacion/sintaxis/casos/cst-ast.yaml"
t = read(rel)
t = replace_in_case(
    t,
    "d088-for-each-body-after-terminator",
    "ast: ForEachEffect(binding=i, source=[1..3], body=EffectBlock(...))",
    "ast: ForEachEffect(binding=i, source=values, body=EffectBlock(...))",
    "for-each newline AST source",
)
t = replace_in_case(
    t,
    "d088-selection-body-after-terminator",
    "ast: SelectionExpr(binding=x, source=[1..3], predicate=ExpressionBlock([], x > 1))",
    "ast: SelectionExpr(binding=x, source=values, predicate=ExpressionBlock([], x > 1))",
    "selection newline AST source",
)
t = replace_in_case(
    t,
    "d088-quantifier-block-after-terminator",
    "ast: QuantifierExpr(Exists, x, [1..3], body=ExpressionBlock([limit], x > limit))",
    "ast: QuantifierExpr(Exists, x, values, body=ExpressionBlock([limit], x > limit))",
    "quantifier newline AST source",
)
t = replace_in_case(
    t,
    "d088-runtime-zero-step-action",
    "  expected_diagnostics:\n  - progression-step-zero-runtime-when-step-is-zero\n  semantic_expectations:\n",
    "  semantic_expectations:\n  - runtime-zero-step-produces-progression-step-zero\n",
    "runtime zero is not compile diagnostic",
)

# Add explicit scope conformance cases.
if "- id: d088-step-cannot-see-iteration-binding\n" in t:
    raise SystemExit("D088 v8 scope cases already present")
append = r'''
- id: d088-step-cannot-see-iteration-binding
  category: validation-after-resolution
  source: "action Broken for mut total: Num {\n    then for each value in [1..8] by value:\n        total += value\n}\n"
  cst_root: MudFileSyntax
  ast: ForEachEffect(binding=value, step=DottedPathExpr(value), ...)
  expected_diagnostics:
  - iteration-binding-not-visible-in-step
  semantic_expectations:
  - source-and-step-resolve-before-iteration-binding
  produces_ast: true
- id: d088-filter-local-not-visible-in-body
  category: validation-after-resolution
  source: "action Broken for values: Int [*], mut total: Int {\n    then for each value in values if {\n        adjusted := value + 1\n        adjusted > 0\n    }:\n        total += adjusted\n}\n"
  cst_root: MudFileSyntax
  ast: ForEachEffect(binding=value, filter=ExpressionBlock(locals=[adjusted], result=...), body=EffectBlock(...))
  expected_diagnostics:
  - filter-local-not-visible-in-loop-body
  semantic_expectations:
  - filter-expression-block-scope-ends-before-effect-body
  produces_ast: true
- id: d088-selection-binding-visible-in-expression-block
  category: expression
  source: "thing Sample {\n    values: Int [*]\n    selected := value in values: {\n        adjusted := value + 1\n        adjusted > 0\n    }\n}\n"
  cst_root: MudFileSyntax
  ast: SelectionExpr(binding=value, source=values, predicate=ExpressionBlock(locals=[adjusted], result=...))
  semantic_expectations:
  - selection-binding-visible-to-expression-block-locals-and-result
  produces_ast: true
'''
t = t.rstrip("\n") + "\n" + append.lstrip("\n")
write(rel, t)


# -----------------------------------------------------------------------------
# Postconditions.
# -----------------------------------------------------------------------------
checks = {
    "notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md": [
        "## Ámbitos de iteración y bloques de expresión",
        "no es visible dentro de `source` ni de `by`",
        "desaparecen antes de entrar en el cuerpo de efectos",
        "En una fuente cuya enumeración se construye como progresión",
    ],
    "especificacion/09-nombres-y-anclas.md": [
        "  - D-088",
        "## Ámbitos de iteración y bloques de expresión",
        "El AST resuelto usa la variante genérica `LocalSymbol(owner, kind, name, ordinal)`",
    ],
    "especificacion/sintaxis/casos/cst-ast.yaml": [
        "ast: ForEachEffect(binding=i, source=values, body=EffectBlock(...))",
        "ast: SelectionExpr(binding=x, source=values, predicate=ExpressionBlock([], x > 1))",
        "ast: QuantifierExpr(Exists, x, values, body=ExpressionBlock([limit], x > limit))",
        "id: d088-step-cannot-see-iteration-binding",
        "id: d088-filter-local-not-visible-in-body",
        "id: d088-selection-binding-visible-in-expression-block",
        "runtime-zero-step-produces-progression-step-zero",
    ],
}
for rel, needles in checks.items():
    text = read(rel)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"missing {needle!r} in {rel}")

if "En esas fuentes puede omitirse `by`" in read("notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md"):
    raise SystemExit("ambiguous default-step antecedent remains")

_, _, runtime_zero = case_block(read("especificacion/sintaxis/casos/cst-ast.yaml"), "d088-runtime-zero-step-action")
if "expected_diagnostics:" in runtime_zero:
    raise SystemExit("runtime-zero case still models evaluation failure as compile-time diagnostic")

print("D088_FIX_V8_OK")
