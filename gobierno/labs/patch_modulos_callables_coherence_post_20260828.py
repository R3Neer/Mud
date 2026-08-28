from pathlib import Path

path = Path.cwd() / "notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md"
old = "16. Navegación LSP desde cada activación a una única definición."
new = "16. Disparo durante la estabilización inicial de un `when` cuya condición comienza verdadera.\n17. Navegación LSP desde cada activación a una única definición."
text = path.read_text(encoding="utf-8")
if new not in text:
    if old not in text:
        raise SystemExit("D-054: cierre de verificación esperado no encontrado")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("D-054 verification evidence preserved")
