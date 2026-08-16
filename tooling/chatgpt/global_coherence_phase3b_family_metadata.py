from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def r(p): return (ROOT/p).read_text(encoding='utf-8')
def w(p,t): (ROOT/p).write_text(t,encoding='utf-8',newline='\n')
def rep(p,o,n,count=1):
    t=r(p); c=t.count(o)
    if c!=count: raise SystemExit(f'{p}: {o!r} count={c} expected={count}')
    w(p,t.replace(o,n,count))

# ---------------------------------------------------------------------
# D-091
# ---------------------------------------------------------------------
d='''---
id: D-091
title: "Identidad de datos de family y anclas de metadatos"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "family, datos asociados, metadatos, anclas subordinadas, reflexión, gramática, CST y AST"
---
# ADR-091 — Identidad de datos de `family` y anclas de metadatos

- Modifica: [[ADR-038-familias-cerradas-de-valores|D-038]] y [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].
- Amplía: [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].

## Contexto

Los datos declarados por una `family` ya constituyen un esquema estable compartido por todos sus miembros, pero D-038 los describía sin identidad propia mientras el capítulo de anclas los agrupaba con la `family`. A la vez, D-087 introdujo valores reflectivos `Metadata` sin asignarles una identidad pública, pese a que tooling y reflexión necesitan poder referirse de forma estable a un metadato configurado concreto.

## Decisión

### Datos declarados de `family`

Cada dato almacenado o calculado declarado directamente en una `family` es un descriptor `Field` estable propiedad de esa `family`. Posee ancla pública subordinada:

```text
family::path.Family::field
```

Usa `FieldKind.Stored` o `FieldKind.Calculated` según corresponda, es siempre inmutable exteriormente y puede poseer metadatos configurados/de usuario mediante un cuerpo de metadatos inmediatamente unido a la declaración:

```mud
family Terrain {
    movementCost: Nat = 1 {
        ~summary = "Coste base de movimiento"
    }

    Plain,
    Mountain { movementCost = 4 }
}
```

El cuerpo del dato contiene exclusivamente declaraciones `~...` y no altera el valor del dato.

### Sobrescrituras por miembro

Una asignación `movementCost = 4` dentro de un miembro es únicamente la sobrescritura del valor efectivo del descriptor `movementCost` para ese miembro. No declara un nuevo `Field`, no posee ancla, no puede poseer metadatos y no crea una identidad `family::Family::Member::movementCost`.

El miembro sí conserva su propia ancla y sus propios metadatos. Por tanto `Mountain~summary` y `Terrain::movementCost~summary` describen entidades distintas, pero no existe un propietario metadata-bearing para la ocurrencia `Mountain.movementCost`.

### Anclas de `Metadata`

Todo metadato estándar configurado o metadato de usuario materializado como valor `Metadata` posee ancla propia. La grafía canónica concatena la ancla del propietario y el nombre de metadato mediante `~`:

```text
thing::game.Person~summary
thing::game.Person::health~description
family::game.Terrain::movementCost~summary
family::game.Terrain::Mountain~deprecated
```

`::` continúa navegando por entidades subordinadas; `~` entra en el espacio de metadatos del propietario. El nombre posterior a `~` es el `~identifier` del descriptor `Metadata`.

Las propiedades intrínsecas `~identifier`, `~anchor`, `~path`, `~file`, `~kind`, `~type` y demás propiedades reflectivas no se convierten por ello en objetos `Metadata` ni reciben una segunda ancla. Solo los valores que aparecen en `owner~metadata` como metadatos configurados o de usuario poseen esta identidad.

`Metadata` expone `~anchor: Anchor`. Esta decisión no añade por mera simetría `~path` ni `~file` al descriptor `Metadata`; esas propiedades solo se incorporarán si su semántica se especifica expresamente.

### Terminalidad

Un valor `Metadata` **no puede poseer metadatos propios**. Su ancla existe para referencia, reflexión y tooling, pero `Metadata` es un descriptor terminal y queda excluido explícitamente del conjunto metadata-bearing. No existe una cadena como `Person~summary~summary`.

## Consecuencias

- los datos de `family` dejan de ser una excepción de identidad y usan el mismo contrato `Field` almacenado/calculado;
- las sobrescrituras de miembro siguen siendo datos del valor, no declaraciones;
- toda metadata materializada tiene identidad estable sin confundirla con propiedades intrínsecas;
- el AST superficial de datos de `family` conserva sus asignaciones de metadatos;
- el AST resuelto de `Metadata` conserva su ancla pública.

## Verificación

1. Dato almacenado y calculado de `family` con ancla estable.
2. Metadata-body válido en una declaración de dato.
3. Rechazo de metadata-body unido a una sobrescritura de miembro.
4. `Field` reflectivo de un dato con `~kind`, `~owner`, `~anchor` y `~metadata` coherentes.
5. Anclas `owner~metadata` para estándar configurado y metadata de usuario.
6. Ausencia de anclas para propiedades intrínsecas.
7. Rechazo de metadata sobre un valor `Metadata`.
8. Una sobrescritura de miembro no crea `family::F::Member::field`.
'''
p=ROOT/'notas/decisiones/ADR-091-identidad-de-datos-family-y-anclas-de-metadatos.md'
if p.exists(): raise SystemExit('D-091 exists')
p.write_text(d,encoding='utf-8',newline='\n')

