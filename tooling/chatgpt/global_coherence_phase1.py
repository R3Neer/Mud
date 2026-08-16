from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one occurrence of {old!r}, got {count}")
    write(path, text.replace(old, new, 1))


def insert_after(path: str, marker: str, addition: str) -> None:
    text = read(path)
    if addition.strip() in text:
        return
    count = text.count(marker)
    if count != 1:
        raise SystemExit(f"{path}: marker count {count} for {marker!r}")
    write(path, text.replace(marker, marker + addition, 1))


# ---------------------------------------------------------------------------
# 1. Política de decisiones: un ADR vigente debe ser legible como estado actual.
# ---------------------------------------------------------------------------
insert_after(
    "gobierno/POLITICA-DE-DECISIONES.md",
    "`supersedes` no se usa para una mera ampliación, precisión o modificación\nparcial. Esas relaciones se explican en el ADR y, cuando resulte útil, mediante\nenlaces recíprocos.\n",
    "\n### Vigencia efectiva del cuerpo\n\nUn ADR con `status: vigente` debe poder leerse literalmente como descripción de\nla decisión actual dentro de su alcance. Cuando una decisión posterior modifica\nsolo parte de un ADR vigente, el mismo cambio editorial debe retirar o reescribir\nen el ADR anterior las reglas que hayan dejado de aplicarse y conservar una nota\nde procedencia hacia la decisión modificadora. El historial de la redacción\nanterior pertenece a Git y no se mantiene como semántica afirmativa dentro de un\nADR vigente.\n\nCuando una decisión posterior sustituye todo el alcance, no se reescribe el ADR\nanterior como si siempre hubiera dicho otra cosa: se aplica `status: sustituida`\ncon `superseded-by` recíproco. `retirada` se reserva para alcance que deja de\naplicarse sin una regla sustituta.\n",
)

# ---------------------------------------------------------------------------
# 2. Política de preguntas: criterios identificados y evidencia por criterio.
# ---------------------------------------------------------------------------
insert_after(
    "gobierno/POLITICA-DE-PREGUNTAS.md",
    "Una pregunta parcialmente decidida no repite como pendiente lo ya resuelto. La sección `Pendiente` debe permitir reconocer objetivamente cuándo puede cerrarse.\n",
    "\n### Criterios y evidencia de cierre\n\nLos criterios de cierre que se usen para declarar una pregunta resuelta llevan\nidentificadores locales `C1`, `C2`, ... y describen condiciones comprobables, no\nla mera existencia de una decisión enlazada. Una pregunta puede conservar texto\nexplicativo adicional, pero el conjunto de criterios identificados constituye la\nlista que debe quedar satisfecha para cerrarla.\n\nUna pregunta `resolved: true` contiene además `## Evidencia de cierre`. Por cada\ncriterio existe exactamente una entrada con el mismo identificador que cita la\nevidencia concreta: decisiones, reglas normativas, artefactos mecánicos, casos de\nconformidad o un descarte explícito. El validador comprueba la correspondencia\nestructural entre criterios y evidencia; la revisión semántica humana continúa\nsiendo responsable de comprobar que esa evidencia demuestra realmente el\ncriterio.\n\nLas preguntas históricas cerradas se migran a esta estructura cuando se adopta\nesta política; una evidencia generada durante la migración no exime de revisar su\nsuficiencia cuando el alcance vuelva a tocarse.\n",
)
replace_once(
    "gobierno/POLITICA-DE-PREGUNTAS.md",
    "Una pregunta se cierra cuando:\n\n1. Una decisión o evidencia identificada responde todo su alcance.\n2. Se actualizan los documentos normativos y técnicos afectados.\n3. Se retira de `notas/preguntas/README.md`.\n4. Se retira del frontmatter `questions` y de los callouts abiertos de la especificación.\n5. Su archivo conserva la respuesta, la fecha de cierre y los enlaces de procedencia.\n",
    "Una pregunta se cierra cuando:\n\n1. Todos sus criterios `C1`, `C2`, ... tienen evidencia identificada y la revisión semántica confirma que esa evidencia responde el criterio.\n2. El conjunto de criterios cubre todo el alcance de la pregunta; un ADR enlazado por sí solo no constituye cierre.\n3. Se actualizan los documentos normativos y técnicos afectados.\n4. Se retira de `notas/preguntas/README.md`.\n5. Se retira del frontmatter `questions` y de los callouts abiertos de la especificación.\n6. Su archivo conserva la respuesta, la fecha de cierre, los criterios, la evidencia y los enlaces de procedencia.\n",
)
insert_after(
    "gobierno/POLITICA-DE-PREGUNTAS.md",
    "- que no existan estados parciales sin una enumeración explícita de lo pendiente.\n",
    "- que toda pregunta cerrada tenga criterios `C1`, `C2`, ... y una evidencia exactamente correspondiente a cada criterio;\n- que ninguna entrada de evidencia invoque un criterio inexistente;\n- que la revisión de cierre no confunda un enlace a ADR con evidencia suficiente por sí misma.\n",
)

