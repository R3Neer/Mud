# Riesgos y restricciones

## Riesgos conceptuales

### Confundir representación semántica con independencia total de arquitectura

Toda semántica ejecutable presupone decisiones: identidad, atomicidad, concurrencia, error, tiempo y azar. MUD puede evitar React o una base de datos, pero no puede ser neutral respecto a su propio modelo operacional.

Mitigación: tratar esas decisiones como semántica explícita y probarlas con implementaciones diferentes.

### Prometer regeneración sin especificar las fronteras

El código generado puede necesitar integración manual. Si esa integración contiene reglas de dominio, `.mud` deja de ser la fuente de verdad.

Mitigación: contratos claros, zonas generadas, adaptadores explícitos y tests que comparen comportamiento.

### Lenguaje natural como fuente accidental

Si la IA “recuerda” una intención que no quedó en `.mud` o en metadatos versionados, el sistema adquiere semántica invisible.

Mitigación: después de cada operación, todo significado duradero debe quedar en fuente o decisión versionada.

### Sobreextensión temprana

La especificación combina compilación, runtime reactivo, búsqueda de estados, generación, integración con IA y Git. Implementarlo horizontalmente puede producir muchas piezas sin un contrato verificable.

Mitigación: núcleo vertical v0 y expansión por escenarios.

## Riesgos semánticos

### No determinismo accidental

Puede entrar por orden de mapas, recorrido de colecciones, resolución de declaraciones `using`, concurrencia o azar.

Mitigación: orden canónico, semillas explícitas, tests repetidos y comparación de IR y trazas byte a byte.

### No terminación

Reglas reactivas pueden oscilar o simular computación no acotada.

Mitigación: detección de ciclos, perfiles restringidos y diagnósticos que separen límite técnico de contradicción semántica.

### Estados intermedios inválidos

Validar en momentos distintos puede cambiar qué reglas se activan y qué acciones se aceptan.

Mitigación: semántica operacional pequeña por pasos y pruebas de trazas completas.

### Explosión combinatoria

Vinculaciones múltiples, dominios calculados, `allowed` y `eventually` pueden crecer exponencialmente.

Mitigación: índices, análisis conservador, presupuestos técnicos visibles y funciones avanzadas fuera del núcleo.

### Identidad inestable

Renombrar o mover namespaces cambia anclas y puede romper historial, referencias y estados persistidos.

Mitigación: migraciones de anclas de primera clase antes de permitir refactors automáticos.

## Riesgos de tooling

### Derivados desincronizados

Grafo, IR, código o documentación pueden no corresponder al mismo modelo.

Mitigación: huella del contenido fuente y versión de compilador en cada derivado; reconstrucción completa disponible.

### Commits contaminados

Una automatización puede incluir cambios previos del usuario o artefactos no relacionados.

Mitigación: índice o worktree aislado, allowlist de archivos y comparación del diff con el plan.

### Rollback incompleto

Editar fuente, generar archivos y ejecutar formateadores deja varias superficies que restaurar.

Mitigación: staging transaccional en un área temporal y publicación solo tras validar, en vez de “deshacer” mutaciones parciales.

### Diagnósticos insuficientes

Un `failed` sin cadena causal vuelve opaca la principal promesa de MUD.

Mitigación: códigos de error estables, anclas, rangos, ondas, lecturas/escrituras y sugerencias de corrección.

## Riesgos de evolución

### IR convertido en API accidental

Materializadores y plugins pueden acoplarse a detalles provisionales.

Mitigación: versión de esquema, compatibilidad declarada y pruebas de migración.

### Sintaxis congelada demasiado pronto

Optimizar por legibilidad antes de estabilizar la semántica genera migraciones costosas.

Mitigación: priorizar AST e IR claros; considerar la sintaxis experimental hasta validar ejemplos reales.

### Decisiones silenciosas en la implementación

Un desarrollador resolverá inevitables huecos si los tests lo exigen.

Mitigación: la implementación debe poder marcar “no especificado” y enlazar la pregunta abierta, no elegir un comportamiento arbitrario.

## Restricciones no negociables

- `.mud` es la única fuente de comportamiento de dominio.
- No se publican estados parciales.
- Un cambio inválido no produce commit.
- Los derivados son reconstruibles.
- Las reglas booleanas son puras.
- La escritura externa pasa por acciones.
- Participantes y `given` permanecen separados.
- El resultado no depende de orden accidental.
- Las cuestiones abiertas no se cierran sin procedencia.
- La implementación no puede ampliar silenciosamente el lenguaje.

## Señales de alarma durante el desarrollo

Detener y revisar si aparece cualquiera de estas situaciones:

- “Por ahora el orden será el que dé el diccionario”.
- “El generador puede añadir esta validación”.
- “Este caso devuelve falso porque es más cómodo”.
- “Guardaremos esta regla solo en el prompt”.
- “Ya migraremos las anclas después”.
- “El límite de ondas define el significado”.
- “El parser decidirá por contexto aunque la gramática sea ambigua”.
- “El commit también incluye estos cambios, pero parecen relacionados”.
