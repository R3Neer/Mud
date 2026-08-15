from __future__ import annotations
from pathlib import Path
import re, sys, yaml

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()

def p(rel): return ROOT / rel
def read(rel): return p(rel).read_text(encoding='utf-8')
def write(rel, text): p(rel).write_text(text.rstrip('\n') + '\n', encoding='utf-8', newline='\n')
def exact(text, old, new, label, count=1):
    actual = text.count(old)
    if actual != count: raise SystemExit(f'{label}: expected {count}, found {actual}')
    return text.replace(old, new, count)
def append_once(text, marker, block):
    if marker in text: return text
    return text.rstrip() + '\n\n' + block.strip() + '\n'
def add_frontmatter_item(text, key, item):
    end = text.find('\n---\n', 4)
    if not text.startswith('---\n') or end < 0: raise SystemExit(f'frontmatter missing: {key}')
    lines = text[4:end].splitlines()
    try: idx = lines.index(key + ':')
    except ValueError: raise SystemExit(f'frontmatter key missing: {key}')
    j = idx + 1; existing=[]
    while j < len(lines) and lines[j].startswith('  - '):
        existing.append(lines[j][4:].strip().strip('"')); j += 1
    if item not in existing: lines.insert(j, f'  - {item}')
    return '---\n' + '\n'.join(lines) + text[end:]
def replace_md_section(text, heading, new_section):
    pat = re.compile(rf'(?ms)^{re.escape(heading)}\n.*?(?=^## [^#]|\Z)')
    m = list(pat.finditer(text))
    if len(m) != 1: raise SystemExit(f'section {heading!r}: expected 1, found {len(m)}')
    return text[:m[0].start()] + new_section.rstrip() + '\n\n' + text[m[0].end():].lstrip('\n')
def replace_yaml_block(text, key, block):
    pat = re.compile(rf'(?ms)^  {re.escape(key)}:\n.*?(?=^  [A-Za-z0-9_-]+:\n|\Z)')
    m = list(pat.finditer(text))
    if len(m) != 1: raise SystemExit(f'YAML block {key}: expected 1, found {len(m)}')
    return text[:m[0].start()] + block.rstrip() + '\n' + text[m[0].end():]

