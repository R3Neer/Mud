from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(p: str) -> str:
    return (ROOT / p).read_text(encoding='utf-8')


def write(p: str, text: str) -> None:
    (ROOT / p).write_text(text, encoding='utf-8', newline='\n')


def replace_once(p: str, old: str, new: str) -> None:
    text = read(p)
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{p}: expected one occurrence of {old!r}, got {n}')
    write(p, text.replace(old, new, 1))


def insert_before(p: str, marker: str, addition: str) -> None:
    text = read(p)
    if addition.strip() in text:
        return
    n = text.count(marker)
    if n != 1:
        raise SystemExit(f'{p}: marker count {n} for {marker!r}')
    write(p, text.replace(marker, addition + marker, 1))


# New decision D-089.
d89 = '''---
id: D-089
title: "Clasificación contextual de formas fuente sin dependencia circular del scanner"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions:
  - "Q-054"
  - "Q-055"
affects:
  - "scanner, formas de unidad, literales de magnitudes de punto, CST, parser, elaboración contextual y conformidad"
---
# ADR-089 — Clasificación contextual de formas fuente sin dependencia circular del scanner

- Modifica: [[ADR-062-literales-canonicos-de-magnitudes-de-punto|D-062]] y [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]].
- Cierra: [[notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos|Q-054]] y [[notas/preguntas/Q-055-literales-de-magnitudes-de-punto|Q-055]].

## Contexto

D-062 y D-076 permiten que información declarada por el propio programa participe en formas fuente: `~format` define la escritura canónica de una magnitud de punto y las unidades admiten identificador, nombre, plural, abreviatura y formas prefijadas. El scanner inicial no puede depender de esas declaraciones sin introducir un ciclo entre tokenización, parsing y resolución.

## Decisión

### Scanner base y clasificador contextual

El scanner base depende exclusivamente de Unicode, trivia y del catálogo léxico fijo de MUD. Produce un flujo sin pérdidas con offsets fuente, pero **no** consulta declaraciones `magnitude`, catálogos de unidades, `~format` ni tipos esperados.

`POINT_LITERAL` y `UNIT_FORM` son tokens contextuales, no producciones del scanner base. Un clasificador contextual puede añadir una alternativa de tokenización sobre un intervalo exacto del texto fuente cuando la resolución y el tipo esperado aporten la información requerida. La alternativa conserva el mismo `source_span`; no reconstruye la escritura concatenando tokens base.

Una implementación puede representar esta frontera como un token lattice, re-tokenización localizada, parser diferido o una estrategia equivalente. Es conforme si el scanner base es independiente del modelo y la clasificación contextual produce exactamente los mismos spans y resultados observables.

### Literales de punto

Cuando una posición de expresión posee un único tipo esperado que es una magnitud `point over` con `~format`, el clasificador intenta consumir desde el offset fuente una representación canónica completa de ese formato. Si coincide de forma exacta e invertible, produce un `POINT_LITERAL` que cubre todo el span reconocido, aunque ese mismo texto pudiera descomponerse en varios tokens base o formar una expresión ordinaria.

En ese contexto, la interpretación `POINT_LITERAL` tiene prioridad sobre la ruta de tokenización base para el mismo span. Sin un tipo esperado único no se crea esa alternativa contextual. La coincidencia debe terminar exactamente donde termina la representación canónica; no puede aceptar un prefijo de una forma más larga que el mismo formato pudiera consumir.

La obligación de invertibilidad de D-062 incluye por tanto la delimitación determinista de la representación completa. Un `~format` que no permita reconocer de forma unívoca el final de su propia forma canónica es inválido para una magnitud de punto.

### Formas de unidad

Las formas de unidad se clasifican después de conocer el catálogo semántico de magnitudes y unidades. El clasificador consulta el texto fuente directamente a partir de una posición en la que la gramática de cantidad admite una unidad. Puede producir `UNIT_FORM` para un identificador, `~name`, `~plural`, `~abbreviation` o forma prefijada habilitada.

Cuando existe un tipo o magnitud esperada, solo compiten las formas compatibles con ella. Sin tipo esperado, una forma únicamente es válida si el catálogo resuelto determina una unidad de manera unívoca. Dos candidatos semánticos distintos con la misma forma visible son ambiguos salvo cualificación admitida por la gramática.

Si varias formas compatibles comparten prefijo, se elige la coincidencia canónica completa más larga. Dos candidatos distintos que consumen exactamente el mismo span continúan siendo ambiguos; el orden de declaración no desempata. La clasificación contextual puede cubrir varios tokens base y no concede significado léxico nuevo a esa secuencia fuera de una posición de unidad.

La adyacencia `3m` se resuelve sobre el mismo offset inmediatamente posterior al número. La presencia o ausencia de trivia antes de una unidad no cambia la unidad seleccionada; el formateador conserva la normalización canónica de D-076.

### CST y AST

La CST sin pérdidas conserva los tokens base y el span fuente suficiente para reproducir la clasificación contextual. Una implementación puede materializar el token contextual en una vista derivada, pero nunca pierde los caracteres originales. El AST superficial conserva `PointLiteral(source_form)` y las formas de unidad ya clasificadas; no contiene una dependencia hacia el catálogo del scanner base.

## Consecuencias

- El scanner inicial deja de consultar información semántica futura.
- `~format` sigue definiendo una forma literal fuente directa, sin delimitador adicional obligatorio.
- Las colisiones entre una forma contextual y una expresión ordinaria se resuelven por contexto semántico, no por prioridad global del scanner.
- Las unidades pueden mantener formas Unicode o configuradas sin convertirlas en identificadores generales.
- La implementación puede ser multipaso, pero la tokenización base continúa siendo reproducible a partir del texto aislado.

## Verificación

1. El scanner base produce el mismo flujo antes y después de resolver declaraciones de magnitud.
2. `07:05:00` se clasifica como un único `POINT_LITERAL` cuando el tipo esperado selecciona su magnitud.
3. La misma secuencia sin tipo esperado único no recibe clasificación de punto.
4. Un formato que colisiona con una expresión ordinaria gana solo bajo el tipo de punto esperado.
5. Se rechaza un formato cuyo final no pueda reconocerse unívocamente.
6. Una forma de unidad única se resuelve sin tipo esperado y una colisión exige contexto o cualificación.
7. Coincidencias de unidad por prefijo usan la forma completa más larga sin depender del orden de declaración.
8. `3m` y `3 m` clasifican la misma unidad y el formateador produce la forma canónica espaciada.
9. CST y round-trip conservan exactamente el texto fuente anterior a la clasificación contextual.
'''
path = ROOT / 'notas/decisiones/ADR-089-clasificacion-contextual-de-formas-fuente.md'
if path.exists():
    raise SystemExit('D-089 already exists')
