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

- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Modificada por: [[notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco|D-068]]

- Relacionada con: [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]]
- Modificada por: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Modificada además por: [[notas/decisiones/ADR-065-cabecera-using-de-fichero|D-065]]
- Ampliada por: [[notas/decisiones/ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas|D-072]]
- Ampliada además por: [[ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]]
- Preguntas relacionadas: Q-001, Q-014, Q-054
- Documentos afectados: futuro `05-modelo-de-programa.md`, futuro `06-lexico.md`, futuro `09-nombres-y-anclas.md`

## Decisión

### Archivos y paths de MUD

El path de MUD se deriva de la ruta relativa dentro de la raíz MUD y no se declara en el archivo. `namespace` no es vocabulario de superficie y `path` no se reserva. Un archivo puede contener declaraciones `using` y varias declaraciones de cualquier categoría.

El archivo es una unidad física, no una unidad de identidad semántica. Cada declaración conserva por separado ancla, dependencias, nodo de grafo, procedencia e historial.

Mover una declaración entre archivos del mismo path no cambia su ancla. Moverla a otro path sí la cambia, salvo una migración explícita todavía definida por Q-014.

### Declaraciones `using`

Se admiten declaraciones `using` exactas y recursivas:

```mud
using warfare.armies
using warfare.armies.*
```

Todas las declaraciones `using` forman la cabecera del fichero y deben aparecer antes de cualquier declaración de primer nivel. Después de la primera declaración nominal o `start with` no puede aparecer otro `using`. Su orden dentro de la cabecera no introduce alcance secuencial.

Para un nombre no cualificado, la búsqueda sigue:

1. Declaraciones locales.
2. Mismo path de MUD.
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

D-038, D-054 y D-055 distinguen las palabras reservadas de las contextuales. Una palabra contextual se reconoce únicamente en una posición gramatical concreta y puede ser un identificador ordinario fuera de ella. `start` es contextual en `start with`; `abstract` lo es delante de `thing`; `always` lo es delante de `rule`. Los metadatos como `~name` o `~prefixes` usan la gramática general postfix `~`, no etiquetas contextuales especiales.

`using`, `with`, `family`, `test`, `otherwise`, `ordered` y el tipo incorporado `Thing` son palabras reservadas. En particular, `ordered` no puede usarse como identificador aunque aparezca fuera de una declaración `family` o de una especificación de colección. `name` no tiene una excepción sintáctica de cuerpo de `thing`: la presentación estándar se configura como `~name`, en un espacio distinto del de campos ordinarios.

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

La raíz incorporada usa el ancla reservada `thing::Thing` conforme a D-068.

Una ancla es globalmente única, sensible a mayúsculas y estable frente a movimientos dentro del mismo path. Se utiliza en el grafo, IR, consultas, diagnósticos, trazabilidad y operaciones semánticas.

D-087 retira `anchor{...}`. El ancla canónica se obtiene mediante el acceso ordinario `expression~anchor` y una plantilla la interpola como cualquier otra expresión: `"{expression~anchor}"`.

D-076 fija la identidad estable de cada unidad mediante el identificador `lowerCamel` obligatorio de su cabecera.

## Consecuencias

- La resolución de nombres no depende del orden de archivos.
- La procedencia física y la identidad semántica son dimensiones distintas.
- El compilador debe detectar ambigüedades en vez de elegir silenciosamente.
- La migración de path necesita una operación explícita, no un simple movimiento de archivo.

## Verificación futura

1. Varias declaraciones por archivo.
2. Movimiento dentro y fuera del path.
3. Declaración `using` exacta, recursiva y ambigua.
4. Resolución cualificada.
5. Colisión por mayúsculas y palabra reservada.
6. Uso ordinario de una palabra contextual fuera de su posición especial.
7. Estabilidad de anclas.
8. Separación entre `action::*`, `test::*`, `rule::*`, `family::*` y `thing::*`.
9. Lectura de un ancla mediante `~anchor` e interpolación mediante un hueco de expresión ordinario.
10. Rechazo de un `using` posterior a una declaración de primer nivel.

## Modificación vigente por D-096

D-096 introduce el módulo como dimensión semántica de visibilidad sin incorporarlo a las anclas. El MudPath nominal y las anclas existentes conservan su forma. `using` continúa resolviendo/importando nombres dentro de un `.mud`; no concede por sí solo permiso para atravesar una frontera modular, que corresponde a `uses` en `mud.module`.
