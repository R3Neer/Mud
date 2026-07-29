---
id: D-059
title: "Intervalos de magnitud y extremos invertidos"
status: vigente
date: 2026-07-29
supersedes: []
superseded-by: []
questions:
  - "Q-018"
affects:
  - "[[especificacion/07-gramatica-concreta]], `especificacion/gramatica/mud.ebnf`"
---
# ADR-059 — Intervalos de magnitud y extremos invertidos

- Modifica: [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos|D-029]], [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]] y [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|D-057]]
- Relacionada con: [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]]
- Preguntas relacionadas: Q-018
- Documentos afectados: [[especificacion/07-gramatica-concreta]], `especificacion/gramatica/mud.ebnf`

## Contexto

Los extremos de un intervalo pueden ser literales o expresiones ya tipadas. Exigir una unidad en cada literal resulta repetitivo cuando todos comparten unidad:

```mud
[1 m..5 m]
```

Sin embargo, eliminar las unidades locales impediría intervalos con presentaciones distintas y casos mixtos:

```mud
[1 m..5 km]
[minimumDistance..5 m]
```

También faltaba fijar qué significa un intervalo lineal cuyos extremos dependen del estado y pasan a aparecer en orden inverso.

## Decisión

### Dos formas de aportar unidades

Un intervalo de magnitud admite unidades locales en sus extremos:

```mud
[1 m..5 m]
[1 m..5 km]
[minimumDistance..5 m]
[1 km..maximumDistance]
[minimumDistance..maximumDistance]
```

Cada extremo finito es una expresión ordinaria. Tras resolver nombres y tipos, ambos extremos deben pertenecer a la misma magnitud y usar representaciones numéricas compatibles. Las cantidades se normalizan a la unidad canónica de esa magnitud antes de compararlas.

Cuando todos los extremos finitos escritos son literales numéricos sin unidad, una única expresión de unidad puede seguir al intervalo:

```mud
[1..5] m
1..5 m
[1..5) km
[*..5] m
[1] m
[] m
```

La unidad exterior se distribuye sobre todos los extremos finitos. Las formas anteriores se elaboran respectivamente como intervalos de cantidades, y `[] unit` produce directamente el intervalo vacío de la magnitud identificada por `unit`.

La forma cerrada sin delimitadores conserva el azúcar de D-029. En particular:

```mud
1..5 m
```

se agrupa como:

```text
(1..5) m
```

y no como `1..(5 m)`.

La unidad exterior no completa intervalos mixtos ni intervalos cuyos extremos sean expresiones:

```mud
[minimumDistance..5] m   # inválido
[minimumDistance..5 m]   # válido
[1 m..5 m] m             # inválido
```

Un literal numérico situado junto a una expresión de magnitud debe llevar su propia unidad. Dentro de una forma delimitada, una unidad escrita antes del cierre pertenece únicamente a ese extremo:

```mud
[1..5 m]                 # inválido: Number frente a Length
[1 m..5 m]               # válido
```

### Forma preferida

Cuando todos los extremos finitos son literales escritos en la misma unidad, la serialización canónica usa una sola unidad exterior:

```mud
[1..5] m
```

La forma repetida `[1 m..5 m]` continúa siendo válida. Las unidades locales son necesarias para conservar presentaciones distintas como `[1 m..5 km]` y para combinar literales con expresiones ya tipadas.

La separación léxica ordinaria entre número y unidad se conserva: las formas canónicas son `1 m` y `5 km`.

### Normalización de intervalos lineales

Sea $l$ el límite inferior efectivo y sea $u$ el límite superior efectivo de un intervalo lineal, después de evaluar expresiones y normalizar unidades.

- Si $l<u$, el intervalo conserva sus extremos abiertos o cerrados.
- Si $l=u$ y ambos lados son cerrados, el resultado es el intervalo unitario.
- Si $l=u$ y algún lado es abierto, el resultado es `empty`.
- Si $l>u$, el resultado es `empty`.

