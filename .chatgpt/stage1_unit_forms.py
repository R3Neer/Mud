from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def rd(rel): return (ROOT/rel).read_text(encoding='utf-8')
def wr(rel, text): (ROOT/rel).write_text(text.rstrip('\n')+'\n', encoding='utf-8', newline='\n')
def one(text, old, new, label):
    n=text.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 occurrence, found {n}')
    return text.replace(old,new,1)

# D-089: make source-form admissibility explicit.
rel='notas/decisiones/ADR-089-clasificacion-contextual-de-formas-fuente.md'
t=rd(rel)
old='''Las formas de unidad se clasifican después de conocer el catálogo semántico de magnitudes y unidades. El clasificador consulta el texto fuente directamente a partir de una posición en la que la gramática de cantidad admite una unidad. Puede producir `UNIT_FORM` para un identificador, `~name`, `~plural`, `~abbreviation` o forma prefijada habilitada.\n\nCuando existe un tipo o magnitud esperada, solo compiten las formas compatibles con ella. Sin tipo esperado, una forma únicamente es válida si el catálogo resuelto determina una unidad de manera unívoca. Dos candidatos semánticos distintos con la misma forma visible son ambiguos salvo cualificación admitida por la gramática.\n'''
new='''Las formas de unidad se clasifican después de conocer el catálogo semántico de magnitudes y unidades. El clasificador consulta el texto fuente directamente a partir de una posición en la que la gramática de cantidad admite una unidad. Puede producir `UNIT_FORM` para un identificador, `~name`, `~plural`, `~abbreviation` o forma prefijada habilitada.\n\nEl identificador, `~name`, `~plural` y `~abbreviation` obedecen el mismo contrato cuando participan como forma fuente. Una forma configurable puede contener espacios U+0020 y otros caracteres Unicode, pero debe contener al menos un carácter alfabético; por tanto no puede estar formada íntegramente por cifras ni íntegramente por caracteres no alfabéticos. Una forma completa que coincida exactamente con una palabra reservada dura de MUD es inválida como forma fuente. Estas restricciones afectan a su uso como sintaxis y no impiden conservar el mismo `Text` como presentación cuando no sea admisible como forma fuente.\n\nLa validación se realiza sobre el cierre de formas habilitadas de cada magnitud, incluidas todas las combinaciones con prefijos permitidos. Dos unidades distintas de la misma magnitud no pueden producir la misma forma fuente, ni directamente ni después de aplicar un prefijo. Una colisión dentro de la magnitud es un error estático de la declaración y no se difiere al lugar de uso. Entre magnitudes distintas continúa aplicándose la desambiguación contextual descrita a continuación.\n\nCuando existe un tipo o magnitud esperada, solo compiten las formas compatibles con ella. Sin tipo esperado, una forma únicamente es válida si el catálogo resuelto determina una unidad de manera unívoca. Dos candidatos semánticos distintos con la misma forma visible entre magnitudes distintas son ambiguos salvo cualificación admitida por la gramática.\n'''
t=one(t,old,new,'D089 forms')
t=one(t,'8. `3m` y `3 m` clasifican la misma unidad y el formateador produce la forma canónica espaciada.\n9. CST y round-trip conservan exactamente el texto fuente anterior a la clasificación contextual.','''8. `3m` y `3 m` clasifican la misma unidad y el formateador produce la forma canónica espaciada.\n9. `~name`, `~plural` y `~abbreviation` aceptan espacios, pero una forma fuente íntegramente numérica o no alfabética se rechaza.\n10. Una forma fuente idéntica a una palabra reservada dura se rechaza.\n11. Las colisiones entre unidades de la misma magnitud se detectan también después de expandir todos los prefijos habilitados.\n12. CST y round-trip conservan exactamente el texto fuente anterior a la clasificación contextual.''','D089 verification')
wr(rel,t)

# D-076: keep the current ADR literally effective.
rel='notas/decisiones/ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente.md'
t=rd(rel)
needle='''Para cada unidad nombrada se habilitan estas formas de entrada:\n\n- El identificador declarado.\n- `~name`, si no es vacío.\n- `~plural`, si no es vacío.\n- `~abbreviation`, si no es vacío.\n- Las formas con prefijo autorizadas por `~prefixes`.\n'''
replacement=needle+'''\nCuando `~name`, `~plural` o `~abbreviation` actúan como forma fuente se someten al mismo criterio de admisibilidad: pueden contener espacios U+0020 y puntuación, pero deben contener al menos un carácter alfabético y no pueden coincidir exactamente con una palabra reservada dura. El texto sigue siendo válido como presentación aunque no sea una forma fuente admisible.\n\nLa unicidad se comprueba sobre todas las formas fuente efectivas de la magnitud, incluidas las combinaciones generadas por cada prefijo habilitado. Una colisión entre dos unidades de la misma magnitud es inválida aunque solo aparezca después de prefijar una de ellas.\n'''
t=one(t,needle,replacement,'D076 source forms')
wr(rel,t)

