---
title: "Comando conversacional /patch de MUD"
status: vigente
scope: "Construcción, validación remota y entrega de paquetes RepoPatcher desde ChatGPT"
repo-patcher-version: "0.2.0"
validation-protocol: "mud-repo-patcher-validation/v1"
---

# Comando `/patch` de MUD

## 1. Activación y naturaleza

Aplica íntegramente estas instrucciones cuando el mensaje del usuario comience por:

```text
/patch
/patch <alcance o cambio concreto>
```

Este documento define un procedimiento conversacional para ChatGPT. No convierte
`/patch` en un comando nativo ni sustituye las políticas del repositorio.

## 2. Resultado obligatorio

El objetivo es entregar un paquete ZIP definitivo que:

1. integre todo el alcance decidido;
2. sea aplicable mediante el RepoPatcher vendorizado en MUD;
3. haya obtenido verde en el laboratorio Windows remoto contra un SHA exacto;
4. sea exactamente el objeto validado y devuelto por `get_validated_candidate`.

No basta con entregar un diff, código suelto, una propuesta textual, un ZIP construido
localmente ni una copia recuperada desde otro artifact.

El repositorio canónico es:

```text
https://github.com/R3Neer/Mud
```

## 3. Alcance conversacional

El seguimiento existe únicamente dentro de la conversación actual.

1. Revisa todo lo concretado en esta conversación.
2. Revisa los `/def` y `/patch` anteriores del mismo chat.
3. Considera cubierto únicamente lo documentado realmente por un `/def` o implementado
   realmente por un `/patch` definitivo.
4. Un borrador, una propuesta, una candidata fallida o un patch incompleto no cubren lo
   que dejaron fuera.
5. No uses otros chats para decidir qué está cubierto.

Con `/patch <alcance>`, implementa íntegramente ese alcance. Con `/patch` sin argumentos,
incluye todas las decisiones concretas, compatibles y suficientemente definidas de la
conversación que todavía no estén reflejadas.

No reduzcas silenciosamente el alcance para producir un paquete más pequeño o fácil de
validar.

## 4. Decisiones frente a detalles de implementación

Distingue expresamente entre:

### 4.1. Decisiones de diseño

Son elecciones que cambian el significado del lenguaje, la experiencia normativa, la
compatibilidad o la política del proyecto. Si falta realmente una de estas elecciones y
existen varias respuestas plausibles con consecuencias materiales distintas, pregunta al
usuario antes de fijarla.

### 4.2. Consecuencias técnicas determinables

No son decisiones nuevas. Debes resolverlas autónomamente cuando se deducen de decisiones
ya aceptadas. Incluyen, entre otras:

- escribir la EBNF correspondiente;
- definir nodos CST y constructores AST coherentes;
- propagar una regla al AST superficial y resuelto;
- actualizar resolución de nombres, anclas, cobertura y casos de conformidad;
- elegir nombres internos, estructura de módulos y operaciones de patch razonables;
- redactar texto normativo que exprese fielmente una decisión cerrada;
- actualizar referencias, índices generados, ejemplos y validadores afectados.

Puedes crear estos detalles sin pedir autorización adicional. «No inventar decisiones» no
significa «no completar la ingeniería necesaria».

### 4.3. Regla ante una duda localizada

Una duda localizada no permite excluir toda una capa de integración.

1. Implementa las consecuencias inequívocas.
2. Aísla la elección verdaderamente abierta.
3. Pregunta de forma concreta solo por esa elección si bloquea el resultado coherente.
4. No presentes como definitivo un patch que omite superficies necesarias.

## 5. Inspección previa obligatoria

Antes de diseñar el paquete:

1. Consulta el repositorio canónico actual y registra el SHA completo de base.
2. Lee `AGENTS.md`.
3. Lee las políticas y README aplicables a cada ruta afectada.
4. Para formalización didáctica, lee íntegramente:
   - `aprendizaje/REGLAS-DIDACTICAS.md`;
   - `aprendizaje/PROGRESO.md`;
   - `especificacion/00-convenciones-editoriales.md`.
5. Para RepoPatcher, inspecciona:
   - `gobierno/USO-DE-REPO-PATCHER.md`;
   - `tooling/repo-patcher-runtime/`;
   - `.github/workflows/validate-repo-patcher-remote.yml`.
6. Localiza decisiones, preguntas, generadores, validadores e índices relacionados.
7. Busca todas las referencias a los conceptos, anclas, producciones y tipos afectados.
8. Comprueba todos los artefactos que puedan quedar desincronizados.

No construyas el paquete solo a partir de fragmentos recordados o del último mensaje.

## 6. Autoridad documental

Respeta esta separación:

- `especificacion/`: norma;
- `aprendizaje/`: material didáctico no normativo;
- `notas/`: análisis, decisiones y preguntas;
- `gobierno/`: procesos;
- `tooling/`: herramientas y validadores.

Para el formato y comportamiento de RepoPatcher prevalecen:

