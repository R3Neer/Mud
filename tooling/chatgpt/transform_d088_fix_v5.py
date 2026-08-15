from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()


def read(rel):
    return (root / rel).read_text(encoding="utf-8")


def write(rel, text):
    (root / rel).write_text(text.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def exact(text, old, new, label, count=1):
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"{label}: expected {count}, found {actual}")
    return text.replace(old, new, count)


def replace_yaml_entry(text, key, next_key, replacement, label):
    start_marker = f"  {key}:\n"
    end_marker = f"  {next_key}:\n"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise SystemExit(f"{label}: could not locate unique entry boundaries")
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + replacement.rstrip("\n") + "\n" + text[end:]


# 1. Concrete grammar: ':' may be followed by physical separation before the body.
rel = "especificacion/gramatica/mud.ebnf"
t = read(rel)
t = exact(
    t,
    '''for-each-effect
    ::= "for" , "each" , iteration-binding , "in" , expression
        , [ "by" , expression ]
        , [ "if" , expression-body ]
        , ":"
        , ( effect | effect-block )
        ;''',
    '''for-each-effect
    ::= "for" , "each" , iteration-binding , "in" , expression
        , [ "by" , expression ]
        , [ "if" , expression-body ]
        , ":"
        , [ required-separation ]
        , ( effect | effect-block )
        ;''',
    "for-each separator",
)
t = exact(
    t,
    '''selection-expression
    ::= iteration-binding , "in" , expression
        , [ "by" , expression ]
        , ":" , expression-body
        ;''',
    '''selection-expression
    ::= iteration-binding , "in" , expression
        , [ "by" , expression ]
        , ":" , [ required-separation ] , expression-body
        ;''',
    "selection separator",
)
t = exact(
    t,
    '''quantifier-expression
    ::= quantifier , variable-name , "in" , expression
        , [ "by" , expression ]
        , ":" , expression-body
        ;''',
    '''quantifier-expression
    ::= quantifier , variable-name , "in" , expression
        , [ "by" , expression ]
        , ":" , [ required-separation ] , expression-body
        ;''',
    "quantifier separator",
)
write(rel, t)


# 2. Lossless CST catalog: keep rhs and reference inventory synchronized with the grammar.
rel = "especificacion/sintaxis/mud-syntax-kinds.yaml"
t = read(rel)
t = replace_yaml_entry(
    t,
    "for-each-effect",
    "iteration-binding",
    '''  for-each-effect:
    kind: ForEachEffectSyntax
    rhs: '"for" , "each" , iteration-binding , "in" , expression , [ "by" , expression ] , [ "if" , expression-body ] , ":" , [ required-separation ] , ( effect | effect-block )'
    references:
    - iteration-binding
    - expression
    - expression-body
    - required-separation
    - effect
    - effect-block''',
    "for-each syntax kind",
)
t = replace_yaml_entry(
    t,
    "selection-expression",
    "point-component-expression",
    '''  selection-expression:
    kind: SelectionExpressionSyntax
    rhs: 'iteration-binding , "in" , expression , [ "by" , expression ] , ":" , [ required-separation ] , expression-body'
    references:
    - iteration-binding
    - expression
    - required-separation
    - expression-body''',
    "selection syntax kind",
)
t = replace_yaml_entry(
    t,
    "quantifier-expression",
    "quantifier",
    '''  quantifier-expression:
    kind: QuantifierExpressionSyntax
    rhs: 'quantifier , variable-name , "in" , expression , [ "by" , expression ] , ":" , [ required-separation ] , expression-body'
    references:
    - quantifier
    - variable-name
    - expression
    - required-separation
    - expression-body''',
    "quantifier syntax kind",
)
write(rel, t)


