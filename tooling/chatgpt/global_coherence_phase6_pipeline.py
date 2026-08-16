from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def r(p): return (ROOT/p).read_text(encoding='utf-8')
def w(p,t): (ROOT/p).write_text(t,encoding='utf-8',newline='\n')

# ------------------------------------------------------------------
# Preserve the current rich semantic schema as the elaborated layer.
# ------------------------------------------------------------------
old_resolved=r('especificacion/sintaxis/mud-resolved-ast.asdl')
elab=old_resolved
elab=elab.replace('-- MUD 1.0 — Contrato del AST resuelto','-- MUD 1.0 — Contrato del AST tipado y elaborado',1)
elab=elab.replace('-- Complementa mud-surface-ast.asdl. Conserva procedencia y forma semántica,\n-- pero sustituye referencias nominales por símbolos y anclas resueltas.', '-- Se construye a partir de mud-resolved-ast.asdl después del tipado y la\n-- elaboración. Conserva símbolos resueltos y añade tipos, dominios, formas\n-- efectivas, conversiones y evidencias de análisis.',1)
elab=elab.replace('module MUDResolved','module MUDElaborated',1)
elab=elab.replace('resolved_','elaborated_')
elab=elab.replace('Resolved','Elaborated')
# Aclaración en la capa elaborada sobre metadata: su ancla ya viene resuelta.
elab=elab.replace('elaborated_metadata = ElaboratedMetadata(anchor identity,', 'elaborated_metadata = ElaboratedMetadata(anchor identity,',1)
w('especificacion/sintaxis/mud-elaborated-ast.asdl',elab)

# ------------------------------------------------------------------
# Name-resolved layer: deliberately no typing/elaboration payload.
# ------------------------------------------------------------------
resolved='''-- MUD 1.0 — Contrato del AST/HIR resuelto nominalmente
--
-- Complementa mud-surface-ast.asdl. Esta capa fija identidad, símbolos,
-- ámbitos, anclas y destino de referencias, pero NO contiene tipos efectivos,
-- dominios elaborados, cardinalidades inferidas, conversiones ni evidencias
-- de terminación. Esas distinciones pertenecen a mud-elaborated-ast.asdl.

module MUDResolved {

    source_span = (string source, int start, int end)

    anchor = (string canonical)

    symbol_id = AnchoredSymbol(anchor value)
              | LocalSymbol(anchor owner, string kind, string name, int ordinal)

    action_access = PublicAction | Subaction

    decision_branch_key = (symbol_id dictionary, string canonical_selector)

    metadata_kind = IntrinsicMetadata(string name)
                  | NameMetadata | PrivateMetadata | SummaryMetadata | DescriptionMetadata | DeprecatedMetadata
                  | PluralMetadata | AbbreviationMetadata | PrefixesMetadata | FormatMetadata
                  | ExtensionMetadata(string name)

    metadata_evaluation = StoredMetadata | CalculatedMetadata

    resolution_site = (source_span origin, string role)

    resolved_project = ResolvedProject(resolved_decl* declarations,
                                       resolved_reference* references,
                                       resolved_decision_branch* decision_branches,
                                       resolved_start_set? start,
                                       dependency_edge* dependencies)

    resolved_decl = ResolvedDecl(anchor identity,
                                 string category,
                                 action_access? action_visibility,
                                 resolved_metadata* metadata,
                                 resolved_member* members)
        attributes (source_span origin)

    resolved_member = ResolvedMember(symbol_id identity,
                                     string category,
                                     resolved_metadata* metadata)
        attributes (source_span origin)

    resolved_metadata = ResolvedMetadata(anchor identity,
                                         symbol_id owner,
                                         metadata_kind kind,
                                         metadata_evaluation evaluation)
        attributes (source_span origin)

    resolved_reference = ResolvedReference(resolution_site site,
                                           symbol_id target)

    resolved_decision_branch = ResolvedDecisionBranch(decision_branch_key key,
                                                       int source_ordinal,
                                                       string is_fallback,
                                                       symbol_id* external_reads)
        attributes (source_span origin)

    resolved_start_set = ResolvedStartSet(anchor* things, anchor* rules)
        attributes (source_span origin)

    -- El grafo nominal solo contiene aristas cuya identidad puede conocerse
    -- antes del tipado. RefersTo cubre referencias escritas a tipos, dominios
    -- nominales y valores; la capa elaborada clasifica después las aristas
    -- que dependan del tipo efectivo.
    dependency_edge = Owns(symbol_id source, symbol_id target)
                    | Specializes(anchor source, anchor target)
                    | RefersTo(symbol_id source, symbol_id target)
                    | InitializesFrom(symbol_id source, symbol_id target)
                    | CalculatesFrom(symbol_id source, symbol_id target)
                    | Reads(symbol_id source, symbol_id target)
                    | ReadsMetadata(symbol_id source, symbol_id target, metadata_kind metadata)
                    | Writes(symbol_id source, symbol_id target)
                    | CallsAction(anchor source, anchor target)
                    | CallsDecision(anchor source, anchor target)
                    | DecisionDependsOn(decision_branch_key branch, symbol_id target)
                    | Creates(symbol_id source, anchor target)
                    | Destroys(symbol_id source, anchor target)
                    | UnitOf(anchor unit, anchor magnitude)
}
'''
w('especificacion/sintaxis/mud-resolved-ast.asdl',resolved)

