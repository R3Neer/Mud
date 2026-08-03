---
id: D-021
title: "Ciclo de vida lógico y suspensión por dependencias"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-048"
  - "Q-049"
affects:
  - "[[especificacion/04-modelo-matematico]], futuros capítulos 11, 21 a 25 y 32"
---
# ADR-021 — Ciclo de vida lógico y suspensión por dependencias

- Actualizada: 2026-07-28 para usar el vocabulario de D-025
- Relacionada con: [[notas/decisiones/ADR-031-aliases-nominales-e-inmutables|D-031]], [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]]
- Modificada por: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Modificada además por: [[ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]]
- Ejemplo actualizado por: [[ADR-079-diagnostico-exterior-de-reglas-always|D-079]]
- Preguntas afectadas: [[notas/preguntas/Q-048-destruccion-con-descendientes-activos|Q-048]], [[notas/preguntas/Q-049-destruccion-y-colecciones-de-thing|Q-049]]
- Documentos afectados: [[especificacion/04-modelo-matematico]], futuros capítulos 11, 21 a 25 y 32

## Contexto

Una semántica que elimina permanentemente estado al ejecutar `destroy` obliga a podar colecciones, reparar cardinalidades, fabricar predeterminados y decidir si la recreación recupera información antigua. También confunde dos intenciones distintas:

- Quitar temporalmente una clase de cosa o ley del juego.
- Eliminar deliberadamente una propiedad y su contenido.

Se desea que `destroy Kingdom` haga desaparecer lógicamente `Kingdom` y las declaraciones que necesitan ese tipo, sin borrar que `King.kingdom` contenía `Panama`. Si `Kingdom` vuelve a crearse, la propiedad y su carga deben reaparecer.

## Decisión

El modelo distingue:

1. Un catálogo de **definiciones canónicas** del programa, que conserva identidades, descriptores y aristas `as` estáticas.
2. Una representación **almacenada** del mundo, que conserva cargas y modificaciones estructurales runtime latentes.
3. Una proyección **efectiva**, que contiene únicamente las partes que participan actualmente en el juego.

Sea $\mathcal D_P$ el conjunto de declaraciones conocidas por el programa y sea $\mathcal L_P\subseteq\mathcal D_P$ el subconjunto con ciclo de vida explícito. Un estado $W$ mantiene, como mínimo:

$$
\operatorname{stored}_W
$$

para la información runtime retenida y:

$$
\operatorname{active}_W:
\mathcal L_P\to\mathbb B
$$

para la activación explícita de las declaraciones con ciclo de vida. La proyección efectiva:

$$
\operatorname{Effective}(W)
$$

se deriva de ambos componentes y de las dependencias entre declaraciones.

`destroy d` cambia la activación de $d$, pero no modifica su definición canónica ni su carga almacenada:

$$
\operatorname{active}_{W'}(d)=\bot
$$

$$
\operatorname{stored}_{W'}(d)
=
\operatorname{stored}_{W}(d)
$$

`create d` vuelve a activar la misma identidad declarativa. Si ya había estado almacenado, la reactivación no lo reinicializa:

$$
\operatorname{stored}_{W'}(d)
=
\operatorname{stored}_{W}(d)
$$

Los inicializadores de la definición canónica se aplican cuando la carga se materializa por primera vez, ya sea mediante `start with` o mediante `create Nombre`. Una reactivación posterior no reinicializa la carga.

## Categorías con ciclo de vida

`create` y `destroy` pueden operar sobre:

- `thing` concretas.
- `thing` abstractas.
- Reglas booleanas.
- Reglas reactivas.
- Reglas `always`.

No operan sobre:

- Aliases.
- Acciones.
- Magnitudes.

Las acciones forman la API estable de escritura. Las magnitudes forman parte del sistema dimensional estático.

## Sintaxis superficial

Conforme a D-054, toda `thing` y regla posee una única definición canónica de primer nivel:

```mud
thing Kingdom {}

abstract thing Place {}

rule CanEnter for person: Person {
    ...
}

rule OpenGate on gate: Gate [mut] {
    ...
}

always rule ValidKingdom on kingdom: Kingdom {
    kingdom.population >= 0
}
otherwise "Invalid population in {kingdom}"
```

Las activaciones runtime omiten categoría y cuerpo:

```mud
create CanEnter
create OpenGate
create ValidKingdom
```

La misma forma activa una `thing`:

```mud
create Kingdom
create Place
```

Las declaraciones presentes al comienzo se enumeran conjuntamente:

```mud
start with {
    Kingdom,
    Place,
    CanEnter
}
```

`destroy` solo necesita una referencia que resuelva de manera unívoca:

```mud
destroy Kingdom
destroy CanEnter
```

Los nombres de declaraciones comparten el espacio necesario para que esa resolución sea inequívoca. Una referencia ambigua debe diagnosticarse; `destroy` no elige una categoría por prioridad.

El compilador puede elaborar internamente estas formas como definición canónica, activación inicial, activación runtime y desactivación. `activate` y `deactivate` no se introducen como palabras de la superficie MUD.

## Suspensión por dependencias

Una declaración almacenada puede no ser efectiva aunque su propia marca explícita siga activa. Sea:

$$
\operatorname{HardDep}_P(d)
$$

el conjunto de dependencias cuya ausencia impide usar $d$. De manera esquemática:

$$
\operatorname{effective}_W(d)
\iff
\operatorname{active}_W(d)
\land
\forall e\in\operatorname{HardDep}_P(d).
\operatorname{effective}_W(e)
$$

Para una propiedad almacenada $p$, son dependencias duras:

- Su propietario.
- Su tipo declarado.
- Las declaraciones necesarias para interpretar su dominio y forma.

Por tanto, si:

```mud
thing King {
    kingdom: Kingdom[1] = Panama
}
```

y se ejecuta:

```mud
destroy Kingdom
```

la propiedad `King.kingdom` deja de pertenecer a $\operatorname{Effective}(W)$, pero continúa almacenada junto con `Panama`. Al recrear `Kingdom`, vuelve a ser efectiva con la misma carga.

La estructura propia de una `thing` destruida desaparece de la proyección efectiva. Su definición canónica permanece en el programa y su carga o modificaciones runtime permanecen almacenadas en el mundo.

## Participantes y declaraciones dependientes

Si el tipo de un participante deja de ser efectivo, no se elimina solo ese parámetro de la firma. Se suspende la declaración que necesita la firma completa:

- Una regla reactiva no produce bindings.
- Una regla `always` no impone temporalmente su invariante.
- Una regla booleana se considera inactiva a efectos de evaluación.
- Una acción dependiente deja temporalmente de ser invocable, aunque las acciones no sean destruibles directamente.

Esta suspensión conserva aridad, nombres de roles y referencias internas. Recrear la dependencia restaura la declaración sin reescribirla.

## Especialización y descendientes

Las aristas declaradas mediante `as` permanecen en la definición canónica del programa. En la proyección efectiva, un descendiente activo no se suspende necesariamente porque una de sus antecesoras esté destruida.

Cuando un camino almacenado:

$$
c = n_0,\ldots,n_k = p
$$

tiene extremos activos y todos sus nodos interiores inactivos, la proyección efectiva puede conectar $c$ con el antecesor activo más próximo $p$. No se atraviesa un antecesor intermedio que continúe activo.

Así, al destruir `Kingdom`:

```text
Thing
└── Kingdom
    └── Panama
```

la proyección efectiva puede ser:

```text
Thing
└── Panama
```

Las propiedades declaradas por `Kingdom` dejan de heredarse mientras esté destruido. Las propiedades propias de `Panama` permanecen si sus dependencias siguen efectivas. Al recrear `Kingdom`, reaparecen las aristas y propiedades almacenadas originales.

La dependencia de especialización declarada con `as` es atravesable en la proyección efectiva y no una dependencia dura que destruya en cascada a todos los descendientes.

## `add` y `remove` sobre propiedades

`add` y `remove` también operan sobre propiedades. La palabra `property` no es necesaria:

```mud
add kingdom: Kingdom[1] = Panama to King
remove kingdom from King
```

Los dos puntos distinguen la adición de una declaración de propiedad de la adición de un miembro:

```mud
add Panama to King.kingdoms
remove Panama from King.kingdoms
```

`remove kingdom from King` elimina la propiedad y su carga almacenada. Volver a añadir una propiedad homónima no recupera automáticamente `Panama`.

Por tanto:

$$
\operatorname{remove}(p)
\implies
p\notin\operatorname{Stored}(W')
$$

mientras que:

$$
\operatorname{destroy}(T)
\land
T\in\operatorname{HardDep}_P(p)
\implies
\begin{cases}
p\in\operatorname{Stored}(W')\\
p\notin\operatorname{Effective}(W')
\end{cases}
$$

## Ausencia de capturas implícitas

Una declaración introducida por `create` no captura variables libres del `then`, acción o binding que ejecuta la creación.

Puede declarar y utilizar:

- Sus propios participantes `on` o `for`.
- Sus propios valores `given` cuando su clase de regla los admita.
- Nombres y anclas globales resolubles.

No puede retener implícitamente un participante ni un `given` perteneciente al contexto creador. Si una ley necesita recordar un dato, ese dato debe representarse explícitamente en el estado del mundo.

Esta regla evita que la misma identidad global reciba cierres diferentes según qué binding la active.

## Alternativas descartadas

### Poda destructiva indiscriminada

Se descarta eliminar automáticamente y de la misma forma todos los miembros de colecciones. D-077 adopta una retirada condicionada: debe conservar la cardinalidad final, las relaciones inmutables retienen pertenencia latente y las relaciones `mut` eliminan la pertenencia almacenada.

### Cascada destructiva

Se descarta destruir automáticamente descendientes y dependientes. La suspensión derivada basta para retirarlos de la proyección cuando sea necesario y conserva la reversibilidad.

### `activate` y `deactivate` en la superficie

Se conservan como posible modelo interno, pero se descartan como vocabulario principal. `create`, `destroy`, `add` y `remove` describen de forma más directa las reglas de un mundo.

### Capturas condicionadas a unicidad

Se descartan. Exigirían definir cuándo se demuestra la unicidad, qué ocurre si cambia y cómo se resuelven dos cargas distintas para una misma identidad.

## Cuestiones todavía abiertas

- Operaciones permitidas sobre propiedades suspendidas.
- Serialización e introspección de la representación almacenada.

## Verificación futura

La suite deberá cubrir:

1. Conservación de una propiedad y su carga tras destruir su tipo.
2. Restauración exacta tras recrear el tipo.
3. Pérdida de carga tras `remove`.
4. Suspensión completa de reglas y acciones con participantes de tipo inactivo.
5. Rechazo de `create` y `destroy` aplicados a un alias, conforme a D-031.
6. Compresión y restauración del grafo efectivo.
7. Conservación de propiedades propias de descendientes.
8. Ausencia de capturas implícitas.
9. Resolución inequívoca de `destroy`.
10. Rechazo de `create` o `destroy` sobre acciones y magnitudes.
