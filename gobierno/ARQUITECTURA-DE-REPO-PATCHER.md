---
title: Arquitectura y responsabilidades de repo-patcher
aliases:
  - Arquitectura de repo-patcher
  - Validación remota de paquetes
  - Publicación de patches validados
tags:
  - mud/gobierno
  - mud/repo-patcher
  - mud/ci
status: borrador
scope: Orquestación, validación remota, aplicación local y publicación de paquetes
current-ci-kit-version: 6
target-ci-kit-version: 7
reviewed-main: e437077f6d391e31c7c00dc3abc2e19f408215ea
reviewed-at: 2026-08-07
---

# Arquitectura y responsabilidades de `repo-patcher`

## 1. Objetivo

Este documento define:

- qué componentes participan en la generación, transporte, validación, aplicación y publicación de un paquete `repo-patcher`;
- qué responsabilidad pertenece a cada componente;
- con qué tecnología está construido o se construirá cada componente;
- qué piezas existen ya en el repositorio;
- qué piezas pertenecen a la dirección v7 y todavía no están implementadas;
- dónde están los límites de confianza y qué componente puede ejecutar código del paquete.

Este documento **no define la semántica del formato `patch.yaml` ni del runtime**. Esa autoridad permanece en:

```text
gobierno/USO-DE-REPO-PATCHER.md
```

La implementación vendorizada del motor permanece en:

```text
tooling/repo-patcher-runtime/repo_patcher/
```

## 2. Estado de las decisiones

### 2.1. Decisiones aceptadas

1. La validación de una candidata debe ser automática y no debe modificar `main`.
2. La candidata debe validarse contra un SHA completo y explícito del repositorio.
3. La identidad del ZIP se representa mediante su SHA-256 exacto.
4. Los plugins solo se ejecutan durante la validación remota si la solicitud contiene consentimiento explícito.
5. La validación remota usa un runner Windows hospedado por GitHub.
6. El camino interactivo v7 usará un puente local saliente que invoque `workflow_dispatch`.
7. El puente local no ejecutará RepoPatcher, plugins, generadores ni validadores del paquete.
8. La cola programada v6 se conservará como mecanismo de recuperación, no como camino interactivo principal.
9. Aplicar un paquete aceptado requiere una aprobación explícita de Samuel.
10. Después de esa aprobación, la aplicación, las comprobaciones, el commit y el push podrán automatizarse.

### 2.2. Propuestas provisionales

1. El puente consultará GitHub aproximadamente cada dos segundos durante una sesión activa.
2. El puente se instalará mediante el Programador de tareas de Windows al iniciar sesión.
3. El workflow v7 aceptará una fuente `issue` además de la fuente manual mediante rama portadora.
4. La lógica de validación se extraerá del YAML a `validate_candidate.py`.
5. La publicación local se encapsulará en un wrapper como `Apply-ValidatedRepoPatch.ps1`.

### 2.3. Cuestiones abiertas

1. Intervalo de consulta definitivo del puente y política de backoff.
2. Formato exacto del recibo de dispatch almacenado en la issue.
3. Si el instalador local realizará el push en la misma confirmación que el commit o pedirá una segunda confirmación.
4. Política de retención de resultados y artifacts más allá de los catorce días actuales.
5. Umbral de latencia que deberá cumplirse antes de declarar v7 operativa.

### 2.4. Alternativas descartadas como camino principal

- cron de GitHub Actions;
- `issue_comment` como única fuente de baja latencia;
- servidor doméstico;
- endpoint público o túnel hacia el portátil;
- runner autoalojado en el portátil;
- MCP personalizado con acciones, mientras ChatGPT Plus no lo permita;
- ejecutar la validación no confiable directamente en el portátil.

## 3. Requisitos

### 3.1. Requisitos funcionales

El sistema debe:

1. recibir exactamente los bytes del ZIP candidato;
2. asociar la candidata a un `request_id` único;
3. asociarla a un `target_sha` completo;
4. verificar tamaño y SHA-256 del ZIP;
5. verificar la estructura segura del ZIP;
6. ejecutar la versión vendorizada de RepoPatcher;
7. ejecutar `package-info`, `explain`, `check`, `apply`, validadores, `git diff --check`, `check` posterior e idempotencia;
8. registrar si existe plugin y si fue autorizado;
9. conservar logs, diff y metadatos;
10. devolver un resultado estructurado;
11. permitir corregir y repetir una candidata sin intervención manual de Samuel;
12. demostrar que el ZIP entregado es el mismo ZIP que obtuvo resultado correcto.