# ------------------------------------------------------------------
# D-094 records the phase boundary.
# ------------------------------------------------------------------
adr='''---
id: D-094
title: "Frontera entre AST resuelto y representación elaborada"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "pipeline, AST superficial, resolución nominal, tipado, elaboración, IR, símbolos, anclas y validadores"
---
# ADR-094 — Frontera entre AST resuelto y representación elaborada

- Modifica: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]], [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].

## Contexto

El esquema llamado `mud-resolved-ast.asdl` mezclaba la salida de resolución nominal con datos que solo pueden existir después del tipado y otros análisis: `resolved_type`, dominios elaborados, cardinalidades efectivas, conversiones, narrowing, formas de resultado y `termination_evidence`. Esa mezcla contradecía el pipeline documentado, que situaba tipado/elaboración **después** del AST resuelto.

## Decisión

MUD conserva cuatro fronteras semánticas distintas después de la CST:

```text
CST sin pérdidas
→ Surface AST
→ Resolved AST/HIR nominal
→ Elaborated AST/HIR tipado
→ IR
```

### Surface AST

Conserva la estructura normalizada escrita y las ambigüedades cuyo significado depende de resolución o tipos. No contiene símbolos ni tipos inferidos.

### Resolved AST/HIR nominal

`mud-resolved-ast.asdl` contiene exclusivamente información disponible tras resolución nominal:

- `AnchoredSymbol` y `LocalSymbol`;
- anclas públicas ya determinadas;
- ámbitos y destinos de referencias;
- clase nominal de declaraciones/miembros;
- identidad y propietario de metadata materializada;
- claves locales de ramas decisionales;
- aristas de dependencia cuya identidad no requiere tipado.

No contiene `resolved_type`, dominios efectivos, cardinalidades inferidas, `collection_shape`, `decision_shape`, conversiones, narrowing ni `termination_evidence`.

Una referencia cuya validez final depende de tipo puede quedar nominalmente resuelta a su símbolo y ser aceptada o rechazada después; resolver un nombre no equivale a certificar que su uso es bien tipado.

### Elaborated AST/HIR

`mud-elaborated-ast.asdl` toma la resolución nominal como entrada y añade:

- tipos y dominios efectivos;
- cardinalidades y su procedencia;
- formas de colección y diccionario;
- conversiones y narrowing;
- resultados efectivos de operaciones y accesos;
- evidencia de terminación y otros análisis estáticos necesarios antes del IR.

Esta capa puede conservar las mismas anclas y `symbol_id`; no crea una segunda identidad para las declaraciones.

### IR

El IR sigue siendo una representación posterior orientada a ejecución, tooling y grafo semántico. No se convierte en fuente de verdad: todas las capas son reconstruibles desde `.mud`.

## Consecuencias

- el nombre “AST resuelto” vuelve a significar resolución, no tipado encubierto;
- diagnósticos de nombre pueden producirse sin construir tipos efectivos;
- tooling puede usar símbolos/anclas aunque el tipado posterior falle;
- los datos de análisis que antes estaban prematuramente en `mud-resolved-ast.asdl` pasan al nuevo esquema elaborado;
- el grafo nominal inicial y el grafo semántico elaborado dejan de fingir ser la misma fase.

## Verificación

1. `mud-resolved-ast.asdl` no define tipos efectivos, dominios elaborados, conversiones ni `termination_evidence`.
2. `mud-elaborated-ast.asdl` conserva esas distinciones y referencia los mismos símbolos/anclas.
3. README, capítulos 08/09 y ADR vigentes describen el mismo orden de fases.
4. El validador comprueba que los tres ASDL normativos no contienen tipos ASDL sin definir y que existen los módulos esperados.
5. Un programa puede construir catálogo de símbolos/anclas aunque un error de tipos impida construir la capa elaborada.
'''
p=ROOT/'notas/decisiones/ADR-094-frontera-ast-resuelto-y-elaborado.md'
if p.exists(): raise SystemExit('D-094 exists')
p.write_text(adr,encoding='utf-8',newline='\n')

