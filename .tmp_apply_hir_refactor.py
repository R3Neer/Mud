from __future__ import annotations

from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: esperaba 1 ocurrencia y encontré {count}: {old[:100]!r}")
    write(path, text.replace(old, new, 1))


def replace_regex_once(path: str, pattern: str, replacement: str) -> None:
    text = read(path)
    new, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{path}: regex esperaba 1 ocurrencia y encontró {count}: {pattern}")
    write(path, new)


D097 = '''---
id: D-097
title: "HIR nominal vigente e IR semántico diferido"
status: vigente
date: 2026-08-28
supersedes: []
superseded-by: []
questions: []
affects:
  - "pipeline, resolución nominal, HIR nominal, tipado, elaboración, futura representación semántica, capítulo 09, validadores y artefactos mecánicos"
---

# ADR-097 — HIR nominal vigente e IR semántico diferido

- Modifica: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]], [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]] y [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].
- Precisa la frontera de fases usada por [[ADR-092-disponibilidad-estatica-de-propiedades-reflectivas|D-092]].

## Contexto

La arquitectura de MUD distingue correctamente el AST superficial, la resolución nominal y las fases posteriores de tipado y elaboración. Sin embargo, el repositorio había fijado un esquema ASDL detallado para la salida semántica posterior antes de disponer de una especificación desarrollada del sistema de tipos y de la elaboración que deberían producirla. Eso convertía decisiones todavía futuras sobre representación interna en un contrato normativo prematuro.

La resolución nominal sí está suficientemente delimitada: nombres, scopes, símbolos, bindings, anclas y las relaciones nominales de propiedad, especialización y referencia pueden definirse sin resolver tipos efectivos ni semántica dinámica.

## Decisión

MUD mantiene actualmente dos representaciones normativas en la cadena de frontend:

1. el AST superficial de `especificacion/sintaxis/mud-surface-ast.asdl`;
2. el HIR nominal producido por resolución de nombres, en `especificacion/nombres/mud-nominal-hir.asdl`.

El HIR nominal contiene únicamente información justificable por resolución nominal. Su grafo admite propiedad, especialización y referencia nominal. No contiene tipos efectivos, dominios efectivos, cardinalidades inferidas, conversiones elaboradas, efectos, dependencias semánticas ni evidencia de terminación.

El tipado y la elaboración siguen siendo fases arquitectónicas posteriores y podrán producir una representación semántica propia. Esa representación se denomina de forma conceptual **IR semántico futuro**, pero MUD no fija todavía:

- un archivo ASDL para ella;
- un esquema de serialización;
- nombres concretos de nodos o aristas;
- una `schemaVersion` actual;
- qué información derivada debe almacenarse materialmente frente a reconstruirse.

El catálogo conceptual de D-051 pasa a ser un conjunto de requisitos que deberá revisarse cuando exista una superficie desarrollada de tipado y elaboración suficiente para diseñar esa representación. No obliga a mantener hoy un esquema mecánico anticipado.

El directorio genérico `especificacion/ir/` deja de ser una superficie normativa. El HIR nominal se ubica junto a la resolución de nombres en `especificacion/nombres/`.

Todo cambio futuro que introduzca o modifique nombres, scopes, propietarios, bindings, categorías nominales, anclas, visibilidad nominal o especialización debe revisar en el mismo cambio el capítulo 09 y el HIR nominal, conforme a MUD-EDIT-004.

## Consecuencias

- Ningún validador puede exigir la existencia de `mud-semantic-ir.asdl`.
- Ningún documento de la especificación actual presenta como existente un contrato posterior a tipado y elaboración.
- El HIR nominal continúa siendo un contrato mecánico normativo y reconstruible desde AST superficial + reglas de resolución.
- Las decisiones que necesitan una distinción semántica posterior pueden conservarla como requisito de elaboración futura sin fijar por adelantado su codificación.
- Diseñar el futuro IR requerirá integrar las superficies de tipos y elaboración que existan entonces y podrá adoptar una estructura distinta a cualquier esquema experimental previo.

## Verificación

1. `especificacion/ir/` no existe.
2. `especificacion/nombres/mud-nominal-hir.asdl` existe y solo modela información nominal.
3. Los validadores no requieren ningún IR semántico actual.
4. El pipeline documental distingue HIR nominal vigente de representación semántica futura todavía no formalizada.
5. Los cambios que afecten resolución nominal tienen una obligación editorial explícita de revisar capítulo 09 + HIR nominal.
'''

