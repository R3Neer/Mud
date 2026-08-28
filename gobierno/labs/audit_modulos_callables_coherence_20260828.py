from pathlib import Path

ROOT = Path.cwd()
SCOPES = [ROOT / "especificacion", ROOT / "notas" / "decisiones", ROOT / "aprendizaje"]
FORBIDDEN = [
    "Clasificación elemental o compuesta de acciones.",
    "Una referencia completamente cualificada se resuelve directamente.",
    "- `given`: valores auxiliares de reglas booleanas y actions.",
    "Un único `start with` global",
    "Sustitución completa del `start with` global.",
    "`and` y `or` combinan activadores respectivamente mediante `All` y `Any`.",
    "IR representa explícitamente `Rise`, `Temporal`, `Changed`, `All` y `Any`",
    "Universo limitado a `thing` concretas y activas.",
    "`take` sobre colección ordenada, no ordenada, dominio",
    "conjuntos separados de activación de `thing` y reglas",
    "llamada a `subaction` fuera de acción o subacción",
    "forma mezclada retirada de `start with`",
    "La activación inicial no mezcla categorías",
    "La visibilidad exterior se vuelve una propiedad de generación/tooling",
    "El `start with` global y el local de tests",
    "No incluye acciones, reglas, tests, declaraciones",
]

hits = []
for scope in SCOPES:
    for path in scope.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".ebnf", ".asdl", ".yaml", ".toml"}:
            continue
        if path.name == "ADR-027-salidas-look-y-message.md":
            continue
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            for pattern in FORBIDDEN:
                if pattern in line:
                    hits.append((path.relative_to(ROOT).as_posix(), lineno, pattern, line.strip()))

if hits:
    for path, lineno, pattern, line in hits:
        print(f"STALE {path}:{lineno}: {pattern!r}: {line}")
    raise SystemExit(f"{len(hits)} residuos editoriales de D-096")

required = {
    "especificacion/sintaxis/cst-sin-perdidas.md": ["D-096", "capacidades exteriores"],
    "notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas.md": ["la cualificación no sustituye la autorización `uses`"],
    "notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md": ["reglas booleanas, actions, subactions y `look`"],
    "notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo.md": ["natural join", "cero o más matches", "no fija una codificación IR cerrada"],
    "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md": ["StartSet(contributions)", "descriptores first-class", "secciones retiradas `things`/`rules`"],
    "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md": ["contrato `uses`", "`~private` queda retirado"],
}
for rel, needles in required.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"{rel}: falta evidencia vigente: {needle!r}")

print("OK: segunda auditoría de coherencia D-096 sin residuos conocidos")
