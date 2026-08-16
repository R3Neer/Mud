from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding='utf-8', newline='\n')


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one match, got {count}: {old!r}')
    write(path, text.replace(old, new, 1))


# ---------------------------------------------------------------------
# D-015: presentation is metadata, not an intrinsic ordinary `name`.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente.md'
replace_once(
    path,
    '- Modificada por: [[notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco|D-068]]\n',
    '- Modificada por: [[notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco|D-068]]\n- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]\n',
)
replace_once(
    path,
    'La propiedad intrínseca `name` tampoco se hereda. Pertenece al descriptor local de cada identidad y, si no se sobrescribe, se deriva de su propio nombre nominal.\n',
    '`~identifier` pertenece al descriptor local de cada identidad y refleja su propio identificador fuente. La presentación configurable `~name` tampoco se hereda desde una antecesora: una descendiente sin configuración explícita deriva su propio valor predeterminado de `~identifier`.\n',
)

# ---------------------------------------------------------------------
# D-028: D-076/D-087 moved all unit presentation/configuration to metadata.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades.md'
replace_once(
    path,
    '- Ampliada por: [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]]\n',
    '- Ampliada por: [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]]\n- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]\n',
)
replace_once(
    path,
    '''magnitude Length {
    root unit meter {
        name = "meter"
        plural = "meters"
        abbreviation = "m"
    }
}
''',
    '''magnitude Length {
    root unit meter {
        ~name = "meter"
        ~plural = "meters"
        ~abbreviation = "m"
    }
}
''',
)
replace_once(
    path,
    'El identificador determina el nombre intrínseco y el ancla. `name`, `plural`, `abbreviation` y `prefixes` son opcionales.\n',
    'El identificador determina `~identifier` y participa en el ancla de la unidad. `~name`, `~plural`, `~abbreviation` y `~prefixes` son metadatos estándar opcionales conforme a D-076/D-087; omitirlos no altera la identidad nominal.\n',
)
replace_once(
    path,
    '''unit minute := 60 seconds {
    name = "minute"
    plural = "minutes"
    abbreviation = "min"
}
''',
    '''unit minute := 60 seconds {
    ~name = "minute"
    ~plural = "minutes"
    ~abbreviation = "min"
}
''',
)
replace_once(
    path,
    'La ausencia de la propiedad `prefixes` no habilita prefijos. `prefixes = empty` es equivalente, `prefixes = all` habilita el catálogo decimal SI completo y `prefixes = [p1, p2, ...]` habilita solo el subconjunto enumerado. La forma desnuda `prefixes` no es válida.\n',
    'La ausencia del metadato `~prefixes` no habilita prefijos. `~prefixes = empty` es equivalente, `~prefixes = all` habilita el catálogo decimal SI completo y `~prefixes = [p1, p2, ...]` habilita solo el subconjunto enumerado. La forma desnuda `~prefixes` no es válida.\n',
)
replace_once(
    path,
    '''    unit fastie := 1 m/s {
        name = "fastie"
        plural = "fasties"
        abbreviation = "fst"
    }
''',
    '''    unit fastie := 1 m/s {
        ~name = "fastie"
        ~plural = "fasties"
        ~abbreviation = "fst"
    }
''',
)
replace_once(
    path,
    '- El lexer y el resolvedor deberán distinguir identificadores, nombres, plurales, abreviaturas y prefijos bajo el contexto de magnitud.\n',
    '- La clasificación contextual y la resolución distinguen el identificador de unidad de sus metadatos de presentación, abreviación y prefijos bajo el contexto de magnitud.\n',
)
replace_once(
    path,
    '7. Ningún prefijo por omisión o `empty`, catálogo completo mediante `all` y subconjunto mediante una colección explícita.\n',
    '7. Ningún prefijo por omisión o `~prefixes = empty`, catálogo completo mediante `~prefixes = all` y subconjunto mediante una colección explícita.\n',
)

# ---------------------------------------------------------------------
# D-035: D-085 removed special anchor interpolation.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas.md'
replace_once(
    path,
    'D-061 añade `anchor{...}` como forma contextual exclusiva de una plantilla `Text`. Produce la escritura canónica del ancla de una declaración o de un valor con identidad nominal anclada, sin convertir las declaraciones en valores ordinarios ni reservar `anchor` fuera de ese contexto.\n',
    'D-085 retira la forma contextual `anchor{...}`. El ancla es una propiedad reflectiva tipada `~anchor`; dentro de una plantilla `Text` se interpola como cualquier otra expresión, por ejemplo `"{value~anchor}"`, y también puede usarse fuera de plantillas.\n',
)

