from pathlib import Path

ROOT = Path('.')


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one occurrence, found {count}: {old!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')


def write_new(path: str, content: str) -> None:
    p = ROOT / path
    if p.exists():
        raise SystemExit(f'{path}: already exists')
    p.write_text(content, encoding='utf-8', newline='\n')


# D-085 deja de prometer identidad pública para una rama funcional.
replace_once(
    'notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md',
    '- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]\n',
    '- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]] y [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]]\n',
)
replace_once(
    'notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md',
    'Las ramas son estáticas durante la ejecución ordinaria y no admiten efectos, llamadas a acciones, asignaciones, `create`, `destroy` ni mutación. El operador semántico o la edición del modelo pueden crear, actualizar, retirar o mover ramas mediante sus anclas propias. Una rama nueva se inserta antes de `_` de forma predeterminada; en un decisional ordenado puede declararse una posición concreta.\n',
    'Las ramas son estáticas durante la ejecución ordinaria y no admiten efectos, llamadas a acciones, asignaciones, `create`, `destroy` ni mutación. La edición del modelo puede crear, actualizar, retirar o mover ramas dentro del diccionario propietario, pero una rama no posee ancla pública ni descriptor metadata-bearing propio. El modelo resuelto usa una clave local de rama: el selector normalizado es su discriminante principal y las colisiones entre selectores iguales se distinguen mediante un índice local sin garantía de persistencia; `_` usa una clave de fallback propia. Una rama nueva se inserta antes de `_` de forma predeterminada; en un decisional ordenado puede declararse una posición concreta.\n',
)

# D-087 explicita la consecuencia que ya se desprendía de su principio de admisión.
replace_once(
    'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md',
    '- Amplía: [[ADR-035-organizacion-nombres-using-y-anclas|D-035]], [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]], [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].\n',
    '- Amplía: [[ADR-035-organizacion-nombres-using-y-anclas|D-035]], [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]], [[ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado|D-070]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].\n- Precisada por: [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]].\n',
)
replace_once(
    'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md',
    'No lo son expresiones, sentencias, operandos, condiciones, cuerpos de cláusula, tokens, nodos arbitrarios del AST ni ramas funcionales sin descriptor estable. `when`, `if`, `then`, `after` y `otherwise` pueden reflejarse como clases presentes mediante `~clauses`, pero sus cuerpos no se convierten en objetos metadata-bearing.\n',
    'No lo son expresiones, sentencias, operandos, condiciones, cuerpos de cláusula, tokens, nodos arbitrarios del AST ni ramas funcionales sin descriptor estable. Una rama de diccionario funcional tampoco posee ancla pública: D-090 le asigna únicamente una clave local dentro de su propietario para la representación resuelta. `when`, `if`, `then`, `after` y `otherwise` pueden reflejarse como clases presentes mediante `~clauses`, pero sus cuerpos no se convierten en objetos metadata-bearing.\n',
)

# Capítulo de nombres y anclas.
replace_once(
    'especificacion/09-nombres-y-anclas.md',
    '  - D-088\n',
    '  - D-088\n  - D-090\n',
)
replace_once(
    'especificacion/09-nombres-y-anclas.md',
    '- los valores incorporados `Prefix`, que se elaboran como constantes y no como declaraciones.\n',
    '- los valores incorporados `Prefix`, que se elaboran como constantes y no como declaraciones;\n- las ramas de diccionarios funcionales, que se identifican solo de forma local dentro de su diccionario propietario.\n',
)
replace_once(
    'especificacion/09-nombres-y-anclas.md',
    '## Anclas de ramas funcionales\n\nCada rama de un diccionario funcional recibe una ancla estable subordinada al ancla del diccionario. Su segmento propio no depende del ordinal fuente; mover una rama cambia su posición en un `FirstMatch`, pero no su identidad. El operador semántico puede dirigir `CREATE`, `UPDATE`, `REMOVE` y `MOVE` a esa ancla.\n\nLas operaciones conjuntistas de funcionales no crean ni fusionan anclas de rama: el nodo compuesto conserva referencias a ambos operandos y su grafo de dependencias es la unión transitiva de los dos.\n',
    '## Claves locales de ramas funcionales\n\n> [!rule] MUD-NAME-006 — Sin ancla pública de rama\n> Una rama de diccionario funcional no introduce símbolo anclado, nombre público ni propietario de metadatos. Su identidad persistente es la del diccionario que la contiene.\n\nEl AST resuelto conserva para cada rama una `decision_branch_key` local al diccionario. Para una rama ordinaria, la clave contiene la forma canónica del selector resuelto y un índice de colisión entre ramas con el mismo selector canónico. El índice solo garantiza unicidad dentro de esa representación resuelta y no constituye identidad persistente. `_` usa una clave `FallbackBranchKey` distinta. El ordinal fuente se conserva por separado porque participa en `FirstMatch`, pero tampoco se convierte en ancla.\n\nLas operaciones de tooling que requieran una referencia persistente deben dirigirse al diccionario propietario y expresar después la edición estructural de su conjunto o secuencia de ramas. `CREATE`, `UPDATE`, `REMOVE` y `MOVE` no pueden tratar una rama como entidad global independiente.\n\nLas operaciones conjuntistas de funcionales no crean ni fusionan claves globales de rama: el nodo compuesto conserva referencias a ambos operandos y su grafo de dependencias es la unión transitiva de los dos.\n',
)
replace_once(
    'especificacion/09-nombres-y-anclas.md',
    'El esquema mecánico [[mud-resolved-ast]] representa esta frontera: una declaración persistente y todo participante declarado usan `AnchoredSymbol`; los locales e iteradores ordinarios usan `LocalSymbol` subordinado a su propietario.\n',
    'El esquema mecánico [[mud-resolved-ast]] representa esta frontera: una declaración persistente y todo participante declarado usan `AnchoredSymbol`; los locales e iteradores ordinarios usan `LocalSymbol` subordinado a su propietario. Las ramas funcionales no son símbolos: sus dependencias se reconstruyen mediante el ancla del diccionario propietario y una `decision_branch_key` local.\n',
)

# Capítulo AST: la sintaxis superficial conserva ramas sin inventar identidad.
replace_once(
    'especificacion/08-sintaxis-abstracta.md',
    '  - D-088\n',
    '  - D-088\n  - D-090\n',
)
replace_once(
    'especificacion/08-sintaxis-abstracta.md',
    'Los paréntesis exigidos por la gramática para un diccionario anidado no sobreviven al AST.\n',
    'Los paréntesis exigidos por la gramática para un diccionario anidado no sobreviven al AST.\n\nLas ramas de un diccionario funcional permanecen nodos de valor en el AST superficial y no reciben `AnchoredSymbol` ni ancla sintética. La resolución conserva su orden fuente y deriva una `decision_branch_key` local al diccionario a partir del selector normalizado; esa clave sirve para reconstrucción y dependencias internas, no para resolución nominal ni metadatos.\n',
)

# Contrato mecánico del AST resuelto.
replace_once(
    'especificacion/sintaxis/mud-resolved-ast.asdl',
    '    decision_mode = FirstMatch | AllMatches\n\n',
    '    decision_mode = FirstMatch | AllMatches\n\n    decision_branch_key = SelectorBranchKey(string canonical_selector, int duplicate_index)\n                        | FallbackBranchKey\n\n',
)
replace_once(
    'especificacion/sintaxis/mud-resolved-ast.asdl',
    '    resolved_decision_branch = ResolvedDecisionBranch(anchor identity,\n                                                       anchor dictionary,\n                                                       int source_ordinal,\n',
    '    resolved_decision_branch = ResolvedDecisionBranch(decision_branch_key key,\n                                                       anchor dictionary,\n                                                       int source_ordinal,\n',
)
replace_once(
    'especificacion/sintaxis/mud-resolved-ast.asdl',
    '                    | DecisionDependsOn(anchor branch, symbol_id target)\n',
    '                    | DecisionDependsOn(anchor dictionary, decision_branch_key branch, symbol_id target)\n',
)

# Decisión nueva que registra el cierre de la contradicción.
write_new(
    'notas/decisiones/ADR-090-ramas-funcionales-sin-ancla-publica.md',
    '''---\nid: D-090\ntitle: "Ramas funcionales sin ancla pública"\nstatus: vigente\ndate: 2026-08-16\nsupersedes: []\nsuperseded-by: []\nquestions: []\naffects:\n  - "diccionarios funcionales, anclas, AST resuelto, grafo de dependencias, operador semántico y tooling"\n---\n\n# ADR-090 — Ramas funcionales sin ancla pública\n\n- Modifica: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].\n- Precisa: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n- Amplía: [[ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]] y [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].\n\n## Contexto\n\nD-085 asignaba anclas propias a las ramas de diccionarios funcionales para poder editarlas de forma independiente. D-087 fijó después un principio más estricto: una entidad metadata-bearing necesita descriptor tipado y ancla pública estable, y excluyó expresamente las ramas funcionales por carecer de descriptor estable. Mantener una ancla pública de rama conservaría dos modelos de identidad incompatibles.\n\n## Decisión\n\nUna rama de diccionario funcional no posee ancla pública, no introduce `AnchoredSymbol` y no puede poseer metadatos propios. La entidad persistente es el diccionario propietario.\n\nEl AST resuelto asigna a cada rama una clave local `decision_branch_key`:\n\n```text\nSelectorBranchKey(canonical_selector, duplicate_index)\nFallbackBranchKey\n```\n\n`canonical_selector` es la forma canónica del selector después de resolución y normalización semántica suficiente para reconstruir la rama. Si varias ramas tienen el mismo selector canónico, `duplicate_index` las distingue solo dentro de la representación resuelta actual. Ese índice no es una ancla, no participa en resolución nominal y no promete estabilidad entre ediciones. El fallback `_` usa una variante propia y única por diccionario.\n\nEl `source_ordinal` continúa conservándose por separado. En `FirstMatch` forma parte del valor funcional porque decide prioridad; en `AllMatches` conserva procedencia y diagnóstico, pero no se convierte en identidad persistente.\n\nLas dependencias de una rama se representan mediante el par formado por el ancla del diccionario propietario y su clave local. Una operación externa que necesite persistencia se dirige al diccionario y expresa la edición de sus ramas como estructura interna del propietario; no puede tratar la rama como entidad global independiente.\n\n## Consecuencias\n\n- Se elimina la contradicción entre D-085 y el principio de admisión de D-087.\n- Mover una rama ordenada puede cambiar semántica sin requerir migración de ancla.\n- Cambiar el selector puede cambiar la clave local sin constituir un renombrado de entidad pública.\n- Dos selectores canónicamente iguales siguen siendo representables; el índice de colisión evita introducir una prohibición nueva.\n- Las operaciones conjuntistas de diccionarios funcionales siguen siendo extensionales y no fusionan identidad de ramas.\n\n## Alternativas descartadas\n\n### Mantener anclas subordinadas por posición\n\nDescartada porque reordenar ramas de `FirstMatch` cambiaría identidad además de semántica y porque D-087 excluye la rama como entidad con descriptor estable.\n\n### Prohibir selectores duplicados para obtener una clave única\n\nDescartada en esta decisión porque convertiría una necesidad de representación en una restricción semántica nueva.\n\n## Verificación\n\n1. `mud-resolved-ast.asdl` no representa la identidad de `ResolvedDecisionBranch` mediante `anchor`.\n2. `DecisionDependsOn` conserva el ancla del diccionario y una clave local de rama.\n3. El catálogo de anclas no enumera ramas funcionales como entidades públicas.\n4. D-085 ya no promete `CREATE`, `UPDATE`, `REMOVE` o `MOVE` dirigidos a una ancla de rama.\n5. D-087 mantiene las ramas fuera de la superficie metadata-bearing.\n''',
)

print('GLOBAL_COHERENCE_PHASE3_DICTIONARY_OK')
