---
title: Ejercicio 02 — Grafo almacenado y efectivo de `thing`
unit: 2
status: vigente
level: 1
tags:
  - mud/aprendizaje
  - mud/ejercicio
---

# Ejercicio 02 — Grafo almacenado y efectivo de `thing`

Referencia: [[aprendizaje/unidades/02-constructos-como-orden-parcial]].

Completa [[aprendizaje/respuestas/02-orden-parcial-de-constructos-respuesta]].

## Enunciado

Considera:

```mud
abstract thing Entity {}

abstract thing Place as Entity {}

thing Settlement as Place {}

thing Alexandria as Settlement {}

thing NileDelta as Place {}

thing Memphis as Settlement {}

thing DeltaCapital as NileDelta, Settlement {}

start with {
    Entity,
    Place,
    Settlement,
    Alexandria,
    NileDelta
}
```

Durante la ejecución:

```mud
create Memphis
create DeltaCapital
```

Todas están activas. Después se ejecuta:

```mud
destroy Settlement
```

`Settlement` queda suspendida, pero sus aristas permanecen almacenadas.

## 1. Identidades

Define:

$$
\mathcal T_P
$$

e indica cuáles se activan mediante `start with` y cuáles se activan después mediante `create`.

Escribe $\mathcal A_{W_0}$ antes de `destroy` y $\mathcal A_{W_1}$ después.

## 2. Relación almacenada

Construye:

$$
R^{\mathsf{stored}}_P
$$

Explica por qué `destroy Settlement` no puede modificarla.

## 3. Relación efectiva antes de destruir

Construye:

$$
R^{\mathsf{eff}}_{P,W_0}
$$

Cuando todas las identidades del camino están activas, no debe aparecer ningún bypass innecesario.

## 4. Relación efectiva después de destruir

Construye:

$$
R^{\mathsf{eff}}_{P,W_1}
$$

Incluye los bypass necesarios desde:

- `Alexandria`.
- `Memphis`.
- `DeltaCapital`.

## 5. Consultas `is`

Evalúa en $W_1$:

| Consulta | Resultado | Camino o razón |
| --- | --- | --- |
| `Alexandria is Place` |  |  |
| `Alexandria is Entity` |  |  |
| `Memphis is Place` |  |  |
| `DeltaCapital is NileDelta` |  |  |
| `DeltaCapital is Place` |  |  |
| `Place is Place` |  |  |
| `Place is Alexandria` |  |  |

No evalúes `x is Settlement`: el tratamiento diagnóstico de operandos inactivos todavía no está cerrado.

## 6. Orden parcial

Explica brevemente por qué el bypass no crea ciclos nuevos y por qué la clausura efectiva sigue siendo antisimétrica.

## 7. Ciclo inválido

¿Por qué debe rechazarse?

```mud
thing Entity as Alexandria {}
```

Escribe el camino no vacío que cerraría el ciclo.

## 8. Membresía estricta

Para:

```mud
places: Place[*]
```

clasifica como admisibles o inadmisibles en $W_1$:

- `Place`.
- `Alexandria`.
- `NileDelta`.
- `Memphis`.
- `Entity`.

Justifica usando:

$$
c\neq\mathsf{Place}
\land
c\ \mathsf{is}\ \mathsf{Place}
$$

## 9. `as` e `is`

Explica qué diferencia existe entre los nodos abstractos correspondientes a:

```mud
thing Alexandria as Settlement {}

Alexandria is Place
```

## 10. Parte insegura

Indica al menos una decisión o paso que hayas tenido que comprobar.

## Criterio de corrección

La respuesta debe:

1. Conservar las aristas almacenadas tras `destroy`.
2. Excluir `Settlement` del portador efectivo de $W_1$.
3. Añadir solo bypass con extremos activos e interior inactivo.
4. Distinguir relación directa y clausura.
5. Aplicar reflexividad y antisimetría.
6. Aplicar la desigualdad obligatoria de membresía.