adr88 = '''---
id: D-088
title: "Iteración, progresiones firmadas y bloques de expresión"
status: vigente
date: 2026-08-15
supersedes: []
superseded-by: []
questions:
  - "Q-018"
  - "Q-028"
  - "Q-029"
affects:
  - "for each, filtros, cuantificadores, selección, dominios escalonados, intervalos, magnitudes, bloques de expresión, gramática, CST y AST"
---

# ADR-088 — Iteración, progresiones firmadas y bloques de expresión

- Modifica: [[ADR-047-cuantificadores-e-iteracion-finita|D-047]], [[ADR-057-gramatica-concreta-y-continuacion|D-057]], [[ADR-071-vinculaciones-locales-en-bloques-booleanos|D-071]], [[ADR-075-dominios-enumerables-all-y-valores-derivados|D-075]], [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]] y [[ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]].
- Conserva: [[ADR-034-number-exacto-y-rumber-binary64|D-034]], [[ADR-040-semantica-numerica-basica-restante|D-040]] y la prohibición de azar en filtros de [[ADR-048-azar-reproducible-y-fallos|D-048]].
- Preguntas relacionadas: [[notas/preguntas/Q-018-intervalos-discontinuos|Q-018]], [[notas/preguntas/Q-028-finitud|Q-028]] y [[notas/preguntas/Q-029-terminacion|Q-029]].

## Contexto

MUD ya dispone de `for each`, cuantificadores, selección pura y dominios escalonados, pero las reglas anteriores mezclaban enumerabilidad, progresión mediante una diferencia y estructura del cuerpo posterior a `:`. D-075 exigía además un paso positivo y D-047 no distinguía con precisión cuándo el filtro de una iteración ordenada puede observar efectos anteriores.

## Fuentes enumerables y `for each`

`for each` acepta cualquier fuente cuya finitud y enumerabilidad puedan demostrarse: colecciones, diccionarios exactos, intervalos enumerables, dominios finitos enumerables y cualquier otro valor con enumeración canónica definida. Un intervalo sigue siendo un intervalo; poder enumerarlo no lo convierte en colección.

```mud
for each i in [1..10]:
    process i
```

La pertenencia de la fuente se captura al comenzar el bucle. Un intervalo vacío produce cero iteraciones. Un intervalo infinito no puede alimentar una construcción que exija enumeración exhaustiva.

## Separador `:` y cuerpos

Cuando una construcción usa `:` para separar una cabecera de un cuerpo subordinado, las llaves pertenecen al cuerpo posterior y nunca sustituyen al separador.

```mud
for each i in [1..10]: {
    doubled := i * 2
    process doubled
}
```

La forma sin `:` es inválida. El cuerpo de `for each` usa exactamente el contrato ejecutable de `then`: un único efecto o llamada a acción, o un bloque de efectos que puede intercalar vinculaciones locales `:=`.

Selecciones y cuantificadores/agregadores conservan igualmente su `:` obligatorio. Su cuerpo puede ser una expresión breve o un bloque de expresión con cero o más vinculaciones locales seguidas de una única expresión final.

## Bloque de expresión

Se generaliza el antiguo `BooleanBlock` a `ExpressionBlock(locals, result)`. La estructura no decide el tipo de `result`; lo hace su propietario. Reglas booleanas, `if`, selección, `exists`, `forall` y `count` aplican su contrato booleano; `when` exige un activador admitido; `sum` un valor agregable; `min` y `max` un valor ordenable.

Las locales son puras, inmutables, secuenciales y no admiten referencias adelantadas, ciclos, redeclaración ni sombreado.

## Filtro de `for each`

El `if` opcional aparece después de `by` y puede ser una expresión o un bloque de expresión. El predicado es puro y no estocástico conforme a D-048.

- Con orden semántico, cada filtro se evalúa inmediatamente antes de su iteración y observa los efectos secuenciales producidos por iteraciones anteriores.
- Sin orden semántico, todos los filtros observan la misma instantánea inicial y las iteraciones aceptadas producen deltas que se consolidan como simultáneos.

Por ello `for each ... if ...` no se define universalmente como desazucaración literal a una selección materializada previa.

## `by` como progresión

`by δ` recibe una expresión ordinaria cuyo valor es una diferencia firmada compatible con la fuente. En construcciones runtime se evalúa exactamente una vez antes de comenzar el recorrido y su valor queda fijado durante esa ejecución.

La compatibilidad se determina por la operación de avance y por las conversiones implícitas exactas admitidas, no por igualdad nominal del tipo recorrido y la diferencia. Un intervalo `Nat` puede usar una diferencia `Int`; un intervalo `Num`, `Nat`, `Int` o `Num` compatibles; una magnitud puede usar otra unidad compatible. En magnitudes de punto el paso es una diferencia de la magnitud lineal subyacente, no otro punto.

Un paso positivo se ancla en el límite inferior; uno negativo, en el superior. Si el límite inicial es abierto, se aplica una vez el paso antes de comprobar el primer candidato. Tras cada valor emitido se suma el paso y el recorrido termina antes del primer candidato exterior. No es necesario alcanzar exactamente el extremo opuesto.

```mud
for each i in [1..8] by 2:
    use i
# 1, 3, 5, 7

for each i in [1..8] by -3:
    use i
# 8, 5, 2
```

Los extremos invertidos continúan normalizándose a `empty`; nunca expresan recorrido descendente.

## Paso cero

Si un paso runtime es demostrablemente cero, existe error estático. Si no puede demostrarse y finalmente evalúa a cero, la resolución produce `failed` y revierte. En un dominio escalonado el paso es estático, por lo que cero siempre es error de elaboración.

## Pasos predeterminados

Puede omitirse `by` únicamente cuando el tipo define un siguiente valor canónico. MUD fija `Nat -> 1`, `Int -> 1` y `Money -> 0.01`. Omitir `by` siempre selecciona el paso positivo. Otros tipos exactos ordenados requieren paso explícito salvo decisión que defina uno canónico.

`Num` admite progresión con paso exacto explícito, pero un intervalo general de `Num` sin paso es inválido. `Rum` conserva la prohibición de D-034: sus intervalos nunca son enumerables y `by` nunca es válido sobre ellos, ni en iteración ni en dominio escalonado. Una colección explícita de valores `Rum` sí puede enumerarse.

## Dominios escalonados

`interval by δ` define un dominio mediante la misma progresión exacta. El paso debe ser estático, no nulo y compatible, y puede ser negativo.

```text
[1..8] by 2   -> {1, 3, 5, 7}
[1..8] by -2  -> {2, 4, 6, 8}
(1..8] by 2   -> {3, 5, 7}
[1..8) by -2  -> {2, 4, 6}
```

El signo determina el anclaje y puede cambiar los miembros del dominio, pero el orden de generación no forma parte del tipo. `all` materializa los miembros en el orden canónico del tipo.

Los dominios escalonados pueden aparecer en cualquier contexto que admita un dominio: campos, componentes, participantes, `given`, formas derivadas, campos públicos y otros propietarios compatibles.

## Intervalos discontinuos y dominios cíclicos de punto

En una forma normalizada con varios segmentos disjuntos el paso se reinicia en cada segmento. Un paso positivo recorre segmentos de menor a mayor y se ancla en el extremo inferior; uno negativo recorre de mayor a menor y se ancla en el superior.

La sintaxis consolidada de intervalos discontinuos sigue abierta en Q-018. D-088 cierra el recorrido descendente explícito: se expresa mediante paso negativo, nunca invirtiendo extremos.

Un dominio cíclico de punto puede enumerarse con diferencia compatible, pero solo durante un periodo fundamental. No se envuelve indefinidamente.

## Otras construcciones con `by`

`by` de progresión se admite también en selección y en `exists`, `forall`, `count`, `sum`, `min` y `max`, siempre que la fuente ofrezca progresión mediante diferencia. No significa stride sobre una colección arbitraria. Una fuente futura puede definir expresamente esa capacidad; esta decisión no introduce un protocolo general. `ordered by path` conserva una semántica distinta.

## Azar

D-088 no permite azar en el filtro de una iteración. Se conserva la prohibición de D-048 hasta que Q-032 cierre identidad de puntos aleatorios, subsemillas y caché por ocurrencia.

## Consecuencias para AST

El AST superficial reemplaza `BooleanBlock` por `ExpressionBlock`, conserva `step` opcional en `for each`, selección y cuantificadores, conserva filtros/cuerpos como `ExpressionBlock` y normaliza el cuerpo breve de `for each` al mismo `EffectBlock` que usa `then`. `by -2` no necesita nodo especial para el signo.

## Diagnósticos

Debe diagnosticarse ausencia de `:`, paso cero, diferencia incompatible, falta de paso cuando no exista predeterminado, fuente infinita/no enumerable, `by` con `Rum`, `by` sobre fuente sin progresión, filtro no booleano, azar en filtro y uso de extremos invertidos como supuesto descenso.

## Verificación

Se verifican fuentes enumerables de todas las clases admitidas, `:` con cuerpo breve y con llaves, filtro breve y con locales, pasos positivos/negativos/runtime, cero estático/runtime, límites abiertos/cerrados, intervalos vacíos/infinitos/discontinuos, dominios escalonados firmados y `all`, `Num`, rechazo `Rum`, selección y seis cuantificadores con `by` y bloque, magnitudes con unidades compatibles, puntos con diferencia lineal, ciclo durante un periodo fundamental y diferencia entre filtro ordenado/no ordenado.
'''
adr_path='notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md'
if p(adr_path).exists(): raise SystemExit('D-088 already exists')
write(adr_path, adr88)