# ---------------------------------------------------------------------
# Grammar family data metadata body.
# ---------------------------------------------------------------------
p='especificacion/gramatica/mud.ebnf'; t=r(p)
old='''stored-family-data-declaration
    ::= field-name , ":" , type-expression
        , [ "=" , constant-expression ]
        ;

calculated-family-data-declaration
    ::= field-name , [ derived-value-shape ] , ":=" , value-expression
        ;
'''
new='''stored-family-data-declaration
    ::= field-name , ":" , type-expression
        , [ "=" , constant-expression ]
        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]
        ;

calculated-family-data-declaration
    ::= field-name , [ derived-value-shape ] , ":=" , value-expression
        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]
        ;
'''
if old not in t: raise SystemExit('family grammar block')
t=t.replace(old,new,1); w(p,t)

# Syntax kinds mirror exact grammar RHS.
p='especificacion/sintaxis/mud-syntax-kinds.yaml'; t=r(p)
old='''  stored-family-data-declaration:
    kind: StoredFamilyDataDeclarationSyntax
    rhs: "field-name , \":\" , type-expression\\n        , [ \"=\" , constant-expression ]"
    references:
    - field-name
    - type-expression
    - constant-expression
  calculated-family-data-declaration:
    kind: CalculatedFamilyDataDeclarationSyntax
    rhs: field-name , [ derived-value-shape ] , ":=" , value-expression
    references:
    - field-name
    - derived-value-shape
    - value-expression
'''
new='''  stored-family-data-declaration:
    kind: StoredFamilyDataDeclarationSyntax
    rhs: "field-name , \":\" , type-expression\\n        , [ \"=\" , constant-expression ]\\n        , [ \"{\" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , \"}\" ]"
    references:
    - field-name
    - type-expression
    - constant-expression
    - declaration-layout
    - metadata-assignment
    - required-separation
  calculated-family-data-declaration:
    kind: CalculatedFamilyDataDeclarationSyntax
    rhs: "field-name , [ derived-value-shape ] , \":=\" , value-expression\\n        , [ \"{\" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , \"}\" ]"
    references:
    - field-name
    - derived-value-shape
    - value-expression
    - declaration-layout
    - metadata-assignment
    - required-separation
'''
if old not in t: raise SystemExit('syntax kinds family block')
t=t.replace(old,new,1); w(p,t)

