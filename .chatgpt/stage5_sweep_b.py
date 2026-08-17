from pathlib import Path
import os

ROOT=Path(os.environ['MUD_TARGET']).resolve()
def r(p): return (ROOT/p).read_text(encoding='utf-8')
def w(p,t): (ROOT/p).write_text(t.rstrip('\n')+'\n',encoding='utf-8',newline='\n')
def one(text,old,new,label):
    n=text.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1, got {n}')
    return text.replace(old,new,1)

# D-054: global start with has mandatory things/rules sections and metadata uses ~.
p='notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md'; t=r(p)
start='### Conjunto inicial `start with`\n'; end='### Inicialización y reactivación\n'
a=t.find(start); b=t.find(end,a)
if a<0 or b<0: raise SystemExit('D054 start section')
section='''### Conjunto inicial `start with`\n\nLas definiciones de `thing` y reglas no quedan activas por aparecer. El único `start with` global separa obligatoriamente ambos universos:\n\n```mud\nstart with {\n    things {\n        Vegetation,\n        Tree\n    }\n\n    rules {\n        CanGrow\n    }\n}\n```\n\nNo existe la forma plana o mezclada. Cada sección recibe expresiones estáticas que aportan cero, una o varias identidades de su categoría: una referencia aporta una, `empty` aporta cero, una colección aporta sus miembros y `all` denota el catálogo estático correspondiente. Una colección de colecciones es inválida. Las identidades repetidas se deduplican y el orden no es observable.\n\nLas expresiones solo pueden depender de información disponible antes de existir mundo runtime. El resultado completo se materializa y valida atómicamente y se estabiliza antes de aceptar acciones externas.\n\nLas acciones, aliases y magnitudes no pertenecen a ninguno de esos conjuntos. Cada test declara un `start with` local con las mismas secciones `things` y `rules`; durante ese test sustituye por completo al global.\n\n'''
t=t[:a]+section+t[b:]
t=t.replace('Las etiquetas reconocidas dentro de una declaración concreta, como `name` y `prefixes` en las declaraciones de unidades o `name =` en un cuerpo de `thing`, son igualmente contextuales y no pertenecen por ello al catálogo general de palabras reservadas.','Los metadatos estándar como `~name` y `~prefixes` usan la gramática general postfix `~`; `name` y `prefixes` no son etiquetas contextuales especiales por esa razón.')
w(p,t)

# D-055: local test start with uses the same structured contract.
p='notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md'; t=r(p)
t=one(t,'''test CounterIncreases {\n    start with {\n        Counter\n    }\n\n    then Counter.value += 1''','''test CounterIncreases {\n    start with {\n        things { Counter }\n        rules { empty }\n    }\n\n    then Counter.value += 1''','D055 example')
# Replace the obsolete schematic subgrammar with the shared declaration.
old='''test-start-with\n    ::= "start" "with" "{"\n        [ declaration-reference\n          { "," declaration-reference }\n        ]\n        "}"\n'''
new='''test-start-with\n    ::= start-with-declaration\n'''
t=one(t,old,new,'D055 schematic grammar')
t=one(t,'''El bloque local conserva la misma naturaleza declarativa que el global:\n\n- Es un conjunto finito y no ordenado.\n- Contiene referencias a definiciones canónicas activables de `thing` y reglas.\n- Separa sus referencias mediante comas y no admite coma final.\n- No contiene instrucciones `create`, asignaciones ni otros efectos.\n- Rechaza referencias repetidas, ambiguas o no activables.''','''El bloque local conserva la misma estructura declarativa que el global de D-085: contiene obligatoriamente las secciones `things { ... }` y `rules { ... }`. Cada una admite contribuciones estáticas de cero, una o varias identidades de su propia categoría mediante referencias, `empty`, colecciones de un nivel o `all` contextual. El orden no es observable y las identidades repetidas se deduplican.\n\nNo contiene instrucciones `create`, asignaciones ni otros efectos, y una contribución de categoría incorrecta o una colección anidada es inválida.''','D055 start prose')
w(p,t)

# D-061: point formatting is metadata and anchors use ordinary postfix reflection.
p='notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text.md'; t=r(p)
for old,new in [
('Dentro del `format` de una magnitud de punto, el propio punto es contextual.','Dentro del `~format` de una magnitud de punto, el propio punto es contextual.'),
('format = "{hour:2}:{minute:2}:{second:2}"','~format = "{hour:2}:{minute:2}:{second:2}"'),
('format = "{week from year:2}"','~format = "{week from year:2}"'),
('La forma incompleta `week from year` solo es válida en un hueco del `format` de una magnitud de punto;','La forma incompleta `week from year` solo es válida en un hueco del `~format` de una magnitud de punto;'),
('La propiedad `format` de una magnitud `point over` usa esta misma sintaxis, no un segundo lenguaje de llaves.','El metadato `~format` de una magnitud `point over` usa esta misma sintaxis, no un segundo lenguaje de llaves.'),
('un campo directo sin `in` publica la coordenada numérica, no el `format`;','un campo directo sin `in` publica la coordenada numérica, no el `~format`;'),
]:
    if old not in t: raise SystemExit(f'D061 stale: {old}')
    t=t.replace(old,new)
