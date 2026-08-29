---
id: D-071
title: "Vinculaciones locales en bloques booleanos"
status: vigente
date: 2026-08-02
supersedes: []
superseded-by: []
questions: []
affects:
  - "reglas booleanas, when, if, after, always, tests, gramática, CST, AST y resolución de nombres locales"
---
# ADR-071 — Vinculaciones locales en bloques booleanos

- Modificada por: [[ADR-101-bloques-de-valor-variables-locales-y-extremos|D-101]].

- Amplía: [[ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]]
- Modifica: [[ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]] y [[ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]]
- Modificada después por: [[ADR-079-diagnostico-exterior-de-reglas-always|D-079]]
- Modificada por: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]

## Contexto

Las condiciones de MUD pueden necesitar cálculos intermedios legibles. Repetirlos dentro de una expresión booleana dificulta su lectura, mientras que convertirlos en campos introduciría estado que no pertenece al mundo.

MUD ya dispone de vinculaciones locales inmutables mediante `:=` en bloques `then`. Falta extender el mismo vocabulario a condiciones sin volver ambiguo qué valor booleano decide la cláusula.

## Decisión

### Bloque booleano

Un bloque booleano contiene, en este orden:

1. Cero o más vinculaciones locales `nombre [forma-derivada] := expresión`, con tipo estático opcional y coerciones derivadas admitidas sobre dominio, cardinalidad, unicidad u orden.
2. Exactamente una expresión final.

La expresión final debe satisfacer el contrato de la construcción propietaria: elabora a `Bool` en reglas booleanas, guardas, invariantes y postcondiciones; en `when`, elabora a un activador admitido por D-058. Toda expresión sin forma de declaración debe ser la última del bloque; una segunda expresión no declarativa es inválida.

```mud
if {
    cost := amount * price
    available := kingdom.money
    available >= cost
}
```

Los bloques booleanos se admiten en:

- Cuerpos de reglas booleanas.
- Cláusulas `when`.
- Cláusulas `if`.
- Cuerpos de reglas `always`.
- Postcondiciones `after` de acciones.
- Aserciones de tests cuando su forma concreta lo permita.

La forma sin llaves y una única expresión continúa siendo válida y se normaliza a un bloque sin locales.

### Evaluación y ámbito

Las vinculaciones locales son puras, inmutables y se evalúan secuencialmente una vez por evaluación de la cláusula, contra la misma instantánea que observa la condición. No crean estado persistente ni sobreviven a otra evaluación.

Cada nombre es visible desde la declaración siguiente hasta:

- La expresión booleana final.
- El `otherwise` asociado, si existe.

No es visible en `then`, en otra cláusula ni fuera del bloque. Se mantienen las prohibiciones de D-066: no hay referencias adelantadas, ciclos, redeclaración ni sombreado.

En un `when`, una local usada por `changes` u `old` se interpreta evaluando su expresión definitoria en cada instantánea requerida; la vinculación no almacena por sí misma un valor entre ondas.

### `after` de tests

El bloque `after` de un test no es una única condición, sino una secuencia no vacía de aserciones. Puede comenzar con cero o más vinculaciones locales comunes, seguidas por una o más aserciones. Las locales son visibles en todas las aserciones y sus `otherwise`.

```mud
after {
    expected := before + amount
    kingdom.soldiers == expected
    kingdom.treasury >= 0
}
```

No pueden intercalarse nuevas declaraciones locales después de la primera aserción. El `then` de un test conserva los bloques de efectos y las vinculaciones locales definidos por D-066.

### Representación abstracta

D-088 generaliza la representación común. El AST superficial normaliza toda condición a:

```text
ExpressionBlock(locals, result)
```

En los contextos definidos por esta decisión, el propietario exige que `result` cumpla el contrato booleano o temporal correspondiente. El diagnóstico `otherwise` pertenece a la construcción propietaria y puede resolver los nombres de `locals`. Un `after` de test usa un bloque propio con locales comunes y una secuencia no vacía de `TestAssertion`.

## Consecuencias

- Los cálculos intermedios no se duplican ni amplían el store.
- La última expresión identifica sin ambigüedad el resultado de la condición.
- El mismo modelo sirve para reglas, guardas, postcondiciones y tests.
- La visibilidad en `otherwise` permite diagnósticos informativos sin crear anclas para locales.

## Verificación

1. Bloque sin locales equivalente a la forma breve.
2. Una o varias locales antes de la expresión final.
3. Rechazo de bloque sin expresión final o con dos expresiones no declarativas.
4. Uso secuencial de una local anterior.
5. Rechazo de referencia adelantada, ciclo, redeclaración y sombreado.
6. Visibilidad en `otherwise` y ausencia de visibilidad en `then`.
7. Reevaluación temporal de locales usadas por `changes` u `old`.
8. Locales comunes en `after` de test con una o varias aserciones.
9. Rechazo de una local posterior a la primera aserción de test.

## Modificación por D-088

La estructura se generaliza a `ExpressionBlock(locals, result)`. Las condiciones mantienen sus contratos booleanos/temporales; selección y `exists`, `forall`, `count`, `min` y `max` pueden escribir tras `:` una expresión breve o `{ locales*; resultado }`, con las mismas reglas de pureza, secuencialidad, ámbito y ausencia de referencias adelantadas, ciclos, redeclaración y sombreado.
