---
title: "Protocolo interno del validador remoto RepoPatcher"
status: vigente
date: 2026-08-11
---

# Protocolo interno del validador remoto RepoPatcher

## Identidad

La identidad de una solicitud es:

```text
request_id
target_sha
package_sha256
package_size
trust_plugin
transport_kind
```

El Worker calcula SHA-256 y tamaño. Un `request_id` repetido con la misma
identidad devuelve el estado existente; con otra identidad devuelve conflicto.

El protocolo de entrada es `files-staged-v1` y el valor persistido de
`transport_kind` es `files_staged_v1`. Después de la entrada produce
exactamente el objeto:

```text
candidates/<package_sha256>.zip
```

Una creación R2 usa `If-None-Match: *`. Si pierde una carrera, vuelve a leer y
verifica bytes, tamaño, hash y metadatos antes de reutilizar el objeto.

## Entrada MCP v1

`stage_candidate_files` recibe un `request_id`, un `batch_id` y archivos UTF-8
completos. Cada archivo incluye ruta POSIX relativa, contenido, tamaño en bytes
y SHA-256. El Worker valida estos valores antes de persistir un lote inmutable.
Un archivo nunca se divide entre lotes y un lote repetido con otros datos es
conflicto.

`submit_candidate` recibe los identificadores explícitos de los lotes, el
número total esperado de archivos, `target_sha` y `trust_plugin`. Relee y
verifica todos los lotes, rechaza rutas duplicadas o colisiones sin distinguir
mayúsculas y construye el ZIP con orden, timestamp y metadatos fijos. Solo
entonces calcula `package_sha256`, almacena `candidates/<sha256>.zip`, crea el
estado durable y hace dispatch.

Los recursos binarios arbitrarios y el base64 fragmentado quedan fuera de v1.
Las operaciones posteriores son `await_validation`,
`read_validation_evidence` y `get_validated_candidate`.

## Dispatch

El registro D1 se crea como `accepted` antes de tocar GitHub. Solo la invocación
que gana `accepted → dispatching` puede llamar a `workflow_dispatch`. La
respuesta normal `200` aporta el run ID directamente. Después se consulta el
run y se fija `control_sha`.

Si se pierde la respuesta, una repetición no vuelve a disparar a ciegas: busca
el run por workflow, título exacto derivado de `request_id`, evento, rama y
ventana temporal. Una coincidencia se asocia; cero coincidencias devuelven un
estado reintentable; más de una es conflicto.

## Carrera de descarga

El runner presenta primero un OIDC válido. Si firma, issuer y audiencia son
correctos pero D1 aún no contiene run y control SHA, recibe:

```http
409 Conflict
Retry-After: 1

{"code":"dispatch_not_committed_yet","retryable":true}
```

El script Windows espera 0, 1, 2, 4, 8 y 15 segundos: tiempos acumulados 0, 1,
3, 7, 15 y 30. Después verifica nuevamente hash y tamaño antes de construir
`request.json`.

## Resultado

La consulta de estado usa el run ID persistido. Cuando GitHub termina, el
Worker descarga el artifact exacto, conserva su ZIP en R2 y extrae únicamente
`result.json`, `candidate.zip` e `infrastructure.json` con límites estrictos.

Un resultado estructurado debe coincidir en:

```text
request_id
workflow_run_id
run_attempt
control_sha
target_sha
package_sha256
package_size
protocol
```

Un verde exige además RepoPatcher `0.2.0`, `result.conclusion == success` y
conclusión GitHub `success`. El ZIP del artifact debe coincidir con el objeto
R2. La entrega lee después ese mismo objeto; nunca reconstruye otro.

## Expiración

Las solicitudes no terminales tienen vencimiento a catorce días. La siguiente
consulta posterior al vencimiento las marca `expired`. Los objetos se conservan
durante esta etapa de pruebas; la política de borrado R2 se fijará antes del
corte de v6.