mods={
'notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md':'''## Modificación por D-088\n\nD-088 generaliza `by` a diferencias firmadas compatibles, evaluadas una vez, y distingue filtros ordenados (ven efectos secuenciales anteriores) de no ordenados (leen la instantánea inicial). Los seis cuantificadores/agregadores admiten `by` y bloques de expresión. `Rum` sigue sin ser enumerable y los dominios cíclicos de punto se recorren como máximo durante un periodo fundamental.''',
'notas/decisiones/ADR-057-gramatica-concreta-y-continuacion.md':'''## Modificación por D-088\n\n`:` es separador obligatorio en toda construcción que lo usa para introducir un cuerpo subordinado; las llaves no lo sustituyen. `for each` pasa a escribir siempre `:` antes de su efecto o bloque. Selecciones y cuantificadores conservan `:` también con `{ ... }`. La gramática añade `by` opcional a selección/cuantiﬁcadores y generaliza `boolean-block` a `expression-block`.''',
'notas/decisiones/ADR-071-vinculaciones-locales-en-bloques-booleanos.md':'''## Modificación por D-088\n\nLa estructura se generaliza a `ExpressionBlock(locals, result)`. Las condiciones mantienen sus contratos booleanos/temporales; selección y cuantificadores/agregadores pueden escribir tras `:` una expresión breve o `{ locales*; resultado }`, con las mismas reglas de pureza, secuencialidad, ámbito y ausencia de referencias adelantadas, ciclos, redeclaración y sombreado.''',
'notas/decisiones/ADR-075-dominios-enumerables-all-y-valores-derivados.md':'''## Modificación por D-088\n\nEl paso de un dominio escalonado deja de exigirse positivo. Sigue siendo estático, exacto, compatible y no nulo, pero puede ser firmado. Positivo ancla en el límite inferior y negativo en el superior; un límite inicial abierto avanza una vez antes del primer candidato. El signo puede cambiar la pertenencia, pero no introduce orden en el tipo; `all` usa el orden canónico. `Rum` continúa excluido.''',
'notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones.md':'''## Modificación por D-088\n\nLa selección pura admite `item in source by step: predicate` cuando la fuente define progresión por diferencia. No es stride sobre una colección arbitraria. El predicado puede ser una expresión breve o un `ExpressionBlock` con locales y sigue siendo puro y determinista. El AST conserva `step?` y el predicado como `ExpressionBlock`.''',
'notas/decisiones/ADR-082-cycle-como-modificador-de-dominio-de-punto.md':'''## Modificación por D-088\n\nUn dominio cíclico de punto puede alimentar una progresión exacta mediante diferencia compatible. La enumeración cubre un único periodo fundamental y nunca repite el ciclo indefinidamente. El signo y los límites se aplican al intervalo fundamental `[a..b)`.'''}
for rel,block in mods.items(): write(rel, append_once(read(rel),'## Modificación por D-088',block))

