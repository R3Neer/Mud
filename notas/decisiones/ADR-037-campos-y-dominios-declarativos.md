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

- Modificada por: [[ADR-103-capacidad-interior-en-valores-derivados|D-103]].

- Modificada por: [[ADR-101-bloques-de-valor-variables-locales-y-extremos|D-101]].

- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]
- Amplía: D-019, D-026
- Modificada por: [[ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].
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
- Todo campo denota una colección conforme a D-026. En un campo almacenado inmutable con inicializador, una cardinalidad omitida se infiere de la forma exterior exacta del valor conforme a D-085; en un campo exteriormente mutable conserva `[1]`.
- `~name` pertenece al espacio de metadatos de D-087. Un campo ordinario llamado `name` pertenece al espacio de miembros y no lo oculta.

La forma concreta de un campo almacenado es:

```text
[mut] nombre : tipo [in dominio] [especificación-de-colección] [= value-body]
```

El dominio precede a la especificación de colección. Un campo calculado usa:

```text
nombre [ forma-derivada ] := value-body
```

donde la forma derivada puede declarar tipo y, conforme a D-075, dominio, cardinalidad y modificadores de colección compatibles con el resultado.

El `mut` exterior pertenece al lugar almacenado y por eso precede al nombre; no es un constructor ni un calificador del tipo. La forma `nombre: mut tipo` es inválida.

El valor explícito de un campo almacenado puede ser una expresión breve o un `ValueBlock`, pero el cuerpo completo debe ser evaluable estáticamente conforme a D-066 y D-101. Puede usar almacenamiento temporal interno si no introduce dependencias runtime ni efectos exteriores. Un campo calculado admite igualmente `ValueBlock` sin adquirir almacenamiento persistente propio.

La anotación de tipo es opcional. Si se omite, el compilador infiere el tipo estático de la expresión; si se escribe, la expresión debe ser compatible con él y la anotación puede aportar el tipo esperado necesario para elaborar literales contextuales. Cuando una expresión sin anotación no tiene un tipo inferible de forma unívoca, la declaración es un error estático y debe escribirlo.

La inferencia no aplica una prioridad predeterminada entre interpretaciones compatibles. Esto incluye tanto la representación de literales numéricos como las formas contextuales compartidas. Por ejemplo, `[3]` puede elaborar una colección unitaria o el intervalo unitario `[3..3]`: ambas formas se conservan y una declaración calculada sin contexto que permita elegir una sola debe anotar su tipo. La omisión está pensada para los usos comunes en los que las operaciones y dependencias de la expresión determinan un único tipo, no para garantizar que toda expresión aislada sea inferible.

El campo calculado siempre conserva en el IR un tipo estático resuelto, haya sido declarado o inferido. No posee carga asignable ni admite `mut` exterior. El tipo nominal o estructural explícito se comprueba estáticamente. Dominio, cardinalidad, `unique` y orden declarados en la forma derivada, exista o no tipo explícito, son coercitivos: transforman el resultado con la misma semántica y normalización que las transformaciones locales equivalentes. `[mut]` no es una coerción creadora de autoridad: actúa como obligación de capacidad y solo se satisface cuando el resultado de origen ya la garantiza a través de transformaciones que preservan la identidad semántica de las `thing` miembros.

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

Los campos calculados deben satisfacer tanto el dominio de su tipo estático como cualquier dominio `in` declarado en su forma derivada. Ese dominio puede ser explícito o derivarse conforme a D-075.

### Puntos de control

Los dominios se preservan en inicialización, materialización, especialización, escrituras, raíces, ondas y estados publicables. Q-003 deberá expresar estos puntos mediante una única semántica operacional y decidir qué estados tentativos internos pueden existir sin ser observables.

La excepción de estados intermedios concedida por D-026 se refiere a cardinalidad dentro del delta privado de un `then`; no elimina la obligación final de dominio.

### Significados contextuales de `in`

El parser y el AST distinguen:

- Restricción declarativa de dominio.
- Restricción local o filtrado de una expresión por dominio.
- Binding de selección.
- Participante relacionado.
- Unidad de presentación de una magnitud.

`in` no expresa pertenencia booleana; esa operación usa `has` y `has not`. Compartir token entre los usos restantes de `in` no fusiona sus significados.

## Consecuencias

- Los dominios forman parte del tipo refinado y del grafo de dependencias.
- La validación de entradas se separa de `if`.
- Una escritura inválida nunca publica estado parcial.
- Los dominios finitos alimentan interfaces, tests, enumeración y `eventually`.

## Verificación futura

1. Dominio constante y calculado.
2. `given` fuera de dominio en regla y action.
3. Campo almacenado fuera de dominio y `in` válido sobre un campo calculado conforme a su forma derivada.
4. Ciclo y dependencia estocástica inválidos.
5. Campo calculado con tipo declarado, inferido y no inferible unívocamente.
6. Rechazo de `mut` exterior y de `[mut]` como autoridad fabricada en campos calculados; aceptación de `[mut]` cuando el origen garantiza la capacidad, y de `in`, cardinalidad, `unique` y orden como coerciones derivadas.
7. Rollback sin estado publicable inválido.
8. Literal contextual `[3]` resuelto por tipo esperado y rechazado sin una inferencia unívoca.
9. Sugerencia de campo almacenado para un cálculo demostrablemente invariante y ausencia de sugerencia cuando dependa de estado cambiante.
10. Inferencia de cardinalidad, dominio y modificadores en un campo calculado mediante operadores de colección.
11. Expresión estática compuesta como valor almacenado y rechazo de dependencias runtime.
12. Rol `for` individual o colectivo restringido por dominio.

## Modificación por D-084

Los aliases estructurales admiten campos derivados y sobrescrituras de predeterminados heredados. Sus formas derivadas siguen la distinción vigente entre anotación verificativa y coerciones de dominio/colección; una coerción no puede fabricar capacidad `[mut]`.