D051 = '''---
id: D-051
title: "Grafo semántico futuro e información reconstruible"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-009"
  - "Q-016"
  - "Q-027"
  - "Q-034"
  - "Q-054"
  - "Q-059"
affects:
  - "arquitectura, HIR nominal, futuro grafo semántico, futura representación posterior a tipado y elaboración, conformidad"
---
# ADR-051 — Grafo semántico futuro e información reconstruible

- Modificada por: [[ADR-097-hir-nominal-vigente-e-ir-semantico-diferido|D-097]].
- Ampliada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]] y [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]].
- Modificada por: [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]], [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]], [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]] y [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].
- Relacionada con: [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]].

## Contexto

Los análisis de impacto, explicación y ejecución necesitarán información semántica derivada, pero esa información no debe convertirse en una fuente alternativa de verdad ni fijarse mecánicamente antes de que las fases que la producen estén formalizadas.

## Decisión

Los archivos `.mud` y las decisiones de versión son la fuente semántica. El AST superficial y el HIR nominal son derivados reconstruibles actuales. La resolución nominal produce `especificacion/nombres/mud-nominal-hir.asdl`, con símbolos, scopes, bindings, anclas y relaciones nominales, sin conclusiones de tipado o elaboración.

Tras tipado y elaboración podrá existir una representación semántica posterior y un grafo semántico consultable derivado de ella. Su codificación concreta queda deliberadamente sin fijar mientras esas fases no dispongan de superficies normativas desarrolladas suficientes.

Cuando se diseñe esa representación futura deberá poder conservar o reconstruir, según corresponda, al menos estas distinciones conceptuales:

- procedencia hasta archivo y rango de origen;
- símbolos y anclas resueltos;
- las tres variantes de regla;
- participantes `for` y `on`, valores `given`, cardinalidad, mutabilidad y modos de vinculación;
- tipos, aliases, dominios, cardinalidades, unidades e intervalos ya elaborados;
- vinculaciones locales y su orden de evaluación;
- efectos, lecturas, escrituras, llamadas y dependencias;
- actividad lógica y dependencias suspendidas;
- `look`, `message`, sus salidas y dependencias diferidas;
- tests, activación local, efectos, aserciones y diagnósticos;
- dependencias de `allowed`, `eventually`, `when`, `if`, `after`, `old` y `always`;
- efectos estructurales `create`, `destroy`, adición y retirada de colecciones;
- derivación dimensional, magnitudes, unidades y equivalencias;
- dependencias generales, de dominio, estocásticas y duras cuando formen parte del análisis definido.

La decisión de qué información se almacena explícitamente, qué se deriva y cómo se serializa pertenece al diseño futuro de tipado/elaboración. Si se introduce un formato de intercambio persistente, deberá llevar versión de esquema compatible y permitir reconstrucción determinista desde las fuentes normativas anteriores.

Q-009 conserva abierto el formato externo y los nombres concretos cuando llegue a existir tal representación; esa pregunta no obliga a crearla anticipadamente.

## Consecuencias

- Una discrepancia en un derivado se resuelve descartándolo y reconstruyéndolo desde las fuentes normativas.
- No existe actualmente un contrato mecánico de IR semántico ni un grafo semántico final normativo.
- El HIR nominal no puede absorber tipos efectivos, dominios efectivos, cardinalidades inferidas, efectos ni evidencia de terminación para compensar esa ausencia.
- Las futuras herramientas de análisis deben esperar a la superficie semántica correspondiente o derivar únicamente información autorizada por las fases ya formalizadas.

## Verificación

1. El HIR nominal es reconstruible desde AST superficial + resolución nominal.
2. El HIR nominal permanece libre de conclusiones de tipado/elaboración.
3. No existe un esquema normativo de IR semántico mientras no estén desarrolladas sus fases productoras.
4. Las obligaciones conceptuales anteriores permanecen disponibles para auditar el diseño futuro sin fijar hoy su representación mecánica.
'''

