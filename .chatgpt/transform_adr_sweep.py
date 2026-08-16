from pathlib import Path
import sys
ROOT=Path(sys.argv[1]).resolve()
def r(p): return (ROOT/p).read_text(encoding='utf-8')
def w(p,t): (ROOT/p).write_text(t.rstrip('\n')+'\n',encoding='utf-8',newline='\n')
def one(p,o,n,label=None):
    t=r(p); c=t.count(o)
    if c!=1: raise SystemExit(f'{label or p}: expected 1 occurrence, got {c}: {o[:90]!r}')
    w(p,t.replace(o,n,1))
def add_relation(p, anchor, line):
    t=r(p)
    if line in t: return
    if anchor not in t: raise SystemExit(f'{p}: relation anchor missing')
    w(p,t.replace(anchor,anchor+line,1))

D87='- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n'

# D-028: units use general metadata.
p='notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades.md'; t=r(p)
for old,new in [
('''    root unit meter {\n        name = "meter"\n        plural = "meters"\n        abbreviation = "m"\n    }''','''    root unit meter {\n        ~name = "meter"\n        ~plural = "meters"\n        ~abbreviation = "m"\n    }'''),
('El identificador determina el nombre intrínseco y el ancla. `name`, `plural`, `abbreviation` y `prefixes` son opcionales.','El identificador determina `~identifier` y el ancla. `~name`, `~plural`, `~abbreviation` y `~prefixes` son metadatos configurables conforme a D-076 y D-087.'),
('''unit minute := 60 seconds {\n    name = "minute"\n    plural = "minutes"\n    abbreviation = "min"\n}''','''unit minute := 60 seconds {\n    ~name = "minute"\n    ~plural = "minutes"\n    ~abbreviation = "min"\n}'''),
('La ausencia de la propiedad `prefixes` no habilita prefijos. `prefixes = empty` es equivalente, `prefixes = all` habilita el catálogo decimal SI completo y `prefixes = [p1, p2, ...]` habilita solo el subconjunto enumerado. La forma desnuda `prefixes` no es válida.','`~prefixes` tiene tipo `Prefix [* unique]` y valor predeterminado `empty`. `~prefixes = all` selecciona el dominio incorporado completo y `~prefixes = [p1, p2, ...]` una colección explícita. No existe una subgramática especial de propiedades de unidad.'),
('''    unit fastie := 1 m/s {\n        name = "fastie"\n        plural = "fasties"\n        abbreviation = "fst"\n    }''','''    unit fastie := 1 m/s {\n        ~name = "fastie"\n        ~plural = "fasties"\n        ~abbreviation = "fst"\n    }'''),
]:
    if t.count(old)!=1: raise SystemExit(f'D028 stale block: {old[:60]!r}')
    t=t.replace(old,new,1)
if 'ADR-087-metadatos' not in t.split('## Contexto',1)[0]:
    marker='- Ampliada por: [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]]\n'
    if marker not in t: raise SystemExit('D028 relation marker')
    t=t.replace(marker,marker+D87,1)
w(p,t)

# D-029: point presentation is ~format metadata.
p='notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos.md'; t=r(p)
for old,new in [
('    format = "{day}:{hour:2}:{minute:2}"','    ~format = "{day}:{hour:2}:{minute:2}"'),
('    format = "{hour:2}:{minute:2}"','    ~format = "{hour:2}:{minute:2}"'),
('    format = "{hour:2}:{minute:2}:{second:2}"','    ~format = "{hour:2}:{minute:2}:{second:2}"'),
('Puede declarar mediante el `format` opcional una representación textual especial.','Puede declarar mediante el metadato `~format` opcional una representación textual especial.'),
('Conforme a D-061, el formato es una plantilla `Text`:', 'Conforme a D-061, `~format` usa una plantilla `Text`:'),
('D-062 exige que el formato de punto sea invertible', 'D-062 exige que `~format` sea invertible'),
('11. `format` opcional y representación cuantitativa ordinaria, con unidad, cuando se omite.', '11. `~format` opcional y representación cuantitativa ordinaria, con unidad, cuando se omite.'),
]:
    if old not in t: raise SystemExit(f'D029 stale text: {old[:60]!r}')
    t=t.replace(old,new)
