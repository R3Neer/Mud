from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def r(p): return (ROOT/p).read_text(encoding='utf-8')
def w(p,t): (ROOT/p).write_text(t,encoding='utf-8',newline='\n')
def one(p,o,n):
    t=r(p); c=t.count(o)
    if c!=1: raise SystemExit(f'{p}: expected one {o!r}, got {c}')
    w(p,t.replace(o,n,1))

# D-092
adr='''---
id: D-092
title: "Tipos de solo lectura completos en `given`"
status: vigente
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "firmas given, diccionarios, capacidades, gramática, CST, AST y diagnósticos"
---
# ADR-092 — Tipos de solo lectura completos en `given`

- Modifica: [[ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]].
- Amplía: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].

## Contexto

`given` representa parámetros auxiliares de solo lectura. D-063 prohíbe tanto mutabilidad exterior como capacidad interior `mut`, pero la gramática concreta restringía además accidentalmente el tipo superior de un `given` a `union-type-expression`, de modo que una flecha de diccionario válida en campos o participantes `for` no podía escribirse como parámetro auxiliar.

## Decisión

Un `given` admite la misma familia estructural de tipos necesaria para representar valores auxiliares, incluidos diccionarios exactos y decisionales y cadenas de flechas:

```mud
given prices: Product -> Money
given policy: Person --> Permission
given nested: A -> B -> C
```

La aceptación de diccionarios **no** concede capacidad de escritura. Ningún `collection-specification` contenido en el tipo completo de un `given`, a ninguna profundidad, puede contener `mut`. Esta regla es recursiva y se aplica también a colecciones o diccionarios escondidos por paréntesis, productos o componentes anidados.

La sintaxis directa usa `given-type-expression`, `given-dictionary-type` y `given-dictionary-link`, cuyas especificaciones de colección son las variantes readonly ya existentes. Los paréntesis continúan reutilizando `type-expression` para conservar la gramática general; después de construir el AST superficial, la validación estática recorre toda la forma y rechaza cualquier `collection_spec.elements_mutable = true` alcanzable desde el `given`.

El AST superficial no introduce una jerarquía paralela de tipos: normaliza las flechas readonly a los mismos `ExactDictionaryType` y `DecisionDictionaryType`, fijando a `false` toda capacidad interior procedente de la sintaxis `given`. `readonly_value_shape` conserva el contrato exterior de la firma.

## Consecuencias

- `given prices: Product -> Money` es válido.
- `given prices: Product -> Money [ordered]` es válido.
- `given prices: Product -> Money [mut]` se rechaza sintácticamente en la forma directa.
- `given prices: (Product -> Money [mut])` también se rechaza, esta vez por validación recursiva de la forma normalizada.
- La corrección no convierte `given` en sujeto mutable ni altera el contrato de llamada de D-063.

## Verificación

1. Diccionario exacto y decisional en `given`.
2. Cadena de diccionarios anidados.
3. Cardinalidad, `unique` y `ordered` readonly en cada enlace.
4. Rechazo de `mut` directo.
5. Rechazo de `mut` oculto bajo paréntesis, producto o nivel anidado.
6. Normalización a los constructores de diccionario generales con capacidad interior falsa.
'''
p=ROOT/'notas/decisiones/ADR-092-tipos-readonly-completos-en-given.md'
if p.exists(): raise SystemExit('D-092 exists')
p.write_text(adr,encoding='utf-8',newline='\n')

# grammar
p='especificacion/gramatica/mud.ebnf'; t=r(p)
old='''given-declaration
    ::= given-name , { "," , given-name } , ":" , union-type-expression , [ given-collection-specification ] , [ "=" , constant-expression ]
        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]
        ;

given-collection-specification
'''
new='''given-declaration
    ::= given-name , { "," , given-name } , ":" , given-type-expression , [ "=" , constant-expression ]
        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]
        ;

given-type-expression
    ::= union-type-expression
        , [ given-collection-specification | given-dictionary-type ]
        ;

given-dictionary-type
    ::= given-dictionary-link , { given-dictionary-link } ;

given-dictionary-link
    ::= dictionary-arrow , given-dictionary-value-type
        , [ given-collection-specification ]
      ;

given-dictionary-value-type
    ::= union-type-expression ;

given-collection-specification
'''
if old not in t: raise SystemExit('given grammar block')
t=t.replace(old,new,1); w(p,t)

