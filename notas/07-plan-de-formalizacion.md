# Plan de formalización e implementación temprana

El orden propuesto reduce primero la incertidumbre semántica y después amplía expresividad. Cada hito debe entregar ejemplos ejecutables, diagnósticos y decisiones registradas.

## Fase 0 — Gobierno de la especificación

Objetivo: disponer de una autoridad versionada y un modo explícito de cambiarla.

Entregables:

- Mover o convertir la especificación inicial en una especificación canónica dentro del repositorio.
- Adoptar estados de decisión y plantilla ADR.
- Numerar requisitos normativos.
- Elegir terminología normativa: “debe”, “puede”, “no puede”.
- Crear corpus inicial de ejemplos válidos e inválidos.

Salida: una modificación de la semántica ya no puede ocurrir solo en código.

## Fase 1 — Gramática del núcleo

Objetivo: hacer inequívoca la superficie incluida en v0.

Entregables:

- Especificación léxica.
- Gramática ejecutable.
- Reglas de terminadores y expresiones multilínea.
- AST de superficie con rangos.
- Parser con recuperación y snapshots de errores.
- Formateo canónico de las formas incluidas.

Salida: todos los ejemplos v0 se parsean o fallan de forma predecible.

## Fase 2 — Modelo semántico estático

Objetivo: resolver qué significa un programa sin ejecutarlo.

Entregables:

- Namespaces, imports exactos y anclas.
- Tabla de símbolos.
- Tipos básicos y conversiones v0.
- Mutabilidad y dominios.
- Variantes de reglas y acciones.
- Análisis de pureza.
- IR versionado.
- Índice y grafo mínimos.

Salida: `mud check` distingue modelos válidos y emite un IR determinista.

## Fase 3 — Runtime transaccional

Objetivo: ejecutar acciones elementales sin reactividad.

Entregables:

- Representación de estado y snapshot.
- Evaluador de expresiones.
- Aplicador de efectos.
- `given`, `if`, `then`, `after` y `old`.
- Dominios e invariantes.
- `accepted`, `rejected`, `failed`.
- Rollback y explicación.

Salida: el escenario de reclutamiento cumple todas las pruebas.

## Fase 4 — Causalidad por ondas

Objetivo: demostrar reactividad determinista.

Entregables:

- Vinculaciones `for` v0.
- Memoria de `when`.
- Pulsos `changes`.
- Snapshots por onda.
- Combinación de efectos.
- Detección de conflictos y ciclos.
- Traza causal.

Salida: el escenario de la puerta y un caso de conflicto son reproducibles.

## Fase 5 — Operaciones semánticas y Git

Objetivo: cambiar el modelo con el mismo rigor con que se ejecuta.

Entregables:

- Consulta por ancla.
- Informe de impacto.
- Plan estructurado CREATE/UPDATE/RETIRE.
- Aplicación aislada de parche.
- Regeneración de IR y grafo.
- Validación, diff y política de commit.
- Restauración ante fallo.

Salida: una petición controlada en lenguaje natural puede transformarse en un commit semántico verificable.

## Fase 6 — Expansión estructural

Orden recomendado:

1. Participantes múltiples.
2. Colecciones y cardinalidades.
3. Diccionarios.
4. Aliases.
5. Familias cerradas.
6. Herencia simple.
7. Campos calculados.
8. Acciones compuestas.
9. Creación y destrucción.
10. Herencia múltiple.

Cada incorporación debe extender la matriz de conflictos, el grafo, IR y tests.

## Fase 7 — Cantidades y azar

Entregables:

- Intervalos completos.
- Magnitudes y unidades.
- Magnitudes de punto.
- Redondeo y conversiones estrechas.
- Modelo determinista de semillas y subsemillas.
- Campos estocásticos y restricciones de lectura.

Estas funciones necesitan decisiones numéricas y de reproducibilidad antes de implementarse.

## Fase 8 — Especulación y alcanzabilidad

Primero `allowed`, reutilizando el runtime transaccional sobre snapshots descartables. Después `eventually`, únicamente para perfiles de mundo que el analizador pueda demostrar finitos.

No se debería empezar `eventually` hasta tener:

- Serialización canónica de estado relevante.
- Enumeración finita de acciones.
- Análisis de creación acotada.
- Terminación de cada transición.
- Presupuesto y diagnóstico de exploración.

## Estrategia de pruebas

Cada fase mantiene cuatro familias:

- **Conformidad**: ejemplos normativos válidos.
- **Diagnósticos**: ejemplos inválidos con código y localización estable.
- **Propiedades**: determinismo, atomicidad, idempotencia de formato y reconstrucción.
- **Diferenciales**: AST/IR/grafo esperado y comparación entre versiones.

Los tests generados son derivados; las pruebas de conformidad de la especificación son activos normativos y deben versionarse.

## Decisiones tecnológicas que pueden esperar

- Lenguaje de implementación definitivo.
- Framework del plugin.
- Base de datos del grafo.
- Persistencia runtime.
- Generador TypeScript sofisticado.

Para v0 basta una implementación que favorezca tipos algebraicos, parser mantenible, tests rápidos y serialización determinista. La elección tecnológica no debe alterar la semántica.

## Primeras tareas concretas

1. Confirmar el alcance v0.
2. Elegir los ejemplos canónicos.
3. Resolver preguntas P0.
4. Escribir EBNF del subconjunto.
5. Definir esquemas AST e IR v0.
6. Definir catálogo de diagnósticos v0.
7. Crear una CLI vacía con `check`.
8. Implementar el primer camino `construct → campo → ancla → IR`.
9. Añadir una característica por prueba vertical, no por capas gigantes.

