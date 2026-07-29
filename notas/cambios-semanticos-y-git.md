# Cambios semánticos y Git

Este documento describe el protocolo de seguridad alrededor de una modificación del modelo. La autoridad del flujo pertenece a [[notas/decisiones/ADR-012-cambios-semanticos-atomicos|D-012]], [[notas/decisiones/ADR-053-operador-semantico-y-flujo-de-autoria|D-053]] y [[gobierno/POLITICA-DE-COMMITS|la política de commits]]. Es distinto de ejecutar una acción dentro de un mundo: aquí se cambia la definición `.mud` del mundo.

## Dos clases de transacción

MUD contiene dos atomicidades relacionadas pero diferentes:

1. **Transacción runtime**: una acción transforma una instancia del mundo o revierte.
2. **Transacción de autoría**: una petición transforma los archivos `.mud` y sus derivados o revierte.

Ambas comparten la filosofía de no publicar estados parciales, pero tienen participantes, validaciones y diagnósticos distintos.

## Clasificación de una petición

Antes de modificar, el operador debe decidir si la petición es:

- Consulta.
- Creación, actualización, retirada o migración.
- Cambio estructural, de API, causal, de dominio o de vinculación.
- Cambio de aleatoriedad, invariante, admisibilidad o alcanzabilidad.
- Ambigua, incompleta, fuera de alcance o intento de eludir restricciones.

Una petición puede recibir varias etiquetas: una operación `UPDATE` puede ser además cambio de API y cambio causal.

## Plan de operaciones

La IA debería producir primero un artefacto estructurado y revisable:

```yaml
intent: "Limitar el reclutamiento diario"
operations:
  - kind: UPDATE
    anchor: action::warfare.armies.Recruit
    change: add-precondition
reads:
  - thing::warfare.armies.Kingdom::lastRecruitmentDate
expected_impacts:
  - rule::warfare.armies.CanRecruit
open_questions: []
```

El formato exacto está abierto, pero debe distinguir la intención humana, las operaciones, las anclas leídas y las consecuencias previstas.

## Flujo atómico

1. Capturar el estado Git y la versión del compilador.
2. Clasificar la petición.
3. Resolver nombres a anclas.
4. Consultar dependencias directas y transitivas.
5. Detectar ambigüedades y decisiones abiertas.
6. Construir el plan de operaciones.
7. Preparar un punto de restauración aislado.
8. Aplicar cambios solo a `.mud` y metadatos autorizados.
9. Formatear.
10. Compilar y validar.
11. Reconstruir grafo e IR.
12. Regenerar materializaciones afectadas.
13. Ejecutar tests.
14. Comparar impacto previsto con impacto observado.
15. Inspeccionar el diff.
16. Confirmar que no se incluyeron cambios ajenos.
17. Crear un commit atómico.

Si falla cualquier paso anterior al commit, se restaura exactamente el estado inicial de la transacción.

Este flujo, la clasificación y el límite de inferencias del operador quedan consolidados en [[notas/decisiones/ADR-053-operador-semantico-y-flujo-de-autoria|D-053]].

## Política para repositorios con cambios previos

El operador no puede asumir que un worktree sucio le pertenece. Opciones seguras:

- Rechazar la mutación hasta aislar cambios.
- Usar un worktree o índice temporal.
- Limitar el parche a archivos y hunks conocidos.

Nunca debe hacer reset destructivo de trabajo ajeno. El commit final solo incluye cambios que pertenecen al plan semántico.

## Commits semánticos

Un commit debería responder:

- Qué intención se atendió.
- Qué operaciones se realizaron.
- Qué anclas cambiaron.
- Si hubo cambio de API, causalidad o dominio.
- Qué validaciones se ejecutaron.
- Qué decisiones o migraciones están relacionadas.

Ejemplo de mensaje:

```text
UPDATE action::warfare.armies.Recruit recruitment limit

Operations:
- UPDATE action::warfare.armies.Recruit
- CREATE rule::warfare.armies.CanRecruitToday

Impact:
- API: unchanged
- Causality: precondition added
- Data migration: none
```

El formato general de los commits se rige por [[gobierno/POLITICA-DE-COMMITS|la política de commits]]. Antes de automatizar parsers de historial debe fijarse además un contrato estable para los campos semánticos legibles por máquina.

## ¿Debe `READ` crear un commit?

No. Una consulta puede quedar en logs de auditoría, pero no modifica la fuente semántica. D-012, D-053 y la política de commits reservan los commits para CREATE, UPDATE, RETIRE, migraciones u otras modificaciones persistentes, no para una lectura aislada.

Si se desea versionar conocimiento obtenido durante una consulta —por ejemplo, cerrar una decisión— eso sería un `UPDATE` sobre metadatos de especificación, no un `READ`.

## Retirada frente a borrado

`RETIRE` sugiere una semántica más rica que borrar texto:

- Comprobar referencias.
- Impedir nuevas dependencias.
- Registrar reemplazo o motivo.
- Permitir migración de anclas.
- Eliminar físicamente solo cuando sea seguro.

La semántica exacta sigue abierta en [[notas/preguntas/Q-015-retirada|Q-015]]. Hasta resolverla, el operador no debe equiparar automáticamente `RETIRE` con eliminar una declaración.

## Validación del impacto

El impacto previsto debe contrastarse con:

- Anclas añadidas, modificadas, retiradas o migradas.
- Cambios de firma de reglas y acciones.
- Lecturas y escrituras nuevas.
- Alteraciones de dominios y cardinalidades.
- Ciclos nuevos.
- Cambios de estocasticidad.
- Materializaciones y tests afectados.

Una diferencia inesperada entre impacto previsto y real debe detener el commit o pedir revisión.

## Reproducibilidad

El commit debería permitir reconstruir:

- Versión de la especificación.
- Versión del compilador y esquema IR.
- Modelo `.mud`.
- Derivados relevantes.
- Resultados de validación.

No todos los derivados necesitan versionarse. La decisión debe basarse en coste, auditabilidad y facilidad de reconstrucción, manteniendo claro que nunca son autoridad semántica.