# syntax-kinds structural replace region
p='especificacion/sintaxis/mud-syntax-kinds.yaml'; t=r(p)
start=t.index('  given-declaration:\n'); end=t.index('  given-collection-specification:\n',start)
new='''  given-declaration:
    kind: GivenDeclarationSyntax
    rhs: 'given-name , { "," , given-name } , ":" , given-type-expression , [ "=" , constant-expression ]\\n        , [ "{" , declaration-layout , [ metadata-assignment , { required-separation , metadata-assignment } , [ required-separation ] ] , "}" ]'
    references:
    - given-name
    - given-type-expression
    - constant-expression
    - declaration-layout
    - metadata-assignment
    - required-separation
  given-type-expression:
    kind: GivenTypeExpressionSyntax
    rhs: 'union-type-expression\\n        , [ given-collection-specification | given-dictionary-type ]'
    references:
    - union-type-expression
    - given-collection-specification
    - given-dictionary-type
  given-dictionary-type:
    kind: GivenDictionaryTypeSyntax
    rhs: given-dictionary-link , { given-dictionary-link }
    references:
    - given-dictionary-link
  given-dictionary-link:
    kind: GivenDictionaryLinkSyntax
    rhs: 'dictionary-arrow , given-dictionary-value-type\\n        , [ given-collection-specification ]'
    references:
    - dictionary-arrow
    - given-dictionary-value-type
    - given-collection-specification
  given-dictionary-value-type:
    kind: GivenDictionaryValueTypeSyntax
    rhs: union-type-expression
    references:
    - union-type-expression
'''
t=t[:start]+new+t[end:]; w(p,t)

# coverage insert new productions after given-declaration
p='especificacion/sintaxis/cobertura-sintactica.yaml'; t=r(p)
needle='''  given-declaration:
    cst: GivenDeclarationSyntax
    ast:
      disposition: constructor
      target: GivenDecl
'''
addition='''  given-type-expression:
    cst: GivenTypeExpressionSyntax
    ast:
      disposition: normalized
      target: readonly_value_shape
  given-dictionary-type:
    cst: GivenDictionaryTypeSyntax
    ast:
      disposition: normalized
      target: declared_type
  given-dictionary-link:
    cst: GivenDictionaryLinkSyntax
    ast:
      disposition: normalized
      target: declared_type
  given-dictionary-value-type:
    cst: GivenDictionaryValueTypeSyntax
    ast:
      disposition: normalized
      target: type_expr
'''
if needle not in t: raise SystemExit('coverage given declaration')
if '  given-type-expression:\n' not in t:
    t=t.replace(needle,needle+addition,1)
w(p,t)

# D063 current behavior + provenance.
p='notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md'; t=r(p)
marker='- Amplía: [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]]\n'
if marker not in t: raise SystemExit('D063 marker')
if 'D-092' not in t:
    t=t.replace(marker,marker+'- Modificada por: [[ADR-092-tipos-readonly-completos-en-given|D-092]]\n',1)
needle='Un `given` no admite mutabilidad exterior ni capacidad interior `mut`. Si una acción necesita escribir la colección suministrada o el estado de una `thing` recibida, ese valor constituye un sujeto de la operación y debe declararse mediante `for`.\n'
addition='''
El tipo de un `given` puede ser un diccionario exacto o decisional y puede encadenar flechas como cualquier otro valor auxiliar. La ausencia de capacidad es recursiva: ninguna colección o enlace de diccionario contenido en la forma completa, incluso bajo paréntesis o productos, puede declarar `mut`.
'''
if needle not in t: raise SystemExit('D063 readonly paragraph')
if addition.strip() not in t:
    t=t.replace(needle,needle+addition,1)
