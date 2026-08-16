from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def r(p): return (ROOT/p).read_text(encoding='utf-8')
def w(p,t): (ROOT/p).write_text(t,encoding='utf-8',newline='\n')
def one(p,o,n):
    t=r(p); c=t.count(o)
    if c!=1: raise SystemExit(f'{p}: {o!r} count={c}')
    w(p,t.replace(o,n,1))

# D-090
d='''---
id: D-090
title: "Claves locales de entradas de diccionario sin anclas de rama"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "diccionarios exactos y decisionales, edición semántica, anclas, AST resuelto y dependencias"
---
# ADR-090 — Claves locales de entradas de diccionario sin anclas de rama

- Modifica: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].
- Amplía: [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].

## Contexto

Las asociaciones de un diccionario exacto son entradas estructurales identificables por su clave y nunca necesitaron identidad pública propia. D-085, en cambio, otorgó anclas a las ramas decisionales para que la edición del modelo pudiera localizarlas. Esa asimetría es innecesaria: direccionar una entrada dentro de su contenedor no exige convertirla en entidad nominal persistente.

## Decisión

### Entradas estructurales

Ni una asociación `key -> value` ni una rama `selector --> result` posee ancla pública, descriptor nominal independiente ni metadatos propios. Ambas forman parte del valor diccionario que las contiene.

La identidad local de una entrada se expresa mediante su clave dentro del diccionario:

- en un diccionario exacto, la clave ordinaria de la asociación;
- en un diccionario decisional, la representación canónica del selector;
- `_` es la clave especial única del fallback decisional.

Una clave local no pertenece al espacio global de anclas y no puede copiarse como sustituto de `~anchor`.

### Clave canónica decisional

La clave decisional depende **solo del selector**, nunca del resultado ni de la posición. Se obtiene de la forma canónica estructural del selector después de la normalización sintáctica necesaria para eliminar diferencias no semánticas de escritura. Whitespace, trivia y separadores numéricos no crean claves distintas cuando el AST superficial normalizado ya los ha eliminado.

MUD no exige demostrar equivalencia lógica para identificar claves. Dos selectores con formas canónicas distintas, como `value.age < 18` y `value.age <= 17`, siguen siendo claves distintas aunque en un dominio concreto pudieran coincidir extensionalmente.

Dentro de un mismo diccionario dos ramas no pueden tener la misma clave canónica. La restricción se aplica también en modo `ordered`. El fallback `_` puede aparecer como máximo una vez.

### Edición

Cambiar únicamente el resultado de una rama conserva su clave local. Cambiar el selector retira la entrada con la clave anterior y crea una entrada con la nueva.

`CREATE`, `UPDATE`, `REMOVE` y, en un decisional `ordered`, `MOVE` localizan una rama mediante el par conceptual `(diccionario, clave-canónica)`. `MOVE` cambia exclusivamente la posición y no altera la clave. Para indicar una posición relativa, las entradas vecinas se direccionan por sus propias claves locales.

La representación concreta del protocolo editorial puede serializar este par de otra manera, pero no lo eleva a ancla pública.

### Representación resuelta

El AST/IR puede conservar una `decision_branch_key` interna formada por el símbolo propietario del diccionario y el selector canónico. Ese identificador local sirve para dependencias y edición, pero no es `AnchoredSymbol` ni participa en migración de anclas.

## Consecuencias

- desaparece la categoría conceptual de «ancla de rama funcional»;
- las ramas continúan sin ser metadata-bearing;
- `MOVE` ya no se usa como argumento para fabricar identidad global;
- exactos y decisionales comparten el principio de «entrada direccionada por clave»;
- cambiar una condición decisional cambia la clave local de la entrada.

## Verificación

1. Ningún descriptor de rama expone `~anchor`.
2. Dos ramas con selector canónico idéntico se rechazan incluso en `ordered`.
3. Cambiar solo el resultado conserva la clave.
4. Cambiar el selector equivale a `REMOVE` + `CREATE` a efectos de identidad local.
5. `MOVE` conserva selector y clave.
6. El AST resuelto no usa `anchor` como identidad de una rama.
'''
p=ROOT/'notas/decisiones/ADR-090-claves-locales-de-entradas-de-diccionario.md'
if p.exists(): raise SystemExit('D-090 exists')
p.write_text(d,encoding='utf-8',newline='\n')

