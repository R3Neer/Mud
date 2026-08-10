---
title: "Fase 0: transporte MCP de paquetes RepoPatcher"
status: en-prueba
date: 2026-08-09
---

# Fase 0: transporte MCP de paquetes RepoPatcher

## Propósito

Esta prueba decide empíricamente cómo transferirá ChatGPT una candidata al futuro validador. Hasta cerrarla no se implementarán D1, GitHub Actions, OIDC ni el harness de validación fuerte.

El prototipo está en `tooling/repo-patcher-mcp-probe/` y ofrece los dos transportes candidatos simultáneamente.

## Criterio de identidad

En cada intento deben coincidir:

```text
SHA-256 calculado antes del envío
== SHA-256 devuelto por el Worker
== SHA-256 de la descarga recibida
```

También debe coincidir el tamaño exacto.

## Matriz pendiente

Cada celda `Envíos exactos` y `Descargas exactas` debe registrar tres intentos independientes.

| Transporte | Tamaño o forma | Envíos exactos | Descargas exactas | Latencia mediana |
| --- | --- | ---: | ---: | ---: |
| ZIP base64 | 1 KiB | pendiente | pendiente | pendiente |
| ZIP base64 | 16 KiB | pendiente | pendiente | pendiente |
| ZIP base64 | 64 KiB | pendiente | pendiente | pendiente |
| ZIP base64 | 128 KiB | pendiente | pendiente | pendiente |
| ZIP base64 | 256 KiB | pendiente | pendiente | pendiente |
| files | paquete pequeño | pendiente | pendiente | pendiente |
| files | paquete MUD representativo | pendiente | pendiente | pendiente |
| files | binario + Unicode | pendiente | pendiente | pendiente |

Esta tabla solo se completará con llamadas iniciadas por ChatGPT Plus. Las pruebas locales del mismo protocolo no se mezclarán con la evidencia que decide el transporte.

## Validación local del prototipo

El 2026-08-09 se ejecutó la matriz completa mediante el cliente MCP 2.0 contra el Worker local y su emulación R2. Cada intento hizo:

1. negociación MCP Streamable HTTP;
2. llamada real a la herramienta;
3. almacenamiento o construcción del ZIP;
4. descarga mediante el enlace devuelto;
5. comprobación de tamaño y SHA-256.

| Transporte | Tamaño o forma | Envíos exactos | Descargas exactas | Latencia mediana local |
| --- | --- | ---: | ---: | ---: |
| ZIP base64 | 1 KiB | 3/3 | 3/3 | 39 ms |
| ZIP base64 | 16 KiB | 3/3 | 3/3 | 57 ms |
| ZIP base64 | 64 KiB | 3/3 | 3/3 | 69 ms |
| ZIP base64 | 128 KiB | 3/3 | 3/3 | 97 ms |
| ZIP base64 | 256 KiB | 3/3 | 3/3 | 99 ms |
| files | paquete pequeño | 3/3 | 3/3 | 30 ms |
| files | paquete MUD representativo | 3/3 | 3/3 | 44 ms |
| files | binario + Unicode | 3/3 | 3/3 | 32 ms |

Esto valida el servidor, R2, la construcción determinista y el cliente MCP de referencia. No demuestra todavía que ChatGPT pueda materializar los argumentos de igual tamaño; por tanto, no autoriza elegir un transporte ni empezar las fases posteriores.

## Validación remota del prototipo

El 2026-08-10 se repitió la misma matriz mediante HTTPS contra el Worker desplegado y el bucket R2 real. El cliente descargó cada objeto desde el enlace devuelto por el MCP y verificó de nuevo tamaño y SHA-256.

| Transporte | Tamaño o forma | Envíos exactos | Descargas exactas | Latencia mediana remota |
| --- | --- | ---: | ---: | ---: |
| ZIP base64 | 1 KiB | 3/3 | 3/3 | 357 ms |
| ZIP base64 | 16 KiB | 3/3 | 3/3 | 348 ms |
| ZIP base64 | 64 KiB | 3/3 | 3/3 | 393 ms |
| ZIP base64 | 128 KiB | 3/3 | 3/3 | 634 ms |
| ZIP base64 | 256 KiB | 3/3 | 3/3 | 746 ms |
| files | paquete pequeño | 3/3 | 3/3 | 296 ms |
| files | paquete MUD representativo | 3/3 | 3/3 | 314 ms |
| files | binario + Unicode | 3/3 | 3/3 | 319 ms |

Esta evidencia confirma el comportamiento del servicio público y de R2. Sigue siendo evidencia auxiliar: la tabla de decisión solo se completará con llamadas originadas por ChatGPT Plus.

