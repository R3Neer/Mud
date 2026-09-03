---
id: D-089
title: "Clasificación contextual de formas fuente sin dependencia circular del scanner"
status: current
date: 2026-08-16
supersedes: []
superseded-by: []
questions:
  - "Q-054"
  - "Q-055"
affects:
  - "scanner, formas de unidad, literales de magnitudes de punto, CST, parser, elaboración contextual y conformidad"
---
# ADR-089 — Clasificación contextual de formas fuente sin dependencia circular del scanner

- Modifica: [[ADR-062-literales-canonicos-de-magnitudes-de-punto|D-062]] y [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]].
- Cierra: [[notas/preguntas/Q-054-catalogo-y-resolucion-lexica-de-unidades-y-prefijos|Q-054]] y [[notas/preguntas/Q-055-literales-de-magnitudes-de-punto|Q-055]].

## Contexto

D-062 y D-076 permiten que información declarada por el propio programa participe en formas fuente: `~format` define la escritura canónica de una magnitud de punto y las unidades admiten identificador, nombre, plural, abreviatura y formas prefijadas. El scanner inicial no puede depender de esas declaraciones sin introducir un ciclo entre tokenización, parsing y resolución.

## Decisión

### Scanner base y clasificador contextual

El scanner base depende exclusivamente de Unicode, trivia y del catálogo léxico fijo de MUD. Produce un flujo sin pérdidas con offsets fuente, pero **no** consulta declaraciones `magnitude`, catálogos de unidades, `~format` ni tipos esperados.

`POINT_LITERAL` y `UNIT_FORM` son tokens contextuales, no producciones del scanner base. Un clasificador contextual puede añadir una alternativa de tokenización sobre un intervalo exacto del texto fuente cuando la resolución y el tipo esperado aporten la información requerida. La alternativa conserva el mismo `source_span`; no reconstruye la escritura concatenando tokens base.

Una implementación puede representar esta frontera como un token lattice, re-tokenización localizada, parser diferido o una estrategia equivalente. Es conforme si el scanner base es independiente del modelo y la clasificación contextual produce exactamente los mismos spans y resultados observables.

### Literales de punto

Cuando una posición de expresión posee un único tipo esperado que es una magnitud `point over` con `~format`, el clasificador intenta consumir desde el offset fuente una representación canónica completa de ese formato. Si coincide de forma exacta e invertible, produce un `POINT_LITERAL` que cubre todo el span reconocido, aunque ese mismo texto pudiera descomponerse en varios tokens base o formar una expresión ordinaria.

En ese contexto, la interpretación `POINT_LITERAL` tiene prioridad sobre la ruta de tokenización base para el mismo span. Sin un tipo esperado único no se crea esa alternativa contextual. La coincidencia debe terminar exactamente donde termina la representación canónica; no puede aceptar un prefijo de una forma más larga que el mismo formato pudiera consumir.

La obligación de invertibilidad de D-062 incluye por tanto la delimitación determinista de la representación completa. Un `~format` que no permita reconocer de forma unívoca el final de su propia forma canónica es inválido para una magnitud de punto.

### Formas de unidad

Las formas de unidad se clasifican después de conocer el catálogo semántico de magnitudes y unidades. El clasificador consulta el texto fuente directamente a partir de una posición en la que la gramática de cantidad admite una unidad. Puede producir `UNIT_FORM` para el identificador declarado, un `~name`, `~plural` o `~abbreviation` admisible, o una forma prefijada habilitada.

El identificador declarado conserva las reglas léxicas ordinarias de identificador de unidad. Los tres valores configurables `~name`, `~plural` y `~abbreviation` comparten, en cambio, el mismo criterio cuando participan como forma fuente: pueden contener espacios U+0020 y puntuación, pero deben contener al menos un carácter alfabético; por tanto no pueden estar formados íntegramente por cifras ni íntegramente por caracteres no alfabéticos. Una forma completa que coincida exactamente con una palabra clave de MUD es inválida como forma fuente. Estas restricciones afectan a su uso como sintaxis y no impiden conservar el mismo valor como presentación cuando no sea admisible como forma fuente.

La validación se realiza sobre el cierre de formas habilitadas de cada magnitud, incluidas todas las combinaciones con prefijos permitidos. Dos unidades distintas de la misma magnitud no pueden producir la misma forma fuente, ni directamente ni después de aplicar un prefijo. Una colisión dentro de la magnitud es un error estático de la declaración y no se difiere al lugar de uso. Entre magnitudes distintas continúa aplicándose la desambiguación contextual descrita a continuación.

Cuando existe un tipo o magnitud esperada, solo compiten las formas compatibles con ella. Sin tipo esperado, una forma únicamente es válida si el catálogo resuelto determina una unidad de manera unívoca. Dos candidatos semánticos distintos con la misma forma visible entre magnitudes distintas son ambiguos salvo cualificación admitida por la gramática.

Si varias formas compatibles comparten prefijo, se elige la coincidencia canónica completa más larga. Dos candidatos distintos que consumen exactamente el mismo span continúan siendo ambiguos; el orden de declaración no desempata. La clasificación contextual puede cubrir varios tokens base y no concede significado léxico nuevo a esa secuencia fuera de una posición de unidad.

La adyacencia `3m` se resuelve sobre el mismo offset inmediatamente posterior al número. La presencia o ausencia de trivia antes de una unidad no cambia la unidad seleccionada; el formateador conserva la normalización canónica de D-076.

### CST y AST

La CST sin pérdidas conserva los tokens base y el span fuente suficiente para reproducir la clasificación contextual. Una implementación puede materializar el token contextual en una vista derivada, pero nunca pierde los caracteres originales. El AST superficial conserva `PointLiteral(source_form)` y las formas de unidad ya clasificadas; no contiene una dependencia hacia el catálogo del scanner base.

## Consecuencias

- El scanner inicial deja de consultar información semántica futura.
- `~format` sigue definiendo una forma literal fuente directa, sin delimitador adicional obligatorio.
- Las colisiones entre una forma contextual y una expresión ordinaria se resuelven por contexto semántico, no por prioridad global del scanner.
- Las unidades pueden mantener formas Unicode o configuradas sin convertirlas en identificadores generales.
- La implementación puede ser multipaso, pero la tokenización base continúa siendo reproducible a partir del texto aislado.

## Verificación

1. El scanner base produce el mismo flujo antes y después de resolver declaraciones de magnitud.
2. `07:05:00` se clasifica como un único `POINT_LITERAL` cuando el tipo esperado selecciona su magnitud.
3. La misma secuencia sin tipo esperado único no recibe clasificación de punto.
4. Un formato que colisiona con una expresión ordinaria gana solo bajo el tipo de punto esperado.
5. Se rechaza un formato cuyo final no pueda reconocerse unívocamente.
6. Una forma de unidad única se resuelve sin tipo esperado y una colisión exige contexto o cualificación.
7. Coincidencias de unidad por prefijo usan la forma completa más larga sin depender del orden de declaración.
8. `3m` y `3 m` clasifican la misma unidad y el formateador produce la forma canónica espaciada.
9. `~name`, `~plural` y `~abbreviation` aceptan espacios, pero una forma fuente íntegramente numérica o no alfabética se rechaza.
10. Una forma fuente idéntica a una palabra clave de MUD se rechaza.
11. Las colisiones entre unidades de la misma magnitud se detectan también después de expandir todos los prefijos habilitados.
12. CST y round-trip conservan exactamente el texto fuente anterior a la clasificación contextual.
