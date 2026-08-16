from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def r(p): return (ROOT/p).read_text(encoding='utf-8')
def w(p,t): (ROOT/p).write_text(t,encoding='utf-8',newline='\n')
def one(p,o,n):
    t=r(p); c=t.count(o)
    if c!=1: raise SystemExit(f'{p}: expected one occurrence, got {c}: {o[:80]!r}')
    w(p,t.replace(o,n,1))
def between(p,start,end,new):
    t=r(p); a=t.find(start); b=t.find(end,a+len(start))
    if a<0 or b<0: raise SystemExit(f'{p}: range markers not found: {start!r} ... {end!r}')
    w(p,t[:a]+new+t[b:])

def provenance(p, marker, line):
    t=r(p)
    if line in t: return
    if marker not in t: raise SystemExit(f'{p}: provenance marker not found')
    w(p,t.replace(marker,marker+line,1))

# D-028: units now use general metadata.
p='notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades.md'; t=r(p)
provenance(p, '- Modificada por:', '') if False else None
for old,new in [
('''    root unit meter {
        name = "meter"
        plural = "meters"
        abbreviation = "m"
    }''','''    root unit meter {
        ~name = "meter"
        ~plural = "meters"
        ~abbreviation = "m"
    }'''),
('El identificador determina el nombre intrínseco y el ancla. `name`, `plural`, `abbreviation` y `prefixes` son opcionales.','El identificador determina `~identifier` y el ancla de la unidad. `~name`, `~plural`, `~abbreviation` y `~prefixes` son metadatos configurables; sus restricciones actuales proceden de D-076 y D-087.'),
('''unit minute := 60 seconds {
    name = "minute"
    plural = "minutes"
    abbreviation = "min"
}''','''unit minute := 60 seconds {
    ~name = "minute"
    ~plural = "minutes"
    ~abbreviation = "min"
}'''),
('La ausencia de la propiedad `prefixes` no habilita prefijos. `prefixes = empty` es equivalente, `prefixes = all` habilita el catálogo decimal SI completo y `prefixes = [p1, p2, ...]` habilita solo el subconjunto enumerado. La forma desnuda `prefixes` no es válida.','`~prefixes` tiene tipo `Prefix [* unique]` y valor predeterminado `empty`. `~prefixes = all` selecciona todo el dominio incorporado de `Prefix` y `~prefixes = [p1, p2, ...]` selecciona una colección ordinaria explícita. No existe una subgramática especial de prefijos de unidad.'),
('''    unit fastie := 1 m/s {
        name = "fastie"
        plural = "fasties"
        abbreviation = "fst"
    }''','''    unit fastie := 1 m/s {
        ~name = "fastie"
        ~plural = "fasties"
        ~abbreviation = "fst"
    }'''),
]:
    if old not in t: raise SystemExit(f'{p}: stale block not found {old[:50]!r}')
    t=t.replace(old,new,1)
if 'D-087' not in t.split('## Decisión',1)[0]:
    marker='- Modificada por: '
    # use simple current provenance section insertion before Amplía/Documents if available
    hdr='- Amplía:'
    if hdr in t: t=t.replace(hdr,'- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n- '+hdr[2:],1)
w(p,t)

# D-029: point format is metadata.
p='notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos.md'; t=r(p)
t=t.replace('    format = "{day}:{hour:2}:{minute:2}"','    ~format = "{day}:{hour:2}:{minute:2}"')
t=t.replace('    format = "{hour:2}:{minute:2}"','    ~format = "{hour:2}:{minute:2}"')
t=t.replace('    format = "{hour:2}:{minute:2}:{second:2}"','    ~format = "{hour:2}:{minute:2}:{second:2}"')
t=t.replace('Puede declarar mediante el `format` opcional una representación textual especial.', 'Puede declarar mediante el metadato `~format` opcional una representación textual especial.')
t=t.replace('el formato es una plantilla `Text`', '`~format` usa una plantilla `Text`')
t=t.replace('el formato de punto sea invertible', '`~format` de punto sea invertible')
if 'D-087' not in t.split('## Decisión',1)[0]:
    marker='- Modificada por: [[ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]]\n'
    if marker in t: t=t.replace(marker,marker+'- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n',1)
