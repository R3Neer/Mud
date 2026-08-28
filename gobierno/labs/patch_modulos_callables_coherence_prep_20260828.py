from pathlib import Path

path = Path.cwd() / "notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md"
old = """7. Un único `start with` global.
8. Independencia respecto del orden de su lista.
9. Rechazo de coma final.
10. Rechazo de referencias duplicadas o no activables.
11. Estado inicial vacío cuando se omite la declaración.
12. Estabilización inicial antes de aceptar acciones externas.
13. Uso ordinario de `start` y `abstract` como identificadores fuera de sus contextos especiales.
14. Tratamiento contextual de `always`, `name`, `prefixes` y etiquetas equivalentes.
15. Sustitución del conjunto global por el `start with` local de cada test.
16. Disparo durante la estabilización inicial de un `when` cuya condición comienza verdadera."""
new = """7. Como máximo un `start with` por módulo y ausencia válida de contribución en un módulo.
8. Independencia del orden y deduplicación dentro del conjunto unificado de contribuciones.
9. Admisión de contribución directa, bloque unificado y coma final opcional.
10. Rechazo de declaraciones no activables, activación de otro módulo y colecciones anidadas.
11. Proyecto cuyos módulos omiten `start with`, equivalente a una contribución inicial vacía.
12. Materialización conjunta de las contribuciones de todos los módulos y estabilización previa a acciones externas.
13. `Thing` siempre efectiva y no activable.
14. Reutilización exacta de estado tras `destroy` y nueva activación.
15. Unión de contribuciones `start with` del cierre transitivo estático de tests alcanzables.
16. Disparo durante la estabilización inicial de un `when` cuya condición comienza verdadera."""
text = path.read_text(encoding="utf-8")
if new not in text:
    if old not in text:
        raise SystemExit("D-054: bloque real de verificación no encontrado")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("D-054 verification coherence prepared")
