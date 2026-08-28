# Representaciones intermedias de MUD

Este directorio contiene contratos mecánicos derivados del AST superficial. No contiene CST ni una segunda sintaxis fuente.

## `mud-nominal-hir.asdl`

Es el contrato normativo producido por resolución de nombres. Contiene símbolos, scopes, bindings, anclas y aristas nominales parciales. No puede contener tipos efectivos, dominios efectivos, cardinalidades, conversiones elaboradas ni evidencia de terminación.

## `mud-semantic-ir.asdl`

Es el esquema normativo posterior a tipado y elaboración. Puede contener tipos efectivos, dominios, cardinalidades, narrowing, dependencias y evidencias de terminación porque se produce después de esas fases.

Ninguna representación intermedia es fuente independiente de verdad. Ambas deben poder descartarse y reconstruirse desde los archivos `.mud`, el AST superficial y la norma aplicable.

El único AST normativo de fuente continúa siendo `especificacion/sintaxis/mud-surface-ast.asdl`.
