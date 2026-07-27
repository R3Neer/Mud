# ADR-014 — Ontología unificada de constructos

- Estado: Vigente
- Fecha: 2026-07-27
- Preguntas: [[notas/08-preguntas-abiertas#Q-041 — Ontología de constructos|Q-041]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[especificacion/04-modelo-matematico]], futuro `11-constructos.md`

## Contexto

La especificación inicial afirma a la vez que `construct` representa cosas, conceptos, categorías, entidades estáticas y entidades runtime. También utiliza vocabulario de «instancias runtime», que puede sugerir una separación entre clases y objetos.

Esa separación no corresponde al modelo conceptual de MUD. Una formalización basada en una función que asignase a cada objeto su clase introduciría dos dominios que el lenguaje no posee.

## Decisión

MUD tiene un único dominio conceptual de constructos.

1. Un constructo no tiene instancias.
2. Todo constructo posee identidad semántica.
3. Todo constructo concreto denota además una cosa concreta con estado propio y puede servir como antecesor de otros constructos.
4. Un constructo abstracto pertenece al mismo dominio y posee identidad, pero no denota por sí mismo una cosa concreta con estado propio.
5. `create` activa una identidad reservada y puede añadir cero o varias relaciones directas mediante `from`, según [[notas/decisiones/ADR-016-creacion-generalizada-de-constructos|ADR-016]].
6. La relación semántica `is` es reflexiva y transitiva.

La procedencia —declaración estática o creación durante la ejecución— y el ciclo de vida no originan dos clases distintas de entidad.

## Distinción formal necesaria

El token `is` cumple dos papeles sintácticos relacionados, pero el AST debe representarlos mediante nodos distintos:

- En una cabecera de `construct`, introduce una relación directa de especialización.
- En una expresión, consulta la relación semántica `is`.

Sea $R_{\mathrm{dir}}$ la relación de especialización directa. [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]] completa la decisión con la formalización:

$$
R_{\mathsf{is}}
:=
R_{\mathrm{dir}}^*
$$

La clausura reflexiva y transitiva explica simultáneamente:

$$
c\mathrel{R_{\mathsf{is}}}c
$$

y:

$$
c_1\mathrel{R_{\mathrm{dir}}}c_2
\land
c_2\mathrel{R_{\mathrm{dir}}}c_3
\Rightarrow
c_1\mathrel{R_{\mathsf{is}}}c_3
$$

La relación directa es acíclica; por tanto, su clausura reflexiva y transitiva es un orden parcial.

## Alternativas

### Clases separadas de instancias

Se descarta. Obliga a decidir si un constructo es clase u objeto y no representa que un constructo concreto pueda ser simultáneamente una cosa y un antecesor.

### Tokens diferentes para declaración y consulta

Esta alternativa se descartó inicialmente, pero fue adoptada después por [[notas/decisiones/ADR-018-from-declara-is-consulta|ADR-018]]: `from` declara antecesores directos e `is` consulta la relación reflexiva y transitiva.

### `is` estricto e irreflexivo

Se descarta. El autor ha decidido que `is` sea reflexivo. La especialización directa puede seguir siendo estricta aunque el operador consulte su clausura reflexiva.

## Consecuencias para el compilador

- El lexer distingue `from` e `is`.
- El parser usa `from` en cabeceras e `is` en expresiones.
- El AST representa la lista de antecesores en la declaración y la consulta booleana en `IsExpression`.
- La resolución debe comprobar que los nombres usados en una cláusula de especialización designan constructos.
- La especialización declarada puede analizarse estáticamente.
- `create` amplía durante la ejecución el conjunto activo y la relación directa activa. Aunque la identidad y su descriptor estén resueltos, una consulta que exija presencia no siempre puede reducirse en compilación.
- La reflexividad no requiere almacenar bucles $c\to c$; se obtiene al consultar la clausura.

## Consecuencias para el uso humano

La sintaxis separa la declaración directa de la consulta derivada:

```mud
construct Kingdom from Place {
}

construct Egypt from Kingdom {
}
```

Las cabeceras con `from` introducen relaciones directas. De ambas declaraciones se derivan:

```mud
Egypt is Kingdom
Egypt is Place
Egypt is Egypt
```

La última expresión puede sorprender si `is` se interpreta informalmente como «hereda directamente de». La documentación deberá presentarlo como «es el mismo constructo o una especialización suya» cuando se use como operador.

## Decisiones posteriores y cuestiones no cerradas

- [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]] fija que los estados son independientes, que solo se heredan esquema y predeterminados, y que `is` es un orden parcial.
- Tipado exacto de los operandos de `is`, especialmente el uso de constructos abstractos.
- Destrucción de un constructo que tenga descendientes vivos.

## Verificación futura

La suite deberá cubrir:

1. Reflexividad: `C is C`.
2. Relación directa: una cabecera `construct B from A` implica `B is A`.
3. Transitividad: `C is B` y `B is A` implican `C is A`.
4. Creación: `create construct N from C {}` hace verdadera `N is C`, mientras `create construct N {}` no añade antecesores.
5. Identidad reservada: destruir y recrear `N` reactiva la misma identidad.
6. Identidad distinta: dos nombres reservados diferentes continúan siendo distintos aunque satisfagan los mismos ancestros y posean el mismo estado.
7. Separación sintáctica de `from` y del operador `is` en el AST.
