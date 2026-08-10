---
title: "Pendientes del validador remoto RepoPatcher"
status: vigente
date: 2026-08-10
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

Debe consultarse antes de cerrar la Fase 0, elegir el adaptador MCP definitivo o retirar la infraestructura v6. El subsistema que aplique localmente el ZIP, haga commit o publique cambios continúa fuera de alcance.

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

Estado: **abierto**.

Evidencia actual:

- ChatGPT Plus pidió confirmación incluso para `probe_get_file`, que es estrictamente de lectura.
- La aplicación móvil volvió a pedirla con **Permitir todas las acciones** seleccionado.
- La lectura sí llegó al Worker y recuperó 1024 bytes con SHA-256 `8c6b6570692b82c082a00868c97c7e88e5fb7e44f33eb449d738c90bc9cc021b`.

Falta:

- repetir la lectura en ChatGPT web o escritorio, conversación nueva y conexión seleccionada explícitamente;
- si no pide confirmación, probar una secuencia de escritura, lectura y segunda candidata;
- si pide confirmación, considerar no fiable la ejecución de varias llamadas desde ChatGPT normal.

Consecuencia:

- no impide construir Worker, D1, R2, Actions ni harness;
- decide si el adaptador final expone varias herramientas o una operación compuesta.

### P2 — Catálogo MCP actualizado en ChatGPT

Estado: **abierto**.

El Worker desplegado expone `probe_wait_and_record`, pero una conversación de ChatGPT conservó el catálogo anterior y no la encontró. El cliente MCP de referencia sí la descubrió y ejecutó.

Falta:

- recrear o refrescar la conexión desde web/escritorio;
- abrir una conversación nueva;
- comprobar que aparecen las cuatro herramientas.

### P3 — Prueba de llamada única larga desde ChatGPT

Estado: **abierto**.

Evidencia disponible:

- el cliente MCP de referencia completó 15 segundos;
- tiempo de servidor: 15.000 ms;
- tiempo de cliente: 15.932 ms;
- los eventos append-only quedaron persistidos en R2.

Falta ejecutar desde ChatGPT una prueba de 120 segundos. Su resultado decidirá si una operación MCP puede esperar de forma cómoda al resultado, pero no cambiará la durabilidad interna del trabajo.

### P4 — Transporte candidato definitivo

Estado: **abierto**.

Ambos caminos siguen disponibles:

```text
submit_candidate_zip
submit_candidate_files
```

Falta completar desde ChatGPT la matriz 3/3 establecida en `FASE-0-TRANSPORTE-MCP.md`. Hasta entonces:

- no eliminar ninguno;
- no declarar cerrada la Fase 0;
- no introducir base64 fragmentado.

### P5 — Adaptador MCP definitivo

Estado: **abierto**.

Alternativas deliberadamente aisladas del núcleo:

```text
varias llamadas
submit → await → evidence → download

una operación compuesta
validate_candidate → espera o reanudación → resultado
```

La selección depende de P1 y P3. Los servicios internos no dependerán de esa selección.

### P6 — Propietario del bucle de corrección

Estado: **abierto**.

Alternativas:

- ChatGPT conserva el razonamiento y repite candidatas mediante varias llamadas;
- un orquestador servidor usa la API de OpenAI con límites explícitos;
- una llamada compuesta coordina un trabajo durable y devuelve cada diagnóstico al cliente.

No se incorporará facturación ni credenciales de la API de OpenAI hasta que P1 determine que hacen falta.

## Pendientes operativos posteriores

### P7 — E2E y latencia

Estado: **en curso; 1/10 verdes**.

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

Incidencias descubiertas y corregidas por este E2E:

- el input `package_size` debe cruzar `workflow_dispatch` como cadena decimal;
- Cloudflare Workers no admite `redirect: "error"`; la descarga firmada usa
  `manual` y rechaza explícitamente una segunda redirección.

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
- Versión desplegada al registrar este documento: `3d59d75d-adda-472a-95c2-f75e57e9e5e6`.
- R2 de prueba operativo.
- Tres herramientas de transporte verificadas desde ChatGPT.
- `probe_wait_and_record` verificada mediante cliente MCP de referencia.
- Matrices local y remota de referencia: 24/24 transferencias exactas.
- Evidencia detallada: `notas/FASE-0-TRANSPORTE-MCP.md`.

## Núcleo común implementado

Desde el 2026-08-10 están implementados y versionados, sin cerrar P1–P6:

- ADR y schemas neutrales;
- harness A/B con preflight no mutante, convergencia y reproducibilidad;
- workflow Windows separado de v6, con control/target y descarga OIDC;
- Worker durable con D1, R2, dispatch directo, reconciliación y artifacts;
- ambos adaptadores de transporte privados;
- pruebas Python y pruebas Workers dentro de `workerd`;
- D1 y R2 reales creados, migración aplicada y Worker desplegado.

El workflow está publicado y el Worker dispone de una credencial fine-grained
limitada a `R3Neer/Mud` y Actions. El primer E2E verde está registrado en P7.
Siguen abiertos P1–P6 y faltan nueve verdes, casos rojos y pruebas de carreras
antes de cualquier corte. Véase `notas/RUNBOOK-VALIDADOR-REMOTO.md`.

## Trabajo autorizado mientras estos puntos siguen abiertos

Puede avanzarse sin resolver P1–P6 en:

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