q18='notas/preguntas/Q-018-intervalos-discontinuos.md'; t=read(q18); t=add_frontmatter_item(t,'decisions','D-088'); t=exact(t,'Permanecen abiertos la sintaxis consolidada de intervalos discontinuos, el orden descendente explícito y varias claves.','Permanece abierta la sintaxis consolidada de intervalos discontinuos y sus claves. D-088 cierra el recorrido descendente explícito: se expresa mediante `by` con diferencia negativa, nunca invirtiendo extremos.','Q18'); write(q18,t)

g=read('especificacion/gramatica/mud.ebnf')
g=exact(g,'boolean-block\n    ::= { local-value-declaration , required-separation }\n        , boolean-expression\n        ;','expression-block\n    ::= { local-value-declaration , required-separation }\n        , expression\n        ;','block rename')
g=g.replace(', boolean-block',', expression-block')
g=exact(g,'expression-clause-body\n    ::= boolean-expression\n      | "{" , declaration-layout , expression-block\n          , [ required-separation ] , "}"\n      ;','expression-clause-body\n    ::= expression\n      | "{" , declaration-layout , expression-block\n          , [ required-separation ] , "}"\n      ;','clause body')
g=exact(g,'for-each-effect\n    ::= "for" , "each" , iteration-binding , "in" , expression\n        , [ "by" , expression ]\n        , [ "if" , boolean-expression ]\n        , effect-block\n        ;','for-each-effect\n    ::= "for" , "each" , iteration-binding , "in" , expression\n        , [ "by" , expression ]\n        , [ "if" , expression-clause-body ]\n        , ":"\n        , ( effect | effect-block )\n        ;','for each')
g=exact(g,'selection-expression\n    ::= iteration-binding , "in" , expression\n        , ":" , boolean-expression\n        ;','selection-expression\n    ::= iteration-binding , "in" , expression\n        , [ "by" , expression ]\n        , ":" , expression-clause-body\n        ;','selection')
g=exact(g,'quantifier-expression\n    ::= quantifier , variable-name , "in" , expression\n        , ":" , expression\n        ;','quantifier-expression\n    ::= quantifier , variable-name , "in" , expression\n        , [ "by" , expression ]\n        , ":" , expression-clause-body\n        ;','quantifier')
if 'boolean-block' in g: raise SystemExit('stale boolean-block')
write('especificacion/gramatica/mud.ebnf',g)