# ------------------------------------------------------------------
# README syntax models.
# ------------------------------------------------------------------
p='especificacion/sintaxis/README.md'; t=r(p)
t=t.replace('| `mud-resolved-ast.asdl` | Normativo mecánico | Contrato del AST resuelto, tipos unión, símbolos, anclas y dependencias. |', '| `mud-resolved-ast.asdl` | Normativo mecánico | Contrato de la resolución nominal: símbolos, anclas, referencias y grafo inicial. |\n| `mud-elaborated-ast.asdl` | Normativo mecánico | Contrato tipado/elaborado: tipos, dominios, cardinalidades, conversiones y evidencias de análisis. |',1)
t=t.replace('→ AST resuelto\n→ tipado/elaboración\n→ IR','→ AST/HIR resuelto nominalmente\n→ tipado/elaboración\n→ AST/HIR elaborado\n→ IR',1)
t=t.replace('`mud-surface-ast.asdl` puede alimentar generadores de:', 'Los esquemas `mud-surface-ast.asdl`, `mud-resolved-ast.asdl` y `mud-elaborated-ast.asdl` pueden alimentar generadores de:',1)
old='''## Límites

Este directorio no define:

- Resolución de nombres y anclas.
- Subtipado.
- Inferencia de tipos.
- Evaluación estática.
- Semántica de efectos.
- Ondas causales.
- Forma canónica del IR.

Las referencias a esas fases sirven únicamente para impedir que el AST superficial las anticipe.
'''
new='''## Límites

Los ASDL de este directorio fijan **la forma de los contratos entre fases**, no sustituyen las reglas semánticas de los capítulos correspondientes. En particular:

- `mud-resolved-ast.asdl` representa el resultado de nombres, ámbitos y anclas definidos en el capítulo 09;
- `mud-elaborated-ast.asdl` representa resultados de tipado y elaboración, pero las reglas que los calculan pertenecen a los capítulos de tipos, dominios y análisis;
- la semántica de efectos, ondas causales y la forma canónica final del IR continúan fuera de este directorio.

La separación existe precisamente para impedir que una fase anticipe silenciosamente datos de la siguiente.
'''
if old not in t: raise SystemExit('syntax README limits')
t=t.replace(old,new,1); w(p,t)

# ------------------------------------------------------------------
# 08 phase description.
# ------------------------------------------------------------------
p='especificacion/08-sintaxis-abstracta.md'; t=r(p)
if '  - D-094\n' not in t:
    t=t.replace('  - D-093\n','  - D-093\n  - D-094\n',1)
old='El contrato de la fase posterior vive en [[mud-resolved-ast]]. Allí las referencias se sustituyen por `AnchoredSymbol` o `LocalSymbol`, las uniones quedan normalizadas y el grafo nominal se expresa mediante aristas reconstruibles.'
new='El contrato de resolución nominal vive en [[mud-resolved-ast]]: allí las referencias se vinculan a `AnchoredSymbol` o `LocalSymbol` y se construye el grafo nominal inicial. Los tipos efectivos, dominios, cardinalidades, conversiones y evidencias de análisis aparecen solo después en [[mud-elaborated-ast]].'
if old not in t: raise SystemExit('08 phase intro')
t=t.replace(old,new,1)
t=t.replace('→ AST resuelto\n→ tipado y elaboración\n→ IR','→ AST/HIR resuelto nominalmente\n→ tipado y elaboración\n→ AST/HIR elaborado\n→ IR',1)
marker='## Relación con la CST\n'
addition='''## Frontera resuelta y elaborada

El AST/HIR resuelto es deliberadamente nominal. Puede existir aunque la compilación contenga un error de tipos: conserva símbolos, anclas, referencias y dependencias nominales suficientes para diagnósticos y tooling. No normaliza uniones por su significado, no calcula dominios efectivos y no inserta conversiones.

La representación elaborada conserva la misma identidad nominal y añade las decisiones que requieren tipado o análisis estático. `mud-elaborated-ast.asdl` contiene por ello las antiguas estructuras de tipos, `collection_shape`, `decision_shape`, conversiones, narrowing y `termination_evidence` que ya no pertenecen al contrato resuelto.

'''
if addition.strip() not in t:
    if marker not in t: raise SystemExit('08 CST marker')
    t=t.replace(marker,addition+marker,1)
w(p,t)