### 3.2. Requisitos no funcionales

El sistema debe aspirar a:

- detección interactiva en menos de tres segundos;
- comienzo del workflow sin esperar un cron;
- validación habitual en menos de un minuto;
- ausencia de escritura sobre el checkout canónico durante la validación;
- ausencia de credenciales de escritura en el proceso que ejecuta plugins;
- ausencia de puertos entrantes en el portátil;
- tolerancia a suspensión y apagado del portátil;
- deduplicación de solicitudes y reintentos;
- trazabilidad mediante `request_id`, `target_sha`, SHA-256 y `run_id`;
- posibilidad de sustituir el orquestador sin reescribir el motor de validación.

## 4. Contexto del sistema

```mermaid
flowchart LR
    Samuel[Samuel]
    ChatGPT[ChatGPT]
    GitHub[GitHub\nRepositorio, Issues y Actions]
    Bridge[Puente local\nPortátil de Samuel]
    Runner[Runner Windows\nhospedado por GitHub]
    LocalRepo[Checkout local de Mud]

    Samuel -->|solicita /patch| ChatGPT
    ChatGPT -->|lee main y crea solicitud| GitHub
    Bridge -->|consulta solicitudes y hace dispatch| GitHub
    GitHub -->|asigna workflow| Runner
    Runner -->|publica resultado y artifact| GitHub
    ChatGPT -->|lee run, logs y artifact| GitHub
    ChatGPT -->|entrega ZIP validado| Samuel
    Samuel -->|aprueba instalación| Bridge
    Bridge -->|aplica paquete aprobado| LocalRepo
    Bridge -->|commit y push autorizados| GitHub
```

### 4.1. Frontera conceptual

```text
PROPONER Y VALIDAR
ChatGPT + GitHub + runner remoto

ACEPTAR Y PUBLICAR
Samuel + instalador local + Git
```

Una validación correcta demuestra aplicabilidad y resultado esperado. No representa por sí sola la decisión de incorporar el cambio a `main`.

## 5. Inventario de componentes

### 5.1. Componentes construidos en v6

| Componente | Ubicación | Tecnología | Responsabilidad | Estado |
| --- | --- | --- | --- | --- |
| Runtime RepoPatcher | `tooling/repo-patcher-runtime/repo_patcher/` | Python | Interpretar, comprobar y aplicar paquetes | Construido y vendorizado, versión 0.2.0 |
| Guía autoritativa del runtime | `gobierno/USO-DE-REPO-PATCHER.md` | Markdown | Documentar formato y comportamiento real | Construida y vigente |
| Transporte por Issues | `tooling/repo-patcher-ci/issue_transport.py` | Python, biblioteca estándar | Codificar, validar y reconstruir ZIP mediante issue y comentarios Base64 | Construido |
| Cola programada | `tooling/repo-patcher-ci/issue_queue.py` | Python, API REST de GitHub | Seleccionar solicitudes, reclamar, reconstruir, finalizar y cerrar | Construida |
| Inspección auxiliar | `tooling/repo-patcher-ci/package_checks.py` | Python | Detectar plugin sin importarlo y comprobar idempotencia semántica | Construida |
| Workflow remoto | `.github/workflows/validate-repo-patcher.yml` | GitHub Actions, YAML, Bash y PowerShell | Preparar, validar y finalizar solicitudes | Construido y activo |
| Envío manual inmediato | `tooling/repo-patcher-ci/Submit-RepoPatch.ps1` | PowerShell, Git, GitHub CLI y Python | Crear rama portadora, subir ZIP, hacer dispatch y localizar el run | Construido; requiere ejecución local manual |
| Recolección manual | `tooling/repo-patcher-ci/Collect-RepoPatchRun.ps1` | PowerShell y GitHub CLI | Seguir el run, descargar artifact y retirar la rama temporal | Construido |
| Consentimiento de plugin | `tooling/repo-patcher-ci/PluginConsent.ps1` | PowerShell | Obtener consentimiento local explícito | Construido |
| Instalador del kit CI | `tooling/repo-patcher-ci/Install-RepoPatcherCI.ps1` | PowerShell | Instalar y verificar el kit v6 | Construido |
| Verificación local del kit | `tooling/repo-patcher-ci/Test-GitHubWorkflow.ps1` | PowerShell, Python y actionlint | Compilar, probar y validar el workflow | Construida |
| Pruebas | `tooling/repo-patcher-ci/test_*.py`, `Test-PluginConsent.ps1` | Python y PowerShell | Probar transporte, cola, runtime, consentimiento y contrato | Construidas |