1. `tooling/repo-patcher-runtime/`;
2. sus pruebas y el workflow vigente;
3. `gobierno/USO-DE-REPO-PATCHER.md`.

No uses campos que el runtime actual ignore. Señala cualquier discrepancia encontrada.

## 7. Auditoría de propagación

Antes de empaquetar, construye internamente una matriz de impacto. Para cada superficie
indica una de estas conclusiones:

```text
modificar
regenerar
validar sin cambios
no aplicable
bloqueado por una decisión abierta
```

Una conclusión «validar sin cambios» debe estar respaldada por una razón concreta. No
basta con decir que un archivo fue auditado.

En cambios de lenguaje comprueba, según corresponda:

- modelo matemático y semántica;
- léxico y categorías de tokens;
- gramática normativa y EBNF;
- syntax kinds y cobertura sintáctica;
- CST sin pérdidas y recuperación;
- transformación CST a AST superficial;
- AST superficial y AST resuelto;
- resolución de nombres, anclas y grafo de dependencias;
- reflexión, metadatos y diagnósticos;
- ejemplos normativos y casos sintácticos;
- decisiones, preguntas e índices;
- generadores y validadores.

Un cambio derivado de una misma decisión puede y debe atravesar todas estas superficies en
un único patch coherente. La atomicidad no exige amputar consecuencias necesarias.

## 8. Diseño del paquete

El nombre humano recomendado es:

```text
mud-<descripcion>-<sha-corto>.zip
```

El ZIP contendrá `patch.yaml` en su raíz y todos sus recursos.

Exige normalmente:

- repositorio `R3Neer/Mud`;
- árbol limpio;
- SHA exacto de base, escrito entre comillas;
- archivos estructurales requeridos.

Prefiere, por orden:

1. operaciones declarativas exactas;
2. archivos completos incluidos como recursos;
3. generadores y validadores existentes;
4. plugin Python únicamente cuando lo anterior no exprese el cambio con seguridad.

Usa precondiciones y aserciones para detectar divergencias. El resultado debe ser
idempotente según el contrato del harness remoto.

## 9. Plugins Python

Los plugins ejecutan código con los permisos del proceso y requieren consentimiento
explícito.

Cuando sean imprescindibles:

- usa exclusivamente la API real del `PatchContext` versionado;
- no escribas directamente en el repositorio;
- no lances procesos externos;
- no accedas a credenciales ni a la red;
- mantén comportamiento determinista e idempotente;
- separa el código en módulos textuales completos cuando resulte grande;
- identifica claramente todo el código ejecutable;
- transporta `trust_plugin: true` únicamente cuando el usuario haya autorizado el plugin.

No ocultes código o recursos dentro de blobs comprimidos o codificados.

## 10. Transporte MCP obligatorio

La entrada estable del validador acepta archivos lógicos UTF-8 completos. Antes de llamar
al complemento, diseña todos los lotes.

### 10.1. Formato permitido

Cada recurso del paquete se transmite como un archivo textual independiente mediante
`stage_candidate_files`.

Está prohibido usar como mecanismo de transporte:

- ZIP en base64;
- `payload.b64`;
- gzip, tar o ZIP anidados;
- JSON comprimido que contenga archivos;
- código Python empaquetado como un blob opaco;
- recursos binarios arbitrarios;
- fragmentos que deban recomponerse para formar un archivo.

Si el paquete necesita varios módulos Python, incluye cada `.py` como archivo lógico
normal. El loader puede cargarlos desde el directorio del paquete, pero no debe
encapsularlos con base64, compresión ni cadenas generadas.

### 10.2. Límites de cada lote

Cada llamada a `stage_candidate_files` admite:

```text
máximo 32 archivos completos
máximo 24.576 caracteres de contenido total
```

Además:

- no dividas un archivo entre llamadas;
- no mezcles dos versiones del mismo path;
- usa rutas POSIX relativas;
- calcula la suma de caracteres antes de cada llamada y deja margen cuando sea posible;
- reparte paquetes grandes entre tantos lotes como sea necesario;
- conserva el mismo `request_id` en todos los lotes de una candidata;
- usa un `batch_id` distinto y descriptivo por lote.

Si un solo recurso supera el límite, rediseña el paquete con operaciones declarativas o
módulos lógicos menores cuando ello no cambie su significado. Si no existe una
descomposición segura, declara el bloqueo: nunca recortes ni dividas silenciosamente un
archivo.

### 10.3. Identidad durante staging

Para texto recién generado no inventes `expected_size` ni `expected_sha256`. El Worker
calcula ambos sobre los bytes UTF-8 recibidos.

Después de cada llamada verifica en la respuesta:

- `request_id` y `batch_id`;
- número y rutas de archivos;
- tamaño y SHA-256 calculados;
- ausencia de error o truncamiento.

No continúes si falta un lote o una respuesta quedó indeterminada.

## 11. Secuencia remota definitiva

Ejecuta exactamente este flujo:

```text
stage_candidate_files × N
→ submit_candidate
→ await_validation hasta estado terminal
→ read_validation_evidence
→ get_validated_candidate si succeeded
```

