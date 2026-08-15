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


rel = "notas/preguntas/Q-029-terminacion.md"
t = read(rel)
old = '''---
id: Q-029
title: Terminación
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-047
  - D-088
affects: []
superseded-by: []
---

# Q-029 — Terminación

## Contenido

Qué clases de acciones y reglas puede certificar el compilador.

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita|D-047]] y [[notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]. Una iteración exhaustiva solo es válida sobre una fuente cuya finitud y enumerabilidad puedan demostrarse; una progresión posee paso fijo por ejecución y los dominios cíclicos se limitan a un periodo fundamental. Permanece abierta la certificación general de terminación de actions, reglas y composiciones más amplias.
'''
new = '''---
id: Q-029
title: Terminación
priority: P2
opened: 2026-07-29
resolved: false
closed:
decisions: []
affects: []
superseded-by: []
---

# Q-029 — Terminación

## Contenido

Qué clases de acciones y reglas puede certificar el compilador.
'''
t = exact(t, old, new, "Q029 restore open scope")
write(rel, t)
print("D088_POSTPUBLISH_Q029_OK")