w(p,t)

# D-035: no contextual name/prefix labels; no anchor interpolation.
p='notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas.md'; t=r(p)
t=t.replace('D-038, D-054 y D-055 distinguen las palabras reservadas de las contextuales. Una palabra contextual se reconoce únicamente en una posición gramatical concreta y puede ser un identificador ordinario fuera de ella. `start` es contextual en `start with`; `abstract` lo es delante de `thing`; `always` lo es delante de `rule`; y etiquetas como `name` o `prefixes` lo son dentro de las declaraciones que las definen.', 'D-038, D-054 y D-055 distinguen las palabras reservadas de las contextuales. Una palabra contextual se reconoce únicamente en una posición gramatical concreta y puede ser un identificador ordinario fuera de ella. `start` es contextual en `start with`; `abstract` lo es delante de `thing`; `always` lo es delante de `rule`. Los metadatos como `~name` o `~prefixes` usan la gramática general postfix `~` y no convierten `name` o `prefixes` en etiquetas contextuales especiales.')
t=t.replace('`using`, `with`, `family`, `test`, `otherwise`, `ordered` y el tipo incorporado `Thing` son palabras reservadas. En particular, `ordered` no puede usarse como identificador aunque aparezca fuera de una declaración `family` o de una especificación de colección. `name` es contextual dentro de un cuerpo de `thing` cuando aparece seguido de `=`; no queda reservado en los demás espacios nominales.', '`using`, `with`, `family`, `test`, `otherwise`, `ordered` y el tipo incorporado `Thing` son palabras reservadas. En particular, `ordered` no puede usarse como identificador aunque aparezca fuera de una declaración `family` o de una especificación de colección. `name` no tiene una excepción sintáctica de cuerpo de `thing`: la presentación estándar se configura como `~name`, en un espacio distinto del de campos ordinarios.')
t=t.replace('D-061 añade `anchor{...}` como forma contextual exclusiva de una plantilla `Text`. Produce la escritura canónica del ancla de una declaración o de un valor con identidad nominal anclada, sin convertir las declaraciones en valores ordinarios ni reservar `anchor` fuera de ese contexto.', 'D-087 retira la interpolación especial `anchor{...}`. El ancla canónica se obtiene mediante el acceso ordinario `expression~anchor` y una plantilla la interpola como cualquier otra expresión: `"{expression~anchor}"`.')
if 'D-087' not in t.split('## Decisión',1)[0]:
    marker='- Modificada por: '
    # append near existing modification lines
    h='- Amplía:'
    if h in t: t=t.replace(h,'- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n- '+h[2:],1)
w(p,t)

# D-036: every participant named; remove anonymous resolution model.
p='notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md'; t=r(p)
start='El nombre de un participante `on`, o de un participante `for` cuya cardinalidad efectiva sea exactamente `[1]`, puede omitirse.'
end='También son roles válidos los valores sin identidad runtime:'
a=t.find(start); b=t.find(end,a)
if a<0 or b<0: raise SystemExit('D036 anonymous range')
replacement='''Todo participante `for`, `on` y `given` debe declarar un identificador fuente explícito. La cardinalidad `[1]` no crea una excepción anónima. Los miembros del participante se acceden a través de ese identificador y no se proyectan implícitamente al ámbito del cuerpo.

```mud
rule IsDestroyed for army: Army {
    army.soldiers == 0
}

rule CanGovern for person: Person, kingdom: Kingdom {
    person.age >= 18 and kingdom.treasury > 0
}
```

El identificador forma parte del slot de firma y, conforme a D-087, participa junto con la clase de cláusula en su ancla subordinada. Reordenar participantes no cambia esa identidad. Una colección sigue sin proyectar implícitamente los campos de sus miembros: el cuerpo usa el nombre del participante en una cuantificación, agregación o iteración explícita.

```mud
rule AllAdults for people: Person in EligibleCitizens [1..* unique] {
    forall person in people: person.age >= 18
}
```

'''
t=t[:a]+replacement+t[b:]
t=t.replace('- La omisión del nombre de participante individual es azúcar sometido a resolución estática no ambigua, no una firma distinta.\n','- Todo participante tiene nombre y ancla subordinada estable conforme a D-087.\n')
t=t.replace('1. Participante individual anónimo y nombrado.\n2. Varios participantes individuales anónimos con accesos unívocos y rechazo de un acceso ambiguo.','1. Participantes `for`, `on` y `given` siempre nombrados y rechazo de la forma anónima.\n2. Acceso a miembros únicamente a través del identificador del participante.')
t=t.replace('13. Nombre obligatorio para cardinalidad distinta de `[1]` y para mutabilidad exterior.','13. Nombre obligatorio para toda cardinalidad, incluida `[1]`, y para mutabilidad exterior.')
w(p,t)

