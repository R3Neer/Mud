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

