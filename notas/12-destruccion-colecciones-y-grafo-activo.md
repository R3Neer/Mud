# Destrucción, colecciones y grafo activo

- Estado: análisis
- Preguntas relacionadas: [[notas/08-preguntas-abiertas#Q-048 — Destrucción con descendientes activos|Q-048]], [[notas/08-preguntas-abiertas#Q-049 — Destrucción y colecciones de constructos|Q-049]]
- Decisiones relacionadas: [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|D-017]], [[notas/decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|D-019]]

## Regla superficial buscada

La explicación para una persona debería poder mantenerse cerca de:

> Si algo deja de existir, desaparece de las colecciones en las que ya no puede estar. Si alguna regla del juego exige que siga habiendo un miembro y no aparece un sustituto, el cambio entero no vale.

La formalización inferior necesita precisar tipo efectivo, mutabilidad, cardinalidad, ondas y rollback.

## Todos los campos como colecciones

Una cardinalidad omitida equivale a `[1]`. Por tanto:

```mud
kingdom: Kingdom
```

es una colección con exactamente un miembro, igual que:

```mud
kingdom: Kingdom [1]
```

`kingdoms: Kingdom [*]` es la misma clase semántica de valor colección con otra restricción de cardinalidad. Un campo derivado también puede modelarse como una colección cuyo valor se recalcula, en vez de almacenarse.

## Dominio activo de un tipo constructo

Sea $\mathcal E_W$ el conjunto de identidades activas y sea $R_W^{\mathsf{is}}$ la especialización activa. Una denotación candidata es:

$$
\llbracket A\rrbracket_W
:=
\{
c\in\mathcal E_W
\mid
(c,A)\in R_W^{\mathsf{is}}
\}
$$

Si `Kingdom` se desactiva, no solo deja de ser miembro la propia identidad `Kingdom`. Un descendiente `Egypt` puede dejar de satisfacer `Egypt is Kingdom` al conectarse temporalmente con los antecesores activos de `Kingdom`. Por tanto, todas las colecciones cuyo tipo de miembro dependa de `Kingdom` deben revalidarse.

## Poda candidata de una colección almacenada

Sea $K$ una colección de miembros de tipo $A$ antes de la destrucción y sea $W'$ el mundo tentativo posterior. Definimos como propuesta:

$$
\operatorname{prune}_{A,W'}(K)
:=
\operatorname{filter}
\left(
K,
\lambda x.\ x\in\llbracket A\rrbracket_{W'}
\right)
$$

La operación elimina todas las apariciones que ya no pertenecen al tipo activo:

- En una secuencia conserva el orden relativo de los supervivientes.
- En un multiconjunto elimina todas las ocurrencias inválidas.
- En un conjunto elimina los miembros inválidos.
- Diccionarios y claves requieren una regla específica todavía abierta.

Esta poda sería una mutación exterior. Conforme a D-019, una colección almacenada sin `mut` no puede cambiar de miembros. En ese caso, la destrucción debería fallar en lugar de atravesar silenciosamente la inmutabilidad.

## Cardinalidad

Tras la poda debe comprobarse:

$$
\left|
\operatorname{prune}_{A,W'}(K)
\right|
\in
\operatorname{card}(K)
$$

Ejemplos:

### Colección singular

```mud
mut kingdom: Kingdom [1]
```

Si su único miembro deja de satisfacer `Kingdom`, la poda produce `empty`, que incumple `[1]`. La destrucción no puede confirmarse salvo que la misma raíz establezca un sustituto antes de la validación final.

Sin el `mut` exterior, tanto la retirada como una sustitución serían inválidas: ambas cambian la colección almacenada.

### Colección sin mínimo positivo

```mud
mut kingdoms: Kingdom [*]
```

La retirada puede dejarla vacía porque `[*]` equivale a `[0..*]`.

### Colección derivada

```mud
kingdoms: Kingdom [*] := all active kingdoms
```

No se poda un valor almacenado: se vuelve a evaluar la expresión en $W'$. No necesita mutabilidad exterior. Su resultado sí debe satisfacer el tipo y la cardinalidad declarados.

## Relación con valores predeterminados

D-017 exige un valor predeterminado para todo tipo bien formado. Si:

```mud
kingdom: Kingdom [1]
```

debe contener obligatoriamente una identidad activa y el dominio activo de `Kingdom` queda vacío, no existe ningún valor que pueda habitar el tipo colección.

Esto favorece una de estas decisiones:

1. Rechazar la destrucción porque produciría un tipo o una posición obligatoria sin valor posible.
2. Permitir referencias a identidades inactivas.
3. Introducir membresía latente separada de la colección visible.

La primera alternativa conserva mejor el significado de «no existe» y evita referencias colgantes. Las otras dos requieren explicar por qué una colección contiene algo que no está activo.

## Recreación

Hay dos semánticas posibles para colecciones almacenadas:

- **Retirada destructiva:** los miembros podados no regresan al reactivar la identidad. Las colecciones derivadas pueden recuperarlos al recalcularse.
- **Membresía latente:** se ocultan mientras no son válidos y reaparecen al reactivar la identidad.

La retirada destructiva es más simple y corresponde a borrar una pieza de las listas del juego. La membresía latente hace reversible la operación, pero añade estado oculto y complica cardinalidad, igualdad, serialización y `old`.

El grafo reservado sí conserva sus aristas porque proceden de declaraciones, no de estado almacenado. No se sigue automáticamente que las colecciones almacenadas deban conservar membresía latente.

## Orden de una transición candidata

Una raíz que destruya una identidad podría evaluarse así:

1. Retirar tentativamente la identidad de $\mathcal E_W$.
2. Comprimir el grafo activo atravesando identidades inactivas.
3. Recalcular la denotación activa de los tipos de constructo.
4. Podar colecciones almacenadas afectadas cuando tengan mutabilidad exterior.
5. Recalcular colecciones derivadas.
6. Ejecutar las ondas reactivas que correspondan.
7. Validar tipos, cardinalidades, reglas `always` y poscondiciones.
8. Confirmar todo o revertir todo.

Queda por decidir si se permiten estados tentativos con cardinalidad insuficiente durante las ondas o si toda reparación debe formar parte de la misma propuesta atómica.

## Recomendación provisional

La combinación más uniforme es:

- Supresión temporal de nodos inactivos en el grafo de especialización.
- Poda destructiva de membresías almacenadas que dejan de estar tipadas.
- Necesidad de mutabilidad exterior para efectuar esa poda.
- Recálculo ordinario de campos derivados.
- Validación final de cardinalidades con rollback completo.
- Ausencia de restauración automática de membresías almacenadas al recrear.

No debe promoverse a norma hasta resolver Q-048 y Q-049 con ejemplos de `[1]`, `[*]`, múltiples antecesores, campos derivados y diccionarios.
