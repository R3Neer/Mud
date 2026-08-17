from pathlib import Path
import os

ROOT=Path(os.environ['MUD_TARGET']).resolve()
def r(p): return (ROOT/p).read_text(encoding='utf-8')
def w(p,t): (ROOT/p).write_text(t.rstrip('\n')+'\n',encoding='utf-8',newline='\n')
def one(text,old,new,label):
    n=text.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1, got {n}')
    return text.replace(old,new,1)

# D-021: activation set has structured thing/rule sections.
p='notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension.md'; t=r(p)
t=one(t,'''Las declaraciones presentes al comienzo se enumeran conjuntamente:\n\n```mud\nstart with {\n    Kingdom,\n    Place,\n    CanEnter\n}\n```''','''Las declaraciones presentes al comienzo se separan por categoría conforme a D-085:\n\n```mud\nstart with {\n    things {\n        Kingdom,\n        Place\n    }\n\n    rules {\n        CanEnter\n    }\n}\n```\n\nNo existe una forma plana que mezcle `thing` y reglas en un mismo conjunto.''','D021 start-with')
w(p,t)

# D-028: units use general metadata.
p='notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades.md'; t=r(p)
for old,new in [
('''    root unit meter {\n        name = "meter"\n        plural = "meters"\n        abbreviation = "m"\n    }''','''    root unit meter {\n        ~name = "meter"\n        ~plural = "meters"\n        ~abbreviation = "m"\n    }'''),
('El identificador determina el nombre intrínseco y el ancla. `name`, `plural`, `abbreviation` y `prefixes` son opcionales.','El identificador determina `~identifier` y el ancla. `~name`, `~plural`, `~abbreviation` y `~prefixes` son metadatos configurables conforme a D-076 y D-087.'),
('''unit minute := 60 seconds {\n    name = "minute"\n    plural = "minutes"\n    abbreviation = "min"\n}''','''unit minute := 60 seconds {\n    ~name = "minute"\n    ~plural = "minutes"\n    ~abbreviation = "min"\n}'''),
('La ausencia de la propiedad `prefixes` no habilita prefijos. `prefixes = empty` es equivalente, `prefixes = all` habilita el catálogo decimal SI completo y `prefixes = [p1, p2, ...]` habilita solo el subconjunto enumerado. La forma desnuda `prefixes` no es válida.','`~prefixes` tiene tipo `Prefix [* unique]` y valor predeterminado `empty`. `~prefixes = all` selecciona el dominio incorporado completo y `~prefixes = [p1, p2, ...]` una colección explícita. No existe una subgramática especial de propiedades de unidad.'),
('''    unit fastie := 1 m/s {\n        name = "fastie"\n        plural = "fasties"\n        abbreviation = "fst"\n    }''','''    unit fastie := 1 m/s {\n        ~name = "fastie"\n        ~plural = "fasties"\n        ~abbreviation = "fst"\n    }'''),
]: t=one(t,old,new,'D028')
w(p,t)

# D-029: point presentation is ~format metadata.
p='notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos.md'; t=r(p)
for old,new in [
('    format = "{day}:{hour:2}:{minute:2}"','    ~format = "{day}:{hour:2}:{minute:2}"'),
('    format = "{hour:2}:{minute:2}"','    ~format = "{hour:2}:{minute:2}"'),
('    format = "{hour:2}:{minute:2}:{second:2}"','    ~format = "{hour:2}:{minute:2}:{second:2}"'),
('Puede declarar mediante el `format` opcional una representación textual especial.','Puede declarar mediante el metadato `~format` opcional una representación textual especial.'),
('Conforme a D-061, el formato es una plantilla `Text`:','Conforme a D-061, `~format` usa una plantilla `Text`:'),
('D-062 exige que el formato de punto sea invertible','D-062 exige que `~format` sea invertible'),
('11. `format` opcional y representación cuantitativa ordinaria, con unidad, cuando se omite.','11. `~format` opcional y representación cuantitativa ordinaria, con unidad, cuando se omite.'),
]: t=one(t,old,new,'D029')
w(p,t)

