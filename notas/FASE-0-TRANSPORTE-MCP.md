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
- Conexión desde ChatGPT: pendiente.
- Transporte elegido: ninguno todavía.