## Primera evidencia desde ChatGPT Plus

El 2026-08-10 ChatGPT Plus descubrió y ejecutó las tres herramientas del complemento privado:

- `probe_store_files` construyó un ZIP determinista de 252 bytes con SHA-256 `cad6f969e82f75e50b5f195c64cf8613623b27905efc0dbda1e5af036c5cf353`;
- `probe_store_base64` transmitió 128 bytes y obtuvo el mismo SHA-256 esperado, `cd4ebf7ae5e0f819a806a8e8cfab3ce07177d30f3279d9cffa9b135b4c62d6a8`;
- `probe_get_file` recuperó el segundo objeto conservando tamaño y SHA-256;
- una entrada base64 incorrecta fue rechazada antes del intento correcto.

Esto demuestra conectividad y exactitud básica desde ChatGPT, pero no satisface todavía las tres repeticiones ni los tamaños y formas de la matriz obligatoria.

ChatGPT solicitó confirmación manual para las operaciones de almacenamiento. Es el comportamiento coherente con sus anotaciones MCP: ambas cambian el estado privado de R2 y se declaran `readOnlyHint: false`, `destructiveHint: false`, `idempotentHint: true` y `openWorldHint: false`. `probe_get_file` se mantiene estrictamente no mutante y se declara `readOnlyHint: true`.

Se hizo después una prueba aislada de `probe_get_file` con el objeto conocido `local-base64-001k-1-1786383573760-998ac3a9e0e94`. ChatGPT pidió una confirmación manual antes de la única llamada, aunque la herramienta estaba anunciada como lectura y no invocó ninguna operación de almacenamiento. Tras aprobarla recuperó correctamente 1024 bytes con SHA-256 `8c6b6570692b82c082a00868c97c7e88e5fb7e44f33eb449d738c90bc9cc021b`.

Por tanto, las anotaciones correctas no bastan para evitar aprobaciones en este complemento privado de ChatGPT Plus. La confirmación observada pertenece a la política del cliente, no a una clasificación errónea del servidor.

No se falsearán las anotaciones para intentar eludirla. El diseño estable todavía puede minimizar las operaciones: una única herramienta de envío por candidata; espera, evidencias y descarga serían lecturas. Sin embargo, mientras el cliente exija una aprobación incluso para cada lectura, este canal MCP no satisface por sí solo los requisitos de cero intervención por candidata ni de corrección automática mediante varias llamadas dentro de la misma interacción.

Este resultado bloquea el paso a las fases de D1, GitHub Actions y harness hasta elegir explícitamente una de estas concesiones arquitectónicas:

1. aceptar aprobaciones manuales en ChatGPT Plus;
2. usar un cliente propio de la API que configure la política de aprobación;
3. trasladar el bucle completo, incluida la corrección de candidatas, a un servicio autónomo distinto de ChatGPT.

## Paquete MUD representativo

La prueba lógica debe incluir en conjunto:

- `patch.yaml` con decenas o cientos de operaciones;
- varios Markdown;
- YAML adicional;
- plugin Python opcional;
- acentos y Unicode;
- muchas rutas;
- recurso binario.

No basta con demostrar que una lista de un solo archivo atraviesa el MCP.

## Regla de salida

1. Si ZIP base64 funciona 3/3 hasta 256 KiB, se conserva `submit_candidate_zip`.
2. En otro caso, si el transporte lógico funciona 3/3 con el paquete representativo, se conserva `submit_candidate_files` y el Worker construye el ZIP definitivo.
3. No se implementará base64 fragmentado.
4. Si ambos fallan, se detiene la arquitectura antes de construir el laboratorio Windows.

Después de decidir se eliminará del servidor la herramienta de transporte descartada.

## Estado actual

- Implementación local: completa; TypeScript compila, 16 pruebas unitarias pasan y la matriz MCP local obtuvo 24/24 transferencias exactas.
- Empaquetado Wrangler: verificado mediante `wrangler deploy --dry-run` (1.020,37 KiB; gzip 177,94 KiB).
- Cuenta Cloudflare: Wrangler autenticado y buckets R2 de producción y preview creados.
- Despliegue Cloudflare: operativo mediante HTTPS, con secreto de ruta y subdominio `workers.dev` registrados.
- Validación remota de referencia: completa; 24/24 envíos y descargas exactos contra R2 real.
- Conexión desde ChatGPT: operativa; exactitud básica demostrada para ambos transportes, matriz completa pendiente.
- Confirmaciones de ChatGPT: incluso `probe_get_file`, estrictamente de solo lectura, requiere aprobación manual; el MCP privado no cumple cero intervención.
- Transporte elegido: ninguno todavía.
