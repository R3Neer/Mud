# RepoPatcher validator Worker

Plano durable y adaptador MCP estable del validador remoto MUD. La Fase 0 eligió
archivos UTF-8 completos por lotes inmutables; el Worker construye el ZIP
determinista y entrega exactamente el objeto que obtuvo verde.

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

POST /<MCP_ROUTE_SECRET>/mcp
GET  /<MCP_ROUTE_SECRET>/downloads/{request_id}/candidate.zip
GET  /<MCP_ROUTE_SECRET>/downloads/{request_id}/evidence.zip

POST /adapter/v1/candidates/zip
POST /adapter/v1/candidates/files
GET  /adapter/v1/requests/{request_id}
GET  /adapter/v1/requests/{request_id}/result
GET  /adapter/v1/requests/{request_id}/candidate

GET  /internal/v1/candidates/{request_id}
```

La ruta MCP usa Streamable HTTP y un segmento secreto almacenado exclusivamente
como `MCP_ROUTE_SECRET`. Las rutas de descarga comparten ese segmento y vuelven
a verificar el objeto R2 antes de servirlo. Las rutas `adapter` antiguas exigen
`Authorization: Bearer ADAPTER_TOKEN` y se conservan temporalmente para los E2E
anteriores; no son API de usuario. La ruta `internal` acepta exclusivamente un
JWT OIDC de GitHub Actions con audiencia `mud-repo-patcher-worker` y claims
ligados al registro D1 exacto.

## Herramientas MCP

```text
stage_candidate_files
submit_candidate
await_validation
read_validation_evidence
get_validated_candidate
```

`stage_candidate_files` acepta lotes de hasta 32 archivos completos y 24 KiB
de contenido textual. El Worker calcula y devuelve tamaño UTF-8 y SHA-256 de
cada entrada. El llamante puede aportar ambos valores como aserciones
opcionales cuando ya posee una identidad previa; no necesita calcularlos para
texto que acaba de generar. Los lotes son inmutables y un archivo nunca se
divide entre llamadas.

`submit_candidate` recibe los `batch_ids` explícitos, reconstruye y revalida
todos los archivos, crea el ZIP determinista y despacha la validación. El valor
persistido de `transport_kind` es `files_staged_v1`. Las tres operaciones de
lectura posteriores usan estado durable; ninguna mantiene una conexión HTTP
abierta mientras se ejecuta GitHub Actions.

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
npm run smoke:mcp -- --stage
```

Las pruebas se ejecutan dentro de `workerd` mediante el pool oficial de
Cloudflare y aplican las migraciones reales sobre D1 emulado. Cubren ZIP golden,
staging UTF-8, catálogo MCP, estado idempotente, transiciones, inmutabilidad R2,
corrupción, claims OIDC y la superficie pública mínima.

El smoke usa por defecto `http://127.0.0.1:8787/local-validator/mcp`. Para una
instancia remota se pasa la URL completa mediante la variable temporal
`MUD_VALIDATOR_MCP_URL`; el script nunca la imprime sin redactar.

## Despliegue

```powershell
npm run types:check
npm run migrate:remote
npm run deploy
```

Cada instancia MCP debe configurar de forma segura:

```powershell
npx wrangler secret put MCP_ROUTE_SECRET
```

La instancia de producción quedó desplegada el 2026-08-11 como versión
`f4c4d549-d01d-43d4-857c-5aecbf8e3c7a`. El smoke remoto verificó el catálogo
exacto de cinco herramientas y un lote staged de 39 bytes.

El despliegue no autoriza retirar v6. El secreto local de smoke del adaptador
antiguo se conserva fuera del repositorio en:

```text
%TEMP%\mud-repo-patcher-validator\adapter-token.txt
```

No debe copiarse a documentación, commits ni conversaciones.
