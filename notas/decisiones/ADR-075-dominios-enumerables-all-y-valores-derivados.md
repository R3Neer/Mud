---
id: D-075
title: "Dominios enumerables, `all` y forma de valores derivados"
status: vigente
date: 2026-08-03
supersedes: []
superseded-by: []
questions:
  - "Q-047"
affects:
  - "dominios, colecciones, campos, vinculaciones locales, AST y conformidad"
---
# ADR-075 — Dominios enumerables, `all` y forma de valores derivados

- Ampliada por: [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]]
- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]

## Contexto

Los intervalos no bastan para restringir valores enumerados, escalonados o nominales. Además, la forma de colección de un valor calculado debe poder expresarse e inferirse igual que en un valor almacenado.

## Decisión

### Dominios

El modelo distingue dominios de intervalos, dominios finitos, dominios escalonados, dominios nombrados y composiciones mediante unión, intersección, diferencia y diferencia simétrica.

```mud
colors: Color in [Red, White] [2] = all
numbers: Num in 0..1 by 0.2 [6] = all
```

`by` convierte un intervalo lineal en un dominio discreto. Su paso es estático, firmado, no nulo, exacto y compatible con el tipo o dimensión. Un paso positivo se ancla en el límite inferior y uno negativo en el superior conforme a D-088. `Num` usa aritmética racional exacta; un dominio `Rum` no se considera enumerable. La cardinalidad siempre usa corchetes y es independiente del dominio.

### Literal contextual `all`

`all` denota la enumeración canónica completa del dominio esperado y requiere contexto. Se admite para `Bool`, families, aliases finitos, dominios finitos, dominios escalonados, el catálogo de prefijos y tipos `thing`. Para un tipo `thing` reúne sus descendientes estrictos activos compatibles; con `Thing` reúne todas las declaraciones `thing` activas salvo el propio tipo incorporado. Cada identidad aparece una sola vez.

Cuando la enumeración depende del mundo, como `all` sobre `thing`, solo puede alimentar un valor calculado `:=`. La cardinalidad se comprueba sobre el resultado de cada evaluación.

### Valores derivados

Campos calculados, datos calculados de families, vinculaciones locales y campos públicos de `look` y `message` comparten esta forma:

```text
nombre [forma-derivada] ":=" expresión
```

La forma derivada es una anotación completa `: tipo`, una restricción `in dominio` seguida opcionalmente por colección, o una colección sin tipo ni dominio. Esto permite tanto `a: A in [B, C] := expresión` como `a in [B, C] := expresión` sin fabricar una anotación de tipo superficial.

El dominio declarado en una forma derivada es coercitivo: filtra el resultado con la misma semántica que la restricción local de dominio. La cardinalidad se comprueba después de esa transformación; una cota inferior que ya no pueda satisfacerse produce la obligación o el fallo correspondiente y nunca fabrica miembros.

Una lista de expresiones separadas por comas construye una colección derivada:

```mud
numbers := a * b, d, c / a
```

Su tipo común y cardinalidad se infieren. La aridad es cardinalidad exacta para colecciones con multiplicidad ordinaria; bajo `unique` solo lo es cuando la distinción de elementos puede demostrarse. Una colección incluida como elemento no se aplana implícitamente.

Una selección `value in source : predicate` y `take amount from source` también producen valores derivados de colección. Conservan los contratos demostrables de su fuente y permiten que la forma derivada declare un dominio o cardinalidad más precisa como obligación independiente.

## Diagnósticos de conversión

Cuando `to` solo aporta un contexto de tipo, el tooling sugiere trasladarlo a la declaración. Si la conversión es constante y segura, también normaliza el valor:

```mud
value := 3.7 to Nat
value: Nat := 4
value: Nat = 4
```

Cada transformación es una sugerencia independiente y solo se ofrece cuando conserva dominios y comportamiento de fallo.

## Verificación

1. Dominios finitos de families, things y cantidades.
2. Cuadrículas exactas y rechazo de pasos inválidos.
3. `all` estático y dinámico con cardinalidad.
4. Dominios y colecciones en toda declaración calculada.
5. Inferencia de listas calculadas, multiplicidad y `unique`.
6. Tres resultados del análisis de dominios derivados.
7. Sugerencias escalonadas de `to`.

## Modificación por D-088

El paso de un dominio escalonado deja de exigirse positivo. Sigue siendo estático, exacto, compatible y no nulo, pero puede ser firmado. Positivo ancla en el límite inferior y negativo en el superior; un límite inicial abierto avanza una vez antes del primer candidato. El signo puede cambiar la pertenencia, pero no introduce orden en el tipo; `all` usa el orden canónico. `Rum` continúa excluido.

## Modificación vigente por D-096

Además del literal contextual `all`, existe `all D`, que materializa la enumeración canónica completa de un dominio enumerable explícito. Los dominios reflectivos visibles admiten formas como `all action`, `all rule`, `all look` y `all A.action(B)`. `all` sin operando conserva su elaboración contextual.
