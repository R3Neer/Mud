---
title: "Fase 0: transporte MCP de paquetes RepoPatcher"
status: en-prueba
date: 2026-08-09
---

# Fase 0: transporte MCP de paquetes RepoPatcher

## Propósito

Esta prueba decide empíricamente cómo transferirá ChatGPT una candidata al validador. El backend, GitHub Actions, OIDC y el harness pudieron adelantarse manteniendo ambos adaptadores privados, pero no se elegirá ni retirará ningún transporte hasta cerrar esta fase.

El prototipo está en `tooling/repo-patcher-mcp-probe/` y ofrece los dos transportes candidatos simultáneamente.

## Criterio de identidad

En cada intento deben coincidir:

```text
SHA-256 calculado antes del envío
== SHA-256 devuelto por el Worker
== SHA-256 de la descarga recibida
```

También debe coincidir el tamaño exacto.

## Matriz desde ChatGPT Plus

Cada celda `Envíos exactos` y `Descargas exactas` debe registrar tres intentos independientes.

| Transporte | Tamaño o forma | Envíos exactos | Descargas exactas | Latencia mediana |
| --- | --- | ---: | ---: | ---: |
| ZIP base64 | 1 KiB | 0/3 | 0/3 | bloqueado antes del Worker |
| ZIP base64 | 16 KiB | no ejecutado | no ejecutado | descarte anticipado |
| ZIP base64 | 64 KiB | no ejecutado | no ejecutado | descarte anticipado |
| ZIP base64 | 128 KiB | no ejecutado | no ejecutado | descarte anticipado |
| ZIP base64 | 256 KiB | no ejecutado | no ejecutado | descarte anticipado |
| files | paquete pequeño | 3/3 | 3/3 | menos de 5 s observados |
| files | paquete MUD representativo, llamada única | 0/3 | 0/3 | 14:02 mediana |
| files | binario + Unicode | 3/3 | 3/3 | unos 5 s |
| files por lotes completos | paquete MUD representativo | pendiente | pendiente | pendiente |

Esta tabla solo usa llamadas iniciadas por ChatGPT Plus. Las recuperaciones independientes desde R2 verifican los bytes aunque ChatGPT pierda el retorno visible. Las pruebas locales del mismo protocolo no se mezclan con la evidencia que decide el transporte.

Los tamaños base64 superiores a 1 KiB se cancelaron porque tres bloqueos de seguridad consecutivos en el tamaño mínimo hacen imposible alcanzar la regla 3/3 hasta 256 KiB. No se gastarán más llamadas en una alternativa ya descartada.

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

## Evidencia de ChatGPT Plus del 11 de agosto

La instalación renovada del complemento descubrió las cuatro herramientas originales. `probe_wait_and_record` completó llamadas de 15 y 120 segundos sin confirmación manual. La llamada de 120 segundos devolvió 25 eventos y exactamente 120.000 ms de tiempo de servidor. Al final, la interfaz mostró un aviso transitorio por exceso de solicitudes; otro chat siguió funcionando. Esta evidencia permite medir llamadas largas, pero refuerza que el diseño final no debe depender de mantener una conexión HTTP abierta.

El cliente solo ofrece de forma global **Permitir acciones de bajo riesgo**. En una conversación solicitó tres aprobaciones iniciales que se concedieron para toda la conversación; las operaciones posteriores no requirieron confirmaciones adicionales. El requisito operativo queda precisado como cero intervención **por candidata después de la autorización inicial de la conversación**.

El transporte ZIP base64 fue bloqueado tres veces antes de alcanzar el Worker, pese a que ChatGPT calculó correctamente los 1024 bytes y el SHA-256 `8c6b6570692b82c082a00868c97c7e88e5fb7e44f33eb449d738c90bc9cc021b`. El transporte directo queda descartado sin probar tamaños superiores.

El transporte lógico mínimo produjo tres veces el mismo ZIP de 178 bytes y SHA-256 `58bc0c3e981696af16f87eb4b188d49fb67d802286ab6a3d9c10566742e10829`. Las descargas contenían el `patch.yaml` exacto, incluido Unicode y timestamp ZIP fijo.

La variante de tres archivos con Unicode y un binario de 2048 bytes produjo tres veces 756 bytes y SHA-256 `20864f4e79b8480a6495ad721c86fc80b92af8e63397a198520f3e78eb531a89`. Las tres recuperaciones independientes confirmaron rutas, contenidos y binario exactos. Con el modo Instant cada intento tardó unos cinco segundos.

La llamada monolítica representativa no es fiable:

1. el primer intento tardó 15:48, almacenó las 28 rutas y todos los textos exactos, pero convirtió el binario esperado de 8192 bytes en 135.846 bytes al añadir datos después del prefijo correcto;
2. el segundo intento tardó 14:02 y no creó ningún objeto en R2;
3. el intento con Instant tardó 14:01 según el reloj del usuario, aunque el modelo afirmó «unos segundos», y tampoco creó objeto.

Por tanto, no se confiará en una sola llamada que materialice unos 32 KiB de JSON. El prototipo 0.2 introduce lotes inmutables de archivos completos: `probe_stage_files` exige tamaño y SHA-256 por archivo, limita cada lote a 24 KiB de contenido textual y nunca divide un archivo ni fragmenta base64; `probe_finalize_files` relee los lotes explícitos, revalida cada archivo y construye el ZIP definitivo. El paquete representativo se divide en `patch`, `support` y `binary`.

