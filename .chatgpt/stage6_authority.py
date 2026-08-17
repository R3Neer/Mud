from pathlib import Path
import os
import yaml

ROOT=Path(os.environ['MUD_TARGET']).resolve()
def r(p): return (ROOT/p).read_text(encoding='utf-8')
def w(p,t): (ROOT/p).write_text(t.rstrip('\n')+'\n',encoding='utf-8',newline='\n')
def one(text,old,new,label):
    n=text.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1, got {n}')
    return text.replace(old,new,1)
def fm(text):
    if not text.startswith('---\n'): return {}
    end=text.find('\n---\n',4)
    return yaml.safe_load(text[4:end]) or {}

# Government owns the lifecycle/authority rule.
p='gobierno/CICLO-DOCUMENTAL.md'; t=r(p)
needle='''Un capítulo `vigente` puede contener cuestiones abiertas solo si la característica afectada queda marcada fuera de MUD 1.0 o si la cuestión no altera su significado.\n\n## Promoción de material'''
replacement='''Un capítulo `vigente` puede contener cuestiones abiertas solo si la característica afectada queda marcada fuera de MUD 1.0 o si la cuestión no altera su significado.\n\n### Autoridad durante la preparación\n\n`normative: true` y `status` son ejes distintos. `normative: true` indica que el archivo pertenece a la superficie destinada a la norma; **no** lo promueve ni equivale a `status: vigente`.\n\nMientras la especificación se formaliza:\n\n- un capítulo `vigente` es autoridad normativa aceptada como conjunto, salvo cuestiones explícitamente fuera de su alcance;\n- un capítulo en `esqueleto`, `borrador`, `propuesta` o `en-revision` es una superficie de integración y revisión, no una autoridad independiente capaz de sustituir una decisión vigente;\n- una afirmación de un capítulo no vigente que reproduce una decisión `vigente` o un artefacto mecánico normativo debe coincidir con ellos; una divergencia es un defecto documental que debe corregirse, no una alternativa semántica;\n- las decisiones `vigente` y los artefactos mecánicos declarados normativos continúan fijando los contratos ya decididos mientras los capítulos que los integran no hayan sido promovidos;\n- si dos fuentes aceptadas y normativas se contradicen, la contradicción bloquea la lectura conforme hasta corregirse: no existe una precedencia silenciosa para escoger la versión conveniente;\n- una cuestión activa que afecte al significado mantiene ese punto abierto con independencia de que el archivo que la contiene sea `normative: true`;\n- el historial Git conserva procedencia, pero una versión retirada no adquiere autoridad subsidiaria por estar disponible.\n\nLa promoción a `vigente` sigue requiriendo la revisión del autor y la pasada de publicación descrita abajo; una herramienta no debe inferir esa aprobación solo porque no queden preguntas abiertas.\n\n## Promoción de material'''
t=one(t,needle,replacement,'government authority section')
w(p,t)

# Editorial conventions point explicitly to the government rule.
p='especificacion/00-convenciones-editoriales.md'; t=r(p)
needle='''- `vigente`\n- `sustituido`\n\n## 3. Enlaces'''
replacement='''- `vigente`\n- `sustituido`\n\n`normative: true` clasifica el archivo dentro de la superficie normativa, pero no sustituye el estado editorial. La autoridad de un capítulo no vigente y la relación con decisiones y artefactos mecánicos se rigen por [[gobierno/CICLO-DOCUMENTAL#Autoridad durante la preparación|Autoridad durante la preparación]].\n\n## 3. Enlaces'''
t=one(t,needle,replacement,'editorial authority link')
w(p,t)

