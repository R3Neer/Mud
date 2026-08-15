from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def read(rel): return (root / rel).read_text(encoding='utf-8')
def write(rel, text): (root / rel).write_text(text.rstrip('\n') + '\n', encoding='utf-8', newline='\n')
def exact(text, old, new, label, count=1):
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f'{label}: expected {count}, found {actual}')
    return text.replace(old, new, count)
def relation(text, anchor, addition, label):
    if addition.strip() in text: return text
    return exact(text, anchor, anchor + addition, label)

# D-033 has a live for-each syntax example.
rel='notas/decisiones/ADR-033-claves-y-enumeracion-de-aliases.md'
t=read(rel)
t=exact(t,'for each coordinate in Coordinate {','for each coordinate in Coordinate: {','D033 foreach colon')
t=relation(t,'- Pregunta relacionada: Q-056\n','- Sintaxis actualizada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]\n','D033 traceability')
write(rel,t)

# D-034's rejected Rum example must be syntactically current so it fails for Rum, not for a missing colon.
rel='notas/decisiones/ADR-034-number-exacto-y-rumber-binary64.md'
t=read(rel)
t=exact(t,'for each value in [r0..r1] by r0.1 {}','for each value in [r0..r1] by r0.1: {}','D034 Rum foreach colon')
t=relation(t,'- Preguntas relacionadas: Q-019, Q-058\n','- Sintaxis actualizada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]\n','D034 traceability')
write(rel,t)

# All live examples in chapter 07 use the mandatory colon.
rel='especificacion/07-gramatica-concreta.md'
t=read(rel)
for old,new,label in [
('for each country in capitalOf {','for each country in capitalOf: {','07 dict keys colon'),
('for each (country, capital) in capitalOf {','for each (country, capital) in capitalOf: {','07 dict pairs colon'),
('then for each product in products {','then for each product in products: {','07 decision results colon'),
('then for each patient in patients {','then for each patient in patients: {','07 treatment colon'),
]:
    t=exact(t,old,new,label)
write(rel,t)

# Conformance cases using old syntax are updated. The direct-iteration-invalid case must fail for source semantics, not grammar.
rel='especificacion/sintaxis/casos/cst-ast.yaml'
t=read(rel)
for old,new,label in [
('for each country in capitals {','for each country in capitals: {','case dict keys colon'),
('for each (country, city) in capitals {','for each (country, city) in capitals: {','case dict pairs colon'),
('for each product in products {','for each product in products: {','case decision application colon'),
('for each result in policy {','for each result in policy: {','case invalid decision iteration colon'),
]:
    t=exact(t,old,new,label)
t=t.replace('id: boolean-block-with-locals','id: expression-block-with-locals')
t=t.replace('id: boolean-block-without-final-expression','id: expression-block-without-final-expression')
t=t.replace('category: boolean-block','category: expression-block')
t=t.replace('boolean-block-locals-and-result','expression-block-locals-and-result')
write(rel,t)

# Transformation prose uses the generalized term as well.
rel='especificacion/sintaxis/cst-a-ast-superficial.md'
t=read(rel)
t=exact(t,'## Bloques booleanos y tests','## Bloques de expresión y tests','projection block heading')
write(rel,t)

print('D088_EXAMPLE_SWEEP_OK')