### 5.2. Componentes decididos para v7 y todavía no construidos

| Componente | Ubicación prevista | Tecnología prevista | Responsabilidad | Estado |
| --- | --- | --- | --- | --- |
| Motor canónico de validación | `tooling/repo-patcher-ci/validate_candidate.py` | Python | Ejecutar toda la secuencia de validación y producir salida estructurada | Pendiente |
| Puente local | `tooling/repo-patcher-bridge/bridge.py` | Python y GitHub CLI o REST | Detectar solicitudes y hacer dispatch inmediato | Pendiente |
| Instalador del puente | `tooling/repo-patcher-bridge/Install-Bridge.ps1` | PowerShell y Programador de tareas | Instalar el puente al iniciar sesión | Pendiente |
| Configuración del puente | `tooling/repo-patcher-bridge/bridge-config.json` | JSON | Configurar repo, workflow, intervalo y rutas de estado | Pendiente |
| Dispatch desde issue | `.github/workflows/validate-repo-patcher.yml` | GitHub Actions | Validar una issue concreta sin rama portadora | Pendiente |
| Wrapper de aplicación validada | `tooling/repo-patcher-ci/Apply-ValidatedRepoPatch.ps1` | PowerShell, Git y Python | Verificar evidencia, aplicar, comprobar, hacer commit y push autorizados | Pendiente |
| Pruebas de latencia y extremo a extremo | `tooling/repo-patcher-ci/test_end_to_end.py` o equivalente | Python y GitHub API | Medir fiabilidad y percentiles | Pendiente |

## 6. Arquitectura construida: v6

```mermaid
flowchart TB
    subgraph GitHub[GitHub]
        Issue[Issue con solicitud y chunks]
        Cron[Schedule cada cinco minutos]
        Workflow[validate-repo-patcher.yml]
        Artifact[Artifacts y logs]
    end

    subgraph Prepare[Job prepare - Ubuntu]
        Queue[issue_queue.py]
        Transport[issue_transport.py]
    end

    subgraph Validate[Job validate - Windows]
        Checks[package_checks.py]
        Runtime[repo_patcher 0.2.0]
        Target[Checkout exacto target_sha]
    end

    subgraph Finalize[Job finalize - Ubuntu]
        Result[Resultado estructurado]
    end

    Issue --> Cron
    Cron --> Workflow
    Workflow --> Queue
    Queue --> Transport
    Transport -->|handoff artifact| Validate
    Target --> Runtime
    Checks --> Runtime
    Runtime --> Artifact
    Artifact --> Finalize
    Finalize --> Result
    Result --> Issue
```

### 6.1. Secuencia de la cola programada v6

```mermaid
sequenceDiagram
    autonumber
    participant Issue as GitHub Issue
    participant Schedule as GitHub schedule
    participant Prepare as Job prepare
    participant Queue as issue_queue.py
    participant Validate as Job validate Windows
    participant RP as RepoPatcher
    participant Finalize as Job finalize

    Schedule->>Prepare: Iniciar escaneo
    Prepare->>Queue: claim
    Queue->>Issue: Buscar solicitud completa más antigua
    Issue-->>Queue: Request y chunks
    Queue->>Issue: Publicar claim
    Queue-->>Prepare: ZIP, request.json y metadatos
    Prepare->>Validate: Handoff artifact
    Validate->>Validate: Checkout exacto target_sha
    Validate->>RP: package-info, explain y check
    Validate->>RP: apply y validadores
    Validate->>Validate: diff-check, check e idempotencia
    Validate-->>Finalize: Conclusión y artifact
    Finalize->>Issue: Publicar resultado
    Finalize->>Issue: Cerrar solicitud
```

