# ADR-035 — Organización, nombres, imports y anclas

- Estado: Vigente
- Fecha: 2026-07-28
- Preguntas relacionadas: Q-001, Q-014, Q-054
- Documentos afectados: futuro `05-modelo-de-programa.md`, futuro `06-lexico.md`, futuro `09-nombres-y-anclas.md`

## Decisión

### Archivos y namespaces

El namespace se deriva de la ruta relativa dentro de la raíz MUD y no se declara en el archivo. Un archivo puede contener imports y varias declaraciones de cualquier categoría.

El archivo es una unidad física, no una unidad de identidad semántica. Cada declaración conserva por separado ancla, dependencias, nodo de grafo, procedencia e historial.

Mover una declaración entre archivos del mismo namespace no cambia su ancla. Moverla a otro namespace sí la cambia, salvo una migración explícita todavía definida por Q-014.

### Imports

Se admiten imports exactos y recursivos:

```mud
import warfare.armies
import warfare.armies.*
```

Para un nombre no cualificado, la búsqueda sigue:

1. Declaraciones locales.
2. Mismo namespace.
3. Imports exactos.
4. Imports recursivos.

Una referencia completamente cualificada se resuelve directamente. Si dos candidatos importados proporcionan el mismo nombre no cualificado, existe ambigüedad y debe escribirse el nombre cualificado.

El orden textual de archivos e imports no decide empates.

### Convenciones de identificadores

- Namespace: segmentos `lowerCamelCase` separados por puntos.
- Declaraciones nominales (`thing`, alias, magnitude, rule, action, look, message y familias): `PascalCase`.
- Campos, componentes, roles, `given` y variables de iteración: `lowerCamelCase`.

Los identificadores son sensibles a mayúsculas. El catálogo de palabras reservadas no puede usarse como nombre de campo, componente, rol, `given`, variable local o declaración.

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
magnitude::physics.Length
rule::warfare.armies.IsDestroyed
action::warfare.armies.Recruit
look::warfare.armies.Summary
message::warfare.armies.Destroyed
```

Una ancla es globalmente única, sensible a mayúsculas y estable frente a movimientos dentro del mismo namespace. Se utiliza en el grafo, IR, consultas, diagnósticos, trazabilidad y operaciones semánticas.

La identidad estable de una unidad sin identificador de cabecera permanece en Q-054.

## Consecuencias

- La resolución de nombres no depende del orden de archivos.
- La procedencia física y la identidad semántica son dimensiones distintas.
- El compilador debe detectar ambigüedades en vez de elegir silenciosamente.
- La migración de namespace necesita una operación explícita, no un simple movimiento de archivo.

## Verificación futura

1. Varias declaraciones por archivo.
2. Movimiento dentro y fuera del namespace.
3. Import exacto, recursivo y ambiguo.
4. Resolución cualificada.
5. Colisión por mayúsculas y palabra reservada.
6. Estabilidad de anclas.
