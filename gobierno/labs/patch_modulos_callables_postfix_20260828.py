from pathlib import Path

ROOT = Path.cwd()

BLOCKS = {
    "notas/preguntas/Q-051-identidad-y-seleccion-de-un-look.md": """
## Criterio de cierre

- C1: fijar cómo se suministran participantes y parámetros de un `look`.
- C2: fijar la cardinalidad conceptual del resultado de una llamada.
- C3: fijar la vista de lectura usada por la consulta.

## Evidencia de cierre

- C1: D-096 define `look` como callable puro con `for` y `given`.
- C2: D-096 define una llamada como exactamente un objeto resultado anónimo; la multiplicidad se expresa en sus campos.
- C3: D-096 define la vista heredada del llamador: estable desde host, instantánea de rule o delta privado visible desde `then`.
""",
    "notas/preguntas/Q-052-entrega-de-message.md": """
## Criterio de cierre

- C1: fijar multiplicidad, deduplicación y orden causal de ocurrencias.
- C2: fijar el momento de evaluación de `when`, `if` y payload.
- C3: fijar el comportamiento exterior ante commit y rollback.

## Evidencia de cierre

- C1: D-096 modela ocurrencias causales con identidad propia, conserva multiplicidad y las propaga por ondas sin deduplicación por payload.
- C2: D-096 evalúa `when` e `if` en la vista causal y distingue proyección causal interna de proyección final exterior.
- C3: D-096 entrega al host solo después de commit y cancela toda entrega exterior si la resolución revierte; el borde de participantes inexistentes se separa en Q-067.
""",
}

for rel, block in BLOCKS.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if "## Criterio de cierre" not in text:
        path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")

print("question closure evidence applied")
