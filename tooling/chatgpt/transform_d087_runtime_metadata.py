from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()


def read(rel):
    return (root / rel).read_text(encoding="utf-8")


def write(rel, text):
    (root / rel).write_text(text.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def exact(text, old, new, label, count=1):
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"{label}: expected {count}, found {actual}")
    return text.replace(old, new, count)


rel = "especificacion/README.md"
t = read(rel)
t = exact(
    t,
    "- Metadatos postfix separados de los campos ordinarios y reglas de escritura de `~name`.",
    "- Metadatos postfix separados de los campos ordinarios; todo acceso `~` es de solo lectura durante la ejecución y los metadatos configurables se modifican mediante edición del modelo.",
    "README chapter 14 metadata",
)
write(rel, t)

rel = "especificacion/04-modelo-matematico.md"
t = read(rel)
t = exact(t, "  - D-086\n---", "  - D-086\n  - D-087\n---", "04 frontmatter D087")
t = exact(
    t,
    "29. El valor inicial de `~name` deriva del nombre nominal no cualificado cuando la categoría lo define; puede escribirse o modificarse únicamente donde su contrato de metadatos lo permita y no se hereda como identidad.",
    "29. El valor predeterminado de `~name` deriva del identificador nominal no cualificado cuando la categoría lo define. Puede configurarse mediante la declaración o edición del modelo, pero ningún acceso `~` puede ser destino de una asignación o actualización runtime; los metadatos no se heredan.",
    "04 stale name mutability",
)
t = exact(
    t,
    "30. La identidad, el tipo nominal efectivo, el path y el ancla no dependen de `~name`; varias entidades pueden compartir la misma presentación. `~path`, `~anchor` y `~file` son inmutables desde MUD.",
    "30. La identidad, el tipo nominal efectivo, el path y el ancla no dependen de `~name`; varias entidades pueden compartir la misma presentación. Todo acceso `~` es de solo lectura durante la ejecución; `~path`, `~anchor` y `~file` son además propiedades intrínsecas y no metadatos configurables.",
    "04 runtime readonly rule",
)
t = exact(
    t,
    "[[notas/decisiones/ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]], [[notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]] y [[notas/decisiones/ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]].",
    "[[notas/decisiones/ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]], [[notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]], [[notas/decisiones/ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]] y [[notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]].",
    "04 provenance D087",
)
write(rel, t)

rel = "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md"
t = read(rel)
old = '''`~name` es mutable para `thing`, declaraciones alias y miembros de `family`. Una escritura runtime usa el objetivo postfix:

```mud
Nora~name = "Nora la Roja"
```

La escritura exige la capacidad correspondiente y participa en la atomicidad y conflictos como una escritura de estado del propietario. En aliases y miembros de familia se almacena separada del payload inmutable; cambiarla no cambia igualdad estructural ni datos asociados.

La interpolación ordinaria de esos valores usa su `~name` efectivo.

#### Identidad y procedencia

`~anchor`, `~path` y `~file` son inmutables y no asignables. `~anchor` produce el ancla pública canónica; `~path`, el path MUD; `~file`, la procedencia física.'''
new = '''D-087 sustituye la mutabilidad runtime que esta decisión había introducido para `~name`. `~name` es un metadato configurable del modelo, pero todo acceso postfix `~` es de solo lectura durante la ejecución. Ninguna propiedad `~` puede aparecer como destino de una asignación o actualización runtime; los cambios configurables se realizan mediante edición del modelo y nueva elaboración. En aliases y miembros de `family`, los metadatos continúan separados del payload inmutable y no alteran igualdad estructural ni datos asociados.

La interpolación ordinaria de esos valores usa su `~name` efectivo.

#### Identidad y procedencia

Todo acceso `~` es runtime-readonly. `~anchor`, `~path` y `~file` son además propiedades intrínsecas, no configurables ni declarables: `~anchor` produce el ancla pública canónica; `~path`, el path MUD; `~file`, la procedencia física.'''
t = exact(t, old, new, "D085 runtime name write block")
t = exact(
    t,
    "13. Lectura, escritura y tipos de metadatos; inmutabilidad de identidad y aviso de `~file`.",
    "13. Lectura y tipos de metadatos; solo lectura runtime de todo acceso `~`, separación de identidad y aviso de `~file`.",
    "D085 verification metadata",
)
write(rel, t)

print("D087_RUNTIME_METADATA_FIX_APPLIED")
