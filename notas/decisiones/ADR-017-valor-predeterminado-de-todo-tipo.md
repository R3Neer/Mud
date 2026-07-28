# ADR-017 — Todo tipo bien formado tiene valor predeterminado

- Estado: Vigente
- Fecha: 2026-07-27
- Pregunta abierta relacionada: [[notas/08-preguntas-abiertas#Q-047 — Selección de predeterminados por tipo|Q-047]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], futuro `10-sistema-de-tipos.md`, futuro `14-campos.md`

## Contexto

MUD permite declarar propiedades sin escribir siempre un inicializador explícito. La semántica necesita determinar su valor inicial sin introducir ausencia implícita ni dejar posiciones obligatorias sin valor.

## Decisión

Todo tipo bien formado posee un valor predeterminado perteneciente a su dominio semántico.

Sea $\mathcal T_P$ el conjunto de tipos bien formados de un programa resuelto y sea $\mathcal V_P$ su universo de valores. Existe una función total:

$$
\operatorname{default}_P:
\mathcal T_P
\to
\mathcal V_P
$$

tal que:

$$
\forall\tau\in\mathcal T_P:
\operatorname{default}_P(\tau)
\in
\llbracket\tau\rrbracket_P
$$

Por tanto, todo tipo bien formado es habitable:

$$
\forall\tau\in\mathcal T_P:
\llbracket\tau\rrbracket_P
\neq
\varnothing
$$

Una construcción de tipos cuyo dominio fuese vacío no podría aceptarse como tipo bien formado.

## Casos ya fijados

Los casos básicos, actualizados por D-028, son:

| Tipo o familia | Valor predeterminado |
| --- | --- |
| `Bool` | `false` |
| `Natural` | `0` |
| `Integer` | `0` |
| `Number` | `0` |
| `Rumber` | `r0` |
| `Text` | `""` |
| `Money` | `0` en contexto `Money` |
| Colecciones | `empty` |
| Diccionarios | `empty` |
| Intervalos | `empty` |

Estos casos no resuelven por sí solos tipos refinados que excluyan el valor base ni colecciones cuya cardinalidad mínima sea positiva.

## Precedencia durante la inicialización

Para una propiedad almacenada, el valor inicial se obtiene en este orden conceptual:

1. Predeterminado explícito efectivo de la propiedad, si existe.
2. Valor predeterminado de su tipo efectivo, en otro caso.
3. Asignación o inicialización explícita de la creación, cuando la sintaxis correspondiente la permita.

La tercera fase sustituye el valor inicial de esa creación; no modifica por ello el predeterminado heredable de la propiedad ni el del tipo.

## Consecuencias

- Una propiedad almacenada obligatoria puede inicializarse aunque omita un predeterminado explícito.
- Los refinamientos, intervalos, familias, aliases, colecciones y tipos que dependan de `thing` deben definir cómo obtienen un elemento distinguido de su dominio.
- La comprobación de buena formación debe garantizar que el predeterminado satisface todas las restricciones del tipo.
- Los materializadores deben reproducir el valor de MUD y no elegir predeterminados propios de la tecnología destino.

## Cuestiones abiertas

Q-047 determinará:

- Los valores de los tipos primitivos todavía no enumerados.
- La regla composicional para aliases, tipos estructurados y colecciones restringidas.
- La selección dentro de intervalos, familias cerradas y refinamientos.
- El tratamiento de tipos cuyo dominio pueda depender del mundo activo.
- Si una declaración puede reemplazar el predeterminado intrínseco de un tipo derivado.

## Verificación futura

La suite deberá comprobar:

1. Existencia y pertenencia al dominio del predeterminado de cada tipo conforme.
2. Rechazo de tipos con dominio vacío.
3. Uso del predeterminado del tipo cuando una propiedad no declara otro.
4. Prioridad del predeterminado explícito de propiedad.
5. Prioridad final de una inicialización explícita de creación.
6. Independencia respecto a los valores predeterminados de la tecnología materializada.