# D-037: current omitted cardinality and calculated shapes.
p='notas/decisiones/ADR-037-campos-y-dominios-declarativos.md'; t=r(p)
t=t.replace('- Todo campo denota una colección conforme a D-026; omitir cardinalidad equivale a `[1]`.\n- Dentro de una `thing`, `name` designa la propiedad intrínseca fijada por D-068 y no puede declararse como campo ordinario.', '- Todo campo denota una colección conforme a D-026. En un campo almacenado inmutable con inicializador, una cardinalidad omitida se infiere de la forma exterior exacta del valor conforme a D-085; en un campo exteriormente mutable conserva `[1]`.\n- `~name` pertenece al espacio de metadatos de D-087. Un campo ordinario llamado `name` pertenece al espacio de miembros y no lo oculta.')
t=t.replace('''Un campo calculado usa exclusivamente:

```text
nombre [ : tipo ] := expresión
```
''','''Un campo calculado usa:

```text
nombre [ forma-derivada ] := expresión
```

donde la forma derivada puede declarar tipo y, conforme a D-075, dominio, cardinalidad y modificadores de colección compatibles con el resultado.
''')
t=t.replace('Los campos calculados también deben satisfacer el dominio de su tipo estático cuando se evalúan, aunque no puedan declarar una cláusula `in` adicional.', 'Los campos calculados deben satisfacer tanto el dominio de su tipo estático como cualquier dominio `in` declarado en su forma derivada. Ese dominio puede ser explícito o derivarse conforme a D-075.')
t=t.replace('3. Campo almacenado fuera de dominio y rechazo de `in` sobre un campo calculado.', '3. Campo almacenado fuera de dominio y `in` válido sobre un campo calculado conforme a su forma derivada.')
t=t.replace('6. Rechazo de `mut` y de especificaciones de colección en campos calculados.', '6. Rechazo de `mut` exterior en campos calculados y aceptación de capacidad interior/modificadores declarados por su forma derivada cuando sean compatibles.')
w(p,t)

# D-039: exact dictionaries use empty and value-unique semantics from D085.
p='notas/decisiones/ADR-039-colecciones-y-diccionarios.md'; t=r(p)
t=t.replace('''La forma:

```mud
Key -> Value [cardinality modifiers]
```

declara un diccionario con claves únicas. `unique` no se aplica porque la unicidad de clave es intrínseca y escribirlo es un error estático. Tampoco se reinterpreta como unicidad de valores: esa restricción debe expresarse, si se incorpora en el futuro, mediante una construcción distinta y explícita.
''','''La forma:

```mud
Key -> Value [cardinality modifiers]
```

declara un diccionario con claves intrínsecamente únicas. El modificador `unique`, cuando se escribe, se aplica a los **valores asociados** conforme a D-085: exige que un mismo valor no quede asociado a más de una clave. Una inserción o sustitución que violaría esa unicidad es una no-op completa y no produce `failed`.
''')
t=t.replace('Leer una clave ausente produce el predeterminado del tipo de valor cuando la lectura exige un valor. D-017 y Q-047 gobiernan la existencia y selección de ese predeterminado. Los contextos que preserven ausencia deberán hacerlo mediante cardinalidad, no mediante `null`.', 'Leer una clave ausente produce `empty` con la forma de salida declarada. La ausencia no produce `failed` por sí misma; solo un contexto posterior cuyo tipo, dominio o cardinalidad no admita cero elementos puede fallar. No se usa `null` ni se sustituye silenciosamente por el predeterminado del tipo de valor.')
t=t.replace('4. Lectura, escritura y retirada de clave ausente.', '4. Lectura ausente como `empty`, escritura y retirada de clave ausente, y `unique` global sobre valores.')
w(p,t)