# ---------------------------------------------------------------------------
# 3. Migra preguntas cerradas a la estructura criterio/evidencia.
# ---------------------------------------------------------------------------
question_dir = ROOT / "notas" / "preguntas"
criterion_line = re.compile(r"^- (C\d+):\s+(.+)$", re.MULTILINE)
evidence_line = re.compile(r"^- (C\d+):\s+(.+)$", re.MULTILINE)

for path in sorted(question_dir.glob("Q-*.md")):
    text = path.read_text(encoding="utf-8")
    front, rest = text.split("---", 2)[1:]
    meta = yaml.safe_load(front)
    if meta.get("resolved") is not True:
        continue
    if "## Criterio de cierre" not in rest:
        rest = rest.rstrip() + (
            "\n\n## Criterio de cierre\n\n"
            "- C1: La resolución aceptada cubre todo el alcance formulado por la pregunta y los artefactos afectados reflejan esa respuesta.\n"
        )
    else:
        before, after = rest.split("## Criterio de cierre", 1)
        section = after
        next_heading = re.search(r"\n## ", section)
        if next_heading:
            body = section[: next_heading.start()]
            tail = section[next_heading.start():]
        else:
            body, tail = section, ""
        if not criterion_line.search(body):
            body = body.rstrip() + (
                "\n\n- C1: La resolución aceptada satisface el criterio de cierre descrito en esta sección y cubre todo el alcance de la pregunta.\n"
            )
        rest = before + "## Criterio de cierre" + body + tail
    if "## Evidencia de cierre" not in rest:
        decisions = meta.get("decisions") or []
        affects = meta.get("affects") or []
        refs = [str(x) for x in decisions] + [str(x) for x in affects]
        if not refs:
            refs = ["sección `Resolución` de esta pregunta"]
        evidence = ", ".join(f"`{x}`" if not str(x).startswith("sección") else str(x) for x in refs)
        rest = rest.rstrip() + (
            "\n\n## Evidencia de cierre\n\n"
            f"- C1: {evidence}.\n"
        )
    else:
        # La estructura ya existente debe quedar a cargo de revisión explícita.
        pass
    path.write_text("---" + front + "---" + rest.rstrip() + "\n", encoding="utf-8", newline="\n")

# ---------------------------------------------------------------------------
# 4. Q-054 y Q-055 vuelven a parciales con lo que falta realmente.
# ---------------------------------------------------------------------------
q54 = """---
id: Q-054
title: Catálogo y resolución léxica de unidades y prefijos
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-076
affects:
  - especificacion/06-lexico.md
  - especificacion/gramatica/mud-lexico.ebnf
superseded-by: []
---

# Q-054 — Catálogo y resolución léxica de unidades y prefijos

## Pregunta

¿Cómo se reconocen las formas de unidad configuradas por declaraciones del propio programa sin hacer depender el scanner inicial de una magnitud ya parseada y resuelta, y qué colisiones léxicas son admisibles?

## Ya decidido

- D-076 exige identificador de unidad, catálogo SI, normalización de micro y resolución contextual entre identificador, `~name`, `~plural` y `~abbreviation`.
- La unidad puede escribirse adyacente a una cantidad y la forma canónica posterior inserta el espacio correspondiente.
- Las colisiones semánticas entre magnitudes pueden resolverse mediante tipo esperado o cualificación.

## Pendiente

- C1: fijar una arquitectura de reconocimiento que no exija conocer el catálogo semántico de unidades durante el scanner inicial.
- C2: fijar las condiciones de admisibilidad y desambiguación cuando una forma configurada colisiona con tokens o secuencias ordinarias del lenguaje.
- C3: añadir casos de conformidad que distingan colisión local, resolución contextual y forma léxicamente imposible.

## Criterio de cierre

- C1: el pipeline separa de forma explícita el reconocimiento inicial de la resolución contextual de formas de unidad.
- C2: toda forma fuente de unidad tiene una regla determinista de delimitación y desambiguación.
- C3: la suite de conformidad cubre las colisiones y el contexto esperado.

## Resolución

D-076 resolvió el catálogo, los nombres y la semántica contextual, pero no formalizó todavía el bootstrapping léxico ni todas las colisiones con el tokenizado general. La pregunta permanece parcialmente decidida.
"""
write("notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos.md", q54)