### 6.2. Camino manual inmediato ya construido

Este camino demuestra que `workflow_dispatch` puede iniciarse inmediatamente desde el portátil. Su inconveniente es que Samuel debe ejecutar el script y el ZIP se transporta mediante una rama temporal.

```mermaid
sequenceDiagram
    autonumber
    actor Samuel
    participant Submit as Submit-RepoPatch.ps1
    participant Git as Git local
    participant GH as GitHub CLI
    participant Remote as GitHub remoto
    participant Actions as GitHub Actions
    participant Collect as Collect-RepoPatchRun.ps1

    Samuel->>Submit: Ejecutar con package.zip
    Submit->>Git: Crear worktree y rama portadora
    Submit->>Git: Añadir ZIP y crear commit temporal
    Submit->>Remote: Push de rama portadora
    Submit->>GH: gh workflow run
    GH->>Actions: workflow_dispatch
    Submit->>GH: Buscar run_id
    GH-->>Submit: run_id
    Submit->>Collect: Seguir ejecución
    Collect->>Actions: gh run watch
    Collect->>Actions: Descargar artifact
    Collect->>Remote: Eliminar rama portadora
    Collect-->>Samuel: Resultado local
```

## 7. Arquitectura decidida: v7

La dirección v7 conserva el runner remoto y sustituye la intervención manual por un puente local. El camino normal ya no necesita una rama portadora: el ZIP permanece en la issue y el dispatch identifica la issue concreta.

```mermaid
flowchart LR
    ChatGPT[ChatGPT]
    Issue[Issue completa]
    Bridge[bridge.py en portátil]
    Dispatch[workflow_dispatch source=issue]
    Prepare[Job prepare]
    Validate[Job validate Windows]
    Finalize[Job finalize]
    Result[Resultado y artifact]

    ChatGPT -->|crea request y chunks| Issue
    Bridge -->|consulta saliente| Issue
    Bridge -->|issue_number y request_id| Dispatch
    Dispatch --> Prepare
    Prepare -->|reconstruye y reclama| Issue
    Prepare --> Validate
    Validate --> Finalize
    Finalize --> Result
    Result --> Issue
    Issue -->|lectura| ChatGPT
```

### 7.1. Secuencia interactiva v7

```mermaid
sequenceDiagram
    autonumber
    actor Samuel
    participant ChatGPT
    participant Issue as GitHub Issue
    participant Bridge as Puente local
    participant API as GitHub API
    participant Prepare as Job prepare
    participant Validate as Runner Windows
    participant Finalize as Job finalize

    Samuel->>ChatGPT: /patch
    ChatGPT->>API: Leer main y documentos aplicables
    API-->>ChatGPT: target_sha y contenido
    ChatGPT->>ChatGPT: Construir ZIP y SHA-256
    ChatGPT->>Issue: Crear solicitud
    ChatGPT->>Issue: Publicar chunks

    loop Consulta rápida con backoff
        Bridge->>API: Buscar solicitudes completas sin dispatch
        API-->>Bridge: issue_number y request_id
    end

    Bridge->>API: workflow_dispatch source=issue
    API-->>Bridge: Aceptación del dispatch
    API->>Prepare: Iniciar workflow
    Prepare->>Issue: Verificar y publicar claim
    Prepare->>Issue: Reconstruir ZIP exacto
    Prepare->>Validate: Handoff
    Validate->>Validate: Validar contra target_sha
    Validate-->>Finalize: Resultado y artifact
    Finalize->>Issue: Publicar resultado y cerrar

    loop Consulta del resultado
        ChatGPT->>API: Leer run, jobs y artifact
        API-->>ChatGPT: Evidencia
    end

    alt Resultado correcto
        ChatGPT-->>Samuel: Entregar ZIP validado
    else Resultado incorrecto
        ChatGPT->>ChatGPT: Corregir candidata
        ChatGPT->>Issue: Crear nueva solicitud
    end
```

### 7.2. Papel del puente

El puente solo pertenece al plano de control.

Puede:

- consultar issues y comentarios;
- reconocer solicitudes completas;
- deduplicar dispatches;
- invocar el workflow;
- registrar estado técnico local;
- aplicar backoff ante fallos de red.

No puede:

