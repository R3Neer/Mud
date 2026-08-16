from pathlib import Path
import sys

ROOT=Path(sys.argv[1]).resolve()

def p(rel): return ROOT/rel
def read(rel): return p(rel).read_text(encoding='utf-8')
def write(rel,text):
    q=p(rel); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(text.rstrip('\n')+'\n',encoding='utf-8',newline='\n')
def exact(text,old,new,label):
    n=text.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1, found {n}')
    return text.replace(old,new,1)
def add_decision(text,d):
    if f'  - {d}\n' in text: return text
    m='decisions:\n'; i=text.find(m)
    if i<0: raise SystemExit('missing decisions frontmatter')
    j=i+len(m)
    while text.startswith('  - ',j): j=text.find('\n',j)+1
    return text[:j]+f'  - {d}\n'+text[j:]

adr='''---
id: D-094
title: "Anclas terminales de metadatos configurados"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "metadatos, reflexión, anclas subordinadas, IR semántico, grafo y tooling"
---

# ADR-094 — Anclas terminales de metadatos configurados

- Precisa: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].
- Amplía: [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]] y [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].

## Decisión

Cada metadato configurado o definido por el autor que se materializa como valor `Metadata` posee una ancla pública subordinada a la de su propietario. La grafía canónica usa el mismo separador `~` del acceso reflectivo:

```text
<ancla-del-propietario>~<identificador-metadata>
```

Ejemplos:

```text
thing::game.Person~summary
thing::game.Person::health~description
family::game.Status::Critical~deprecated
family::game.Status::score~summary
action::game.Attack::for::attacker~summary
```

`::` continúa navegando por entidades semánticas subordinadas; `~` entra en el espacio de metadata del propietario. El identificador posterior a `~` es la forma canónica del nombre del metadato y no introduce una categoría superior `metadata`.

Las propiedades intrínsecas como `~type`, `~path`, `~file`, `~kind` o el propio `~anchor` no son objetos `Metadata`, no aparecen en `~metadata` y no reciben una ancla de metadata. Un acceso intrínseco sigue siendo reflectivo, pero su existencia no materializa un descriptor configurable.

`Metadata` expone `~anchor: Anchor`. Esta decisión no añade por simetría `~path` ni `~file`; esas propiedades requerirían un contrato semántico propio si se desean en el futuro.

## Terminalidad

`Metadata` es un descriptor terminal. Aunque sea una entidad estable y anclada, **no puede poseer metadata propia** y no expone `~metadata`. Esta es una excepción deliberada al principio general de admisión de D-087 y evita una torre recursiva `owner~meta~meta...`.

## IR y resolución

La resolución deriva la ancla del objeto `Metadata` a partir de la ancla resuelta del propietario y del identificador canónico del metadato. No aparece sintaxis fuente nueva ni cambia el AST superficial.

El IR distingue:

- `metadata_kind`: categoría de objetos `Metadata` configurados;
- `metadata_property`: propiedad postfix elaborada, que puede ser intrínseca o referir un `metadata_kind` configurable.

Una propiedad intrínseca nunca se convierte accidentalmente en `SemanticMetadata`.

## Consecuencias

- Los objetos `Metadata` pueden ser referenciados de forma estable por tooling y grafo.
- Renombrar un metadato de usuario cambia su ancla; cambiar su valor no.
- Renombrar/mover el propietario cambia también la ancla subordinada del metadato conforme a la migración ordinaria de anclas.
- La metadata de un miembro de `family` posee ancla bajo el miembro; la sobrescritura de un dato de `family` sigue sin ser un descriptor y no puede poseer metadata.

## Verificación

1. `SemanticMetadata` conserva una ancla propia.
2. `thing::game.Person::health~description` es una ancla válida de metadata configurada.
3. Ninguna propiedad intrínseca aparece como objeto `Metadata` ni recibe ancla de metadata.
4. El descriptor `Metadata` expone `~anchor` y no expone `~metadata`.
5. El AST superficial no cambia por esta decisión.
'''
write('notas/decisiones/ADR-094-anclas-terminales-de-metadatos-configurados.md',adr)

