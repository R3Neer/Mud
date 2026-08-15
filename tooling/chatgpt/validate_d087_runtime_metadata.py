from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()


def read(rel):
    return (root / rel).read_text(encoding="utf-8")


def need(rel, needle):
    if needle not in read(rel):
        raise SystemExit(f"MISSING {needle!r} in {rel}")


def forbid(rel, needle):
    if needle in read(rel):
        raise SystemExit(f"STALE {needle!r} in {rel}")


readme = "especificacion/README.md"
forbid(readme, "reglas de escritura de `~name`")
need(readme, "todo acceso `~` es de solo lectura durante la ejecución")

model = "especificacion/04-modelo-matematico.md"
need(model, "  - D-087")
forbid(model, "puede escribirse o modificarse únicamente donde su contrato de metadatos lo permita")
need(model, "ningún acceso `~` puede ser destino de una asignación o actualización runtime")
need(model, "Todo acceso `~` es de solo lectura durante la ejecución")
need(model, "ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087")

d85 = "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md"
forbid(d85, "`~name` es mutable para `thing`")
forbid(d85, 'Nora~name = "Nora la Roja"')
need(d85, "D-087 sustituye la mutabilidad runtime")
need(d85, "Ninguna propiedad `~` puede aparecer como destino de una asignación o actualización runtime")
need(d85, "Todo acceso `~` es runtime-readonly")
need(d85, "solo lectura runtime de todo acceso `~`")

print("D087_RUNTIME_METADATA_INVARIANTS_OK")