- importar plugins del paquete;
- ejecutar RepoPatcher;
- ejecutar generadores o validadores;
- modificar el checkout local de Mud;
- hacer commit o push de cambios funcionales;
- decidir que un paquete debe incorporarse.

## 8. Motor canónico de validación v7

La lógica hoy embebida en PowerShell dentro del workflow debe extraerse a un único programa:

```text
tooling/repo-patcher-ci/validate_candidate.py
```

Interfaz prevista:

```text
python validate_candidate.py \
    --repo TARGET_REPO \
    --package PACKAGE_ZIP \
    --target-sha SHA \
    --request REQUEST_JSON \
    --output-directory RESULT_DIR \
    [--trust-plugin]
```

### 8.1. Flujo interno

```mermaid
flowchart TD
    Input[ZIP, request y target_sha]
    Identity[Verificar SHA-256 y SHA objetivo]
    Plugin[Detectar plugin sin importarlo]
    Consent{Plugin presente}
    Authorized{Consentimiento explícito}
    Info[package-info]
    Explain[explain]
    Check1[check previo]
    Apply[apply y comandos declarados]
    Diff[git diff --check]
    Check2[check posterior]
    Idempotence[Probar segundo plan no-op]
    Evidence[Escribir result.json, logs y diff]
    Fail[Fallo estructurado]

    Input --> Identity --> Plugin --> Consent
    Consent -->|No| Info
    Consent -->|Sí| Authorized
    Authorized -->|Sí| Info
    Authorized -->|No| Fail
    Info --> Explain --> Check1 --> Apply --> Diff --> Check2 --> Idempotence --> Evidence
    Identity -->|Error| Fail
    Plugin -->|Error| Fail
    Explain -->|Error| Fail
    Check1 -->|Error| Fail
    Apply -->|Error| Fail
    Diff -->|Error| Fail
    Check2 -->|Error| Fail
    Idempotence -->|Error| Fail
    Fail --> Evidence
```

### 8.2. Salidas canónicas

```text
result.json
request.json
validation-metadata.json
validation-transcript.txt
failure-summary.txt
applied.patch
git-diff-binary.patch
git-status.txt
git-diff-stat.txt
```

El workflow, una prueba local u otro orquestador futuro deben consumir las mismas salidas.

## 9. Estados de una solicitud

```mermaid
stateDiagram-v2
    [*] --> Incompleta: issue creada
    Incompleta --> Completa: todos los chunks presentes
    Completa --> Despachada: puente o fallback crea workflow
    Despachada --> Reclamada: prepare publica claim
    Reclamada --> Validando: runner recibe handoff
    Validando --> Correcta: todas las comprobaciones pasan
    Validando --> Incorrecta: alguna comprobación falla
    Reclamada --> Completa: claim expira sin resultado
    Correcta --> Cerrada: finalize publica resultado
    Incorrecta --> Cerrada: finalize publica diagnóstico
    Cerrada --> [*]
```

### 9.1. Identidades persistentes

| Identidad | Función |
| --- | --- |
| `request_id` | Distinguir una candidata lógica |
| `issue_number` | Localizar el transporte y su estado |
| `package_sha256` | Identificar exactamente los bytes del ZIP |
| `target_sha` | Identificar exactamente la revisión validada |
| `run_id` | Localizar la ejecución remota |
| `artifact_name` | Localizar la evidencia producida |

## 10. Límites de confianza

```mermaid
flowchart LR
    subgraph TrustedControl[Plano de control confiable]
        ChatGPT[Generación de candidata]
        Bridge[Puente local]
        Prepare[Job prepare]
        Finalize[Job finalize]
    end

    subgraph UntrustedExecution[Plano de ejecución no confiable]
        Package[ZIP candidato]
        Plugin[Plugin Python]
        Commands[Generadores y validadores]
        Worker[Job validate Windows]
    end

    subgraph Persistent[Estado persistente]
        Repo[Git repository]
        Issues[Issues]
        Artifacts[Artifacts]
    end

    ChatGPT --> Issues
    Bridge --> Issues
    Bridge --> Prepare
    Prepare --> Package
    Package --> Worker
    Plugin --> Worker
    Commands --> Worker
    Worker --> Artifacts
    Finalize --> Issues
    Repo --> Worker
```

### 10.1. Reglas de seguridad