path.write_text(d89, encoding='utf-8', newline='\n')

# 06: add D-089 and describe two lexical views.
p = 'especificacion/06-lexico.md'
text = read(p)
text = text.replace('  - D-087\n---', '  - D-087\n  - D-089\n---', 1)
text = text.replace(
    'Este capítulo define cómo se transforma un flujo Unicode en tokens. La gramática normativa está en [[gramatica/mud-lexico.ebnf]]. La sintaxis que consume esos tokens pertenece a [[07-gramatica-concreta]].',
    'Este capítulo define el scanner base y la clasificación contextual de formas fuente. El scanner base transforma Unicode en tokens sin consultar el modelo; `POINT_LITERAL` y `UNIT_FORM` se añaden únicamente en una vista contextual posterior conforme a D-089. La gramática léxica base está en [[gramatica/mud-lexico.ebnf]]. La sintaxis que consume las vistas significativas pertenece a [[07-gramatica-concreta]].',
    1,
)
old_adj = 'Después de reconocer un literal numérico, el flujo significativo puede reconocer inmediatamente una forma de unidad habilitada, sin exigir trivia intermedia. Por ello `3m`, `90km/h` y `r0.1m` producen los mismos tokens significativos que sus formas espaciadas. Un identificador alfanumérico completo conserva prioridad fuera de esa frontera; `R2D2` y `ronto` no se dividen como número y unidad.\n\nLa forma canónica inserta un espacio entre número y primera unidad. Esta normalización pertenece al formateador, no al resaltador léxico.\n'
new_adj = 'El scanner base no necesita conocer unidades para reconocer la frontera posterior a un número. Cuando la gramática de cantidad admite una unidad, el clasificador contextual de D-089 consulta el texto fuente desde ese offset y puede cubrir una forma habilitada sin exigir trivia intermedia. Por ello `3m`, `90km/h` y `r0.1m` obtienen la misma clasificación semántica que sus formas espaciadas. Fuera de una posición de unidad, `R2D2`, `ronto` y cualquier secuencia semejante conservan exclusivamente su tokenización base.\n\nLa forma canónica inserta un espacio entre número y primera unidad. Esta normalización pertenece al formateador, no al scanner base ni al resaltador.\n'
if old_adj not in text:
    raise SystemExit('06 adjacency block not found')