# D-054: structured global start with and no metadata-era contextual labels.
p='notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md'; t=r(p)
start='### Conjunto inicial `start with`\n'
end='### Inicialización y reactivación\n'
a=t.find(start); b=t.find(end,a)
if a<0 or b<0: raise SystemExit('D054 start range')
section='''### Conjunto inicial `start with`

Las definiciones de `thing` y reglas no quedan activas por el mero hecho de aparecer. El único `start with` global separa obligatoriamente ambos universos:

```mud
start with {
    things {
        Vegetation,
        Tree
    }

    rules {
        CanGrow
    }
}
```

No existe la forma plana o mezclada. Cada sección recibe expresiones estáticas que aportan cero, una o varias identidades de su categoría: una referencia aporta una, `empty` aporta cero, una colección aporta sus miembros y `all` denota el catálogo estático correspondiente. Una colección de colecciones es inválida. Las identidades repetidas se deduplican y el orden no es observable.

Las expresiones solo pueden depender de información disponible antes de existir mundo runtime, incluidos metadatos estáticos compatibles. El resultado completo se materializa y valida atómicamente y se estabiliza antes de aceptar acciones externas.

Sea $\\mathcal T_P$ el catálogo de `thing` activables y $\\mathcal R_P$ el catálogo de reglas activables. La declaración determina dos conjuntos independientes:

$$
\\operatorname{initialThings}_P \\subseteq \\mathcal T_P
\\qquad
\\operatorname{initialRules}_P \\subseteq \\mathcal R_P
$$

Conforme a D-041, las vinculaciones reactivas presentes en la primera instantánea materializada usan un anterior virtual falso para su primer `when` booleano; las vinculaciones que nazcan durante esa estabilización siguen la regla ordinaria de línea base sin disparo.

Las acciones, aliases y magnitudes no pertenecen a ninguno de esos conjuntos. Conforme a D-055 y D-085, cada test declara un `start with` local con las mismas secciones `things` y `rules`; durante ese test sustituye por completo al global.

'''
t=t[:a]+section+t[b:]
t=t.replace('Las etiquetas reconocidas dentro de una declaración concreta, como `name` y `prefixes` en las declaraciones de unidades o `name =` en un cuerpo de `thing`, son igualmente contextuales y no pertenecen por ello al catálogo general de palabras reservadas.', 'Los metadatos estándar como `~name` y `~prefixes` usan la gramática general postfix `~`; `name` y `prefixes` no son etiquetas contextuales especiales por esa razón.')
old='''start-with-declaration
    ::= "start" "with" "{"
        [ declaration-reference
          { "," declaration-reference }
        ]
        "}"
'''
new='''start-with-declaration
    ::= "start" "with" "{"
        "things" "{" contribution-list "}"
        "rules" "{" contribution-list "}"
        "}"
'''
if old not in t: raise SystemExit('D054 start ebnf')
t=t.replace(old,new,1)
t=t.replace('InitialActivationSet(references)', 'InitialActivationSet(things, rules)',1)
t=t.replace('`CreateReference` no contiene un descriptor. `InitialActivationSet` conserva procedencia textual para diagnósticos, pero su significado es un conjunto no ordenado.', '`CreateReference` no contiene un descriptor. `InitialActivationSet` conserva por separado las contribuciones de `things` y `rules`; cada resultado efectivo es un conjunto no ordenado.')
if 'D-085' not in t.split('## Decisión',1)[0]:
    marker='- Modificada por: '
    # insert before docs line
    h='- Documentos afectados:'
    if h in t: t=t.replace(h,'- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].\n'+h,1)
