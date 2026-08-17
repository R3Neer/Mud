from pathlib import Path
import os

ROOT=Path(os.environ['MUD_TARGET']).resolve()
def rd(r): return (ROOT/r).read_text(encoding='utf-8')
def wr(r,t): (ROOT/r).write_text(t.rstrip('\n')+'\n',encoding='utf-8',newline='\n')
def one(t,a,b,label):
    n=t.count(a)
    if n!=1: raise SystemExit(f'{label}: expected 1, found {n}')
    return t.replace(a,b,1)

# D-094: Metadata exposes anchor, path and file, but remains terminal.
r='notas/decisiones/ADR-094-anclas-terminales-de-metadatos-configurados.md'; t=rd(r)
t=one(t,
'''`Metadata` expone `~anchor: Anchor`. Esta decisión no añade por simetría `~path` ni `~file`; esas propiedades requerirían un contrato semántico propio si se desean en el futuro.\n''',
'''`Metadata` expone `~anchor: Anchor`, `~path: MudPath` y `~file: MudFile`. `~path` es el path lógico de la entidad propietaria dentro del programa: entrar en el espacio terminal `~<metadata>` no crea un namespace distinto. `~file` identifica el archivo físico en el que está declarada esa configuración de metadata; en una declaración directa coincide normalmente con el archivo del propietario, pero se deriva de la procedencia del propio `Metadata` y no de una copia almacenada del valor del propietario.\n\nEstas tres propiedades son intrínsecas y calculadas del descriptor. No aparecen en `~metadata`, no materializan nuevos objetos `Metadata` y no requieren campos redundantes en el IR cuando puedan derivarse de ancla, propietario y procedencia.\n''','D094 capabilities')
t=one(t,'4. El descriptor `Metadata` expone `~anchor` y no expone `~metadata`.\n5. El AST superficial no cambia por esta decisión.','''4. El descriptor `Metadata` expone `~anchor`, `~path` y `~file` y no expone `~metadata`.
5. `Metadata~path` conserva el path lógico del propietario y `Metadata~file` conserva la procedencia física de la declaración de metadata.
6. El AST superficial no cambia por esta decisión.''','D094 verification')
wr(r,t)

# D-087 descriptor contract.
r='notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md'; t=rd(r)
old='''~identifier  : Name\n~anchor      : Anchor\n~type        : Type\n~domain      : Domain\n~cardinality : Cardinality\n~kind        : MetadataKind\n~owner       : Declaration | Field | Component | Participant | FamilyMember | Unit\n~calculated  : Bool\n'''
new='''~identifier  : Name\n~anchor      : Anchor\n~path        : MudPath\n~file        : MudFile\n~type        : Type\n~domain      : Domain\n~cardinality : Cardinality\n~kind        : MetadataKind\n~owner       : Declaration | Field | Component | Participant | FamilyMember | Unit\n~calculated  : Bool\n'''
t=one(t,old,new,'D087 Metadata descriptor')
needle='''Las propiedades intrínsecas no se convierten en `Metadata` y no reciben ancla de metadata. Los nombres intrínsecos y estándar reservados no pueden ser ocultados por un metadato de usuario. La ancla de un metadato configurado se deriva como `<ancla-propietario>~<identificador-metadata>`; cambiar su valor no cambia identidad.\n'''
replacement=needle+'''\nPara un descriptor `Metadata`, `~path` conserva el `MudPath` lógico de su propietario y `~file` se deriva de la procedencia física de la declaración de metadata. Ninguna de estas propiedades materializa metadata adicional. `Metadata` continúa siendo terminal y no expone `~metadata`.\n'''
t=one(t,needle,replacement,'D087 Metadata capability prose')
wr(r,t)

# Chapter 09.
r='especificacion/09-nombres-y-anclas.md'; t=rd(r)
old='''Cada valor `Metadata` configurado posee a su vez una ancla terminal formada añadiendo `~<identificador-metadata>` a la ancla del propietario, por ejemplo `thing::game.Person::health~description`. Esa ancla sirve para reflexión y tooling; no convierte a `Metadata` en propietario de otros metadatos. `Metadata~anchor` es válido, mientras `Metadata~metadata` no forma parte del contrato.\n'''
new='''Cada valor `Metadata` configurado posee a su vez una ancla terminal formada añadiendo `~<identificador-metadata>` a la ancla del propietario, por ejemplo `thing::game.Person::health~description`. Esa ancla sirve para reflexión y tooling; no convierte a `Metadata` en propietario de otros metadatos.\n\n`Metadata` expone `~anchor`, `~path` y `~file`. Su `~path` es el path lógico de la entidad propietaria y su `~file` procede del archivo físico donde se declaró esa configuración de metadata. Entrar en `~<identificador-metadata>` cambia la identidad terminal, no el namespace lógico. Estas propiedades son intrínsecas del descriptor y no aparecen en la colección `~metadata`. `Metadata~metadata` no forma parte del contrato.\n'''
t=one(t,old,new,'09 Metadata capabilities')
wr(r,t)

# Minimal conformance cases.
r='especificacion/sintaxis/casos/cst-ast.yaml'; t=rd(r)
if 'id: metadata-descriptor-path-file' not in t:
    t += r'''
- id: metadata-descriptor-path-file
  category: validation-after-resolution
  source: "thing Person {\n    ~summary = \"Person descriptor\"\n}\nrule MetadataLocation {\n    forall metadata in Person~metadata: metadata~path == Person~path and metadata~file == Person~file\n}\n"
  cst_root: MudFileSyntax
  semantic_expectations:
  - configured-metadata-exposes-anchor-path-file
  - metadata-path-is-owner-logical-path
  - metadata-file-comes-from-metadata-source-provenance
  produces_ast: true
- id: metadata-descriptor-remains-terminal
  category: validation-after-resolution
  source: "thing Person {\n    ~summary = \"Person descriptor\"\n}\nrule NoMetadataTower {\n    forall metadata in Person~metadata: metadata~metadata~count == 0\n}\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - metadata-descriptor-has-no-metadata-property
  produces_ast: true
'''
wr(r,t)
print('STAGE3_OK')
