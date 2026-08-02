# Gramáticas normativas de MUD

Este directorio contiene las gramáticas de referencia de MUD 1.0:

- `mud-lexico.ebnf`: transformación de Unicode fuente en tokens significativos y formas léxicas.
- `mud.ebnf`: transformación de tokens significativos en sintaxis concreta.

La representación sin pérdidas, el catálogo de nodos CST y el AST superficial se documentan en [[../sintaxis/README|sintaxis/]].

Ambas usan este dialecto EBNF:

```text
regla       ::= expresión ;
alternativa ::= a | b ;
opcional    ::= [ a ] ;
repetición  ::= { a } ;
grupo       ::= ( a | b ) ;
terminal    ::= "texto exacto" ;
especial    ::= ? condición definida en prosa ? ;
```

Los detalles normativos del dialecto se encuentran en [[../03-notacion]].

Símbolo inicial:

- Léxico: `mud-source`.
- Concreto: `mud-file`.

## Productos

`mud-lexico.ebnf` no implica que una implementación deba descartar comentarios o espacios. [[../06-lexico]] define un flujo completo con trivia y una vista significativa para la gramática.

`mud.ebnf` produce la agrupación inventariada en:

- `../sintaxis/mud-syntax-kinds.yaml`.
- `../sintaxis/cst-sin-perdidas.md`.

La proyección abstracta se define en:

- `../08-sintaxis-abstracta.md`.
- `../sintaxis/mud-surface-ast.asdl`.
- `../sintaxis/cst-a-ast-superficial.md`.

## Scanner modal

Las plantillas `Text` requieren modos anidados. `mud-lexico.ebnf` mantiene el inventario de las formas especiales; [[../06-lexico]] define el algoritmo; `mud.ebnf` analiza los tokens emitidos dentro de interpolaciones.

Las formas de unidad y de magnitud de punto también son contextuales. Que exista un token contextual no anticipa su resolución semántica.

## Separación de responsabilidades

La EBNF distingue reconocimiento de elaboración. No intenta comprobar:

- Existencia de nombres.
- Compatibilidad de tipos.
- Constancia de expresiones.
- Validez de dominios.
- Clasificación de acciones.
- Selección de receptor múltiple.

Las restricciones concretas no expresadas cómodamente en EBNF se validan después de la CST y antes del AST.

Validación editorial:

```powershell
python especificacion/gramatica/validate_grammar.py
```

La comprobación detecta producciones duplicadas, indefinidas o inalcanzables. No sustituye las futuras pruebas de conformidad del parser.

Comprobación conjunta de gramática, CST y AST:

```powershell
python especificacion/sintaxis/validate_syntax_model.py
```

La primera comprobación detecta producciones duplicadas, indefinidas o inalcanzables. La segunda comprueba inventario CST, cobertura y destinos ASDL. Ninguna sustituye las pruebas de conformidad de un parser.

## Política de cambio

Toda modificación estructural de una producción debe actualizar en el mismo commit:

1. La EBNF.
2. La explicación de [[../07-gramatica-concreta]].
3. `mud-syntax-kinds.yaml`.
4. `cobertura-sintactica.yaml`.
5. La transformación CST → AST cuando proceda.
6. El ASDL cuando cambie una distinción abstracta.
7. Los casos de frontera afectados.

Las implementaciones pueden usar cualquier técnica de scanning o parsing si producen la misma CST observable, los mismos rechazos y el mismo AST superficial normalizado.
