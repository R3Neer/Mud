# ADR-037 — Campos y dominios declarativos

- Estado: Vigente
- Fecha: 2026-07-28
- Amplía: D-019, D-026
- Preguntas relacionadas: Q-003, Q-017
- Documentos afectados: futuro `14-campos-y-mutabilidad.md`, futuro `17-dominios-e-intervalos.md`, futuro `30-restricciones-finales.md`

## Decisión

### Clases de campo

```mud
name: Text = ""
mut treasury: Money = 0
age: Natural in 0..150 [1] = 18
subjects: Person [* unique]
maintenanceCost := soldiers * 2
displayCost: Money := maintenanceCost
```

- `=` introduce carga almacenada.
- `:=` introduce una expresión calculada y pura.
- `mut` concede mutabilidad exterior conforme a D-019.
- Todo campo denota una colección conforme a D-026; omitir cardinalidad equivale a `[1]`.

La forma concreta de un campo almacenado es:

```text
[mut] nombre : tipo [in dominio] [especificación-de-colección] [= valor]
```

El dominio precede a la especificación de colección. Un campo calculado usa exclusivamente:

```text
nombre [ : tipo ] := expresión
```

La anotación de tipo es opcional. Si se omite, el compilador infiere el tipo estático de la expresión; si se escribe, la expresión debe ser compatible con él y la anotación puede aportar el tipo esperado necesario para elaborar literales contextuales. Cuando una expresión sin anotación no tiene un tipo inferible de forma unívoca, la declaración es un error estático y debe escribirlo.

El campo calculado siempre conserva en el IR un tipo estático resuelto, haya sido declarado o inferido. No posee carga asignable y no admite `mut`, una cláusula `in` ni una especificación de colección. La cardinalidad y demás propiedades de colección de su resultado proceden del tipo estático de la expresión, no de una segunda restricción escrita en la declaración.

### Dominios

`in` restringe valores admisibles:

```mud
age: Natural in 0..150
given amount: Natural in 1..100
```

Puede aparecer en campos, componentes de alias y `given`. Un dominio calculado debe ser puro, determinista, no estocástico, analizable y libre de ciclos inválidos.

En un campo almacenado, `in` aparece después del tipo y antes de la especificación de colección:

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