# D-087 debe ser literalmente vigente.
rel='notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md'
t=read(rel)
t=exact(t,
'- Precisada por: [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]], [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]] y [[ADR-092-disponibilidad-estatica-de-propiedades-reflectivas|D-092]].',
'- Precisada por: [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]], [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]], [[ADR-092-disponibilidad-estatica-de-propiedades-reflectivas|D-092]] y [[ADR-094-anclas-terminales-de-metadatos-configurados|D-094]].',
'D087 precisions')
t=exact(t,
'''No lo son expresiones, sentencias, operandos, condiciones, cuerpos de cláusula, tokens, nodos arbitrarios del AST ni ramas funcionales sin descriptor estable. Una rama de diccionario funcional tampoco posee ancla pública: D-090 le asigna únicamente una clave local dentro de su propietario para la representación resuelta. `when`, `if`, `then`, `after` y `otherwise` pueden reflejarse como clases presentes mediante `~clauses`, pero sus cuerpos no se convierten en objetos metadata-bearing.''',
'''No lo son expresiones, sentencias, operandos, condiciones, cuerpos de cláusula, tokens, nodos arbitrarios del AST ni ramas funcionales sin descriptor estable. Una rama de diccionario funcional tampoco posee ancla pública: D-090 le asigna únicamente una clave local dentro de su propietario para el IR semántico. `when`, `if`, `then`, `after` y `otherwise` pueden reflejarse como clases presentes mediante `~clauses`, pero sus cuerpos no se convierten en objetos metadata-bearing.\n\nUn valor `Metadata` configurado sí posee descriptor y ancla propios para reflexión y tooling, pero es **terminal**: no puede poseer metadata propia y no expone `~metadata`. D-094 fija esta excepción deliberada al principio de admisión.''',
'D087 terminal metadata')
t=exact(t,
'''Un valor `Metadata` expone al menos:\n\n```text\n~identifier  : Name\n~type        : Type''',
'''Un valor `Metadata` expone al menos:\n\n```text\n~identifier  : Name\n~anchor      : Anchor\n~type        : Type''',
'D087 metadata anchor property')
t=exact(t,
'''Las propiedades intrínsecas no se convierten en `Metadata`. Los nombres intrínsecos y estándar reservados no pueden ser ocultados por un metadato de usuario.''',
'''Las propiedades intrínsecas no se convierten en `Metadata` y no reciben ancla de metadata. Los nombres intrínsecos y estándar reservados no pueden ser ocultados por un metadato de usuario. La ancla de un metadato configurado se deriva como `<ancla-propietario>~<identificador-metadata>`; cambiar su valor no cambia identidad.''',
'D087 intrinsic distinction')
write(rel,t)

# 09: catálogo de anclas.
rel='especificacion/09-nombres-y-anclas.md'
t=add_decision(read(rel),'D-094')
t=exact(t,
'''type::Nat\ntype::Prefix\n```''',
'''type::Nat\ntype::Prefix\nthing::game.people.Person::friends~summary\n```''',
'09 anchor example')
t=exact(t,
'''La forma canónica es `<categoría>::<nombre-cualificado>` y, para una declaración anidada, añade `::<miembro>` por cada propietario. Los identificadores de MUD no contienen `::`, de modo que la separación es inequívoca.''',
'''La forma canónica es `<categoría>::<nombre-cualificado>` y, para una declaración anidada, añade `::<miembro>` por cada propietario. Un metadato configurado añade `~<identificador-metadata>` a la ancla de su propietario. Los identificadores de MUD no contienen `::` y `~` pertenece al espacio postfix reservado, de modo que ambas separaciones son inequívocas.''',
'09 canonical anchors')
t=exact(t,
'''- participantes `for`, `on` y `given`;\n- tipos incorporados.''',
'''- participantes `for`, `on` y `given`;\n- metadatos configurados y de usuario materializados como `Metadata`;\n- tipos incorporados.''',
'09 anchored list')
t=exact(t,
'''- las ramas de diccionarios funcionales, que se identifican solo de forma local dentro de su diccionario propietario.''',
'''- las ramas de diccionarios funcionales, que se identifican solo de forma local dentro de su diccionario propietario;\n- las propiedades reflectivas intrínsecas, que no materializan objetos `Metadata`.''',
'09 nonanchored list')
t=exact(t,
'''Todo participante `for`, `on` y `given` tiene nombre y ancla subordinada basada en propietario, clase de cláusula e identificador. La posición no forma parte de la identidad. Los participantes son símbolos anclados; los locales ordinarios continúan como `LocalSymbol`. Los miembros heredados conservan descriptor, ancla y metadatos de su declaración original. `~metadata` enumera solo metadatos configurados, nunca propiedades intrínsecas.''',
'''Todo participante `for`, `on` y `given` tiene nombre y ancla subordinada basada en propietario, clase de cláusula e identificador. La posición no forma parte de la identidad. Los participantes son símbolos anclados; los locales ordinarios continúan como `LocalSymbol`. Los miembros heredados conservan descriptor, ancla y metadatos de su declaración original. `~metadata` enumera solo metadatos configurados, nunca propiedades intrínsecas.\n\nCada valor `Metadata` configurado posee a su vez una ancla terminal formada añadiendo `~<identificador-metadata>` a la ancla del propietario, por ejemplo `thing::game.Person::health~description`. Esa ancla sirve para reflexión y tooling; no convierte a `Metadata` en propietario de otros metadatos. `Metadata~anchor` es válido, mientras `Metadata~metadata` no forma parte del contrato.''',
'09 metadata anchors')
write(rel,t)

