---
id: D-063
title: "Firmas, `given` y vinculaciones `on` conjuntas"
status: vigente
date: 2026-07-30
supersedes: []
superseded-by: []
questions:
  - "Q-011"
  - "Q-012"
  - "Q-013"
affects:
  - "firmas, llamadas, capacidades, vinculaciones automáticas, análisis de nombres, AST, IR y diagnósticos"
---
# ADR-063 — Firmas, `given` y vinculaciones `on` conjuntas

- Modifica: [[notas/decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|D-019]], [[notas/decisiones/ADR-036-participantes-receptores-y-llamadas|D-036]], [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]] y [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|D-057]]
- Amplía: [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]]
- Cierra de nuevo: [[notas/preguntas/Q-011-vinculacion-nombrada-de-participantes|Q-011]], [[notas/preguntas/Q-012-valores-given-nombrados|Q-012]] y [[notas/preguntas/Q-013-restricciones-relacionales-entre-participantes-on|Q-013]]
- Documentos afectados: firmas, llamadas, capacidades, vinculaciones automáticas, análisis de nombres, AST, IR y diagnósticos

## Contexto

MUD separa los sujetos de una operación, declarados mediante `for`, de sus parámetros auxiliares `given`. La vinculación posicional original de `given` impedía omitir un valor predeterminado intermedio y trataba `nombre = expresión` como una etiqueta que no vinculaba por nombre.

Las cabeceras `on` relacionadas también se resolvían de izquierda a derecha. Esa restricción impedía expresar relaciones simétricas o cíclicas aunque el mundo activo y todas las colecciones observadas fueran finitos:

```mud
rule MutualFriends on
    alice in bob.friends,
    bob in alice.friends
{
    ...
}
```

## Decisión

### Valores `given`

Todo `given` tiene nombre obligatorio, es de solo lectura y puede declarar un valor predeterminado estático:

```mud
given
    origin: Square = Capital,
    depth: Nat,
    exhaustive: Bool = false
```

Un `given` no admite mutabilidad exterior ni capacidad interior `mut`. Si una acción necesita escribir la colección suministrada o el estado de una `thing` recibida, ese valor constituye un sujeto de la operación y debe declararse mediante `for`.

La anotación de un `given` admite la expresión general de tipo, incluidos tipos diccionario exactos y decisionales. Por ejemplo, `given prices: Product -> Money` es válido. La posibilidad de escribir un diccionario no concede capacidad: todas sus colecciones y valores siguen sometidos a la prohibición anterior de `mut` en `given`.

El predeterminado:

- Es una expresión estática cerrada, pura y determinista.
- No puede consultar participantes, otros `given`, valores locales ni estado del mundo.
- Puede usar literales, valores nominales conocidos estáticamente y operaciones entre constantes.
- Se elabora con el tipo esperado y debe satisfacer el dominio y la especificación de colección del `given`.

Los `given` con predeterminado pueden aparecer en cualquier posición de la firma.

### Argumentos posicionales y nombrados

Una llamada puede usar:

1. Argumentos exclusivamente posicionales.
2. Un prefijo posicional seguido por argumentos nombrados.
3. Argumentos exclusivamente nombrados.

Después del primer argumento nombrado no puede aparecer uno posicional.

Los argumentos posicionales vinculan los `given` aún no vinculados en orden de declaración. Solo puede omitirse posicionalmente un sufijo completo cuyos `given` tengan predeterminado.

Un argumento `nombre = expresión` realiza vinculación nominal real. Puede:

- Vincular cualquier `given` todavía no vinculado.
- Omitir un `given` intermedio que tenga predeterminado.
- Aparecer en un orden distinto al de la firma.

No puede repetir un nombre ni usar uno desconocido. Al terminar la llamada, todo `given` sin predeterminado debe estar vinculado exactamente una vez.

La forma desordenada es válida, pero el compilador sugiere ordenar los argumentos nombrados según la declaración:

```mud
game.Search(depth = 3, origin = Capital)
```

se sugiere como:

```mud
game.Search(origin = Capital, depth = 3)
```

La sugerencia conserva exactamente la vinculación y no se emite cuando el orden ya es canónico.

### Receptores `for`

Todo rol `for` tiene identificador fuente explícito, incluida cardinalidad `[1]`, conforme a D-087. La firma conserva el orden de declaración, pero ese orden no sustituye a la identidad estable del slot.

La forma de receptor multiparte nombrado continúa siendo exacta, exhaustiva y no mezclable con posiciones. Puede reordenar roles, pero el compilador sugiere el orden de declaración. La declaración de la firma nunca contiene participantes anónimos.

### Capacidad interior inútil

La capacidad interior `[mut]` expresa permiso, no la garantía de que el tipo ofrezca estado modificable. Por tanto, escribirla sobre una colección o un diccionario cuyos valores efectivos sean básicos, aliases, miembros de `family` u otros valores inmutables es legal.

Cuando el análisis pueda demostrar que ningún valor accesible mediante esa capacidad puede ser mutable, el compilador emite una sugerencia para retirar `[mut]`. No es un aviso: el programa es correcto, no existe riesgo y la retirada conserva su comportamiento efectivo.

En un diccionario:

- El `mut` exterior permite crear o retirar asociaciones y sustituir el valor de una clave existente.
- `[mut]` concede capacidad exclusivamente sobre valores `thing` materialmente asociados.
- Nunca concede capacidad sobre las claves.
- No atraviesa aliases ni contenedores anidados y no introduce mutabilidad profunda.
- Una lectura de clave ausente produce `empty` con la forma declarada y no concede capacidad interior como si existiera una asociación.

