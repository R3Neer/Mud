from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one match, found {count}: {old[:100]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    "notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente.md",
    """La especialización hereda:\n\n- declaraciones de campos;\n- restricciones;\n- dominios;\n- valores predeterminados efectivos;\n- los demás elementos de esquema que la especificación autorice expresamente.\n""",
    """La especialización hereda:\n\n- declaraciones de campos;\n- restricciones;\n- dominios;\n- valores predeterminados efectivos;\n- inicializadores de `thing` aplicables;\n- los demás elementos de esquema que la especificación autorice expresamente.\n""",
)
replace_once(
    "notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente.md",
    """La definición canónica de una `thing` concreta puede declarar antecesoras e inicializadores:\n\n```mud\nthing N as BaseOne, BaseTwo {\n    ...\n}\n```\n\nAl activarla por primera vez mediante `start with` o:\n\n```mud\ncreate N\n```\n\nla inicialización de $N$ parte de los predeterminados efectivos de sus antecesoras, incorpora las declaraciones locales y aplica después las inicializaciones explícitas. No parte de sus estados activos. Sin antecesoras, los campos sin predeterminado explícito emplean el de su tipo. Una reactivación conserva la carga almacenada conforme a D-021.\n\nLas asignaciones concretas del bloque inicializan $N$, pero no se convierten en predeterminados heredables. Solo una declaración explícita de predeterminado forma parte del esquema.\n""",
    """La definición canónica de una `thing`, concreta o abstracta, puede declarar antecesoras e inicializadores:\n\n```mud\nthing N as BaseOne, BaseTwo {\n    field = value\n}\n\nabstract thing A as BaseOne {\n    field = value\n}\n```\n\nLa forma `field = value` no declara un campo. Debe dirigirse a un campo almacenado ya aportado por el esquema heredado. Una misma definición de `thing` no puede declarar localmente un campo y además inicializarlo mediante otra instrucción `field = value`. La forma `field: Type = value` sigue siendo una única declaración de campo con predeterminado y no cuenta como un inicializador separado.\n\nUna `thing` abstracta no materializa carga propia, pero sus inicializadores forman parte de la especialización y pueden contribuir a la primera materialización de una descendiente concreta. Para un mismo campo, un inicializador declarado en una descendiente más específica sustituye a los inicializadores heredados menos específicos. Si un mismo inicializador original alcanza una descendiente por varias rutas de un diamante, se deduplica por origen; inicializadores independientes e incomparables que compitan por el mismo campo producen conflicto, sin prioridad por el orden escrito de `as`, conforme a D-084.\n\nAl activar por primera vez una `thing` concreta mediante `start with` o:\n\n```mud\ncreate N\n```\n\nla inicialización de $N$ parte de los predeterminados efectivos de sus antecesoras, incorpora las declaraciones locales y aplica después los inicializadores efectivos. No parte de los estados activos de sus antecesoras. Sin antecesoras, los campos sin predeterminado explícito emplean el de su tipo. Una reactivación conserva la carga almacenada conforme a D-021.\n\nLos inicializadores no se convierten en declaraciones de campo ni en predeterminados de esquema. Que un inicializador de una `thing` abstracta pueda heredarse como contribución de inicialización no cambia el predeterminado heredable del campo.\n""",
)
replace_once(
    "notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente.md",
    """```mud\nthing France as Kingdom {\n    treasury = 20\n}\n```\n\nAl activarse por primera vez, `France.treasury` vale `20`, pero esa asignación no se convierte en predeterminado para futuras descendientes de `France`.\n""",
    """```mud\nthing France as Kingdom {\n    treasury = 20\n}\n```\n\nAl activarse por primera vez, `France.treasury` vale `20`, pero esa asignación de una `thing` concreta no se convierte en predeterminado ni en inicializador heredable para futuras descendientes de `France`.\n\n```mud\nabstract thing RichKingdom as Kingdom {\n    treasury = 20\n}\n\nthing Lydia as RichKingdom {}\n```\n\n`RichKingdom` no materializa una tesorería propia. Su inicializador sí contribuye a la primera materialización de `Lydia`, que comienza con `treasury = 20`.\n\nEs inválido declarar e inicializar por separado el mismo campo en una sola definición:\n\n```mud\nthing Broken as Kingdom {\n    treasury: Money = 10\n    treasury = 20\n}\n```\n""",
)
replace_once(
    "notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente.md",
    """6. Aplicación de los inicializadores canónicos en la primera activación.\n7. Ausencia de propagación implícita a futuras descendientes.\n""",
    """6. Aplicación de los inicializadores efectivos en la primera activación.\n7. Herencia de inicializadores desde `thing` abstractas y ausencia de propagación desde inicializadores locales de `thing` concretas.\n8. Rechazo de declarar un campo e inicializarlo por separado dentro de la misma `thing`.\n9. Deduplicación por origen y conflicto sin prioridad para inicializadores abstractos heredados por especialización múltiple.\n""",
)