# D-078 enumera las nuevas entidades ancladas.
rel='notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial.md'
t=read(rel)
t=exact(t,
'''Poseen ancla las declaraciones globales, campos en su propietario original, componentes, datos asociados declarados por una `family`, miembros de `family`, unidades declaradas, participantes `for`/`on`/`given` y tipos incorporados.''',
'''Poseen ancla las declaraciones globales, campos en su propietario original, componentes, datos asociados declarados por una `family`, miembros de `family`, unidades declaradas, participantes `for`/`on`/`given`, metadatos configurados materializados como `Metadata` y tipos incorporados.''',
'D078 metadata anchors')
write(rel,t)

# D-092: terminalidad como disponibilidad estática.
rel='notas/decisiones/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas.md'
t=read(rel)
marker='- Ajustada a la frontera de fases de [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].\n'
if 'D-094' not in t:
    if t.count(marker)!=1: raise SystemExit('D092 relation marker')
    t=t.replace(marker,marker+'- Precisa la terminalidad de `Metadata` conforme a [[ADR-094-anclas-terminales-de-metadatos-configurados|D-094]].\n',1)
t=exact(t,
'''La regla de disponibilidad se aplica también al resto de propiedades reflectivas conforme al conjunto de propietarios de su contrato. Una propiedad cuyo resultado admita ausencia o colección vacía sigue distinguiendo esa ausencia de la inexistencia de la propiedad.''',
'''La regla de disponibilidad se aplica también al resto de propiedades reflectivas conforme al conjunto de propietarios de su contrato. Una propiedad cuyo resultado admita ausencia o colección vacía sigue distinguiendo esa ausencia de la inexistencia de la propiedad. En particular, `Metadata` admite su contrato intrínseco incluido `~anchor`, pero no admite `~metadata`: D-094 lo define como descriptor terminal.''',
'D092 metadata terminal')
write(rel,t)

# IR: separar objeto Metadata de propiedad postfix intrínseca.
rel='especificacion/ir/mud-semantic-ir.asdl'
t=read(rel)
t=exact(t,
'''    metadata_kind = IntrinsicMetadata(string name)\n                  | NameMetadata | PrivateMetadata | SummaryMetadata | DescriptionMetadata | DeprecatedMetadata\n                  | PluralMetadata | AbbreviationMetadata | PrefixesMetadata | FormatMetadata\n                  | ExtensionMetadata(string name)''',
'''    metadata_kind = NameMetadata | PrivateMetadata | SummaryMetadata | DescriptionMetadata | DeprecatedMetadata\n                  | PluralMetadata | AbbreviationMetadata | PrefixesMetadata | FormatMetadata\n                  | ExtensionMetadata(string name)\n\n    metadata_property = IntrinsicProperty(string name)\n                      | ConfiguredProperty(metadata_kind kind)''',
'IR metadata kinds')
t=exact(t,
'''    semantic_metadata = SemanticMetadata(symbol_id owner,\n                                         metadata_kind kind,''',
'''    semantic_metadata = SemanticMetadata(anchor identity,\n                                         symbol_id owner,\n                                         metadata_kind kind,''',
'IR metadata anchor')
t=exact(t,
'''                  | MetadataAccessExpr(semantic_expr receiver,\n                                       metadata_kind metadata,\n                                       semantic_type result_type)''',
'''                  | MetadataAccessExpr(semantic_expr receiver,\n                                       metadata_property metadata,\n                                       semantic_type result_type)''',
'IR metadata access property')
write(rel,t)

# Casos: ancla derivada y terminalidad semántica.
rel='especificacion/sintaxis/casos/cst-ast.yaml'
t=read(rel)
if '- id: configured-metadata-anchor\n' not in t:
    t=t.rstrip()+'''\n- id: configured-metadata-anchor\n  category: metadata\n  source: "thing Nora {\\n    ~summary = \\\"Persona principal\\\"\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: StoredMetadataAssignment(summary, ...)\n  normalizations:\n  - metadata-anchor=thing::Nora~summary\n  - intrinsic-properties-do-not-materialize-metadata\n  produces_ast: true\n- id: metadata-descriptor-terminal\n  category: reflection-contract\n  source: "thing Nora {\\n    ~summary = \\\"Persona principal\\\"\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: StoredMetadataAssignment(summary, ...)\n  semantic_expectations:\n  - configured-metadata-exposes-anchor\n  - metadata-does-not-expose-metadata\n  produces_ast: true\n'''
write(rel,t)

print('METADATA_ANCHOR_TRANSFORM_OK')
