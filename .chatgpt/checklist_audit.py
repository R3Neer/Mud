from __future__ import annotations

from pathlib import Path
import os
import re
import yaml

ROOT = Path(os.environ.get("MUD_AUDIT_ROOT", Path(__file__).resolve().parents[1])).resolve()


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def fm(rel: str) -> dict:
    text = read(rel)
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    return yaml.safe_load(text[4:end]) or {}


def present(rel: str, needle: str) -> bool:
    return needle in read(rel)


def heading(title: str) -> None:
    print(f"\n=== {title} ===")


heading("BASE")
print("audit-root", ROOT)

heading("CHECKLIST STATUS")
checks = []
checks.append((1, "partial", "D-089 exists; user-specific UnitForm admissibility/collision rule still absent"))
checks.append((2, "done", "D-090 removes public branch anchors and uses canonical selector key"))
checks.append((3, "mismatch", "D-093 removes normative Resolved AST, but checklist requires a nominal Resolved AST/HIR"))
checks.append((4, "partial", "decision policy already requires vigente ADR text to be effective; global stale-ADR sweep still required"))
checks.append((5, "done", "D-091 anchors family-data descriptors and keeps member overrides unanchored"))
checks.append((6, "partial", "D-094 anchors Metadata but explicitly omits Metadata~path/~file; user now requires both"))
checks.append((7, "partial", "D-032 already decides contextual alias construction; modern spec/IR/cases need explicit promotion"))
checks.append((8, "done", "GivenDecl now uses TypeExpr and admits dictionary types"))
checks.append((9, "done", "D-095 defines min/max(empty) -> empty [0..1]"))
checks.append((10, "done", "Q-060 exists for TypeKind catalog"))
checks.append((11, "done", "question policy/validator implement criterion evidence; Q-054/Q-055 are closed after D-089 formalization"))
checks.append((12, "partial", "modern chapters remain propuesta/esqueleto; authority/readability needs explicit audit after ADR cleanup"))
for n, state, why in checks:
    print(f"{n:02d} {state.upper():8} {why}")

heading("SPEC STATUSES")
for rel in [
    "especificacion/00-convenciones-editoriales.md",
    "especificacion/04-modelo-matematico.md",
    "especificacion/06-lexico.md",
    "especificacion/07-gramatica-concreta.md",
    "especificacion/08-sintaxis-abstracta.md",
    "especificacion/09-nombres-y-anclas.md",
]:
    data = fm(rel)
    print(rel, "status=", data.get("status"), "questions=", data.get("questions", []))

heading("ADR COUNTS")
counts = {}
for path in sorted((ROOT / "notas/decisiones").glob("ADR-*.md")):
    data = fm(str(path.relative_to(ROOT)))
    counts[data.get("status", "<none>")] = counts.get(data.get("status", "<none>"), 0) + 1
print(counts)

heading("KNOWN STALE SEMANTIC PATTERNS IN VIGENTE ADRS")
patterns = {
    "anonymous-participant": re.compile(r"an[oó]nim", re.I),
    "anchor-interpolation": re.compile(r"anchor\{"),
    "old-start-flat": re.compile(r"start with\s*\{"),
    "resolved-ast": re.compile(r"mud-resolved-ast|AST resuelto", re.I),
    "old-unit-property": re.compile(r"\b(?:name|plural|abbreviation|format|prefixes)\s*=\s*", re.I),
    "branch-anchor": re.compile(r"ancla.{0,35}rama|rama.{0,35}ancla", re.I),
}
for path in sorted((ROOT / "notas/decisiones").glob("ADR-*.md")):
    rel = str(path.relative_to(ROOT))
    data = fm(rel)
    if data.get("status") != "vigente":
        continue
    text = path.read_text(encoding="utf-8")
    hits = []
    for name, pattern in patterns.items():
        if pattern.search(text):
            hits.append(name)
    if hits:
        print(rel, ",".join(hits))

heading("MECHANICAL RESIDUES")
for needle in ["BooleanBlock", "mud-resolved-ast.asdl", "MetadataAttachment", "UnitProperties", "AnchorInterpolation"]:
    found = []
    for root in [ROOT / "especificacion", ROOT / "notas"]:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".asdl", ".ebnf", ".yaml", ".py"}:
                try:
                    txt = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                if needle in txt:
                    found.append(str(path.relative_to(ROOT)))
    print(needle, found)

heading("POINT 1 UNIT FORMS")
for rel in [
    "notas/decisiones/ADR-089-clasificacion-contextual-de-formas-fuente.md",
    "notas/decisiones/ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente.md",
    "especificacion/06-lexico.md",
    "notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos.md",
]:
    text = read(rel)
    print(rel,
          "spaces=", bool(re.search(r"espaci|varios tokens|varias unidades", text, re.I)),
          "digits-ban=", bool(re.search(r"cifras|d[ií]git", text, re.I)),
          "symbols-ban=", bool(re.search(r"s[ií]mbol", text, re.I)),
          "keyword-collision=", bool(re.search(r"keyword|palabra reservada", text, re.I)))

heading("POINT 3 PIPELINE")
print("D093 no-second-AST=", present("notas/decisiones/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado.md", "no construye un segundo AST normativo"))
print("old resolved schema exists=", (ROOT / "especificacion/sintaxis/mud-resolved-ast.asdl").exists())
print("semantic IR exists=", (ROOT / "especificacion/ir/mud-semantic-ir.asdl").exists())

heading("POINT 6 METADATA")
d94 = read("notas/decisiones/ADR-094-anclas-terminales-de-metadatos-configurados.md")
print("D094 path omitted=", "no añade por simetría `~path` ni `~file`" in d94)
print("D087 Metadata descriptor path=", bool(re.search(r"### Descriptor `Metadata`.*?~path", read("notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md"), re.S)))

heading("POINT 7 CONTEXTUAL ALIAS")
d32 = read("notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal.md")
print("D032 literal basic contextual=", 'playerName: PlayerName = "Ada"' in d32)
for rel in ["especificacion/08-sintaxis-abstracta.md", "especificacion/sintaxis/casos/cst-ast.yaml", "especificacion/ir/mud-semantic-ir.asdl"]:
    text = read(rel)
    print(rel, "contextual-alias-markers=", any(x in text for x in ["ContextualAlias", "construcción contextual", "contextual construction", "PlayerName"]))

heading("POINTS 8-11")
print("given dictionary TypeExpr=", "`GivenDecl` usa el mismo `TypeExpr`" in read("especificacion/08-sintaxis-abstracta.md"))
print("D095 exists=", (ROOT / "notas/decisiones/ADR-095-extremos-vacios-como-ausencia-ordinaria.md").exists())
print("Q060 exists=", any((ROOT / "notas/preguntas").glob("Q-060-*.md")))
q54 = fm("notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos.md")
q55 = fm("notas/preguntas/Q-055-literales-de-magnitudes-de-punto.md")
print("Q054 resolved=", q54.get("resolved"), "Q055 resolved=", q55.get("resolved"))

print("\nAUDIT_COMPLETE")
