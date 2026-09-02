from __future__ import annotations

import argparse
import os
import tempfile
import tomllib
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROFILE = Path(__file__).with_name("mud-es-en.toml")
GLOSSARY = ROOT / "notas" / "glosario-de-traduccion-es-en.md"


def escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render() -> str:
    data = tomllib.loads(PROFILE.read_text(encoding="utf-8-sig"))
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for term in data.get("terms", []):
        groups[str(term.get("category", "Other"))].append(term)
    lines = [
        "---",
        "title: Glosario transitorio de traducción español-inglés",
        "aliases:",
        "  - Glosario de migración al inglés",
        "tags:",
        "  - mud/notas",
        "  - mud/traduccion",
        "status: activo",
        "decisions:",
        "  - D-104",
        "temporary: true",
        f'temporary-reason: "{data["temporary-reason"]}"',
        f'temporary-delete-when: "{data["temporary-delete-when"]}"',
        "---",
        "",
        "# Glosario transitorio de traducción español-inglés",
        "",
        "> [!warning]",
        "> Esta es una vista humana generada desde `tooling/translation/mud-es-en.toml`.",
        "> No se edita a mano ni define semántica nueva de Mud.",
        "",
        "## Contrato de migración",
        "",
        "El perfil conserva código, matemáticas, HTML, URLs, rutas, embeds, destinos",
        "de enlaces, identificadores y valores contractuales de frontmatter. Traduce",
        "etiquetas visibles y los campos editoriales seleccionados. El destino es",
        "inglés británico (`EN-GB`).",
        "",
        "En `[[path|label]]` se conserva `path`; en `[label](URL)` se conserva la URL.",
        "Los términos `force` se imponen mediante marcadores opacos y los términos",
        "`review` requieren una decisión contextual.",
        "",
        "## Formas Mud protegidas",
        "",
        "| Forma literal | Forma literal | Forma literal |",
        "| --- | --- | --- |",
    ]
    literals = data.get("protected", {}).get("literals", [])
    for index in range(0, len(literals), 3):
        row = [f"`{escape(value)}`" for value in literals[index : index + 3]]
        row.extend([""] * (3 - len(row)))
        lines.append("| " + " | ".join(row) + " |")
    for category, terms in groups.items():
        lines.extend(["", f"## {category}", "", "| Español | Inglés canónico | Tratamiento | Nota |", "| --- | --- | --- | --- |"])
        for term in terms:
            target = escape(term.get("target", "—"))
            lines.append(f"| {escape(term['source'])} | {target} | `{escape(term.get('mode', 'force'))}` | {escape(term.get('note', ''))} |")
    lines.extend(["", "## Decisiones de estilo", ""])
    lines.extend(f"- {item}" for item in data.get("style", {}).get("guidance", []))
    lines.extend(["", "## Grafías estadounidenses prohibidas", "", ", ".join(f"`{item}`" for item in data.get("style", {}).get("forbidden", [])) + ".", ""])
    return "\n".join(lines)


def write_atomic(path: Path, value: str) -> None:
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    expected = render()
    current = GLOSSARY.read_text(encoding="utf-8-sig") if GLOSSARY.exists() else ""
    if arguments.check:
        if current != expected:
            print(f"ERROR: {GLOSSARY.relative_to(ROOT)} is not generated from {PROFILE.relative_to(ROOT)}")
            return 1
        print("OK: el glosario temporal coincide con el perfil TOML")
        return 0
    write_atomic(GLOSSARY, expected)
    print(f"Generated {GLOSSARY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
