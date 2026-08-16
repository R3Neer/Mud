from pathlib import Path
import re

ROOT = Path.cwd()
SCOPES = [ROOT/'notas'/'decisiones', ROOT/'especificacion']
FILES = []
for scope in SCOPES:
    if scope.is_dir():
        FILES.extend(p for p in scope.rglob('*') if p.is_file() and p.suffix.lower() in {'.md','.ebnf','.asdl','.yaml'})

patterns = {
    'anonymous-participants': re.compile(r'(?i)(an[oó]nim|omitir(?:se)?\s+(?:el\s+)?nombre|nombre\s+(?:es\s+)?opcional|rol\s+sin\s+nombre|participante\s+sin\s+nombre)'),
    'participant-anchor-denial': re.compile(r'(?i)(?:for|on|given).{0,100}(?:sin\s+ancla|no\s+(?:tiene|posee)[^\n]{0,20}ancla)|(?:roles?|participantes?)[^\n]{0,100}(?:sin\s+ancla|no\s+(?:tienen|poseen)[^\n]{0,20}ancla)'),
    'branch-public-anchor': re.compile(r'(?i)(ancla(?:s)?\s+(?:propia|p[uú]blica)?[^\n]{0,60}rama|rama(?:s)?[^\n]{0,80}ancla(?:s)?|branch[^\n]{0,60}anchor)'),
    'given-readonly-subgrammar': re.compile(r'(given-collection-specification|given-collection-modifier|ReadonlyValueShape|readonly_value_shape|ReadonlyCollectionSpec|readonly_collection_spec)'),
    'given-mut-loophole': re.compile(r'(?i)given[^\n]{0,140}(?:producci[oó]n\s+excluye\s+`?mut`?|solo[^\n]{0,30}(?:colecci[oó]n|nivel exterior))'),
    'empty-extrema-error': re.compile(r'(?i)(min[^\n]{0,80}max[^\n]{0,100}(?:fuente\s+vac[ií]a|vac[ií]o)[^\n]{0,60}(?:error|fall)|agregaci[oó]n\s+extrema\s+vac[ií]a[^\n]{0,50}(?:error|fall)|error\s+de\s+agregaci[oó]n\s+(?:extrema\s+)?vac[ií]a)'),
    'family-data-no-identity': re.compile(r'(?i)datos?\s+asociad[^\n]{0,100}(?:no\s+posee[^\n]{0,20}(?:identidad|ancla)|sin\s+(?:identidad|ancla))'),
    'family-member-name-field': re.compile(r'`name:\s*Text`\s+intr[ií]nseco'),
    'metadata-runtime-write': re.compile(
        r'(?i)(?:'
        r'(?:asignar|escribir|modificar|mutable)[^\n]{0,80}`?~(?:name|plural|abbreviation|summary|description)`?[^\n]{0,80}(?:runtime|ejecuci[oó]n)'
        r'|'
        r'`?~(?:name|plural|abbreviation)`?[^\n]{0,80}(?:asignable|mutable\s+en\s+runtime|escritura\s+runtime)'
        r')'
    ),
    'metadata-dot-syntax': re.compile(r'\.~[A-Za-z_]'),
    'metadata-recursive': re.compile(r'(?i)Metadata[^\n]{0,80}(?:puede\s+(?:tener|poseer)|metadata-bearing)[^\n]{0,80}metad'),
    'signature-property-universal': re.compile(r'(?i)(?:toda|cualquier)\s+(?:declaraci[oó]n|descriptor)[^\n]{0,100}`~(?:for|on|given)`|`~(?:for|on|given)`[^\n]{0,100}(?:toda|cualquier)\s+(?:declaraci[oó]n|descriptor))'),
    'resolved-ast-pretyping': re.compile(r'(?i)(AST\s+resuelto[^\n]{0,80}(?:antes\s+de|→)\s*(?:tipado|elaboraci[oó]n)|resoluci[oó]n\s+de\s+nombres\s*\n?→\s*AST\s+resuelto\s*\n?→\s*tipado)'),
    'contextual-cast-collapse': re.compile(r'(?i)(?:literal|construcci[oó]n)[^\n]{0,100}(?:contextual)[^\n]{0,100}(?:ConversionExpr|equivale[^\n]{0,20}`?to`?)'),
}

print('AUDIT_BEGIN')
counts = {k: 0 for k in patterns}
for path in sorted(FILES):
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding='utf-8')
    for i, line in enumerate(text.splitlines(), 1):
        for key, pat in patterns.items():
            if pat.search(line):
                counts[key] += 1
                print(f'{key}\t{rel}:{i}\t{line.strip()}')
print('AUDIT_COUNTS')
for key in sorted(counts):
    print(f'{key}\t{counts[key]}')
print('AUDIT_END')