# ---------------------------------------------------------------------
# D-061: current template/rendering semantics after D-085/D-087.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text.md'
replace_once(
    path,
    '- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]\n',
    '- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]] y [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]\n',
)
old = '''Los literales ordinarios y multilínea de `Text` son plantillas. Dentro de ellos:

- `{e}` evalúa la expresión MUD `e` e inserta la representación textual de su valor;
- `anchor{d}` inserta el ancla canónica de la entidad designada por `d`;
- `\\{` y `\\}` insertan llaves literales;
- una llave sin escapar que no forme un hueco válido es un error;
- `\\u{...}` continúa siendo un escape Unicode indivisible y no abre un hueco.

`anchor` es contextual únicamente dentro de una plantilla y no se convierte en palabra reservada general. Fuera de ella puede seguir siendo un identificador ordinario.
'''
new = '''Los literales ordinarios y multilínea de `Text` son plantillas. Dentro de ellos:

- `{e}` evalúa la expresión MUD `e` e inserta la representación textual de su valor;
- un ancla se interpola mediante la expresión ordinaria `{e~anchor}` cuando la categoría estática de `e` expone esa propiedad;
- `\\{` y `\\}` insertan llaves literales;
- una llave sin escapar que no forme un hueco válido es un error;
- `\\u{...}` continúa siendo un escape Unicode indivisible y no abre un hueco.

No existe un hueco especial `anchor{...}` ni un token contextual `anchor` dentro de plantillas. `~anchor` es una propiedad tipada ordinaria del sistema reflectivo y también puede usarse fuera de `Text`.
'''
replace_once(path, old, new)
replace_once(path, '| `thing` | El valor de su propiedad intrínseca `name` |\n', '| `thing` | Su presentación `~name` efectiva |\n')
replace_once(path, '| Miembro de `family` | El nombre nominal del miembro |\n', '| Miembro de `family` | Su presentación `~name` efectiva |\n')
replace_once(path, '| Magnitud de punto | Su `format`, si existe; en otro caso, la representación ordinaria de su coordenada como magnitud |\n', '| Magnitud de punto | Su `~format`, si está configurado; en otro caso, la representación ordinaria de su coordenada como magnitud |\n')
replace_once(
    path,
    'La representación de una magnitud escribe la abreviatura de la unidad cuando exista. En otro caso usa su nombre singular para `1` y `-1`, y el plural declarado para los demás valores; si no hay plural, reutiliza el nombre. Las unidades derivadas usan la proyección canónica de sus factores con unidad. Los factores nominales sin unidad permanecen en el tipo, pero no producen texto; si la proyección completa es vacía se escribe solo el número. Una magnitud de punto sin `format` no introduce una excepción: representa su coordenada mediante estas mismas reglas.\n',
    'La representación de una magnitud escribe `~abbreviation` de la unidad cuando esté configurado. En otro caso usa `~name` para `1` y `-1`, y `~plural` para los demás valores; si no hay plural configurado, reutiliza `~name`. Las unidades derivadas usan la proyección canónica de sus factores con unidad. Los factores nominales sin unidad permanecen en el tipo, pero no producen texto; si la proyección completa es vacía se escribe solo el número. Una magnitud de punto sin `~format` no introduce una excepción: representa su coordenada mediante estas mismas reglas.\n',
)
replace_once(path, 'En una magnitud de punto, `in` transforma la coordenada completa y omite su `format`: las 13:30 expresadas `in hour` producen `13.5 h`, no el componente `13`.\n', 'En una magnitud de punto, `in` transforma la coordenada completa y omite su `~format`: las 13:30 expresadas `in hour` producen `13.5 h`, no el componente `13`.\n')
replace_once(path, 'El receptor debe ser una magnitud de punto. Ambas unidades deben pertenecer a su magnitud subyacente y la unidad extraída no puede ser mayor que la contenedora. El resultado es `Nat`, se calcula respecto del origen canónico mediante resto euclídeo y no depende de las unidades escritas en `format`. Por tanto, pueden extraerse picosegundos de un tiempo cuyo formato solo muestre horas, minutos y segundos.\n', 'El receptor debe ser una magnitud de punto. Ambas unidades deben pertenecer a su magnitud subyacente y la unidad extraída no puede ser mayor que la contenedora. El resultado es `Nat`, se calcula respecto del origen canónico mediante resto euclídeo y no depende de las unidades escritas en `~format`. Por tanto, pueden extraerse picosegundos de un tiempo cuyo formato solo muestre horas, minutos y segundos.\n')
replace_once(path, 'Dentro del `format` de una magnitud de punto, el propio punto es contextual. La sucesión habitual conserva la forma compacta:\n', 'Dentro del `~format` de una magnitud de punto, el propio punto es contextual. La sucesión habitual conserva la forma compacta:\n')
replace_once(path, 'format = "{hour:2}:{minute:2}:{second:2}"\n', '~format = "{hour:2}:{minute:2}:{second:2}"\n')
replace_once(path, 'format = "{week from year:2}"\n', '~format = "{week from year:2}"\n')
replace_once(path, 'La forma incompleta `week from year` solo es válida en un hueco del `format` de una magnitud de punto; fuera de él exige el receptor `in punto`.\n', 'La forma incompleta `week from year` solo es válida en un hueco de `~format` de una magnitud de punto; fuera de él exige el receptor `in punto`.\n')
replace_once(path, 'La propiedad `format` de una magnitud `point over` usa esta misma sintaxis, no un segundo lenguaje de llaves. Sus nombres como `hour`, `minute` o `second` se resuelven en el punto contextual; `{hour:2}` solicita dos posiciones a la izquierda.\n', 'El metadato `~format` de una magnitud `point over` usa esta misma sintaxis, no un segundo lenguaje de llaves. Sus nombres como `hour`, `minute` o `second` se resuelven en el punto contextual; `{hour:2}` solicita dos posiciones a la izquierda.\n')
replace_once(path, 'Omitirla es legal, pero produce un aviso cuando existe una unidad seleccionable porque hace depender una frontera pública de su proyección canónica. El arreglo sugerido añade explícitamente esa unidad. Una magnitud sin unidades publica su número y no produce el aviso. En una magnitud de punto, un campo directo sin `in` publica la coordenada numérica, no el `format`; para publicar la representación formateada se declara un campo `Text`, por ejemplo `timeText := "{clock.time}"`.\n', 'Omitirla es legal, pero produce un aviso cuando existe una unidad seleccionable porque hace depender una frontera pública de su proyección canónica. El arreglo sugerido añade explícitamente esa unidad. Una magnitud sin unidades publica su número y no produce el aviso. En una magnitud de punto, un campo directo sin `in` publica la coordenada numérica, no el `~format`; para publicar la representación formateada se declara un campo `Text`, por ejemplo `timeText := "{clock.time}"`.\n')