w(p,t)

# D-055: local test start with is structured like global.
p='notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md'; t=r(p)
old='''test-start-with
    ::= "start" "with" "{"
        [ declaration-reference
          { "," declaration-reference }
        ]
        "}"
'''
new='''test-start-with
    ::= "start" "with" "{"
        "things" "{" contribution-list "}"
        "rules" "{" contribution-list "}"
        "}"
'''
if old not in t: raise SystemExit('D055 flat EBNF')
t=t.replace(old,new,1)
t=t.replace('''El bloque local conserva la misma naturaleza declarativa que el global:

- Es un conjunto finito y no ordenado.
- Contiene referencias a definiciones canónicas activables de `thing` y reglas.
- Separa sus referencias mediante comas y no admite coma final.
- No contiene instrucciones `create`, asignaciones ni otros efectos.
- Rechaza referencias repetidas, ambiguas o no activables.
''','''El bloque local conserva la misma estructura declarativa que el global de D-085: contiene obligatoriamente las secciones `things { ... }` y `rules { ... }`. Cada una admite contribuciones estáticas de cero, una o varias identidades de su propia categoría mediante referencias, `empty`, colecciones de un nivel o `all` contextual. El orden no es observable y las identidades repetidas se deduplican.

No contiene instrucciones `create`, asignaciones ni otros efectos, y una contribución de categoría incorrecta o una colección anidada es inválida.
''')
t=t.replace('Sea $\\mathcal L_P$ el conjunto de declaraciones activables del programa $P$ y sea $I_t\\subseteq\\mathcal L_P$ el conjunto local del test $t$. El estado previo al escenario se obtiene mediante:', 'Sean $T_t$ y $R_t$ los conjuntos locales de `thing` y reglas del test. El estado previo al escenario se obtiene materializando conjuntamente ambas secciones:')
t=t.replace('\\operatorname{materialize}(P,I_t)', '\\operatorname{materialize}(P,T_t,R_t)')
if 'D-085' not in t.split('## Decisión',1)[0]:
    marker='- Ampliada además por: [[ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]]\n'
    if marker in t: t=t.replace(marker,marker+'- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].\n',1)
w(p,t)

# D-061: modern ~format and ordinary ~anchor interpolation.
p='notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text.md'; t=r(p)
t=t.replace('Dentro del `format` de una magnitud de punto, el propio punto es contextual.', 'Dentro del `~format` de una magnitud de punto, el propio punto es contextual.')
t=t.replace('format = "{hour:2}:{minute:2}:{second:2}"','~format = "{hour:2}:{minute:2}:{second:2}"')
t=t.replace('format = "{week from year:2}"','~format = "{week from year:2}"')
t=t.replace('La forma incompleta `week from year` solo es válida en un hueco del `format` de una magnitud de punto;', 'La forma incompleta `week from year` solo es válida en un hueco del `~format` de una magnitud de punto;')
t=t.replace('La propiedad `format` de una magnitud `point over` usa esta misma sintaxis, no un segundo lenguaje de llaves.', 'El metadato `~format` de una magnitud `point over` usa esta misma sintaxis, no un segundo lenguaje de llaves.')
t=t.replace('un campo directo sin `in` publica la coordenada numérica, no el `format`;', 'un campo directo sin `in` publica la coordenada numérica, no el `~format`;')
start='### Interpolación de anclas\n'
end='## Consecuencias\n'
a=t.find(start); b=t.find(end,a)
if a<0 or b<0: raise SystemExit('D061 anchor range')
section='''### Anclas dentro de plantillas

No existe una interpolación especial `anchor{...}`. D-087 hace de `~anchor` una propiedad reflectiva ordinaria y tipada, por lo que se interpola mediante la sintaxis general de expresiones:

```mud
"Rule: {CanRecruit~anchor}"
"Kingdom: {kingdom}; identity: {kingdom~anchor}"
```

El acceso solo es válido cuando la categoría estática del receptor expone `~anchor`. La plantilla no convierte por ello declaraciones arbitrarias en valores ni introduce un token especial `anchor`.

'''
t=t[:a]+section+t[b:]
t=t.replace('- El AST distingue fragmentos literales, huecos de valor, especificaciones numéricas y huecos de ancla.','- El AST distingue fragmentos literales, huecos de valor y especificaciones numéricas; las anclas usan interpolaciones de expresión ordinarias.')
t=t.replace('- El nombre visible de una `thing` puede diferir de su ancla; `anchor{...}` conserva la identidad canónica.','- La presentación `~name` puede diferir de `~anchor`; ambas son propiedades reflectivas separadas.')
t=t.replace('9. Obtención de anclas de declaraciones y valores nominales mediante `anchor{...}`.\n10. Rechazo de `anchor{...}` sobre valores sin identidad anclada.', '9. Obtención de anclas mediante interpolación ordinaria de `expression~anchor`.\n10. Rechazo de `~anchor` cuando la categoría estática del receptor no expone esa propiedad.')
if 'D-087' not in t.split('## Decisión',1)[0]:
    marker='- Modificada por:'
    # fallback insert before docs
    h='- Documentos afectados:'
    if h in t: t=t.replace(h,'- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n'+h,1)