D078 = '''---
id: D-078
title: "Resolución nominal, catálogo de anclas y grafo inicial"
status: vigente
date: 2026-08-03
supersedes: []
superseded-by: []
questions:
  - "Q-014"
affects:
  - "capítulo 09, AST superficial, HIR nominal, resolución nominal, tabla de símbolos, anclas, diagnósticos, LSP, grafo nominal, tipado y elaboración posteriores"
---
# ADR-078 — Resolución nominal, catálogo de anclas y grafo inicial

- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]], [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]], [[ADR-096-modulos-callables-look-message-y-activacion|D-096]] y [[ADR-097-hir-nominal-vigente-e-ir-semantico-diferido|D-097]].
- Amplía: [[ADR-035-organizacion-nombres-using-y-anclas|D-035]] y [[ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas|D-072]].

## Decisión

La norma denomina **path de MUD** a la identidad lógica derivada de las carpetas. No se escribe una cabecera `namespace` ni se reserva `path`. El LSP puede mostrar una cabecera virtual, copiar el nombre cualificado y revelar la procedencia física sin modificar el archivo.

Todas las declaraciones superiores de un path comparten un espacio nominal. La búsqueda de un nombre no cualificado consulta, en orden, entorno léxico, propietario o receptor implícito, path actual, `using` exactos, `using` recursivos e incorporados. Se elige el primer nivel no vacío; una categoría incompatible no habilita continuar. Candidatos con la misma ancla se deduplican y anclas distintas son ambiguas. Un `using` no reexporta. Cuando un candidato pertenece a otro módulo, `using` solo lo aporta a la resolución nominal: alcanzarlo exige además que `uses` autorice la dependencia y que el símbolo pertenezca al cierre visible del contrato modular. Un nombre cualificado tampoco elude esa frontera.

No existe sombreado de un nombre visible. Las convenciones `PascalCase`, `lowerCamel` y `lowerCamel` de unidad son requisitos estáticos con arreglo automático.

Poseen ancla las declaraciones nominales de primer nivel, campos en su propietario original, componentes, datos asociados declarados por una `family`, miembros de `family`, unidades declaradas, participantes `for`/`on`/`given`, metadatos configurados materializados como `Metadata` y tipos incorporados. Un campo heredado conserva el ancla declarativa del antecesor aunque su estado sea independiente en cada `thing`. Iteradores, vinculaciones locales ordinarias y valores globales no nominales solo reciben identidad interna efímera.

Las categorías canónicas son `thing`, `alias`, `family`, `magnitude`, `unit`, `rule`, `action`, `look`, `message`, `test` y `type`. Las declaraciones anidadas prolongan el ancla del propietario con `::<miembro>`; una contribución modular `start with` de primer nivel no tiene nombre ni ancla. La pertenencia a módulo es una dimensión de visibilidad y dependencia y no añade un componente al ancla nominal.

La resolución nominal crea símbolos, anclas, scopes y bindings de referencias cuya categoría ya puede determinarse y los materializa en `especificacion/nombres/mud-nominal-hir.asdl`. Los nombres de tipos se vinculan nominalmente a sus símbolos, pero la comprobación de compatibilidad, uniones, dominios, cardinalidades y miembros dependientes del tipo pertenece al tipado y la elaboración. La norma usa entornos y conjuntos de candidatos; un scope graph es una implementación posible, no autoridad.

El HIR nominal contiene únicamente las familias de relaciones que esta fase puede justificar: propiedad/contención (`Owns`), especialización (`Specializes`) y referencia nominal (`RefersTo`). Las relaciones que dependan de tipo efectivo, dominio, inicialización elaborada, cálculo, efecto o terminación quedan fuera del HIR y pertenecen a fases posteriores cuya representación mecánica todavía no está fijada.

La especialización nominal incluye `thing` y aliases. Los componentes y campos derivados de un alias poseen ancla bajo la categoría `alias`; un miembro heredado conserva el ancla de su origen. Una sobrescritura de predeterminado no introduce un nuevo miembro público ni una nueva ancla.

## Migraciones

Una ancla cambia con categoría, path o nombre cualificado. El tooling conserva una correspondencia dirigida explícita para migrar referencias persistentes, pero el ancla anterior no se convierte en alias fuente. Q-014 conserva abiertos el formato externo, composición, colisiones, conservación y aplicación sobre mundos persistidos.

## Verificación

1. Primer nivel no vacío y categoría incompatible sin caída posterior.
2. Colisión global entre categorías.
3. Deduplicación por ancla y ambigüedad real.
4. Ausencia de sombreado y errores de casing reparables.
5. Anclas de campos heredados, miembros, unidades y builtins.
6. Participantes declarados con ancla pública y símbolos locales ordinarios sin ella.
7. HIR nominal construible antes del tipado completo y libre de tipos, dominios, cardinalidades y terminación elaborados.
8. El grafo HIR se limita a `Owns`, `Specializes` y `RefersTo`.
9. Un `using` o un nombre cualificado no atraviesa una frontera modular sin `uses` y contrato visible.
10. La pertenencia a módulo no altera el ancla nominal.
'''

