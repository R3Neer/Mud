# ADR-015 — Especialización acíclica y estado independiente

- Estado: Vigente
- Fecha: 2026-07-27
- Actualizada: 2026-07-28 para usar el vocabulario de D-025
- Preguntas: [[notas/preguntas/Q-042-especializacion-desde-una-thing-concreta|Q-042]], [[notas/preguntas/Q-043-ciclos-de-especializacion|Q-043]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[especificacion/04-modelo-matematico]], futuro `11-things.md`

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
- los demás elementos de esquema que la especificación autorice expresamente.

No hereda, copia ni observa el estado mutable actual de la antecesora.

Cada `thing` concreta posee estado independiente. Mutar una `thing` no modifica por sí solo el estado de sus descendientes.

La definición canónica de una `thing` concreta puede declarar antecesoras e inicializadores:

```mud
thing N as BaseOne, BaseTwo {
    ...
}
```

Al activarla por primera vez mediante `start with` o:

```mud
create N
```

la inicialización de $N$ parte de los predeterminados efectivos de sus antecesoras, incorpora las declaraciones locales y aplica después las inicializaciones explícitas. No parte de sus estados activos. Sin antecesoras, los campos sin predeterminado explícito emplean el de su tipo. Una reactivación conserva la carga almacenada conforme a D-021.

Las asignaciones concretas del bloque inicializan $N$, pero no se convierten en predeterminados heredables. Solo una declaración explícita de predeterminado forma parte del esquema.

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
- La inicialización calcula predeterminados efectivos antes de aplicar asignaciones explícitas.
- Escribir sobre una antecesora no añade lecturas ni escrituras implícitas sobre sus descendientes.
- `is` afecta a sustituibilidad y resolución de esquema, no propaga estado.

## Ejemplo

```mud
thing Kingdom {
    mut treasury: Money = 0
}

thing Egypt as Kingdom {
}
```

Al activarse por primera vez, `Egypt` empieza con `treasury = 0`. Una escritura posterior sobre `Kingdom.treasury` no modifica `Egypt.treasury`.

```mud
thing France as Kingdom {
    treasury = 20
}
```

Al activarse por primera vez, `France.treasury` vale `20`, pero esa asignación no se convierte en predeterminado para futuras descendientes de `France`.

## Verificación

1. Rechazo de aristas reflexivas y ciclos no triviales.
2. Especialización múltiple acíclica.
3. Antisimetría de `is`.
4. Independencia de estados.
5. Inicialización desde predeterminados efectivos.
6. Aplicación de los inicializadores canónicos en la primera activación.
7. Ausencia de propagación implícita a futuras descendientes.