if 'ADR-087-metadatos' not in t.split('## Contexto',1)[0]:
    marker='- Modificada por: [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]], [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]], [[notas/decisiones/ADR-062-literales-canonicos-de-magnitudes-de-punto|D-062]] y [[ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]]\n'
    if marker not in t: raise SystemExit('D029 relation marker')
    t=t.replace(marker,marker+D87,1)
w(p,t)

# D-035: metadata names no longer contextual labels; anchor{} retired.
p='notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas.md'; t=r(p)
for old,new in [
('D-038, D-054 y D-055 distinguen las palabras reservadas de las contextuales. Una palabra contextual se reconoce únicamente en una posición gramatical concreta y puede ser un identificador ordinario fuera de ella. `start` es contextual en `start with`; `abstract` lo es delante de `thing`; `always` lo es delante de `rule`; y etiquetas como `name` o `prefixes` lo son dentro de las declaraciones que las definen.','D-038, D-054 y D-055 distinguen las palabras reservadas de las contextuales. Una palabra contextual se reconoce únicamente en una posición gramatical concreta y puede ser un identificador ordinario fuera de ella. `start` es contextual en `start with`; `abstract` lo es delante de `thing`; `always` lo es delante de `rule`. Los metadatos como `~name` o `~prefixes` usan la gramática general postfix `~`, no etiquetas contextuales especiales.'),
('`using`, `with`, `family`, `test`, `otherwise`, `ordered` y el tipo incorporado `Thing` son palabras reservadas. En particular, `ordered` no puede usarse como identificador aunque aparezca fuera de una declaración `family` o de una especificación de colección. `name` es contextual dentro de un cuerpo de `thing` cuando aparece seguido de `=`; no queda reservado en los demás espacios nominales.','`using`, `with`, `family`, `test`, `otherwise`, `ordered` y el tipo incorporado `Thing` son palabras reservadas. En particular, `ordered` no puede usarse como identificador aunque aparezca fuera de una declaración `family` o de una especificación de colección. `name` no tiene una excepción sintáctica de cuerpo de `thing`: la presentación estándar se configura como `~name`, en un espacio distinto del de campos ordinarios.'),
('D-061 añade `anchor{...}` como forma contextual exclusiva de una plantilla `Text`. Produce la escritura canónica del ancla de una declaración o de un valor con identidad nominal anclada, sin convertir las declaraciones en valores ordinarios ni reservar `anchor` fuera de ese contexto.','D-087 retira `anchor{...}`. El ancla canónica se obtiene mediante el acceso ordinario `expression~anchor` y una plantilla la interpola como cualquier otra expresión: `"{expression~anchor}"`.'),
('9. Interpolación contextual de un ancla y uso ordinario de `anchor` fuera de plantillas.','9. Lectura de un ancla mediante `~anchor` e interpolación mediante un hueco de expresión ordinario.'),
]:
    if old not in t: raise SystemExit(f'D035 stale text: {old[:60]!r}')
    t=t.replace(old,new,1)
if 'ADR-087-metadatos' not in t.split('## Decisión',1)[0]:
    marker='- Modificada además por: [[notas/decisiones/ADR-065-cabecera-using-de-fichero|D-065]]\n'
    if marker not in t: raise SystemExit('D035 marker')
    t=t.replace(marker,marker+D87,1)
w(p,t)

