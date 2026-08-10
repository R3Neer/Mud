---
title: "Arquitectura del validador remoto RepoPatcher"
status: aceptada
date: 2026-08-10
---

# Arquitectura del validador remoto RepoPatcher

## Contexto

ChatGPT debe poder proponer un paquete RepoPatcher, comprobarlo en el entorno
normativo Windows contra un commit inmutable y entregar exactamente los bytes
que superaron la validación. La cola v6 demuestra el proceso, pero su polling,
sus issues y sus ramas portadoras añaden latencia y acoplan el transporte al
validador.

La Fase 0 todavía no ha decidido si ChatGPT enviará un ZIP en base64 o una lista
de archivos lógicos. Tampoco está resuelta la política real de confirmaciones
del cliente. Esas incógnitas no deben contaminar el núcleo durable.

## Decisión

Se construirá un camino nuevo en paralelo a v6:

```text
adaptador MCP
  → servicio de candidatas
    → R2 (bytes por SHA-256) + D1 (estado por request_id)
      → workflow_dispatch
        → runner Windows
          → harness de control + runtime del target_sha
```

Las fronteras son:

- el adaptador MCP solo traduce la interacción de ChatGPT al contrato interno;
- el servicio persiste antes de hacer dispatch y no depende de una conexión
  HTTP abierta para conservar el trabajo;
- R2 contiene los bytes y D1 contiene identidad, estado y asociaciones;
- GitHub Actions es el laboratorio Windows efímero;
- el harness procede del `workflow_sha` confiable;
- RepoPatcher 0.2.0 procede del `target_sha` y se verifica por ruta y versión;
- el paquete solo se ejecuta en clones descartables A y B;
- el resultado terminal y el ZIP verde son inmutables.

El flujo después de construir el ZIP es idéntico para ambos transportes. Por
eso la elección pendiente solo afecta a la entrada del adaptador.

## Plano de control y plano objetivo

```text
workspace/
├── control/       workflow_sha; harness y schemas
├── target-source/ target_sha; fuente Git y runtime vendorizado
└── validation/
    ├── run-a/Mud/
    └── run-b/Mud/
```

`target-source` nunca será el repositorio de un comando que cargue plugins.
`explain`, `check`, `apply` y la replanificación se ejecutarán en procesos
separados. El entorno de esos procesos no contendrá credenciales.

## Garantías del harness

Para cada clon:

1. `explain` y `check` deben dejar idénticos filesystem, HEAD, índice, status y
   diff;
2. `apply` parte de un árbol limpio y ejecuta generadores y validadores;
3. `git diff --check` debe ser correcto;
4. una replanificación con `require_clean=False` debe proponer cero rutas y no
   modificar ningún estado observable.

Entre A y B se comparan los estados finales, incluido el índice semántico con
`git ls-files --stage -z`. Los bytes físicos de `.git/index` solo se comparan
dentro del mismo clon.

Esta doble ejecución aporta evidencia fuerte de reproducibilidad; no demuestra
determinismo universal ante todas las fuentes externas posibles.

## Seguridad

- `trust_plugin` se transporta y registra explícitamente.
- Un paquete con plugin se rechaza antes de cargarlo si no está autorizado.
- El job que ejecuta código candidato solo recibe `contents: read` e
  `id-token: write`.
- El token OIDC se usa para descargar la candidata y se elimina, junto con
  cualquier credencial, antes de ejecutar código candidato.
- El Worker valida firma, tiempos, audiencia y la identidad exacta de
  repositorio, run, intento, workflow, SHA, ref, runner y actor.
- Los clones son descartables; `control` y `target-source` se fotografían antes
  y después para detectar escrituras laterales.

Esto aísla datos y credenciales. No se afirma que un proceso Python arbitrario
carezca de red o de acceso al resto del runner; esa propiedad exigiría un
sandbox de sistema operativo adicional y no forma parte de RepoPatcher 0.2.0.

## Durabilidad y carreras

La solicitud se inserta en D1 antes del dispatch. La asociación posterior del
`workflow_run_id` es condicional, idempotente y recuperable. Si el runner llega
antes de esa asociación, el Worker devuelve `409 dispatch_not_committed_yet` y
el runner reintenta hasta 30 segundos. Un dispatch cuya respuesta se pierde se
reconcilia por workflow, `request_id` y ventana temporal.

Las transiciones son monotónicas:

```text
accepted → dispatching → queued → running
                                  ├→ succeeded
                                  ├→ failed
                                  └→ infrastructure_error
accepted/dispatching/queued/running → expired
```

## Consecuencias

- v6 permanece intacta hasta diez ejecuciones E2E verdes del sistema nuevo;
- no se crean issues, commits, ramas ni PR desde el sistema nuevo;
- el adaptador MCP puede cambiar entre varias herramientas y una operación
  compuesta sin reescribir almacenamiento, workflow ni harness;
- la aplicación local, commit y push siguen fuera de alcance;
- las decisiones aún abiertas se mantienen en
  `notas/PENDIENTES-VALIDADOR-REMOTO.md`.

