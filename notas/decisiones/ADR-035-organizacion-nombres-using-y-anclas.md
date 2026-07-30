---
id: D-035
title: "Organización, nombres, `using` y anclas"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-001"
  - "Q-014"
  - "Q-054"
affects:
  - "futuro `05-modelo-de-programa.md`, futuro `06-lexico.md`, futuro `09-nombres-y-anclas.md`"
---
# ADR-035 — Organización, nombres, `using` y anclas

- Relacionada con: [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]]
- Modificada por: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Modificada además por: [[notas/decisiones/ADR-065-cabecera-using-de-fichero|D-065]]
- Preguntas relacionadas: Q-001, Q-014, Q-054
- Documentos afectados: futuro `05-modelo-de-programa.md`, futuro `06-lexico.md`, futuro `09-nombres-y-anclas.md`

## Decisión

### Archivos y namespaces

El namespace se deriva de la ruta relativa dentro de la raíz MUD y no se declara en el archivo. Un archivo puede contener declaraciones `using` y varias declaraciones de cualquier categoría.

El archivo es una unidad física, no una unidad de identidad semántica. Cada declaración conserva por separado ancla, dependencias, nodo de grafo, procedencia e historial.

Mover una declaración entre archivos del mismo namespace no cambia su ancla. Moverla a otro namespace sí la cambia, salvo una migración explícita todavía definida por Q-014.

### Declaraciones `using`

Se admiten declaraciones `using` exactas y recursivas:

```mud
using warfare.armies
using warfare.armies.*
```

Todas las declaraciones `using` forman la cabecera del fichero y deben aparecer antes de cualquier declaración de primer nivel. Después de la primera declaración nominal o `start with` no puede aparecer otro `using`. Su orden dentro de la cabecera no introduce alcance secuencial.

Para un nombre no cualificado, la búsqueda sigue:

1. Declaraciones locales.
2. Mismo namespace.
3. Declaraciones `using` exactas.
4. Declaraciones `using` recursivas.

Una referencia completamente cualificada se resuelve directamente. Si dos candidatos importados proporcionan el mismo nombre no cualificado, existe ambigüedad y debe escribirse el nombre cualificado.

El orden textual de archivos y declaraciones `using` no decide empates.

### Convenciones de identificadores

- Namespace: segmentos `lowerCamelCase` separados por puntos.
- Declaraciones nominales (`thing`, `alias`, `family`, `magnitude`, `rule`, `action`, `test`, `look` y `message`): `PascalCase`.
- Miembros de una `family`: `PascalCase`.
- Campos, componentes, roles, `given` y variables de iteración: `lowerCamelCase`.

Los identificadores son sensibles a mayúsculas. El catálogo de palabras reservadas no puede usarse como nombre de campo, componente, rol, `given`, variable local o declaración.

D-038, D-054 y D-055 distinguen las palabras reservadas de las contextuales. Una palabra contextual se reconoce únicamente en una posición gramatical concreta y puede ser un identificador ordinario fuera de ella. `start` es contextual en `start with`; `abstract` lo es delante de `thing`; `always` lo es delante de `rule`; y etiquetas como `name` o `prefixes` lo son dentro de las declaraciones que las definen.

`using`, `with`, `family`, `test`, `otherwise` y `ordered` son palabras reservadas. En particular, `ordered` no puede usarse como identificador aunque aparezca fuera de una declaración `family` o de una especificación de colección.

### Nombres cualificados y anclas

Los nombres cualificados usan puntos:

```text
warfare.armies.Army
geometry.Square
```

Las anclas usan `::` y no contienen el archivo:

```text
thing::warfare.armies.Army
thing::warfare.armies.Army::morale
alias::geometry.Square
alias::geometry.Square::file
family::warfare.armies.Severity
magnitude::physics.Length
rule::warfare.armies.IsDestroyed
action::warfare.armies.Recruit
test::warfare.armies.RecruitIncreasesArmy
look::warfare.armies.Summary
message::warfare.armies.Destroyed
```

Una ancla es globalmente única, sensible a mayúsculas y estable frente a movimientos dentro del mismo namespace. Se utiliza en el grafo, IR, consultas, diagnósticos, trazabilidad y operaciones semánticas.

D-061 añade `anchor{...}` como forma contextual exclusiva de una plantilla `Text`. Produce la escritura canónica del ancla de una declaración o de un valor con identidad nominal anclada, sin convertir las declaraciones en valores ordinarios ni reservar `anchor` fuera de ese contexto.

La identidad estable de una unidad sin identificador de cabecera permanece en Q-054.

## Consecuencias

- La resolución de nombres no depende del orden de archivos.
- La procedencia física y la identidad semántica son dimensiones distintas.
- El compilador debe detectar ambigüedades en vez de elegir silenciosamente.
- La migración de namespace necesita una operación explícita, no un simple movimiento de archivo.

## Verificación futura

1. Varias declaraciones por archivo.
2. Movimiento dentro y fuera del namespace.
3. Declaración `using` exacta, recursiva y ambigua.
4. Resolución cualificada.
5. Colisión por mayúsculas y palabra reservada.
6. Uso ordinario de una palabra contextual fuera de su posición especial.
7. Estabilidad de anclas.
8. Separación entre `action::*`, `test::*`, `rule::*`, `family::*` y `thing::*`.
9. Interpolación contextual de un ancla y uso ordinario de `anchor` fuera de plantillas.
10. Rechazo de un `using` posterior a una declaración de primer nivel.
