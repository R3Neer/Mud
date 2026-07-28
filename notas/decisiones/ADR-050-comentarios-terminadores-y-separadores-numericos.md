# ADR-050 — Comentarios, terminadores y separadores numéricos

- Estado: Vigente; continuación de línea abierta
- Fecha: 2026-07-28
- Pregunta relacionada: Q-001
- Documentos afectados: léxico, gramática concreta, formateador

## Contexto

Estas reglas léxicas son independientes de la ontología y deben quedar fijadas sin mantener manualmente un catálogo paralelo de palabras clave.

## Decisión

### Comentarios

MUD admite:

1. comentario de línea desde `#` hasta el salto de línea;
2. comentario de línea cerrado por un segundo `#` antes del salto;
3. comentario multilínea delimitado por `###`.

```mud
soldiers = 1_000 # hasta fin de línea
soldiers = 1_000 # comentario # morale = 100
soldiers = ### comentario multilínea ### 1_000
```

Los comentarios multilínea no se anidan. El lexer reconoce `###` antes que `#`. Dentro de una cadena de `Text`, estos delimitadores no tienen significado léxico.

El contenido de un comentario no genera tokens, instrucciones ni terminadores. Después de retirarlo, el texto restante debe seguir siendo sintácticamente válido.

Un comentario de línea cerrado explícitamente no atraviesa un salto. Un delimitador multilínea sin pareja o los delimitadores sobrantes que dejen texto inválido producen diagnóstico.

### Terminadores

Una instrucción termina mediante `;` o un salto de línea que actúe como terminador. Q-001 debe definir cuándo un salto continúa una construcción incompleta en vez de terminarla; el formateador no puede decidirlo mediante sangría significativa.

### Separadores numéricos

`_` puede agrupar cifras para lectura, con grupos ordinarios de tres cifras. No altera el valor. El prefijo `r` se rige por D-034.

## Consecuencias

- Comentarios y terminadores deben resolverse en el lexer antes del parser.
- El resaltador puede implementarlos sin conocer el modelo semántico.
- El catálogo de palabras reservadas se generará desde la gramática consolidada.
- El catálogo distingue palabras reservadas de palabras contextuales conforme a D-054; que el parser reconozca `start`, `abstract`, `name` o `prefixes` en posiciones concretas no las convierte en palabras reservadas.

## Verificación

1. Las tres formas de comentario.
2. Delimitadores dentro de cadenas.
3. Prioridad de `###` y rechazo del anidamiento.
4. Símbolos sintácticos inocuos dentro de comentarios.
5. Terminación por `;` y por salto.
6. Literales con separadores válidos e inválidos.