text = read(path)
start = text.index('### Interpolación de anclas')
end = text.index('## Consecuencias', start)
anchor_section = '''### Interpolación de anclas

D-085 elimina la forma especial `anchor{...}`. Las anclas se obtienen mediante la propiedad reflectiva tipada `~anchor` y una plantilla no introduce ningún mecanismo adicional:

```mud
"Rule: {CanRecruit~anchor}"
"Kingdom: {kingdom}; identity: {kingdom~anchor}"
```

El mismo acceso puede aparecer fuera de `Text`. Una categoría estática que no exponga `~anchor` produce el diagnóstico ordinario de propiedad reflectiva no disponible; no existe un error ni un nodo AST específico de «hueco de ancla».

'''
text = text[:start] + anchor_section + text[end:]
write(path, text)
replace_once(path, '- El AST distingue fragmentos literales, huecos de valor, especificaciones numéricas y huecos de ancla.\n', '- El AST distingue fragmentos literales, huecos de valor y especificaciones numéricas; las anclas usan la misma interpolación de expresiones que cualquier otro valor renderizable.\n')
replace_once(path, '- El nombre visible de una `thing` puede diferir de su ancla; `anchor{...}` conserva la identidad canónica.\n', '- La presentación `~name` de una `thing` puede diferir de su identidad; `~identifier` y `~anchor` permiten consultar explícitamente esa identidad reflectiva.\n')
replace_once(path, '- `in` sirve tanto para magnitudes lineales como de punto y, en estas últimas, evita el formato.\n', '- `in` sirve tanto para magnitudes lineales como de punto y, en estas últimas, evita `~format`.\n')
replace_once(path, '- La extracción de componentes no queda limitada por el formato visible.\n', '- La extracción de componentes no queda limitada por `~format`.\n')
replace_once(path, '9. Obtención de anclas de declaraciones y valores nominales mediante `anchor{...}`.\n', '9. Obtención de anclas mediante la propiedad reflectiva `~anchor`, incluida su interpolación ordinaria en `Text`.\n')
replace_once(path, '10. Rechazo de `anchor{...}` sobre valores sin identidad anclada.\n', '10. Rechazo de `~anchor` cuando la categoría estática del receptor no expone esa propiedad.\n')
replace_once(path, '12. Extracción `picosecond from second in time` independiente del `format`.\n', '12. Extracción `picosecond from second in time` independiente de `~format`.\n')

