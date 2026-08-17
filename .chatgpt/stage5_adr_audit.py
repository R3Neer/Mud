from pathlib import Path
import os,re,sys,yaml
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
except Exception:
    pass
ROOT=Path(os.environ['MUD_TARGET']).resolve()
patterns={
 'anonymous-participant': re.compile(r'particip.{0,50}(an[oó]nim|sin\s+nombre)|an[oó]nim.{0,50}particip',re.I),
 'anchor-interpolation': re.compile(r'anchor\{',re.I),
 'flat-start-with': re.compile(r'start with\s*\{',re.I),
 'runtime-metadata-write': re.compile(r'~name.{0,80}(mutable|escrib|modific)|(?:asign|escrib|modific).{0,80}~name',re.I),
 'old-unit-properties': re.compile(r'(?m)^\s*(?:name|plural|abbreviation|prefixes|format)\s*=\s*'),
 'public-branch-anchor': re.compile(r'(?:rama.{0,90}ancla\s+p[uú]blica|ancla\s+p[uú]blica.{0,90}rama)',re.I),
 'resolved-ast': re.compile(r'mud-resolved-ast|AST resuelto',re.I),
 'family-data-no-identity': re.compile(r'datos? asociados?.{0,120}(?:no (?:posee|tiene) (?:identidad|ancla)|sin (?:identidad|ancla))',re.I),
}
print('=== VIGENTE ADR SEMANTIC SUSPECTS ===')
for p in sorted((ROOT/'notas/decisiones').glob('ADR-*.md')):
    txt=p.read_text(encoding='utf-8')
    if not txt.startswith('---\n'): continue
    end=txt.find('\n---\n',4); fm=yaml.safe_load(txt[4:end]) or {}
    if fm.get('status')!='vigente': continue
    for name,pat in patterns.items():
        for m in pat.finditer(txt):
            line=txt.count('\n',0,m.start())+1
            before=max(0,m.start()-90); after=min(len(txt),m.end()+140)
            snippet=' '.join(txt[before:after].split())
            print(f'{p.relative_to(ROOT)}:{line}: {name}: {snippet}')
print('ADR_AUDIT_COMPLETE')
