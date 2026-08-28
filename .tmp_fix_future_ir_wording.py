from pathlib import Path

ROOT = Path(__file__).resolve().parent


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: esperaba 1 ocurrencia y encontré {count}: {old[:120]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    "notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal.md",
    "- El IR usa `ContextualAliasConstructionExpr` para la construcción dirigida por tipo esperado y reserva `ConversionExpr` para un `to` explícito.\n- La comparación aporta expectativas en ambas direcciones sin introducir coerciones implícitas.\n- La futura representación semántica posterior a tipado y elaboración conserva explícitamente la construcción contextual y el alias nominal incluso cuando su representación coincide con otro tipo.",
    "- La elaboración distingue la construcción contextual dirigida por el tipo esperado de una conversión nominal `to` explícita.\n- La comparación aporta expectativas en ambas direcciones sin introducir coerciones implícitas.\n- El resultado elaborado debe conservar o hacer reconstruibles la construcción contextual y el alias nominal incluso cuando su representación coincide con otro tipo; su codificación mecánica todavía no está fijada.",
)

replace_once(
    "notas/decisiones/ADR-070-cst-sin-perdidas-y-ast-superficial-normalizado.md",
    "Estas decisiones pertenecen a la resolución nominal cuando dependen solo de identidad y bindings, o al representación semántica posterior a tipado y elaboración cuando requieren tipado o elaboración.",
    "Estas decisiones pertenecen a la resolución nominal cuando dependen solo de identidad y bindings, o a las fases posteriores de tipado y elaboración cuando requieren tipos u otras conclusiones elaboradas.",
)

replace_once(
    "notas/decisiones/ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas.md",
    "La separación entre CST, AST superficial, resultados de resolución nominal e representación semántica posterior a tipado y elaboración exige fijar cómo se representan ámbitos y candidatos. También debe distinguirse qué nombres poseen identidad semántica persistente y qué nombres solo vinculan valores dentro de una declaración.",
    "La separación entre CST, AST superficial, resultados de resolución nominal y fases posteriores de tipado y elaboración exige fijar cómo se representan ámbitos y candidatos. También debe distinguirse qué nombres poseen identidad semántica persistente y qué nombres solo vinculan valores dentro de una declaración.",
)

replace_once(
    "notas/decisiones/ADR-074-uniones-nominales-y-estrechamiento.md",
    "- La futura representación semántica posterior a tipado y elaboración conserva alternativas nominales normalizadas y la alternativa elegida por cada incorporación.",
    "- La elaboración determina las alternativas nominales normalizadas y la alternativa elegida por cada incorporación; cualquier representación posterior debe conservarlas o permitir reconstruirlas.",
)

replace_once(
    "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md",
    "El AST superficial conserva que la cardinalidad fue omitida; la futura representación semántica posterior a tipado y elaboración elaborado registra la cardinalidad efectiva y su procedencia `InferredFromInitializer`, `OrdinaryScalarDefault` o `Explicit`.",
    "El AST superficial conserva que la cardinalidad fue omitida; tipado y elaboración determinan la cardinalidad efectiva y deben conservar suficiente procedencia para distinguir `InferredFromInitializer`, `OrdinaryScalarDefault` y `Explicit`. La codificación mecánica posterior todavía no está fijada.",
)
replace_once(
    "notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada.md",
    "La futura representación semántica posterior a tipado y elaboración registra para cada decisional:",
    "La elaboración debe determinar para cada diccionario decisional, y cualquier representación posterior debe conservar o permitir reconstruir:",
)

replace_once(
    "notas/decisiones/ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios.md",
    "El operador derecho se resuelve durante la elaboración. Los tipos estructurales y las identidades singleton se rechazan durante tipado/elaboración antes de producir la forma correspondiente dla futura representación semántica posterior a tipado y elaboración.\n\nLas operaciones conjuntistas pueden conservarse como `BinaryExpr` en el AST superficial porque su clase depende de los tipos resueltos. La futura representación semántica posterior a tipado y elaboración distingue:\n\n```text\nExactDictionarySetOperationExpr(operator, left, right, resultType)\nFunctionalDictionarySetOperationExpr(operator, left, right, resultType)\n```\n\nLa aplicación del segundo nodo equivale a aplicar ambos operandos en la misma instantánea y ejecutar después la operación de colección. Nunca se materializa una lista fusionada de ramas ni se intenta demostrar equivalencia lógica entre selectores.\n\nLa futura representación semántica posterior a tipado y elaboración diferencia también:\n\n```text\nTypeTestExpr                # pertenencia transitiva de is\nExactNominalTypeTestExpr    # identidad nominal exacta de iis\n```",
    "El operador derecho se resuelve durante la elaboración. Los tipos estructurales y las identidades singleton se rechazan durante tipado/elaboración antes de obtener un resultado elaborado válido.\n\nLas operaciones conjuntistas pueden conservarse como `BinaryExpr` en el AST superficial porque su clase depende de los tipos resueltos. La elaboración debe distinguir operaciones sobre diccionarios exactos de operaciones sobre diccionarios funcionales y determinar su tipo de resultado. La forma mecánica posterior de esa distinción todavía no está fijada.\n\nUna operación conjuntista sobre funcionales equivale a aplicar ambos operandos en la misma instantánea y ejecutar después la operación de colección sobre sus resultados. Nunca se materializa una lista fusionada de ramas ni se intenta demostrar equivalencia lógica entre selectores.\n\nLa elaboración debe distinguir asimismo la pertenencia nominal transitiva de `is` de la identidad nominal exacta de `iis`. El AST superficial conserva ambas formas; cualquier representación posterior debe preservar o permitir reconstruir esa distinción sin que esta decisión fije nombres concretos de nodos.",
)