Cada nivel anidado conserva sus propias capacidades.

### Cabeceras `on` conjuntas

Los nombres declarados en una cabecera `on` son visibles en toda la cabecera, incluso antes de su posición textual. La elaboración ocurre en dos fases:

1. Se recogen los roles, nombres, anotaciones y restricciones.
2. Se resuelven conjuntamente sus tipos y dominios.

Un participante relacionado admite una anotación que refine nominalmente los miembros de la colección:

```mud
alice: Person in bob.friends
```

La anotación no declara el tipo de `bob.friends`. Exige que `alice` satisfaga simultáneamente el tipo de miembro de esa colección y `is Person`. Así puede seleccionar una especialización dentro de una colección declarada con una raíz más general.

Las restricciones de tipo de toda la cabecera deben poseer una solución nominal única. Si existen varias soluciones o ninguna, el programa es inválido y debe añadir anotaciones suficientes.

### Universo y conjunto de vinculaciones

`on` vincula un valor individual por rol. En una forma directa sin `in`, el universo del rol es el conjunto finito de `thing` concretas y activas de la instantánea leída que satisfacen su tipo efectivo. En una forma relacionada `nombre[: Tipo] in fuente`, el universo procede de los miembros de esa fuente finita enumerable y la anotación opcional actúa como refinamiento. Un tipo sin universo implícito finito, por ejemplo `Nat`, no puede usar la forma directa.

Sea `r_1,\ldots,r_n` el orden textual de los roles y sean `U_1,\ldots,U_n` sus universos así obtenidos. La cabecera denota el conjunto:

$$
B
=
\{
(v_1,\ldots,v_n)\in U_1\times\cdots\times U_n
\mid
\text{todas las restricciones relacionales son verdaderas}
\}.
$$

Las restricciones se interpretan conjuntamente. Una pertenencia repetida por multiplicidad no duplica una misma asignación de roles.

Esta definición es un join relacional finito, no un punto fijo. La implementación puede usar productos filtrados, índices, joins u otra estrategia siempre que produzca el mismo conjunto.

Un ciclo de restricciones no constituye un ciclo de cálculo:

```mud
a in b.neighbours,
b in c.neighbours,
c in a.neighbours
```

Todas las colecciones se leen en la misma instantánea de inicio. Los efectos no alteran retroactivamente las vinculaciones de la onda; pueden producir vinculaciones distintas en la siguiente. Los ciclos entre campos calculados continúan sometidos a sus reglas propias y no se legitiman por aparecer en `on`.

### Identidad, orientación y orden técnico

Una vinculación es una asignación total de roles. No se impone desigualdad implícita: dos roles pueden recibir el mismo valor si satisfacen sus restricciones.

Los roles también conservan orientación. Si una relación simétrica admite tanto `(Alice, Bob)` como `(Bob, Alice)`, ambas son vinculaciones distintas. MUD no deduplica parejas por simetría ni presupone que el cuerpo trate los roles de igual manera.

Semánticamente, las vinculaciones de una onda forman un conjunto y su orden no decide los efectos. Cuando todos los valores vinculados son `thing`, el orden técnico reproducible ya definido por anclas continúa disponible para trazas y diagnósticos; D-096 no convierte esa convención técnica en un orden semántico de los valores `on` generales.

## Consecuencias

- Las etiquetas de `given` pasan a ser vinculaciones nominales.
- Añadir un `given` con predeterminado puede conservar llamadas anteriores.
- Los predeterminados no introducen dependencias entre parámetros.
- `given` no transporta ninguna capacidad de escritura.
- Los ciclos de `on` son restricciones finitas y no evaluación recursiva.
- AST e IR conservan predeterminados, modo de vinculación, orden escrito, orden canónico sugerido, refinamientos nominales y el conjunto resuelto de restricciones.
- El análisis de capacidades distingue asociación presente de lectura predeterminada de una clave ausente.

## Verificación

1. `given` con predeterminado inicial, intermedio y final.
2. Omisión posicional exclusiva de un sufijo predeterminado.
3. Omisión nominal de un predeterminado intermedio.
4. Prefijo posicional seguido de nombres y rechazo de una posición posterior.
5. Rechazo de argumento repetido, desconocido o requerido ausente.
6. Sugerencia de orden canónico en argumentos y receptores nombrados.
7. Rechazo de ambos `mut` en `given`.
8. Sugerencia, no aviso ni error, para `[mut]` demostrablemente inútil.
9. Escritura exterior de colecciones y diccionarios de valores inmutables mediante `for mut`.
10. Capacidad interior sobre valores `thing` presentes y ausencia de capacidad sobre claves, aliases, niveles anidados o valores predeterminados de claves ausentes.
11. Referencia adelantada entre roles `on`.
12. Refinamiento `role: Type in expression`.
13. Join acíclico, ciclo de dos roles y ciclo de tres roles.
14. Rechazo de inferencia nominal ambigua.
15. Universo implícito de `thing` concretas y activas para `on` directo y fuente finita enumerable para `on ... in fuente`, incluido rechazo de un tipo sin universo implícito finito.
16. Conservación de dos orientaciones simétricas y de una vinculación reflexiva permitida.

## Modificación vigente por D-096

`on` conserva su papel de binding automático y no absorbe las ocurrencias de `message`: la causalidad de messages/rules pertenece a `when`. D-096 amplía la forma relacionada `nombre[: Tipo] in fuente` a valores procedentes de una fuente finita enumerable. La forma directa sin `in` sigue seleccionando identidades `thing` del universo implícito.