# 3. Normative prose: make the accepted newline form explicit.
rel = "especificacion/07-gramatica-concreta.md"
t = read(rel)
t = exact(
    t,
    "El `:` es obligatorio. Las llaves pertenecen al cuerpo posterior y no sustituyen el separador. El cuerpo breve debe ser un efecto o llamada a acción; el bloque comparte el contrato de `then`.",
    "El `:` es obligatorio. Las llaves pertenecen al cuerpo posterior y no sustituyen el separador. El cuerpo puede comenzar en la misma línea o después de uno o más terminadores; esa separación física no cambia su estructura abstracta. El cuerpo breve debe ser un efecto o llamada a acción; el bloque comparte el contrato de `then`.",
    "07 separator prose",
)
write(rel, t)

rel = "notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md"
t = read(rel)
t = exact(
    t,
    "La forma sin `:` es inválida. El cuerpo de `for each` usa exactamente el contrato ejecutable de `then`: un único efecto o llamada a acción, o un bloque de efectos que puede intercalar vinculaciones locales `:=`.",
    "La forma sin `:` es inválida. Tras `:` el cuerpo puede comenzar en la misma línea o después de una separación física por terminadores; el salto no cambia el AST. El cuerpo de `for each` usa exactamente el contrato ejecutable de `then`: un único efecto o llamada a acción, o un bloque de efectos que puede intercalar vinculaciones locales `:=`.",
    "D088 separator prose",
)
write(rel, t)

rel = "especificacion/sintaxis/cst-sin-perdidas.md"
t = read(rel)
t = exact(
    t,
    "Entre las categorías concretas inventariadas se encuentra `ExpressionBlockSyntax`, que conserva en orden las declaraciones locales iniciales y la expresión final. La categoría no fija por sí sola el contrato de esa expresión: el propietario decide si debe ser booleana, temporal, agregable u ordenable. La CST no amplía por sí sola su ámbito hasta `otherwise`; esa relación se establece al proyectar y resolver la construcción propietaria.",
    "Entre las categorías concretas inventariadas se encuentra `ExpressionBlockSyntax`, que conserva en orden las declaraciones locales iniciales y la expresión final. La categoría no fija por sí sola el contrato de esa expresión: el propietario decide si debe ser booleana, temporal, agregable u ordenable. En `for each`, selección y cuantificadores, los `TERMINATOR` escritos entre `:` y el comienzo del cuerpo permanecen en la CST como separación concreta y desaparecen al proyectar el AST. La CST no amplía por sí sola su ámbito hasta `otherwise`; esa relación se establece al proyectar y resolver la construcción propietaria.",
    "CST separator prose",
)
write(rel, t)

rel = "especificacion/sintaxis/cst-a-ast-superficial.md"
t = read(rel)
anchor = "## Bloques booleanos y tests\n\n"
if anchor not in t:
    # D-088 may already have generalized the heading in a later transform.
    anchor = "## Bloques de expresión y tests\n\n"
if anchor not in t:
    raise SystemExit("CST->AST separator prose: heading not found")
addition = "Los terminadores opcionales escritos después de `:` en `for each`, selección y cuantificadores son separación concreta: no producen nodos ni cambian `ExpressionBlock`/`EffectBlock`.\n\n"
if addition not in t:
    t = t.replace(anchor, anchor + addition, 1)
write(rel, t)


# 4. D-047: distinguish canonical materialization order from explicit traversal direction.
rel = "notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md"
t = read(rel)
t = exact(
    t,
    "La enumeración canónica procede del tipo: orden declarado de una familia cerrada, producto lexicográfico de un alias estructural, orden del diccionario o colección, u orden ascendente de un intervalo.",
    "La enumeración canónica procede del tipo: orden declarado de una familia cerrada, producto lexicográfico de un alias estructural, orden del diccionario o colección, u orden ascendente de un intervalo cuando se materializa canónicamente. El orden de recorrido de una progresión explícita es independiente: `by` negativo recorre desde el límite superior hacia valores menores conforme a D-088 sin cambiar el orden canónico del tipo o dominio.",
    "D047 canonical order",
)
write(rel, t)


# 5. Reciprocal question traceability where D-088 actually narrows the open question.
rel = "notas/preguntas/Q-018-intervalos-discontinuos.md"
t = read(rel)
t = exact(
    t,
    "Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]] y [[notas/decisiones/ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]].",
    "Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]], [[notas/decisiones/ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]] y [[notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]].",
    "Q018 status traceability",
)
write(rel, t)

