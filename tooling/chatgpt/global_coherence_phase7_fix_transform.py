from pathlib import Path

p = Path('tooling/chatgpt/global_coherence_phase7_adr_sweep.py')
text = p.read_text(encoding='utf-8')
old = '''old='''start-with-declaration
    ::= \"start\" \"with\" \"{\"
        [ declaration-reference
          { \",\" declaration-reference }
        ]
        \"}\"
'''
new='''start-with-declaration
    ::= \"start\" \"with\" \"{\"
        \"things\" \"{\" contribution-list \"}\"
        \"rules\" \"{\" contribution-list \"}\"
        \"}\"
'''
if old not in t: raise SystemExit('D054 start ebnf')
t=t.replace(old,new,1)
'''
new = '''ebnf_start=t.find('start-with-declaration\\n    ::= \"start\" \"with\" \"{\"')
if ebnf_start < 0: raise SystemExit('D054 start ebnf start')
ebnf_end=t.find('\\n```', ebnf_start)
if ebnf_end < 0: raise SystemExit('D054 start ebnf end')
new='''start-with-declaration
    ::= \"start\" \"with\" \"{\"
        \"things\" \"{\" contribution-list \"}\"
        \"rules\" \"{\" contribution-list \"}\"
        \"}\"'''
t=t[:ebnf_start]+new+t[ebnf_end:]
'''
if old not in text:
    raise SystemExit('phase7 transform D054 matcher block not found')
p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')
print('PHASE7_TRANSFORM_MATCHER_FIXED')