s=read('especificacion/sintaxis/mud-surface-ast.asdl').replace('boolean_block','expression_block').replace('BooleanBlock','ExpressionBlock')
s=exact(s,'           | ForEachEffect(iteration_binding binding,\n                           expr source,\n                           expr? order_key,\n                           expr? guard,\n                           effect_block body)','           | ForEachEffect(iteration_binding binding,\n                           expr source,\n                           expr? step,\n                           expression_block? filter,\n                           effect_block body)','foreach ast')
s=exact(s,'         | SelectionExpr(iteration_binding binding,\n                         expr source,\n                         expr predicate)\n         | QuantifierExpr(quantifier_kind kind,\n                          variable_name variable,\n                          expr source,\n                          expr body)','         | SelectionExpr(iteration_binding binding,\n                         expr source,\n                         expr? step,\n                         expression_block predicate)\n         | QuantifierExpr(quantifier_kind kind,\n                          variable_name variable,\n                          expr source,\n                          expr? step,\n                          expression_block body)','expr ast')
write('especificacion/sintaxis/mud-surface-ast.asdl',s)

cov=read('especificacion/sintaxis/cobertura-sintactica.yaml').replace('  boolean-block:\n','  expression-block:\n').replace('cst: BooleanBlockSyntax','cst: ExpressionBlockSyntax').replace('target: BooleanBlock','target: ExpressionBlock'); write('especificacion/sintaxis/cobertura-sintactica.yaml',cov)

k=read('especificacion/sintaxis/mud-syntax-kinds.yaml').replace('boolean-block','expression-block').replace('BooleanBlockSyntax','ExpressionBlockSyntax')
k=replace_yaml_block(k,'expression-block','''  expression-block:\n    kind: ExpressionBlockSyntax\n    rhs: "{ local-value-declaration , required-separation }\\n        , expression"\n    references:\n    - local-value-declaration\n    - required-separation\n    - expression''')
k=replace_yaml_block(k,'expression-clause-body','''  expression-clause-body:\n    kind: ExpressionClauseBodySyntax\n    rhs: "expression\\n      | \\\"{\\\" , declaration-layout , expression-block\\n          , [ required-separation ] , \\\"}\\\""\n    references:\n    - expression\n    - declaration-layout\n    - expression-block\n    - required-separation''')
k=replace_yaml_block(k,'for-each-effect','''  for-each-effect:\n    kind: ForEachEffectSyntax\n    rhs: "\\\"for\\\" , \\\"each\\\" , iteration-binding , \\\"in\\\" , expression\\n        , [ \\\"by\\\" , expression ]\\n        , [ \\\"if\\\" , expression-clause-body ]\\n        , \\\":\\\"\\n        , ( effect | effect-block )"\n    references:\n    - iteration-binding\n    - expression\n    - expression-clause-body\n    - effect\n    - effect-block''')
k=replace_yaml_block(k,'selection-expression','''  selection-expression:\n    kind: SelectionExpressionSyntax\n    rhs: "iteration-binding , \\\"in\\\" , expression\\n        , [ \\\"by\\\" , expression ]\\n        , \\\":\\\" , expression-clause-body"\n    references:\n    - iteration-binding\n    - expression\n    - expression-clause-body''')
k=replace_yaml_block(k,'quantifier-expression','''  quantifier-expression:\n    kind: QuantifierExpressionSyntax\n    rhs: "quantifier , variable-name , \\\"in\\\" , expression\\n        , [ \\\"by\\\" , expression ]\\n        , \\\":\\\" , expression-clause-body"\n    references:\n    - quantifier\n    - variable-name\n    - expression\n    - expression-clause-body''')
write('especificacion/sintaxis/mud-syntax-kinds.yaml',k)

