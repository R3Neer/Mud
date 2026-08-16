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
# D-087 relation graph: make later modifications reciprocal and explicit.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md'
replace_once(
    path,
    '- Modifica: [[ADR-036-participantes-receptores-y-llamadas|D-036]], [[ADR-037-campos-y-dominios-declarativos|D-037]], [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]] y [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].\n',
    '- Modifica: [[ADR-036-participantes-receptores-y-llamadas|D-036]], [[ADR-037-campos-y-dominios-declarativos|D-037]], [[ADR-038-familias-cerradas-de-valores|D-038]], [[ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]], [[ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas|D-072]], [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]] y [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].\n',
)

# ---------------------------------------------------------------------
# D-036: D-087 removed anonymous participants. Keep examples and tests current.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md'
text = read(path)
start = text.index('El nombre de un participante `on`, o de un participante `for` cuya cardinalidad efectiva sea exactamente `[1]`, puede omitirse.')
end = text.index('También son roles válidos los valores sin identidad runtime:', start)
replacement = '''Todo participante `for`, `on` y `given` declara un identificador fuente explícito, con independencia de su cardinalidad. D-087 retira la antigua proyección implícita de miembros desde participantes anónimos: el cuerpo accede a cada participante mediante su identificador y los accesos no cualificados siguen las reglas ordinarias de resolución.

Un rol `for` colectivo conserva igualmente su nombre y se usa explícitamente en cuantificaciones, agregaciones o iteraciones:

```mud
rule AllAdults for people: Person in EligibleCitizens [1..*, unique] {
    forall person in people: person.age >= 18
}
```

El identificador nombra el slot de la firma y participa en su ancla subordinada; la posición textual no constituye identidad persistente.

'''
text = text[:start] + replacement + text[end:]
write(path, text)
replace_once(path, 'En cambio, un participante individual `on World` o `for World` selecciona `thing` concretas activas cuyo tipo satisface `is World`.', 'En cambio, un participante individual `on world: World` o `for world: World` selecciona `thing` concretas activas cuyo tipo satisface `is World`.')
replace_once(path, '- La omisión del nombre de participante individual es azúcar sometido a resolución estática no ambigua, no una firma distinta.\n', '- Todo participante posee identificador fuente explícito; no existe proyección implícita de miembros desde un participante anónimo.\n')
replace_once(path, '- D-025 y esta decisión resuelven Q-011 para participantes nombrados.\n', '- D-025 y esta decisión resuelven Q-011 para participantes.\n')
replace_once(path, '1. Participante individual anónimo y nombrado.\n2. Varios participantes individuales anónimos con accesos unívocos y rechazo de un acceso ambiguo.\n', '1. Participantes individuales `for`, `on` y `given` con identificador explícito.\n2. Rechazo de participantes anónimos, también con cardinalidad efectiva `[1]`.\n')
replace_once(path, '13. Nombre obligatorio para cardinalidad distinta de `[1]` y para mutabilidad exterior.\n', '13. Identificador obligatorio para todo participante, con independencia de cardinalidad o mutabilidad exterior.\n')

# ---------------------------------------------------------------------
# D-063: the later participant rule removes anonymous receiver slots.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md'
replace_once(
    path,
    '- Amplía: [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]]\n',
    '- Amplía: [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]]\n- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]\n',
)
old = '''Los roles `for` conservan sus reglas de nombre:

- Un rol de cardinalidad exactamente `[1]` puede ser anónimo cuando la resolución del cuerpo es unívoca.
- Un rol colectivo o exteriormente mutable debe tener nombre.
- Un rol anónimo solo admite vinculación posicional.

'''
new = '''Todo rol `for` posee identificador fuente explícito conforme a D-087, también cuando su cardinalidad efectiva es `[1]`. La llamada puede vincular ese slot por posición o por nombre; la vinculación posicional no convierte el rol declarado en anónimo ni permite omitir posiciones requeridas.

'''
replace_once(path, old, new)

# ---------------------------------------------------------------------
# D-072/D-078: participants are anchored; iterators and ordinary locals are not.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas.md'
replace_once(
    path,
    '- Ampliada por: [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]]\n',
    '- Ampliada por: [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]]\n- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]\n',
)
replace_once(
    path,
    'Roles, `given`, variables de iteración y vinculaciones locales son símbolos léxicos sin ancla. Pueden repetir nombre en declaraciones o bloques independientes, pero no dentro de un mismo ámbito ni mediante sombreado de un nombre visible.\n',
    'Los participantes `for`, `on` y `given` son símbolos léxicos con ancla pública subordinada al propietario, la clase de cláusula y su identificador conforme a D-087. Variables de iteración y vinculaciones locales ordinarias continúan siendo símbolos léxicos sin ancla pública. Los nombres pueden repetirse en declaraciones o bloques independientes, pero no dentro de un mismo ámbito ni mediante sombreado de un nombre visible.\n',
)
text = read(path)
start = text.index('### Referencias diagnósticas')
end = text.index('### Migración de anclas', start)
replacement = '''### Referencias diagnósticas

Un participante se identifica mediante su ancla subordinada canónica. Un símbolo léxico que realmente carece de ancla, como un iterador o una vinculación local ordinaria, puede describirse combinando el ancla de su propietario con una etiqueta humana:

```text
action::game.Heal - local remaining
```

La escritura descriptiva del local es información diagnóstica, no una ancla nueva. Cuando existe fuente disponible, el span continúa siendo la localización principal.

'''
text = text[:start] + replacement + text[end:]
write(path, text)
replace_once(path, '3. Ausencia de ancla para roles, `given`, iteradores y locales.\n', '3. Ancla subordinada para participantes `for`/`on`/`given` y ausencia de ancla pública para iteradores y locales ordinarios.\n')
replace_once(path, '6. Diagnóstico descriptivo de un símbolo local sin fabricar una ancla.\n', '6. Diagnóstico descriptivo de un iterador o local ordinario sin fabricar una ancla.\n')

