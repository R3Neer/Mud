# ADR-053 — Operador semántico y flujo de autoría

- Estado: Vigente como política de producto
- Fecha: 2026-07-28
- Preguntas relacionadas: Q-008, Q-015, Q-036, Q-039, Q-040
- Documentos afectados: cambios semánticos, Git, tooling del operador

## Contexto

La interacción en lenguaje natural debe transformar el modelo mediante operaciones comprobables. No puede ocultar reglas nuevas en la IA ni editar `.mud` sin analizar consecuencias.

## Decisión

Antes de modificar, el operador clasifica la petición al menos por:

- consulta o cambio;
- `CREATE`, `UPDATE`, `RETIRE` o migración;
- cambio estructural, de API, causal, de vinculación, dominio, tipo, azar, invariante, admisibilidad o alcanzabilidad;
- ambigua, incompleta, fuera de alcance o intento de eludir restricciones.

Puede aplicar únicamente inferencias mecánicas ya definidas por el lenguaje, como cardinalidad `[1]`, ausencia de `given` cuando no se necesitan valores, `empty`, órdenes canónicos y finitud derivable. No inventa participantes, `given`, dominios, reglas, acciones, `after`, `always` ni significado de `allowed` o `eventually`.

El flujo de una mutación es:

1. capturar estado Git y versiones;
2. resolver intención, nombres y anclas;
3. consultar decisiones, dudas y grafo;
4. calcular impacto y ambigüedades;
5. producir un plan de operaciones;
6. preparar restauración aislada;
7. editar fuente y metadatos autorizados;
8. formatear, compilar y validar;
9. reconstruir grafo e IR;
10. materializar y ejecutar pruebas;
11. contrastar impacto previsto y observado;
12. inspeccionar diff, rutas y cambios ajenos;
13. crear un commit atómico.

Un fallo anterior al commit restaura el estado inicial. Un worktree sucio no autoriza a modificar ni descartar trabajo ajeno.

Las consultas puras `READ` no crean commit. Si una consulta cierra una duda o modifica documentación, esa modificación es `UPDATE`, no `READ`.

## Consecuencias

- Un plugin para Codex es una interfaz posible sobre servicios de consulta, gestión de reglas y gestión de acciones; sus nombres históricos no son API normativa.
- La agenda conserva estado, procedencia y preguntas, pero no añade semántica al mundo.
- `RETIRE`, permisos de aprobación y el contrato de explicación siguen abiertos.

## Verificación

1. Clasificación multietiqueta de peticiones representativas.
2. Rechazo de una inferencia de dominio no autorizada.
3. Restauración tras fallo en cualquier fase.
4. Commit limitado al plan y ausencia de commit para `READ`.
5. Detección de impacto inesperado antes de confirmar.
