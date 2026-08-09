"""Generate deterministic Phase 0 payloads without third-party dependencies."""

from __future__ import annotations

import base64
import hashlib
import io
import json
import tempfile
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo


OUTPUT = Path(tempfile.gettempdir()) / "mud-repo-patcher-mcp-probe" / "inputs"
ZIP_SIZES = (1024, 16 * 1024, 64 * 1024, 128 * 1024, 256 * 1024)


def exact_zip(size: int) -> bytes:
    def build(payload: bytes) -> bytes:
        stream = io.BytesIO()
        info = ZipInfo("probe.bin", date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = ZIP_STORED
        info.external_attr = 0o100644 << 16
        with ZipFile(stream, "w", compression=ZIP_STORED) as archive:
            archive.writestr(info, payload)
        return stream.getvalue()

    overhead = len(build(b""))
    if size < overhead:
        raise ValueError(f"{size} is smaller than the ZIP overhead {overhead}")
    payload = bytes((index * 131 + 17) % 256 for index in range(size - overhead))
    result = build(payload)
    if len(result) != size:
        raise AssertionError((len(result), size))
    return result


def file(path: str, content: str | bytes) -> dict[str, str]:
    if isinstance(content, bytes):
        return {
            "path": path,
            "encoding": "base64",
            "content": base64.b64encode(content).decode("ascii"),
        }
    return {"path": path, "encoding": "utf8", "content": content}


def representative_files() -> list[dict[str, str]]:
    operations = []
    files = []
    for index in range(120):
        path = f"notas/prueba/ruta-{index:03d}.md"
        operations.append(
            "\n".join(
                [
                    f"  - op: create_file",
                    f"    path: {path}",
                    "    content: |",
                    f"      Evidencia número {index}: áéíóú, ñ, λ y 日本語.",
                ]
            )
        )
    patch_yaml = "\n".join(
        [
            "schema: 1",
            "id: fase-0-representativa",
            "title: Paquete representativo de transporte",
            "target:",
            "  repository: R3Neer/Mud",
            "operations:",
            *operations,
            "",
        ]
    )
    files.append(file("patch.yaml", patch_yaml))
    for index in range(24):
        files.append(
            file(
                f"docs/capitulo-{index:02d}.md",
                f"# Capítulo {index}\n\nContenido reproducible con acentos: canción, árbol y pingüino.\n",
            )
        )
    files.extend(
        [
            file("config/validacion.yaml", "schema: 1\nstrict: true\nlocale: es-ES\n"),
            file(
                "plugin.py",
                "def build(context):\n    context.note('plugin opcional de Fase 0')\n",
            ),
            file("assets/recurso.bin", bytes((index * 73 + 29) % 256 for index in range(8192))),
        ]
    )
    return files


def write_json(name: str, value: object) -> None:
    (OUTPUT / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for size in ZIP_SIZES:
        data = exact_zip(size)
        label = f"zip-{size // 1024:03d}k"
        path = OUTPUT / f"{label}.zip"
        path.write_bytes(data)
        sha256 = hashlib.sha256(data).hexdigest()
        manifest.append({"name": path.name, "size": size, "sha256": sha256})
        write_json(
            f"{label}-request.json",
            {
                "request_id": f"phase0-{label}-attempt-REPLACE",
                "content_base64": base64.b64encode(data).decode("ascii"),
                "expected_sha256": sha256,
            },
        )

    write_json(
        "files-minimal-request.json",
        {
            "request_id": "phase0-files-minimal-attempt-REPLACE",
            "files": [
                file(
                    "patch.yaml",
                    "schema: 1\nid: fase-0-minimal\ntitle: Mínimo\noperations: []\n",
                )
            ],
        },
    )
    write_json(
        "files-representative-request.json",
        {
            "request_id": "phase0-files-representative-attempt-REPLACE",
            "files": representative_files(),
        },
    )
    write_json(
        "files-unicode-binary-request.json",
        {
            "request_id": "phase0-files-unicode-attempt-REPLACE",
            "files": [
                file("carpeta/áéíóú-日本語.md", "España, pingüino, λ, 😀\n"),
                file("recursos/todos-los-bytes.bin", bytes(range(256)) * 8),
                file("patch.yaml", "schema: 1\nid: unicode-binario\noperations: []\n"),
            ],
        },
    )
    write_json("base64-manifest.json", manifest)
    print(f"Generated {len(manifest)} ZIP probes and 3 logical payloads in {OUTPUT}")


if __name__ == "__main__":
    main()