D093 = '''---
id: D-093
title: "AST superficial, HIR nominal y fase semántica posterior"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "pipeline, AST superficial, HIR nominal, resolución de nombres, tabla de símbolos, grafo nominal, tipado, elaboración, futura representación semántica y validadores"
---

# ADR-093 — AST superficial, HIR nominal y fase semántica posterior

- Modifica: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].
- Modificada por: [[ADR-097-hir-nominal-vigente-e-ir-semantico-diferido|D-097]].
- Precisa: [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]], [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]], [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]].

## Contexto

Una representación que mezcle resolución nominal con tipos efectivos, dominios elaborados, cardinalidades inferidas y pruebas de terminación borra fronteras de fase útiles. La arquitectura debe distinguir la forma fuente, el resultado de resolución nominal y el significado que solo puede conocerse después de tipado y elaboración, sin obligar a fijar prematuramente la representación de esta última fase.

## Decisión

MUD posee un único AST de fuente: el **AST superficial** producido a partir de la CST sin pérdidas. Conserva la forma abstracta escrita y su procedencia sin anticipar resolución, tipado ni elaboración.

La resolución de nombres consume ese AST y produce un **HIR nominal** normativo. El HIR no duplica toda la sintaxis de fuente: registra exclusivamente información cuya existencia depende de resolución nominal:

- símbolos anclados y `LocalSymbol`;
- propietarios y ámbitos léxicos;
- bindings de cada referencia superficial a un símbolo;
- anclas públicas;
- aristas nominales de propiedad, especialización y referencia.

El HIR nominal no puede contener tipos efectivos, narrowing, dominios efectivos, formas de colección, cardinalidades efectivas o inferidas, conversiones elaboradas, pruebas de terminación ni ninguna otra conclusión que requiera tipado o elaboración. Su esquema normativo vive en `especificacion/nombres/mud-nominal-hir.asdl`.

El tipado y la elaboración consumen el AST superficial junto con el HIR nominal. Su resultado semántico pertenece a una fase arquitectónica posterior, pero el repositorio no fija todavía un esquema mecánico normativo para representarlo. Ese contrato se diseñará cuando las superficies de tipos y elaboración estén suficientemente desarrolladas.

Ningún artefacto derivado es una fuente semántica independiente: se reconstruye desde los archivos `.mud`, las decisiones de versión y las fases anteriores aplicables.

## Pipeline

```text
texto fuente
→ scanner y clasificación contextual
→ CST sin pérdidas
→ AST superficial
→ resolución nominal
→ HIR nominal: símbolos + scopes + bindings + anclas + grafo nominal parcial
→ tipado y elaboración
→ representación semántica posterior por formalizar
→ análisis posteriores / ejecución
```

El HIR nominal es deliberadamente menor que un AST resuelto completo y no anticipa conclusiones de tipos.

## Consecuencias

- `mud-surface-ast.asdl` continúa siendo el único esquema AST de fuente.
- `especificacion/nombres/mud-nominal-hir.asdl` es el contrato de salida de resolución nominal.
- No existe actualmente un ASDL normativo posterior a tipado/elaboración.
- D-078 describe la construcción del HIR nominal y no promete tipos o dominios elaborados.
- Los validadores deben comprobar la autoconsistencia del HIR nominal y prohibir en él conceptos reservados a elaboración.

## Verificación

1. El directorio de sintaxis contiene un único esquema AST de fuente: `mud-surface-ast.asdl`.
2. El pipeline contiene explícitamente `Surface AST → HIR nominal → tipado/elaboración → representación semántica futura`.
3. El HIR nominal representa símbolos, scopes, bindings, anclas y `Owns | Specializes | RefersTo`.
4. El HIR nominal no contiene tipos efectivos, dominios efectivos, cardinalidades ni evidencia de terminación.
5. No se exige un esquema semántico posterior antes de formalizar las fases que lo producen.
6. El validador rechaza tipos ASDL desconocidos y conceptos elaborados dentro del HIR nominal.
'''

write("notas/decisiones/ADR-097-hir-nominal-vigente-e-ir-semantico-diferido.md", D097)
write("notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles.md", D051)
write("notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial.md", D078)
write("notas/decisiones/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado.md", D093)