# Surface AST data descriptors retain metadata.
p='especificacion/sintaxis/mud-surface-ast.asdl'; t=r(p)
old='''    family_data_decl = StoredFamilyDataDecl(field_name name,
                                            value_shape shape,
                                            expr? default_value)
                     | CalculatedFamilyDataDecl(field_name name,
                                                derived_value_shape? shape,
                                                expr value)
'''
new='''    family_data_decl = StoredFamilyDataDecl(field_name name,
                                            value_shape shape,
                                            expr? default_value,
                                            metadata_assignment* metadata)
                     | CalculatedFamilyDataDecl(field_name name,
                                                derived_value_shape? shape,
                                                expr value,
                                                metadata_assignment* metadata)
'''
if old not in t: raise SystemExit('surface family data')
t=t.replace(old,new,1); w(p,t)

# Resolved metadata has its own public anchor; intrinsic accesses do not instantiate it.
p='especificacion/sintaxis/mud-resolved-ast.asdl'; t=r(p)
old='''    resolved_metadata = ResolvedMetadata(symbol_id owner,
                                         metadata_kind kind,
                                         resolved_type type,
                                         metadata_evaluation evaluation,
                                         resolved_expr value)
'''
new='''    resolved_metadata = ResolvedMetadata(anchor identity,
                                         symbol_id owner,
                                         metadata_kind kind,
                                         resolved_type type,
                                         metadata_evaluation evaluation,
                                         resolved_expr value)
'''
if old not in t: raise SystemExit('resolved metadata')
t=t.replace(old,new,1); w(p,t)

# D-087 current semantics.
p='notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md'; t=r(p)
if '- Modificada por: [[ADR-091-identidad-de-datos-family-y-anclas-de-metadatos|D-091]]' not in t:
    marker='- Amplía: [[ADR-035-organizacion-nombres-using-y-anclas|D-035]], [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]], [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].\n'
    if marker not in t: raise SystemExit('D087 marker')
    t=t.replace(marker,marker+'- Modificada por: [[ADR-091-identidad-de-datos-family-y-anclas-de-metadatos|D-091]].\n',1)
t=t.replace('Por ello pueden ser metadata-bearing las declaraciones nominales ancladas, miembros de `family`, unidades, campos almacenados/calculados/públicos, componentes de alias y participantes `for`/`on`/`given`.', 'Por ello pueden ser metadata-bearing las declaraciones nominales ancladas, miembros de `family`, datos almacenados/calculados declarados por una `family`, unidades, campos almacenados/calculados/públicos, componentes de alias y participantes `for`/`on`/`given`. Un dato de `family` usa descriptor `Field`; una sobrescritura del dato dentro de un miembro no crea descriptor ni propietario metadata-bearing.')
old='''Un valor `Metadata` expone al menos:

```text
~identifier  : Name
~type        : Type
~domain      : Domain
~cardinality : Cardinality
~kind        : MetadataKind
~owner       : Declaration | Field | Component | Participant | FamilyMember | Unit
~calculated  : Bool
```

Las propiedades intrínsecas no se convierten en `Metadata`. Los nombres intrínsecos y estándar reservados no pueden ser ocultados por un metadato de usuario.
'''
new='''Un valor `Metadata` expone al menos:

```text
~identifier  : Name
~anchor      : Anchor
~type        : Type
~domain      : Domain
~cardinality : Cardinality
~kind        : MetadataKind
~owner       : Declaration | Field | Component | Participant | FamilyMember | Unit
~calculated  : Bool
```

Su ancla concatena la ancla del propietario y `~identifier`, por ejemplo `thing::game.Person::health~summary`. Los datos declarados por una `family` son propietarios `Field`, por lo que no requieren una variante adicional de `~owner`.

Las propiedades intrínsecas no se convierten en `Metadata` ni reciben ancla de metadata. Los nombres intrínsecos y estándar reservados no pueden ser ocultados por un metadato de usuario. `Metadata` es terminal: aunque posea ancla pública, no puede tener metadatos propios.
'''
if old not in t: raise SystemExit('D087 Metadata descriptor')
t=t.replace(old,new,1)
t=t.replace('Campos y componentes pueden llevar inmediatamente un cuerpo que contenga solo declaraciones `~...`.', 'Campos, componentes y datos declarados por una `family` pueden llevar inmediatamente un cuerpo que contenga solo declaraciones `~...`.')
w(p,t)

