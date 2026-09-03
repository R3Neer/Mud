---
id: D-100
title: "Orden lógico, procedencia, pertenencia y consolidación de efectos"
status: current
date: 2026-08-29
supersedes: []
superseded-by: []
questions:
  - "Q-006"
  - "Q-032"
affects:
  - "aliases, colecciones, pertenencia, gramática, sintaxis, azar, efectos, ondas y conflictos"
---
# ADR-100 — Orden lógico, procedencia, pertenencia y consolidación de efectos

- Modificada por: [[ADR-103-capacidad-interior-en-valores-derivados|D-103]].

- Modificada por: [[ADR-101-bloques-de-valor-variables-locales-y-extremos|D-101]].

- Modifica: [[ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|D-019]], [[ADR-023-consolidacion-de-efectos-estructurales|D-023]], [[ADR-037-campos-y-dominios-declarativos|D-037]], [[ADR-038-familias-cerradas-de-valores|D-038]], [[ADR-039-colecciones-y-diccionarios|D-039]], [[ADR-043-consulta-especulativa-allowed|D-043]], [[ADR-046-algebra-y-conflictos-de-efectos|D-046]], [[ADR-048-azar-reproducible-y-fallos|D-048]], [[ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]], [[ADR-057-gramatica-concreta-y-continuacion|D-057]], [[ADR-064-orden-por-ruta-estable|D-064]], [[ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|D-080]], [[ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]], [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]], [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]] y [[ADR-096-modulos-callables-look-message-y-activacion|D-096]].
- Preguntas relacionadas: [[../preguntas/Q-006-conflictos|Q-006]] y [[../preguntas/Q-032-aleatoriedad-reproducible|Q-032]].

## Contexto

MUD ya distingue colecciones ordenadas y no ordenadas, efectos concurrentes calculados desde una instantánea común y una composición estructural canónica. Quedaban sin unificar la persistencia lógica del orden, la procedencia necesaria para ordenar valores sin comparador común, las transformaciones locales de colecciones, la pertenencia booleana y varias reglas de consolidación concurrente.

## Decisión

### Refinamiento heredado de campos

Un campo almacenado heredado solo puede refinar su contrato cuando es exteriormente inmutable. Un campo almacenado con `mut` exterior es invariante: su contrato no puede estrecharse ni ampliarse por especialización.

Un campo derivado heredado puede refinar su contrato. Si procede de un único miembro original conserva su expresión definitoria; el descendiente solo fortalece el contrato efectivo. Tipo, dominio, cardinalidad, `unique` y orden se admiten únicamente cuando el nuevo contrato es sustituible por todos los contratos heredados relevantes.

### Orden lógico y procedencia

El orden de una colección `ordered` forma parte de su valor lógico durante toda su existencia. No se reconstruye cuando una operación decide observarlo. Un filtrado, selección, copia, asignación, paso de valor, vista, serialización o carga que preserve orden debe transportar la misma secuencia lógica, salvo que la operación declare expresamente que elimina o sustituye ese orden.

Cada ocurrencia conserva además una procedencia estable cuando esta puede llegar a ser semánticamente relevante. La procedencia es distinta del orden lógico actual: una colección no ordenada carece de secuencia lógica, pero puede conservar procedencia de sus ocurrencias. Filtrar o retirar conserva la procedencia de las ocurrencias supervivientes; reordenar cambia la secuencia lógica y no la identidad de procedencia; una ocurrencia nueva recibe procedencia nueva. Una implementación puede omitir físicamente esta información solo cuando demuestre que nunca será observable.

Toda operación cuya semántica dependa de orden consume el orden lógico de la colección, no el orden de hash, recorrido físico o materialización. No existen prioridades de dominio especiales que reemplacen este principio.

### Transformaciones locales de colecciones

Una especificación de colección aplicada localmente a una expresión es una transformación del valor temporal. En declaraciones de valor, el contrato es verificativo y nunca transforma el valor. En declaraciones derivadas, el tipo nominal o estructural escrito se comprueba estáticamente, mientras que dominio, cardinalidad, `unique` y orden declarados en la forma derivada, exista o no tipo explícito, son coercitivos sobre el resultado y usan la misma normalización que la transformación local equivalente.

Las transformaciones locales se normalizan, con independencia del orden textual de los modificadores, en este orden:

1. restricción de dominio;
2. `unique`;
3. establecimiento o sustitución de orden;
4. cardinalidad.

La restricción local de dominio usa la forma:

```mud
people in Adults
```

y filtra los miembros que no pertenecen al dominio. `unique` elimina ocurrencias repetidas. `ordered by ruta` establece el orden por la clave indicada y usa procedencia estable para desempatar claves iguales. `ordered` usa el orden total semántico intrínseco del tipo completo cuando existe; si el tipo completo no posee un comparador total común, usa la procedencia de todas las ocurrencias. No se inventa un orden entre ramas de una unión por posición textual, nombre nominal, tag interno o identidad de implementación.