# Move the current nominal contract into the names surface and retire the premature semantic IR surface.
src_hir = ROOT / "especificacion/ir/mud-nominal-hir.asdl"
dst_hir = ROOT / "especificacion/nombres/mud-nominal-hir.asdl"
if not src_hir.exists():
    raise SystemExit("No existe el HIR nominal de origen")
dst_hir.parent.mkdir(parents=True, exist_ok=True)
src_hir.rename(dst_hir)
for obsolete in [ROOT / "especificacion/ir/mud-semantic-ir.asdl", ROOT / "especificacion/ir/README.md"]:
    if not obsolete.exists():
        raise SystemExit(f"Falta artefacto esperado antes de retirada: {obsolete}")
    obsolete.unlink()
try:
    (ROOT / "especificacion/ir").rmdir()
except OSError as exc:
    raise SystemExit(f"especificacion/ir no quedó vacía: {exc}")

write("especificacion/nombres/README.md", '''# Resolución nominal de MUD

Este directorio contiene el contrato mecánico normativo de la fase de resolución de nombres. Complementa [[../09-nombres-y-anclas|09. Nombres, paths y anclas]] y no define tipado ni semántica dinámica.

## `mud-nominal-hir.asdl`

Es la salida normativa de resolución nominal sobre el AST superficial. Conserva símbolos, scopes, bindings, anclas y las relaciones nominales `Owns`, `Specializes` y `RefersTo`.

No puede contener tipos efectivos, dominios efectivos, cardinalidades inferidas, narrowing, conversiones elaboradas, efectos, dependencias semánticas ni evidencia de terminación. Esas conclusiones pertenecen a fases posteriores todavía no formalizadas mecánicamente.

El HIR nominal es derivado y reconstruible: no constituye una fuente semántica independiente.
''')

# Specification: keep only currently formalized phase boundaries.
replace_once("especificacion/08-sintaxis-abstracta.md", "  - D-096\n", "  - D-096\n  - D-097\n")
replace_once("especificacion/08-sintaxis-abstracta.md",
'''La resolución nominal opera sobre este AST y produce el HIR normativo `ir/mud-nominal-hir.asdl`, que materializa símbolos, scopes, bindings, anclas y un grafo nominal parcial sin duplicar la sintaxis de fuente. Tras tipado y elaboración, el contrato semántico vive en `ir/mud-semantic-ir.asdl`, donde aparecen tipos efectivos, dominios, cardinalidades, dependencias y otras formas elaboradas.''',
'''La resolución nominal opera sobre este AST y produce el HIR normativo `nombres/mud-nominal-hir.asdl`, que materializa símbolos, scopes, bindings, anclas y un grafo nominal parcial sin duplicar la sintaxis de fuente. Los tipos efectivos, dominios, cardinalidades, dependencias y demás conclusiones elaboradas pertenecen a fases posteriores de tipado y elaboración cuya representación mecánica todavía no está fijada.''')
replace_once("especificacion/08-sintaxis-abstracta.md", "→ IR semántico tipado/elaborado", "→ representación semántica posterior todavía no formalizada")
replace_once("especificacion/08-sintaxis-abstracta.md",
"Tipos efectivos, dominios efectivos, cardinalidades, conversiones elaboradas y evidencia de terminación están prohibidos hasta el IR semántico.",
"Tipos efectivos, dominios efectivos, cardinalidades, conversiones elaboradas y evidencia de terminación quedan fuera del HIR nominal y pertenecen a fases posteriores de tipado y elaboración.")
replace_once("especificacion/08-sintaxis-abstracta.md", "se rechaza estáticamente antes del IR semántico.", "se rechaza estáticamente durante las fases posteriores de validación y tipado.")
replace_once("especificacion/08-sintaxis-abstracta.md",
"La resolución y el tipado deben demostrar que `value` produce estáticamente `Type`; tras elaboración el IR semántico usa directamente el tipo representado. Una llamada ordinaria sin `~type` continúa siendo un valor.",
"La resolución y el tipado deben demostrar que `value` produce estáticamente `Type`; la elaboración posterior obtiene directamente el tipo representado. La forma mecánica de esa elaboración todavía no está fijada. Una llamada ordinaria sin `~type` continúa siendo un valor.")
replace_once("especificacion/08-sintaxis-abstracta.md",
"El IR semántico distingue ambas operaciones: `ContextualAliasConstructionExpr(literal, target_alias)` representa construcción dirigida por el tipo esperado y `ConversionExpr(value, target_type)` representa `to` escrito explícitamente. El AST superficial no añade un nodo de alias contextual porque todavía conserva el literal y el contexto que lo espera.",
"La elaboración posterior debe distinguir la construcción de alias dirigida por el tipo esperado de la conversión nominal `to` escrita explícitamente. El AST superficial no añade un nodo de alias contextual porque todavía conserva el literal y el contexto que lo espera; la representación mecánica de la distinción elaborada se fijará con esa fase.")