rel = "notas/preguntas/Q-028-finitud.md"
t = read(rel)
t = exact(
    t,
    "  - D-081\n",
    "  - D-081\n  - D-088\n",
    "Q028 decision list",
)
t = exact(
    t,
    "Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-044-alcanzabilidad-eventually|D-044]], [[notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita|D-047]] y [[notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]].",
    "Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-044-alcanzabilidad-eventually|D-044]], [[notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita|D-047]], [[notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]] y [[notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]].",
    "Q028 status traceability",
)
t = exact(
    t,
    "La incapacidad de demostrar finitud o enumerabilidad rechaza estáticamente el uso que las exige; no produce una respuesta negativa en runtime. La misma obligación se aplica a filtros y `take`. Falta definir el análisis y sus diagnósticos.",
    "La incapacidad de demostrar finitud o enumerabilidad rechaza estáticamente el uso que las exige; no produce una respuesta negativa en runtime. La misma obligación se aplica a filtros y `take`. D-088 mantiene esa exigencia para `for each`, selección y cuantificadores/agregadores, y limita los dominios cíclicos recorribles a un único periodo fundamental. Falta definir el análisis y sus diagnósticos.",
    "Q028 D088 scope",
)
write(rel, t)


# 6. Conformance examples for a body starting on the following line.
rel = "especificacion/sintaxis/casos/cst-ast.yaml"
t = read(rel)
case_marker = "- id: d088-for-each-body-after-terminator\n"
if case_marker in t:
    raise SystemExit("D088 v5 cases already present")
append = r'''
- id: d088-for-each-body-after-terminator
  category: iteration
  source: "action Accumulate for mut total: Int {\n    then for each i in [1..3]:\n        total += i\n}\n"
  cst_root: MudFileSyntax
  ast: ForEachEffect(binding=i, source=[1..3], body=EffectBlock(...))
  normalizations:
  - discard-separation-after-colon
  produces_ast: true
- id: d088-selection-body-after-terminator
  category: expression
  source: "thing Sample {\n    selected := x in [1..3]:\n        x > 1\n}\n"
  cst_root: MudFileSyntax
  ast: SelectionExpr(binding=x, source=[1..3], predicate=ExpressionBlock([], x > 1))
  normalizations:
  - discard-separation-after-colon
  produces_ast: true
- id: d088-quantifier-block-after-terminator
  category: expression
  source: "rule HasLarge {\n    exists x in [1..3]:\n        {\n            limit := 1\n            x > limit\n        }\n}\n"
  cst_root: MudFileSyntax
  ast: QuantifierExpr(Exists, x, [1..3], body=ExpressionBlock([limit], x > limit))
  normalizations:
  - discard-separation-after-colon
  produces_ast: true
'''
t = t.rstrip("\n") + "\n" + append.lstrip("\n")
write(rel, t)


# 7. Postconditions.
checks = {
    "especificacion/gramatica/mud.ebnf": [
        ', ":"\n        , [ required-separation ]\n        , ( effect | effect-block )',
        ', ":" , [ required-separation ] , expression-body',
    ],
    "especificacion/sintaxis/mud-syntax-kinds.yaml": [
        'for-each-effect:',
        'required-separation',
        'selection-expression:',
        'quantifier-expression:',
    ],
    "notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md": [
        "El orden de recorrido de una progresión explícita es independiente",
    ],
    "notas/preguntas/Q-028-finitud.md": ["  - D-088", "un único periodo fundamental"],
    "especificacion/sintaxis/casos/cst-ast.yaml": [
        "id: d088-for-each-body-after-terminator",
        "id: d088-selection-body-after-terminator",
        "id: d088-quantifier-block-after-terminator",
    ],
}
for rel, needles in checks.items():
    text = read(rel)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"missing {needle!r} in {rel}")

print("D088_FIX_V5_OK")
