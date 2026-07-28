# ADR-049 — Operadores, precedencia e intervalos normalizados

- Estado: Vigente
- Fecha: 2026-07-28
- Preguntas relacionadas: Q-001, Q-018, Q-050
- Documentos afectados: expresiones, intervalos, gramática

## Contexto

La referencia contenía el catálogo de operadores y su precedencia, pero es anterior a `to`, a la nominalidad completa de aliases y al sistema actual de magnitudes.

## Decisión

### Familias de operadores

| Familia | Formas |
| --- | --- |
| Aritmética | `+`, `-`, `*`, `/`, `%` |
| Comparación | `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `in` |
| Lógica | `!`/`not`, `&`/`and`, `|`/`or`, `^`/`xor`, `=>`/`implies`, `<=>`/`iff` |
| Intervalos | `|`/`union`, `&`/`intersection`, `^`/`xor`, `-`/`except` |
| Colecciones | `|`/`union`, `&`/`intersection`, `^`/`xor`, `-`/`except` |
| Texto | `|` para concatenación de `Text` |

Los tokens compartidos se resuelven por tipos y contexto sintáctico; no autorizan coerciones entre booleanos, números, colecciones e intervalos.

La igualdad se define por clase de valor:

- `thing`: identidad;
- `family`: tipo nominal y miembro;
- alias: mismo tipo nominal y contenido;
- números: valor dentro de la misma representación o tras conversión explícita;
- magnitudes: cantidad normalizada dimensionalmente compatible;
- intervalos: conjunto normalizado;
- colección ordenada: secuencia;
- colección no ordenada: multiplicidad;
- diccionario: conjunto de asociaciones clave–valor.

`is` consulta la relación reflexiva y transitiva de especialización entre `thing`; no es igualdad ni casting.

### Precedencia

De mayor a menor:

1. acceso `.`, indexación `[]` y llamada `()`;
2. prefijos `old`, `allowed`, negación y signo;
3. multiplicación, división y módulo;
4. suma, resta y `except`;
5. sufijos `to Type` e `in unit`;
6. comparaciones, `is` y pertenencia `in`;
7. conjunción e intersección;
8. disyunción, unión y concatenación;
9. diferencia simétrica;
10. implicación;
11. bicondicional;
12. `eventually ... through ...`.

`to` y el `in` de unidad se aplican al valor completo acumulado a su izquierda. El parser continúa después sobre el resultado convertido:

```mud
population / regions to Population
distance + offset in km
value to A to B
```

se agrupan como `(population / regions) to Population`, `(distance + offset) in km` y `(value to A) to B`.

Las cadenas homogéneas de `<`, `<=`, `>`, `>=` y `==` se elaboran como conjunciones de pares adyacentes. Lo mismo ocurre con `iff`. `!=`, `is`, pertenencia `in` e `implies` no se encadenan.

`|` concatena `Text`. Los demás operadores conjuntistas no se aplican a `Text`, ni la concatenación se hereda implícitamente por aliases nominales de `Text`. Sobre colecciones compatibles, los cuatro operadores forman el álgebra de multiconjuntos de D-039; `|` no concatena colecciones.

### Intervalos

Las operaciones de unión, intersección, diferencia simétrica y diferencia producen una forma normalizada por contenido: segmentos disjuntos, ordenados y sin duplicados. Dos intervalos son iguales si sus formas normalizadas denotan el mismo conjunto.

`empty` denota el intervalo vacío. Los literales básicos y las reglas de `*`, `[n]`, ciclos y límites canónicos pertenecen a D-029; la enumeración pertenece a D-047.

## Consecuencias

- La sobrecarga nunca se decide por una prioridad de implementación.
- Comparar aliases distintos o `Number` con `Rumber` requiere `to`.
- El catálogo completo de tipos admitidos y resultados por operador sigue siendo trabajo del sistema de tipos.

## Verificación

1. Parseos que distingan cada nivel de precedencia.
2. Igualdad y desigualdad de cada clase de valor.
3. Normalización equivalente de intervalos.
4. Rechazo de sobrecargas sin combinación tipada.
5. Conversión acumulativa y continuación con operadores posteriores.
6. Encadenamientos admitidos y rechazados.
7. Concatenación de `Text` y rechazo de las demás operaciones conjuntistas.
8. Resolución de los cuatro operadores conjuntistas sobre colecciones compatibles.