con='especificacion/07-gramatica-concreta.md'; t=add_frontmatter_item(read(con),'decisions','D-088')
sec='''## `for each`, progresiones, selección y cuantificadores\n\n`for each` acepta cualquier fuente finita y enumerable: colecciones, diccionarios exactos, intervalos enumerables, dominios finitos enumerables y cualquier otro valor con enumeración canónica. Un intervalo no se convierte en colección por poder recorrerse.\n\n```mud\nfor each person in kingdom.people if person.hungry:\n    person.health -= 1\n\nfor each value in [0..100] by 5: {\n    doubled := value * 2\n    total += doubled\n}\n```\n\nEl `:` es obligatorio. Las llaves pertenecen al cuerpo posterior y no sustituyen el separador. El cuerpo breve debe ser un efecto o llamada a acción; el bloque comparte el contrato de `then`.\n\n### Filtro de iteración\n\n`by` precede a `if`. El filtro puede ser una expresión o un bloque de expresión con locales. Es puro y no estocástico. Con orden semántico se evalúa justo antes de cada iteración y observa efectos secuenciales anteriores; sin orden semántico todos los filtros leen la instantánea inicial y los deltas aceptados se consolidan simultáneamente. Un diccionario exacto puede vincular `(key, value)`.\n\n### Progresión `by`\n\n`by` recibe una diferencia firmada compatible y se evalúa una vez antes del recorrido runtime. Positivo ancla en el límite inferior y negativo en el superior. Un límite inicial abierto avanza una vez antes del primer candidato. La progresión termina antes del primer candidato exterior y no necesita alcanzar el extremo opuesto. Los extremos invertidos siguen produciendo `empty`.\n\n```text\n[1..8] by 2   -> 1, 3, 5, 7\n[1..8] by -3  -> 8, 5, 2\n(1..8] by 2   -> 3, 5, 7\n[1..8) by -2  -> 6, 4, 2\n```\n\nUn paso runtime demostrablemente cero es error estático; si puede variar y finalmente vale cero, produce `failed`. En un dominio escalonado cero siempre es error estático. La compatibilidad usa la operación de avance y conversiones implícitas exactas, no identidad nominal: `Nat` puede avanzar por `Int`, `Num` por diferencias exactas compatibles y las magnitudes por unidades compatibles. En una magnitud de punto el paso es una diferencia lineal.\n\n`by` no es stride sobre colecciones arbitrarias. `ordered by ruta` conserva otra semántica.\n\n### Pasos predeterminados y números\n\n`Nat` e `Int` usan `1`; `Money`, `0.01`. Omitir `by` elige siempre el paso positivo. Otros tipos exactos ordenados requieren paso explícito salvo siguiente canónico definido. `Num` admite paso exacto explícito y un intervalo general de `Num` sin paso es inválido. `Rum` nunca admite `by`; una colección explícita de `Rum` sí es enumerable.\n\n### Dominios escalonados\n\n`interval by step` usa la misma progresión para definir pertenencia y el paso estático puede ser negativo. El signo puede cambiar los miembros, pero el orden no forma parte del tipo. `all` materializa en orden canónico; `Nat in [1..8] by -2 = all` produce `2, 4, 6, 8`. En intervalos discontinuos el paso se reinicia por segmento; positivo recorre segmentos de menor a mayor y negativo al revés. Un dominio cíclico de punto recorre como máximo un periodo fundamental.\n\n### Selección y cuantificadores\n\nSelección y `exists`, `forall`, `count`, `sum`, `min`, `max` aceptan `by` cuando la fuente define progresión y mantienen `:` aunque el cuerpo tenga llaves. El bloque contiene locales `:=` seguidas de una expresión final. Selección, `exists`, `forall` y `count` exigen contrato booleano; `sum`, valor agregable; `min`/`max`, valor ordenable.\n\n```mud\nselected := x in source by step: {\n    threshold := limit\n    x < threshold\n}\n\nsum x in source by step: {\n    adjusted := x.amount - x.exempt\n    adjusted\n}\n```\n\nUna selección devuelve directamente las ocurrencias aceptadas y conserva multiplicidad, unicidad y orden demostrables. Su predicado sigue siendo puro y determinista.\n\n### `take` e indexación\n\n`take amount from source` conserva su semántica existente. Sobre fuente ordenada o con enumeración canónica toma el prefijo; sobre colección/diccionario no ordenado con elección real muestrea reproduciblemente sin reemplazo. La indexación posicional sigue exigiendo orden observable.\n'''
t=replace_md_section(t,'## `for each` y cuantificadores',sec); write(con,t)

