from pathlib import Path

p = Path('notas/decisiones/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas.md')
text = p.read_text(encoding='utf-8')
old = '''Por tanto:\n\n```mud\nthing A\n\n# error estático: Thing no soporta ~for\ncheck := A~for\n```\n\ny, conceptualmente:\n\n```mud\naction Ping {\n    then create A\n}\n\n# válido: Action soporta ~for; Ping omitió la cláusula\nparticipants := Ping~for  # empty\n```\n'''
new = '''Por tanto, este programa alcanza el AST superficial pero contiene un error estático en el acceso reflectivo:\n\n```mud\nthing A\n\nrule InvalidForReflection {\n    A~for == empty\n}\n```\n\nEn cambio, una categoría compatible puede omitir la cláusula y producir `empty`:\n\n```mud\nthing A\n\naction Ping {\n    then create A\n}\n\nrule PingHasNoForParticipants {\n    Ping~for == empty\n}\n```\n'''
if text.count(old) != 1:
    raise SystemExit('D-092: expected old examples exactly once')
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8', newline='\n')
print('GLOBAL_COHERENCE_PHASE5C_EXAMPLES_OK')
