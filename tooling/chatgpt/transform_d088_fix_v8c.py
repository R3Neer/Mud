from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()


def read(rel):
    return (root / rel).read_text(encoding="utf-8")


def write(rel, text):
    (root / rel).write_text(text.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def exact(text, old, new, label, count=1):
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"{label}: expected {count}, found {actual}")
    return text.replace(old, new, count)


# D-088: Q-018 blocks concrete discontinuous-interval syntax, not the already
# decided single-period traversal rule for cyclic point domains.
rel = "notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md"
t = read(rel)
t = exact(
    t,
    "Se verifican fuentes enumerables de todas las clases admitidas, `:` con cuerpo breve y con llaves, filtro breve y con locales, pasos positivos/negativos/runtime, evaluación única del paso, cero estático/runtime, límites abiertos/cerrados, intervalos vacíos/infinitos, dominios escalonados firmados y `all`, `Num`, rechazo de progresión `Rum`, colección explícita de `Rum`, selección y los seis cuantificadores con `by` y bloque, magnitudes con unidades compatibles y diferencia entre filtro ordenado/no ordenado. La verificación concreta de intervalos discontinuos y del periodo fundamental cíclico se completa cuando Q-018 cierre la forma fuente consolidada necesaria para expresarlos sin ambigüedad; su semántica queda fijada por esta decisión.",
    "Se verifican fuentes enumerables de todas las clases admitidas, `:` con cuerpo breve y con llaves, filtro breve y con locales, pasos positivos/negativos/runtime, evaluación única del paso, cero estático/runtime, límites abiertos/cerrados, intervalos vacíos/infinitos, dominios escalonados firmados y `all`, `Num`, rechazo de progresión `Rum`, colección explícita de `Rum`, selección y los seis cuantificadores con `by` y bloque, magnitudes con unidades compatibles y diferencia entre filtro ordenado/no ordenado. La verificación concreta de intervalos discontinuos se completa cuando Q-018 cierre su forma fuente consolidada; su semántica queda fijada por esta decisión. El requisito de recorrer como máximo un periodo fundamental de un dominio cíclico pertenece a la verificación de D-082 y no depende de Q-018.",
    "D088 verification scope",
)
write(rel, t)


# D-082 owns the conformance obligation for cyclic traversal.
rel = "notas/decisiones/ADR-082-cycle-como-modificador-de-dominio-de-punto.md"
t = read(rel)
t = exact(
    t,
    "5. Conservación de las formas de cardinalidad `[1]`, `[1..3]` y `[1..3 mut]`.\n\n## Modificación por D-088",
    "5. Conservación de las formas de cardinalidad `[1]`, `[1..3]` y `[1..3 mut]`.\n6. Una progresión sobre un dominio cíclico de punto visita como máximo un periodo fundamental y nunca se envuelve indefinidamente.\n\n## Modificación por D-088",
    "D082 cyclic verification",
)
write(rel, t)


# Q-029 deliberately remains open. D-088 establishes termination for this
# finite-iteration construct but does not decide general action/rule certification.
q29 = read("notas/preguntas/Q-029-terminacion.md")
for needle in ("resolved: false", "decisions: []", "Qué clases de acciones y reglas puede certificar el compilador."):
    if needle not in q29:
        raise SystemExit(f"Q029 state unexpectedly changed: missing {needle!r}")
if "D-088" in q29 or "D-047" in q29 or "parcialmente decidida" in q29:
    raise SystemExit("Q029 was incorrectly promoted to partially decided")

# Postconditions.
d88 = read("notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md")
if "intervalos discontinuos y del periodo fundamental cíclico" in d88:
    raise SystemExit("D088 still ties cyclic verification to Q018")
if "El requisito de recorrer como máximo un periodo fundamental de un dominio cíclico pertenece a la verificación de D-082" not in d88:
    raise SystemExit("D088 cyclic verification ownership missing")

d82 = read("notas/decisiones/ADR-082-cycle-como-modificador-de-dominio-de-punto.md")
if "6. Una progresión sobre un dominio cíclico de punto visita como máximo un periodo fundamental" not in d82:
    raise SystemExit("D082 cyclic conformance item missing")

print("D088_FIX_V8C_OK")