replace_once(
    "especificacion/07-gramatica-concreta.md",
    "### Inicializadores concretos\n",
    "### Inicializadores de `thing`\n",
)
replace_once(
    "especificacion/07-gramatica-concreta.md",
    """Una `thing` concreta puede inicializar de forma local un campo almacenado de su esquema efectivo mediante una asignación sin redeclarar el campo:\n\n```text\nfieldName = static-expression\n```\n\nEl objetivo se conserva como nombre de campo hasta la resolución y puede corresponder a un campo local o heredado. No declara un campo nuevo, no sustituye su predeterminado heredable y no puede dirigirse a un campo calculado. El valor usa `constant-expression`, por lo que debe ser una expresión estática cerrada. Una `abstract thing` no posee estado concreto propio y no puede contener esta forma; se rechaza durante la validación previa al AST.\n""",
    """Una `thing`, concreta o abstracta, puede inicializar un campo almacenado ya aportado por su esquema heredado mediante una asignación sin redeclarar el campo:\n\n```text\nfieldName = static-expression\n```\n\nEl objetivo se conserva como nombre de campo hasta la resolución. No declara un campo nuevo, no sustituye su predeterminado heredable y no puede dirigirse a un campo calculado. Debe resolver a un campo heredado: una misma `thing` no puede declarar localmente `fieldName` y además contener una instrucción separada `fieldName = ...`. La forma `fieldName: Type = value` es una sola declaración con predeterminado y sigue siendo válida. El valor del inicializador usa `constant-expression`, por lo que debe ser una expresión estática cerrada.\n\nEn una `abstract thing`, el inicializador no materializa carga propia; se conserva como contribución heredada para la primera materialización de descendientes concretos. En una `thing` concreta, el inicializador local se aplica a su propia primera materialización y no se hereda por sus descendientes. Un inicializador más específico sustituye a uno heredado menos específico. La especialización múltiple no obtiene prioridad del orden de `as`: el mismo origen se deduplica y contribuciones independientes e incomparables sobre el mismo campo entran en conflicto conforme a D-084.\n""",
)
replace_once(
    "especificacion/07-gramatica-concreta.md",
    """En `France`, `20` inicializa únicamente la carga propia de `France.treasury` en su primera materialización. No se convierte en el predeterminado que heredarían descendientes de `France`, y una reactivación posterior a `destroy France` conserva la carga almacenada en vez de ejecutar de nuevo el inicializador. Esta distinción implementa D-015 y el ciclo de primera materialización fijado por D-054.\n\n`name = valor` no posee un significado intrínseco especial: si `name` es un campo almacenado ordinario del esquema efectivo, usa esta misma forma; `~name` continúa siendo el metadato de presentación.\n""",
    """En `France`, `20` inicializa únicamente la carga propia de `France.treasury` en su primera materialización. No se convierte en el predeterminado ni en un inicializador heredable para descendientes de `France`, y una reactivación posterior a `destroy France` conserva la carga almacenada en vez de ejecutar de nuevo el inicializador. Esta distinción implementa D-015 y el ciclo de primera materialización fijado por D-054.\n\n```mud\nabstract thing RichKingdom as Kingdom {\n    treasury = 20\n}\n\nthing Lydia as RichKingdom\n```\n\n`RichKingdom` no posee una carga concreta de `treasury`, pero su inicializador participa en la primera materialización de `Lydia`.\n\nEs inválido mezclar declaración e inicializador separado del mismo campo en una definición:\n\n```mud\nthing Broken as Kingdom {\n    treasury: Money = 10\n    treasury = 20\n}\n```\n\n`name = valor` no posee un significado intrínseco especial: si `name` es un campo almacenado heredado del esquema efectivo, usa esta misma forma; `~name` continúa siendo el metadato de presentación.\n""",
)

replace_once(
    "especificacion/08-sintaxis-abstracta.md",
    "- Inicializadores concretos de estado.\n",
    "- Inicializadores de campos heredados.\n",
)
replace_once(
    "especificacion/08-sintaxis-abstracta.md",
    """Conserva una forma `fieldName = constant-expression` escrita en el cuerpo de una `thing` concreta. La validación previa al AST rechaza esta forma en una `abstract thing`. No es un `StoredFieldDecl` y no se incorpora a `defaultValue`: D-015 exige que inicialice únicamente el estado propio de esa identidad y que no se convierta en esquema heredable. `name` permanece como `FieldName` sin resolver y `value` como `expr`; la resolución y elaboración posteriores comprueban que el objetivo sea un campo almacenado efectivo y que el valor satisfaga su tipo y dominio.\n\nLa secuencia de inicializadores se conserva separada de la de campos porque la semántica declarativa aplica primero el esquema y sus predeterminados efectivos y después las inicializaciones concretas. La CST sigue conservando el orden físico intercalado del cuerpo.\n""",
    """Conserva una forma `fieldName = constant-expression` escrita en el cuerpo de una `thing`, sea concreta o abstracta. No es un `StoredFieldDecl` y no se incorpora a `defaultValue`: D-015 mantiene separados el predeterminado de esquema y la contribución de inicialización. `name` permanece como `FieldName` sin resolver y `value` como `expr`; la resolución y elaboración posteriores comprueban que el objetivo sea un campo almacenado heredado y que el valor satisfaga su tipo y dominio.\n\nLa validación previa al AST rechaza que una misma definición contenga una declaración local de campo y un `ThingInitializer` con el mismo nombre. Una declaración `fieldName: Type = value` conserva su `defaultValue` dentro del `StoredFieldDecl` y no genera `ThingInitializer`.\n\nLa secuencia de inicializadores se conserva separada de la de campos. En una `thing` abstracta representa contribuciones heredables de inicialización sin materializar carga propia; en una concreta representa contribuciones a su primera materialización. La CST sigue conservando el orden físico intercalado del cuerpo.\n""",
)

