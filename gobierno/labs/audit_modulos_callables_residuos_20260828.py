from pathlib import Path

ROOT = Path.cwd()
SCOPES = [ROOT / "especificacion", ROOT / "notas" / "decisiones", ROOT / "aprendizaje"]
PATTERNS = [
    "things {",
    "rules {",
    "StartSet(things",
    "No ejecuta acciones reales.",
    "No se mezclan llamadas y efectos directos en el mismo `then`.",
    "Todas las hojas de una composición:",
    "`on` continúa vinculando una sola `thing` por rol",
    "`on` continúa vinculando exclusivamente `thing` individuales.",
    "Los `message` detectados se conservan como ocurrencias tentativas. Sus propiedades se calculan sobre el estado final",
    "La multiplicidad, orden y deduplicación de mensajes siguen en Q-052.",
    "`~private` solo es válido",
    "~private      : Bool = false",
    "~private = true",
    "`~private`, `~summary`, `~description` y `~deprecated` pueden usarse como defaults",
    "| `look` | sí | no | no |",
    "Una `subaction` solo puede invocarse desde el cuerpo de otra `action` o `subaction`.",
]

hits = []
for scope in SCOPES:
    for path in scope.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".ebnf", ".asdl", ".yaml", ".toml"}:
            continue
        # D-027 es histórico y sustituido; sus formulaciones antiguas son legítimas como historial.
        if path.name == "ADR-027-salidas-look-y-message.md":
            continue
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            for pattern in PATTERNS:
                if pattern in line:
                    hits.append((path.relative_to(ROOT).as_posix(), lineno, pattern, line.strip()))

if hits:
    for path, lineno, pattern, line in hits:
        print(f"RESIDUE {path}:{lineno}: {pattern!r}: {line}")
    raise SystemExit(f"{len(hits)} residuos críticos")

print("OK: sin residuos críticos conocidos de D-096")
