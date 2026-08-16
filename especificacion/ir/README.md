# IR semántico de MUD

Este directorio contiene contratos mecánicos posteriores a resolución nominal, tipado y elaboración. No contiene CST ni AST de fuente.

## `mud-semantic-ir.asdl`

Es el esquema normativo del significado elaborado reconstruible de un programa. Puede contener tipos efectivos, dominios, cardinalidades, narrowing, dependencias y evidencias de terminación porque se produce después de esas fases.

El IR no es fuente independiente de verdad. Debe poder descartarse y reconstruirse desde los archivos `.mud`, el AST superficial y las decisiones/versiones aplicables.

El AST normativo de fuente continúa siendo `especificacion/sintaxis/mud-surface-ast.asdl`.