### 11.1. Envío

`submit_candidate` debe incluir:

- `protocol: mud-repo-patcher-validation/v1`;
- el mismo `request_id` usado en staging;
- SHA completo inspeccionado como `target_sha`;
- todos los `batch_ids`, una sola vez y en orden deliberado;
- número total exacto de archivos;
- `trust_plugin` explícito.

No reconstruyas el ZIP: el Worker debe construir el objeto definitivo a partir de los
lotes almacenados.

### 11.2. Espera y diagnóstico

Usa `await_validation` hasta obtener:

```text
succeeded
failed
infrastructure_error
expired
```

Después usa `read_validation_evidence`.

Si el fallo pertenece a la candidata:

1. analiza el diagnóstico real;
2. corrige los archivos necesarios;
3. crea una nueva `request_id`;
4. vuelve a ejecutar todo el ciclo sin pedir intervención, salvo que aparezca una decisión
   de diseño auténticamente abierta.

No corrijas contenido semántico debido a un fallo puramente infraestructural.

### 11.3. Pérdida temporal de herramientas

Los permisos concedidos al complemento no garantizan que toda llamada vaya a ejecutarse.
La interfaz puede bloquear una acción o dejar de exponer temporalmente una herramienta.

Si ocurre:

1. conserva el `request_id`, el run ID y todos los hashes conocidos;
2. no reconstruyas el ZIP;
3. no repitas `submit_candidate` con otra identidad si el request ya fue aceptado;
4. intenta reanudar el mismo request mediante las herramientas estables cuando vuelvan a
   estar disponibles;
5. si no puedes ejecutar el paso final, detente y marca el resultado como borrador.

El archivo `candidate.zip` incluido dentro de la evidencia, aunque tenga los mismos bytes,
no sustituye contractualmente a `get_validated_candidate`.

## 12. Qué demuestra el laboratorio

El workflow remoto usa el control confiable y el runtime RepoPatcher 0.2.0 procedente del
`target_sha`. Ejecuta sobre clones Windows limpios:

- `package-info`;
- `explain` y `check` con comprobación de ausencia de efectos laterales;
- aplicación completa independiente en A y B;
- generadores y validadores;
- `git diff --check`;
- replanificación no mutante con `changed_paths() == []` dentro de cada clon;
- comparación semántica entre A y B como evidencia de reproducibilidad;
- comprobación de que control y target-source no fueron modificados.

No describas esta convergencia como un «segundo `apply`»: RepoPatcher 0.2.0 exige un árbol
limpio para la aplicación normal y el harness no aplica dos veces sobre el árbol sucio.

## 13. Entrega estricta

Solo existe un `/patch` definitivo cuando se cumplen simultáneamente estas condiciones:

1. `state == succeeded`;
2. la evidencia identifica el `target_sha` correcto y RepoPatcher 0.2.0;
3. se ejecutó `get_validated_candidate` para ese mismo `request_id`;
4. el enlace entregado procede de esa respuesta;
5. SHA-256 y tamaño coinciden con la candidata validada.

Está prohibido sustituir el paso final por:

- una reconstrucción local;
- el ZIP previo al staging;
- una copia extraída de `evidence.zip`;
- otro objeto con hash coincidente;
- un enlace perteneciente a otra `request_id`.

Si `get_validated_candidate` no está disponible, informa de que los bytes pueden tener
evidencia favorable, pero el procedimiento `/patch` no terminó. El resultado será DRAFT.

La respuesta definitiva incluirá:

- enlace devuelto por `get_validated_candidate`;
- objetivo implementado;
- SHA base completo;
- archivos afectados;
- validaciones ejecutadas;
- SHA-256 y tamaño del ZIP;
- exclusiones reales y su justificación.

## 14. Exclusiones y cobertura

Solo excluye:

- preguntas de diseño genuinamente abiertas;
- contradicciones que necesiten una decisión del usuario;
- trabajo expresamente fuera del alcance solicitado;
- superficies demostrablemente no afectadas tras auditarlas.

No son motivos válidos de exclusión:

- que la integración sea extensa;
- que exija modificar gramática, CST, AST o resolución de nombres;
- que haya que crear detalles técnicos deducibles;
- que el paquete necesite varios lotes MCP;
- que una solución integral tarde más en razonar.

Enumera las exclusiones en la entrega. Después del comando solo se considera cubierto lo
implementado realmente por el ZIP definitivo; todo lo demás continúa pendiente en la
conversación.

## 15. Prohibiciones resumidas

No:

- uses la cola de issues o el workflow v6 en el camino normal;
- hagas commits, ramas, issues o PR desde el complemento;
- construyas un ZIP posterior a la validación;
- entregues el ZIP incluido en la evidencia como sustituto;
- encapsules archivos en base64 o blobs comprimidos;
- ejecutes un segundo `apply` sobre un checkout ya modificado;
- afirmes que una comprobación se ejecutó si solo fue inspeccionada;
- declares completa una integración parcial de decisiones ya cerradas.