text = text.replace(old_adj, new_adj, 1)
marker = '## Comentarios\n'
section = '''## Clasificación contextual de formas fuente\n\n> [!rule] MUD-LEX-012 — Independencia del scanner base\n> El scanner base solo depende del texto Unicode y del léxico fijo de MUD. No consulta declaraciones, tipos esperados, `~format` ni catálogos de unidad. Todos sus tokens y trivia conservan offsets exactos en el texto fuente.\n\n> [!rule] MUD-LEX-013 — Alternativa contextual por span\n> `POINT_LITERAL` y `UNIT_FORM` son clasificaciones contextuales sobre spans del texto original. El clasificador puede cubrir una o varias unidades del tokenizado base, pero debe conservar el intervalo fuente exacto y no puede fabricar caracteres al recomponer tokens.\n\n> [!rule] MUD-LEX-014 — Prioridad dirigida por contexto\n> Una alternativa contextual existe únicamente cuando su contexto semántico satisface el contrato de D-089. Cuando un único tipo de punto esperado reconoce exactamente su `~format`, `POINT_LITERAL` prevalece sobre una interpretación ordinaria del mismo span. Sin contexto suficiente, esa alternativa no existe.\n\n> [!rule] MUD-LEX-015 — Determinismo de unidad\n> `UNIT_FORM` usa el catálogo semántico ya resuelto. El tipo esperado restringe candidatos; sin él la forma debe ser globalmente unívoca. Entre coincidencias compatibles de distinta longitud gana la forma completa más larga; dos candidatos distintos para el mismo span son ambiguos.\n\nLa arquitectura concreta puede usar token lattice, re-tokenización localizada o parsing diferido. Esas estrategias no son observables siempre que reproduzcan las reglas anteriores y el round-trip de la CST.\n\n'''
if section.strip() not in text:
    if marker not in text:
        raise SystemExit('06 comments marker not found')
    text = text.replace(marker, section + marker, 1)
old_units = 'Las formas de unidad pueden contener Unicode y no son identificadores generales. Se reconocen contextualmente contra el catálogo construido a partir de las declaraciones `magnitude`.\n\n> [!warning]\n> [[notas/decisiones/ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]] fija el catálogo de prefijos, la resolución de colisiones y la identidad estable. `UNIT_FORM` conserva la escritura encontrada; la resolución semántica selecciona después una unidad declarada o una forma prefijada estructural.\n'
new_units = 'Las formas de unidad pueden contener Unicode y no son identificadores generales. El scanner base conserva su tokenización textual ordinaria; únicamente el clasificador contextual de D-089 puede superponer `UNIT_FORM` en una posición donde la sintaxis de cantidad admita una unidad.\n\n> [!warning]\n> [[notas/decisiones/ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]] fija el catálogo de prefijos y las formas habilitadas. D-089 fija su reconocimiento sin dependencia circular: `UNIT_FORM` conserva la escritura encontrada y se selecciona contra el catálogo semántico ya resuelto.\n'
if old_units not in text:
    raise SystemExit('06 unit intro not found')
