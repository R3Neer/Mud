from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
p=root/'notas/decisiones/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas.md'
t=p.read_text(encoding='utf-8')
repls={
'  - "reflexión, metadatos, participantes, resolución, tipado, AST resuelto, diagnósticos y tooling"':'  - "reflexión, metadatos, participantes, resolución nominal, tipado, IR semántico, diagnósticos y tooling"',
'Solo los accesos válidos llegan al AST resuelto con tipo de resultado.':'Solo los accesos válidos se elaboran en el IR semántico con tipo de resultado.',
'5. El AST resuelto solo contiene `MetadataAccessExpr` para propiedades compatibles con la categoría estática resuelta.':'5. El IR semántico solo contiene `MetadataAccessExpr` para propiedades compatibles con la categoría estática resuelta.'
}
for old,new in repls.items():
    if t.count(old)!=1: raise SystemExit(f'expected 1 occurrence: {old!r}, found {t.count(old)}')
    t=t.replace(old,new,1)
marker='- Precisa: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].\n'
if 'D-093' not in t:
    if t.count(marker)!=1: raise SystemExit('D092 relation marker mismatch')
    t=t.replace(marker, marker+'- Ajustada a la frontera de fases de [[ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].\n',1)
p.write_text(t.rstrip('\n')+'\n',encoding='utf-8',newline='\n')
print('D092_ARCH_FIX_OK')
