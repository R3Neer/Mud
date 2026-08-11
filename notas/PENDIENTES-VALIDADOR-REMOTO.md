---
title: "Pendientes del validador remoto RepoPatcher"
status: vigente
date: 2026-08-11
---

# Pendientes del validador remoto RepoPatcher

## Propósito

Este documento conserva las decisiones abiertas, experimentos incompletos y condiciones de corte del sistema:

```text
/patch en ChatGPT
→ candidata exacta
→ validación Windows contra target_sha
→ diagnóstico y posible corrección
→ entrega del mismo ZIP que obtuvo verde
```

Debe consultarse antes de modificar el adaptador MCP definitivo o retirar la infraestructura v6. La Fase 0 ya está cerrada. El subsistema que aplique localmente el ZIP, haga commit o publique cambios continúa fuera de alcance.

## Decisiones ya fijadas

- El núcleo será independiente del número de llamadas MCP.
- La ejecución será durable y recuperable; una conexión HTTP abierta nunca será la única propietaria del trabajo.
- R2 conservará los bytes candidatos y las evidencias; D1 conservará estado e identidad.
- GitHub Actions seguirá siendo el laboratorio Windows efímero.
- El harness usará RepoPatcher 0.2.0 del `target_sha`, mientras su plano de control procederá del `workflow_sha` confiable.
- `explain` y `check` solo se ejecutarán en un clon descartable y deberán ser no mutantes.
- La convergencia no hará un segundo `apply` sobre un árbol sucio.
- La reproducibilidad se contrastará con dos clones limpios A/B.
- v6 permanecerá disponible hasta obtener diez ejecuciones E2E verdes con el sistema nuevo.
- No se falsearán anotaciones MCP para evitar aprobaciones.

## Pendientes que bloquean el corte, pero no el núcleo común

### P1 — Política real de aprobaciones de ChatGPT

Estado: **cerrado**.

Evidencia actual:

- La configuración final del complemento permite todas las acciones sin preguntar.
- Las pruebas decisivas de staging y finalización se ejecutaron sin confirmaciones manuales.
- El cliente puede pedir autorizaciones iniciales en otras configuraciones, pero no forman parte del contrato ni condicionan la arquitectura.

El requisito de cero intervención por candidata queda satisfecho en la configuración probada.

### P2 — Catálogo MCP actualizado en ChatGPT

Estado: **cerrado**.

Se recreó la conexión en modo desarrollador. El catálogo renovado mostró y ejecutó las cuatro herramientas originales, incluida `probe_wait_and_record`. Los cambios posteriores de catálogo seguirán requiriendo reinstalar o renovar el complemento.

### P3 — Prueba de llamada única larga desde ChatGPT

Estado: **cerrado**.

ChatGPT completó llamadas de 15 y 120 segundos sin confirmación manual y recibió sus resultados terminales. La prueba de 120 segundos registró 25 eventos y 120.000 ms. La interfaz mostró después un aviso transitorio de protección, por lo que el sistema definitivo conservará estado durable y consultas cortas; no dependerá de una conexión HTTP larga.

### P4 — Transporte candidato definitivo

Estado: **cerrado**.

Resultados:

```text
ZIP base64: descartado tras 0/3 a 1 KiB por bloqueo del cliente
files monolítico: descartado tras 0/3 representativos exactos
files UTF-8 por lotes completos: 3/3 representativos exactos desde ChatGPT
```

Se eligió staging de archivos UTF-8 completos, con tamaño y SHA-256 por archivo, seguido de finalización determinista. Los tres ZIP midieron 6008 bytes y compartieron SHA-256 `a199b3814e7e64e53f3b393b3d12862535d0907d43c6d712ccae8b32ddca2811`. No se implementará base64 fragmentado y los recursos binarios arbitrarios quedan fuera de v1.

### P5 — Adaptador MCP definitivo

Estado: **en implementación**.

Se usarán varias llamadas cortas, idempotentes y reanudables:

```text
stage_candidate_files → submit_candidate → await_validation
→ read_validation_evidence → get_validated_candidate
```

El staging usa archivos completos y lotes inmutables; nunca divide un archivo. El aviso posterior a la prueba de 120 segundos descarta depender de una operación compuesta mantenida abierta. Los servicios internos continúan independientes del número exacto de herramientas.

### P6 — Propietario del bucle de corrección

Estado: **cerrado**.

ChatGPT conserva el razonamiento, lee el diagnóstico y repite candidatas mediante varias llamadas en la misma conversación autorizada. No se incorporarán facturación ni credenciales de la API de OpenAI en v1.

## Pendientes operativos posteriores

### P7 — E2E y latencia

Estado: **en curso; 2/10 verdes que cumplen el contrato vigente**.

Primer verde real, 2026-08-10:

- `request_id`: `remote-e2e-20260810-03`;
- run: `31430689484`;
- `target_sha` y `control_sha`: `f56b69a460ffdb7c724376851b1d08d6410516cc`;
- RepoPatcher: `0.2.0`;
- paquete: 364 bytes, SHA-256
  `97d68cfbbcddc5bdeea8b16d45649fe2332a58e903b9c38f7b6f49b762eee0dd`;
- aceptación D1: `20:46:48Z`; workflow completado: `20:47:40Z`;
- latencia del camino normal hasta el verde de Actions: aproximadamente 52 segundos;
- el objeto entregado por el Worker volvió a medir 364 bytes y produjo el mismo
  SHA-256.

