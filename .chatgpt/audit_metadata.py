from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
def r(p): return (root/p).read_text(encoding='utf-8')
def need(p,s):
    if s not in r(p): raise SystemExit(f'MISSING {s!r} in {p}')
def forbid(p,s):
    if s in r(p): raise SystemExit(f'STALE {s!r} in {p}')
need('notas/decisiones/ADR-094-anclas-terminales-de-metadatos-configurados.md','<ancla-del-propietario>~<identificador-metadata>')
need('notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md','no puede poseer metadata propia y no expone `~metadata`')
need('especificacion/09-nombres-y-anclas.md','thing::game.Person::health~description')
need('especificacion/ir/mud-semantic-ir.asdl','semantic_metadata = SemanticMetadata(anchor identity,')
need('especificacion/ir/mud-semantic-ir.asdl','metadata_property = IntrinsicProperty(string name)')
need('especificacion/ir/mud-semantic-ir.asdl','ConfiguredProperty(metadata_kind kind)')
forbid('especificacion/ir/mud-semantic-ir.asdl','metadata_kind = IntrinsicMetadata')
need('notas/decisiones/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas.md','`Metadata` admite su contrato intrínseco incluido `~anchor`, pero no admite `~metadata`')
need('especificacion/sintaxis/casos/cst-ast.yaml','metadata-anchor=thing::Nora~summary')
print('METADATA_ANCHOR_AUDIT_OK')
