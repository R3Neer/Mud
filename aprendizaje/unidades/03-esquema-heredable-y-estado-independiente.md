---
title: Unidad 03 — Esquema heredable y estado independiente
aliases:
  - Esquema y estado de `thing`
unit: 3
status: planificada
level: 1-a-2
depends-on:
  - "[[aprendizaje/unidades/02-constructos-como-orden-parcial]]"
concepts:
  - esquema efectivo
  - estado independiente
  - posición almacenada
  - propiedad suspendida
  - buena formación
  - valor predeterminado
  - colección
spec-chapters:
  - "[[especificacion/04-modelo-matematico]]"
  - "[[especificacion/README#11. `Thing`, especialización e identidad]]"
  - "[[especificacion/README#14. Campos, mutabilidad y capacidades]]"
decisions:
  - D-014
  - D-015
  - D-054
  - D-017
  - D-019
  - D-021
  - D-025
  - D-026
tags:
  - mud/aprendizaje
  - mud/unidad
---

# Unidad 03 — Esquema heredable y estado independiente

> [!abstract]
> Esta unidad está planificada y ya ha sido alineada con el modelo actual. Se activará después de revisar la Unidad 02. No contiene todavía ejercicios ni soluciones.

## Pregunta de MUD

Si:

```mud
thing Egypt as Kingdom {
}
```

entonces `Egypt` puede heredar la propiedad `treasury`, pero una mutación de `Kingdom.treasury` no cambia `Egypt.treasury`.

La pregunta será:

> ¿Cómo derivamos las propiedades efectivas de cada `thing` sin confundir esquema heredado, predeterminado, carga almacenada y estado activo?

## Objetivos previstos

La unidad enseñará a:

1. Derivar antecesores desde el orden parcial efectivo.
2. Distinguir propiedades declaradas y efectivas.
3. Modelar la fusión de propiedades homónimas.
4. Separar predeterminado de valor almacenado actual.
5. Definir posiciones almacenables y efectivas.
6. Relacionar el store con propiedades suspendidas.
7. Escribir condiciones de buena formación.
8. Demostrar la independencia del estado de antecesores y descendientes.
9. Modelar todos los campos como colecciones.
10. Aplicar membresía estricta y mutabilidad ortogonal.

## Prerrequisito de activación

Antes de activarla se revisará:

[[aprendizaje/respuestas/02-orden-parcial-de-constructos-respuesta]]

La revisión deberá demostrar:

- Orientación correcta de las aristas.
- Distinción entre grafo almacenado y efectivo.
- Cálculo de bypass.
- Distinción entre relación directa y clausura.
- Reflexividad, transitividad y antisimetría.
- Membresía estricta respecto del tipo.

## Decisiones que no se reabrirán

- Existe un único dominio de `thing`; no hay clases e instancias.
- `Thing` es la raíz abstracta incorporada y toda `thing` satisface `is Thing`.
- La sintaxis vigente usa `thing`, `as` e `is`.
- Cada `thing` posee una única definición canónica; `start with` y `create Nombre` solo cambian su actividad.
- Los ciclos de especialización se rechazan.
- Se heredan esquema y predeterminados, nunca estado activo.
- `name` es una propiedad intrínseca local al descriptor: no pertenece al esquema heredable ni al store.
- Cada `thing` concreta posee estado independiente.
- Todo tipo bien formado posee un predeterminado.
- Todo campo denota una colección.
- Mutabilidad exterior y capacidad interior son ortogonales.
- `destroy` suspende estructura y conserva carga.
- `remove` sobre una propiedad elimina declaración y contenido.
- Una colección de tipo `T` exige $c\neq T\land c\ \mathsf{is}\ T$.

## Secuencia prevista

```text
orden parcial efectivo
→ propiedades declaradas
→ esquema efectivo
→ fusión o conflicto
→ predeterminado efectivo
→ posiciones almacenables
→ carga independiente
→ proyección efectiva
→ buena formación
```

## Problemas que deberá resolver

### Identidad de propiedades

Una propiedad heredada desde la misma ancla se deduplica. Dos propiedades homónimas procedentes de anclas distintas deben fusionarse bajo reglas compatibles o producir un error estático.

### Predeterminado frente a estado

Un predeterminado pertenece al esquema:

$$
\operatorname{default}_P(\tau)
\in
\llbracket\tau\rrbracket_P
$$

El valor actual pertenece al mundo. Un inicializador de la definición canónica determina la primera carga de esa identidad cuando se activa por primera vez, pero no convierte ese valor actual en predeterminado heredable.

La selección concreta por constructor de tipos sigue abierta en [[notas/preguntas/Q-047-seleccion-de-predeterminados-por-tipo|Q-047]].

### Todo campo es una colección

La cardinalidad omitida equivale a `[1]`. No crea una categoría escalar.

Se estudiarán por separado:

- Mutabilidad exterior: cambiar la colección.
- Capacidad interior: modificar las `thing` alcanzadas como miembros.
- Membresía estricta: excluir el ancla exacta del tipo.

### Posiciones almacenadas y efectivas

La Unidad 01 introdujo posiciones materializadas. Ahora habrá que distinguir:

$$
\operatorname{Pos}^{\mathsf{stored}}_{P,W}
$$

de:

$$
\operatorname{Pos}^{\mathsf{eff}}_{P,W}
$$

Una propiedad suspendida puede conservar su posición y carga almacenadas sin aparecer en la proyección efectiva.

### Store total o parcial

Compararemos:

$$
\operatorname{store}_W:
\mathcal T_P\times\mathcal F_P
\rightharpoonup
\mathcal V_P
$$

con:

$$
\operatorname{store}_W:
\operatorname{Pos}^{\mathsf{stored}}_{P,W}
\to
\mathcal V_P
$$

La elección se justificará por los invariantes que haga explícitos, no por gusto notacional.

### Estados tentativos

D-026 permite que estados intermedios dentro del delta privado de un `then` incumplan temporalmente cardinalidad, siempre que el resultado final se demuestre válido. Esta unidad solo preparará las posiciones y valores; la prueba abstracta de efectos pertenecerá a una unidad posterior.

## Reparto didáctico previsto

Nivel 1 a 2:

- Codex demostrará un esquema efectivo sencillo.
- El autor derivará las posiciones válidas de una variación.
- Ambos compararán las representaciones del store.
- El autor construirá un contraejemplo contra una fusión ingenua.

## Entregables futuros

Cuando se active se crearán:

- `aprendizaje/ejercicios/03-esquema-y-estado-ejercicio.md`
- `aprendizaje/respuestas/03-esquema-y-estado-respuesta.md`

No se crean todavía para no adelantar trabajo del autor antes de enseñar la técnica.
