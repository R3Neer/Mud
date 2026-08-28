from __future__ import annotations

import argparse
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def replace_if_present(path: Path, old: str, new: str, label: str) -> None:
    text = read(path)
    count = text.count(old)
    if count > 1:
        raise SystemExit(f"{label}: anclaje ambiguo ({count} apariciones) en {path}")
    if count == 1:
        write(path, text.replace(old, new, 1))


def remove_private(root: Path) -> None:
    spec = root / "especificacion/07-gramatica-concreta.md"
    replace_if_present(
        spec,
        "\n\n### Metadata de usuario llamada `private`\n\n`private` no es un metadato estándar ni controla visibilidad. Como `metadata-name` admite identificadores ordinarios, `~private` puede declararse y consultarse como metadata de usuario cuando el propietario admita metadata configurable. Se comporta como cualquier otra metadata de extensión y no recibe tratamiento especial.\n",
        "\n",
        "07/private",
    )

    adr87 = root / "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md"
    replace_if_present(
        adr87,
        "\n`~private` queda retirado por D-096 y cualquier intento de declararlo como metadato estándar es inválido. La exposición exterior se deriva de la frontera de módulo, la categoría operacional y el cierre de tipos requerido por el contrato; no se expresa mediante un booleano metadata-bearing.\n",
        "",
        "D-087/private-estandar",
    )
    replace_if_present(
        adr87,
        " `~private` no existe.",
        "",
        "D-087/private-default",
    )
    replace_if_present(
        adr87,
        "11. Rechazo de `~private` como nombre estándar retirado y ausencia de ese default de archivo.\n12. `~summary`, `~description` y `~deprecated` en elementos subordinados.\n13. Colecciones y diccionarios con propiedades intrínsecas tipadas.\n14. Narrowing categorial de declaraciones.\n15. Eliminación completa de `anchor{...}`.",
        "11. `~summary`, `~description` y `~deprecated` en elementos subordinados.\n12. Colecciones y diccionarios con propiedades intrínsecas tipadas.\n13. Narrowing categorial de declaraciones.\n14. Eliminación completa de `anchor{...}`.",
        "D-087/private-verificacion",
    )
    replace_if_present(
        adr87,
        "\n`~private` queda retirado por completo como metadato estándar y como default de fichero. La visibilidad exterior se deriva de módulo, categoría operacional y cierre de tipos.",
        "\nLa visibilidad exterior se deriva de módulo, categoría operacional y cierre de tipos.",
        "D-087/private-modificacion",
    )

    adr91 = root / "notas/decisiones/ADR-091-datos-de-family-como-descriptores-anclados.md"
    replace_if_present(
        adr91,
        "\n`~private` no es válido en datos asociados de `family` ni en ninguna otra declaración: D-096 lo retira del lenguaje.\n",
        "\n",
        "D-091/private-decision",
    )
    replace_if_present(
        adr91,
        "\n## Modificación vigente por D-096\n\nLa referencia histórica a las ubicaciones donde D-087 permitía `~private` queda reemplazada: `~private` ya no forma parte del lenguaje. El resto del contrato de descriptores de datos de `family` permanece vigente.\n",
        "",
        "D-091/private-modificacion",
    )

    adr96 = root / "notas/decisiones/ADR-096-modulos-callables-look-message-y-activacion.md"
    replace_if_present(
        adr96,
        "`message` como salida diferida al host, privacidad mediante `~private`, activación separada",
        "`message` como salida diferida al host, activación separada",
        "D-096/private-contexto",
    )
    replace_if_present(
        adr96,
        "`~private` deja de ser metadato estándar y desaparece también como default de fichero. El identificador `private` permanece disponible como nombre ordinario de metadata de usuario: una metadata `~private` no recibe significado especial ni controla visibilidad. La visibilidad se deriva de la categoría semántica, el módulo propietario, los contratos entre módulos y el cierre de tipos requerido por esos contratos.",
        "La visibilidad se deriva de la categoría semántica, el módulo propietario, los contratos entre módulos y el cierre de tipos requerido por esos contratos.",
        "D-096/private-visibilidad",
    )

    inventory = root / "notas/inventario-saneamiento-especificacion.md"
    replace_if_present(
        inventory,
        "\n## Decisiones aclaradas durante el saneamiento\n\n### `~private`\n\n`~private` no tiene significado estándar ni controla visibilidad o frontera modular. Sin embargo, `private` puede usarse como nombre de metadata ordinaria de extensión del mismo modo que cualquier otro `identifier` permitido en `metadata-name`.\n\nPor tanto, cualquier regla que reserve o prohíba específicamente la grafía `~private` es un defecto. La corrección no debe reintroducir ninguna semántica estándar de privacidad.\n",
        "",
        "inventario/private",
    )

    hits: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = read(path)
        except (UnicodeDecodeError, OSError):
            continue
        if "~private" in text:
            hits.append(str(path.relative_to(root)))
    if hits:
        raise SystemExit("quedan apariciones de ~private: " + ", ".join(sorted(hits)))


