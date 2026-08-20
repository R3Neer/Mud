---
id: D-015
title: "Especialización acíclica y estado independiente"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-042"
  - "Q-043"
affects:
  - "[[especificacion/04-modelo-matematico]], futuro `11-things.md`"
---
# ADR-015 — Especialización acíclica y estado independiente

- Modificada por: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]
- Actualizada: 2026-07-28 para usar el vocabulario de D-025
- Actualizada: 2026-08-20 para permitir inicializadores heredables en `thing` abstractas y separar declaración local de inicialización.
- Modificada por: [[notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco|D-068]]
- Preguntas: [[notas/preguntas/Q-042-especializacion-desde-una-thing-concreta|Q-042]], [[notas/preguntas/Q-043-ciclos-de-especializacion|Q-043]]
- Documentos afectados: [[especificacion/04-modelo-matematico]], futuro `11-things.md`

## Contexto

[[notas/decisiones/ADR-014-ontologia-unificada-de-things|ADR-014]] establece que toda `thing` concreta es simultáneamente una cosa con estado propio y una posible antecesora. Esto obliga a precisar:

1. Si una descendiente observa o copia el estado mutable actual de una antecesora concreta.
2. Si la relación de especialización directa admite ciclos entre identidades distintas.

## Decisión

### Estado independiente

La especialización hereda:

- declaraciones de campos;
- restricciones;
- dominios;
- valores predeterminados efectivos;
- inicializadores de `thing` aplicables;
- los demás elementos de esquema que la especificación autorice expresamente.

No hereda, copia ni observa el estado mutable actual de la antecesora.

La propiedad intrínseca `name` tampoco se hereda. Pertenece al descriptor local de cada identidad y, si no se sobrescribe, se deriva de su propio nombre nominal.

Cada `thing` concreta posee estado independiente. Mutar una `thing` no modifica por sí solo el estado de sus descendientes.

La definición canónica de una `thing`, concreta o abstracta, puede declarar antecesoras e inicializadores:

```mud
thing N as BaseOne, BaseTwo {
    field = value
}

abstract thing A as BaseOne {
    field = value
}
```

La forma `field = value` no declara un campo. Debe dirigirse a un campo almacenado ya aportado por el esquema heredado. Una misma definición de `thing` no puede declarar localmente un campo y además inicializarlo mediante otra instrucción `field = value`. La forma `field: Type = value` sigue siendo una única declaración de campo con predeterminado y no cuenta como un inicializador separado.

Una `thing` abstracta no materializa carga propia, pero sus inicializadores forman parte de la especialización y pueden contribuir a la primera materialización de una descendiente concreta. Para un mismo campo, un inicializador declarado en una descendiente más específica sustituye a los inicializadores heredados menos específicos. Si un mismo inicializador original alcanza una descendiente por varias rutas de un diamante, se deduplica por origen; inicializadores independientes e incomparables que compitan por el mismo campo producen conflicto, sin prioridad por el orden escrito de `as`, conforme a D-084.

Al activar por primera vez una `thing` concreta mediante `start with` o:

```mud
create N
```

la inicialización de $N$ parte de los predeterminados efectivos de sus antecesoras, incorpora las declaraciones locales y aplica después los inicializadores efectivos. No parte de los estados activos de sus antecesoras. Sin antecesoras, los campos sin predeterminado explícito emplean el de su tipo. Una reactivación conserva la carga almacenada conforme a D-021.

Los inicializadores no se convierten en declaraciones de campo ni en predeterminados de esquema. Que un inicializador de una `thing` abstracta pueda heredarse como contribución de inicialización no cambia el predeterminado heredable del campo.

### Especialización acíclica

La relación directa $R_{\mathrm{dir}}$ no contiene ciclos:

- no admite $(t,t)$;
- no admite ningún camino no vacío que empiece y termine en la misma `thing`.

La relación:

$$
R_{\mathsf{is}}
:=
R_{\mathrm{dir}}^*
$$

es reflexiva, transitiva y antisimétrica. Por tanto:

$$
t_1\mathrel{R_{\mathsf{is}}}t_2
\land
t_2\mathrel{R_{\mathsf{is}}}t_1
\Rightarrow
t_1=t_2.
$$

La reflexividad de `is` pertenece a la clausura y no introduce bucles en $R_{\mathrm{dir}}$.

## Alternativas descartadas

- **Delegación viva al estado de la antecesora:** produciría cambios no locales y complicaría ondas, rollback y explicación.
- **Copia del estado actual al activar:** haría que una misma primera activación dependiera de estado mutable ajeno.
- **Ciclos:** convertirían `is` en un preorden e impedirían resolver campos y predeterminados de forma bien fundada.

## Consecuencias

- El grafo fijado por las definiciones canónicas debe ser acíclico.
- El IR separa esquema heredable de estado mutable.
- La inicialización calcula predeterminados efectivos antes de aplicar inicializadores efectivos.
- Los inicializadores de abstractas se heredan como contribuciones de inicialización, no como predeterminados de esquema.
- Una definición no puede declarar y después inicializar separadamente el mismo campo.
- Escribir sobre una antecesora no añade lecturas ni escrituras implícitas sobre sus descendientes.
- `is` afecta a sustituibilidad y resolución de esquema, no propaga estado.

## Ejemplo

```mud
thing Kingdom {
    mut treasury: Money = 0
}

thing Egypt as Kingdom {}
```

Al activarse por primera vez, `Egypt` empieza con `treasury = 0`. Una escritura posterior sobre `Kingdom.treasury` no modifica `Egypt.treasury`.

```mud
thing France as Kingdom {
    treasury = 20
}
```

Al activarse por primera vez, `France.treasury` vale `20`, pero esa asignación no se convierte en predeterminado para futuras descendientes de `France`.

```mud
thing Being {
    age: Nat = 0
}

abstract thing Adult as Being {
    age = 18
}

thing Clara as Adult {}
```

`Adult` no materializa una carga propia para `age`, pero aporta `age = 18` a la inicialización efectiva de `Clara`. Una descendiente más específica puede sustituir esa contribución con su propio inicializador.

Es inválido declarar e inicializar separadamente el mismo campo en una única definición:

```mud
thing Broken {
    age: Nat
    age = 18
}
```

## Verificación

1. Rechazo de aristas reflexivas y ciclos no triviales.
2. Especialización múltiple acíclica.
3. Antisimetría de `is`.
4. Independencia de estados.
5. Inicialización desde predeterminados efectivos.
6. Aplicación de los inicializadores efectivos en la primera activación.
7. Herencia de inicializadores desde `thing` abstractas, con sustitución por una contribución más específica y deduplicación de diamantes por origen.
8. Rechazo de una declaración local de campo acompañada por un inicializador separado del mismo campo en la misma `thing`.
9. Ausencia de propagación implícita del estado mutable actual a futuras descendientes.

## Ampliación por D-084

La aciclicidad y la política no ordenada de antecesores se aplican también a aliases. Para miembros heredados, un diamante deduplica el mismo origen; miembros independientes con el mismo nombre entran en conflicto. En aliases no existe estado mutable propio que heredar.
