---
id: D-041
title: "Contratos de las tres clases de regla"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-005"
  - "Q-050"
affects:
  - "modelo del lenguaje, semántica estática, semántica dinámica"
---
# ADR-041 — Contratos de las tres clases de regla

- Relacionada con: [[notas/decisiones/ADR-025-vocabulario-cabeceras-y-bloques|D-025]], [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]]
- Modificada por: [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]]
- Modificada además por: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Preguntas relacionadas: Q-005, Q-050
- Documentos afectados: modelo del lenguaje, semántica estática, semántica dinámica

## Contexto

MUD utiliza una sola palabra declarativa, `rule`, para tres mecanismos distintos. Compartir nombre no debe permitir cuerpos ambiguos ni una variante general con combinaciones arbitrarias de cláusulas.

## Decisión

El AST contiene tres variantes distintas: regla booleana, regla reactiva y regla `always`.

- Modificada también por: [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]]
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
Sus `given` son valores de solo lectura y pueden declarar predeterminados estáticos. Las llamadas los vinculan por posición o por nombre conforme a D-063.

}
```

Declara vinculaciones automáticas mediante `on`, no admite `given`, exige `when`, admite `if` y produce efectos mediante `then`. No ejecuta acciones reales. Puede consultar reglas booleanas y usar `allowed` si el grafo resultante sigue siendo acíclico.

Sea $W_n$ la instantánea leída al comienzo de la onda $n$ y sea $v_n(b,e)$ el valor de la expresión $e$ para la vinculación $b$ en esa instantánea. Para una vinculación que ya posea memoria, un `when e` puramente booleano dispara únicamente cuando:

$$
\neg v_{n-1}(b,e)\land v_n(b,e).
$$

Por tanto, solo dispara en la transición $\mathsf{false}\longrightarrow\mathsf{true}$. El runtime conserva el valor anterior por identidad de vinculación.

El sufijo `changes` admite cualquier expresión pura con igualdad definida y produce en la onda $n$ el pulso:

$$
Los roles de una misma cabecera `on` se resuelven conjuntamente y pueden formar restricciones relacionales cíclicas finitas conforme a D-063.

\operatorname{changes}_n(b,e)
\iff
v_{n-1}(b,e)\ne v_n(b,e).
$$

Este pulso se calcula directamente para cada par de instantáneas de inicio consecutivas. No es un booleano almacenado, no se restablece mediante un cambio a `false` y no se somete de nuevo a la detección $\mathsf{false}\rightarrow\mathsf{true}$. Si $e$ cambia entre dos pares consecutivos de instantáneas, `changes` pulsa en ambas ondas. Solo importa el cambio neto entre instantáneas; los valores transitorios dentro de un delta privado no son observables.

Los activadores temporales se componen con las palabras `and` y `or`. Un operando booleano ordinario de una composición se eleva a su transición `false` → `true`; no se interpreta como un nivel sostenido. La gramática, el alcance de `old` y la elaboración formal de estas combinaciones se fijan en D-058.

### Inicialización de la memoria reactiva

Las vinculaciones presentes en la primera instantánea obtenida al materializar conjuntamente el `start with` global o local reciben para cada rama booleana elevada un valor anterior virtual $\mathsf{false}$. Si la rama es verdadera en esa primera instantánea de estabilización, pulsa. Las expresiones temporales, incluidos `changes` y `old`, comparan la instantánea inicial consigo misma: `changes` no pulsa y `old e` vale lo mismo que `e`.

Una vinculación que no estaba presente en esa primera instantánea, ya sea por activación posterior de una regla o por aparición de participantes, no participa en la raíz u onda que la crea. En su primera onda activa memoriza el valor actual sin disparar `when` ni producir un pulso `changes`. Desde la onda siguiente compara normalmente dos instantáneas. En particular, si memoriza $\mathsf{false}$ y la condición es $\mathsf{true}$ en la onda posterior, `when` dispara; si memoriza inicialmente $\mathsf{true}$, esa mera aparición no dispara.

### Regla `always`

```mud
always rule ValidPosition on game: Game {
    game.position in game.board
    otherwise "A position is outside the board of {game}"
}
```

Declara vinculaciones automáticas mediante `on`, no admite `given`, no es invocable y no produce efectos. Su cuerpo contiene una condición pura y puede añadir un diagnóstico `Text` mediante `otherwise`. La condición se comprueba automáticamente en los puntos normativos de validación. Una infracción evalúa perezosamente el diagnóstico sobre el estado tentativo infractor y produce `failed` con esa causa, nunca `rejected`, conforme a D-061. Si se omite, el compilador emite un aviso y el runtime genera una razón predeterminada.

### Ciclo de vida común

Las tres variantes poseen una definición canónica única de primer nivel, pueden activarse mediante `start with` o `create Nombre` y suspenderse mediante `destroy`, conforme a D-021 y D-054. Conservan su variante al reactivarse. La suspensión de una regla `always` retira temporalmente su obligación; la reactivación no permite publicar un estado que la incumpla.

Las tres variantes comparten la categoría de ancla `rule::*`. En particular, `always` es una palabra contextual delante de `rule`, no una categoría nominal ni un prefijo de ancla independiente.

## Consecuencias

- Una cabecera o combinación de cláusulas que corresponda a más de una variante se rechaza.
- Solo las reglas booleanas forman llamadas con resultado.
- Solo las reactivas forman consecuencias causales.
- Solo `always` convierte una falsedad en fallo de invariante.
- Q-005 todavía debe fijar la identidad canónica, la retirada de memoria y su posible conservación cuando una vinculación desaparece y reaparece.

## Verificación

1. Un ejemplo válido y otro inválido por cada variante.
2. Rechazo de `given` en una regla `on`.
3. Rechazo de efectos en reglas booleanas y `always`.
4. Disparo de un `when` puramente booleano únicamente en `false → true`.
5. Poda de una llamada booleana suspendida.
6. `changes` pulsa en cambios consecutivos sin una onda falsa intermedia.
7. Ausencia de pulso cuando una expresión cambia transitoriamente pero conserva el mismo valor entre instantáneas.
8. Disparo inicial de un `when` verdadero procedente de `start with`.
9. Inicialización sin disparo de una vinculación creada fuera de `start with`.
10. Composición de dos cambios y de un cambio con una transición booleana mediante `and` y `or`.
11. Pulsos consecutivos preservados dentro de una composición temporal.
12. Aviso para una regla `always` sin `otherwise`, generación de una razón predeterminada y propagación de un diagnóstico explícito al `failed`.
