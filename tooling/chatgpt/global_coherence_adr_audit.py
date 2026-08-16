from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
DIR=ROOT/'notas/decisiones'
patterns={
    'anonymous-participant': re.compile(r'an[oó]nim|puede omitirse|sin nombre', re.I),
    'legacy-anchor-interpolation': re.compile(r'anchor\{'),
    'legacy-dot-name': re.compile(r'\.name\b'),
    'legacy-name-assignment': re.compile(r'(?<!~)\bname\s*='),
    'legacy-format-assignment': re.compile(r'(?<!~)\bformat\s*='),
    'legacy-plural-assignment': re.compile(r'(?<!~)\bplural\s*='),
    'legacy-abbreviation-assignment': re.compile(r'(?<!~)\babbreviation\s*='),
    'legacy-prefixes-assignment': re.compile(r'(?<!~)\bprefixes\s*='),
    'flat-start-with': re.compile(r'start with'),
    'branch-anchor': re.compile(r'ancla.{0,40}rama|rama.{0,40}ancla', re.I),
    'runtime-metadata-write': re.compile(r'~name\s*(?:=|\+=|-=)|escrib(?:ir|ible).{0,30}~name|modific(?:ar|able).{0,30}~name', re.I),
    'family-data-no-identity': re.compile(r'datos?.{0,80}(?:no posee|sin identidad|no tiene).{0,30}identidad', re.I),
    'old-minmax-error': re.compile(r'agregaci[oó]n.{0,20}vac[ií]a|min.{0,40}max.{0,80}error', re.I),
    'resolved-typed-mix': re.compile(r'AST resuelto.{0,100}(?:tipo|dominio|cardinalidad|terminaci[oó]n)', re.I),
}

for p in sorted(DIR.glob('ADR-*.md')):
    text=p.read_text(encoding='utf-8')
    front=text.split('---',2)[1] if text.startswith('---') else ''
    if not re.search(r'^status:\s*vigente\s*$',front,re.M):
        continue
    lines=text.splitlines()
    hits=[]
    for i,line in enumerate(lines,1):
        for key,pat in patterns.items():
            if pat.search(line):
                hits.append((i,key,line.strip()))
    if hits:
        print(f'### {p.relative_to(ROOT)}')
        for i,key,line in hits:
            print(f'{i:04d} [{key}] {line}')