replace_once("especificacion/09-nombres-y-anclas.md", "  - D-096\n", "  - D-096\n  - D-097\n")
replace_once("especificacion/09-nombres-y-anclas.md",
"La resolución nominal registra estas vinculaciones como símbolos locales subordinados a su propietario; el IR semántico usa la variante genérica `LocalSymbol(owner, kind, name, ordinal)`. Estas vinculaciones no introducen una clase de símbolo ni una categoría de ancla nuevas.",
"La resolución nominal registra estas vinculaciones en el HIR como `LocalSymbol(owner, kind, name, ordinal)` subordinados a su propietario. Estas vinculaciones no introducen una clase de símbolo ni una categoría de ancla nuevas.")
replace_once("especificacion/09-nombres-y-anclas.md", "el HIR nominal de `ir/mud-nominal-hir.asdl`", "el HIR nominal de `nombres/mud-nominal-hir.asdl`")
replace_once("especificacion/09-nombres-y-anclas.md",
"4. La elaboración completa accesos, llamadas, abreviaturas contextuales y demás significado dependiente de tipos en el IR semántico.",
"4. La elaboración completa accesos, llamadas, abreviaturas contextuales y demás significado dependiente de tipos; su representación mecánica posterior todavía no está fijada.")
replace_regex_once("especificacion/09-nombres-y-anclas.md",
r"## Grafo nominal inicial\n\n.*?\n## Conformidad",
'''## Grafo nominal inicial

Después de la resolución nominal se construye un grafo parcial sobre símbolos resueltos. El HIR nominal conserva exactamente estas familias de aristas:

- `Owns`: propiedad o contención nominal;
- `Specializes`: especialización nominal entre declaraciones;
- `RefersTo`: referencia nominal cuyo origen y destino ya son símbolos resueltos.

Tipos y dominios efectivos, inicialización elaborada, cálculos, lecturas, escrituras, efectos, magnitudes derivadas y demás relaciones dependientes de tipos no pertenecen a esta fase. Se determinan, cuando corresponda, durante tipado y elaboración posteriores.

El grafo parcial no sustituye al AST ni constituye una fuente de verdad. Su finalidad es materializar exclusivamente las conclusiones de resolución nominal que deben sobrevivir como contrato entre el AST superficial y el sistema de tipos.

## Conformidad''')
replace_once("especificacion/09-nombres-y-anclas.md",
"El IR semántico conserva para cada rama una `decision_branch_key` local al diccionario. Para una rama ordinaria, la clave es la forma canónica del selector resuelto. Dos ramas ordinarias con la misma forma canónica dentro del mismo diccionario son inválidas: compartirían la misma clave estructural local. `_` usa una clave `FallbackBranchKey` distinta y única. El ordinal fuente se conserva por separado porque participa en `FirstMatch`, pero tampoco se convierte en ancla.",
"Cada rama funcional posee una `decision_branch_key` estructural local al diccionario para las fases que necesiten reconstrucción o dependencias posteriores. Para una rama ordinaria, la clave es la forma canónica del selector resuelto. Dos ramas ordinarias con la misma forma canónica dentro del mismo diccionario son inválidas: compartirían la misma clave estructural local. `_` usa una clave `FallbackBranchKey` distinta y única. Esa clave no es un símbolo, no pertenece al HIR nominal y su representación mecánica posterior no se fija todavía. El ordinal fuente se conserva por separado porque participa en `FirstMatch`, pero tampoco se convierte en ancla.")

replace_once("especificacion/sintaxis/cst-a-ast-superficial.md", "  - D-096\n", "  - D-096\n  - D-097\n")
replace_once("especificacion/sintaxis/cst-a-ast-superficial.md", "se rechaza estáticamente para `given` antes de producir IR semántico.", "se rechaza estáticamente para `given` durante las fases posteriores de validación y tipado.")
replace_once("especificacion/sintaxis/cst-a-ast-superficial.md",
"`reflected-type` consume una `postfix-expression` seguida por `~type` y produce `ReflectedType(value)`; la elaboración posterior exige que la propiedad denote estáticamente `Type` y sustituye esa forma por el tipo representado en el IR semántico.",
"`reflected-type` consume una `postfix-expression` seguida por `~type` y produce `ReflectedType(value)`; la elaboración posterior exige que la propiedad denote estáticamente `Type` y obtiene el tipo representado. La forma mecánica posterior a tipado y elaboración todavía no está fijada.")

