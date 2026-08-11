---
title: "Runbook del validador remoto RepoPatcher"
status: vigente
date: 2026-08-11
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
Versión Worker actual: e4f09664-ed6e-4e05-8e39-75491dac339b
```

Las migraciones `0001_initial.sql` y `0002_staged_transport.sql` están aplicadas
y `/health` respondió correctamente el 2026-08-11 con el protocolo
`mud-repo-patcher-validator/v1`. `ADAPTER_TOKEN` está configurado; su copia de
smoke solo está en TEMP y no se registra aquí. `GITHUB_DISPATCH_TOKEN` es
fine-grained, está limitado a `R3Neer/Mud`, concede Actions de lectura/escritura y caduca el
2027-08-10. La variable GitHub `REPO_PATCHER_WORKER_URL` también está
configurada con la URL anterior.

El adaptador MCP estable usa además el secret `MCP_ROUTE_SECRET`. Su valor
forma el primer segmento de la URL del complemento y no se registra en Git ni
en este documento. Es independiente de `ADAPTER_TOKEN`, que solo protege las
rutas privadas antiguas.

La copia local de recuperación de la ruta MCP se conserva fuera del repositorio
en `%TEMP%\mud-repo-patcher-validator\mcp-route-secret.txt`. No debe añadirse a
Git ni reutilizarse como otra credencial.

La Fase 0 está cerrada. El transporte elegido es staging de archivos UTF-8
completos en lotes inmutables y finalización determinista en el Worker. La
sonda `mud-repo-patcher-mcp-probe`, versión
`22619184-837b-4a16-8c13-a8361f06e1ca`, verificó 3/3 paquetes representativos
desde ChatGPT. El adaptador estable ya incorpora ese contrato. Su smoke remoto
enumeró exactamente las cinco herramientas públicas y almacenó un lote UTF-8
de 39 bytes en 3,3 segundos mediante el cliente MCP de referencia. Worker 0.2.1
calculó y devolvió tamaño y SHA sin exigir identidad previa al cliente. Falta
actualizar la URL del complemento de ChatGPT e iniciar la serie E2E definitiva.

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

Después se detectó que `git diff` omitía archivos nuevos. El harness genera
ahora la evidencia completa mediante un índice Git temporal; la ejecución
`remote-e2e-20260810-04`, run `31431845357`, produjo un patch de 221 bytes con
la ruta creada. Esa ejecución tardó 91,1 segundos porque instalar PyYAML desde
la red consumió 32 segundos.

El workflow instala ahora el wheel fijado
`pyyaml-6.0.3-cp313-cp313-win_amd64.whl` después de verificar SHA-256 y sin
acceso a índice. La ejecución `remote-e2e-20260810-05`, run `31432380172`,
terminó en D1 en 59,2 segundos y volvió a entregar exactamente 377 bytes con
SHA-256 `77ca23adf7a98335b046ff579615cf44f30225438d6513f80328a446d50f486a`.

La ingestión se reanudó sobre el mismo artifact sin lanzar otro runner, lo que
verifica la recuperación idempotente de este tramo.

El 2026-08-11 se completó el primer ciclo íntegro desde ChatGPT a través del
MCP estable: request `remote-mcp-e2e-20260811-01`, run `31453323782`. El target
y el control fueron `9a1464e8b30d546132b8cdb3f8cfabc41a7fd61c`; D1 alcanzó
`succeeded` en 58,608 segundos con RepoPatcher 0.2.0. El ZIP entregado midió
422 bytes y su SHA-256 fue
`85a77745d400028bd3313185830109fba99f09222771dc32ce09bfed7d43f794`.
La verificación independiente confirmó igualdad byte por byte entre la descarga
y la copia del artifact, 16 checks verdes y reproducibilidad sin diferencias.
La conversación tardó cerca de dos minutos debido a ocho consultas, una
latencia de orquestación que debe medirse y reducirse por separado.

El run 03 no cuenta para el corte porque permitió descubrir que su diff estaba
incompleto. Quedan siete verdes, candidata roja, corrección, duplicados y carreras antes de
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

No retirar v6 hasta completar P7 y diez verdes E2E. El cron
de issues, ramas portadoras y scripts antiguos siguen siendo fallback mientras
el sistema nuevo no haya cumplido esa condición.
