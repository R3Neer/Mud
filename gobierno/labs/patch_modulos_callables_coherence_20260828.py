from pathlib import Path

ROOT = Path.cwd()


def rewrite(rel: str, old: str, new: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"{rel}: bloque esperado no encontrado: {old[:120]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_after(rel: str, marker: str, insertion: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if insertion in text:
        return
    if marker not in text:
        raise SystemExit(f"{rel}: marcador esperado no encontrado: {marker!r}")
    path.write_text(text.replace(marker, marker + insertion, 1), encoding="utf-8")


# La CST no conserva una clasificación de actions que D-096 retiró.
insert_after(
    "especificacion/sintaxis/cst-sin-perdidas.md",
    "  - D-087\n",
    "  - D-096\n",
)
rewrite(
    "especificacion/sintaxis/cst-sin-perdidas.md",
    "- Clasificación elemental o compuesta de acciones.",
    "- Clasificación semántica de invocaciones callable, capacidades exteriores o composición de consecuencias.",
)

# D-035: una cualificación completa no atraviesa por sí sola la frontera modular.
rewrite(
    "notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas.md",
    "Una referencia completamente cualificada se resuelve directamente.",
    "Una referencia completamente cualificada evita ambigüedad de nombres, pero solo se resuelve si la declaración pertenece al cierre modular visible; la cualificación no sustituye la autorización `uses` de D-096.",
)

# D-036: look participa en el contrato general de given.
rewrite(
    "notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md",
    "- `given`: valores auxiliares de reglas booleanas y actions.",
    "- `given`: valores auxiliares de reglas booleanas, actions, subactions y `look`.",
)

# D-042: distinguir raíz exterior de invocación interna.
rewrite(
    "notas/decisiones/ADR-042-acciones-raiz-y-resultados.md",
    "- puede solicitarse desde el exterior o desde otra acción;\n- inicia una resolución causal y es atómica junto con todas sus ondas.",
    "- una `action` puede solicitarse desde el exterior y, en ese caso, inicia la resolución causal raíz;\n- una `action` o `subaction` invocada desde un `then` se incorpora a la resolución causal ya activa y no abre una raíz independiente;\n- la resolución completa es atómica junto con todas sus ondas.",
)

# D-054: la verificación debe comprobar la superficie modular vigente, no la forma retirada.
rewrite(
    "notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial.md",
    "7. Un único `start with` global con secciones obligatorias `things` y `rules`.\n8. Independencia del orden dentro de cada sección.\n9. Rechazo de la forma plana, de secciones ausentes y de coma final.\n10. Rechazo de una regla en `things`, de una `thing` en `rules` y de colecciones anidadas.\n11. Programa sin `start with`, equivalente a ambas secciones vacías.\n12. Activación inicial conjunta y estabilización previa a acciones externas.\n13. `Thing` siempre efectiva y no activable.\n14. Reutilización exacta de estado tras `destroy` y nueva activación.\n15. Sustitución del conjunto global por el `start with` local de un test.\n16. Navegación LSP desde cada activación a una única definición.",
    "7. Como máximo un `start with` por módulo y ausencia válida de contribución en un módulo.\n8. Independencia del orden y deduplicación dentro del conjunto unificado de contribuciones.\n9. Admisión de contribución directa, bloque unificado y coma final opcional.\n10. Rechazo de declaraciones no activables, activación de otro módulo y colecciones anidadas.\n11. Proyecto cuyos módulos omiten `start with`, equivalente a una contribución inicial vacía.\n12. Materialización conjunta de las contribuciones de todos los módulos y estabilización previa a acciones externas.\n13. `Thing` siempre efectiva y no activable.\n14. Reutilización exacta de estado tras `destroy` y nueva activación.\n15. Unión de contribuciones `start with` del cierre transitivo estático de tests alcanzables.\n16. Navegación LSP desde cada activación a una única definición.",
)

# D-055: test no es action, pero sí puede ser una operación de test invocada desde otro test.
rewrite(
    "notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md",
    "- No es invocable como acción ni consultable como regla.",
    "- No es invocable como `action` ni consultable como regla; en contexto de pruebas puede invocarse como operación `test` desde el `then` de otro test visible conforme a D-096.",
)
rewrite(
    "notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md",
    "`then` utiliza la semántica ordinaria de un bloque de efectos y forma la transición probada. Las asignaciones y demás modificaciones escritas al comienzo de `then` no pertenecen al estado inicial: son efectos de la prueba.",
    "`then` utiliza la semántica ordinaria de consecuencias y forma la transición probada. Puede mezclar efectos, locales y llamadas permitidas, incluidas operaciones `test` visibles en contexto de pruebas. Las asignaciones y demás modificaciones escritas al comienzo de `then` no pertenecen al estado inicial: son efectos de la prueba. Invocar un test cuyo `start with` ya participó en el cierre inicial no vuelve a materializar esa contribución.",
)
rewrite(
    "notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise.md",
    "4. Sustitución completa del `start with` global.\n5. Rechazo de instrucciones y asignaciones dentro del `start with` local.\n6. Materialización y estabilización antes de `then`.",
    "4. Unión de `start with` del cierre transitivo estático de tests alcanzables, sin aplicar la activación ordinaria de los módulos.\n5. Rechazo de instrucciones y asignaciones dentro de una contribución `start with` de test.\n6. Materialización y estabilización antes del `then` raíz, llamada posterior sin reactivación y rechazo de ciclos ejecutables entre tests.",
)

# D-058: la sintaxis temporal produce matches, no un Bool/pulso agregado ni All/Any semánticos.
rewrite(
    "notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo.md",
    "### Composición\n\n`and` y `or` combinan activadores respectivamente mediante `All` y `Any`. Cuando uno de sus operandos ya es temporal, un operando `Bool` ordinario se eleva a `Rise`:\n\n```mud\nwhen position changes or ready\n```\n\nequivale a:\n\n```text\nAny(Changed(position), Rise(ready))\n```\n\ny:\n\n```mud\nwhen position changes and velocity changes\n```\n\nexige que ambas diferencias netas ocurran entre las mismas dos instantáneas de inicio.\n\nUna subexpresión booleana ordinaria entre paréntesis se eleva como una unidad. Así, `(ready or authorized) and position changes` contiene `Rise(ready or authorized)`, no dos activadores independientes.\n\nLos activadores solo se combinan inicialmente mediante las palabras `and` y `or`. `not`, `xor`, `=>`, `<=>`, `&`, `|` y `^` no aceptan operandos `Trigger`. Esta restricción no impide usar operadores booleanos ordinarios dentro de la expresión booleana de un `Rise` o `Temporal`.",
    "### Composición\n\nUn trigger produce cero o más matches causales. Las formas temporales `Rise`, `Temporal` y `Changed` describen cuándo una vinculación aporta un match; cuando un operando ordinario `Bool` participa en una composición temporal se eleva a `Rise` como antes.\n\n`and` realiza natural join de los matches compatibles de ambos operandos y, si no comparten bindings, su producto cartesiano. `or` realiza la unión de matches. Las identidades de ocurrencias causales forman parte del match, de modo que dos ocurrencias distintas no se deduplican aunque tengan el mismo payload.\n\n```mud\nwhen position changes and velocity changes\n```\n\nrequiere matches compatibles cuyas diferencias netas correspondan al mismo paso entre instantáneas. Una subexpresión booleana ordinaria entre paréntesis se eleva como una unidad: `(ready or authorized) and position changes` usa `Rise(ready or authorized)`, no dos fuentes independientes.\n\nLos triggers solo se combinan inicialmente mediante las palabras `and` y `or`. `not`, `xor`, `=>`, `<=>`, `&`, `|` y `^` no aceptan operandos `Trigger`. Esta restricción no impide usar operadores booleanos ordinarios dentro de la expresión booleana de un `Rise` o `Temporal`. D-096 añade además como fuentes declarativas ocurrencias de `message`, disparos de rules reactivas y evaluaciones de `always`.",
)
rewrite(
    "notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo.md",
    "- El AST de superficie conserva `changes` como sufijo; el IR representa explícitamente `Rise`, `Temporal`, `Changed`, `All` y `Any`.",
    "- El AST de superficie conserva `changes` como sufijo y la composición escrita; el modelo semántico debe preservar el comportamiento de cero o más matches, sus bindings/testigos y las identidades causales. D-096 no fija una codificación IR cerrada de esos matches.",
)
rewrite(
    "notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo.md",
    "2. Unión y coincidencia de activadores mediante `or` y `and`.",
    "2. Unión de matches mediante `or` y natural join/producto cartesiano compatible mediante `and`, preservando ocurrencias causalmente distintas.",
)

# D-063: los casos de conformidad reflejan ambos universos de on.
rewrite(
    "notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas.md",
    "15. Universo limitado a `thing` concretas y activas.",
    "15. Universo implícito de `thing` concretas y activas para `on` directo y fuente finita enumerable para `on ... in fuente`, incluido rechazo de un tipo sin universo implícito finito.",
)

# D-081: un dominio solo entra en take tras materialización explícita.
rewrite(
    "notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones.md",
    "3. `take` sobre colección ordenada, no ordenada, dominio, diccionario y `Text`.",
    "3. `take` sobre colección ordenada, no ordenada, `all D`, diccionario y `Text`, y rechazo de un dominio desnudo como fuente productora de colección.",
)

# D-085: eliminar restos de la activación separada y del antiguo contrato de Any/subaction.
rewrite(
    "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md",
    "- conjuntos separados de activación de `thing` y reglas;",
    "- un único `StartSet(contributions)` para activación unificada;",
)
rewrite(
    "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md",
    "2. llamada a `subaction` fuera de acción o subacción;",
    "2. uso de `subaction` como raíz exterior o fuera de un contexto semántico `then`;",
)
rewrite(
    "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md",
    "14. forma mezclada retirada de `start with`.",
    "14. uso de las secciones retiradas `things`/`rules` dentro de `start with`.",
)
rewrite(
    "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md",
    "- La activación inicial no mezcla categorías y admite selecciones estáticas composables.",
    "- La activación inicial reúne declaraciones activables `thing | rule` por módulo en un conjunto unificado, deduplicado y sin orden semántico.",
)
rewrite(
    "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md",
    "1. Accesibilidad externa e interna de `action` y `subaction`, ancla compartida y rollback completo.",
    "1. Capacidad exterior exclusiva de `action`, invocación de `action`/`subaction` desde contextos `then`, ancla compartida y rollback completo.",
)
rewrite(
    "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md",
    "10. `start with` por secciones, `empty`, colecciones de un nivel, deduplicación, `all` contextual y rechazo de colecciones anidadas.",
    "10. `start with` unificado por módulo, forma directa y de bloque, `empty`, colecciones de un nivel, deduplicación, `all D` cuando se materializa un dominio y rechazo de colecciones anidadas.",
)

# D-087: visibilidad exterior deja de ser una mera preferencia de tooling.
rewrite(
    "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md",
    "- La visibilidad exterior se vuelve una propiedad de generación/tooling y no una regla de acceso interna.",
    "- La visibilidad exterior se deriva del módulo propietario, su contrato `uses`, la categoría operacional y el cierre de tipos; el tooling presenta esa frontera, no la inventa.",
)
rewrite(
    "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md",
    "- El `start with` global y el local de tests permanecen fuera de la superficie metadata-bearing.",
    "- Las contribuciones `start with` de módulos y tests permanecen fuera de la superficie metadata-bearing.",
)

# D-088: selección sobre dominio exige all D, mientras recorridos/cuantiﬁcadores pueden consumirlo directamente.
rewrite(
    "notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md",
    "`by` de progresión se admite también en selección y en `exists`, `forall`, `count`, `sum`, `min` y `max`, siempre que la fuente ofrezca progresión mediante diferencia. No significa stride sobre una colección arbitraria. La semántica de ausencia de `min` y `max` es la de D-095: ningún candidato produce `empty` con cardinalidad `[0..1]`. Una fuente futura puede definir expresamente esa capacidad; esta decisión no introduce un protocolo general. `ordered by path` conserva una semántica distinta.",
    "`by` de progresión se admite también en selección y en `exists`, `forall`, `count`, `sum`, `min` y `max`, siempre que la fuente ofrezca progresión mediante diferencia. Si la selección parte conceptualmente de un dominio, su fuente debe escribirse materializada como `all D`; los recorridos y cuantificadores que no producen una colección pueden consumir el dominio directamente. `by` no significa stride sobre una colección arbitraria. La semántica de ausencia de `min` y `max` es la de D-095: ningún candidato produce `empty` con cardinalidad `[0..1]`. Una fuente futura puede definir expresamente esa capacidad; esta decisión no introduce un protocolo general. `ordered by path` conserva una semántica distinta.",
)

print("D-096 coherence pass 2 applied")