# ------------------------------------------------------------------
# 09 stages and resolved schema.
# ------------------------------------------------------------------
p='especificacion/09-nombres-y-anclas.md'; t=r(p)
if '  - D-094\n' not in t:
    t=t.replace('  - D-091\n---','  - D-091\n  - D-094\n---',1)
old='''## Etapas

1. El AST superficial aporta nombres y procedencia.
2. La resolución nominal crea símbolos y resuelve declaraciones cuya categoría ya es conocida.
3. El sistema de tipos resuelve uniones, dominios y referencias dependientes del tipo.
4. La resolución de miembros completa accesos, llamadas y abreviaturas contextuales.
'''
new='''## Etapas

1. El AST superficial aporta nombres, estructura y procedencia sin símbolos resueltos.
2. La resolución nominal crea `AnchoredSymbol`/`LocalSymbol`, fija anclas, ámbitos y destinos de referencias que pueden decidirse por nombre, y produce `mud-resolved-ast.asdl`.
3. El sistema de tipos y la elaboración resuelven uniones, dominios, cardinalidades, conversiones y miembros cuya selección depende del tipo; el resultado pertenece a `mud-elaborated-ast.asdl`.
4. El IR recibe únicamente una representación ya elaborada y conserva las identidades nominales anteriores.
'''
if old not in t: raise SystemExit('09 stages')
t=t.replace(old,new,1)
old='El esquema mecánico [[mud-resolved-ast]] representa esta frontera: una declaración persistente y todo participante declarado usan `AnchoredSymbol`; los locales e iteradores ordinarios usan `LocalSymbol` subordinado a su propietario.'
new='El esquema mecánico [[mud-resolved-ast]] representa exclusivamente esta frontera nominal: una declaración persistente y todo participante declarado usan `AnchoredSymbol`; los locales e iteradores ordinarios usan `LocalSymbol` subordinado a su propietario. [[mud-elaborated-ast]] conserva esos símbolos y añade después tipos, dominios, formas efectivas y evidencias de análisis.'
if old not in t: raise SystemExit('09 resolved schema sentence')
t=t.replace(old,new,1); w(p,t)

# ------------------------------------------------------------------
# D-078 current identity + phase boundary.
# ------------------------------------------------------------------
p='notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial.md'; t=r(p)
if 'D-094' not in t:
    t=t.replace('- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]', '- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]], [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]], [[ADR-091-identidad-de-datos-family-y-anclas-de-metadatos|D-091]] y [[ADR-094-frontera-ast-resuelto-y-elaborado|D-094]]',1)
old='Poseen ancla las declaraciones globales, campos en su propietario original, componentes, miembros de family, unidades declaradas y tipos incorporados. Un campo heredado conserva el ancla declarativa del antecesor aunque su estado sea independiente en cada `thing`. Roles, `given`, iteradores, vinculaciones locales y valores globales no nominales solo reciben identidad interna efímera.'
new='Poseen ancla las declaraciones globales, campos en su propietario original, componentes, miembros y datos declarados de `family`, unidades declaradas, participantes nombrados `for`/`on`/`given`, metadatos materializados y tipos incorporados. Un campo heredado conserva el ancla declarativa del antecesor aunque su estado sea independiente en cada `thing`. Iteradores, vinculaciones locales ordinarias, sobrescrituras de datos de `family` y valores globales no nominales solo reciben identidad interna no pública.'
if old not in t: raise SystemExit('D078 identity paragraph')
t=t.replace(old,new,1)
old='La resolución se ejecuta por etapas: primero símbolos nominales, después tipos y dominios, y finalmente miembros dependientes del tipo. La norma usa entornos y conjuntos de candidatos; un scope graph es una implementación posible, no autoridad.'
new='La resolución nominal fija primero símbolos, anclas, ámbitos y referencias decidibles por nombre y produce el AST/HIR resuelto. Tipos, dominios, cardinalidades, conversiones y miembros cuya selección depende del tipo se calculan después en la representación elaborada. La norma usa entornos y conjuntos de candidatos; un scope graph es una implementación posible, no autoridad.'
if old not in t: raise SystemExit('D078 stages')
t=t.replace(old,new,1)
t=t.replace('Tras resolver nombres puede construirse el esqueleto del grafo con aristas de propiedad, especialización, referencia, tipo, dominio, inicialización, cálculo y efecto. El tipado completa y valida aristas posteriores sin impedir construir este grafo nominal inicial.', 'Tras resolver nombres puede construirse el esqueleto del grafo con identidad, propiedad, especialización y referencias nominales, además de dependencias cuya fuente y destino ya sean conocidos. La representación elaborada clasifica y completa aristas de tipo, dominio y otras relaciones que dependan del tipo efectivo sin impedir construir antes este grafo nominal inicial.',1)
w(p,t)

