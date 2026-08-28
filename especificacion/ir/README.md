# Representaciones intermedias de MUD

Este directorio contiene contratos mecánicos derivados del AST superficial. No contiene CST ni una segunda sintaxis fuente.

## `mud-nominal-hir.asdl`

Es el contrato normativo producido por resolución de nombres. Contiene símbolos, scopes, bindings, anclas y aristas nominales parciales. No puede contener tipos efectivos, dominios efectivos, cardinalidades, conversiones elaboradas ni evidencia de terminación.

## `mud-semantic-ir.asdl`

Es el esquema normativo posterior a tipado y elaboración. Declara una versión de esquema obligatoria y conserva las distinciones elaboradas necesarias para reconstruir tipos efectivos, dominios, cardinalidades, firmas, cuerpos semánticos, efectos, activación modular, dependencias, narrowing y evidencias de terminación.

Las declaraciones conservan una clase semántica explícita y separan participantes `for`, patrones conjuntos `on` y valores `given`. Los cuerpos distinguen reglas booleanas, reactivas y `always`, actions/subactions, `look`, `message` y tests. Los bloques ejecutables conservan el orden de vinculaciones locales y efectos, y los tests conservan su activación local, efectos, aserciones y diagnósticos.

El IR conserva también el conjunto de activación de cada módulo junto con sus `uses`. La forma interna exacta de los matches causales de triggers no se fija mientras no exista un contrato normativo adicional que deba sobrevivir a la elaboración.

Ninguna representación intermedia es fuente independiente de verdad. Ambas deben poder descartarse y reconstruirse desde los archivos `.mud`, el AST superficial y la norma aplicable.

El único AST normativo de fuente continúa siendo `especificacion/sintaxis/mud-surface-ast.asdl`.