# Editorial invariant specific to name resolution propagation.
replace_once("especificacion/00-convenciones-editoriales.md", "decisions:\n  - D-070\n", "decisions:\n  - D-070\n  - D-097\n")
anchor = "Un cambio de gramática que afecte a la estructura debe actualizar en el mismo commit el catálogo CST, la cobertura, la transformación y el ASDL correspondientes.\n"
addition = anchor + '''\n> [!rule] MUD-EDIT-004 — Propagación de resolución nominal\n> Todo cambio que introduzca, elimine o modifique nombres, ámbitos, propietarios, bindings, categorías nominales, anclas, visibilidad nominal, cualificación o especialización debe revisar en el mismo cambio `09-nombres-y-anclas.md` y `nombres/mud-nominal-hir.asdl`. Si afecta a su contrato, ambas superficies y sus validadores deben actualizarse atómicamente.\n\nLa revisión debe comprobar al menos qué símbolos se crean, en qué scope viven, qué nombre los resuelve, qué propietario tienen, si reciben ancla pública y qué relaciones `Owns`, `Specializes` o `RefersTo` produce la resolución. Una regla dependiente de tipos, efectos o elaboración no se añade al HIR nominal para satisfacer artificialmente esta obligación.\n'''
replace_once("especificacion/00-convenciones-editoriales.md", anchor, addition)

agents_anchor = "- Una decisión vigente debe integrarse en toda superficie normativa ya desarrollada cuya responsabilidad cubra su alcance. Si la ubicación canónica todavía no existe, no se inventa una superficie provisional solo para alojarla, pero ninguna superficie existente puede contradecirla.\n"
replace_once("AGENTS.md", agents_anchor, agents_anchor + "- Si el cambio afecta resolución nominal, debe aplicarse además MUD-EDIT-004 y revisarse `especificacion/09-nombres-y-anclas.md` junto con `especificacion/nombres/mud-nominal-hir.asdl`.\n")

cycle_anchor = "- Validadores editoriales específicos de MUD-EDIT-002 y MUD-EDIT-003 cuando existan.\n"
replace_once("gobierno/CICLO-DOCUMENTAL.md", cycle_anchor, cycle_anchor + "- Aplicación de MUD-EDIT-004 y coherencia entre capítulo 09 + HIR nominal cuando el cambio afecte resolución de nombres.\n")

# Keep older current ADRs literal without claiming that a concrete semantic IR already exists.
for path in (ROOT / "notas/decisiones").glob("ADR-*.md"):
    if path.name in {
        "ADR-051-grafo-semantico-e-ir-reconstruibles.md",
        "ADR-078-resolucion-nominal-anclas-y-grafo-inicial.md",
        "ADR-093-ast-superficial-unico-e-ir-semantico-elaborado.md",
        "ADR-097-hir-nominal-vigente-e-ir-semantico-diferido.md",
    }:
        continue
    text = path.read_text(encoding="utf-8")
    text = text.replace("el IR semántico", "la futura representación semántica posterior a tipado y elaboración")
    text = text.replace("El IR semántico", "La futura representación semántica posterior a tipado y elaboración")
    text = text.replace("IR semántico", "representación semántica posterior a tipado y elaboración")
    path.write_text(text, encoding="utf-8")

# The active cleanup inventory should describe the current boundary, not require the retired artifact.
replace_regex_once("notas/inventario-saneamiento-especificacion.md",
r"## Etapa 4 — auditoría de decisiones vigentes\n\n.*?\n## Etapa 5 — auditoría específica de la integración D-096",
'''## Etapa 4 — auditoría de decisiones vigentes

Completada. Se recorrieron las decisiones vigentes contra las superficies normativas ya desarrolladas y contra los hogares futuros declarados por el mapa de la especificación.

La frontera vigente después de D-097 mantiene como superficie mecánica actual el HIR nominal de resolución de nombres y difiere cualquier esquema posterior a tipado/elaboración hasta que esas fases estén desarrolladas. La auditoría exige por tanto coherencia del AST superficial, capítulo 09 y HIR nominal; los requisitos semánticos posteriores se clasifican como `M` cuando todavía no existe su superficie canónica.

El grafo nominal queda limitado a `Owns`, `Specializes` y `RefersTo`. Tipos efectivos, dominios, cardinalidades, efectos y dependencias semánticas no se introducen en el HIR para compensar la ausencia de una representación posterior.

## Etapa 5 — auditoría específica de la integración D-096''')