path = 'notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial.md'
replace_once(
    path,
    '- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]\n',
    '- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]\n- Ampliada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]]\n',
)
replace_once(
    path,
    'Poseen ancla las declaraciones globales, campos en su propietario original, componentes, miembros de family, unidades declaradas y tipos incorporados. Un campo heredado conserva el ancla declarativa del antecesor aunque su estado sea independiente en cada `thing`. Roles, `given`, iteradores, vinculaciones locales y valores globales no nominales solo reciben identidad interna efímera.\n',
    'Poseen ancla las declaraciones globales, campos en su propietario original, componentes, miembros de `family`, datos almacenados/calculados declarados por una `family`, unidades declaradas, participantes `for`/`on`/`given` y tipos incorporados. Un campo heredado conserva el ancla declarativa del antecesor aunque su estado sea independiente en cada `thing`. Iteradores, vinculaciones locales ordinarias y valores globales no nominales solo reciben identidad interna efímera.\n',
)
replace_once(path, '5. Anclas de campos heredados, members, unidades y builtins.\n6. Símbolos locales sin ancla pública.\n', '5. Anclas de campos heredados, miembros, datos declarados de `family`, unidades, participantes y builtins.\n6. Iteradores y vinculaciones locales ordinarias sin ancla pública.\n')

# ---------------------------------------------------------------------
# D-038: family member presentation moved from a pseudo-field to metadata.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-038-familias-cerradas-de-valores.md'
replace_once(
    path,
    '- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]]\n',
    '- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]], [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]]\n',
)
replace_once(
    path,
    'Cada miembro posee un `name: Text` intrínseco cuyo predeterminado es su nombre nominal declarado. Puede sobrescribirse mediante `name = "..."` sin cambiar identidad, igualdad, ancla ni orden. Una sobrescritura idéntica recibe sugerencia de eliminación. En una plantilla `Text`, interpolar un miembro produce su `name` efectivo.\n',
    'Cada miembro posee `~identifier: Name` como identificador fuente y el metadato configurable `~name: Name` como presentación humana. `~name` toma por defecto una presentación derivada de `~identifier`; configurarlo mediante `~name = "..."` no cambia identidad, igualdad, ancla ni orden. Una configuración idéntica al predeterminado puede recibir sugerencia de eliminación. En una plantilla `Text`, interpolar un miembro usa su `~name` efectivo.\n',
)
replace_once(path, '14. Renderización nominal de un miembro y acceso explícito a un dato `Text` alternativo.\n', '14. Presentación de un miembro mediante `~name` sin alterar `~identifier`, identidad, ancla ni igualdad.\n')

# ---------------------------------------------------------------------
# D-085: later decisions removed metadata assignment targets and branch anchors.
# ---------------------------------------------------------------------
path = 'notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md'
replace_once(path, 'Cada metadato conserva su tipo, mutabilidad y restricciones propias. El prefijo `~` no implica mutabilidad.\n', 'Cada metadato conserva su tipo, modo de evaluación y restricciones propias. El prefijo `~` no implica mutabilidad y D-087 prohíbe usar cualquier acceso `~` como destino runtime.\n')
replace_once(path, '- `MetadataAccessExpr` y objetivos asignables de metadato;\n', '- `MetadataAccessExpr` separado de los objetivos asignables ordinarios;\n')
replace_once(path, '- ancla estable de cada rama;\n', '- `decision_branch_key` local de cada rama junto con el ancla del diccionario propietario para dependencias;\n')

# ---------------------------------------------------------------------
# High-level specification index and semantic conformance case.
# ---------------------------------------------------------------------
path = 'especificacion/README.md'
replace_once(path, '- Formación y unicidad de anclas, incluidas anclas estables de ramas decisionales.\n', '- Formación y unicidad de anclas, y claves locales de ramas decisionales sin ancla pública propia.\n')
replace_once(path, '- El grafo registra anclas de rama, lecturas de metadatos, operaciones funcionales, dependencias combinadas y evidencia de terminación.\n', '- El grafo registra claves locales de rama junto con el ancla del diccionario propietario, lecturas de metadatos, operaciones funcionales, dependencias combinadas y evidencia de terminación.\n')

path = 'especificacion/sintaxis/casos/cst-ast.yaml'
replace_once(
    path,
    '  - update-branch-by-stable-anchor\n  - remove-branch-by-stable-anchor\n  - move-branch-preserves-anchor-and-changes-first-match-order\n',
    '  - update-branch-within-owner-by-local-key\n  - remove-branch-within-owner-by-local-key\n  - move-branch-changes-first-match-order-without-anchor-migration\n  - no-public-branch-anchor\n',
)

print('PHASE5_RESIDUE_CLEANUP_OK')
