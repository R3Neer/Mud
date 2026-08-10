# MUD RepoPatcher validator

Este directorio contiene el plano de control confiable del validador remoto.
No contiene ni sustituye el runtime vendorizado de RepoPatcher.

## Frontera de versiones

- `control`: este directorio, obtenido desde `github.workflow_sha`;
- `target`: `tooling/repo-patcher-runtime` del commit exacto que se valida;
- `candidate`: ZIP inmutable identificado por SHA-256.

El harness comprueba que `repo_patcher.__file__` pertenece al runtime del
target. Los clones de validación nunca se usan como fuente de imports.

## Contratos

Los schemas de `contracts/` definen el intercambio estable entre Worker,
workflow y harness. No deciden si el adaptador MCP inicial recibe bytes base64
o archivos lógicos.

## Estado de implementación

La arquitectura está fijada en `notas/ADR-VALIDADOR-REMOTO.md`. La Fase 0 y el
corte de v6 siguen condicionados por `notas/PENDIENTES-VALIDADOR-REMOTO.md`.

## Harness

`validate_candidate.py` recibe dos checkouts ya verificados, crea
`validation/run-a/Mud` y `validation/run-b/Mud`, y produce un directorio de
evidencias. No hace red ni obtiene credenciales.

Ejemplo de ejecución por el workflow:

```powershell
python control/tooling/repo-patcher-validator/validate_candidate.py `
  --control-root control `
  --target-source target-source `
  --validation-root validation `
  --package candidate.zip `
  --request request.json `
  --output evidence `
  --target-sha $TargetSha `
  --control-sha $ControlSha `
  --workflow-run-id $RunId `
  --run-attempt $RunAttempt
```

El proceso devuelve `0` solo para una candidata verde. Tanto los fallos del
paquete como los de infraestructura producen `result.json`, diagnóstico,
transcript y todas las evidencias alcanzadas.

## Pruebas locales

```powershell
python tooling/repo-patcher-validator/test_snapshot.py
python tooling/repo-patcher-validator/test_validate_candidate.py
```

Las pruebas cubren archivos ignorados y binarios, índice físico y semántico,
historia requerida, candidata verde, consentimiento de plugin, efectos
laterales durante `explain` y divergencia de un generador aleatorio entre A/B.