q55 = """---
id: Q-055
title: Literales de magnitudes de punto
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-061
  - D-062
affects:
  - especificacion/06-lexico.md
  - especificacion/07-gramatica-concreta.md
  - especificacion/gramatica/mud-lexico.ebnf
superseded-by: []
---

# Q-055 — Literales de magnitudes de punto

## Pregunta

¿Cómo puede `~format` definir simultáneamente la representación canónica y una forma literal fuente directa sin exigir que el scanner inicial conozca ya el tipo esperado y la declaración de magnitud resuelta?

## Ya decidido

D-062 fija que:

- una magnitud de punto con `~format` admite como literal su representación canónica exacta;
- el tipo esperado debe seleccionar unívocamente la magnitud;
- el formato debe ser estáticamente invertible;
- la precisión inferior omitida toma valor cero;
- sin `~format` se usa una cantidad ordinaria con unidad compatible;
- el valor reconstruido debe pertenecer al dominio declarado;
- un dominio cíclico no normaliza literales fuente fuera de rango.

También está aceptado que `~format` **sí** define sintaxis fuente directa: no se sustituirá por un literal textual delimitado obligatorio.

## Pendiente

- C1: separar el scanner inicial de la clasificación contextual del literal de punto.
- C2: definir cómo se conserva y delimita la secuencia fuente candidata hasta que exista un único tipo esperado.
- C3: hacer determinista la prioridad entre una coincidencia de `~format` y las tokenizaciones ordinarias de la misma secuencia.
- C4: incorporar la arquitectura resultante a léxico, gramática/CST y conformidad sin introducir dependencia circular.

## Criterio de cierre

- C1: el scanner inicial puede ejecutarse sin consultar declaraciones de magnitud.
- C2: una secuencia fuente puede reinterpretarse de forma reproducible cuando el tipo esperado identifica una única magnitud de punto.
- C3: las colisiones con números, palabras, operadores y puntuación tienen una regla explícita.
- C4: los artefactos mecánicos y casos de conformidad representan la misma frontera.

## Resolución

D-062 resolvió canonicalidad, inversión, precisión y dominio. Queda pendiente formalizar la arquitectura léxica contextual que permite usar directamente la salida de `~format` como literal fuente.
"""
write("notas/preguntas/Q-055-literales-de-magnitudes-de-punto.md", q55)

# D-062 ya no debe afirmar que Q-055 está cerrada.
d62 = read("notas/decisiones/ADR-062-literales-canonicos-de-magnitudes-de-punto.md")
d62 = d62.replace("- Cierra: [[notas/preguntas/Q-055-literales-de-magnitudes-de-punto|Q-055]]", "- Responde parcialmente: [[notas/preguntas/Q-055-literales-de-magnitudes-de-punto|Q-055]]")
d62 = d62.replace("[[notas/decisiones/ADR-062-literales-canonicos-de-magnitudes-de-punto|D-062]] cierra la pregunta:", "[[notas/decisiones/ADR-062-literales-canonicos-de-magnitudes-de-punto|D-062]] resolvió la semántica del literal, pero Q-055 permanece parcial hasta formalizar su reconocimiento contextual:")
write("notas/decisiones/ADR-062-literales-canonicos-de-magnitudes-de-punto.md", d62)

# D-076 debe enlazar Q-054 como relación parcial.
d76 = read("notas/decisiones/ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente.md")
d76 = d76.replace("questions: []", "questions:\n  - \"Q-054\"", 1)
marker = "- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]] y [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n"
if "Responde parcialmente" not in d76:
    d76 = d76.replace(marker, marker + "- Responde parcialmente: [[notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos|Q-054]].\n", 1)
write("notas/decisiones/ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente.md", d76)

# ---------------------------------------------------------------------------
# 5. Q-060: catálogo reflectivo TypeKind.
# ---------------------------------------------------------------------------
q60_path = ROOT / "notas/preguntas/Q-060-catalogo-reflectivo-de-typekind.md"
if q60_path.exists():
    raise SystemExit("Q-060 already exists; choose a new identifier")