POLICY = '''---
title: Política de archivos temporales de MUD
aliases:
  - Archivos temporales
tags:
  - mud/gobierno
  - mud/temporales
status: vigente
---

# Política de archivos temporales de MUD

## Propósito

Esta política regula los documentos que deben permanecer versionados durante varios commits porque coordinan trabajo en curso, pero que no forman parte del estado permanente del proyecto.

Un archivo efímero ordinario no se versiona. Logs, builds, caches, volcados, estado local de herramientas y demás residuos reproducibles deben vivir fuera del repositorio o quedar cubiertos por `.gitignore`.

## Fuente de verdad

El frontmatter del propio documento es la única fuente de verdad sobre su temporalidad. Un documento Markdown intencionadamente temporal usa:

```yaml
temporary: true
temporary-reason: "Motivo por el que debe permanecer versionado"
temporary-delete-when: "Condición semántica de eliminación"
temporary-delete-after: 2026-09-30
```

`temporary-delete-after` es opcional y solo se usa cuando existe una fecha límite objetiva.

No se usa `temporary: false`. Si un documento temporal pasa legítimamente a ser permanente, se eliminan `temporary` y todas las propiedades `temporary-*`. Si deja de ser necesario, se elimina el archivo.

## Significado de las propiedades

- `temporary: true`: el documento debe desaparecer eventualmente o abandonar explícitamente su ciclo temporal convirtiéndose en permanente.
- `temporary-reason`: explica por qué merece estar versionado mientras tanto. Es obligatorio y no puede estar vacío.
- `temporary-delete-when`: condición semántica obligatoria que determina cuándo debe eliminarse. Es obligatoria y no puede estar vacía.
- `temporary-delete-after`: fecha límite opcional en formato ISO `YYYY-MM-DD`. Una fecha ya vencida bloquea el commit.

Las propiedades son planas. No se mantiene un registro manual paralelo de archivos temporales.

## Alcance

El contrato `temporary:*` se aplica a documentos Markdown intencionadamente versionados. Un artefacto temporal no Markdown no se introduce en `main` mediante esta política; debe mantenerse fuera del repositorio, en una rama de laboratorio o quedar cubierto por una política específica que establezca un ciclo de vida equivalente.

## Vista de Obsidian

`[[temporales.base|gobierno/temporales.base]]` es una vista humana derivada de las Properties de las notas. No es una segunda fuente de verdad y ningún archivo se añade manualmente a ella.

La Base ofrece:

- **Temporales activos**: todos los documentos con `temporary: true`.
- **Con fecha límite**: temporales que declaran `temporary-delete-after`, ordenados por fecha.
- **Metadata incompleta**: temporales sin motivo o sin condición de eliminación.

## Validación mecánica

Desde la raíz del repositorio:

```powershell
python gobierno/validate_temporaries.py
```

El validador:

- descubre documentos Markdown versionados y no ignorados;
- imprime siempre el inventario de temporales activos;
- exige `temporary-reason` y `temporary-delete-when` no vacíos;
- rechaza `temporary: false` y propiedades `temporary-*` sin `temporary: true`;
- valida `temporary-delete-after` como fecha ISO cuando existe;
- falla si una fecha límite ya ha vencido.

El validador no intenta interpretar condiciones semánticas arbitrarias como «se complete la Etapa 8». La persona o agente que prepara el commit debe revisar el inventario impreso y decidir si alguna condición ya se cumple.

## Gate antes de cada commit

Antes de crear cualquier commit se ejecuta el validador y se revisa el inventario de `temporary: true`.

Si la condición `temporary-delete-when` de un documento ya se cumple, el documento debe eliminarse antes de cerrar el commit, salvo que el propio cambio esté modificando explícitamente su ciclo de vida. Una fecha `temporary-delete-after` vencida es un bloqueo mecánico y no puede ignorarse mediante una excepción informal.

La revisión se aplica a todos los temporales activos, no solo a los archivos modificados por el commit.
'''