El smoke test local del nuevo protocolo listó seis herramientas, almacenó los tres lotes, verificó 28 archivos y 25.988 bytes fuente y produjo un ZIP determinista de 6456 bytes con SHA-256 `23f423b6a95a21edbbbd22eb462f0a57723661c6505b92342067d2e27a5bdf4e`. Falta repetir este camino desde ChatGPT Plus.

Las primeras pruebas del complemento antiguo solicitaron confirmaciones incluso para `probe_get_file`. La instalación renovada mostró después un comportamiento más preciso: puede pedir varias autorizaciones iniciales para toda la conversación y ejecutar sin nuevas interrupciones las operaciones posteriores. Esta limitación de interfaz se acepta porque Samuel trabaja habitualmente en conversaciones largas.

No se falsearán las anotaciones MCP: almacenamiento y staging siguen declarados mutantes, no destructivos e idempotentes; la recuperación sigue siendo lectura. Ya no se considera necesario un cliente propio ni trasladar fuera de ChatGPT el bucle de corrección únicamente para eliminar la autorización inicial.

## Fase 0B: una única llamada larga

Se probó además si una llamada MCP podía permanecer abierta durante todo un trabajo largo, como evidencia de los límites del cliente, no como fundamento del diseño definitivo.

La herramienta experimental `probe_wait_and_record` acepta un `probe_id` nuevo y una duración de 15, 30, 60 o 120 segundos. Persiste en R2 eventos append-only de inicio, heartbeat cada cinco segundos y finalización. El endpoint secreto `probe-timings/<probe_id>` permite consultar después esos eventos aunque ChatGPT haya abandonado la llamada.

Se medirán por separado:

- tiempo de servidor entre inicio y finalización;
- tiempo observado por el cliente MCP de referencia;
- si ChatGPT recibe el resultado terminal tras una sola aprobación;
- último heartbeat persistido cuando el cliente falle o desconecte;
- tiempo aproximado percibido en la interacción de ChatGPT.

La telemetría del Worker no puede observar el instante exacto en el que la interfaz de ChatGPT muestra el resultado. Esa última medida se registrará como evidencia del cliente, no se inferirá del reloj del servidor.

| Cliente | Duración solicitada | Aprobaciones | Servidor completó | ChatGPT recibió resultado | Tiempo servidor | Tiempo cliente |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| MCP de referencia | 15 s | n/a | sí | n/a | 15.000 ms | 15.932 ms |
| ChatGPT Plus | 15 s | 0 | sí | sí | 15.000 ms | recibido |
| ChatGPT Plus | 30 s | pendiente | pendiente | pendiente | pendiente | pendiente |
| ChatGPT Plus | 60 s | pendiente | pendiente | pendiente | pendiente | pendiente |
| ChatGPT Plus | 120 s | 0 | sí | sí | 120.000 ms | recibido con aviso posterior |

Aunque 120 segundos terminó y volvió a ChatGPT sin aprobación, la interfaz mostró después un aviso transitorio de protección. El bucle definitivo seguirá siendo asíncrono, con estado persistente y consultas cortas; no dependerá de mantener abierta una llamada HTTP.

La prueba remota de referencia `reference-long-15-20260810-003` registró inicio, heartbeats a 5.484 y 10.639 segundos y finalización exactamente a los 15.000 segundos. El cliente recibió la respuesta y volvió a descargar la telemetría en 15.932 segundos. Esto valida Worker, Streamable HTTP, persistencia R2 y consulta posterior; no sustituye la prueba desde ChatGPT.

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

1. ZIP base64 queda descartado tras 0/3 incluso a 1 KiB.
2. Si el transporte lógico por lotes completos funciona 3/3 con el paquete representativo, el Worker construirá el ZIP definitivo desde esos lotes inmutables.
3. No se implementará base64 fragmentado.
4. Si ambos fallan, se detiene la arquitectura antes de construir el laboratorio Windows.

Después de decidir se eliminará del servidor la herramienta de transporte descartada.

## Estado actual

- Implementación local: prototipo 0.2 completo; TypeScript compila, 19 pruebas unitarias pasan y el smoke MCP incremental finaliza el paquete representativo exacto.
- Empaquetado Wrangler: verificado mediante `wrangler deploy --dry-run` (1.029,19 KiB; gzip 179,97 KiB).
- Cuenta Cloudflare: Wrangler autenticado y buckets R2 de producción y preview creados.
- Despliegue Cloudflare: prototipo 0.2 publicado en la versión Worker `22619184-837b-4a16-8c13-a8361f06e1ca`, con staging por lotes completos.
- Validación remota de referencia: completa; 24/24 envíos y descargas exactos contra R2 real.
- Conexión desde ChatGPT: operativa; paquete mínimo y Unicode/binario obtuvieron 3/3, mientras ZIP base64 y `files` monolítico quedaron descartados.
- Confirmaciones de ChatGPT: una conversación puede exigir tres autorizaciones iniciales; después no pidió intervención adicional por operación.
- Sonda de llamada larga: 15 y 120 segundos completados desde ChatGPT; no se usará como fundamento de la arquitectura asíncrona.
- Transporte elegido: dirección provisional `files` por lotes completos; falta 3/3 representativo desde ChatGPT antes de cerrar la fase.