abs='especificacion/08-sintaxis-abstracta.md'; t=add_frontmatter_item(read(abs),'decisions','D-088').replace('BooleanBlock','ExpressionBlock').replace('boolean_block','expression_block')
blocks='''## Bloques de expresión\n\nLa estructura común es `ExpressionBlock(locals, result)`. `locals` conserva las declaraciones `:=` y `result` la única expresión final. El nodo no fija el tipo del resultado: el propietario aplica su contrato booleano, temporal, agregable u ordenable. La forma breve normaliza a `ExpressionBlock([], expression)`. Las locales son puras, inmutables, secuenciales y sin referencias adelantadas, ciclos, redeclaración ni sombreado. El `otherwise` asociado no forma parte del bloque.\n'''
t=replace_md_section(t,'## Bloques booleanos',blocks)
needle='### Asignables\n\n`AssignableExpr` conserva una base y sufijos de miembro o índice. La comprobación de que la base designa un lugar escribible pertenece a resolución, tipos y efectos.\n'
t=exact(t,needle,needle+'\n### Iteración `for each`\n\n`ForEachEffect(binding, source, step?, filter?, body)` conserva la expresión `by`, el filtro como `ExpressionBlock` y normaliza efecto breve/bloque posterior a `:` a `EffectBlock`. Dirección, paso predeterminado, compatibilidad, orden del filtro y paso cero pertenecen a elaboración.\n','08 iteration')
t=t.replace('### Conversiones\n','''### Selección y cuantificadores\n\n`SelectionExpr(binding, source, step?, predicate)` conserva `step?` y normaliza el predicado a `ExpressionBlock`. `QuantifierExpr(kind, variable, source, step?, body)` hace lo mismo para los seis cuantificadores/agregadores. El AST no decide el contrato de tipo de `body`.\n\n### Conversiones\n''',1); write(abs,t)

proj='especificacion/sintaxis/cst-a-ast-superficial.md'; t=read(proj).replace('BooleanBlock','ExpressionBlock').replace('boolean_block','expression_block')
t=exact(t,'### Iteración\n\nLa vinculación simple produce `ValueIterationBinding`. La pareja entre paréntesis produce `DictionaryIterationBinding`.\n','### Iteración\n\nLa vinculación simple produce `ValueIterationBinding`. La pareja entre paréntesis produce `DictionaryIterationBinding`. `for each` conserva `by` como `step?`, normaliza `if` a `ExpressionBlock` y convierte tanto el efecto breve como el bloque tras `:` en `EffectBlock`. Dirección, compatibilidad y paso cero pertenecen a fases posteriores.\n','projection iteration')
t=exact(t,'`binding in source: predicate` produce `SelectionExpr(binding, source, predicate)`. La vinculación simple o de diccionario reutiliza respectivamente `ValueIterationBinding` o `DictionaryIterationBinding`; su alcance queda limitado al predicado.\n','`binding in source [by step]: predicate` produce `SelectionExpr(binding, source, step?, predicate)`. La vinculación simple o de diccionario reutiliza `ValueIterationBinding` o `DictionaryIterationBinding`; su alcance queda limitado al predicado. La forma breve y `{ locales*; resultado }` convergen en `ExpressionBlock`.\n\nLos cuantificadores/agregadores producen `QuantifierExpr(kind, variable, source, step?, body)`, con `body` como `ExpressionBlock`. La transformación no decide contrato de tipo ni admisibilidad de la progresión.\n','projection selection'); write(proj,t)

