# ADR-015 — Especialización acíclica y estado independiente

- Estado: Vigente
- Fecha: 2026-07-27
- Preguntas: [[notas/08-preguntas-abiertas#Q-042 — Herencia desde un constructo concreto|Q-042]], [[notas/08-preguntas-abiertas#Q-043 — Ciclos de especialización|Q-043]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[especificacion/04-modelo-matematico]], futuro `11-constructos.md`

## Contexto

[[notas/decisiones/ADR-014-ontologia-unificada-de-constructos|ADR-014]] establece que todo constructo concreto es simultáneamente una cosa con estado propio y un posible antecesor de otros constructos. Esa unificación obliga a precisar:

1. Si un descendiente observa o copia el estado mutable actual de un antecesor concreto.
2. Si la relación de especialización directa admite ciclos entre identidades distintas.

Ambas decisiones afectan al store, la inicialización, la causalidad, el rollback, la resolución de campos y el significado algebraico de `is`.

## Decisión

### Estado independiente

La especialización hereda:

- Declaraciones de campos.
- Restricciones.
- Dominios.
- Valores predeterminados efectivos.
- Los demás elementos de esquema que la especificación autorice expresamente.

La especialización no hereda, copia ni observa el estado mutable actual del antecesor.

Cada constructo concreto posee estado independiente. La mutación de un constructo no modifica por sí sola el estado de sus descendientes.

Al crear un constructo concreto mediante `create N from C_1,\ldots,C_n`, la inicialización de $N$ parte de los valores predeterminados efectivos obtenidos de sus antecesores y aplica después las asignaciones explícitas del bloque de creación. No parte de los valores que sus estados activos contengan en ese momento. Si no hay antecesores, no existen predeterminados heredados.

Las asignaciones del bloque `create` inicializan el estado de $N$; no se convierten por ello en nuevos valores predeterminados heredables por futuros descendientes de $N$.

### Especialización acíclica

La relación de especialización directa $R_{\mathrm{dir}}$ no puede contener ciclos. En particular:

- No puede contener una arista directa $(c,c)$.
- No puede existir un camino no vacío que comience y termine en el mismo constructo.

La relación semántica:

$$
R_{\mathsf{is}}
:=
R_{\mathrm{dir}}^*
$$

es, por tanto:

- Reflexiva.
- Transitiva.
- Antisimétrica.

En consecuencia, $R_{\mathsf{is}}$ es un orden parcial sobre los constructos:

$$
c_1\mathrel{R_{\mathsf{is}}}c_2
\land
c_2\mathrel{R_{\mathsf{is}}}c_1
\Rightarrow
c_1=c_2
$$

La reflexividad de `is` es una propiedad de la clausura y no requiere introducir bucles en $R_{\mathrm{dir}}$.

## Alternativas

### Delegación viva al estado del antecesor

Se descarta porque una mutación local produciría cambios no locales en todos los descendientes. Complicaría dependencias, ondas, atomicidad, rollback y explicación de resultados.

### Copia del estado actual al crear

Se descarta porque haría depender la inicialización de un constructo de un estado mutable ajeno y convertiría una misma operación de creación en contextualmente distinta aunque las declaraciones no cambiasen.

### Ciclos admitidos

Se descarta porque convertiría `is` en un preorden: dos constructos con identidades diferentes podrían especializarse mutuamente. También impediría una resolución finita y bien fundada de la herencia de campos y predeterminados.

## Consecuencias para el compilador

- El grafo de especialización estática debe comprobarse como grafo dirigido acíclico.
- La resolución de campos y predeterminados puede recorrer antecesores sin riesgo de ciclos.
- Añadir mediante `create` un constructo fresco con aristas hacia constructos existentes no puede formar un ciclo por sí solo.
- Cualquier futura operación que permita cambiar antecesores deberá preservar la aciclicidad.
- El IR debe separar metadatos heredables de estado mutable.
- La inicialización debe calcular predeterminados efectivos antes de aplicar las asignaciones explícitas de `create`.

## Consecuencias semánticas

Sea $a$ antecesor de $c$. Una escritura sobre un campo almacenado de $a$ no implica una escritura sobre la posición correspondiente de $c$.

Los conjuntos de lectura y escritura de una acción no incluyen descendientes por el mero hecho de modificar un antecesor. La relación `is` afecta a sustituibilidad y resolución de esquema, pero no constituye un canal implícito de propagación de estado.

## Ejemplo

```mud
construct Kingdom {
    mut treasury: Money = 0M
}

construct Egypt is Kingdom {
}
```

`Egypt` comienza con el predeterminado efectivo `treasury = 0M`. Si posteriormente:

```mud
Kingdom.treasury = 100M
```

el valor de `Egypt.treasury` no cambia.

De igual modo, tras:

```mud
create France from Kingdom {
    treasury = 20M
}
```

`France.treasury` vale `20M`. Si más adelante se crea un descendiente de `France` sin inicialización explícita, la asignación `20M` no actúa como predeterminado heredable.

## Verificación futura

La suite deberá comprobar:

1. Rechazo de una arista directa reflexiva.
2. Rechazo de ciclos de dos o más constructos.
3. Aceptación de especialización múltiple acíclica.
4. Antisimetría de `is`.
5. Independencia entre el estado de un antecesor concreto y sus descendientes.
6. Inicialización desde predeterminados efectivos, no desde estado activo.
7. Aplicación de las asignaciones de `create` después de los predeterminados.
8. Ausencia de propagación implícita de las asignaciones de `create` a descendientes futuros.
