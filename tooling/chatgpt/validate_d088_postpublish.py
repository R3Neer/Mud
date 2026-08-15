from pathlib import Path
import sys
import yaml

root = Path(sys.argv[1]).resolve()


def read(rel):
    return (root / rel).read_text(encoding="utf-8")


def need(rel, needle):
    if needle not in read(rel):
        raise SystemExit(f"MISSING {needle!r} in {rel}")


def forbid(rel, needle):
    if needle in read(rel):
        raise SystemExit(f"STALE {needle!r} in {rel}")


d88 = "notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md"
for needle in (
    "resolución de nombres, gramática, CST y AST",
    "## Ámbitos de iteración y bloques de expresión",
    "no es visible dentro de `source` ni de `by`",
    "desaparecen antes de entrar en el cuerpo de efectos",
    "En una fuente cuya enumeración se construye como progresión",
    "action Accumulate for values: Int [* ordered]",
    "action Forward for mut total: Num",
    "fallo de evaluación `progression-step-zero`",
    "El requisito de recorrer como máximo un periodo fundamental de un dominio cíclico pertenece a la verificación de D-082",
):
    need(d88, needle)
for needle in (
    "En esas fuentes puede omitirse `by`",
    "process i",
    "process doubled",
    "use i",
    "intervalos discontinuos y del periodo fundamental cíclico",
):
    forbid(d88, needle)

names = "especificacion/09-nombres-y-anclas.md"
need(names, "  - D-088")
need(names, "## Ámbitos de iteración y bloques de expresión")
need(names, "la fuente y el `by` opcional se resuelven antes de introducir la vinculación")
need(names, "no permanece visible en el cuerpo de efectos")
need(names, "LocalSymbol(owner, kind, name, ordinal)")

d82 = "notas/decisiones/ADR-082-cycle-como-modificador-de-dominio-de-punto.md"
need(d82, "6. Una progresión sobre un dominio cíclico de punto visita como máximo un periodo fundamental")

q29 = "notas/preguntas/Q-029-terminacion.md"
need(q29, "resolved: false")
need(q29, "decisions: []")
forbid(q29, "parcialmente decidida")
forbid(q29, "  - D-088")
forbid(q29, "  - D-047")

for rel in (
    "notas/decisiones/ADR-033-claves-y-enumeracion-de-aliases.md",
    "notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md",
):
    forbid(rel, "    ...")
forbid("notas/decisiones/ADR-034-number-exacto-y-rumber-binary64.md", "for each value in [r0..r1] by r0.1: {}")

cases_path = "especificacion/sintaxis/casos/cst-ast.yaml"
data = yaml.safe_load(read(cases_path))
by_id = {case["id"]: case for case in data["cases"]}
for case_id in (
    "d088-for-each-body-after-terminator",
    "d088-selection-body-after-terminator",
    "d088-quantifier-block-after-terminator",
    "d088-runtime-zero-step-action",
    "d088-step-cannot-see-iteration-binding",
    "d088-filter-local-not-visible-in-body",
    "d088-selection-binding-visible-in-expression-block",
):
    if case_id not in by_id:
        raise SystemExit(f"missing D088 case {case_id}")

if "source=values" not in by_id["d088-for-each-body-after-terminator"]["ast"]:
    raise SystemExit("for-each newline AST source mismatch")
if "source=values" not in by_id["d088-selection-body-after-terminator"]["ast"]:
    raise SystemExit("selection newline AST source mismatch")
if ", values," not in by_id["d088-quantifier-block-after-terminator"]["ast"]:
    raise SystemExit("quantifier newline AST source mismatch")

runtime_zero = by_id["d088-runtime-zero-step-action"]
if "expected_diagnostics" in runtime_zero:
    raise SystemExit("runtime zero still modeled as compile diagnostic")
if "runtime-zero-step-produces-progression-step-zero" not in runtime_zero.get("semantic_expectations", []):
    raise SystemExit("runtime-zero semantic expectation missing")

if by_id["d088-step-cannot-see-iteration-binding"].get("expected_diagnostics") != ["iteration-binding-not-visible-in-step"]:
    raise SystemExit("step scope diagnostic mismatch")
if by_id["d088-filter-local-not-visible-in-body"].get("expected_diagnostics") != ["filter-local-not-visible-in-loop-body"]:
    raise SystemExit("filter-local scope diagnostic mismatch")

# D-087 follow-up must survive untouched.
model = "especificacion/04-modelo-matematico.md"
need(model, "ningún acceso `~` puede ser destino de una asignación o actualización runtime")
need(model, "Todo acceso `~` es de solo lectura durante la ejecución")
forbid("especificacion/README.md", "reglas de escritura de `~name`")
forbid("notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md", "`~name` es mutable para `thing`")

print("D088_POSTPUBLISH_INVARIANTS_OK")