w(p,t)

# D-063: all for participants named.
p='notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md'; t=r(p)
old='''Los roles `for` conservan sus reglas de nombre:

- Un rol de cardinalidad exactamente `[1]` puede ser anónimo cuando la resolución del cuerpo es unívoca.
- Un rol colectivo o exteriormente mutable debe tener nombre.
- Un rol anónimo solo admite vinculación posicional.

La forma de receptor multiparte nombrado continúa siendo exacta, exhaustiva y no mezclable con posiciones. Puede reordenar roles, pero el compilador sugiere el orden de declaración. Los receptores posicionales no pueden omitir roles.
'''
new='''Todo rol `for` tiene identificador fuente explícito, incluida cardinalidad `[1]`, conforme a D-087. La firma conserva el orden de declaración, pero ese orden no sustituye a la identidad estable del slot.

La forma de receptor multiparte nombrado continúa siendo exacta, exhaustiva y no mezclable con posiciones. Puede reordenar roles, pero el compilador sugiere el orden de declaración. Los receptores posicionales siguen disponibles cuando la sintaxis de llamada los admita, pero la declaración de la firma nunca contiene participantes anónimos.
'''
if old not in t: raise SystemExit('D063 anonymous for block')
t=t.replace(old,new,1)
if 'D-087' not in t.split('## Contexto',1)[0]:
    marker='- Modificada por: [[ADR-092-tipos-readonly-completos-en-given|D-092]]\n'
    if marker in t: t=t.replace(marker,marker+'- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n',1)
w(p,t)