Estas reglas fijan la normalización por orden de extremos. No excluyen otros intervalos vacíos por contenido; por ejemplo, un tipo discreto puede no contener ningún valor entre dos extremos abiertos consecutivos.

La inversión no denota recorrido descendente ni envoltura. El posible orden descendente de enumeración permanece separado en Q-018.

Construir `empty` de esta manera es una operación válida y total. Un campo calculado cuyos extremos se crucen pasa a denotar el intervalo vacío; el cruce no es por sí mismo un error de evaluación.

### Interacción con acciones y restricciones

Una acción no produce `failed` por el mero hecho de que un intervalo evaluado durante su resolución se vuelva vacío.

El resultado depende del uso posterior:

- un `given` que no pertenezca al intervalo vacío produce `rejected`;
- un `if` que compruebe pertenencia en él puede resultar falso y producir `rejected`;
- un `after` que exija que no esté vacío y resulte falso produce `rejected`;
- si el intervalo forma un dominio y deja un valor almacenado fuera de dominio, el estado tentativo es inválido y produce `failed`;
- si provoca el incumplimiento de una regla `always`, produce `failed`.

Un error real al evaluar un extremo —por ejemplo, una referencia inválida— conserva la taxonomía ordinaria de fallos y no se convierte en `empty`.

### Ciclos

La normalización a `empty` se aplica a intervalos lineales. No introduce semántica cíclica implícita.

La forma `[a..b cycle)` de D-029 continúa siendo exclusiva del dominio de una magnitud de punto. Debe definir un periodo estrictamente positivo y conserva sus límites numéricos desnudos en la representación canónica; las nuevas unidades locales o exteriores no se admiten en esa cabecera.

## Consecuencias

- El AST distingue intervalos con extremos ordinarios de intervalos numéricos con unidad compartida.
- `[] unit` aporta tipo de magnitud al intervalo vacío sin depender de un contexto exterior.
- La elaboración de `1..5 unit` debe resolver la unidad como común al intervalo completo.
- La normalización de unidades precede a la comparación y a la normalización por orden de extremos.
- Los intervalos lineales son valores totales: cruzar sus extremos produce `empty`, no una excepción.
- La invalidez de un estado se decide por sus dominios e invariantes, no por la mera existencia de un intervalo vacío.

## Alternativas descartadas

### Prohibir las unidades locales

Impediría expresar intervalos con unidades diferentes o con un literal junto a un campo de magnitud.

### Aplicar la unidad exterior a expresiones mixtas

Formas como `[minimumDistance..5] m` ocultarían qué subexpresiones reciben contexto de unidad y complicarían la elaboración. El literal local debe ser una cantidad completa.

### Fallar al invertir extremos

Haría parcial la construcción de intervalos y convertiría una operación conjuntista normal en un error de resolución. El conjunto definido por límites lineales invertidos es vacío; las restricciones que no toleren ese vacío ya producen el resultado operativo correspondiente.

### Interpretar la inversión como descenso o ciclo

Mezclaría contenido del intervalo, orden de enumeración y topología cíclica. MUD conserva esas tres decisiones separadas.

## Verificación

1. Unidad compartida en formas cerradas, abiertas, unitarias, ilimitadas y vacías.
2. Agrupación de `1..5 m` como unidad común al intervalo.
3. Unidades locales iguales y distintas con normalización dimensional.
4. Campo de magnitud y literal con unidad local obligatoria.
5. Rechazo de `[field..5] m`, `[1..5 m]` y de una segunda unidad exterior.
6. Rechazo de extremos de magnitudes distintas o representaciones incompatibles.
7. Extremos iguales cerrados producen un unitario; con algún lado abierto producen `empty`.
8. Extremos invertidos dinámicamente producen `empty` sin fallo por construcción.
9. Dominio vacío que excluye un valor almacenado produce `failed`.
10. `if`, `given` o `after` falsos a causa del vacío producen `rejected`.
11. Ausencia de interpretación descendente o cíclica implícita.
12. Conservación de las restricciones especiales de dominios de magnitud y de `[a..b cycle)`.