BASE = '''filters:
  and:
    - 'temporary == true'

properties:
  temporary-reason:
    displayName: Motivo
  temporary-delete-when:
    displayName: Eliminar cuando
  temporary-delete-after:
    displayName: Fecha límite

views:
  - type: table
    name: Temporales activos
    order:
      - file.name
      - temporary-reason
      - temporary-delete-when
      - temporary-delete-after

  - type: table
    name: Con fecha límite
    filters:
      and:
        - 'file.hasProperty("temporary-delete-after")'
    order:
      - file.name
      - temporary-reason
      - temporary-delete-when
      - temporary-delete-after
    sort:
      - property: temporary-delete-after
        direction: ASC

  - type: table
    name: Metadata incompleta
    filters:
      or:
        - 'note["temporary-reason"].isEmpty()'
        - 'note["temporary-delete-when"].isEmpty()'
    order:
      - file.name
      - temporary-reason
      - temporary-delete-when
      - temporary-delete-after
'''

VALIDATOR = '''from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

TEMP_KEYS = {
    "temporary",
    "temporary-reason",
    "temporary-delete-when",
    "temporary-delete-after",
}
ISO_DATE = re.compile(r"^\\d{4}-\\d{2}-\\d{2}$")


@dataclass(frozen=True)
class Temporary:
    path: Path
    reason: str
    delete_when: str
    delete_after: date | None


def scalar(raw: str) -> object:
    raw = raw.strip()
    if raw == "true":
        return True
    if raw == "false":
        return False
    if raw.startswith('"') and raw.endswith('"'):
        return json.loads(raw)
    if raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1].replace("''", "'")
    return raw


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\\n"):
        return {}
    end = text.find("\\n---\\n", 4)
    if end < 0:
        return {}
    result: dict[str, object] = {}
    for line in text[4:end].splitlines():
        if not line or line.startswith((" ", "\\t", "#")) or ":" not in line:
            continue
        key, raw = line.split(":", 1)
        if key in TEMP_KEYS:
            result[key] = scalar(raw)
    return result


def markdown_files(root: Path) -> list[Path]:
    try:
        completed = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                "*.md",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return sorted(path for path in root.rglob("*.md") if ".git" not in path.parts)
    return sorted(root / item.decode("utf-8") for item in completed.stdout.split(b"\\0") if item)


def validate(root: Path) -> tuple[list[Temporary], list[str]]:
    active: list[Temporary] = []
    errors: list[str] = []
    today = date.today()

    for path in markdown_files(root):
        data = frontmatter(path)
        present = TEMP_KEYS.intersection(data)
        if not present:
            continue
        rel = path.relative_to(root)
        flag = data.get("temporary")

        if flag is False:
            errors.append(f"{rel}: no se admite temporary: false; elimina las propiedades temporary-* si el archivo es permanente")
            continue
        if flag is not True:
            errors.append(f"{rel}: las propiedades temporary-* requieren temporary: true")
            continue

        reason = data.get("temporary-reason")
        delete_when = data.get("temporary-delete-when")
        reason_text = reason.strip() if isinstance(reason, str) else ""
        when_text = delete_when.strip() if isinstance(delete_when, str) else ""
        if not reason_text:
            errors.append(f"{rel}: falta temporary-reason no vacío")
        if not when_text:
            errors.append(f"{rel}: falta temporary-delete-when no vacío")

        deadline: date | None = None
        raw_deadline = data.get("temporary-delete-after")
        if raw_deadline is not None:
            if not isinstance(raw_deadline, str) or not ISO_DATE.fullmatch(raw_deadline):
                errors.append(f"{rel}: temporary-delete-after debe usar YYYY-MM-DD")
            else:
                try:
                    deadline = date.fromisoformat(raw_deadline)
                except ValueError:
                    errors.append(f"{rel}: temporary-delete-after no es una fecha válida")
                else:
                    if today > deadline:
                        errors.append(f"{rel}: temporary-delete-after venció el {deadline.isoformat()}")

        active.append(Temporary(rel, reason_text, when_text, deadline))

    return active, errors


def print_inventory(active: list[Temporary]) -> None:
    print("Temporales activos:")
    if not active:
        print("  ninguno")
        return
    for item in sorted(active, key=lambda value: str(value.path)):
        deadline = item.delete_after.isoformat() if item.delete_after else "—"
        print(f"- {item.path}")
        print(f"  motivo: {item.reason or '[FALTA]'}")
        print(f"  eliminar cuando: {item.delete_when or '[FALTA]'}")
        print(f"  fecha límite: {deadline}")
    print("Revisión semántica obligatoria: comprueba si alguna condición 'eliminar cuando' ya se cumple.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida documentos temporales intencionadamente versionados.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    root = args.root.resolve()
    active, errors = validate(root)
    print_inventory(active)
    if errors:
        print("Errores:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def govern(root: Path) -> None:
    write(root / "gobierno/POLITICA-DE-ARCHIVOS-TEMPORALES.md", POLICY)
    write(root / "gobierno/temporales.base", BASE)
    write(root / "gobierno/validate_temporaries.py", VALIDATOR)

    agents = root / "AGENTS.md"
    replace_if_present(
        agents,
        "\n## Git\n",
        "\n## Archivos temporales\n\nLos documentos intencionadamente temporales se rigen por `gobierno/POLITICA-DE-ARCHIVOS-TEMPORALES.md`. Los archivos efímeros ordinarios no se versionan.\n\nAntes de crear cualquier commit se debe ejecutar `python gobierno/validate_temporaries.py` y revisar el inventario completo de documentos con `temporary: true`. Si la condición `temporary-delete-when` de alguno ya se cumple, debe eliminarse antes de cerrar el commit, salvo que el propio cambio modifique explícitamente su ciclo de vida.\n\nLa temporalidad se declara únicamente en el frontmatter del documento; `gobierno/temporales.base` es una vista derivada y no un registro independiente.\n\n## Git\n",
        "AGENTS/temporales",
    )

    commit_policy = root / "gobierno/POLITICA-DE-COMMITS.md"
    replace_if_present(
        commit_policy,
        "- Archivos temporales o estado local de Obsidian.",
        "- Archivos efímeros ordinarios, builds, logs, caches, volcados o estado local de Obsidian.\n\nUn documento intencionadamente temporal puede permanecer versionado únicamente bajo [[POLITICA-DE-ARCHIVOS-TEMPORALES|la política de archivos temporales]]. Su temporalidad no lo exime de la atomicidad del commit ni convierte residuos efímeros en material versionable.",
        "commits/atomicidad-temporales",
    )
    replace_if_present(
        commit_policy,
        "## Proceso previo\n\nAntes de crear un commit, Codex debe:\n\n1. Leer las instrucciones aplicables.\n2. Revisar `git status`.\n3. Identificar archivos previos o ajenos.\n4. Inspeccionar el diff.\n5. Ejecutar validaciones disponibles.\n6. Añadir únicamente los archivos de la unidad atómica.\n7. Revisar el diff staged.\n8. Crear el commit.\n9. Confirmar que el estado posterior es el esperado.",
        "## Gate de archivos temporales\n\nAntes de cualquier commit se ejecuta:\n\n```powershell\npython gobierno/validate_temporaries.py\n```\n\nEl inventario impreso debe revisarse completo. Si la condición `temporary-delete-when` de algún documento ya se cumple, ese documento debe eliminarse antes de cerrar el commit, salvo que el propio cambio modifique explícitamente su ciclo de vida. Una fecha `temporary-delete-after` vencida bloquea mecánicamente el commit.\n\n## Proceso previo\n\nAntes de crear un commit, Codex debe:\n\n1. Leer las instrucciones aplicables.\n2. Revisar `git status`.\n3. Identificar archivos previos o ajenos.\n4. Inspeccionar el diff.\n5. Ejecutar `python gobierno/validate_temporaries.py` y revisar semánticamente todo su inventario.\n6. Ejecutar las demás validaciones disponibles.\n7. Añadir únicamente los archivos de la unidad atómica.\n8. Revisar el diff staged.\n9. Crear el commit.\n10. Confirmar que el estado posterior es el esperado.",
        "commits/gate-temporales",
    )

    gov_readme = root / "gobierno/README.md"
    replace_if_present(
        gov_readme,
        "- [[POLITICA-DE-COMMITS|Política de commits]]\n",
        "- [[POLITICA-DE-COMMITS|Política de commits]]\n- [[POLITICA-DE-ARCHIVOS-TEMPORALES|Política de archivos temporales]]\n- [[temporales.base|Vista de temporales activos]]\n",
        "gobierno/readme-temporales",
    )

    inventory = root / "notas/inventario-saneamiento-especificacion.md"
    replace_if_present(
        inventory,
        "temporary: true\n---",
        "temporary: true\ntemporary-reason: \"Checklist operativo del saneamiento de la especificación\"\ntemporary-delete-when: \"Se complete la Etapa 8 del saneamiento de la especificación\"\n---",
        "inventario/frontmatter-temporal",
    )
    replace_if_present(
        inventory,
        "\n> [!warning] Artefacto temporal\n> Este archivo existe únicamente mientras el saneamiento por etapas siga abierto. Debe eliminarse en el mismo cambio que cierre la Etapa 8; Git conserva el historial y este checklist no debe quedar archivado como documentación permanente.\n",
        "",
        "inventario/warning-temporal",
    )
    replace_if_present(
        inventory,
        "9. eliminar `notas/inventario-saneamiento-especificacion.md` en el mismo cambio que cierre la etapa.\n",
        "",
        "inventario/delete-redundante",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("private", "govern"))
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.phase == "private":
        remove_private(root)
    else:
        govern(root)


if __name__ == "__main__":
    main()
