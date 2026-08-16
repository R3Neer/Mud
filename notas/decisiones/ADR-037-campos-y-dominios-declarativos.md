---
id: D-037
title: "Campos y dominios declarativos"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-003"
  - "Q-017"
  - "Q-061"
affects:
  - "futuro `14-campos-y-mutabilidad.md`, futuro `17-dominios-e-intervalos.md`, futuro `30-restricciones-finales.md`"
---
# ADR-037 — Campos y dominios declarativos

- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]
- Amplía: D-019, D-026
- Modificada por: [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]]
- Modificada por: [[notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco|D-068]]
- Ampliada por: [[ADR-075-dominios-enumerables-all-y-valores-derivados|D-075]]
- Preguntas relacionadas: Q-003, Q-017
- Documentos afectados: futuro `14-campos-y-mutabilidad.md`, futuro `17-dominios-e-intervalos.md`, futuro `30-restricciones-finales.md`

## Decisión

### Clases de campo

```mud
title: Text = ""
mut treasury: Money = 0
age: Nat in 0..150 [1] = 18
subjects: Person [* unique]
maintenanceCost := soldiers * 2
displayCost: Money := maintenanceCost
```

- `=` introduce carga almacenada.
- `:=` introduce una expresión calculada y pura.
- `mut` concede mutabilidad exterior conforme a D-019.
- Todo campo denota una colección conforme a D-026; omitir cardinalidad equivale a `[1]`.
- Dentro de una `thing`, `name` designa la propiedad intrínseca fijada por D-068 y no puede declararse como campo ordinario.

La forma concreta de un campo almacenado es:

```text
[mut] nombre : tipo [in dominio] [especificación-de-colección] [= expresión-estática]
```

El dominio precede a la especificación de colección. Un campo calculado usa exclusivamente:

```text
nombre [ : tipo ] := expresión
```

El `mut` exterior pertenece al lugar almacenado y por eso precede al nombre; no es un constructor ni un calificador del tipo. La forma `nombre: mut tipo` es inválida.

El valor explícito de un campo almacenado es una expresión estática cerrada conforme a D-066. Puede combinar literales, valores nominales y operaciones constantes, pero no consultar estado, participantes, `given`, locales ni actividad del mundo. Se evalúa y normaliza durante la compilación.

La anotación de tipo es opcional. Si se omite, el compilador infiere el tipo estático de la expresión; si se escribe, la expresión debe ser compatible con él y la anotación puede aportar el tipo esperado necesario para elaborar literales contextuales. Cuando una expresión sin anotación no tiene un tipo inferible de forma unívoca, la declaración es un error estático y debe escribirlo.

La inferencia no aplica una prioridad predeterminada entre interpretaciones compatibles. Esto incluye tanto la representación de literales numéricos como las formas contextuales compartidas. Por ejemplo, `[3]` puede elaborar una colección unitaria o el intervalo unitario `[3..3]`: ambas formas se conservan y una declaración calculada sin contexto que permita elegir una sola debe anotar su tipo. La omisión está pensada para los usos comunes en los que las operaciones y dependencias de la expresión determinan un único tipo, no para garantizar que toda expresión aislada sea inferible.

El campo calculado siempre conserva en el IR un tipo estático resuelto, haya sido declarado o inferido. No posee carga asignable ni admite `mut` exterior. Puede declarar tipo, dominio y especificación de colección —incluida capacidad interior `[mut]`— como contrato comprobado sobre el resultado. La anotación no transforma la expresión ni crea miembros.

Por ejemplo, si `leftChars` tiene tipo `Char [1..5]` y `rightChars` tiene tipo `Char [0..2]`, `combinedChars := leftChars | rightChars` infiere `Char [1..7]` conforme al álgebra de D-039. El resultado no adquiere modificadores que las reglas de propagación no puedan garantizar.

Cuando el contexto de declaración también admita un campo almacenado y la expresión calculada sea estática cerrada, el compilador debe sugerir la forma almacenada inmutable equivalente. La sugerencia es conservadora, no cambia la validez del programa y no autoriza una reescritura automática. No procede si la expresión depende de estado o si almacenarla alteraría sus dependencias o su momento de evaluación.

### Dominios

`in` restringe valores admisibles:

```mud
age: Nat in 0..150
given amount: Nat in 1..100
for people: Person in EligibleCitizens [1..* unique]
```

Puede aparecer en campos, componentes de alias, roles `for` y `given`. Un dominio calculado debe ser puro, determinista, no estocástico, analizable y libre de ciclos inválidos.

En un campo almacenado o un rol `for`, `in` aparece después del tipo y antes de la especificación de colección:

```mud
citizens: Person in EligibleCitizens [1..* unique]
```

La semántica del tipo y las conversiones explícitas se aplican antes de comprobar pertenencia al dominio.

### Resultados por contexto

- `given` fuera de dominio al solicitar una action: `rejected` antes de evaluar `if`, raíz u ondas.
- `given` fuera de dominio al consultar una regla booleana: resultado `false`; si es constante, puede diagnosticarse estáticamente.
- Campo fuera de dominio en un estado candidato: la resolución resulta `failed` y revierte.
- Inicializador constante fuera de dominio: error estático.

Los campos calculados también deben satisfacer el dominio de su tipo estático cuando se evalúan, aunque no puedan declarar una cláusula `in` adicional.

### Puntos de control

Los dominios se preservan en inicialización, materialización, especialización, escrituras, raíces, ondas y estados publicables. Q-003 deberá expresar estos puntos mediante una única semántica operacional y decidir qué estados tentativos internos pueden existir sin ser observables.

La excepción de estados intermedios concedida por D-026 se refiere a cardinalidad dentro del delta privado de un `then`; no elimina la obligación final de dominio.

### Significados contextuales de `in`

El parser y el AST distinguen:

- Restricción de dominio.
- Pertenencia booleana.
- Participante relacionado.
- Unidad de presentación de una magnitud.

Compartir token no fusiona sus significados.

## Consecuencias

- Los dominios forman parte del tipo refinado y del grafo de dependencias.
- La validación de entradas se separa de `if`.
- Una escritura inválida nunca publica estado parcial.
- Los dominios finitos alimentan interfaces, tests, enumeración y `eventually`.

## Verificación futura

1. Dominio constante y calculado.
2. `given` fuera de dominio en regla y action.
3. Campo almacenado fuera de dominio y rechazo de `in` sobre un campo calculado.
4. Ciclo y dependencia estocástica inválidos.
5. Campo calculado con tipo declarado, inferido y no inferible unívocamente.
6. Rechazo de `mut` y de especificaciones de colección en campos calculados.
7. Rollback sin estado publicable inválido.
8. Literal contextual `[3]` resuelto por tipo esperado y rechazado sin una inferencia unívoca.
9. Sugerencia de campo almacenado para un cálculo demostrablemente invariante y ausencia de sugerencia cuando dependa de estado cambiante.
10. Inferencia de cardinalidad, dominio y modificadores en un campo calculado mediante operadores de colección.
11. Expresión estática compuesta como valor almacenado y rechazo de dependencias runtime.
12. Rol `for` individual o colectivo restringido por dominio.

## Modificación por D-084

Los aliases estructurales admiten campos derivados y sobrescrituras de predeterminados heredados. Los derivados pueden declarar una forma colectiva como `wounded [* mut] := ...`. La capacidad interior pertenece al campo derivado y no depende de la fuente.