# Index: state/authority are different; remove stale branch-anchor description.
p='especificacion/README.md'; t=r(p)
t=one(t,
'''- Autoridad actual: los capítulos vigentes de este directorio y las decisiones vigentes enlazadas. El historial Git conserva la procedencia retirada, pero no tiene autoridad subsidiaria.''',
'''- Autoridad actual: los capítulos `vigente`, las decisiones `vigente` y los artefactos mecánicos declarados normativos fijan los contratos ya aceptados dentro de su alcance. Los capítulos todavía no vigentes integran y explican ese material, pero no pueden sustituirlo por una variante propia. Una contradicción entre fuentes normativas aceptadas es un defecto que debe corregirse, no una regla de precedencia. El historial Git conserva procedencia retirada, pero no tiene autoridad subsidiaria.''',
'index authority')
old='''## Carácter normativo\n\nCada contenido tendrá uno de estos estados:\n\n- **Normativo**: define la conformidad de una implementación.\n- **Informativo**: explica una norma sin ampliarla.\n- **Propuesta**: texto todavía no aprobado.\n- **Abierto**: cuestión sin semántica definitiva.\n\nLas palabras se usarán con este sentido:'''
new='''## Carácter normativo y estado editorial\n\nLa superficie y la madurez editorial no son lo mismo:\n\n- `normative: true` indica que un archivo pertenece a la superficie destinada a definir conformidad; no significa que su redacción completa esté aprobada.\n- `status` sigue el ciclo `esqueleto → borrador → propuesta → en-revision → vigente`; solo `vigente` acepta el capítulo como norma actual en conjunto.\n- En capítulos no vigentes, las reglas respaldadas por decisiones `vigente` y artefactos mecánicos normativos son integraciones de contratos ya decididos, no una autorización para contradecirlos.\n- Una cuestión activa que cambie significado mantiene ese punto **abierto**. La implementación no puede escoger una respuesta y presentarla como MUD 1.0 cerrado.\n- Ejemplos, intuiciones y notas marcadas como informativas explican el contrato sin ampliarlo.\n\nEl detalle de autoridad y promoción vive en [[gobierno/CICLO-DOCUMENTAL#Autoridad durante la preparación|el ciclo documental]]. Cada capítulo muestra su `status` y sus `questions` en el frontmatter; los capítulos 05–09 repiten además una nota de estado al comienzo para que esa frontera sea visible durante la lectura lineal.\n\nLas palabras se usarán con este sentido:'''
t=one(t,old,new,'index normative section')
t=one(t,'La gramática léxica ejecutable vivirá en `gramatica/mud-lexico.ebnf`.','La gramática léxica ejecutable vive en `gramatica/mud-lexico.ebnf`.','index lexical tense')
t=one(t,'- Formación y unicidad de anclas, incluidas anclas estables de ramas decisionales.','- Formación y unicidad de anclas públicas; las ramas funcionales de diccionarios decisionales usan claves locales y no reciben ancla pública conforme a D-090.','index branch anchors')
w(p,t)

# Make the editorial boundary visible in the modern chapters without changing status.
for rel in [
    'especificacion/05-texto-fuente.md',
    'especificacion/06-lexico.md',
    'especificacion/07-gramatica-concreta.md',
    'especificacion/08-sintaxis-abstracta.md',
    'especificacion/09-nombres-y-anclas.md',
]:
    t=r(rel); data=fm(t)
    if data.get('status')!='propuesta': raise SystemExit(f'{rel}: expected propuesta, got {data.get("status")}')
    if '> [!note] Estado editorial' in t: continue
    qs=data.get('questions') or []
    qtext=(f' Las cuestiones activas `{", ".join(qs)}` delimitan aspectos que siguen abiertos y no deben leerse como semántica cerrada.' if qs else ' El frontmatter no enumera cuestiones activas, pero la promoción completa sigue pendiente de la revisión editorial del autor.')
    note=(
        '> [!note] Estado editorial\n'
        '> Este capítulo está en `propuesta`: su redacción completa todavía no ha sido promovida a `vigente`. '
        '`normative: true` señala que pertenece a la superficie normativa, no una aprobación implícita. '
        'Las reglas que integran decisiones `vigente` o artefactos mecánicos normativos deben coincidir con ellos; una discrepancia es un defecto documental.'
        + qtext + '\n\n'
    )
    marker='## Estado y propósito\n\n'
    t=one(t,marker,marker+note,rel+' status note')
    w(rel,t)

print('STAGE6_AUTHORITY_OK')