# ---------------------------------------------------------------------
# D-068: title must describe the current intrinsic/configurable split.
# The body itself has already been rewritten by the preceding phase-5 script.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md'
replace_once(path, 'title: "`Thing` universal y nombre intrínseco"\n', 'title: "`Thing` universal, identificador y presentación reflectiva"\n')
replace_once(path, '# ADR-068 — `Thing` universal y nombre intrínseco\n', '# ADR-068 — `Thing` universal, identificador y presentación reflectiva\n')

# ---------------------------------------------------------------------
# D-070 and syntax coverage: remove stale terminology only.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado.md'
replace_once(
    path,
    'Esta decisión se ha actualizado al vocabulario y a la gramática vigentes: usa los tipos numéricos breves de [[ADR-067-nombres-breves-de-tipos-numericos|D-067]], integra el `name` intrínseco de [[ADR-068-thing-universal-y-nombre-intrinseco|D-068]] y representa los literales de comillas dobles conforme a [[ADR-069-literales-char-con-comillas-dobles|D-069]]. En particular, el AST superficial no inventa un nodo léxico distinto para `Char`; esa elaboración requiere contexto de tipos.\n',
    'Esta decisión se ha actualizado al vocabulario y a la gramática vigentes: usa los tipos numéricos breves de [[ADR-067-nombres-breves-de-tipos-numericos|D-067]], integra la separación entre `~identifier`, `~name` y campos ordinarios conforme a [[ADR-068-thing-universal-y-nombre-intrinseco|D-068]] y D-087, y representa los literales de comillas dobles conforme a [[ADR-069-literales-char-con-comillas-dobles|D-069]]. En particular, el AST superficial no inventa un nodo léxico distinto para `Char`; esa elaboración requiere contexto de tipos.\n',
)
path = 'especificacion/sintaxis/cobertura-sintactica.yaml'
replace_once(path, '      reason: alternativa integrada en ThingDecl como nombre intrínseco o campo\n', '      reason: alternativa integrada en ThingDecl como campo\n')

# ---------------------------------------------------------------------
# Keep D-087 relation graph reciprocal for direct modifications above.
# This exact line is produced by the preceding phase-5 scripts.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md'
old = '- Modifica: [[ADR-036-participantes-receptores-y-llamadas|D-036]], [[ADR-037-campos-y-dominios-declarativos|D-037]], [[ADR-038-familias-cerradas-de-valores|D-038]], [[ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]], [[ADR-068-thing-universal-y-nombre-intrinseco|D-068]], [[ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas|D-072]], [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]] y [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].\n'
new = '- Modifica: [[ADR-015-especializacion-aciclica-y-estado-independiente|D-015]], [[ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[ADR-036-participantes-receptores-y-llamadas|D-036]], [[ADR-037-campos-y-dominios-declarativos|D-037]], [[ADR-038-familias-cerradas-de-valores|D-038]], [[ADR-061-resultados-fallidos-y-plantillas-text|D-061]], [[ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]], [[ADR-068-thing-universal-y-nombre-intrinseco|D-068]], [[ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas|D-072]], [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]] y [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].\n'
replace_once(path, old, new)

print('PHASE5_DEEP_RESIDUE_CLEANUP_OK')
