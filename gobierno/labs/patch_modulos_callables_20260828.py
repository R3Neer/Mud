from __future__ import annotations

import re
from pathlib import Path

ROOT = Path.cwd()
DATE = "2026-08-28"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def replace_exact(path: str, old: str, new: str, *, count: int = 1) -> None:
    text = read(path)
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"{path}: expected {count} occurrences, found {actual}: {old[:80]!r}")
    write(path, text.replace(old, new, count))


def append_once(path: str, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    write(path, text + "\n" + block.rstrip() + "\n")


def create_once(path: str, content: str) -> None:
    p = ROOT / path
    if p.exists():
        current = p.read_text(encoding="utf-8")
        if current != content:
            raise SystemExit(f"{path}: existing content differs")
        return
    write(path, content)


# ---------------------------------------------------------------------
# Questions: retire broad legacy questions and create focused open ones.
# ---------------------------------------------------------------------

q51 = """---
id: Q-051
title: Identidad y selección de un look
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-08-28
decisions:
  - D-027
  - D-061
  - D-096
affects: []
superseded-by: []
---

# Q-051 — Identidad y selección de un `look`

Estado: **resuelta** mediante [[notas/decisiones/ADR-096-modulos-callables-look-message-y-activacion|D-096]].

Un `look` es un callable puro con participantes `for` y parámetros `given`. Una llamada devuelve exactamente un objeto resultado de tipo anónimo, no una secuencia especial de filas. La vista de lectura procede del contexto de llamada: estado estable desde el host, instantánea de la rule o delta privado visible desde un `then`.

Las cuestiones que permanecen abiertas ya no son de identidad/selección básica del `look`: el join de resultados dinámicos se sigue en Q-065 y la identidad de tipos anónimos en Q-068.
"""
write("notas/preguntas/Q-051-identidad-y-seleccion-de-un-look.md", q51)

q52 = """---
id: Q-052
title: Entrega de message
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-08-28
decisions:
  - D-027
  - D-096
affects: []
superseded-by: []
---

# Q-052 — Entrega de `message`

Estado: **resuelta** mediante [[notas/decisiones/ADR-096-modulos-callables-look-message-y-activacion|D-096]].

D-096 fija la multiplicidad por ocurrencias causales, la ausencia de deduplicación por payload, el orden causal por ondas, la evaluación causal de `when`/`if`, la propagación a la onda siguiente y la cancelación de entrega exterior cuando la resolución revierte. MUD y el host observan la misma identidad de ocurrencia, con proyección causal interna y proyección final exterior.

El único borde material no resuelto de la antigua pregunta se separa en Q-067: qué proyección exterior corresponde cuando un participante deja de existir antes del estado final.
"""
write("notas/preguntas/Q-052-entrega-de-message.md", q52)

questions = {
"Q-062-gramatica-completa-de-mud-module.md": ("Gramática completa de `mud.module`", "P1", "Fijar la sintaxis completa del archivo `mud.module`: forma de `uses`, reglas de separación y cualquier metadato adicional sin duplicar el MudPath derivado del directorio.", "gramática de módulo, texto fuente, tooling"),
"Q-063-varianza-y-compatibilidad-de-callables.md": ("Varianza y compatibilidad de tipos callable", "P1", "Formalizar compatibilidad y varianza de tipos callable en entradas, salidas, lugares mutables y uniones, manteniendo separada la capacidad exterior de `action` frente a `subaction`.", "tipado callable, subtyping, narrowing"),
"Q-064-aliases-y-especializacion-entre-modulos.md": ("Aliases y especialización nominal entre módulos", "P1", "Decidir qué especialización nominal de aliases puede atravesar una frontera modular y qué cierre de contrato exige, sin trasladar automáticamente la prohibición ya fijada para herencia de `thing`.", "módulos, aliases, tipos"),
"Q-065-join-de-resultados-dinamicos-de-look.md": ("Join de resultados dinámicos de `look`", "P1", "Definir el resultado estático de una invocación dinámica de `look` cuando el conjunto de alternativas posee varios mínimos comunes incomparables, y precisar cuándo se forma una unión.", "look, callables, tipado"),
"Q-066-binding-nominal-de-descriptores-borrados.md": ("Binding nominal de descriptores callable borrados", "P1", "Definir cómo se recuperan o exigen los nombres de roles `for` y `given` al invocar un descriptor callable cuyo tipo estático ha borrado parte de la identidad nominal de la declaración concreta.", "callables, resolución, binding"),
"Q-067-participantes-de-message-inexistentes-al-final.md": ("Participantes de `message` inexistentes al estado final", "P1", "Decidir la proyección exterior de una ocurrencia confirmada cuando alguno de sus bindings `on` deja de existir o de estar activo antes del estado estable final, preservando la identidad causal interna.", "message, lifecycle, frontera host"),
"Q-068-identidad-de-tipos-anonimos.md": ("Identidad e igualdad estructural de tipos anónimos", "P1", "Definir cuándo dos tipos anónimos estructuralmente iguales, incluidos resultados de `look` y payloads de `message`, son el mismo tipo para igualdad, hashing, cachés y reflexión.", "tipos anónimos, reflexión, look, message"),
}
for filename, (title, priority, body, affects) in questions.items():
    qid = filename.split("-", 2)[0] + "-" + filename.split("-", 2)[1]
    content = f"""---
id: {qid}
title: {title}
priority: {priority}
opened: {DATE}
resolved: false
closed:
decisions:
  - D-096
affects:
  - {affects}
superseded-by: []
---

# {qid} — {title}

## Contenido

{body}
"""
    create_once(f"notas/preguntas/{filename}", content)


# ---------------------------------------------------------------------
# D-027 is wholly replaced. Other vigente ADRs receive literal deltas.
# ---------------------------------------------------------------------

d27 = "notas/decisiones/ADR-027-salidas-look-y-message.md"
replace_exact(d27, "status: vigente", "status: sustituida")
replace_exact(d27, "superseded-by: []", "superseded-by:\n  - \"D-096\"")
append_once(d27, "Sustituida íntegramente por D-096", """## Estado posterior

Esta decisión fue **sustituida íntegramente por [[ADR-096-modulos-callables-look-message-y-activacion|D-096]]**. Su descripción de `look` sin `given`, `message` como salida con campos evaluados únicamente al final y la frontera exclusivamente host se conserva aquí solo como historial.
""")

replace_exact(
    "notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md",
    "Reglas reactivas, `always`, `look` y `message` no admiten `given`.",
    "Reglas reactivas, `always` y `message` no admiten `given`. Un `look` sí admite `given` conforme a D-096."
)

amendments = {
"notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas.md": """## Modificación vigente por D-096

D-096 introduce el módulo como dimensión semántica de visibilidad sin incorporarlo a las anclas. El MudPath nominal y las anclas existentes conservan su forma. `using` continúa resolviendo/importando nombres dentro de un `.mud`; no concede por sí solo permiso para atravesar una frontera modular, que corresponde a `uses` en `mud.module`.
""",
"notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md": """## Modificación vigente por D-096

Un `look` admite `given` con las reglas generales de binding y defaults. Las declaraciones gobernadas por `on` siguen sin `given` y, cuando se usan como trigger, se referencian sin `()`. Los valores callable almacenados se invocan mediante la forma ordinaria de receptores y argumentos; almacenar el descriptor no pre-vincula roles ni `given`.

Además, un participante relacionado `on nombre: Tipo in fuente` puede vincular valores de una fuente finita enumerable, no solo identidades `thing`. La forma directa sin fuente continúa reservada al universo implícito de `thing`; por tanto `on n: Nat` sin fuente finita es inválido.
""",
"notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla.md": """## Modificación vigente por D-096

Una rule reactiva continúa sin ser callable como regla booleana, pero su `then` puede invocar actions y subactions reales dentro de la resolución causal activa. Rules reactivas y `always` pueden además actuar como fuentes declarativas de trigger: la reactiva pulsa cuando dispara efectivamente y la `always` cuando se evalúa para la vinculación/onda correspondiente. Actions, subactions, looks, reglas booleanas y tests no adquieren esa condición de trigger.
""",
"notas/decisiones/ADR-042-acciones-raiz-y-resultados.md": """## Modificación vigente por D-096

Se retira la clasificación semántica entre action elemental y compuesta. Todo `then` es una secuencia ordenada que puede mezclar efectos, locales, llamadas y `for each`. Una llamada interna observa el delta privado del punto textual y aporta sus efectos a la misma resolución. `action` conserva capacidad de raíz exterior; `subaction` es reutilizable desde cualquier `then` pero no puede ser raíz exterior. Los `after` anidados se evalúan contra el estado estable tentativo final de la resolución completa.
""",
"notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola.md": """## Modificación vigente por D-096

Un `message` es una ocurrencia causal con identidad y bindings, no una mera salida cuyos campos se difieren al estado final. La ocurrencia nacida en una onda queda disponible como trigger en la onda siguiente. Dentro de MUD su payload se proyecta sobre la vista causal de nacimiento; hacia el host, tras commit, se proyecta sobre el estado estable final. Ambas proyecciones pertenecen a la misma ocurrencia. La estabilización exige además ausencia de consecuencias/ocurrencias causales pendientes.
""",
"notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md": """## Modificación vigente por D-096

La activación inicial pasa a ser modular. Cada módulo puede contribuir como máximo un `start with`; todas las contribuciones se combinan y materializan conjuntamente antes de la estabilización. `start with` ya no separa `things` y `rules`, no establece orden y solo puede activar declaraciones con ciclo de vida del mismo módulo.
""",
"notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md": """## Modificación vigente por D-096

El `start with` de test usa la superficie unificada de D-096. Para un test raíz se calcula estáticamente el cierre transitivo de tests que puede llamar y se unen sus contribuciones de activación antes de ejecutar el cuerpo. Los tests pueden cruzar módulos solo en contexto de pruebas, mediante operaciones de test visibles y dependencias `uses`; una llamada posterior no vuelve a ejecutar el `start with` del test alcanzado.
""",
"notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo.md": """## Modificación vigente por D-096

El álgebra de `Trigger` se generaliza de pulsos booleanos a cero o más matches causales. Un match conserva bindings/testigos e identidad de ocurrencias. `and` realiza natural join de matches compatibles y `or` su unión. Messages, rules reactivas y `always` pueden ser fuentes declarativas de trigger; una referencia a declaración `on` no usa paréntesis de llamada.
""",
"notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md": """## Modificación vigente por D-096

`on` conserva su papel de binding automático y no absorbe las ocurrencias de `message`: la causalidad de messages/rules pertenece a `when`. D-096 amplía la forma relacionada `nombre[: Tipo] in fuente` a valores procedentes de una fuente finita enumerable. La forma directa sin `in` sigue seleccionando identidades `thing` del universo implícito.
""",
"notas/decisiones/ADR-065-cabecera-using-de-fichero.md": """## Modificación vigente por D-096

`using` sigue siendo una cabecera de resolución de nombres de un `.mud`. La nueva dependencia modular `uses` vive en `mud.module` y autoriza el cruce de la frontera semántica; un `using` no crea esa autorización y un `uses` no importa automáticamente todos los nombres en cada fichero.
""",
"notas/decisiones/ADR-075-dominios-enumerables-all-y-valores-derivados.md": """## Modificación vigente por D-096

Además del literal contextual `all`, existe `all D`, que materializa la enumeración canónica completa de un dominio enumerable explícito. Los dominios reflectivos visibles admiten formas como `all action`, `all rule`, `all look` y `all A.action(B)`. `all` sin operando conserva su elaboración contextual.
""",
"notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones.md": """## Modificación vigente por D-096

Selección y `take` producen colecciones. Cuando su fuente conceptual es un dominio, debe materializarse explícitamente mediante `all D`; por ejemplo `candidate in all Actions: ...` y `take n from all D`. Recorridos y cuantificadores que no producen una colección pueden consumir directamente un dominio finito enumerable.
""",
"notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md": """## Modificación vigente por D-096

Se sustituye la sección de activación estructurada que exigía bloques separados `things` y `rules`. `start with` acepta una contribución directa o un bloque unificado de expresiones que aportan declaraciones activables `thing | rule`; las identidades se deduplican y el orden no es semántico. La activación se agrega por módulo.

También se amplía `subaction`: puede invocarse desde cualquier contexto `then`, no solo desde otra action/subaction, sin adquirir capacidad de raíz exterior.
""",
"notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md": """## Modificación vigente por D-096

`~private` queda retirado por completo como metadato estándar y como default de fichero. La visibilidad exterior se deriva de módulo, categoría operacional y cierre de tipos. La reflexión cruzada de módulo solo es válida si su contrato garantiza que no puede devolver entidades invisibles; no se permite filtrar silenciosamente una colección reflectiva para ocultarlas. Tooling completo y reflexión disponible al código MUD siguen siendo superficies distintas.
""",
"notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md": """## Modificación vigente por D-096

Las operaciones que producen una colección desde un dominio, incluida la selección, requieren materialización explícita `all D`. Los recorridos `for each` y cuantificadores pueden consumir directamente dominios finitos enumerables porque no materializan por sí mismos una colección. Actions, rules reactivas y messages admiten además locales puras previas entre metadatos y cláusulas de comportamiento.
""",
}
for path, block in amendments.items():
    append_once(path, "## Modificación vigente por D-096", block)

replace_exact(
    "notas/decisiones/ADR-091-datos-de-family-como-descriptores-anclados.md",
    "`~private` continúa sin ser válido en datos asociados de `family`: D-087 lo restringe a declaraciones de primer nivel compatibles y a campos pertenecientes a una `thing`.",
    "`~private` no es válido en datos asociados de `family` ni en ninguna otra declaración: D-096 lo retira del lenguaje."
)
append_once(
    "notas/decisiones/ADR-091-datos-de-family-como-descriptores-anclados.md",
    "## Modificación vigente por D-096",
    """## Modificación vigente por D-096

La referencia histórica a las ubicaciones donde D-087 permitía `~private` queda reemplazada: `~private` ya no forma parte del lenguaje. El resto del contrato de descriptores de datos de `family` permanece vigente.
"""
)


# ---------------------------------------------------------------------
# Grammar: closed surface changes only. mud.module grammar stays Q-062.
# ---------------------------------------------------------------------

grammar = "especificacion/gramatica/mud.ebnf"
replace_exact(
    grammar,
    'look-declaration\n    ::= "look" , nominal-name\n        , [ for-clause ]\n        , "{"',
    'look-declaration\n    ::= "look" , nominal-name\n        , [ for-clause ]\n        , [ given-clause ]\n        , "{"'
)
replace_exact(
    grammar,
    'reactive-rule-declaration\n    ::= "rule" , nominal-name\n        , [ on-clause ]\n        , "{" , declaration-layout\n        , [ metadata-assignment , { required-separation , metadata-assignment } , required-separation ]\n        , when-clause',
    'reactive-rule-declaration\n    ::= "rule" , nominal-name\n        , [ on-clause ]\n        , "{" , declaration-layout\n        , [ metadata-assignment , { required-separation , metadata-assignment } , required-separation ]\n        , { local-value-declaration , required-separation }\n        , when-clause'
)
replace_exact(
    grammar,
    'action-signature-body\n    ::= nominal-name\n        , [ for-clause ]\n        , [ given-clause ]\n        , "{" , declaration-layout\n        , [ metadata-assignment , { required-separation , metadata-assignment } , required-separation ]\n        , [ action-if-clause , required-separation ]',
    'action-signature-body\n    ::= nominal-name\n        , [ for-clause ]\n        , [ given-clause ]\n        , "{" , declaration-layout\n        , [ metadata-assignment , { required-separation , metadata-assignment } , required-separation ]\n        , { local-value-declaration , required-separation }\n        , [ action-if-clause , required-separation ]'
)
replace_exact(
    grammar,
    'message-declaration\n    ::= "message" , nominal-name\n        , [ on-clause ]\n        , "{" , declaration-layout\n        , [ metadata-assignment , { required-separation , metadata-assignment } , required-separation ]\n        , when-clause',
    'message-declaration\n    ::= "message" , nominal-name\n        , [ on-clause ]\n        , "{" , declaration-layout\n        , [ metadata-assignment , { required-separation , metadata-assignment } , required-separation ]\n        , { local-value-declaration , required-separation }\n        , when-clause'
)
replace_exact(
    grammar,
    'start-with-declaration\n    ::= "start" , "with"\n        , "{" , declaration-layout\n        , "things" , start-contribution-body\n        , required-separation\n        , "rules" , start-contribution-body\n        , declaration-layout , "}"\n        ;\n\nstart-contribution-body\n    ::= "{" , declaration-layout\n        , [ expression\n            , { "," , declaration-layout , expression }\n          ]\n        , declaration-layout , "}"\n        ;',
    'start-with-declaration\n    ::= "start" , "with"\n        , ( expression | start-contribution-body )\n        ;\n\nstart-contribution-body\n    ::= "{" , declaration-layout\n        , expression\n        , { "," , declaration-layout , expression }\n        , [ "," ]\n        , declaration-layout , "}"\n        ;'
)
replace_exact(
    grammar,
    'prefix-operator\n    ::= "not" | "+" | "-" | "old" | "allowed" ;',
    'prefix-operator\n    ::= "not" | "+" | "-" | "old" | "allowed" | "all" ;'
)


# ---------------------------------------------------------------------
# Surface AST and semantic IR.
# ---------------------------------------------------------------------

ast = "especificacion/sintaxis/mud-surface-ast.asdl"
replace_exact(
    ast,
    '                   | ReactiveRuleDecl(nominal_name name,\n                                      on_clause? participants,\n                                      metadata_assignment* metadata,\n                                      expression_block activator,',
    '                   | ReactiveRuleDecl(nominal_name name,\n                                      on_clause? participants,\n                                      metadata_assignment* metadata,\n                                      local_value_decl* leading_locals,\n                                      expression_block activator,'
)
replace_exact(
    ast,
    '                   | ActionDecl(action_kind kind,\n                                nominal_name name,\n                                for_clause? participants,\n                                given_clause? givens,\n                                metadata_assignment* metadata,\n                                action_guard? guard,',
    '                   | ActionDecl(action_kind kind,\n                                nominal_name name,\n                                for_clause? participants,\n                                given_clause? givens,\n                                metadata_assignment* metadata,\n                                local_value_decl* leading_locals,\n                                action_guard? guard,'
)
replace_exact(
    ast,
    '                   | LookDecl(nominal_name name,\n                              for_clause? participants,\n                              metadata_assignment* metadata,',
    '                   | LookDecl(nominal_name name,\n                              for_clause? participants,\n                              given_clause? givens,\n                              metadata_assignment* metadata,'
)
replace_exact(
    ast,
    '                   | MessageDecl(nominal_name name,\n                                 on_clause? participants,\n                                 metadata_assignment* metadata,\n                                 expression_block activator,',
    '                   | MessageDecl(nominal_name name,\n                                 on_clause? participants,\n                                 metadata_assignment* metadata,\n                                 local_value_decl* leading_locals,\n                                 expression_block activator,'
)
replace_exact(ast, '    start_set = StartSet(expr* things, expr* rules)', '    start_set = StartSet(expr* contributions)')
replace_exact(
    ast,
    '    prefix_operator = LogicalNot\n                    | UnaryPlus\n                    | UnaryMinus\n                    | OldValue\n                    | AllowedQuery',
    '    prefix_operator = LogicalNot\n                    | UnaryPlus\n                    | UnaryMinus\n                    | OldValue\n                    | AllowedQuery\n                    | EnumerateAll'
)

ir = "especificacion/ir/mud-semantic-ir.asdl"
replace_exact(
    ir,
    '    metadata_kind = NameMetadata | PrivateMetadata | SummaryMetadata | DescriptionMetadata | DeprecatedMetadata',
    '    metadata_kind = NameMetadata | SummaryMetadata | DescriptionMetadata | DeprecatedMetadata'
)
replace_exact(
    ir,
    '    semantic_project = SemanticProject(semantic_decl* declarations,\n                                       semantic_decision_branch* decision_branches,\n                                       dependency_edge* dependencies)',
    '    semantic_project = SemanticProject(semantic_module* modules,\n                                       semantic_decl* declarations,\n                                       semantic_decision_branch* decision_branches,\n                                       dependency_edge* dependencies)\n\n    semantic_module = SemanticModule(string logical_path, string* uses)\n        attributes (source_span origin)'
)
replace_exact(
    ir,
    '    semantic_decl = SemanticDecl(anchor identity,\n                                 string category,',
    '    semantic_decl = SemanticDecl(anchor identity,\n                                 string module_path,\n                                 string category,'
)
replace_exact(ir, '    semantic_start_set = SemanticStartSet(anchor* things, anchor* rules)', '    semantic_start_set = SemanticStartSet(anchor* declarations)')
append_once(
    ir,
    '-- D-096:',
    """-- D-096: el modelo elaborado debe preservar pertenencia modular, `uses`,
-- activación unificada y ausencia de `~private`. La representación exacta de
-- matches causales de trigger permanece deliberadamente abierta; no se fija aquí
-- una codificación interna que cierre la decisión provisional de bindings.
"""
)


# ---------------------------------------------------------------------
# Narrative spec surfaces. They are not promoted beyond their own status;
# the sections below eliminate direct contradiction with D-096.
# ---------------------------------------------------------------------

append_once(
    "especificacion/05-texto-fuente.md",
    "## Frontera física de módulo (D-096)",
    """## Frontera física de módulo (D-096)

Un archivo `.mud` debe pertenecer al módulo determinado por el `mud.module` de su directorio ancestro más cercano. Un `mud.module` anidado abre una nueva frontera y un `.mud` sin ancestro modular es inválido. El nombre lógico del módulo se deriva del MudPath del directorio y no se repite obligatoriamente en el archivo de módulo.

`uses` pertenece a `mud.module` y autoriza dependencias de contrato entre módulos; `using` pertenece a los `.mud` y resuelve/importa nombres. Ninguno sustituye al otro. La gramática completa de `mud.module` permanece abierta en Q-062.
"""
)
append_once(
    "especificacion/09-nombres-y-anclas.md",
    "## Módulos, `uses` y anclas (D-096)",
    """## Módulos, `uses` y anclas (D-096)

La pertenencia a módulo es una dimensión de visibilidad y dependencia, no un componente adicional del ancla nominal. `uses` autoriza el conocimiento del contrato de otro módulo; un `using` no concede esa autorización. La resolución cruzada solo puede alcanzar operaciones y tipos pertenecientes al cierre visible del contrato modular.
"""
)
append_once(
    "especificacion/07-gramatica-concreta.md",
    "## Actualización de superficie por D-096",
    """## Actualización de superficie por D-096

D-096 sustituye dentro de este capítulo cualquier formulación anterior incompatible en cuatro puntos: `look` admite `given`; actions, rules reactivas y messages admiten locales `:=` antes de sus cláusulas de comportamiento; `all D` materializa explícitamente un dominio enumerable y convive con el literal contextual `all`; `start with` ya no separa `things` y `rules`, sino que acepta una expresión o un bloque unificado de contribuciones. La EBNF normativa refleja estas formas.

La sintaxis concreta completa de `mud.module` no se fija aquí mientras Q-062 siga abierta.
"""
)
append_once(
    "especificacion/08-sintaxis-abstracta.md",
    "## Actualización de AST por D-096",
    """## Actualización de AST por D-096

`LookDecl` conserva `given_clause?`; `ActionDecl`, `ReactiveRuleDecl` y `MessageDecl` conservan sus locales previas; `StartSet` contiene una única secuencia de contribuciones y no dos listas `things`/`rules`; `all D` se conserva como `PrefixExpr(EnumerateAll, D)`, mientras el `all` contextual sigue siendo `AllLiteral`.
"""
)
append_once(
    "especificacion/sintaxis/cst-a-ast-superficial.md",
    "## D-096 — `look`, locales, `all D` y `start with`",
    """## D-096 — `look`, locales, `all D` y `start with`

- `look-declaration` proyecta su `given-clause` opcional a `LookDecl.givens`.
- Las `local-value-declaration` situadas entre metadatos y cláusulas de action/rule reactiva/message se proyectan a `leading_locals` de su declaración, no al `EffectBlock` posterior.
- El prefijo `all D` se normaliza como `PrefixExpr(EnumerateAll, D)`; el literal contextual sin operando conserva `AllLiteral`.
- `start-with-declaration` normaliza tanto la forma de una expresión como el bloque de expresiones a un único `StartSet(contributions)` y conserva el orden fuente solo como procedencia, no como semántica de activación.
"""
)

replace_exact(
    "especificacion/README.md",
    "- Definiciones canónicas de `thing` y reglas, `start with` separado en `things` y `rules`, y activaciones mediante `create Nombre`.",
    "- Definiciones canónicas de `thing` y reglas, `start with` unificado por módulo y activaciones mediante `create Nombre`."
)


# ---------------------------------------------------------------------
# Rewrite legacy structured start-with examples in prose and YAML sources.
# This is syntax-only; it does not touch negative historical mentions.
# ---------------------------------------------------------------------

def flatten_actual_start(text: str) -> str:
    pattern = re.compile(
        r"start with \{\s*things\s*\{(?P<things>.*?)\}\s*rules\s*\{(?P<rules>.*?)\}\s*\}",
        re.S,
    )
    def repl(m: re.Match[str]) -> str:
        t = m.group("things").strip()
        r = m.group("rules").strip()
        parts = [p for p in (t, r) if p]
        body = ",\n        ".join(parts)
        return "start with {\n        " + body + "\n    }"
    return pattern.sub(repl, text)


def flatten_escaped_start(text: str) -> str:
    pattern = re.compile(
        r"start with \{\\n\s*things\s*\{(?P<things>.*?)\}\\n\s*rules\s*\{(?P<rules>.*?)\}\\n\s*\}",
        re.S,
    )
    def repl(m: re.Match[str]) -> str:
        t = m.group("things").strip()
        r = m.group("rules").strip()
        parts = [p for p in (t, r) if p]
        body = ", ".join(parts)
        return "start with {\\n        " + body + "\\n    }"
    text = pattern.sub(repl, text)
    inline = re.compile(r"start with \{\s*things \{(?P<things>[^{}]*)\}\s*rules \{(?P<rules>[^{}]*)\}\s*\}")
    return inline.sub(lambda m: "start with { " + ", ".join(x.strip() for x in (m.group('things'), m.group('rules')) if x.strip()) + " }", text)

for p in list((ROOT / "especificacion").rglob("*.md")) + list((ROOT / "aprendizaje").rglob("*.md")):
    text = p.read_text(encoding="utf-8")
    new = flatten_actual_start(text)
    if new != text:
        p.write_text(new, encoding="utf-8")

cases_path = ROOT / "especificacion/sintaxis/casos/cst-ast.yaml"
cases = cases_path.read_text(encoding="utf-8")
cases = flatten_escaped_start(cases)
cases = cases.replace("StartSet(things=[all], rules=[empty, CanGrow])", "StartSet(contributions=[all, empty, CanGrow])")
cases = cases.replace("StartSet(things, rules)", "StartSet(contributions)")
cases = cases.replace("StartSet(things=[AllLiteral(Thing)])", "StartSet(contributions=[PrefixExpr(EnumerateAll, Thing)])")
cases_path.write_text(cases, encoding="utf-8")

# Positive ~private cases are obsolete. Keep negative diagnostics/history only.
cases = cases_path.read_text(encoding="utf-8")
cases = cases.replace("PrivateMetadata", "ExtensionMetadata(private-obsolete)")
cases_path.write_text(cases, encoding="utf-8")

# 07 may still describe ~private positively; make the local chapter explicit.
append_once(
    "especificacion/07-gramatica-concreta.md",
    "`~private` no forma parte de la gramática semántica vigente",
    """### Retirada de `~private`

`~private` no forma parte de la gramática semántica vigente. Una grafía `~private` no adquiere significado estándar por ser léxicamente parecida a un metadato de extensión; la validación contextual debe rechazarla como nombre reservado retirado.
"""
)

print("patch transformation applied")
