from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def patch(path: str, old: str, new: str, label: str) -> None:
    p = root / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, found {count}")
    p.write_text(text.replace(old, new, 1).rstrip("\n") + "\n", encoding="utf-8", newline="\n")

patch(
    "especificacion/07-gramatica-concreta.md",
    "`Num` admite paso exacto explícito y un intervalo general de `Num` sin paso es inválido. `Rum` nunca admite `by`; una colección explícita de `Rum` sí es enumerable.",
    "`Num` admite paso exacto explícito y un intervalo general de `Num` sin paso es inválido. Los intervalos de `Rum` nunca admiten `by`, ni en iteración ni en dominios escalonados; una colección explícita de valores `Rum` sí es enumerable.",
    "clarify Rum progression",
)
patch(
    "notas/decisiones/ADR-057-gramatica-concreta-y-continuacion.md",
    "selección/cuantiﬁcadores",
    "selección/cuantificadores",
    "normalize quantifier spelling",
)
print("D088_FIX_V2_OK")