cases='especificacion/sintaxis/casos/cst-ast.yaml'; t=read(cases).replace('BooleanBlock','ExpressionBlock')
if 'id: for-each-requires-colon' not in t:
    t=t.rstrip()+'''\n- id: for-each-requires-colon\n  category: validation-before-ast\n  source: "action Iterate for mut total: Nat {\\n    then for each i in [1..5] {\\n        total += i\\n    }\\n}\\n"\n  cst_root: MudFileSyntax\n  expected_diagnostics: [for-each-missing-colon]\n  produces_ast: false\n- id: for-each-negative-step\n  category: effect\n  source: "action Iterate for mut total: Int {\\n    then for each i in [1..8] by -3:\\n        total += i\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: ForEachEffect(binding=i, source=1..8, step=PrefixExpr(UnaryMinus, 3), filter=None, body=EffectBlock(...))\n  produces_ast: true\n- id: for-each-filter-expression-block\n  category: effect\n  source: "action Feed for people: Person [* mut] {\\n    then for each person in people if {\\n        hungry := person.hunger > 0\\n        awake := person.state == Awake\\n        hungry and awake\\n    }:\\n        person.health += 1\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: ForEachEffect(filter=ExpressionBlock(locals=[hungry, awake], result=...), body=EffectBlock(...))\n  produces_ast: true\n- id: for-each-static-zero-step\n  category: validation-after-resolution\n  source: "action Broken for mut total: Int {\\n    then for each i in [1..8] by 0:\\n        total += i\\n}\\n"\n  cst_root: MudFileSyntax\n  expected_diagnostics: [progression-step-zero]\n  produces_ast: true\n- id: selection-by-expression-block\n  category: expression\n  source: "thing Sample {\\n    chosen := value in [1..10] by 2: {\\n        limit := 7\\n        value < limit\\n    }\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: SelectionExpr(value, 1..10, step=2, predicate=ExpressionBlock(locals=[limit], result=...))\n  produces_ast: true\n- id: quantifier-by-expression-block\n  category: expression\n  source: "rule Enough {\\n    count value in [1..10] by 2: {\\n        threshold := 5\\n        value >= threshold\\n    } > 0\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: QuantifierExpr(Count, value, 1..10, step=2, body=ExpressionBlock(locals=[threshold], result=...))\n  produces_ast: true\n- id: sum-by-expression-block\n  category: expression\n  source: "thing Sample {\\n    total := sum value in [1..10] by 2: {\\n        doubled := value * 2\\n        doubled\\n    }\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: QuantifierExpr(Sum, value, 1..10, step=2, body=ExpressionBlock(locals=[doubled], result=doubled))\n  produces_ast: true\n- id: negative-stepped-domain-all\n  category: domain\n  source: "thing Sample {\\n    values: Nat in [1..8] by -2 [4] = all\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: StoredFieldDecl(values, domain=SteppedDomain(1..8, PrefixExpr(UnaryMinus, 2)), defaultValue=AllLiteral)\n  normalizations: [signed-domain-step-preserved, all-materializes-domain-in-canonical-order]\n  produces_ast: true\n- id: rumber-stepped-domain-rejected\n  category: validation-after-resolution\n  source: "thing Sample {\\n    value: Rum in [r0..r1] by r0.1\\n}\\n"\n  cst_root: MudFileSyntax\n  expected_diagnostics: [rumber-progression-not-enumerable]\n  produces_ast: true\n- id: magnitude-step-compatible-units\n  category: validation-after-resolution\n  source: "action Walk for mut total: Length {\\n    then for each distance in [1 m..10 m] by 50 cm:\\n        total += distance\\n}\\n"\n  cst_root: MudFileSyntax\n  ast: ForEachEffect(step=QuantityValueExpr(50 cm), ...)\n  normalizations: [elaborate-compatible-difference-units]\n  produces_ast: true\n'''
write(cases,t)

for rel,needle in [('especificacion/gramatica/mud.ebnf','expression-block'),('especificacion/sintaxis/mud-surface-ast.asdl','ExpressionBlock(local_value_decl* locals, expr result)'),('notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md','## Paso cero')]:
    if needle not in read(rel): raise SystemExit(f'missing postcondition {needle} in {rel}')
print('D088_TRANSFORM_OK')