replace_once(
    "especificacion/sintaxis/cst-a-ast-superficial.md",
    """`thing-body` y `thing-body-declaration` no generan nodos AST independientes. `metadata-assignment` sí produce un nodo propio y no se convierte en campo. Cada `field-declaration` alimenta la secuencia `fields`; en una `thing` concreta, cada `thing-initializer` produce `ThingInitializer(fieldName, value)` en la secuencia `initializers`, sin plegarse dentro de `StoredFieldDecl.defaultValue`. Una `abstract thing` con `thing-initializer` se rechaza durante la validación previa al AST. La omisión del cuerpo y un cuerpo explícito vacío producen las mismas secuencias vacías; el terminador se descarta como layout.\n""",
    """`thing-body` y `thing-body-declaration` no generan nodos AST independientes. `metadata-assignment` sí produce un nodo propio y no se convierte en campo. Cada `field-declaration` alimenta la secuencia `fields`; cada `thing-initializer`, tanto en una `thing` concreta como abstracta, produce `ThingInitializer(fieldName, value)` en la secuencia `initializers`, sin plegarse dentro de `StoredFieldDecl.defaultValue`. Si una misma definición declara localmente un campo y contiene un `thing-initializer` con el mismo nombre, se rechaza durante la validación previa al AST. La omisión del cuerpo y un cuerpo explícito vacío producen las mismas secuencias vacías; el terminador se descarta como layout.\n""",
)
replace_once(
    "especificacion/sintaxis/cst-a-ast-superficial.md",
    """Una forma `name = valor` ya no recibe un rechazo sintáctico especial. Se proyecta como cualquier otro `ThingInitializer`; la resolución posterior decide si `name` designa realmente un campo almacenado del esquema efectivo. El metadato de presentación continúa escribiéndose `~name = valor`.\n""",
    """Una forma `name = valor` no recibe un rechazo sintáctico especial. Se proyecta como cualquier otro `ThingInitializer`; la resolución posterior decide si `name` designa realmente un campo almacenado heredado del esquema efectivo. Si la misma `thing` declara localmente un campo ordinario `name`, la combinación se rechaza por la regla general que impide declarar e inicializar por separado el mismo campo. El metadato de presentación continúa escribiéndose `~name = valor`.\n""",
)

cases_path = Path("especificacion/sintaxis/casos/cst-ast.yaml")
cases = cases_path.read_text(encoding="utf-8")
old_case = r'''- id: abstract-thing-concrete-initializer-rejected
  category: validation-before-ast
  source: "abstract thing AbstractCounter {\n    value: Nat\n    value = 1\n}\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - abstract-thing-cannot-have-initializer
  produces_ast: false
'''
new_cases = r'''- id: abstract-thing-inherited-initializer
  category: thing
  source: "thing Being {\n    age: Nat = 0\n}\nabstract thing Adult as Being {\n    age = 18\n}\nthing Clara as Adult\n"
  cst_root: MudFileSyntax
  ast: ThingDecl(Adult, isAbstract=Enabled, initializers=[ThingInitializer(age, 18)])
  normalizations:
  - preserve-abstract-initializer-for-descendant-materialization
  produces_ast: true
- id: thing-local-field-and-initializer-rejected
  category: validation-before-ast
  source: "thing Broken {\n    age: Nat = 18\n    age = 20\n}\n"
  cst_root: MudFileSyntax
  expected_diagnostics:
  - thing-field-cannot-be-declared-and-initialized-separately
  produces_ast: false
'''
if cases.count(old_case) != 1:
    raise SystemExit("cst-ast.yaml: old abstract initializer rejection case not found exactly once")
cases_path.write_text(cases.replace(old_case, new_cases, 1), encoding="utf-8")

replace_once(
    "especificacion/sintaxis/validate_syntax_model.py",
    """        "thing-concrete-initializer",\n        "thing-name-field-initializer",\n        "abstract-thing-concrete-initializer-rejected",\n        "subaction-internal-call",\n""",
    """        "thing-concrete-initializer",\n        "thing-name-field-initializer",\n        "abstract-thing-inherited-initializer",\n        "thing-local-field-and-initializer-rejected",\n        "subaction-internal-call",\n""",
)

assert "abstract-thing-cannot-have-initializer" not in cases_path.read_text(encoding="utf-8")
assert "Una `abstract thing` no posee estado concreto propio y no puede contener esta forma" not in Path("especificacion/07-gramatica-concreta.md").read_text(encoding="utf-8")
assert "thing-field-cannot-be-declared-and-initialized-separately" in cases_path.read_text(encoding="utf-8")