# D-036: participants are always named.
p='notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md'; t=r(p)
start='El nombre de un participante `on`, o de un participante `for` cuya cardinalidad efectiva sea exactamente `[1]`, puede omitirse.'
end='También son roles válidos los valores sin identidad runtime:'
a=t.find(start); b=t.find(end,a)
if a<0 or b<0: raise SystemExit('D036 anonymous range')
replacement='''Todo participante `for`, `on` y `given` debe declarar un identificador fuente explícito. La cardinalidad `[1]` no crea una excepción anónima. Los miembros se acceden a través de ese identificador y no se proyectan implícitamente al ámbito del cuerpo.\n\n```mud\nrule IsDestroyed for army: Army {\n    army.soldiers == 0\n}\n\nrule CanGovern for person: Person, kingdom: Kingdom {\n    person.age >= 18 and kingdom.treasury > 0\n}\n```\n\nEl identificador forma parte del slot de firma y, conforme a D-087, participa junto con la clase de cláusula en su ancla subordinada. Reordenar participantes no cambia esa identidad. Una colección sigue sin proyectar implícitamente los campos de sus miembros.\n\n'''
t=t[:a]+replacement+t[b:]
t=t.replace('- La omisión del nombre de participante individual es azúcar sometido a resolución estática no ambigua, no una firma distinta.\n','- Todo participante tiene nombre y ancla subordinada estable conforme a D-087.\n')
t=t.replace('1. Participante individual anónimo y nombrado.\n2. Varios participantes individuales anónimos con accesos unívocos y rechazo de un acceso ambiguo.','1. Participantes `for`, `on` y `given` siempre nombrados y rechazo de la forma anónima.\n2. Acceso a miembros únicamente a través del identificador del participante.')
t=t.replace('13. Nombre obligatorio para cardinalidad distinta de `[1]` y para mutabilidad exterior.','13. Nombre obligatorio para toda cardinalidad, incluida `[1]`, y para mutabilidad exterior.')
if 'ADR-087-metadatos' not in t.split('## Decisión',1)[0]:
    marker='- Modificada por: [[ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]]\n'
    if marker in t: t=t.replace(marker,marker+D87,1)
w(p,t)

# D-037: omitted cardinality, normal .name field, derived shapes.
p='notas/decisiones/ADR-037-campos-y-dominios-declarativos.md'; t=r(p)
old='''- Todo campo denota una colección conforme a D-026; omitir cardinalidad equivale a `[1]`.\n- Dentro de una `thing`, `name` designa la propiedad intrínseca fijada por D-068 y no puede declararse como campo ordinario.'''
new='''- Todo campo denota una colección conforme a D-026. En un campo almacenado inmutable con inicializador, una cardinalidad omitida se infiere de la forma exterior exacta del valor conforme a D-085; en un campo exteriormente mutable conserva `[1]`.\n- `~name` pertenece al espacio de metadatos de D-087. Un campo ordinario llamado `name` pertenece al espacio de miembros y no lo oculta.'''
if old not in t: raise SystemExit('D037 field bullets')
t=t.replace(old,new,1)
old='''El dominio precede a la especificación de colección. Un campo calculado usa exclusivamente:\n\n```text\nnombre [ : tipo ] := expresión\n```'''
new='''El dominio precede a la especificación de colección. Un campo calculado usa:\n\n```text\nnombre [ forma-derivada ] := expresión\n```\n\ndonde la forma derivada puede declarar tipo y, conforme a D-075, dominio, cardinalidad y modificadores de colección compatibles con el resultado.'''
if old not in t: raise SystemExit('D037 calculated shape')
t=t.replace(old,new,1)
t=t.replace('Los campos calculados también deben satisfacer el dominio de su tipo estático cuando se evalúan, aunque no puedan declarar una cláusula `in` adicional.','Los campos calculados deben satisfacer tanto el dominio de su tipo estático como cualquier dominio `in` declarado en su forma derivada. Ese dominio puede ser explícito o derivarse conforme a D-075.',1)
t=t.replace('3. Campo almacenado fuera de dominio y rechazo de `in` sobre un campo calculado.','3. Campo almacenado fuera de dominio y `in` válido sobre un campo calculado conforme a su forma derivada.',1)
t=t.replace('6. Rechazo de `mut` y de especificaciones de colección en campos calculados.','6. Rechazo de `mut` exterior en campos calculados y aceptación de capacidad interior/modificadores declarados por su forma derivada cuando sean compatibles.',1)
w(p,t)