1. `prepare` y `finalize` pueden escribir en issues, pero no ejecutan código del paquete.
2. `validate` ejecuta código del paquete, pero no recibe permisos de escritura en issues.
3. El puente usa credenciales locales de GitHub, pero no entrega esas credenciales al paquete.
4. El runner usa checkouts separados para el plano de control y el `target_sha`.
5. El plugin se autoriza por candidata, no por autor ni por historial.
6. El ZIP validado se identifica por bytes, no solo por contenido lógico.
7. El checkout usado para validar es temporal y desechable.
8. La aplicación final local puede ejecutar el plugin únicamente después de la aprobación explícita de Samuel y de verificar la identidad del ZIP validado.

## 11. Aplicación y publicación

La validación remota y la incorporación a `main` son operaciones distintas.

```mermaid
sequenceDiagram
    autonumber
    actor Samuel
    participant Installer as Apply-ValidatedRepoPatch.ps1
    participant GitHub as GitHub
    participant Repo as Checkout local
    participant RP as RepoPatcher
    participant Git

    Samuel->>Installer: Aprobar request_id
    Installer->>GitHub: Descargar evidencia y ZIP validado
    GitHub-->>Installer: target_sha, package_sha256 y artifact
    Installer->>Installer: Verificar SHA-256 del ZIP
    Installer->>Repo: Verificar HEAD y estado limpio

    alt Identidad o base incorrecta
        Installer-->>Samuel: Rechazar aplicación
    else Identidad correcta
        Installer->>RP: apply sobre checkout local
        RP-->>Installer: Diff y resultado
        Installer->>Repo: Comprobaciones finales
        Installer-->>Samuel: Mostrar resumen
        Samuel->>Installer: Confirmar publicación
        Installer->>Git: Crear commit atómico
        Installer->>GitHub: Push autorizado
        GitHub-->>Installer: Commit publicado
        Installer-->>Samuel: SHA publicado
    end
```

### 11.1. Responsabilidad de la decisión

| Acción | Responsable de decidir | Responsable de ejecutar |
| --- | --- | --- |
| Diseñar candidata | Samuel y ChatGPT | ChatGPT |
| Validar candidata | Política automática | GitHub Actions |
| Corregir candidata fallida | ChatGPT | ChatGPT |
| Aceptar incorporación | Samuel | Samuel |
| Aplicar paquete aceptado | Samuel autoriza | Wrapper local y RepoPatcher |
| Crear commit | Política de commits | Wrapper local o Codex |
| Hacer push | Samuel autoriza | Wrapper local o Codex |

## 12. Matriz de responsabilidades técnicas

| Paso | Componente actual v6 | Componente objetivo v7 | Ejecuta código del paquete |
| --- | --- | --- | ---: |
| Leer el repositorio y las instrucciones | ChatGPT mediante GitHub | Igual | No |
| Construir el ZIP | ChatGPT | Igual | No |
| Codificar para issue | `issue_transport.py encode` o ChatGPT | Igual | No |
| Detectar solicitud | `schedule` + `issue_queue.py` | `bridge.py`; schedule como fallback | No |
| Crear workflow | cron o `Submit-RepoPatch.ps1` | `bridge.py` mediante dispatch | No |
| Reclamar solicitud | `issue_queue.py claim` | `issue_queue.py` adaptado a issue concreta | No |
| Reconstruir ZIP | `issue_transport.py` | Igual | No |
| Detectar plugin | `package_checks.py` | `validate_candidate.py` usando helper | No |
| Validar y aplicar temporalmente | Bloque PowerShell del workflow | `validate_candidate.py` | Sí |
| Publicar resultado | `issue_queue.py finalize` | Igual o adaptado | No |
| Revisar evidencia | ChatGPT | Igual | No |
| Aplicar al checkout real | Manual | Wrapper local futuro | Sí |
| Crear commit | Manual o Codex | Wrapper local futuro | No |
| Push | Manual con autorización | Wrapper local futuro con autorización | No |

## 13. Recuperación y fallos

