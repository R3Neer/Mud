# Estado durable de una validación

## Registro D1

La clave primaria es `request_id`. La identidad inmutable de una solicitud es
la tupla:

```text
(target_sha, package_sha256, package_size, trust_plugin, transport_kind)
```

Repetir un `request_id` con la misma tupla devuelve el estado existente.
Repetirlo con otra tupla es conflicto.

Campos persistidos:

```text
request_id primary key
schema_version
transport_kind
target_sha
package_sha256
package_size
trust_plugin
state
github_run_id nullable
github_run_url nullable
github_run_attempt
control_sha nullable
conclusion nullable
runtime_version nullable
result_object_key nullable
created_at
dispatched_at nullable
started_at nullable
completed_at nullable
expires_at
```

## Transiciones

Solo se aceptan actualizaciones condicionales desde el estado esperado:

```text
accepted → dispatching
dispatching → queued
queued → running
running → succeeded | failed | infrastructure_error
no terminal → expired
```

Los estados terminales no cambian. Asociar un mismo run, intento o resultado
dos veces es un no-op; asociar valores diferentes es conflicto.

## Carrera dispatch/D1

El request existe antes de llamar a GitHub. El run se asocia después de recibir
la respuesta `200` del dispatch. Si Actions solicita el ZIP antes de esa
asociación, el endpoint responde:

```http
HTTP/1.1 409 Conflict
Retry-After: 1
Content-Type: application/json

{"code":"dispatch_not_committed_yet","retryable":true}
```

El cliente reintenta en los tiempos acumulados 0, 1, 3, 7, 15 y 30 segundos.