# D-068: presentation moved entirely to ~name metadata.
p='notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md'; t=r(p)
t=t.replace('Su ancla canónica es `thing::Thing`; `anchor{Thing}` produce esa escritura. El ancla pertenece al lenguaje y no ocupa un path declarable por el programa.', 'Su ancla canónica es `thing::Thing`; `Thing~anchor` produce ese valor reflectivo. El ancla pertenece al lenguaje y no ocupa un path declarable por el programa.')
start='### Propiedad intrínseca `name`\n'
end='## Consecuencias\n'
a=t.find(start); b=t.find(end,a)
if a<0 or b<0: raise SystemExit('D068 name section')
section='''### Metadato estándar `~name`

D-087 retira la propiedad especial `.name` y la asignación contextual `name = ...`. Toda `thing` expone el metadato estándar de presentación:

```text
~name: Name
```

Si no se configura, su valor se deriva del identificador fuente no cualificado. Puede configurarse al comienzo del cuerpo mediante la gramática general de metadatos:

```mud
thing BlackCastle {
    ~name = "El Castillo Negro"
}
```

`~name` pertenece al descriptor, no al store runtime; todo acceso `~` es de solo lectura durante la ejecución. No se hereda como valor de presentación: una descendiente sin configuración propia deriva su `~name` de su propio `~identifier`.

Dos `thing` pueden compartir el mismo `~name`; igualdad, resolución y anclaje continúan usando identidad. La interpolación ordinaria de una `thing` usa su presentación efectiva, mientras `{value~anchor}` muestra la identidad canónica cuando se necesita expresamente.

El espacio de metadatos es distinto del espacio de miembros. Por ello una `thing` puede declarar un campo ordinario `name` y accederlo como `.name` sin ocultar ni sustituir `~name`.

'''
t=t[:a]+section+t[b:]
t=t.replace('- `name` no introduce estado heredado, conflictos de fusión ni escrituras adicionales.\n- Los campos ordinarios llamados `name` dejan de ser válidos dentro de cuerpos de `thing`; aliases, familias y otros contextos conservan sus propios espacios estructurales.', '- `~name` no introduce estado heredado, conflictos de fusión ni escrituras runtime.\n- Un campo ordinario `name` puede coexistir con `~name` porque `.` y `~` pertenecen a espacios distintos.')
t=t.replace('3. Ancla incorporada `thing::Thing` y renderización mediante `anchor{Thing}`.', '3. Ancla incorporada `thing::Thing` y lectura reflectiva mediante `Thing~anchor`.')
t=t.replace('6. `name` predeterminado igual al nombre nominal no cualificado.\n7. Sobrescritura mediante un único literal `Text` sin interpolaciones.\n8. Rechazo de redeclaración, mutabilidad, cálculo, escritura runtime e interpolación en la sobrescritura.\n9. Ausencia de herencia del `name` sobrescrito.\n10. `{value}` usa `value.name` y `anchor{value}` conserva la identidad canónica.\n11. Nombres visibles duplicados sin fusión de identidades.', '6. `~name` predeterminado derivado de `~identifier`.\n7. Configuración `~name = "..."` mediante la gramática general de metadatos y construcción contextual de `Name`.\n8. Rechazo de escritura runtime sobre `~name`.\n9. Ausencia de herencia del `~name` configurado.\n10. `{value}` usa la presentación efectiva y `{value~anchor}` la identidad canónica.\n11. Presentaciones duplicadas sin fusión de identidades y coexistencia de un campo ordinario `.name`.')
t=t.replace('Los aliases no reciben una propiedad intrínseca `name`. Su declaración conserva un nombre nominal y un ancla de tipo, pero cada valor alias solo posee los componentes declarados. Un alias estructural puede declarar un componente ordinario `name: Text`. Los miembros de `family` conservan su nombre intrínseco propio.', 'Aliases, miembros de `family` y demás categorías metadata-bearing aplicables usan también el metadato estándar `~name` de D-087. Un alias estructural puede además declarar un componente ordinario `name: Text`; ambos espacios son independientes.')
if 'D-087' not in t.split('## Decisión',1)[0]:
    marker='- Modificada por:'
    h='- Amplía:'
    if h in t: t=t.replace(h,'- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n- '+h[2:],1)
w(p,t)

# D-085: remove two stale consequences left after D087/D090/D094.
p='notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md'; t=r(p)
t=t.replace('- `MetadataAccessExpr` y objetivos asignables de metadato;', '- `MetadataAccessExpr` exclusivamente como lectura; ningún acceso `~` forma parte de los objetivos asignables;')
t=t.replace('El AST resuelto o IR registra para cada decisional:', 'La representación elaborada o el IR registra para cada decisional:')
t=t.replace('- ancla estable de cada rama;', '- clave local canónica de cada rama conforme a D-090;')
if 'D-094' not in t.split('## Contexto',1)[0]:
    marker='- Modificada por: [[ADR-090-claves-locales-de-entradas-de-diccionario|D-090]]\n'
    if marker in t: t=t.replace(marker,marker+'- Modificada por: [[ADR-094-frontera-ast-resuelto-y-elaborado|D-094]].\n',1)
w(p,t)

print('PHASE7_ADR_SWEEP_OK')