# D-038 becomes current for family identity/metadata; also update member presentation syntax.
p='notas/decisiones/ADR-038-familias-cerradas-de-valores.md'; t=r(p)
marker='- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]\n'
if marker not in t: raise SystemExit('D038 marker')
if 'D-091' not in t:
    t=t.replace(marker,marker+'- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]] y [[ADR-091-identidad-de-datos-family-y-anclas-de-metadatos|D-091]]\n',1)
old='Cada miembro posee un `name: Text` intrínseco cuyo predeterminado es su nombre nominal declarado. Puede sobrescribirse mediante `name = "..."` sin cambiar identidad, igualdad, ancla ni orden. Una sobrescritura idéntica recibe sugerencia de eliminación. En una plantilla `Text`, interpolar un miembro produce su `name` efectivo.'
new='Cada miembro posee `~identifier: Name` y el metadato configurable `~name: Name`, cuyo predeterminado se deriva del identificador nominal. Configurar `~name = "..."` no cambia identidad, igualdad, ancla ni orden. Una configuración idéntica al predeterminado puede recibir sugerencia de eliminación. En una plantilla `Text`, interpolar un miembro usa su presentación `~name` efectiva.'
if old not in t: raise SystemExit('D038 old name')
t=t.replace(old,new,1)
# add metadata body after stored/calculated shapes.
needle='El dato calculado reutiliza la forma general definida por D-037:\n'
addition='Cada declaración de dato posee descriptor `Field`, ancla subordinada a la `family` y puede llevar un cuerpo inmediato formado exclusivamente por declaraciones `~...`. El cuerpo describe el dato para toda la familia; no describe el valor efectivo de un miembro concreto.\n\n'
if addition not in t:
    if needle not in t: raise SystemExit('D038 calculated marker')
    t=t.replace(needle,addition+needle,1)
t=t.replace('Todos los miembros comparten exactamente ese esquema. El subbloque opcional de un miembro contiene únicamente asignaciones que sustituyen los valores predeterminados de datos almacenados; no puede declarar datos nuevos, omitir el nombre del dato asignado, modificar su tipo, dominio o especificación de colección ni asignar un dato calculado.', 'Todos los miembros comparten exactamente ese esquema. El subbloque opcional de un miembro contiene metadatos del propio miembro al comienzo y, después, únicamente asignaciones que sustituyen los valores predeterminados de datos almacenados. Una asignación de miembro no declara un dato nuevo, no posee ancla ni puede llevar metadata-body; tampoco puede modificar tipo, dominio o colección ni asignar un dato calculado.')
old='''Los datos asociados, almacenados o calculados:

- Son inmutables.
- No poseen identidad ni ciclo de vida propios.
- Se consultan como propiedades del valor de familia, por ejemplo `terrain.movementCost`.
- No alteran la identidad ni la igualdad del miembro: siguen dependiendo de la familia nominal y el nombre del miembro.
'''
new='''Los datos asociados declarados, almacenados o calculados:

- Son inmutables.
- Poseen descriptor `Field`, ancla subordinada `family::...::dato` y pueden tener metadatos.
- No poseen ciclo de vida runtime independiente.
- Se consultan como propiedades del valor de familia, por ejemplo `terrain.movementCost`.
- No alteran la identidad ni la igualdad del miembro: siguen dependiendo de la familia nominal y el nombre del miembro.

La sobrescritura de un dato en un miembro es solo un valor efectivo del descriptor de la familia: no tiene ancla ni metadatos propios.
'''
if old not in t: raise SystemExit('D038 no identity block')
t=t.replace(old,new,1)
w(p,t)

