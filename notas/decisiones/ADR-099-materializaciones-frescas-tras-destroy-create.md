---
id: D-099
title: "Materializaciones frescas tras `destroy` y `create`"
status: current
date: 2026-08-28
supersedes: []
superseded-by: []
questions:
  - Q-005
  - Q-046
  - Q-049
  - Q-032
affects:
  - "ciclo de vida de `thing`, materialización, estado almacenado, suspensión por dependencias, estructura runtime y memoria reactiva"
  - "D-021, D-041, D-054, D-058 y D-077"
  - "capítulo 04 y futuros capítulos 11, 21 a 25 y 32"
---

# ADR-099 — Materializaciones frescas tras `destroy` y `create`

- Modifica: [[ADR-021-ciclo-de-vida-logico-y-suspension|D-021]], [[ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]], [[ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]] y [[ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]].
- Mantiene abiertas: [[notas/preguntas/Q-005-identidad-y-ciclo-de-vida-de-vinculaciones|Q-005]], Q-046 y Q-032 en los aspectos no fijados aquí. Q-049 permanece cerrada; esta decisión conserva su resolución sobre pertenencias y solo precisa la política de materialización propia.

## Contexto

D-021 y D-054 hacían que `destroy d` retirase una declaración de la proyección efectiva pero conservase también la carga runtime propia de una `thing`; un `create d` posterior reactivaba esa misma carga sin ejecutar de nuevo inicializadores. Esa regla resolvía correctamente un problema distinto: cuando otra declaración deja de ser interpretable porque depende de una declaración destruida, su estado no debe borrarse por el mero hecho de quedar suspendido.

Ambas situaciones no necesitan compartir política. Si `King.kingdom` almacena `Panama` y se destruye el tipo `Kingdom`, la propiedad pertenece a `King`: puede conservar su carga de forma latente mientras su tipo no es efectivo. En cambio, si se destruye una `thing` concreta cuyo propio campo `health` vale `2`, conservar ese `2` después de `create` convierte `destroy` en una desactivación temporal y hace que una nueva materialización no vuelva a su estado declarado.

La misma distinción afecta a modificaciones estructurales runtime propias de una `thing` y a la memoria temporal de una rule explícitamente destruida.

## Decisión

### Identidad canónica y materialización

La definición canónica y la identidad semántica de una `thing` sobreviven a `destroy`. Lo que no sobrevive es su materialización runtime propia.

Para una `thing` concreta activa se distingue conceptualmente entre:

1. su definición e identidad canónicas, pertenecientes al programa;
2. su materialización runtime actual, que contiene su carga de campos almacenados y las modificaciones estructurales runtime cuyo propietario es esa `thing`;
3. las cargas de otras declaraciones que pueden referirse a su identidad o depender de su tipo.

`destroy d`, cuando la transición completa es válida, termina la materialización actual de la `thing` concreta `d`. La identidad, descriptor, antecesoras declaradas y definición canónica permanecen disponibles para una futura materialización.

Una `thing` abstracta no posee carga concreta propia que reinicializar; su `destroy` conserva la semántica de retirada de actividad y suspensión estructural que corresponda.

### Carga propia y estructura runtime

Al confirmarse `destroy d` sobre una `thing` concreta se descartan:

- los valores almacenados propios de su materialización actual;
- las modificaciones runtime de estructura cuyo propietario sea `d`, incluidos campos añadidos durante esa materialización;
- las retiradas runtime de propiedades canónicas de `d`: una futura materialización vuelve a partir de la definición canónica, no de la estructura editada de la materialización terminada.

Por tanto, si:

```mud
thing Goblin {
    mut health: Nat = 10
}
```

alcanza `health = 2`, después de una secuencia confirmada `destroy Goblin` seguida más tarde por `create Goblin`, la nueva materialización comienza otra vez con `health = 10`.

Esta regla no introduce identidades sucesivas: ambas materializaciones corresponden a la misma identidad canónica `Goblin`.

### Nueva materialización mediante `create`

`create d` sobre una `thing` canónica sin materialización activa crea una materialización fresca usando las reglas ordinarias de primera materialización:

- se reconstruye el esquema efectivo desde la definición canónica y sus contribuciones heredadas aplicables;
- se aplican de nuevo predeterminados e inicializadores;
- no se recuperan valores ni modificaciones estructurales de la materialización destruida.

La política de semillas y resultados de inicializadores estocásticos continúa bajo Q-032; esta decisión solo exige que la operación sea una nueva materialización y no una recuperación de carga anterior.

La aplicabilidad de `create` cuando la declaración ya está activa continúa bajo Q-046.

### Suspensión por dependencia no es destrucción

Que una declaración deje de ser efectiva porque una dependencia dura está inactiva no destruye su materialización ni su carga. Solo un `destroy` dirigido a la propia declaración aplica el descarte de carga definido aquí.

En particular:

```mud
thing King {
    kingdom: Kingdom = Panama
}
```

seguido por:

```mud
destroy Kingdom
```

hace que `King.kingdom` deje temporalmente de pertenecer a la proyección efectiva mientras su tipo declarado no sea efectivo. La propiedad y su carga `Panama` pertenecen a `King` y permanecen almacenadas. Si `create Kingdom` confirma una nueva materialización de `Kingdom`, `King.kingdom` puede volver a ser efectiva con el mismo valor `Panama`.