# 06: expose the lexical/contextual contract as rules.
rel='especificacion/06-lexico.md'
t=rd(rel)
needle='''> [!rule] MUD-LEX-015 — Determinismo de unidad\n> `UNIT_FORM` usa el catálogo semántico ya resuelto. El tipo esperado restringe candidatos; sin él la forma debe ser globalmente unívoca. Entre coincidencias compatibles de distinta longitud gana la forma completa más larga; dos candidatos distintos para el mismo span son ambiguos.\n'''
replacement=needle+'''\n> [!rule] MUD-LEX-016 — Admisibilidad de formas fuente de unidad\n> El identificador de una unidad y los valores no vacíos de `~name`, `~plural` y `~abbreviation` pueden participar como `UNIT_FORM`. Una forma configurable puede contener espacios U+0020 y puntuación, pero debe contener al menos un carácter alfabético y no puede coincidir exactamente con una palabra reservada dura. Una cadena que no cumpla este contrato puede seguir siendo texto de presentación, pero no se incorpora al catálogo de formas fuente.\n\n> [!rule] MUD-LEX-017 — Unicidad intramagnitud tras prefijos\n> Para cada magnitud, el conjunto de formas fuente de sus unidades se cierra bajo todas las combinaciones de prefijos habilitadas antes de comprobar unicidad. Dos unidades distintas no pueden generar la misma forma completa, directamente o por prefijado. La colisión es un error estático de la declaración de la magnitud y no se resuelve por orden de declaración ni por contexto de uso.\n'''
t=one(t,needle,replacement,'06 unit rules')
wr(rel,t)

# Q-054 remains closed because the missing criteria are now formalized.
rel='notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos.md'
t=rd(rel)
t=one(t,
'''D-076 fija catálogo, formas habilitadas, prefijos y adyacencia. D-089 separa el scanner base del clasificador contextual: `UNIT_FORM` se crea únicamente sobre el texto fuente cuando el catálogo semántico ya está resuelto. El tipo esperado restringe candidatos; sin él se exige unicidad global, las coincidencias de distinta longitud usan la forma completa más larga y un mismo span con varios candidatos sigue siendo ambiguo.\n''',
'''D-076 fija catálogo, formas habilitadas, prefijos y adyacencia. D-089 separa el scanner base del clasificador contextual: `UNIT_FORM` se crea únicamente sobre el texto fuente cuando el catálogo semántico ya está resuelto. El tipo esperado restringe candidatos; sin él se exige unicidad global, las coincidencias de distinta longitud usan la forma completa más larga y un mismo span con varios candidatos sigue siendo ambiguo. `MUD-LEX-016` permite espacios en `~name`, `~plural` y `~abbreviation` cuando actúan como forma fuente, exige al menos un carácter alfabético y excluye palabras reservadas duras; `MUD-LEX-017` comprueba colisiones dentro de una magnitud después de expandir todas las combinaciones de prefijos permitidas.\n''','Q054 resolution')
t=one(t,'- C2: `D-089` y `MUD-LEX-015`.\n- C3: verificación de D-089 y reglas de adyacencia de D-076/06-léxico.','- C2: `D-089`, `MUD-LEX-015`, `MUD-LEX-016` y `MUD-LEX-017`.\n- C3: verificación de D-089 y reglas `MUD-LEX-015` a `MUD-LEX-017`, además de la adyacencia de D-076/06-léxico.','Q054 evidence')
wr(rel,t)

# Add conformance-oriented cases. These are syntax-valid declarations whose semantic expectations exercise the contextual catalog.
rel='especificacion/sintaxis/casos/cst-ast.yaml'
data=yaml.safe_load(rd(rel))
cases=data['cases']
ids={c.get('id') for c in cases}
new_cases=[
 {
  'id':'unit-form-multispace-name', 'category':'validation-after-resolution',
  'source':'magnitude Length {\n    root unit meter {\n        ~name = "long meter"\n        ~plural = "long meters"\n        ~abbreviation = "m"\n    }\n}\nthing Sample {\n    length: Length = 3 long meters\n}\n',
  'cst_root':'MudFileSyntax','produces_ast':True,
  'semantic_expectations':['unit-form-may-cover-multiple-base-tokens','unit-form-resolves-to-meter']
 },
 {
  'id':'unit-form-all-digits-rejected','category':'validation-after-resolution',
  'source':'magnitude Length {\n    root unit meter {\n        ~abbreviation = "123"\n    }\n}\n',
  'cst_root':'MudFileSyntax','produces_ast':True,'expected_diagnostics':['unit-source-form-requires-alphabetic-character']
 },
 {
  'id':'unit-form-all-symbols-rejected','category':'validation-after-resolution',
  'source':'magnitude Length {\n    root unit meter {\n        ~abbreviation = "/+"\n    }\n}\n',
  'cst_root':'MudFileSyntax','produces_ast':True,'expected_diagnostics':['unit-source-form-requires-alphabetic-character']
 },
 {
  'id':'unit-form-keyword-rejected','category':'validation-after-resolution',
  'source':'magnitude Length {\n    root unit meter {\n        ~name = "in"\n    }\n}\n',
  'cst_root':'MudFileSyntax','produces_ast':True,'expected_diagnostics':['unit-source-form-reserved-word']
 },
 {
  'id':'unit-form-prefixed-collision-rejected','category':'validation-after-resolution',
  'source':'magnitude Length {\n    root unit meter {\n        ~name = "meter"\n        ~prefixes = [kilo]\n    }\n    unit kilometer = 1000 meter {\n        ~name = "kilometer"\n    }\n}\n',
  'cst_root':'MudFileSyntax','produces_ast':True,'expected_diagnostics':['duplicate-unit-source-form-after-prefix-expansion']
 },
]
for c in new_cases:
    if c['id'] not in ids: cases.append(c)
wr(rel,yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=120))
print('STAGE1_OK')
