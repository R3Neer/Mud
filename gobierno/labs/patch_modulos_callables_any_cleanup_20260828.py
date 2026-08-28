from pathlib import Path

path = Path.cwd() / "especificacion/07-gramatica-concreta.md"
old = "`Any` es el tipo superior abierto de los valores MUD del proyecto. Incluye básicos, valores incorporados como los miembros de `Prefix`, `thing`, aliases, miembros de `family`, magnitudes, intervalos, colecciones, diccionarios y productos estructurales. No incluye acciones, reglas, tests, declaraciones ni nodos de AST como valores ordinarios."
new = "`Any` es el tipo superior abierto de los valores MUD del proyecto. Incluye básicos, valores incorporados como los miembros de `Prefix`, identidades `thing`, aliases, miembros de `family`, magnitudes, intervalos, colecciones, diccionarios, productos estructurales y descriptores first-class de declaraciones y tipos conforme a D-096. Los nodos de AST no son valores MUD por el mero hecho de existir como representación del compilador."
text = path.read_text(encoding="utf-8")
if new in text:
    pass
elif text.count(old) == 1:
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
else:
    raise SystemExit(f"07-gramatica-concreta: se esperaba exactamente una formulación legacy de Any y hay {text.count(old)}")
print("07-gramatica-concreta Any aligned with D-096")