Una cota superior de cardinalidad recorta después de filtrar, deduplicar y ordenar. Una cota inferior exige que existan suficientes miembros y nunca fabrica miembros. Una transformación local no puede introducir capacidad interior `[mut]` ni otra autoridad que la expresión de origen no posea. En una forma derivada, `[mut]` es por tanto una obligación de capacidad: puede conservarse a través de transformaciones que mantengan la identidad semántica de las mismas `thing`, pero nunca se obtiene por coerción.

La escritura de una cardinalidad exacta local que sería indistinguible de una indexación conserva la indexación como forma corta; la transformación exacta puede escribirse como intervalo degenerado, por ejemplo `[2..2]`. Una especificación que contiene `unique` u `ordered` es inequívocamente una transformación.

### Pertenencia booleana

La pertenencia booleana se escribe con el contenedor a la izquierda:

```mud
inventory has Key
inventory has not BrokenKey
0..100 has score
```

`has` es palabra reservada y `has not` es la negación canónica. `in` no es un operador booleano de pertenencia: se conserva para restricciones, filtros, dominios, bindings y conversiones donde corresponda. `not in` no forma parte de la pertenencia booleana vigente.

### Inserciones concurrentes y orden de procedencia

Cuando inserciones concurrentes compatibles necesitan completar una relación de procedencia y no existe criterio semántico natural que prefiera una sobre otra, MUD usa una elección pseudoaleatoria reproducible sobre el mismo sistema de semilla semántica que los demás puntos aleatorios del lenguaje. El punto de elección posee identidad semántica estable y no depende del consumo secuencial accidental de un PRNG global, del scheduler, del orden físico de llegada, de hashes, del tiempo de máquina ni del orden fuente entre `then` concurrentes.

La elección produce una extensión lineal del orden parcial causal: respeta toda relación causal real y solo decide entre ocurrencias concurrentes. Se elige sobre el grupo concurrente completo; no se implementa mediante comparaciones aleatorias independientes por pares que puedan introducir ciclos. Una vez fijado, el resultado pasa a formar parte de la procedencia estable y no se vuelve a sortear cuando una colección se observa o se transforma posteriormente en `ordered`.

En una colección `unique`, las inserciones concurrentes equivalentes se fusionan antes de completar el orden. La ocurrencia superviviente conserva conjuntamente todas las causas, sin elegir una causa ganadora. Sobre las ocurrencias supervivientes se induce una relación causal acíclica que preserva las restricciones causales semánticamente válidas de todas las causas fusionadas; solo después se completa reproduciblemente el orden que falte. La representación o el algoritmo concreto para obtener esa relación inducida es un detalle de implementación mientras conserve esas propiedades.

### Forma normal aritmética concurrente

Los efectos aritméticos concurrentes sobre un mismo destino se normalizan en tres acumuladores:

- `Δ`: suma firmada de todos los `+=` y `-=`;
- `P`: producto de todos los factores `*=`;
- `Q`: producto de todos los divisores `/=`.

La aplicación canónica es:

```text
x' = ((x + Δ) * P) / Q
```

con identidades `Δ = 0`, `P = 1` y `Q = 1`. La familia aditiva se aplica antes que la multiplicativa. No se modela `/=` mediante un inverso obligatorio ni se introducen divisiones o redondeos intermedios derivados de un orden arbitrario entre efectos concurrentes.

Factores multiplicativos y divisivos se cancelan cuando las leyes del tipo garantizan que la cancelación preserva exactamente la semántica, incluido el caso aceptado `*= 3` junto con `/= 3`. Una simplificación no puede ocultar división por cero, overflow, incumplimientos de dominio, unidades ni otra propiedad observable. Un denominador consolidado inválido produce el fallo que corresponda a la división del tipo y la transición se revierte.

Las asignaciones concurrentes al mismo valor continúan siendo compatibles; asignaciones a valores distintos son conflicto. Una asignación mezclada con actualización aritmética continúa siendo conflicto.


### Consolidación de acumuladores locales de `for each`

Una mutable local exterior a un `for each` puede ser escrita por sus iteraciones. Si la fuente posee orden semántico, las iteraciones son secuenciales y cada una observa el valor dejado por la anterior. Si carece de orden semántico, todas parten de la misma proyección previa y sus modificaciones sobre el slot se consolidan como concurrentes mediante las mismas reglas algebraicas que los efectos equivalentes. Por ello varios `+=` compatibles pueden formar una reducción, mientras `x = x + value` produce asignaciones absolutas concurrentes y no recibe semántica especial de acumulador.

El slot sigue siendo almacenamiento del frame local, no estado del mundo; aplicar la misma álgebra no convierte la mutación local en un efecto persistente.

### Regla general de consolidación

