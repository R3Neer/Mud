# ADR-049 — Operadores, precedencia e intervalos normalizados

- Estado: Vigente
- Fecha: 2026-07-28
- Modificada por: [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
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
| Lógica | `not`, `and`, `or`, `xor`, `=>`, `<=>` |
| Temporal | sufijo `changes`; composición con `and`, `or` dentro de `when` |
| Intervalos | `|`, `&`, `^`, `-` |
| Colecciones | `|`, `&`, `^`, `-` |
| Texto | `|` para concatenación de `Text` |

Los tokens compartidos se resuelven por tipos y contexto sintáctico; no autorizan coerciones entre booleanos, números, colecciones e intervalos.

Cada operación posee una única escritura canónica. `not`, `and`, `or` y `xor` son exclusivamente lógicos. `|`, `&` y `^` no se aplican a `Bool`: expresan respectivamente unión, intersección y diferencia simétrica sobre intervalos o colecciones, salvo la concatenación de `Text` ya indicada. `-` continúa compartido por resta cuantitativa y diferencia conjuntista. `=>` expresa implicación y `<=>`, bicondicional.

Se eliminan del lenguaje fuente `!`, `implies`, `iff`, `union`, `intersection` y `except`. Las palabras retiradas dejan de estar reservadas y pueden usarse como identificadores. El token `!=` permanece como desigualdad independiente y no presupone que exista un operador unitario `!`.

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

1. acceso `.`, indexación `[]`, llamada `()` y extracción completa `unit from container in point`;
2. prefijos `old`, `allowed`, `not` y signo;
3. multiplicación, división y módulo;
4. suma, resta y diferencia conjuntista;
5. sufijos `to Type` e `in unit`;
6. comparaciones, `is` y pertenencia `in`;
7. sufijo temporal `changes`;
8. conjunción e intersección;
9. disyunción, unión y concatenación;
10. diferencia simétrica;
11. implicación;
12. bicondicional;
13. `eventually ... through ...`.

En un `when` temporal, solo las palabras `and` y `or` componen activadores. Los símbolos `&` y `|` conservan sus operaciones tipadas ordinarias y se rechazan si reciben un activador; tampoco se aplican a estos `not`, `xor`, `^`, `=>` ni `<=>`. D-058 define la elevación de operandos booleanos y la semántica de la composición.

`to` y el `in` de unidad se aplican al valor completo acumulado a su izquierda. El parser continúa después sobre el resultado convertido:

```mud
population / regions to Population
distance + offset in km
value to A to B
```

se agrupan como `(population / regions) to Population`, `(distance + offset) in km` y `(value to A) to B`.

Las cadenas homogéneas de `<`, `<=`, `>`, `>=` y `==` se elaboran como conjunciones de pares adyacentes. Lo mismo ocurre con `<=>`. `!=`, `is`, pertenencia `in` y `=>` no se encadenan.

`|` concatena `Text`. Los demás operadores conjuntistas no se aplican a `Text`, ni la concatenación se hereda implícitamente por aliases nominales de `Text`. Sobre colecciones compatibles, los cuatro operadores forman el álgebra de multiconjuntos de D-039; `|` no concatena colecciones.

### Intervalos

Las operaciones de unión, intersección, diferencia simétrica y diferencia producen una forma normalizada por contenido: segmentos disjuntos, ordenados y sin duplicados. Dos intervalos son iguales si sus formas normalizadas denotan el mismo conjunto.

`empty` denota el intervalo vacío. Los literales básicos y las reglas de `*`, `[n]`, ciclos y límites canónicos pertenecen a D-029; la enumeración pertenece a D-047.

D-059 incorpora intervalos de magnitud con unidades locales o una unidad común exterior. Sus extremos se comparan después de normalizar unidades. Un intervalo lineal con límite inferior mayor que el superior, o con límites iguales y algún lado abierto, se normaliza a `empty`; nunca adquiere implícitamente orden descendente ni semántica cíclica.

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
9. Rechazo de los aliases retirados y de `!` aislado, con conservación de `!=`.
10. Separación estática entre `xor` lógico y `^` conjuntista.
11. Precedencia de `changes` por debajo de comparaciones y por encima de `and` y `or`.
12. Rechazo de operadores distintos de las palabras `and` y `or` sobre activadores temporales.
13. Normalización equivalente de intervalos de magnitud con unidades locales y compartidas.
14. Normalización a `empty` de extremos lineales invertidos o degenerados abiertos.