# D-039: dictionary unique is value-unique; missing lookup is empty.
p='notas/decisiones/ADR-039-colecciones-y-diccionarios.md'; t=r(p)
old='''declara un diccionario con claves únicas. `unique` no se aplica porque la unicidad de clave es intrínseca y escribirlo es un error estático. Tampoco se reinterpreta como unicidad de valores: esa restricción debe expresarse, si se incorpora en el futuro, mediante una construcción distinta y explícita.'''
new='''declara un diccionario con claves intrínsecamente únicas. El modificador `unique`, cuando se escribe, se aplica a los **valores asociados** conforme a D-085: exige que un mismo valor no quede asociado a más de una clave. Una inserción o sustitución que violaría esa unicidad es una no-op completa y no produce `failed`.'''
if old not in t: raise SystemExit('D039 unique')
t=t.replace(old,new,1)
t=t.replace('Leer una clave ausente produce el predeterminado del tipo de valor cuando la lectura exige un valor. D-017 y Q-047 gobiernan la existencia y selección de ese predeterminado. Los contextos que preserven ausencia deberán hacerlo mediante cardinalidad, no mediante `null`.','Leer una clave ausente produce `empty` con la forma de salida declarada. La ausencia no produce `failed` por sí misma; solo un contexto posterior cuyo tipo, dominio o cardinalidad no admita cero elementos puede fallar. No se usa `null` ni se sustituye silenciosamente por el predeterminado del tipo de valor.',1)
t=t.replace('4. Lectura, escritura y retirada de clave ausente.','4. Lectura ausente como `empty`, escritura y retirada de clave ausente, y `unique` global sobre valores.',1)
w(p,t)

# D-054: structured global start with and metadata spelling.
p='notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md'; t=r(p)
start='### Conjunto inicial `start with`\n'; end='### Inicialización y reactivación\n'
a=t.find(start); b=t.find(end,a)
if a<0 or b<0: raise SystemExit('D054 start section')
section='''### Conjunto inicial `start with`\n\nLas definiciones de `thing` y reglas no quedan activas por aparecer. El único `start with` global separa obligatoriamente ambos universos:\n\n```mud\nstart with {\n    things {\n        Vegetation,\n        Tree\n    }\n\n    rules {\n        CanGrow\n    }\n}\n```\n\nNo existe la forma plana o mezclada. Cada sección recibe expresiones estáticas que aportan cero, una o varias identidades de su categoría: una referencia aporta una, `empty` aporta cero, una colección aporta sus miembros y `all` denota el catálogo estático correspondiente. Una colección de colecciones es inválida. Las identidades repetidas se deduplican y el orden no es observable.\n\nLas expresiones solo pueden depender de información disponible antes de existir mundo runtime. El resultado completo se materializa y valida atómicamente y se estabiliza antes de aceptar acciones externas.\n\nLas acciones, aliases y magnitudes no pertenecen a ninguno de esos conjuntos. Cada test declara un `start with` local con las mismas secciones `things` y `rules`; durante ese test sustituye por completo al global.\n\n'''
t=t[:a]+section+t[b:]
t=t.replace('Las etiquetas reconocidas dentro de una declaración concreta, como `name` y `prefixes` en las declaraciones de unidades o `name =` en un cuerpo de `thing`, son igualmente contextuales y no pertenecen por ello al catálogo general de palabras reservadas.','Los metadatos estándar como `~name` y `~prefixes` usan la gramática general postfix `~`; `name` y `prefixes` no son etiquetas contextuales especiales por esa razón.')
if 'ADR-085' not in t.split('## Contexto',1)[0]:
    marker='- Documentos afectados:'
    t=t.replace(marker,'- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].\n'+marker,1)
w(p,t)