La consolidación de efectos sigue tres niveles:

1. dentro de una misma clase se usa combinación algebraica, idempotente o normalización específica cuando esté definida;
2. entre clases distintas se usa una composición canónica del lenguaje cuando esté declarada;
3. si no existe ninguna de las anteriores, la coincidencia es conflicto.

No se deduce conflicto solo porque dos efectos parezcan expresar intenciones opuestas, ni compatibilidad por analogía con otra familia.

Para efectos estructurales concurrentes se conserva la composición canónica:

```text
create → add → remove → destroy
```

Este orden es una normalización declarativa del delta, no una secuencia temporal observable. Por ello `create X || destroy X` deja `X` ausente y `add A || remove A` deja `A` retirada. `unique` no cambia esta regla. Dentro de un único `then`, en cambio, el orden textual sí representa secuencialidad local: `destroy X; create X` termina solicitando activación y `create X; destroy X` termina solicitando destrucción. Una historia como crear, trabajar con una entidad y destruirla debe expresarse causalmente, no inferirse de efectos concurrentes independientes.

### Diagnóstico de conflictos

Un conflicto verdadero que el compilador demuestra inevitable es error estático. Si demuestra que el conflicto es posible pero no inevitable, emite warning. Si demuestra que los destinos no pueden coincidir o que los efectos consolidan de forma compatible, no emite diagnóstico de conflicto. Si un conflicto advertido o no decidible estáticamente se materializa en runtime, la resolución produce `failed` y rollback completo.

El análisis puede explotar el grafo explícito de reglas, actions, subactions, bindings, tipos, dominios, guardas y causalidad. La potencia mínima que toda implementación debe alcanzar sigue abierta.

## Consecuencias

- El parser y el AST distinguen `has`/`has not`, restricción local `in` y selección `binding in source : predicate`.
- El AST deja de representar pertenencia booleana mediante `Membership`/`NotMembership` asociados a `in`.
- Las transformaciones locales conservan una representación propia y no admiten `mut`.
- La procedencia es por ocurrencia, no solo por valor.
- El runtime debe identificar establemente los puntos aleatorios de consolidación y completar orden respetando causalidad.
- La consolidación aritmética deja de considerar conflictiva la mezcla aditiva/multiplicativa compatible y aplica la forma `(Δ, P, Q)`.
- La consolidación estructural no expone estados intermedios entre deltas concurrentes.

## Alternativas descartadas

Se descartan:

- `in` y `not in` como pertenencia booleana;
- ordenar ramas heterogéneas por orden textual, tags, nombres o identidades accidentales;
- un orden total universal entre todos los efectos concurrentes basado en fuente, anclas, hashes, productores o scheduler;
- diferir indefinidamente el orden de inserciones simultáneas hasta que una operación posterior lo observe;
- comparadores aleatorios por pares para construir el orden;
- elegir una asignación distinta ganadora mediante azar, posición fuente o prioridad implícita;
- políticas locales configurables de `latest wins`, prioridades o resolución de conflictos;
- convertir toda división concurrente en multiplicación por inversos;
- tratar automáticamente `add A || remove A` como conflicto;
- interpretar `create → add → remove → destroy` como tiempo observable;
- permitir que una transformación local fabrique capacidad `[mut]`.

## Cuestiones abiertas

Q-006 continúa parcialmente decidida. Permanecen abiertas las familias para las que todavía no se haya fijado una combinación algebraica o composición canónica concreta, incluidos los casos restantes de diccionarios, propiedades, cardinalidad estructural y write-back parcialmente solapado. También continúa sin fijarse la precisión mínima obligatoria del análisis estático de conflictos. Q-032 continúa parcialmente decidida únicamente en las reglas de caché y reintentos y en la exposición de resultados estocásticos; el algoritmo concreto de derivación o subsemillas no requiere una decisión adicional mientras preserve el contrato semántico ya fijado.

## Verificación

La conformidad deberá cubrir como mínimo:

1. refinamientos heredados que fortalecen garantías y rechazo de los que retiran capacidad;
2. persistencia del orden lógico a través de filtros, copias y asignaciones;
3. orden intrínseco de tipos totalmente ordenables y fallback de procedencia para tipos heterogéneos;
4. normalización local dominio → `unique` → orden → cardinalidad y rechazo de `[mut]` local;
5. `has` y `has not`, con rechazo de `in` como pertenencia booleana;
6. fusión previa de inserciones `unique` y extensión lineal reproducible respetuosa con causalidad;
7. forma aritmética `(Δ, P, Q)`, cancelaciones válidas y fallos preservados;
8. conflicto entre asignaciones distintas y entre asignación y aritmética;
9. composición estructural `create → add → remove → destroy` y diferencia con la secuencialidad dentro de un `then`;
10. error, warning, ausencia de diagnóstico y `failed` runtime según lo demostrable.