```mermaid
flowchart TD
    Request[Solicitud completa]
    BridgeUp{Puente disponible}
    Dispatch[Dispatch inmediato]
    Schedule[Schedule de recuperación]
    Runner{Runner disponible}
    Retry[Reintento o nueva candidata]
    Result[Resultado persistente]

    Request --> BridgeUp
    BridgeUp -->|Sí| Dispatch
    BridgeUp -->|No| Schedule
    Dispatch --> Runner
    Schedule --> Runner
    Runner -->|Sí| Result
    Runner -->|No| Retry
    Retry --> Dispatch
```

### 13.1. Casos previstos

| Fallo | Comportamiento esperado |
| --- | --- |
| Portátil apagado | La issue permanece; el schedule puede recuperarla y el puente la verá al reanudarse |
| Puente sin red | Backoff; no se ejecuta código del paquete |
| Dispatch duplicado | Claim y resultado persistentes evitan procesado efectivo duplicado |
| Runner no disponible | GitHub mantiene o reintenta el job; la solicitud conserva identidad |
| Claim sin resultado | Puede reclamarse tras el umbral de caducidad |
| ZIP corrupto | Falla antes de ejecutar RepoPatcher |
| Plugin no autorizado | Falla antes de importarlo |
| Validador falla | Se conserva artifact y diagnóstico |
| Aplicación local sobre SHA distinto | El wrapper rechaza la operación |
| ZIP local distinto al validado | El wrapper rechaza la operación |

## 14. Plan de implementación

### Fase 1. Motor independiente

- crear `validate_candidate.py`;
- mover la secuencia de validación fuera del bloque PowerShell;
- mantener las mismas salidas y semántica;
- ejecutar las pruebas actuales contra el motor extraído.

### Fase 2. Dispatch de issue concreta

- ampliar `workflow_dispatch` con `source`, `issue_number` y `request_id`;
- permitir que `prepare` reconstruya una issue concreta;
- conservar la rama portadora como modo manual de diagnóstico;
- conservar el schedule como recuperación.

### Fase 3. Puente local

- crear `bridge.py`;
- implementar consulta condicional, deduplicación y backoff;
- instalar mediante tarea al inicio de sesión;
- registrar estado sin almacenar nuevos secretos;
- demostrar que no ejecuta código del paquete.

### Fase 4. Aplicación validada

- crear `Apply-ValidatedRepoPatch.ps1`;
- verificar `request_id`, `package_sha256`, `target_sha` y estado limpio;
- aplicar mediante RepoPatcher;
- mostrar el diff;
- crear commit conforme a `POLITICA-DE-COMMITS.md`;
- hacer push solo después de autorización explícita.

### Fase 5. Pruebas de aceptación

- declarativo válido;
- plugin rechazado sin consentimiento;
- plugin autorizado;
- ZIP corrupto;
- SHA inexistente;
- paquete no idempotente;
- validador fallido;
- solicitudes simultáneas;
- dispatch duplicado;
- suspensión y reanudación del portátil;
- veinte validaciones consecutivas con medición de latencia.

## 15. Criterios de aceptación v7

La arquitectura v7 no se considerará operativa hasta demostrar:

```text
ninguna modificación del checkout canónico durante validación
ninguna credencial de control visible al código del paquete
ninguna solicitud procesada dos veces de forma efectiva
identidad exacta entre ZIP validado y ZIP entregado
recuperación de solicitudes cuando el puente no está disponible
detección local p95 inferior a 3 segundos
validación total p50 inferior a 45 segundos
validación total p95 inferior a 90 segundos
```

El objetivo de diseño sigue siendo completar habitualmente la validación en menos de un minuto. El umbral p95 inicial permite medir la variabilidad del aprovisionamiento de runners antes de imponer un requisito más estricto.

## 16. Autoridad documental propuesta

La documentación debería dividirse así:

| Documento | Autoridad |
| --- | --- |
| `gobierno/USO-DE-REPO-PATCHER.md` | Formato, semántica y comportamiento del runtime |
| `gobierno/ARQUITECTURA-DE-REPO-PATCHER.md` | Componentes, responsabilidades, flujos, seguridad y estados |
| `tooling/repo-patcher-ci/README.md` | Uso operativo del kit instalado y comandos concretos |
| Tests y workflow | Contrato ejecutable de la implementación |

`USO-DE-REPO-PATCHER.md` debería enlazar este documento, pero no absorber todos sus diagramas. Así se evita mezclar la especificación del motor con una arquitectura de orquestación que puede evolucionar independientemente.