# 09: data anchors and metadata anchor namespace.
p='especificacion/09-nombres-y-anclas.md'; t=r(p)
if '  - D-091\n' not in t:
    t=t.replace('  - D-090\n---','  - D-090\n  - D-091\n---',1)
t=t.replace('- miembros de family;\n- unidades declaradas;', '- miembros de family;\n- datos almacenados y calculados declarados por una family;\n- unidades declaradas;',1)
old='''D-087 generaliza `~`: `~identifier` es el identificador fuente, `~name` es presentación configurable y todo acceso `~` es runtime-readonly. Solo poseen metadatos propios entidades semánticas estables con descriptor tipado y ancla pública: declaraciones nominales, miembros de `family`, unidades, campos, componentes y participantes. Se excluyen expresiones, cuerpos de cláusula y ambos `start with` como propietarios; el global continúa sin ancla.

Todo participante `for`, `on` y `given` tiene nombre y ancla subordinada basada en propietario, clase de cláusula e identificador. La posición no forma parte de la identidad. Los participantes son símbolos anclados; los locales ordinarios continúan como `LocalSymbol`. Los miembros heredados conservan descriptor, ancla y metadatos de su declaración original. `~metadata` enumera solo metadatos configurados, nunca propiedades intrínsecas.
'''
new='''D-087 generaliza `~`: `~identifier` es el identificador fuente, `~name` es presentación configurable y todo acceso `~` es runtime-readonly. Poseen metadatos propios entidades semánticas estables con descriptor tipado y ancla pública: declaraciones nominales, miembros de `family`, datos declarados por una `family`, unidades, campos, componentes y participantes. Se excluyen expresiones, cuerpos de cláusula, sobrescrituras de datos en miembros y ambos `start with` como propietarios; el global continúa sin ancla.

Todo participante `for`, `on` y `given` tiene nombre y ancla subordinada basada en propietario, clase de cláusula e identificador. La posición no forma parte de la identidad. Los participantes son símbolos anclados; los locales ordinarios continúan como `LocalSymbol`. Los miembros heredados conservan descriptor, ancla y metadatos de su declaración original. `~metadata` enumera solo metadatos configurados, nunca propiedades intrínsecas.

### Anclas de metadatos

Cada valor `Metadata` configurado o de usuario tiene una ancla obtenida anexando `~identifier` a la ancla de su propietario: `thing::game.Person~summary`, `thing::game.Person::health~description` o `family::game.Terrain::movementCost~summary`. El separador `~` distingue el espacio de metadata del encadenamiento subordinado `::`.

Las propiedades intrínsecas no son valores `Metadata` y no reciben estas anclas. Un valor `Metadata` tampoco puede poseer metadatos propios: la identidad `owner~metadata` es terminal.
'''
if old not in t: raise SystemExit('09 metadata block')
t=t.replace(old,new,1)
w(p,t)

# 08 AST documentation.
p='especificacion/08-sintaxis-abstracta.md'; t=r(p)
if '  - D-091\n' not in t:
    t=t.replace('  - D-090\n---','  - D-090\n  - D-091\n---',1)
t=t.replace('Todo constructor superficial que represente directamente un propietario metadata-bearing conserva una secuencia `metadata_assignment* metadata`. Esto incluye declaraciones nominales admitidas por D-087, unidades, campos, componentes y participantes.', 'Todo constructor superficial que represente directamente un propietario metadata-bearing conserva una secuencia `metadata_assignment* metadata`. Esto incluye declaraciones nominales admitidas por D-087, unidades, campos, componentes, datos declarados por `family` y participantes.')
t=t.replace('Los datos asociados no admiten mutabilidad exterior. Su colección puede conceder capacidad interior sobre `thing` contenidas.\n\nCada `FamilyMember` conserva', 'Los datos asociados no admiten mutabilidad exterior. Su colección puede conceder capacidad interior sobre `thing` contenidas. `StoredFamilyDataDecl` y `CalculatedFamilyDataDecl` conservan además `metadata_assignment* metadata`; cada declaración corresponde a un descriptor `Field` anclado de la familia.\n\nUna `FamilyDataAssignment` dentro de un miembro no contiene metadatos ni crea descriptor/ancla nuevos. Cada `FamilyMember` conserva')
marker='## Declaraciones de `thing`\n'
addition='''Los valores `Metadata` configurados adquieren ancla durante resolución mediante `owner-anchor~metadata-name`. Las propiedades intrínsecas pueden aparecer como `metadata_kind` en un acceso resuelto, pero no instancian `ResolvedMetadata`; este constructor representa únicamente metadata materializada y conserva su propia ancla. `Metadata` no es metadata-bearing.

'''
if addition.strip() not in t:
    if marker not in t: raise SystemExit('08 marker')
    t=t.replace(marker,addition+marker,1)
