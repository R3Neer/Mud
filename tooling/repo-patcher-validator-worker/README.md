# RepoPatcher validator Worker

Plano durable del validador remoto MUD. Este Worker no es todavía el adaptador
MCP final: mantiene ambos transportes privados hasta cerrar la Fase 0.

## Recursos

```text
Worker: mud-repo-patcher-validator
D1:     mud-repo-patcher-validator
R2:     mud-repo-patcher-validator
R2 dev: mud-repo-patcher-validator-preview
```

Los nombres y el ID D1 están declarados en `wrangler.jsonc`. Las credenciales
solo se almacenan como secrets de Workers.

## Fronteras HTTP

```text
GET  /health

POST /adapter/v1/candidates/zip
POST /adapter/v1/candidates/files
GET  /adapter/v1/requests/{request_id}
GET  /adapter/v1/requests/{request_id}/result
GET  /adapter/v1/requests/{request_id}/candidate

GET  /internal/v1/candidates/{request_id}
```

Las rutas `adapter` exigen `Authorization: Bearer ADAPTER_TOKEN`. Solo son la
interfaz privada que envolverá el MCP definitivo; no deben publicarse como una
API de usuario. La ruta `internal` acepta exclusivamente un JWT OIDC de GitHub
Actions con audiencia `mud-repo-patcher-worker` y claims ligados al registro
D1 exacto.

## GitHub

El camino sencillo usa un token fine-grained:

```powershell
npx wrangler secret put GITHUB_DISPATCH_TOKEN
```

Debe estar limitado a `R3Neer/Mud` y conceder **Actions: read and write**. El
actor del token debe aparecer en `GITHUB_ALLOWED_ACTORS` porque será el actor
del claim OIDC del workflow.

Como alternativa se pueden definir estos tres secrets y omitir el token
persistente:

```text
GITHUB_APP_ID
GITHUB_INSTALLATION_ID
GITHUB_APP_PRIVATE_KEY
```

La GitHub App debe estar instalada solo en el repositorio y tener Actions de
lectura/escritura. En ese caso `GITHUB_ALLOWED_ACTORS` debe contener el login
del bot que inicia el dispatch.

## Desarrollo

```powershell
npm install
npm run types
npm run typecheck
npm test
npm run migrate:local
npm run dev
```

Las pruebas se ejecutan dentro de `workerd` mediante el pool oficial de
Cloudflare y aplican las migraciones reales sobre D1 emulado. Cubren ZIP golden,
estado idempotente, transiciones, inmutabilidad R2, corrupción, claims OIDC y
la superficie pública mínima.

## Despliegue

```powershell
npm run types:check
npm run migrate:remote
npm run deploy
```

El despliegue no cierra la Fase 0 ni autoriza retirar v6. El secreto local de
smoke del adaptador se conserva fuera del repositorio en:

```text
%TEMP%\mud-repo-patcher-validator\adapter-token.txt
```

No debe copiarse a documentación, commits ni conversaciones.
