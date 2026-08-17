from pathlib import Path
import os

ROOT = Path(os.environ['MUD_TARGET']).resolve()

def read(path):
    return (ROOT / path).read_text(encoding='utf-8')

def write(path, text):
    (ROOT / path).write_text(text.rstrip('\n') + '\n', encoding='utf-8', newline='\n')

def replace_once(path, old, new):
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected 1 occurrence, got {count}')
    write(path, text.replace(old, new, 1))

replace_once(
    'especificacion/README.md',
    '- Autoridad actual: los capítulos vigentes de este directorio y las decisiones vigentes enlazadas. El historial Git conserva la procedencia retirada, pero no tiene autoridad subsidiaria.',
    '- Autoridad actual: los capítulos con `status: vigente` y las decisiones vigentes enlazadas. Un archivo con `normative: true` pertenece a la superficie normativa, pero su `status` determina si el capítulo completo ya tiene autoridad consolidada. Los capítulos no vigentes pueden incorporar reglas respaldadas por decisiones vigentes, pero no las sustituyen ni cierran cuestiones abiertas. El historial Git conserva la procedencia retirada, pero no tiene autoridad subsidiaria.'
)

replace_once(
    'especificacion/README.md',
    '''Cada contenido tendrá uno de estos estados:\n\n- **Normativo**: define la conformidad de una implementación.\n- **Informativo**: explica una norma sin ampliarla.\n- **Propuesta**: texto todavía no aprobado.\n- **Abierto**: cuestión sin semántica definitiva.\n''',
    '''La superficie y el estado de publicación son ejes distintos. `normative: true` indica que el archivo está destinado a contener reglas de conformidad; no equivale por sí solo a aprobación. El ciclo `esqueleto → borrador → propuesta → en-revision → vigente` determina la autoridad del capítulo como unidad.\n\n- **Capítulo vigente**: su texto normativo es autoridad consolidada.\n- **Capítulo no vigente**: puede transcribir o explicar contratos ya fijados por decisiones vigentes y artefactos mecánicos coherentes, pero el capítulo completo sigue en preparación y no puede introducir autoridad nueva por encima de esas fuentes.\n- **Contenido informativo**: explica una norma sin ampliarla.\n- **Cuestión abierta**: carece de semántica definitiva hasta que el proceso de decisiones la cierre o la excluya explícitamente del perfil aplicable.\n\nUna contradicción entre un capítulo no vigente y una decisión vigente se considera un defecto documental; no una nueva elección semántica. Una contradicción entre prosa normativa y un artefacto mecánico normativo también es un defecto y debe corregirse, conforme a MUD-EDIT-001.\n'''
)

replace_once(
    'especificacion/00-convenciones-editoriales.md',
    '''Estados:\n\n- `esqueleto`\n- `borrador`\n- `propuesta`\n- `en-revision`\n- `vigente`\n- `sustituido`\n''',
    '''Estados:\n\n- `esqueleto`\n- `borrador`\n- `propuesta`\n- `en-revision`\n- `vigente`\n- `sustituido`\n\n`normative: true` clasifica el archivo dentro de la superficie normativa, pero no adelanta su estado de publicación. Solo `status: vigente` concede autoridad consolidada al capítulo como unidad. Antes de ese estado, el texto puede incorporar contratos ya cerrados por decisiones vigentes y artefactos mecánicos coherentes, pero no puede modificar esos contratos ni resolver por sí solo una cuestión abierta.\n\nSi un capítulo no vigente contradice una decisión vigente, la contradicción es un defecto editorial que debe corregirse antes de promover el capítulo. No se interpreta como una sustitución tácita de la decisión. La relación entre prosa y artefactos mecánicos normativos sigue regida por MUD-EDIT-001: una divergencia entre ambos es un defecto, no una regla de prioridad silenciosa.\n'''
)

replace_once(
    'gobierno/CICLO-DOCUMENTAL.md',
    '''Un capítulo `vigente` puede contener cuestiones abiertas solo si la característica afectada queda marcada fuera de MUD 1.0 o si la cuestión no altera su significado.\n''',
    '''Un capítulo `vigente` puede contener cuestiones abiertas solo si la característica afectada queda marcada fuera de MUD 1.0 o si la cuestión no altera su significado.\n\n### Autoridad durante la promoción\n\nLa ubicación en `especificacion/` y `normative: true` indican que un archivo pertenece a la superficie normativa, no que todo su contenido esté ya aprobado. La autoridad del capítulo como unidad aparece al alcanzar `status: vigente`.\n\nAntes de `vigente`, un capítulo puede recoger reglas que ya tengan autoridad por decisiones vigentes y por artefactos mecánicos normativos coherentes. Esa transcripción no concede al capítulo potestad para cambiar esas reglas, cerrar preguntas o introducir una semántica alternativa. Si diverge de una decisión vigente, existe un defecto documental que bloquea la promoción. Si prosa y artefacto mecánico divergen, se aplica la regla editorial MUD-EDIT-001: la divergencia debe resolverse explícitamente y ninguna de las dos superficies adquiere prioridad silenciosa.\n\nPor tanto, la promoción a `vigente` certifica el capítulo completo; no es el mecanismo que hace vigentes retroactivamente las decisiones que ya documentaba.\n'''
)

print('STAGE6_AUTHORITY_OK')
