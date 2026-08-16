from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one occurrence, found {count}: {old!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')


# Reciprocal traceability for the genuinely open shape question.
replace_once(
    'notas/decisiones/ADR-037-campos-y-dominios-declarativos.md',
    '''questions:\n  - "Q-003"\n  - "Q-017"\n''',
    '''questions:\n  - "Q-003"\n  - "Q-017"\n  - "Q-061"\n''',
)
replace_once(
    'notas/decisiones/ADR-038-familias-cerradas-de-valores.md',
    '''questions:\n  - "Q-024"\n  - "Q-047"\n''',
    '''questions:\n  - "Q-024"\n  - "Q-047"\n  - "Q-061"\n''',
)
replace_once(
    'notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md',
    'questions: []\n',
    'questions:\n  - "Q-061"\n',
)
replace_once(
    'notas/decisiones/ADR-091-datos-de-family-como-descriptores-anclados.md',
    'questions: []\n',
    'questions:\n  - "Q-061"\n',
)

# D-038's stored-data shape now shows the metadata body added by D-091.
replace_once(
    'notas/decisiones/ADR-038-familias-cerradas-de-valores.md',
    'nombre : tipo [in dominio] [especificación-de-colección] [= predeterminado]\n',
    'nombre : tipo [in dominio] [especificación-de-colección] [= predeterminado] [metadata-body]\n',
)

# The mechanical case must use the actual surface-ASDL field retained while Q-061 is open.
replace_once(
    'especificacion/sintaxis/casos/cst-ast.yaml',
    'CalculatedFamilyDataDecl(costly, type=Bool, metadata=[StoredMetadataAssignment(summary)])',
    'CalculatedFamilyDataDecl(costly, shape=ExplicitDerivedShape(Bool), metadata=[StoredMetadataAssignment(summary)])',
)

# Q-061 names the later decision that widened calculated-value shapes generally.
p = Path('notas/preguntas/Q-061-forma-de-datos-calculados-de-family.md')
text = p.read_text(encoding='utf-8')
text = text.replace(
    '''decisions:\n  - D-037\n  - D-038\n  - D-091\n''',
    '''decisions:\n  - D-037\n  - D-038\n  - D-085\n  - D-091\n''',
)
text = text.replace(
    'D-038 escribe `nombre [: tipo] := expresión` y excluye `in` y especificaciones de colección. La EBNF vigente, en cambio, usa `[ derived-value-shape ]`, que también reconoce dominio y forma colectiva. El AST superficial conserva esa forma amplia. D-091 añade identidad de descriptor y metadata-body a los datos asociados, pero no necesita elegir entre ambas variantes y por tanto deja esta contradicción abierta.\n',
    'D-038 escribe `nombre [: tipo] := expresión` y excluye `in` y especificaciones de colección. D-085 modificó D-037 y consolidó para los valores calculados una forma derivada más amplia; la EBNF vigente de `family` usa `[ derived-value-shape ]`, que también reconoce dominio y forma colectiva, y el AST superficial conserva esa forma. No está decidido si D-038 debe mantener su excepción estrecha o alinearse con la ampliación posterior. D-091 añade identidad de descriptor y metadata-body a los datos asociados, pero no necesita elegir entre ambas variantes y por tanto deja esta contradicción abierta.\n',
)
p.write_text(text, encoding='utf-8', newline='\n')

print('GLOBAL_COHERENCE_PHASE4C_TRACEABILITY_OK')
