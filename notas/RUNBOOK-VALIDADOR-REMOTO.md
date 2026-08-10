---
title: "Runbook del validador remoto RepoPatcher"
status: vigente
date: 2026-08-10
---

# Runbook del validador remoto RepoPatcher

## Estado desplegado

```text
Cuenta Cloudflare: 17c938c850094bf1cf41ba3848666820
Worker: mud-repo-patcher-validator
URL: https://mud-repo-patcher-validator.mud-repo-patcher-mcp-probe.workers.dev
D1: 4522dc3f-483a-41ac-873c-b30eb73936cd (WEUR)
R2 producción: mud-repo-patcher-validator
R2 preview: mud-repo-patcher-validator-preview
Versión Worker actual: b0a7f1d8-bf58-4f1d-beb6-0c2ba6b35c22
```

La migración `0001_initial.sql` está aplicada y `/health` respondió correctamente
el 2026-08-10. `ADAPTER_TOKEN` está configurado; su copia de smoke solo está en
TEMP y no se registra aquí. `GITHUB_DISPATCH_TOKEN` es fine-grained, está
limitado a `R3Neer/Mud`, concede Actions de lectura/escritura y caduca el
2027-08-10. La variable GitHub `REPO_PATCHER_WORKER_URL` también está
configurada con la URL anterior.

## Primer E2E verde

El 2026-08-10 se completó:

- request `remote-e2e-20260810-03`;
- run `31430689484`;
- SHA de control y target
  `f56b69a460ffdb7c724376851b1d08d6410516cc`;
- Actions terminó correctamente en unos 52 segundos desde la aceptación;
- `result.json` declaró éxito y RepoPatcher `0.2.0`;
- el ZIP almacenado y el descargado midieron 364 bytes y compartieron SHA-256
  `97d68cfbbcddc5bdeea8b16d45649fe2332a58e903b9c38f7b6f49b762eee0dd`.

El primer procesamiento descubrió dos incompatibilidades ya corregidas:

- `package_size` se declara y transmite como cadena decimal;
- la descarga del artifact usa `redirect: manual`, único modo de rechazo
  explícito compatible con Workers, y falla si la URL firmada vuelve a redirigir.

La ingestión se reanudó sobre el mismo artifact sin lanzar otro runner, lo que
verifica la recuperación idempotente de este tramo.

Quedan nueve verdes, candidata roja, corrección, duplicados y carreras antes de
cumplir el criterio de corte. La credencial debe rotarse antes de su caducidad.

## Verificación local

```powershell
tooling/repo-patcher-validator/Test-RemoteWorkflow.ps1

Set-Location tooling/repo-patcher-validator-worker
npm run typecheck
npm test
npm run types:check
```

## Cloudflare

```powershell
npx wrangler whoami
npx wrangler d1 migrations list mud-repo-patcher-validator --remote
npx wrangler deployments list
npx wrangler tail
```

Una modificación de schema debe añadir una migración; no se edita una aplicada.
Antes de desplegar se regeneran tipos y se ejecutan las pruebas en `workerd`.

## Diagnóstico

- `dispatch_reconciliation_pending`: GitHub puede haber aceptado un dispatch
  cuya respuesta se perdió; repetir la consulta, no crear otro request igual.
- `dispatch_not_committed_yet`: carrera normal; el script Windows reintenta.
- `candidate_validation_failed`: candidata roja; leer `result.json` y
  `diagnostic.txt`.
- `infrastructure_error`: identidad, checkout, artifact, OIDC o servicio externo.
- `stored_object_corrupt`: detener entregas; no sobrescribir la key y auditar R2.
- `oidc_claim_mismatch`: comparar D1, run y configuración antes de reintentar.

## Corte

No retirar v6 hasta completar los pendientes P1–P7 y diez verdes E2E. El cron
de issues, ramas portadoras y scripts antiguos siguen siendo fallback mientras
el sistema nuevo no haya cumplido esa condición.
