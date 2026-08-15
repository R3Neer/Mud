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


# D-088: Q-018 only blocks concrete discontinuous-interval verification.
rel = "notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md"
t = read(rel)
t = exact(
    t,
    "Se verifican fuentes enumerables de todas las clases admitidas, `:` con cuerpo breve y con llaves, filtro breve y con locales, pasos positivos/negativos/runtime, evaluación única del paso, cero estático/runtime, límites abiertos/cerrados, intervalos vacíos/infinitos, dominios escalonados firmados y `all`, `Num`, rechazo de progresión `Rum`, colección explícita de `Rum`, selección y los seis cuantificadores con `by` y bloque, magnitudes con unidades compatibles y diferencia entre filtro ordenado/no ordenado. La verificación concreta de intervalos discontinuos y del periodo fundamental cíclico se completa cuando Q-018 cierre la forma fuente consolidada necesaria para expresarlos sin ambigüedad; su semántica queda fijada por esta decisión.",
    "Se verifican fuentes enumerables de todas las clases admitidas, `:` con cuerpo breve y con llaves, filtro breve y con locales, pasos positivos/negativos/runtime, evaluación única del paso, cero estático/runtime, límites abiertos/cerrados, intervalos vacíos/infinitos, dominios escalonados firmados y `all`, `Num`, rechazo de progresión `Rum`, colección explícita de `Rum`, selección y los seis cuantificadores con `by` y bloque, magnitudes con unidades compatibles y diferencia entre filtro ordenado/no ordenado. La verificación concreta de intervalos discontinuos se completa cuando Q-018 cierre su forma fuente consolidada; su semántica queda fijada por esta decisión. El requisito de recorrer como máximo un periodo fundamental de un dominio cíclico pertenece a la verificación de D-082 y no depende de Q-018.",
    "D088 verification scope",
)
write(rel, t)


# D-082: D-088 adds an explicit conformance obligation.
rel = "notas/decisiones/ADR-082-cycle-como-modificador-de-dominio-de-punto.md"
t = read(rel)
t = exact(
    t,
    "5. Conservación de las formas de cardinalidad `[1]`, `[1..3]` y `[1..3 mut]`.\n\n## Modificación por D-088",
    "5. Conservación de las formas de cardinalidad `[1]`, `[1..3]` y `[1..3 mut]`.\n6. Una progresión sobre un dominio cíclico de punto visita como máximo un periodo fundamental y nunca se envuelve indefinidamente.\n\n## Modificación por D-088",
    "D082 verification",
)
write(rel, t)


# Q-029: D-047 and D-088 partially decide structural termination of finite iteration,
# while general certification of actions/rules remains open.
rel = "notas/preguntas/Q-029-terminacion.md"
t = read(rel)
t = exact(t, "resolved: false", "resolved:", "Q029 partial status")
t = exact(t, "decisions: []", "decisions:\n  - D-047\n  - D-088", "Q029 decisions")
t = exact(
    t,
    "Qué clases de acciones y reglas puede certificar el compilador.",
    "Qué clases de acciones y reglas puede certificar el compilador.\n\nEstado: **parcialmente decidida** mediante [[notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita|D-047]] y [[notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]. Una iteración exhaustiva solo es válida sobre una fuente cuya finitud y enumerabilidad puedan demostrarse; una progresión posee paso fijo por ejecución y los dominios cíclicos se limitan a un periodo fundamental. Permanece abierta la certificación general de terminación de actions, reglas y composiciones más amplias.",
    "Q029 content",
)
write(rel, t)


# Postconditions.
if "intervalos discontinuos y del periodo fundamental cíclico" in read("notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md"):
    raise SystemExit("D088 still ties cyclic verification to Q018")
if "6. Una progresión sobre un dominio cíclico" not in read("notas/decisiones/ADR-082-cycle-como-modificador-de-dominio-de-punto.md"):
    raise SystemExit("D082 cyclic verification missing")
q29 = read("notas/preguntas/Q-029-terminacion.md")
for needle in ("  - D-047", "  - D-088", "Estado: **parcialmente decidida**", "Permanece abierta la certificación general"):
    if needle not in q29:
        raise SystemExit(f"Q029 missing {needle!r}")

print("D088_FIX_V7_OK")