# D-035: metadata spelling and anchor interpolation.
p='notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas.md'; t=r(p)
for old,new in [
('D-038, D-054 y D-055 distinguen las palabras reservadas de las contextuales. Una palabra contextual se reconoce únicamente en una posición gramatical concreta y puede ser un identificador ordinario fuera de ella. `start` es contextual en `start with`; `abstract` lo es delante de `thing`; `always` lo es delante de `rule`; y etiquetas como `name` o `prefixes` lo son dentro de las declaraciones que las definen.','D-038, D-054 y D-055 distinguen las palabras reservadas de las contextuales. Una palabra contextual se reconoce únicamente en una posición gramatical concreta y puede ser un identificador ordinario fuera de ella. `start` es contextual en `start with`; `abstract` lo es delante de `thing`; `always` lo es delante de `rule`. Los metadatos como `~name` o `~prefixes` usan la gramática general postfix `~`, no etiquetas contextuales especiales.'),
('`using`, `with`, `family`, `test`, `otherwise`, `ordered` y el tipo incorporado `Thing` son palabras reservadas. En particular, `ordered` no puede usarse como identificador aunque aparezca fuera de una declaración `family` o de una especificación de colección. `name` es contextual dentro de un cuerpo de `thing` cuando aparece seguido de `=`; no queda reservado en los demás espacios nominales.','`using`, `with`, `family`, `test`, `otherwise`, `ordered` y el tipo incorporado `Thing` son palabras reservadas. En particular, `ordered` no puede usarse como identificador aunque aparezca fuera de una declaración `family` o de una especificación de colección. `name` no tiene una excepción sintáctica de cuerpo de `thing`: la presentación estándar se configura como `~name`, en un espacio distinto del de campos ordinarios.'),
('D-061 añade `anchor{...}` como forma contextual exclusiva de una plantilla `Text`. Produce la escritura canónica del ancla de una declaración o de un valor con identidad nominal anclada, sin convertir las declaraciones en valores ordinarios ni reservar `anchor` fuera de ese contexto.','D-087 retira `anchor{...}`. El ancla canónica se obtiene mediante el acceso ordinario `expression~anchor` y una plantilla la interpola como cualquier otra expresión: `"{expression~anchor}"`.'),
('9. Interpolación contextual de un ancla y uso ordinario de `anchor` fuera de plantillas.','9. Lectura de un ancla mediante `~anchor` e interpolación mediante un hueco de expresión ordinario.'),
]: t=one(t,old,new,'D035')
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
w(p,t)

# D-037: current field/cardinality/derived-shape contracts.
p='notas/decisiones/ADR-037-campos-y-dominios-declarativos.md'; t=r(p)
t=one(t,'''- Todo campo denota una colección conforme a D-026; omitir cardinalidad equivale a `[1]`.\n- Dentro de una `thing`, `name` designa la propiedad intrínseca fijada por D-068 y no puede declararse como campo ordinario.''','''- Todo campo denota una colección conforme a D-026. En un campo almacenado inmutable con inicializador, una cardinalidad omitida se infiere de la forma exterior exacta del valor conforme a D-085; en un campo exteriormente mutable conserva `[1]`.\n- `~name` pertenece al espacio de metadatos de D-087. Un campo ordinario llamado `name` pertenece al espacio de miembros y no lo oculta.''','D037 bullets')
t=one(t,'''El dominio precede a la especificación de colección. Un campo calculado usa exclusivamente:\n\n```text\nnombre [ : tipo ] := expresión\n```''','''El dominio precede a la especificación de colección. Un campo calculado usa:\n\n```text\nnombre [ forma-derivada ] := expresión\n```\n\ndonde la forma derivada puede declarar tipo y, conforme a D-075, dominio, cardinalidad y modificadores de colección compatibles con el resultado.''','D037 shape')
t=one(t,'Los campos calculados también deben satisfacer el dominio de su tipo estático cuando se evalúan, aunque no puedan declarar una cláusula `in` adicional.','Los campos calculados deben satisfacer tanto el dominio de su tipo estático como cualquier dominio `in` declarado en su forma derivada. Ese dominio puede ser explícito o derivarse conforme a D-075.','D037 domain')
t=t.replace('3. Campo almacenado fuera de dominio y rechazo de `in` sobre un campo calculado.','3. Campo almacenado fuera de dominio y `in` válido sobre un campo calculado conforme a su forma derivada.',1)
t=t.replace('6. Rechazo de `mut` y de especificaciones de colección en campos calculados.','6. Rechazo de `mut` exterior en campos calculados y aceptación de capacidad interior/modificadores declarados por su forma derivada cuando sean compatibles.',1)
w(p,t)

# D-039: dictionary unique applies to values; missing lookup is empty.
p='notas/decisiones/ADR-039-colecciones-y-diccionarios.md'; t=r(p)
t=one(t,'declara un diccionario con claves únicas. `unique` no se aplica porque la unicidad de clave es intrínseca y escribirlo es un error estático. Tampoco se reinterpreta como unicidad de valores: esa restricción debe expresarse, si se incorpora en el futuro, mediante una construcción distinta y explícita.','declara un diccionario con claves intrínsecamente únicas. El modificador `unique`, cuando se escribe, se aplica a los **valores asociados** conforme a D-085: exige que un mismo valor no quede asociado a más de una clave. Una inserción o sustitución que violaría esa unicidad es una no-op completa y no produce `failed`.','D039 unique')
t=one(t,'Leer una clave ausente produce el predeterminado del tipo de valor cuando la lectura exige un valor. D-017 y Q-047 gobiernan la existencia y selección de ese predeterminado. Los contextos que preserven ausencia deberán hacerlo mediante cardinalidad, no mediante `null`.','Leer una clave ausente produce `empty` con la forma de salida declarada. La ausencia no produce `failed` por sí misma; solo un contexto posterior cuyo tipo, dominio o cardinalidad no admita cero elementos puede fallar. No se usa `null` ni se sustituye silenciosamente por el predeterminado del tipo de valor.','D039 missing lookup')
t=t.replace('4. Lectura, escritura y retirada de clave ausente.','4. Lectura ausente como `empty`, escritura y retirada de clave ausente, y `unique` global sobre valores.',1)
w(p,t)

print('STAGE5_SWEEP_A_OK')