replace_once(
    "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md",
    "No lo son expresiones, sentencias, operandos, condiciones, cuerpos de cláusula, tokens, nodos arbitrarios del AST ni ramas funcionales sin descriptor estable. Una rama de diccionario funcional tampoco posee ancla pública: D-090 le asigna únicamente una clave local dentro de su propietario para la futura representación semántica posterior a tipado y elaboración. `when`, `if`, `then`, `after` y `otherwise` pueden reflejarse como clases presentes mediante `~clauses`, pero sus cuerpos no se convierten en objetos metadata-bearing.",
    "No lo son expresiones, sentencias, operandos, condiciones, cuerpos de cláusula, tokens, nodos arbitrarios del AST ni ramas funcionales sin descriptor estable. Una rama de diccionario funcional tampoco posee ancla pública: su identidad estructural local pertenece al diccionario propietario y sirve para reconstrucción y análisis posteriores, sin convertirse en ancla ni símbolo. `when`, `if`, `then`, `after` y `otherwise` pueden reflejarse como clases presentes mediante `~clauses`, pero sus cuerpos no se convierten en objetos metadata-bearing.",
)
replace_once(
    "notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md",
    "- El AST superficial conserva declaraciones de metadatos y cuerpos de metadatos; la futura representación semántica posterior a tipado y elaboración distingue propiedades intrínsecas de valores `Metadata` configurados.",
    "- El AST superficial conserva declaraciones y cuerpos de metadatos; tipado y elaboración distinguen propiedades intrínsecas de valores `Metadata` configurados. La codificación mecánica posterior de esa distinción todavía no está fijada.",
)

replace_once(
    "notas/decisiones/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas.md",
    "Determinan la categoría estática del receptor, aplican narrowing cuando exista y seleccionan el contrato de propiedad. Si ninguna propiedad compatible existe para todos los casos todavía posibles del receptor, emiten error estático. Solo los accesos válidos se elaboran en la futura representación semántica posterior a tipado y elaboración con tipo de resultado.",
    "Determinan la categoría estática del receptor, aplican narrowing cuando exista y seleccionan el contrato de propiedad. Si ninguna propiedad compatible existe para todos los casos todavía posibles del receptor, emiten error estático. Solo los accesos válidos llegan a elaboración, que determina su tipo de resultado; la representación mecánica posterior todavía no está fijada.",
)
replace_once(
    "notas/decisiones/ADR-092-disponibilidad-estatica-de-propiedades-reflectivas.md",
    "5. La futura representación semántica posterior a tipado y elaboración solo contiene `MetadataAccessExpr` para propiedades compatibles con la categoría estática resuelta.",
    "5. Tipado y elaboración solo aceptan accesos de metadata compatibles con la categoría estática resuelta y determinan su tipo de resultado.",
)

# Quality gates for accidental automatic wording and prematurely fixed future node names.
for path in (ROOT / "notas/decisiones").glob("ADR-*.md"):
    text = path.read_text(encoding="utf-8")
    for bad in ["al representación", "e representación", "elaboración elaborado", "dla futura"]:
        if bad in text:
            raise SystemExit(f"{path.name}: redacción automática defectuosa: {bad}")

for bad_node in [
    "ContextualAliasConstructionExpr",
    "ExactDictionarySetOperationExpr",
    "FunctionalDictionarySetOperationExpr",
    "ExactNominalTypeTestExpr",
]:
    offenders = []
    for path in (ROOT / "notas/decisiones").glob("ADR-*.md"):
        if bad_node in path.read_text(encoding="utf-8"):
            offenders.append(path.name)
    if offenders:
        raise SystemExit(f"nodo futuro todavía fijado por ADR: {bad_node}: {offenders}")

Path(__file__).unlink()