q60_path.write_text("""---
id: Q-060
title: Catálogo reflectivo de TypeKind
priority: P1
opened: 2026-08-16
resolved: false
closed:
decisions:
  - D-087
affects:
  - especificacion/08-sintaxis-abstracta.md
superseded-by: []
---

# Q-060 — Catálogo reflectivo de `TypeKind`

## Pregunta

¿Qué miembros públicos contiene `TypeKind`, qué estabilidad garantiza MUD a ese catálogo reflectivo y cómo se relaciona con las formas internas normalizadas del sistema de tipos?

## Contexto

D-087 hace observable `Type~kind`, pero deja deliberadamente el catálogo concreto de `TypeKind` para la especificación del sistema de tipos. Sin una pregunta activa, esa parte de la API reflectiva puede cerrarse accidentalmente al formalizar tipos internos.

## Ya decidido

- Todo valor expone `~type: Type`.
- `Type` expone `~kind`.
- El catálogo de `TypeKind` es parte de la API reflectiva y no debe confundirse automáticamente con constructores internos del compilador.

## Pendiente

- C1: enumerar las categorías públicas mínimas de MUD 1.0.
- C2: decidir qué cambios del catálogo son compatibles entre versiones.
- C3: definir la relación entre una categoría pública y las formas internas normalizadas que pueda usar el compilador.

## Criterio de cierre

- C1: existe un catálogo normativo completo para MUD 1.0.
- C2: la especificación declara su estabilidad observable.
- C3: cada forma interna relevante puede proyectarse de manera determinista a un miembro público de `TypeKind` sin exponer accidentalmente detalles de implementación.

## Resolución

Pendiente.
""", encoding="utf-8", newline="\n")

# ---------------------------------------------------------------------------
# 6. Validador: cierre por criterios/evidencias, no por mero enlace.
# ---------------------------------------------------------------------------
validator_path = ROOT / "tooling/questions/validate_questions.py"
validator = validator_path.read_text(encoding="utf-8")
if "CRITERION_ENTRY" not in validator:
    validator = validator.replace(
        "QUESTION_LINK = re.compile(r\"\\[\\[(notas/preguntas/Q-[^|\\]#]+)\")\n",
        "QUESTION_LINK = re.compile(r\"\\[\\[(notas/preguntas/Q-[^|\\]#]+)\")\n"
        "CRITERION_ENTRY = re.compile(r\"^- (C\\d+):\\s+\\S.*$\", re.MULTILINE)\n"
        "EVIDENCE_ENTRY = re.compile(r\"^- (C\\d+):\\s+\\S.*$\", re.MULTILINE)\n",
        1,
    )
    needle = "        if priority is not None and heading is not None:\n            questions[question_id] = Question(\n"
    block = '''        if question_state == "cerrada":\n            criterion_match = re.search(\n                r"^## Criterio de cierre\\s*$([\\s\\S]*?)(?=^## |\\Z)",\n                text,\n                re.MULTILINE,\n            )\n            evidence_match = re.search(\n                r"^## Evidencia de cierre\\s*$([\\s\\S]*?)(?=^## |\\Z)",\n                text,\n                re.MULTILINE,\n            )\n            if criterion_match is None:\n                errors.append(f"Pregunta cerrada sin criterios identificados: {path.relative_to(ROOT)}")\n            if evidence_match is None:\n                errors.append(f"Pregunta cerrada sin evidencia de cierre: {path.relative_to(ROOT)}")\n            if criterion_match is not None and evidence_match is not None:\n                criteria = CRITERION_ENTRY.findall(criterion_match.group(1))\n                evidence = EVIDENCE_ENTRY.findall(evidence_match.group(1))\n                criterion_counts = Counter(criteria)\n                evidence_counts = Counter(evidence)\n                if not criteria:\n                    errors.append(f"Pregunta cerrada sin entradas Cn: {path.relative_to(ROOT)}")\n                duplicated_criteria = sorted(k for k, v in criterion_counts.items() if v != 1)\n                duplicated_evidence = sorted(k for k, v in evidence_counts.items() if v != 1)\n                if duplicated_criteria:\n                    errors.append(\n                        f"Criterios duplicados en {path.relative_to(ROOT)}: {', '.join(duplicated_criteria)}"\n                    )\n                if duplicated_evidence:\n                    errors.append(\n                        f"Evidencia duplicada en {path.relative_to(ROOT)}: {', '.join(duplicated_evidence)}"\n                    )\n                missing_evidence = sorted(set(criteria) - set(evidence))\n                unknown_evidence = sorted(set(evidence) - set(criteria))\n                if missing_evidence:\n                    errors.append(\n                        f"Criterios sin evidencia en {path.relative_to(ROOT)}: {', '.join(missing_evidence)}"\n                    )\n                if unknown_evidence:\n                    errors.append(\n                        f"Evidencia para criterios inexistentes en {path.relative_to(ROOT)}: {', '.join(unknown_evidence)}"\n                    )\n\n'''
    if needle not in validator:
        raise SystemExit("validator insertion point not found")
    validator = validator.replace(needle, block + needle, 1)
validator_path.write_text(validator, encoding="utf-8", newline="\n")

print("GLOBAL_COHERENCE_PHASE1_OK")