# ------------------------------------------------------------------
# D-051 reconstructibility across explicit layers.
# ------------------------------------------------------------------
p='notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles.md'; t=r(p)
if 'D-094' not in t:
    marker='- Ampliada por: [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]]\n'
    if marker not in t: raise SystemExit('D051 marker')
    t=t.replace(marker,marker+'- Modificada por: [[ADR-094-frontera-ast-resuelto-y-elaborado|D-094]]\n',1)
t=t.replace('Los archivos `.mud` y sus decisiones de versión son la única fuente semántica. El AST, la tabla de símbolos, el grafo y el IR se reconstruyen a partir de ella.', 'Los archivos `.mud` y sus decisiones de versión son la única fuente semántica. CST, AST superficial, AST/HIR resuelto, representación elaborada, tabla de símbolos, grafo e IR se reconstruyen a partir de ella.',1)
needle='El AST conserva forma escrita y procedencia. El IR conserva significado resuelto y debe:\n'
new='El AST superficial conserva forma escrita y procedencia. La capa resuelta conserva identidad nominal; la elaborada conserva tipos, dominios y análisis estáticos. El IR conserva el significado ya elaborado y debe:\n'
if needle not in t: raise SystemExit('D051 AST line')
t=t.replace(needle,new,1)
w(p,t)

# ------------------------------------------------------------------
# D-070 phase chain.
# ------------------------------------------------------------------
p='notas/decisiones/ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado.md'; t=r(p)
if 'D-094' not in t:
    t=t.replace('- Ampliada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]', '- Ampliada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]] y [[ADR-094-frontera-ast-resuelto-y-elaborado|D-094]]',1)
t=t.replace('→ AST resuelto\n→ tipado/elaboración\n→ IR','→ AST/HIR resuelto nominalmente\n→ tipado/elaboración\n→ AST/HIR elaborado\n→ IR',1)
t=t.replace('Estas decisiones pertenecen al AST resuelto o elaborado.', 'La resolución de identidad pertenece al AST/HIR resuelto; toda decisión que requiera tipos efectivos pertenece a la representación elaborada.',1)
w(p,t)

# ------------------------------------------------------------------
# Validator now checks all normative ASDL contracts.
# ------------------------------------------------------------------
p='especificacion/sintaxis/validate_syntax_model.py'; t=r(p)
old='''    asdl_path = root / "especificacion/sintaxis/mud-surface-ast.asdl"

    syntax_productions = production_names(grammar)
'''
new='''    asdl_path = root / "especificacion/sintaxis/mud-surface-ast.asdl"
    resolved_asdl_path = root / "especificacion/sintaxis/mud-resolved-ast.asdl"
    elaborated_asdl_path = root / "especificacion/sintaxis/mud-elaborated-ast.asdl"

    syntax_productions = production_names(grammar)
'''
if old not in t: raise SystemExit('validator paths')
t=t.replace(old,new,1)
needle='''    for unknown in sorted(asdl_used - asdl_defined - {"int", "string", "identifier"}):
        problems.append(Problem(str(asdl_path), f"tipo ASDL no definido: {unknown}"))

    cases_path = root / "especificacion/sintaxis/casos/cst-ast.yaml"
'''
addition='''    for unknown in sorted(asdl_used - asdl_defined - {"int", "string", "identifier"}):
        problems.append(Problem(str(asdl_path), f"tipo ASDL no definido: {unknown}"))

    for semantic_asdl, module_name in (
        (resolved_asdl_path, "MUDResolved"),
        (elaborated_asdl_path, "MUDElaborated"),
    ):
        if not semantic_asdl.is_file():
            problems.append(Problem(str(semantic_asdl), "falta esquema ASDL normativo"))
            continue
        defined, used = asdl_types_and_uses(semantic_asdl)
        for unknown in sorted(used - defined - {"int", "string", "identifier"}):
            problems.append(Problem(str(semantic_asdl), f"tipo ASDL no definido: {unknown}"))
        if f"module {module_name}" not in semantic_asdl.read_text(encoding="utf-8"):
            problems.append(Problem(str(semantic_asdl), f"falta módulo requerido: {module_name}"))

    cases_path = root / "especificacion/sintaxis/casos/cst-ast.yaml"
'''
if needle not in t: raise SystemExit('validator insertion')
t=t.replace(needle,addition,1)
w(p,t)

print('PHASE6_PIPELINE_OK')