w(p,t)

# 07 concrete family explanation + provenance.
p='especificacion/07-gramatica-concreta.md'; t=r(p)
if '  - D-091\n' not in t:
    # insert after latest known D-088 if present
    if '  - D-088\n' in t: t=t.replace('  - D-088\n','  - D-088\n  - D-091\n',1)
    else: raise SystemExit('07 D088 marker')
marker='## Uniones de tipos y flechas exteriores\n'
addition='''## `family`

Los datos asociados declarados directamente en una `family` pueden llevar un cuerpo de metadatos igual que un campo o componente:

```mud
family Terrain {
    movementCost: Nat = 1 {
        ~summary = "Coste base"
    }

    Plain,
    Mountain {
        movementCost = 4
    }
}
```

El cuerpo unido a `movementCost: ...` contiene exclusivamente declaraciones `~...` y describe el descriptor del dato para toda la `family`. La asignación `movementCost = 4` dentro de `Mountain` es solo una sobrescritura de valor y no admite cuerpo ni metadatos propios.

'''
if addition.strip() not in t:
    if marker not in t: raise SystemExit('07 union marker')
    t=t.replace(marker,addition+marker,1)
w(p,t)

# CST -> AST transformation doc.
p='especificacion/sintaxis/cst-a-ast-superficial.md'; t=r(p)
marker='## Normalización de colecciones\n'
addition='''## `family`

`stored-family-data-declaration` y `calculated-family-data-declaration` proyectan sus cuerpos `~...` directamente a la secuencia `metadata` de `StoredFamilyDataDecl` o `CalculatedFamilyDataDecl`. El bloque concreto desaparece como agrupación, igual que en campos y componentes.

`family-data-assignment` continúa produciendo únicamente `FamilyDataAssignment(name, value)`: una sobrescritura dentro de un miembro no acepta metadata-body y no fabrica identidad sintáctica adicional.

'''
if addition.strip() not in t:
    if marker not in t: raise SystemExit('cst mapping marker')
    t=t.replace(marker,addition+marker,1)
w(p,t)

# Cases: append structural coverage.
p='especificacion/sintaxis/casos/cst-ast.yaml'; t=r(p)
case='''- id: family-data-metadata
  category: family
  source: "family Terrain {\\n    movementCost: Nat = 1 {\\n        ~summary = \\\"Coste base\\\"\\n    }\\n\\n    Plain,\\n    Mountain { movementCost = 4 }\\n}\\n"
  cst_root: MudFileSyntax
  ast: StoredFamilyDataDecl(movementCost, metadata=[StoredMetadataAssignment(summary)])
  normalizations:
  - family-data-metadata-to-owner
  produces_ast: true
- id: family-data-override-metadata-invalid
  category: validation-before-ast
  source: "family Terrain {\\n    movementCost: Nat = 1\\n    Plain,\\n    Mountain {\\n        movementCost = 4 { ~summary = \\\"No permitido\\\" }\\n    }\\n}\\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - family-data-override-metadata-not-allowed
  produces_ast: false
'''
if 'id: family-data-metadata' not in t:
    t=t.rstrip()+'\n'+case
w(p,t)

print('PHASE3B_FAMILY_METADATA_OK')
