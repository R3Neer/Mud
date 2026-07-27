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
5. `create C N` crea un constructo concreto nuevo $N$ y lo relaciona con $C$ mediante el mismo `is` utilizado por una declaración estática.
6. La relación semántica `is` es reflexiva y transitiva.

La procedencia —declaración estática o creación durante la ejecución— y el ciclo de vida no originan dos clases distintas de entidad.

## Distinción formal necesaria

El token `is` cumple dos papeles sintácticos relacionados, pero el AST debe representarlos mediante nodos distintos:

- En una cabecera de `construct`, introduce una relación directa de especialización.
- En una expresión, consulta la relación semántica `is`.

Sea $R_{\mathrm{dir}}$ la relación de especialización directa. La formalización candidata del operador es:

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

La ecuación es una formalización candidata de la decisión, no cierra todavía si $R_{\mathrm{dir}}$ debe ser acíclica.

## Alternativas

### Clases separadas de instancias

Se descarta. Obliga a decidir si un constructo es clase u objeto y no representa que un constructo concreto pueda ser simultáneamente una cosa y un antecesor.

### Tokens diferentes para declaración y consulta

Podrían utilizarse palabras como `extends` e `is`. Se descarta por ahora porque ambos usos expresan la misma relación conceptual y sus posiciones gramaticales permiten distinguirlos.

### `is` estricto e irreflexivo

Se descarta. El autor ha decidido que `is` sea reflexivo. La especialización directa puede seguir siendo estricta aunque el operador consulte su clausura reflexiva.

## Consecuencias para el compilador

- El lexer necesita un único token `is`.
- El parser puede distinguir ambos usos por contexto: una cláusula de cabecera y una expresión no comparten posición gramatical.
- El AST debe evitar un nodo genérico ambiguo: la declaración añade una arista directa y la expresión construye una consulta booleana.
- La resolución debe comprobar que los nombres usados en una cláusula de especialización designan constructos.
- La especialización declarada puede analizarse estáticamente.
- `create` amplía durante la ejecución el conjunto de constructos y la relación directa, por lo que las consultas sobre constructos creados no siempre pueden reducirse completamente en compilación.
- La reflexividad no requiere almacenar bucles $c\to c$; se obtiene al consultar la clausura.

## Consecuencias para el uso humano

La reutilización de `is` es coherente si se explica la diferencia entre relación directa y relación derivada:

```mud
construct Kingdom is Place {
}

construct Egypt is Kingdom {
}
```

La primera cabecera introduce una relación directa. De ambas declaraciones se derivan:

```mud
Egypt is Kingdom
Egypt is Place
Egypt is Egypt
```

La última expresión puede sorprender si `is` se interpreta informalmente como «hereda directamente de». La documentación deberá presentarlo como «es el mismo constructo o una especialización suya» cuando se use como operador.

## Cuestiones no cerradas

- [[notas/08-preguntas-abiertas#Q-042 — Herencia desde un constructo concreto|Q-042]]: distinguir predeterminados heredados de estado mutable vivo.
- [[notas/08-preguntas-abiertas#Q-043 — Ciclos de especialización|Q-043]]: decidir si `is` es un orden parcial o solo un preorden.
- Tipado exacto de los operandos de `is`, especialmente el uso de constructos abstractos.
- Destrucción de un constructo que tenga descendientes vivos.

## Verificación futura

La suite deberá cubrir:

1. Reflexividad: `C is C`.
2. Relación directa: una cabecera `B is A` implica `B is A`.
3. Transitividad: `C is B` y `B is A` implican `C is A`.
4. Creación: `create C N` hace verdadera `N is C`.
5. Identidad: dos constructos creados por separado continúan siendo distintos aunque satisfagan los mismos ancestros y posean el mismo estado.
6. Separación sintáctica de la cláusula y el operador en el AST.