# D-085 current semantics.
p='notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md'
t=r(p)
marker='- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]\n'
if marker not in t: raise SystemExit('D085 provenance marker')
t=t.replace(marker,marker+'- Modificada por: [[ADR-090-claves-locales-de-entradas-de-diccionario|D-090]]\n',1)
old='Las ramas son estáticas durante la ejecución ordinaria y no admiten efectos, llamadas a acciones, asignaciones, `create`, `destroy` ni mutación. El operador semántico o la edición del modelo pueden crear, actualizar, retirar o mover ramas mediante sus anclas propias. Una rama nueva se inserta antes de `_` de forma predeterminada; en un decisional ordenado puede declararse una posición concreta.'
new='Las ramas son estáticas durante la ejecución ordinaria y no admiten efectos, llamadas a acciones, asignaciones, `create`, `destroy` ni mutación. No poseen ancla propia: el operador semántico o la edición del modelo las localizan dentro del diccionario por la forma canónica de su selector, con `_` como clave especial del fallback. El resultado no forma parte de esa clave. Una rama nueva se inserta antes de `_` de forma predeterminada; en un decisional ordenado puede declararse una posición concreta mediante claves locales.'
if old not in t: raise SystemExit('D085 branch anchor paragraph')
t=t.replace(old,new,1)
# insert uniqueness rule in both modes-independent paragraph
needle='Un diccionario decisional:\n\n'
addition='Dos ramas del mismo diccionario con el mismo selector canónico son inválidas, aunque el diccionario sea `ordered`; MUD no intenta demostrar equivalencia lógica entre selectores canónicamente distintos. `_` puede aparecer como máximo una vez.\n\n'
if addition not in t:
    if needle not in t: raise SystemExit('D085 dictionary marker')
    t=t.replace(needle,addition+needle,1)
w(p,t)

# 09 replace public anchor section with local keys.
p='especificacion/09-nombres-y-anclas.md'; t=r(p)
old='''## Anclas de ramas funcionales

Cada rama de un diccionario funcional recibe una ancla estable subordinada al ancla del diccionario. Su segmento propio no depende del ordinal fuente; mover una rama cambia su posición en un `FirstMatch`, pero no su identidad. El operador semántico puede dirigir `CREATE`, `UPDATE`, `REMOVE` y `MOVE` a esa ancla.

Las operaciones conjuntistas de funcionales no crean ni fusionan anclas de rama: el nodo compuesto conserva referencias a ambos operandos y su grafo de dependencias es la unión transitiva de los dos.
'''
new='''## Claves locales de entradas de diccionario

Las asociaciones exactas y las ramas decisionales no poseen ancla pública propia. Son entradas estructurales del valor diccionario y se direccionan dentro de su contenedor mediante una clave local conforme a D-090.

En un diccionario exacto se usa la clave ordinaria. En un decisional se usa la forma canónica del selector; el resultado y la posición no participan en esa clave y `_` es la clave especial del fallback. `CREATE`, `UPDATE`, `REMOVE` y `MOVE` pueden usar el par `(diccionario, clave-local)` sin convertirlo en `AnchoredSymbol` ni someterlo a migración de anclas.

Las operaciones conjuntistas de funcionales no crean ni fusionan identidades de rama: el nodo compuesto conserva referencias a ambos operandos y su grafo de dependencias es la unión transitiva de los dos.
'''
if old not in t: raise SystemExit('09 branch anchor section')
t=t.replace(old,new,1)
# add D090 in frontmatter
if '  - D-090\n' not in t:
    t=t.replace('  - D-088\n---','  - D-088\n  - D-090\n---',1)
w(p,t)

# Resolved AST internal composite branch key, never anchor.
p='especificacion/sintaxis/mud-resolved-ast.asdl'; t=r(p)
needle='    decision_mode = FirstMatch | AllMatches\n\n'
if needle not in t: raise SystemExit('resolved decision_mode')
t=t.replace(needle,needle+'    decision_branch_key = (symbol_id dictionary, string canonical_selector)\n\n',1)
old='''    resolved_decision_branch = ResolvedDecisionBranch(anchor identity,
                                                       anchor dictionary,
                                                       int source_ordinal,
                                                       string is_fallback,
                                                       resolved_expr selector,
                                                       resolved_expr result,
                                                       symbol_id* external_reads)
'''
new='''    resolved_decision_branch = ResolvedDecisionBranch(decision_branch_key key,
                                                       int source_ordinal,
                                                       string is_fallback,
                                                       resolved_expr selector,
                                                       resolved_expr result,
                                                       symbol_id* external_reads)
'''
if old not in t: raise SystemExit('resolved branch constructor')
t=t.replace(old,new,1)
old='                    | DecisionDependsOn(anchor branch, symbol_id target)\n'
new='                    | DecisionDependsOn(decision_branch_key branch, symbol_id target)\n'
if old not in t: raise SystemExit('DecisionDependsOn')
t=t.replace(old,new,1)
w(p,t)

# 08 notes resolved distinction.
p='especificacion/08-sintaxis-abstracta.md'; t=r(p)
marker='## Familias\n'
addition='''## Entradas de diccionario

Las asociaciones exactas y ramas decisionales permanecen estructuras internas del valor diccionario; no se convierten en declaraciones ancladas. El AST resuelto puede asignar a una rama una `decision_branch_key` interna compuesta por su diccionario propietario y el selector canónico para dependencias y edición. Esa clave no es una ancla pública y el resultado de la rama no participa en ella.

'''
if addition.strip() not in t:
    if marker not in t: raise SystemExit('08 family marker')
    t=t.replace(marker,addition+marker,1)
if '  - D-090\n' not in t:
    t=t.replace('  - D-088\n---','  - D-088\n  - D-090\n---',1)
w(p,t)

print('PHASE3A_DICTIONARY_KEYS_OK')
