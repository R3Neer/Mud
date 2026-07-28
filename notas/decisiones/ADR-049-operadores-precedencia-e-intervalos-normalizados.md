# ADR-049 — Operadores, precedencia e intervalos normalizados

- Estado: Vigente como base; gramática completa abierta
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
| Lógica | `!`/`not`, `&`/`and`, `|`/`or`, `=>`/`implies`, `<=>`/`iff` |
| Intervalos | `|`/`union`, `&`/`intersection`, `^`/`xor`, `-`/`except` |

Los tokens compartidos se resuelven por tipos y contexto sintáctico; no autorizan coerciones entre booleanos, números, colecciones e intervalos.

La igualdad se define por clase de valor:

- `thing`: identidad;
- familia cerrada: tipo nominal y alternativa;
- alias: mismo tipo nominal y contenido;
- números: valor dentro de la misma representación o tras conversión explícita;
- magnitudes: cantidad normalizada dimensionalmente compatible;
- intervalos: conjunto normalizado;
- colección ordenada: secuencia;
- colección no ordenada: multiplicidad;
- diccionario: conjunto de asociaciones clave–valor.

`is` consulta la relación reflexiva y transitiva de especialización entre `thing`; no es igualdad ni casting.

### Precedencia heredada

De mayor a menor:

1. acceso `.`, indexación `[]` y llamada `()`;
2. receptor multiparte;
3. `old`;
4. `allowed`;
5. negación;
6. multiplicación, división y módulo;
7. suma y resta;
8. comparaciones, `is` e `in`;
9. conjunción e intersección;
10. disyunción y unión;
11. diferencia simétrica;
12. implicación;
13. bicondicional;
14. `eventually ... through ...`.

Esta lista es vinculante para las formas que contiene. Q-001 debe insertar `to`, construcción contextual y cualquier forma nueva, además de fijar asociatividad y prohibiciones de encadenamiento.

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
5. Casos que obliguen a parentetizar hasta fijar `to`.