# Validator: move HIR responsibility to nombres and remove the premature semantic IR contract.
path = "especificacion/sintaxis/validate_syntax_model.py"
text = read(path)
text = text.replace('nominal_hir_path = root / "especificacion/ir/mud-nominal-hir.asdl"', 'nominal_hir_path = root / "especificacion/nombres/mud-nominal-hir.asdl"')
text = text.replace('semantic_ir_path = root / "especificacion/ir/mud-semantic-ir.asdl"', 'retired_ir_dir = root / "especificacion/ir"')
text = text.replace('problems.append(Problem(str(retired_resolved_ast_path), "contrato retirado: use HIR nominal + IR semántico"))', 'problems.append(Problem(str(retired_resolved_ast_path), "contrato retirado: use AST superficial + HIR nominal"))')
old = '''    if not semantic_ir_path.exists():
        problems.append(Problem(str(semantic_ir_path), "falta el contrato del IR semántico"))
        semantic_ir_defined, semantic_ir_used = set(), set()
    else:
        semantic_ir_defined, semantic_ir_used = asdl_types_and_uses(semantic_ir_path)
'''
if old not in text:
    raise SystemExit("validator: no encontré bloque de semantic_ir_path")
text = text.replace(old, '''    if retired_ir_dir.exists():
        problems.append(Problem(str(retired_ir_dir), "superficie retirada: el HIR nominal vive en especificacion/nombres y no existe todavía un IR semántico normativo"))
''')
old = '''    for unknown in sorted(semantic_ir_used - semantic_ir_defined - {"int", "string", "identifier"}):
        problems.append(Problem(str(semantic_ir_path), f"tipo ASDL no definido: {unknown}"))
    if semantic_ir_path.exists() and "module MUDSemanticIR" not in semantic_ir_path.read_text(encoding="utf-8"):
        problems.append(Problem(str(semantic_ir_path), "falta module MUDSemanticIR"))
'''
if old not in text:
    raise SystemExit("validator: no encontré validación ASDL semántica")
text = text.replace(old, '''    if nominal_hir_path.exists():
        hir_text = nominal_hir_path.read_text(encoding="utf-8")
        for fragment in ["Owns(", "Specializes(", "RefersTo("]:
            if fragment not in hir_text:
                problems.append(Problem(str(nominal_hir_path), f"falta relación nominal requerida: {fragment}"))
''')
old = '''        root / "especificacion/ir/mud-semantic-ir.asdl": [
            "ExactNominalTypeTestExpr(",
            "ExactDictionarySetOperationExpr(",
            "FunctionalDictionarySetOperationExpr(",
            "ContextualAliasConstructionExpr(",
        ],
'''
if old not in text:
    raise SystemExit("validator: no encontré required_fragments del IR semántico")
text = text.replace(old, '')
write(path, text)

# Regenerate decision index from metadata after adding D-097 and retitling D-051/D-093.
subprocess.run(["python", "tooling/decisions/manage_decisions.py", "generate"], cwd=ROOT, check=True)

# Global invariants of the new boundary.
if (ROOT / "especificacion/ir").exists():
    raise SystemExit("especificacion/ir sigue existiendo")
if not (ROOT / "especificacion/nombres/mud-nominal-hir.asdl").exists():
    raise SystemExit("falta el HIR nominal en especificacion/nombres")
for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts or p.name == Path(__file__).name:
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    if "mud-semantic-ir.asdl" in text:
        raise SystemExit(f"referencia obsoleta a mud-semantic-ir.asdl en {p.relative_to(ROOT)}")
    if "ir/mud-nominal-hir.asdl" in text:
        raise SystemExit(f"referencia obsoleta al path antiguo del HIR en {p.relative_to(ROOT)}")
for p in (ROOT / "especificacion").rglob("*.md"):
    if "IR semántico" in p.read_text(encoding="utf-8"):
        raise SystemExit(f"la especificación actual todavía da superficie al IR semántico: {p.relative_to(ROOT)}")

# This helper is deliberately ephemeral and must not survive the candidate tree.
(ROOT / Path(__file__).name).unlink()
