# Gramáticas normativas de MUD

Este directorio contiene las gramáticas de referencia de MUD 1.0:

- `mud-lexico.ebnf`: transformación de Unicode fuente en tokens.
- `mud.ebnf`: transformación de tokens en sintaxis concreta.

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

La EBNF distingue reconocimiento sintáctico de elaboración semántica. Las restricciones que requieren nombres o tipos —por ejemplo, decidir si `in` expresa pertenencia o una unidad— están identificadas en [[../07-gramatica-concreta]] y no amplían las formas aceptadas.

Símbolo inicial:

- Léxico: `mud-source`.
- Concreto: `mud-file`.

Las implementaciones pueden usar otra técnica de parsing si producen la misma agrupación y los mismos rechazos.

Validación editorial:

```powershell
python especificacion/gramatica/validate_grammar.py
```

La comprobación detecta producciones duplicadas, indefinidas o inalcanzables. No sustituye las futuras pruebas de conformidad del parser.