# D-055: structured local test start with.
p='notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md'; t=r(p)
old='''El bloque local conserva la misma naturaleza declarativa que el global:\n\n- Es un conjunto finito y no ordenado.\n- Contiene referencias a definiciones canónicas activables de `thing` y reglas.\n- Separa sus referencias mediante comas y no admite coma final.\n- No contiene instrucciones `create`, asignaciones ni otros efectos.\n- Rechaza referencias repetidas, ambiguas o no activables.'''
new='''El bloque local conserva la misma estructura declarativa que el global de D-085: contiene obligatoriamente las secciones `things { ... }` y `rules { ... }`. Cada una admite contribuciones estáticas de cero, una o varias identidades de su propia categoría mediante referencias, `empty`, colecciones de un nivel o `all` contextual. El orden no es observable y las identidades repetidas se deduplican.\n\nNo contiene instrucciones `create`, asignaciones ni otros efectos, y una contribución de categoría incorrecta o una colección anidada es inválida.'''
if old not in t: raise SystemExit('D055 start prose')
t=t.replace(old,new,1)
if 'ADR-085' not in t.split('## Contexto',1)[0]:
    marker='- Ampliada además por: [[ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]]\n'
    if marker not in t: raise SystemExit('D055 relation marker')
    t=t.replace(marker,marker+'- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].\n',1)
w(p,t)

# D-061: ~format and ordinary ~anchor interpolation.
p='notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text.md'; t=r(p)
for old,new in [
('Dentro del `format` de una magnitud de punto, el propio punto es contextual.','Dentro del `~format` de una magnitud de punto, el propio punto es contextual.'),
('format = "{hour:2}:{minute:2}:{second:2}"','~format = "{hour:2}:{minute:2}:{second:2}"'),
('format = "{week from year:2}"','~format = "{week from year:2}"'),
('La forma incompleta `week from year` solo es válida en un hueco del `format` de una magnitud de punto;','La forma incompleta `week from year` solo es válida en un hueco del `~format` de una magnitud de punto;'),
('La propiedad `format` de una magnitud `point over` usa esta misma sintaxis, no un segundo lenguaje de llaves.','El metadato `~format` de una magnitud `point over` usa esta misma sintaxis, no un segundo lenguaje de llaves.'),
('un campo directo sin `in` publica la coordenada numérica, no el `format`;','un campo directo sin `in` publica la coordenada numérica, no el `~format`;'),
]:
    if old not in t: raise SystemExit(f'D061 stale {old[:60]!r}')
    t=t.replace(old,new)
start='### Interpolación de anclas\n'; end='## Consecuencias\n'
a=t.find(start); b=t.find(end,a)
if a<0 or b<0: raise SystemExit('D061 anchor section')
section='''### Anclas dentro de plantillas\n\nNo existe una interpolación especial `anchor{...}`. D-087 hace de `~anchor` una propiedad reflectiva ordinaria y tipada, por lo que se interpola mediante la sintaxis general de expresiones:\n\n```mud\n"Rule: {CanRecruit~anchor}"\n"Kingdom: {kingdom}; identity: {kingdom~anchor}"\n```\n\nEl acceso solo es válido cuando la categoría estática del receptor expone `~anchor`. La plantilla no introduce un token especial `anchor`.\n\n'''
t=t[:a]+section+t[b:]
t=t.replace('- El AST distingue fragmentos literales, huecos de valor, especificaciones numéricas y huecos de ancla.','- El AST distingue fragmentos literales, huecos de valor y especificaciones numéricas; las anclas usan interpolaciones de expresión ordinarias.')
t=t.replace('- El nombre visible de una `thing` puede diferir de su ancla; `anchor{...}` conserva la identidad canónica.','- La presentación `~name` puede diferir de `~anchor`; ambas son propiedades reflectivas separadas.')
t=t.replace('9. Obtención de anclas de declaraciones y valores nominales mediante `anchor{...}`.\n10. Rechazo de `anchor{...}` sobre valores sin identidad anclada.','9. Obtención de anclas mediante interpolación ordinaria de `expression~anchor`.\n10. Rechazo de `~anchor` cuando la categoría estática del receptor no expone esa propiedad.')
if 'ADR-087-metadatos' not in t.split('## Contexto',1)[0]:
    marker='- Documentos afectados:'
    t=t.replace(marker,D87+marker,1)
