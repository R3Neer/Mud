from pathlib import Path

path = Path.cwd() / "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md"
text = path.read_text(encoding="utf-8")
legacy = "~private      : Bool = false\n"
count = text.count(legacy)
if count == 1:
    path.write_text(text.replace(legacy, "", 1), encoding="utf-8")
elif count == 0:
    pass
else:
    raise SystemExit(f"D-087: se esperaban como máximo 1 líneas legacy de ~private y hay {count}")
print("D-087 legacy ~private removed")
