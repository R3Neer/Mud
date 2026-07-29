---
id: D-026
title: "Membresía estricta y cardinalidad por `then`"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-003"
  - "Q-021"
  - "Q-047"
affects:
  - "[[notas/02-modelo-del-lenguaje]], [[notas/03-semantica-de-ejecucion]], [[especificacion/04-modelo-matematico]], futuro `10-sistema-de-tipos.md`, futuro `15-colecciones.md`"
---
# ADR-026 — Membresía estricta y cardinalidad por `then`

- Preguntas afectadas: [[notas/preguntas/Q-003-puntos-de-validacion|Q-003]], [[notas/preguntas/Q-021-analisis-estatico-de-conflictos|Q-021]], [[notas/preguntas/Q-047-seleccion-de-predeterminados-por-tipo|Q-047]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[notas/03-semantica-de-ejecucion]], [[especificacion/04-modelo-matematico]], futuro `10-sistema-de-tipos.md`, futuro `15-colecciones.md`

## Contexto

Una colección tipada por una `thing` contiene especializaciones suyas, no la propia identidad que actúa como tipo. También es necesario fijar si una modificación de colección debe respetar la cardinalidad después de cada instrucción o al completar una unidad atómica de efectos.

## Decisión

### Membresía de `thing`

Sea $T$ la `thing` que aparece como tipo de miembro y sea $c$ una identidad candidata. La pertenencia es válida exactamente cuando:

$$
c\neq T
\land
c\ \mathsf{is}\ T
$$

No existe `reflexive` ni otro modificador que permita el caso $c=T$.

Por ejemplo, una propiedad:

```mud
kingdom: Kingdom[1]
```

puede contener `Panama` si `Panama is Kingdom` y `Panama != Kingdom`. No puede contener `Kingdom`.

Esta condición compara el miembro con el ancla de tipo, no con la identidad propietaria de la propiedad. Si `Alice is Person`, una propiedad de `Alice` tipada como `Person` sí puede contener `Alice`, porque `Alice != Person`.

### Punto de comprobación local

Las instrucciones de un mismo `then` se evalúan secuencialmente sobre su delta privado. Los estados intermedios de ese delta no tienen que satisfacer los límites de cardinalidad. Al terminar el `then`, cada colección modificada debe respetar su cardinalidad declarada.

Así, para una colección de cardinalidad `[1]`, este patrón puede ser válido dentro de un único bloque:

```mud
then {
    remove oldKing from kingdom.kings
    add newKing to kingdom.kings
}
```

No es válido repartir la sustitución entre dos `then`. Cada `then` debe preservar por sí mismo la cardinalidad; ninguno puede depender de un efecto concurrente ajeno para reparar su resultado.

### Obligación estática

La comprobación es una obligación de prueba del análisis estático. Para cada `then` $t$, cada colección afectada $p$ y todo estado de entrada bien formado permitido por los tipos y guardas, el compilador debe demostrar:

$$
\ell_p
\leq
\left|\operatorname{apply}(t,p)\right|
\leq
u_p
$$

donde $[\ell_p,u_p]$ es la cardinalidad declarada y $\operatorname{apply}(t,p)$ es el contenido final de $p$ en el delta privado de $t$.

El análisis debe ser sensible, como mínimo, a:

- El intervalo inicial posible de tamaños.
- La presencia o ausencia demostrable del miembro retirado.
- La unicidad y multiplicidad de la colección.
- Las guardas y ramas de control.
- La secuencia completa de efectos del `then`.

Si la obligación no puede demostrarse, el programa se rechaza conservadoramente. No se difiere una posible infracción local al runtime.

### Compatibilidad entre `then`

La prueba local no basta cuando varios `then` pueden modificar la misma colección en una oleada. El análisis de conflictos debe demostrar que su consolidación también conserva la cardinalidad, o demostrar que los bloques son mutuamente excluyentes. Si no puede probar ninguna de las dos cosas, el programa se rechaza.

Por ejemplo, dos bloques que añaden elementos distintos a una colección vacía `[0..1]` son válidos localmente, pero no pueden coexistir en una misma oleada salvo que el compilador demuestre exclusión mutua.

## Consecuencias

- No existe un modificador `reflexive` en el léxico, la gramática, el AST ni el IR.
- La cardinalidad es una propiedad de salida de cada `then`, no de cada estado intermedio de su delta.
- Las reglas estáticas necesitan un análisis abstracto de intervalos y efectos de colección.
- La aceptación del lenguaje es deliberadamente conservadora: un programa seguro pero no demostrable puede ser rechazado.
- La consolidación conserva una comprobación de bien formación como defensa del runtime, pero alcanzarla indicaría un defecto del compilador o una entrada externa inválida, no un conflicto semántico esperado.

## Interacción con valores predeterminados

Una colección de `thing` con mínimo positivo necesita un valor predeterminado que sea una especialización estricta del tipo escrito. D-017 sigue exigiendo que todo tipo bien formado tenga predeterminado; Q-047 debe determinar cuándo tal tipo es bien formado y cuándo se exige un inicializador explícito.

## Verificación futura

1. Aceptación de un descendiente estricto.
2. Rechazo del ancla exacta.
3. Rechazo léxico o sintáctico de `reflexive`.
4. Sustitución `remove`–`add` válida dentro del mismo `then`.
5. Rechazo de cada mitad de esa sustitución en `then` separados.
6. Análisis de ramas que conservan y que rompen los límites.
7. Rechazo de dos efectos localmente válidos cuya consolidación puede desbordar.
8. Aceptación cuando se demuestra exclusión mutua.