w(p,t)

# 07 explanation and provenance.
p='especificacion/07-gramatica-concreta.md'; t=r(p)
if '  - D-092\n' not in t:
    t=t.replace('  - D-091\n','  - D-091\n  - D-092\n',1)
marker='## `family`\n'
addition='''## Tipos de `given`

`given` usa una forma de tipo de solo lectura que admite diccionarios completos:

```mud
rule HasPrice given prices: Product -> Money {
    true
}
```

Las flechas se normalizan a los mismos tipos diccionario del resto de MUD, pero toda especificación de colección de la forma completa debe carecer de `mut`. La comprobación es recursiva y rechaza también una capacidad mutable oculta dentro de paréntesis, productos o niveles anidados.

'''
if addition.strip() not in t:
    if marker not in t: raise SystemExit('07 family marker')
    t=t.replace(marker,addition+marker,1)
w(p,t)

# 08 explanation; no AST schema change.
p='especificacion/08-sintaxis-abstracta.md'; t=r(p)
if '  - D-092\n' not in t:
    t=t.replace('  - D-091\n','  - D-091\n  - D-092\n',1)
marker='## Magnitudes\n'
addition='''## Tipos readonly de `given`

La subgramática `given-type-expression` no crea una familia AST paralela. Se normaliza a `readonly_value_shape`; sus flechas producen los constructores generales `ExactDictionaryType` y `DecisionDictionaryType`. Toda especificación readonly se traduce con `elements_mutable = false`, y una pasada estática recursiva rechaza cualquier `collection_spec` mutable que haya entrado a través de una forma parentizada general.

'''
if addition.strip() not in t:
    if marker not in t: raise SystemExit('08 magnitude marker')
    t=t.replace(marker,addition+marker,1)
w(p,t)

# cst->ast documentation
p='especificacion/sintaxis/cst-a-ast-superficial.md'; t=r(p)
marker='## `family`\n'
addition='''## Tipos de `given`

`given-type-expression`, `given-dictionary-type`, `given-dictionary-link` y `given-dictionary-value-type` son envoltorios concretos de una forma readonly. La transformación construye los mismos `declared_type` de diccionario usados por `type-expression`, pero convierte cada `given-collection-specification` en una colección con capacidad interior falsa y mantiene el exterior en `readonly_value_shape`.

Después de normalizar, la validación recorre la forma completa. Si cualquier subárbol procedente de una forma general parentizada conserva `elements_mutable = true`, el `given` es inválido aunque la palabra `mut` no aparezca en el nivel exterior.

'''
if addition.strip() not in t:
    if marker not in t: raise SystemExit('cst family marker')
    t=t.replace(marker,addition+marker,1)
w(p,t)

# cases
p='especificacion/sintaxis/casos/cst-ast.yaml'; t=r(p)
cases='''- id: given-exact-dictionary
  category: given
  source: "rule HasPrice given prices: Product -> Money {\\n    true\\n}\\n"
  cst_root: MudFileSyntax
  ast: GivenDecl(prices, ExactDictionaryType(Product, Money), readonly=true)
  normalizations:
  - given-dictionary-to-general-dictionary-type
  produces_ast: true
- id: given-decision-dictionary-ordered
  category: given
  source: "rule Policy given policy: Person --> Permission [ordered] {\\n    true\\n}\\n"
  cst_root: MudFileSyntax
  ast: GivenDecl(policy, DecisionDictionaryType(Person, Permission, ordered), readonly=true)
  normalizations:
  - given-dictionary-to-general-dictionary-type
  produces_ast: true
- id: given-hidden-mut-invalid
  category: validation-before-ast
  source: "rule Bad given prices: (Product -> Money [mut]) {\\n    true\\n}\\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - given-type-cannot-contain-mut
  produces_ast: false
'''
if 'id: given-exact-dictionary' not in t:
    t=t.rstrip()+'\n'+cases
w(p,t)

print('PHASE4_GIVEN_OK')