w(p,t)

# D-063: participant declarations are never anonymous.
p='notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md'; t=r(p)
old='''Los roles `for` conservan sus reglas de nombre:\n\n- Un rol de cardinalidad exactamente `[1]` puede ser anónimo cuando la resolución del cuerpo es unívoca.\n- Un rol colectivo o exteriormente mutable debe tener nombre.\n- Un rol anónimo solo admite vinculación posicional.\n\nLa forma de receptor multiparte nombrado continúa siendo exacta, exhaustiva y no mezclable con posiciones. Puede reordenar roles, pero el compilador sugiere el orden de declaración. Los receptores posicionales no pueden omitir roles.'''
new='''Todo rol `for` tiene identificador fuente explícito, incluida cardinalidad `[1]`, conforme a D-087. La firma conserva el orden de declaración, pero ese orden no sustituye a la identidad estable del slot.\n\nLa forma de receptor multiparte nombrado continúa siendo exacta, exhaustiva y no mezclable con posiciones. Puede reordenar roles, pero el compilador sugiere el orden de declaración. La declaración de la firma nunca contiene participantes anónimos.'''
if old not in t: raise SystemExit('D063 anonymous block')
t=t.replace(old,new,1)
if 'ADR-087-metadatos' not in t.split('## Contexto',1)[0]:
    marker='- Documentos afectados:'
    t=t.replace(marker,D87+marker,1)
w(p,t)

# D-068: ~name metadata and ordinary ~anchor.
p='notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md'; t=r(p)
t=t.replace('Su ancla canónica es `thing::Thing`; `anchor{Thing}` produce esa escritura.','Su ancla canónica es `thing::Thing`; `Thing~anchor` produce ese valor reflectivo.',1)
start='### Propiedad intrínseca `name`\n'; end='## Consecuencias\n'
a=t.find(start); b=t.find(end,a)
if a<0 or b<0: raise SystemExit('D068 name section')
section='''### Metadato estándar `~name`\n\nD-087 retira la propiedad especial `.name` y la asignación contextual `name = ...`. Toda `thing` expone el metadato estándar `~name: Name`. Si no se configura, se deriva del identificador fuente no cualificado; puede configurarse al comienzo del cuerpo mediante la gramática general de metadatos:\n\n```mud\nthing BlackCastle {\n    ~name = "El Castillo Negro"\n}\n```\n\n`~name` pertenece al descriptor y todo acceso `~` es de solo lectura runtime. No se hereda como valor de presentación: una descendiente sin configuración propia deriva su nombre de su propio `~identifier`. Dos `thing` pueden compartir presentación sin compartir identidad. Un campo ordinario `name` pertenece al espacio de miembros y puede coexistir con `~name`.\n\n'''
t=t[:a]+section+t[b:]
t=t.replace('- `name` no introduce estado heredado, conflictos de fusión ni escrituras adicionales.\n- Los campos ordinarios llamados `name` dejan de ser válidos dentro de cuerpos de `thing`; aliases, familias y otros contextos conservan sus propios espacios estructurales.','- `~name` no introduce estado heredado, conflictos de fusión ni escrituras runtime.\n- Un campo ordinario `name` puede coexistir con `~name` porque `.` y `~` pertenecen a espacios distintos.')
t=t.replace('3. Ancla incorporada `thing::Thing` y renderización mediante `anchor{Thing}`.','3. Ancla incorporada `thing::Thing` y lectura reflectiva mediante `Thing~anchor`.')
if 'ADR-087-metadatos' not in t.split('## Contexto',1)[0]:
    marker='- Modifica:'
    t=t.replace(marker,D87+marker,1)
w(p,t)

print('ADR_SWEEP_TRANSFORM_OK')
