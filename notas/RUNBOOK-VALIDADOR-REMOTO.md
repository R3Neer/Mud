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
Versión Worker actual: d7c8a2b1-abc3-467d-939c-b36445df11a5
```

La migración `0001_initial.sql` está aplicada y `/health` respondió correctamente
el 2026-08-10. `ADAPTER_TOKEN` está configurado; su copia de smoke solo está en
TEMP y no se registra aquí. La variable GitHub `REPO_PATCHER_WORKER_URL` también
está configurada con la URL anterior.

## Bloqueos para el primer E2E

1. Publicar en `main` el workflow y el control actualmente locales.
2. Crear un token GitHub fine-grained limitado a `R3Neer/Mud`, permiso
   **Actions: read and write**.
3. Guardarlo sin imprimirlo:

   ```powershell
   Set-Location tooling/repo-patcher-validator-worker
   npx wrangler secret put GITHUB_DISPATCH_TOKEN
   ```

4. Confirmar que el actor del token figura en `GITHUB_ALLOWED_ACTORS`.
5. Hacer un dispatch verde controlado y verificar artifact, D1 y entrega exacta.

No se reutiliza automáticamente el token configurado en `gh`: convertir una
credencial local general en secreto de infraestructura requiere una decisión
explícita.

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
