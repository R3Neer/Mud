# Resolución nominal de MUD

Este directorio contiene el contrato mecánico normativo de la fase de resolución de nombres. Complementa [[../09-nombres-y-anclas|09. Nombres, paths y anclas]] y no define tipado ni semántica dinámica.

## `mud-nominal-hir.asdl`

Es la salida normativa de resolución nominal sobre el AST superficial. Conserva símbolos, scopes, bindings, anclas y las relaciones nominales `Owns`, `Specializes` y `RefersTo`.

No puede contener tipos efectivos, dominios efectivos, cardinalidades inferidas, narrowing, conversiones elaboradas, efectos, dependencias semánticas ni evidencia de terminación. Esas conclusiones pertenecen a fases posteriores todavía no formalizadas mecánicamente.

El HIR nominal es derivado y reconstruible: no constituye una fuente semántica independiente.