text = text.replace(old_units, new_units, 1)
# Replace any stale point-form paragraph phrases conservatively.
text = text.replace('Una magnitud `point over` puede habilitar escrituras contextuales mediante su propiedad `format`', 'Una magnitud `point over` puede habilitar escrituras contextuales mediante su metadato `~format`')
text = text.replace('El scanner representa una coincidencia válida como `POINT_LITERAL`', 'El clasificador contextual representa una coincidencia válida como `POINT_LITERAL`')
write(p, text)

# Baseline lexical EBNF no longer defines semantic forms.
p = 'especificacion/gramatica/mud-lexico.ebnf'
text = read(p)
text = text.replace('      | point-form\n', '')
text = text.replace('      | unit-form\n', '')
unit_block = '(* UNIT_FORM es contextual y procede del catálogo de unidades ya resuelto. *)\nunit-form\n    ::= ? forma Unicode de unidad habilitada por una declaración magnitude ? ;\n\npoint-form\n    ::= ? forma canónica contextual de D-062 para el tipo de punto esperado ? ;\n\n'
if unit_block not in text:
    raise SystemExit('lexical contextual block not found')
text = text.replace(unit_block, '(* UNIT_FORM y POINT_LITERAL no son producciones del scanner base.\n   D-089 los define como clasificaciones contextuales sobre spans fuente. *)\n\n', 1)
write(p, text)

# D-062: contextual classifier, new provenance, Q-055 closed by D-089.
p = 'notas/decisiones/ADR-062-literales-canonicos-de-magnitudes-de-punto.md'
text = read(p)
text = text.replace('- Modificada por: [[ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]]', '- Modificada por: [[ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]] y [[ADR-089-clasificacion-contextual-de-formas-fuente|D-089]]', 1)
text = text.replace('- Responde parcialmente: [[notas/preguntas/Q-055-literales-de-magnitudes-de-punto|Q-055]]', '- Cerrada conjuntamente por esta decisión y [[ADR-089-clasificacion-contextual-de-formas-fuente|D-089]]: [[notas/preguntas/Q-055-literales-de-magnitudes-de-punto|Q-055]]', 1)
text = text.replace('El lexer conserva `POINT_LITERAL` como token contextual, pero el análisis requiere el tipo esperado y la declaración de magnitud resuelta.', '`POINT_LITERAL` es una clasificación contextual de D-089 sobre el span fuente; el scanner base no requiere el tipo esperado ni la declaración de magnitud resuelta.')
# Modern metadata spelling in the positive current decision.
text = text.replace('declara `format`', 'declara `~format`')
text = text.replace('su propiedad `format`', 'su metadato `~format`')
text = text.replace('sin `format`', 'sin `~format`')
text = text.replace('con `format`', 'con `~format`')
text = text.replace('    format = "{hour:2}:{minute:2}:{second:2}"', '    ~format = "{hour:2}:{minute:2}:{second:2}"')
write(p, text)

# D-076: provenance and explicit contextual classifier.
p = 'notas/decisiones/ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente.md'
text = read(p)
text = text.replace('[[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].', '[[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]] y [[ADR-089-clasificacion-contextual-de-formas-fuente|D-089]].', 1)
text = text.replace('- Responde parcialmente: [[notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos|Q-054]].', '- Cierra junto con D-089: [[notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos|Q-054]].', 1)
text = text.replace('El léxico acepta una unidad inmediatamente después del literal numérico:', 'El clasificador contextual de D-089 acepta una unidad inmediatamente después del literal numérico, sin exigir al scanner base conocer el catálogo:')
text = text.replace('El resaltador reconoce número y unidad como tokens distintos aun sin espacio.', 'La vista contextual reconoce número y unidad como tokens distintos aun sin espacio; el tokenizado base permanece independiente del catálogo.')
write(p, text)

