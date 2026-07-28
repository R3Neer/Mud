# ADR-041 — Contratos de las tres clases de regla

- Estado: Vigente
- Fecha: 2026-07-28
- Relacionada con: [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|D-025]], [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]]
- Preguntas relacionadas: Q-005, Q-050
- Documentos afectados: modelo del lenguaje, semántica estática, semántica dinámica

## Contexto

MUD utiliza una sola palabra declarativa, `rule`, para tres mecanismos distintos. Compartir nombre no debe permitir cuerpos ambiguos ni una variante general con combinaciones arbitrarias de cláusulas.

## Decisión

El AST contiene tres variantes distintas: regla booleana, regla reactiva y regla `always`.

### Regla booleana

```mud
rule CanAttack for
    attacker: Army,
    defender: Army
given
    maximumDistance: Length
{
    ...
}
```

Declara participantes mediante `for`, puede declarar `given`, es pura y devuelve `Bool`. Puede usar cuantificadores, agregaciones booleanas, `allowed` y, cuando el análisis lo admita, `eventually`.

No puede escribir estado, ejecutar efectos, crear, destruir ni leer directamente un campo estocástico calculado. Se consulta explícitamente mediante el protocolo de receptores y argumentos de D-036.

Una regla booleana no efectiva se elabora conforme a la poda estructural de D-022, no como una llamada que devuelve un booleano fijo.

### Regla reactiva

```mud
rule OpenGate on gate: Gate [mut] {
    when gate.unlocked
    if not gate.open
    then gate.open = true
}
```

Declara vinculaciones automáticas mediante `on`, no admite `given`, exige `when`, admite `if` y produce efectos mediante `then`. No ejecuta acciones reales. Puede consultar reglas booleanas y usar `allowed` si el grafo resultante sigue siendo acíclico.

Para cada vinculación, `when e` dispara únicamente por la transición:

$$
\mathsf{false}\longrightarrow\mathsf{true}.
$$

El runtime conserva el valor anterior por identidad de vinculación. `changes e` solo aparece dentro de `when` y produce un pulso por cambio neto confirmado de `e`.

### Regla `always`

```mud
always rule ValidPosition on game: Game {
    ...
}
```

Declara vinculaciones automáticas mediante `on`, no admite `given`, no es invocable y no produce efectos. Su cuerpo es una condición pura que se comprueba automáticamente en los puntos normativos de validación. Una infracción produce `failed`, nunca `rejected`.

### Ciclo de vida común

Las tres variantes poseen una definición canónica única de primer nivel, pueden activarse mediante `start with` o `create Nombre` y suspenderse mediante `destroy`, conforme a D-021 y D-054. Conservan su variante al reactivarse. La suspensión de una regla `always` retira temporalmente su obligación; la reactivación no permite publicar un estado que la incumpla.

Las tres variantes comparten la categoría de ancla `rule::*`. En particular, `always` es una palabra contextual delante de `rule`, no una categoría nominal ni un prefijo de ancla independiente.

## Consecuencias

- Una cabecera o combinación de cláusulas que corresponda a más de una variante se rechaza.
- Solo las reglas booleanas forman llamadas con resultado.
- Solo las reactivas forman consecuencias causales.
- Solo `always` convierte una falsedad en fallo de invariante.
- Q-005 todavía debe fijar la identidad, nacimiento y retirada de la memoria de una vinculación.

## Verificación

1. Un ejemplo válido y otro inválido por cada variante.
2. Rechazo de `given` en una regla `on`.
3. Rechazo de efectos en reglas booleanas y `always`.
4. Disparo reactivo únicamente en `false → true`.
5. Poda de una llamada booleana suspendida.
