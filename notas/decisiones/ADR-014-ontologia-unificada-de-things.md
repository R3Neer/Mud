# ADR-014 — Ontología unificada de `thing`

- Estado: Vigente
- Fecha: 2026-07-27
- Actualizada: 2026-07-28 para usar el vocabulario de D-025
- Preguntas: [[notas/08-preguntas-abiertas#Q-041 — Ontología de `thing`|Q-041]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[especificacion/04-modelo-matematico]], futuro `11-things.md`

## Contexto

Hablar de «instancias runtime» puede sugerir una separación entre clases y objetos. Esa separación no corresponde al modelo conceptual de MUD: una formalización basada en una función que asignase a cada objeto su clase introduciría dos dominios que el lenguaje no posee.

## Decisión

MUD tiene un único dominio conceptual de `thing`.

1. Una `thing` no tiene instancias.
2. Toda `thing` posee identidad semántica.
3. Toda `thing` concreta denota además una cosa concreta con estado propio y puede servir como antecesora de otras.
4. Una `thing` abstracta pertenece al mismo dominio y posee identidad, pero no denota por sí misma una cosa concreta con estado propio.
5. Cada `thing` tiene una única definición canónica; `as` fija en ella cero o varias relaciones directas y `create Nombre` solo activa esa identidad, según [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].
6. La relación semántica `is` es reflexiva y transitiva.

La procedencia —declaración estática o activación durante la ejecución— y el ciclo de vida no originan categorías ontológicas distintas.

## Distinción formal

`as` e `is` operan sobre niveles distintos:

- `as` introduce antecesores directos en la cabecera de una `thing` estática o creada.
- `is` es un operador de expresión que consulta la relación semántica derivada.

Sea $R_{\mathrm{dir}}$ la relación de especialización directa. [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]] la completa con:

$$
R_{\mathsf{is}}
:=
R_{\mathrm{dir}}^*.
$$

Por tanto:

$$
t\mathrel{R_{\mathsf{is}}}t
$$

y:

$$
t_1\mathrel{R_{\mathrm{dir}}}t_2
\land
t_2\mathrel{R_{\mathrm{dir}}}t_3
\Rightarrow
t_1\mathrel{R_{\mathsf{is}}}t_3.
$$

La relación directa es acíclica; su clausura reflexiva y transitiva es un orden parcial.

## Alternativas

### Clases separadas de instancias

Se descarta. Obliga a decidir si una `thing` es clase u objeto y no representa que una `thing` concreta pueda ser simultáneamente una cosa y una antecesora.

### Una sola palabra para declaración y consulta

Se descarta. Aunque el parser pudiera distinguir los contextos, ocultaría la diferencia entre añadir una arista directa y consultar una clausura. La sintaxis vigente usa `as` e `is`, conforme a [[notas/decisiones/ADR-018-as-declara-is-consulta|ADR-018]] y D-025.

### `is` estricto e irreflexivo

Se descarta. La especialización directa es estricta, pero `is` consulta su clausura reflexiva.

## Consecuencias

- El lexer distingue `as` e `is`.
- El parser usa `as` en cabeceras e `is` en expresiones.
- El AST representa los antecesores en la declaración y la consulta en `IsExpression`.
- La resolución comprueba que los nombres posteriores a `as` designan `thing`.
- `create` amplía el conjunto activo y la relación directa activa sin introducir otra clase de identidad.
- La reflexividad no requiere almacenar bucles $t\to t$.

## Ejemplo

```mud
thing Kingdom as Place {
}

thing Egypt as Kingdom {
}
```

De esas cabeceras se derivan:

```mud
Egypt is Kingdom
Egypt is Place
Egypt is Egypt
```

La documentación debe presentar `is` como «es la misma `thing` o una especialización suya», no como «hereda directamente de».

## Verificación

1. Reflexividad: `T is T`.
2. Relación directa: `thing B as A {}` implica `B is A`.
3. Transitividad.
4. `thing N as C {}` declara verdadera `N is C` cuando ambas identidades son efectivas; `thing N {}` no añade antecesores.
5. Destruir y recrear `N` conserva la identidad.
6. Dos nombres distintos siguen siendo distintos aunque compartan antecesores y estado.
7. Separación de `as` e `is` en el AST.
