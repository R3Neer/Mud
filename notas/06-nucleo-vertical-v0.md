# Núcleo vertical v0

## Objetivo

Construir el corte más pequeño que demuestre la tesis completa:

```text
.mud
→ parsear
→ resolver anclas
→ validar
→ producir IR y grafo
→ ejecutar una acción transaccional
→ explicar el resultado
→ aplicar un cambio semántico y validarlo
```

No es “la primera parte del parser”; es una prueba vertical de la fuente de verdad al comportamiento observable.

## Escenario canónico

Un reino tiene tesoro y soldados. Puede reclutar una cantidad dentro de un dominio, si tiene dinero. El reclutamiento reduce el tesoro y aumenta soldados. Un invariante impide tesoro negativo y una poscondición comprueba que no se pierdan soldados.

Este escenario cubre:

- Una `thing`.
- Campos básicos y `mut`.
- Dominios.
- Una regla booleana pura.
- Una acción con participante `on`.
- Un valor `given`.
- `if`, `then`, `after` y `old`.
- Una regla `always`.
- `accepted`, `rejected` y `failed`.
- Rollback.
- Anclas, lecturas y escrituras.

Un segundo escenario pequeño, como una puerta que se abre al desbloquearse, añade una única regla reactiva y demuestra dos ondas.

## Sintaxis incluida

- Namespaces derivados de carpetas.
- Un archivo o varios archivos por namespace.
- Imports exactos.
- `thing` concreta sin especialización.
- Tipos `Bool`, `Natural`, `Integer`, `Number`, `Rumber`, `Text` y `Money`.
- Campos almacenados, `mut` y dominios de intervalos cerrados.
- Regla booleana con un participante.
- Regla reactiva con un participante.
- Regla `always` con un participante.
- Acción elemental con un participante.
- `given`, `if`, `then`, `after` y `old`.
- Asignaciones `=`, `+=` y `-=`.
- Expresiones aritméticas, comparación y lógica.
- Comentarios de línea simples.
- Salto de línea y `;` como terminadores una vez formalizada su interacción.

## Semántica incluida

- Identidad estable de declaraciones.
- Resolución de nombres sin declaraciones `using` recursivas.
- Tipado estático.
- Pureza de reglas booleanas.
- Comprobación de mutabilidad.
- Dominios de campos y `given`.
- Raíz atómica.
- Reglas reactivas por ondas.
- Detección básica de conflicto.
- Reglas `always`.
- `after` y `old`.
- Confirmación o rollback.
- Resultado y explicación causal.

## Artefactos incluidos

- CLI `check`.
- Formateador mínimo o impresión canónica.
- AST con rangos de fuente.
- IR JSON versionado.
- Índice de anclas.
- Grafo con `DECLARES_FIELD`, `READS`, `WRITES`, `IF_READS`, `AFTER_READS` y dependencias de reglas.
- Runtime en memoria.
- Fixtures de estado.
- Tests positivos, negativos y de rollback.

## Fuera de v0

- Herencia, especialmente múltiple.
- Aliases nominales estructurales, inmutables y estáticos.
- Familias cerradas.
- Colecciones y diccionarios.
- Creación y destrucción runtime.
- Acciones compuestas.
- Magnitudes y unidades.
- Campos calculados.
- Dominios dinámicos.
- `allowed`.
- `eventually`.
- Aleatoriedad.
- Imports recursivos.
- Participantes múltiples y vinculación nombrada.
- Comentarios cerrados con `#...#` y multilínea `###...###`.
- Materialización TypeScript completa.
- Integración conversacional automática.

Excluirlos de v0 no revoca su diseño; impide que la incertidumbre avanzada bloquee la validación del núcleo.

## Pruebas de aceptación

### Compilación

- Un modelo válido produce siempre el mismo IR.
- Un nombre ambiguo, escritura sin `mut` o tipo incompatible produce diagnóstico localizado.
- Dos declaraciones con la misma ancla se rechazan.

### Ejecución

- Reclutamiento válido termina en `accepted`.
- Cantidad fuera de dominio termina en `rejected` sin evaluar `if`.
- Fondos insuficientes terminan en `rejected`.
- Poscondición falsa restaura el estado anterior.
- Invariante incumplida termina en `failed` y restaura.
- La puerta desbloqueada activa una reacción en la onda siguiente.
- Un ciclo reactivo de prueba falla con explicación.

### Trazabilidad

- El IR enumera participantes y `given` por separado.
- El grafo identifica campos leídos y escritos.
- La explicación nombra acción raíz, reglas activadas, ondas y motivo del resultado.

### Cambio semántico

- Añadir un límite al dominio muestra impacto antes de editar.
- El parche modifica solo las anclas previstas.
- Un cambio inválido no deja archivos ni derivados parciales.

## Criterio de finalización

v0 termina cuando los dos escenarios canónicos pasan por el flujo completo y los resultados son deterministas. No termina por número de módulos implementados ni por porcentaje de la gramática inicial.
