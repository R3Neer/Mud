from pathlib import Path
import sys

ROOT=Path(sys.argv[1]).resolve()

def read(rel): return (ROOT/rel).read_text(encoding='utf-8')
def write(rel,text): (ROOT/rel).write_text(text.rstrip('\n')+'\n',encoding='utf-8',newline='\n')
def exact(text,old,new,label):
    n=text.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1, found {n}')
    return text.replace(old,new,1)
def add_relation(text,marker,line,label):
    if line in text: return text
    if text.count(marker)!=1: raise SystemExit(f'{label}: relation marker mismatch')
    return text.replace(marker,marker+line,1)

# 08
rel='especificacion/08-sintaxis-abstracta.md'; t=read(rel)
t=exact(t,
'''El contrato de la fase posterior vive en [[mud-resolved-ast]]. Allí las referencias se sustituyen por `AnchoredSymbol` o `LocalSymbol`, las uniones quedan normalizadas y el grafo nominal se expresa mediante aristas reconstruibles.''',
'''La resolución nominal opera sobre este AST sin fabricar un segundo árbol normativo: produce símbolos, bindings, anclas y un grafo nominal parcial. Tras tipado y elaboración, el contrato semántico vive en `ir/mud-semantic-ir.asdl`, donde aparecen tipos efectivos, dominios, cardinalidades, dependencias y otras formas elaboradas.''',
'08 phase contract')
t=exact(t,
'''→ resolución de nombres\n→ AST resuelto\n→ tipado y elaboración\n→ IR''',
'''→ resolución nominal: símbolos + bindings + grafo parcial\n→ tipado y elaboración\n→ IR semántico''',
'08 pipeline')
t=exact(t,
'''La clasificación como elemental o compuesta requiere resolver los `ActionCallCandidateEffect`; por ello pertenece al AST resuelto. La forma superficial no inventa una clasificación basada únicamente en la apariencia de un `postfix-expression`.''',
'''La clasificación como elemental o compuesta requiere resolver los `ActionCallCandidateEffect`; por ello pertenece al IR semántico después de resolución y elaboración. La forma superficial no inventa una clasificación basada únicamente en la apariencia de un `postfix-expression`.''',
'08 action classification')
write(rel,t)

# D-070
rel='notas/decisiones/ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado.md'; t=read(rel)
t=add_relation(t,'- Ampliada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]\n','- Ajustada a la frontera de fases de [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].\n','D070 relation')
t=exact(t,
'''→ resolución\n→ AST resuelto\n→ tipado/elaboración\n→ IR''',
'''→ resolución nominal: símbolos + bindings + grafo parcial\n→ tipado/elaboración\n→ IR semántico''',
'D070 pipeline')
t=exact(t,
'''Estas decisiones pertenecen al AST resuelto o elaborado.''',
'''Estas decisiones pertenecen a la resolución nominal cuando dependen solo de identidad y bindings, o al IR semántico cuando requieren tipado o elaboración.''',
'D070 deferred ambiguities')
write(rel,t)

# D-072
rel='notas/decisiones/ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas.md'; t=read(rel)
t=add_relation(t,'- Ampliada por: [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]]\n','- Ajustada a la frontera de fases de [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].\n','D072 relation')
t=exact(t,
'''La separación entre CST, AST superficial y AST resuelto exige fijar cómo se representan ámbitos y candidatos. También debe distinguirse qué nombres poseen identidad semántica persistente y qué nombres solo vinculan valores dentro de una declaración.''',
'''La separación entre CST, AST superficial, resultados de resolución nominal e IR semántico exige fijar cómo se representan ámbitos y candidatos. También debe distinguirse qué nombres poseen identidad semántica persistente y qué nombres solo vinculan valores dentro de una declaración.''',
'D072 context')
write(rel,t)

# D-073
rel='notas/decisiones/ADR-073-as-thing-explicito-redundante.md'; t=read(rel)
t=exact(t,'  - "especialización de thing, diagnósticos, AST resuelto, formateadores y acciones de código"','  - "especialización de thing, diagnósticos, resolución nominal, IR semántico, formateadores y acciones de código"','D073 affects')
t=add_relation(t,'- Modifica: [[ADR-018-as-declara-is-consulta|D-018]] y [[ADR-068-thing-universal-y-nombre-intrinseco|D-068]]\n','- Ajustada a la frontera de fases de [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].\n','D073 relation')
write(rel,t)

# D-074
rel='notas/decisiones/ADR-074-uniones-nominales-y-estrechamiento.md'; t=read(rel)
if 'D-093' not in t:
    marker='## Contexto\n'
    if t.count(marker)!=1: raise SystemExit('D074 context marker')
    t=t.replace(marker,'- Ajustada a la frontera de fases de [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].\n\n'+marker,1)
t=exact(t,'- El AST resuelto conserva alternativas nominales normalizadas y la alternativa elegida por cada incorporación.','- El IR semántico conserva alternativas nominales normalizadas y la alternativa elegida por cada incorporación.','D074 consequence')
write(rel,t)

# D-085
rel='notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md'; t=read(rel)
t=exact(t,'El AST resuelto o IR registra para cada decisional:','El IR semántico registra para cada decisional:','D085 semantic representation')
write(rel,t)

# D-086
rel='notas/decisiones/ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios.md'; t=read(rel)
t=exact(t,'Los tipos estructurales y las identidades singleton se rechazan antes de construir el AST resuelto.','Los tipos estructurales y las identidades singleton se rechazan durante tipado/elaboración antes de producir la forma correspondiente del IR semántico.','D086 reject stage')
t=exact(t,'Las operaciones conjuntistas pueden conservarse como `BinaryExpr` en el AST superficial porque su clase depende de los tipos resueltos. El AST resuelto o IR distingue:','Las operaciones conjuntistas pueden conservarse como `BinaryExpr` en el AST superficial porque su clase depende de los tipos resueltos. El IR semántico distingue:','D086 set ops')
t=exact(t,'El AST resuelto diferencia también:','El IR semántico diferencia también:','D086 tests')
write(rel,t)

# D-087
rel='notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md'; t=read(rel)
t=exact(t,'- El AST superficial conserva declaraciones de metadatos y cuerpos de metadatos; el AST resuelto distingue propiedades intrínsecas de valores `Metadata` configurados.','- El AST superficial conserva declaraciones de metadatos y cuerpos de metadatos; el IR semántico distingue propiedades intrínsecas de valores `Metadata` configurados.','D087 consequence')
write(rel,t)

print('ARCH_RESIDUES_TRANSFORM_OK')