# Close Q-054 and Q-055 with exact evidence.
q54 = '''---
id: Q-054
title: Catálogo y resolución léxica de unidades y prefijos
priority: P2
opened: 2026-07-29
resolved: true
closed: 2026-08-16
decisions:
  - D-076
  - D-089
affects:
  - especificacion/06-lexico.md
  - especificacion/gramatica/mud-lexico.ebnf
superseded-by: []
---

# Q-054 — Catálogo y resolución léxica de unidades y prefijos

## Pregunta

¿Cómo se reconocen las formas de unidad configuradas por declaraciones del propio programa sin hacer depender el scanner inicial de una magnitud ya parseada y resuelta, y qué colisiones léxicas son admisibles?

## Resolución

D-076 fija catálogo, formas habilitadas, prefijos y adyacencia. D-089 separa el scanner base del clasificador contextual: `UNIT_FORM` se crea únicamente sobre el texto fuente cuando el catálogo semántico ya está resuelto. El tipo esperado restringe candidatos; sin él se exige unicidad global, las coincidencias de distinta longitud usan la forma completa más larga y un mismo span con varios candidatos sigue siendo ambiguo.

## Criterio de cierre

- C1: el pipeline separa de forma explícita el reconocimiento inicial de la resolución contextual de formas de unidad.
- C2: toda forma fuente de unidad tiene una regla determinista de delimitación y desambiguación.
- C3: la norma exige conformidad para colisiones, contexto esperado y adyacencia.

## Evidencia de cierre

- C1: `D-089`, `MUD-LEX-012` y `MUD-LEX-013`.
- C2: `D-089` y `MUD-LEX-015`.
- C3: verificación de D-089 y reglas de adyacencia de D-076/06-léxico.
'''
write('notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos.md', q54)
q55 = '''---
id: Q-055
title: Literales de magnitudes de punto
priority: P2
opened: 2026-07-29
resolved: true
closed: 2026-08-16
decisions:
  - D-061
  - D-062
  - D-089
affects:
  - especificacion/06-lexico.md
  - especificacion/07-gramatica-concreta.md
  - especificacion/gramatica/mud-lexico.ebnf
superseded-by: []
---

# Q-055 — Literales de magnitudes de punto

## Pregunta

¿Cómo puede `~format` definir simultáneamente la representación canónica y una forma literal fuente directa sin exigir que el scanner inicial conozca ya el tipo esperado y la declaración de magnitud resuelta?

## Resolución

D-062 conserva la forma fuente directa, la canonicalidad, la inversión y el dominio. D-089 hace que el scanner base ignore `~format`; cuando una posición posee un único tipo de punto esperado, el clasificador contextual lee el span fuente original y puede producir `POINT_LITERAL` con prioridad sobre la tokenización ordinaria del mismo span. Sin tipo esperado único esa alternativa no existe.

La inversión estática incluye la capacidad de reconocer de forma determinista el final de la representación completa. Por ello no se necesita un delimitador nuevo y tampoco existe dependencia circular del scanner base.

## Criterio de cierre

- C1: el scanner inicial puede ejecutarse sin consultar declaraciones de magnitud.
- C2: una secuencia fuente se reclasifica reproduciblemente cuando el tipo esperado identifica una única magnitud de punto.
- C3: las colisiones con una interpretación ordinaria tienen una prioridad explícita.
- C4: los artefactos léxicos distinguen scanner base y clasificación contextual.

## Evidencia de cierre

- C1: `D-089` y `MUD-LEX-012`.
- C2: `D-062`, `D-089` y `MUD-LEX-013`.
- C3: `D-089` y `MUD-LEX-014`.
- C4: `especificacion/06-lexico.md` y `especificacion/gramatica/mud-lexico.ebnf`.
'''
write('notas/preguntas/Q-055-literales-de-magnitudes-de-punto.md', q55)

# Closed questions return to archive-only export profiles.
p = 'tooling/markdown_export/profiles.toml'
text = read(p)
for profile in ('language', 'current'):
    header = f'[profiles.{profile}]'
    pos = text.index(header)
    ex = text.index('exclude = [', pos)
    end = text.index(']\n', ex)
    block = text[ex:end]
    additions = []
    for q in (
        'notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos.md',
        'notas/preguntas/Q-055-literales-de-magnitudes-de-punto.md',
    ):
        if q not in block:
            additions.append(f'    "{q}",\n')
    if additions:
        text = text[:end] + ''.join(additions) + text[end:]
write(p, text)

print('GLOBAL_COHERENCE_PHASE2_LEXICAL_OK')
