from pathlib import Path

p = Path('tooling/chatgpt/x.py')
text = p.read_text(encoding='utf-8')
start = text.find("old='''start-with-declaration")
if start < 0:
    raise SystemExit('D054 old matcher start not found')
needle = "t=t.replace(old,new,1)\n"
end = text.find(needle, start)
if end < 0:
    raise SystemExit('D054 old matcher end not found')
end += len(needle)
replacement = (
    "ebnf_start=t.find('start-with-declaration\\n    ::= \\\"start\\\" \\\"with\\\" \\\"{\\\"')\n"
    "if ebnf_start < 0: raise SystemExit('D054 start ebnf start')\n"
    "ebnf_end=t.find('\\n```', ebnf_start)\n"
    "if ebnf_end < 0: raise SystemExit('D054 start ebnf end')\n"
    "new='start-with-declaration\\n    ::= \\\"start\\\" \\\"with\\\" \\\"{\\\"\\n        \\\"things\\\" \\\"{\\\" contribution-list \\\"}\\\"\\n        \\\"rules\\\" \\\"{\\\" contribution-list \\\"}\\\"\\n        \\\"}\\\"'\n"
    "t=t[:ebnf_start]+new+t[ebnf_end:]\n"
)
p.write_text(text[:start] + replacement + text[end:], encoding='utf-8', newline='\n')
print('PHASE7_TRANSFORM_MATCHER_FIXED')