# Top-level bullet describing template interpolation.
t=t.replace('- `anchor{d}` inserta el ancla canónica de la entidad designada por `d`;\n','- `{e}` también puede interpolar `e~anchor` cuando la categoría estática de `e` expone esa propiedad;\n')
start='### Interpolación de anclas\n'; end='## Consecuencias\n'
a=t.find(start); b=t.find(end,a)
if a<0 or b<0: raise SystemExit('D061 anchor section')
section='''### Anclas dentro de plantillas\n\nNo existe una interpolación especial `anchor{...}`. D-087 hace de `~anchor` una propiedad reflectiva ordinaria y tipada, por lo que se interpola mediante la sintaxis general de expresiones:\n\n```mud\n"Rule: {CanRecruit~anchor}"\n"Kingdom: {kingdom}; identity: {kingdom~anchor}"\n```\n\nEl acceso solo es válido cuando la categoría estática del receptor expone `~anchor`. La plantilla no introduce un token especial `anchor`.\n\n'''
t=t[:a]+section+t[b:]
t=t.replace('- El AST distingue fragmentos literales, huecos de valor, especificaciones numéricas y huecos de ancla.','- El AST distingue fragmentos literales, huecos de valor y especificaciones numéricas; las anclas usan interpolaciones de expresión ordinarias.')
t=t.replace('- El nombre visible de una `thing` puede diferir de su ancla; `anchor{...}` conserva la identidad canónica.','- La presentación `~name` puede diferir de `~anchor`; ambas son propiedades reflectivas separadas.')
t=t.replace('9. Obtención de anclas de declaraciones y valores nominales mediante `anchor{...}`.\n10. Rechazo de `anchor{...}` sobre valores sin identidad anclada.','9. Obtención de anclas mediante interpolación ordinaria de `expression~anchor`.\n10. Rechazo de `~anchor` cuando la categoría estática del receptor no expone esa propiedad.')
w(p,t)

# D-063: participants are never anonymous; dictionary absence follows D-085.
p='notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md'; t=r(p)
t=one(t,'''Los roles `for` conservan sus reglas de nombre:\n\n- Un rol de cardinalidad exactamente `[1]` puede ser anónimo cuando la resolución del cuerpo es unívoca.\n- Un rol colectivo o exteriormente mutable debe tener nombre.\n- Un rol anónimo solo admite vinculación posicional.\n\nLa forma de receptor multiparte nombrado continúa siendo exacta, exhaustiva y no mezclable con posiciones. Puede reordenar roles, pero el compilador sugiere el orden de declaración. Los receptores posicionales no pueden omitir roles.''','''Todo rol `for` tiene identificador fuente explícito, incluida cardinalidad `[1]`, conforme a D-087. La firma conserva el orden de declaración, pero ese orden no sustituye a la identidad estable del slot.\n\nLa forma de receptor multiparte nombrado continúa siendo exacta, exhaustiva y no mezclable con posiciones. Puede reordenar roles, pero el compilador sugiere el orden de declaración. La declaración de la firma nunca contiene participantes anónimos.''','D063 participants')
t=t.replace('Una lectura de clave ausente puede producir el predeterminado ordinario, pero no concede capacidad interior sobre él como si existiera una asociación.','Una lectura de clave ausente produce `empty` con la forma declarada y no concede capacidad interior como si existiera una asociación.',1)
w(p,t)

# D-068: ~name is metadata; anchors use postfix reflection.
p='notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md'; t=r(p)
t=one(t,'Su ancla canónica es `thing::Thing`; `anchor{Thing}` produce esa escritura.','Su ancla canónica es `thing::Thing`; `Thing~anchor` produce ese valor reflectivo.','D068 builtin anchor')
start='### Propiedad intrínseca `name`\n'; end='## Consecuencias\n'
a=t.find(start); b=t.find(end,a)
if a<0 or b<0: raise SystemExit('D068 name section')
section='''### Metadato estándar `~name`\n\nD-087 retira la propiedad especial `.name` y la asignación contextual `name = ...`. Toda `thing` expone el metadato estándar `~name: Name`. Si no se configura, se deriva del identificador fuente no cualificado; puede configurarse al comienzo del cuerpo mediante la gramática general de metadatos:\n\n```mud\nthing BlackCastle {\n    ~name = "El Castillo Negro"\n}\n```\n\n`~name` pertenece al descriptor y todo acceso `~` es de solo lectura runtime. No se hereda como valor de presentación: una descendiente sin configuración propia deriva su nombre de su propio `~identifier`. Dos `thing` pueden compartir presentación sin compartir identidad. Un campo ordinario `name` pertenece al espacio de miembros y puede coexistir con `~name`.\n\n'''
t=t[:a]+section+t[b:]
t=t.replace('- `name` no introduce estado heredado, conflictos de fusión ni escrituras adicionales.\n- Los campos ordinarios llamados `name` dejan de ser válidos dentro de cuerpos de `thing`; aliases, familias y otros contextos conservan sus propios espacios estructurales.','- `~name` no introduce estado heredado, conflictos de fusión ni escrituras runtime.\n- Un campo ordinario `name` puede coexistir con `~name` porque `.` y `~` pertenecen a espacios distintos.')
t=t.replace('3. Ancla incorporada `thing::Thing` y renderización mediante `anchor{Thing}`.','3. Ancla incorporada `thing::Thing` y lectura reflectiva mediante `Thing~anchor`.')
t=t.replace('10. `{value}` usa `value.name` y `anchor{value}` conserva la identidad canónica.','10. `{value~name}` usa la presentación configurada y `{value~anchor}` conserva la identidad canónica.')
w(p,t)

# D-092: Metadata intrinsic contract now includes path and file as well as anchor.
p='notas/decisiones/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas.md'; t=r(p)
t=one(t,'En particular, `Metadata` admite su contrato intrínseco incluido `~anchor`, pero no admite `~metadata`: D-094 lo define como descriptor terminal.','En particular, `Metadata` admite su contrato intrínseco, incluidos `~anchor`, `~path` y `~file`, pero no admite `~metadata`: D-094 lo define como descriptor terminal.','D092 metadata contract')
w(p,t)

print('STAGE5_SWEEP_B_OK')