El retraso hasta `completed_at` de D1 en esta ejecución no representa el camino
normal: se empleó en diagnosticar y corregir la ingestión del primer artifact.
La solicitud se reanudó de forma idempotente sin ejecutar otro runner.

Este primer verde funcional no se cuenta entre los diez de corte: reveló que el
diff de Git no incluía archivos nuevos sin seguimiento. Los snapshots y la
reproducibilidad sí eran correctos, pero la evidencia `applied.patch` estaba
incompleta.

Verdes con el contrato completo:

| Request | Run | Estado D1 | Evidencia | Latencia D1 |
| --- | ---: | --- | --- | ---: |
| `remote-e2e-20260810-04` | `31431845357` | `succeeded` | diff completo, 221 bytes | 91,1 s |
| `remote-e2e-20260810-05` | `31432380172` | `succeeded` | diff completo y ZIP exacto | 59,2 s |

La ejecución 04 descargó PyYAML desde PyPI y dedicó 32 segundos a esa operación.
Desde la ejecución 05, el plano de control contiene el wheel Windows CPython
3.13 de PyYAML 6.0.3, verifica su SHA-256 y lo instala con `--no-index`; esa
instalación tardó 6 segundos. El ZIP entregado en la ejecución 05 conservó sus
377 bytes y el SHA-256
`77ca23adf7a98335b046ff579615cf44f30225438d6513f80328a446d50f486a`.

Incidencias descubiertas y corregidas por este E2E:

- el input `package_size` debe cruzar `workflow_dispatch` como cadena decimal;
- Cloudflare Workers no admite `redirect: "error"`; la descarga firmada usa
  `manual` y rechaza explícitamente una segunda redirección.
- el diff completo de archivos nuevos o ignorados se genera con un índice Git
  temporal, sin modificar el índice físico del clon;
- PyYAML se instala desde un wheel Windows 3.13 fijado y verificado, fuera de la
  red del camino crítico.

Antes del corte deben existir:

- candidata verde;
- candidata roja con diagnóstico útil;
- repetición con candidata corregida;
- duplicados y carreras recuperados;
- fallo de infraestructura distinguible de fallo del paquete;
- diez verdes consecutivos;
- mediana inferior a un minuto y al menos ocho de diez ejecuciones inferiores a un minuto.

### P8 — Retirada de v6

Estado: **prohibida por ahora**.

Solo después de P7 se podrán retirar cola de issues, cron, ramas portadoras, scripts locales y transporte antiguo. El dispatch manual y los artifacts permanecerán como fallback.

### P9 — Aplicación local y publicación

Continúa fuera de alcance:

```text
ZIP verde
→ RepoPatcher local
→ commit
→ push
```

Tendrá permisos y credenciales separados si se implementa en el futuro.

## Componentes experimentales ya disponibles

- Worker: `mud-repo-patcher-mcp-probe`.
- Versión desplegada al registrar este documento: `22619184-837b-4a16-8c13-a8361f06e1ca`.
- R2 de prueba operativo.
- Seis herramientas experimentales desplegadas; `probe_stage_files` y `probe_finalize_files` quedaron verificadas 3/3 desde ChatGPT con el paquete UTF-8 representativo.
- `probe_wait_and_record` verificada mediante cliente MCP de referencia.
- Matrices local y remota de referencia: 24/24 transferencias exactas.
- Evidencia detallada: `notas/FASE-0-TRANSPORTE-MCP.md`.

## Núcleo común implementado

Desde el 2026-08-10 están implementados y versionados:

- ADR y schemas neutrales;
- harness A/B con preflight no mutante, convergencia y reproducibilidad;
- workflow Windows separado de v6, con control/target y descarga OIDC;
- Worker durable con D1, R2, dispatch directo, reconciliación y artifacts;
- ambos adaptadores de transporte privados;
- pruebas Python y pruebas Workers dentro de `workerd`;
- D1 y R2 reales creados, migración aplicada y Worker desplegado.

El workflow está publicado y el Worker dispone de una credencial fine-grained
limitada a `R3Neer/Mud` y Actions. Los E2E están registrados en P7.
P1–P4 y P6 están cerrados. Falta terminar el adaptador definitivo P5, además de ocho verdes, casos rojos y pruebas de carreras P7 antes de cualquier corte. Véase `notas/RUNBOOK-VALIDADOR-REMOTO.md`.

## Trabajo autorizado mientras estos puntos siguen abiertos

Mientras P5 y P7 sigan abiertos puede avanzarse en:

- contratos y schemas neutrales;
- máquina de estados D1;
- identidad e inmutabilidad R2;
- autenticación OIDC Actions → Worker;
- dispatch idempotente y reconciliación;
- separación `control`/`target`;
- harness Windows;
- snapshots, preflight, aplicación A/B, convergencia y reproducibilidad;
- artifacts y evidencias;
- pruebas locales y de integración que no retiren v6.

## Regla de reanudación

Al retomar cualquiera de los pendientes se registrarán:

1. cliente y plataforma usados;
2. conversación nueva o reutilizada;
3. herramientas visibles;
4. política de aprobación seleccionada;
5. número de confirmaciones;
6. argumentos y resultado exactos;
7. hashes, tamaños y tiempos cuando proceda;
8. decisión que la evidencia permite tomar.