Esta conservación ajena no implica conservar la carga propia de la materialización destruida de `Kingdom`.

### Referencias y membresías a la identidad destruida

Las referencias latentes continúan apuntando a la misma identidad canónica y pueden volver a ser efectivas cuando exista una nueva materialización compatible.

La política de colecciones de D-077 se conserva:

- una relación sin capacidad `mut` puede retener latentemente una pertenencia a la identidad retirada y restaurarla con la nueva materialización;
- una relación `mut` elimina esa pertenencia almacenada al destruir la identidad y `create` no la recompone por sí solo;
- destruir el tipo declarado de una propiedad suspende la propiedad completa y conserva su carga, porque esa carga pertenece al propietario de la propiedad y no al tipo destruido.

Toda retirada, restauración de membresías y reaparición de cargas suspendidas continúa sometida a validación atómica de cardinalidad y dominio.

### Atomicidad de la nueva materialización

Una `create d` que materializa de nuevo una `thing` debe validar conjuntamente:

- la nueva carga propia obtenida de definición, predeterminados e inicializadores;
- las pertenencias latentes que D-077 pueda restaurar;
- las declaraciones y propiedades ajenas que vuelvan a ser efectivas al reaparecer la dependencia.

Si el estado resultante no es bien formado, la transición produce `failed` y rollback. No queda confirmada una materialización parcial.

### Memoria de rules explícitamente destruidas

`destroy r` sobre una rule termina también la memoria runtime perteneciente a esa activación de la rule. En una rule reactiva se descartan sus líneas base y memoria temporal de bindings asociadas a la activación destruida.

Si `create r` la activa de nuevo después de `start with`, se trata temporalmente como una activación posterior: su primera onda activa establece la línea base actual sin disparar `when`, `changes` ni expresiones temporales únicamente por la reactivación. Desde la onda siguiente compara normalmente con esa nueva línea base.

Una rule booleana no conserva memoria temporal de este tipo. Una `always` vuelve a imponer su invariante conforme a sus puntos ordinarios de validación.

Esta decisión fija el efecto de un `destroy` explícito sobre la memoria de la rule. Q-005 permanece abierta para la identidad canónica de bindings y para la política de memoria cuando una vinculación desaparece o una rule queda meramente suspendida por causas distintas de su destrucción explícita.

## Consecuencias

- `destroy` deja de ser una mera desactivación con hibernación de la carga propia de una `thing` concreta.
- `create` después de `destroy` materializa de nuevo la misma identidad canónica, no una identidad nueva ni una recuperación de la carga anterior.
- Los resets de respawn que coincidan con los predeterminados e inicializadores declarados salen naturalmente de `destroy` + `create`; reglas de respawn que necesiten conservar o modificar información adicional siguen siendo lógica de dominio explícita.
- La suspensión por dependencia conserva su carácter reversible y no borra estado ajeno.
- Las ediciones estructurales runtime propias de una materialización no sobreviven a su destrucción.
- La memoria temporal de una rule explícitamente destruida no atraviesa su nueva activación.

## Alternativas descartadas

### Conservar toda carga propia tras `destroy`

Se descarta la política anterior. Hace que `destroy` se comporte como `deactivate` y obliga a expresar aparte incluso la reinicialización ordinaria de una nueva materialización.

### Borrar también cargas ajenas suspendidas

Se descarta. La desaparición de un tipo o dependencia no convierte en propiedad suya los datos almacenados por otras identidades. La suspensión estructural sigue siendo reversible.

### Crear una identidad runtime nueva

Se descarta. `create` sigue operando sobre una identidad canónica predeclarada y no introduce instanciación, IDs frescos ni encarnaciones nominales distintas.

### Conservar modificaciones estructurales de la materialización destruida

Se descarta. Una nueva materialización reconstruye su estructura desde la definición canónica; conservar `add`/`remove` anteriores mezclaría una materialización terminada con la siguiente.

### Conservar la memoria temporal de una rule destruida

Se descarta. Una rule que dejó explícitamente de existir en el mundo no debe comparar su nueva activación con una instantánea perteneciente a la activación anterior.

## Verificación

1. Una `thing` destruida y recreada conserva identidad y descriptor, pero recupera valores iniciales en vez de su carga anterior.
2. Los campos añadidos runtime a la materialización destruida no reaparecen; las propiedades canónicas retiradas runtime sí reaparecen desde la definición.
3. Una propiedad ajena suspendida por destruir su tipo conserva exactamente su carga y vuelve a proyectarse al recrear el tipo.
4. La suspensión derivada de una dependencia no borra la carga propia de la declaración suspendida.
5. Las relaciones inmutables y `mut` conservan la diferencia de restauración fijada por D-077.
6. Una nueva materialización que haría inválida una cardinalidad o dominio produce `failed` y rollback completo.
7. Una rule reactiva destruida y recreada establece una línea base nueva sin disparar por la mera reactivación.
8. Q-005 continúa abierta para desapariciones de bindings y suspensiones no causadas por `destroy` explícito.
9. Q-032 continúa gobernando la reproducibilidad concreta de inicializadores aleatorios entre materializaciones.
