---
title: "Uso de repo-patcher"
status: vigente
scope: "Entrega y validación de paquetes descargables"
repo-patcher-version: "0.2.0"
package-format: 1
audited-runtime-commit: "15a9c1f61cd154a5c8dfcfc6500f70f0e9e78c66"
---

# Guía técnica autoritativa de `repo-patcher` 0.2.0

## 1. Autoridad y versión exacta

Esta guía describe la implementación vendorizada en:

```text
tooling/repo-patcher-runtime/repo_patcher/
```

La versión exacta es `0.2.0`, declarada por `repo_patcher.__version__` en
`repo_patcher/__init__.py`.

Para resolver discrepancias se usa esta precedencia:

1. Código vendorizado de `tooling/repo-patcher-runtime/`.
2. Workflow y comprobaciones vigentes.
3. Esta guía.

Las referencias técnicas se expresan como `archivo::símbolo` en lugar de números de
línea. Así siguen siendo verificables aunque una edición inserte o retire líneas sin
cambiar el comportamiento descrito.

## 2. Modelo de paquete

Un paquete es:

- un directorio con `patch.yaml` directamente en su raíz; o
- un ZIP con `patch.yaml` en la raíz; o
- un ZIP con exactamente un directorio de primer nivel que contenga `patch.yaml`.

Ejemplos válidos:

```text
patch.zip
├── patch.yaml
├── transform.py
└── files/
```

```text
patch.zip
└── mi-patch/
    ├── patch.yaml
    └── files/
```

El extractor comprueba que las rutas resueltas permanezcan dentro del directorio
temporal. Si no existe `patch.yaml`, o existen varios candidatos de primer nivel, el
paquete se rechaza.

Fuente: `repo_patcher/patch_source.py::_safe_extract`,
`repo_patcher/patch_source.py::_manifest_root` y
`repo_patcher/patch_source.py::open_patch_source`.

## 3. Manifiesto `patch.yaml`

### 3.1. Nivel raíz

| Campo | Obligatorio | Tipo | Predeterminado | Semántica |
| --- | ---: | --- | --- | --- |
| `schema` | No | entero igual a `1` | `1` | Cualquier otro valor se rechaza. |
| `id` | Sí | texto no vacío | — | Identidad del paquete. |
| `version` | No | texto, entero o real | `"1"` | Se normaliza a texto. |
| `title` | Sí | texto no vacío | — | Título humano. |
| `description` | No | texto | `""` | Descripción humana. |
| `repository` | No | mapa | `{}` | Restricciones de nombre y remote. |
| `compatibility` | No | mapa | `{}` | Restricciones de Git y archivos. |
| `plugin` | No | mapa o `null` | `null` | Plugin Python. |
| `operations` | Condicional | lista de mapas | `[]` | Debe existir `operations`, `plugin` o ambos. |
| `generators` | No | lista de comandos | `[]` | Se ejecutan tras escribir cambios. |
| `validators` | No | lista de comandos | `[]` | Se ejecutan después de los generadores. |

El runtime no rechaza campos raíz desconocidos: los ignora. Un error tipográfico puede,
por tanto, quedar silenciosamente sin efecto. No se deben usar campos que el runtime no
lee.

Fuente: `repo_patcher/manifest.py::load_manifest`.

### 3.2. Restricción de repositorio

```yaml
repository:
  names: [Mud]
  remotes:
    - github.com/R3Neer/Mud
```

Se admiten las formas singular y plural:

```yaml
repository:
  name: Mud
  remote: https://github.com/R3Neer/Mud.git
```

El nombre de la carpeta se compara sin distinguir mayúsculas. El remote se normaliza:
se elimina `.git`, se aceptan formas URL y `git@host:ruta`, y se compara en minúsculas.

Fuentes: `repo_patcher/manifest.py::load_manifest` y
`repo_patcher/gitops.py::normalize_remote`, `origin_remote`,
`verify_compatibility`.

### 3.3. Compatibilidad

```yaml
compatibility:
  clean_worktree: true
  exact_heads:
    - 0123456789abcdef0123456789abcdef01234567
  required_ancestor: 89abcdef0123456789abcdef0123456789abcdef
  required_files:
    - AGENTS.md
```

| Campo | Alias | Tipo | Predeterminado | Semántica |
| --- | --- | --- | --- | --- |
| `clean_worktree` | — | booleano | `true` | Se exige durante `apply`; `explain` y `check` no lo exigen. |
| `exact_heads` | `exact_head` | texto o lista | vacío | `HEAD` debe coincidir literalmente con uno de los SHA. |
| `required_ancestor` | — | texto o `null` | `null` | Se usa `git merge-base --is-ancestor`. |
| `required_files` | — | texto o lista | vacío | Cada ruta debe existir bajo la ruta construida desde la repo. |

El contrato de limpieza equivale a:

```text
git status --porcelain=v1 --untracked-files=all
```

Incluye cambios staged, unstaged y no rastreados no ignorados. No enumera archivos
ignorados.

`required_files` no aplica una validación independiente contra `..`; los paquetes de MUD
no deben usar rutas que pretendan escapar de la repo.

Fuentes: `repo_patcher/manifest.py::load_manifest`,
`repo_patcher/gitops.py::verify_compatibility` y
`repo_patcher/gitops.py::clean_worktree_contract`.

### 3.4. Plugin

```yaml
plugin:
  file: transform.py
  entrypoint: apply
```

- `file` es obligatorio y no vacío si existe `plugin`.
- `entrypoint` es opcional y vale `apply` por defecto.
- La ruta resuelta debe permanecer dentro del paquete y existir como archivo.
- Importar el módulo ejecuta su código de nivel superior.
- El entrypoint debe ser invocable y recibe `(ctx, manifest)`.

Fuente: `repo_patcher/manifest.py::load_manifest` y
`repo_patcher/plugin.py::load_plugin`.

### 3.5. Operaciones declarativas

Cada elemento de `operations` debe contener exactamente una operación cuyo payload sea un
mapa.

Fuente general: `repo_patcher/operations.py::apply_declarative_operations`.

#### `create`

```yaml
- create:
    path: docs/nuevo.md
    content: "contenido\n"
```

O desde el paquete:

```yaml
- create:
    path: docs/nuevo.md
    source: files/nuevo.md
```

Si existe `source`, se usa esa fuente. Si el destino ya existe con los mismos bytes, es
no-op; con contenido distinto, es conflicto.

#### `delete`

```yaml
- delete:
    path: docs/obsoleto.md
```

Un archivo ausente produce no-op.

#### `replace`

```yaml
- replace:
    path: README.md
    old: "antes"
    new: "después"
    count: 1
```

`count` debe ser entero. Cero coincidencias es no-op solo cuando `new` no está vacío y ya
aparece en el archivo. Si `count >= 0`, el número total de apariciones debe ser exactamente
`count`; un valor negativo reemplaza todas.

#### `regex_replace`

```yaml
- regex_replace:
    path: archivo.md
    pattern: "(?m)^Viejo$"
    replacement: "Nuevo"
    count: 1
    flags: [MULTILINE]
```

Los flags se resuelven por nombre en el módulo `re`. Cero sustituciones es conflicto. En
0.2.0 no hay una comprobación explícita del tipo de `count` antes de pasarlo a `re.subn`.
`regex_replace` no implementa detección automática de «ya aplicado».

#### `append_once`

```yaml
- append_once:
    path: README.md
    marker: "## Instalación"
    content: |
      ## Instalación

      Texto.
```

Si `marker` aparece en cualquier posición, no cambia nada. En otro caso añade el contenido
tras recortar el final existente y el propio bloque.

#### `assert_contains`

```yaml
- assert_contains:
    path: AGENTS.md
    text: "Instrucciones"
```

Falla si falta el fragmento.

#### `assert_not_contains`

```yaml
- assert_not_contains:
    path: README.md
    text: "texto retirado"
```

Falla si aparece el fragmento.

Las operaciones desconocidas se rechazan.

Fuentes de semántica: `repo_patcher/context.py::PatchContext` y sus métodos
`create_text_file`, `create_from_patch`, `delete_file`, `replace_exact`,
`replace_regex`, `append_once`, `assert_contains` y `assert_not_contains`.

### 3.6. Generadores y validadores

```yaml
generators:
  - name: Regenerar índice
    command: ["{python}", tooling/generate.py]
    cwd: .
    env:
      MODE: generated
```

Cada entrada admite:

- `command`: lista no vacía de textos, obligatoria;
- `name`: texto, opcional;
- `cwd`: texto relativo a la repo, `.` por defecto;
- `env`: mapa texto a texto.

Sustituciones literales:

```text
{python} → intérprete actual
{repo}   → raíz de la repo
{patch}  → raíz física o temporal del paquete
```

No se usa shell. El preflight comprueba `cwd` y ejecutable, pero no ejecuta el comando.
Durante `apply`, stdout y stderr se capturan como UTF-8 con sustitución de errores. Las
rutas creadas por cada comando se atribuyen a la transacción para una limpieza limitada si
hay rollback.

Fuente: `repo_patcher/commands.py::_expand`, `preflight_commands` y
`execute_commands`.

## 4. Comandos y consentimiento de plugins

Comandos públicos:

```text
repo-patcher tutorial
repo-patcher doctor
repo-patcher package-info
repo-patcher explain
repo-patcher check
repo-patcher apply
```

Fuente: `repo_patcher/cli.py::_parser` y `main`.

### `package-info`

- abre el paquete;
- carga el manifiesto;
- no carga ni ejecuta el plugin;
- muestra un SHA-256 lógico del árbol del paquete.

El SHA lógico no es el SHA-256 de los bytes del ZIP. El transporte CI calcula además el
hash exacto del archivo ZIP.

### `explain` y `check`

Ambos construyen el plan completo en memoria:

1. verifican compatibilidad;
2. ejecutan operaciones declarativas sobre el contexto virtual;
3. cargan y ejecutan virtualmente el plugin si existe;
4. hacen preflight de generadores y validadores.

No escriben cambios ni ejecutan generadores o validadores. `check` con código cero significa
que pudo construir el plan; no demuestra por sí solo que una segunda aplicación sea no-op.

### `apply`

Construye el mismo plan, exige limpieza cuando corresponde y, si existen cambios:

1. crea una transacción;
2. escribe el contexto virtual;
3. ejecuta generadores;
4. comprueba que `HEAD` no cambió;
5. ejecuta validadores;
6. ejecuta `git diff --check`;
7. vuelve a comprobar `HEAD`;
8. emite el diff si se solicitó.

Si el plan no contiene cambios, retorna sin ejecutar generadores ni validadores.

Fuente: `repo_patcher/engine.py::build_plan` y `apply_plan`.

### Consentimiento local

Si el manifiesto contiene plugin, `explain`, `check` y `apply` exigen consentimiento antes
de cargarlo:

- en una terminal interactiva se solicita escribir `SI`;
- `--trust-plugin` concede consentimiento no interactivo;
- sin consentimiento se aborta antes de cargar el plugin.

El consentimiento debe aplicarse a los tres comandos. Añadir `--trust-plugin` únicamente a
`apply` no sirve porque `explain` y `check` también ejecutan el plugin virtualmente.

El plugin no está aislado: es Python arbitrario ejecutado con los permisos del proceso. La
autorización no debe inferirse por el origen del paquete.

Fuente: `repo_patcher/cli.py::_confirm_plugin` y `main`,
`repo_patcher/plugin.py::load_plugin`.

## 5. API del plugin

Firma esperada:

```python
def apply(ctx, manifest) -> None:
    ...
```

`manifest` es `repo_patcher.models.Manifest`.

`ctx` es `repo_patcher.context.PatchContext` y ofrece:

```text
exists
read_bytes
read_text
write_bytes
write_text
create_text_file
create_from_patch
delete_file
replace_exact
replace_regex
append_once
assert_contains
assert_not_contains
load_yaml
save_yaml
note
original_bytes
changed_paths
is_already_applied
commit_to_disk
restore_original
```

Los plugins deben usar el contexto virtual. No deben llamar a `commit_to_disk` ni
`restore_original`: son operaciones del motor. Tampoco deben escribir directamente en la
repo ni lanzar procesos externos; hacerlo evita que el motor pueda atribuir y revertir los
cambios con garantías.

Las rutas recibidas por `PatchContext` no pueden ser absolutas ni contener `..`, y su ruta
resuelta debe permanecer bajo la repo.

Fuente: `repo_patcher/context.py::PatchContext`,
`repo_patcher/models.py::Manifest` y `repo_patcher/plugin.py::load_plugin`.

## 6. Transacción y rollback de 0.2.0

La implementación 0.2.0 no usa como mecanismo ordinario de rollback:

```text
git reset --hard
git clean -fd
```

Antes de escribir, `RepositoryTransaction` captura:

- `HEAD` inicial;
- conjunto de rutas existentes fuera de `.git`;
- snapshots de archivos rastreados;
- snapshots de archivos no rastreados no ignorados;
- bytes del índice Git;
- rutas nuevas atribuibles al contexto, generadores y validadores.

En caso de error intenta, por pasos independientes:

1. restaurar los archivos registrados por `PatchContext`;
2. restaurar `HEAD` mediante `git update-ref` si cambió;
3. restaurar archivos rastreados, incluidos tipo, contenido y modo cuando sea posible;
4. restaurar archivos no rastreados no ignorados preexistentes;
5. eliminar solo rutas nuevas atribuidas a la aplicación y ausentes al inicio;
6. restaurar los bytes del índice Git.

La limpieza de directorios nuevos es conservadora: usa `rmdir` y no borra recursivamente un
directorio que contenga elementos no atribuidos o bloqueados.

Cada paso produce un diagnóstico. Si alguno falla, el error final enumera rutas en estado
incierto y conserva por separado la causa primaria de la aplicación.

Fuentes: `repo_patcher/transaction.py::RepositoryTransaction`,
`repo_patcher/transaction.py::FileSnapshot`,
`repo_patcher/errors.py::RollbackReport` y
`repo_patcher/errors.py::ApplyRollbackError`.

### Límite sobre archivos ignorados

La transacción registra que las rutas ignoradas preexistían y no las elimina como rutas
nuevas. Sin embargo, no crea un snapshot general del contenido de todos los archivos
ignorados. Si un generador o validador modifica directamente un archivo ignorado
preexistente que no pasó por `PatchContext`, su contenido no está necesariamente restaurado.

Por ello se mantiene la recomendación:

```yaml
compatibility:
  clean_worktree: true
```

Y los generadores, validadores y plugins deben limitar sus escrituras a rutas controladas.

## 7. Idempotencia y estados

No existe una base de datos de paquetes aplicados. Un paquete se considera ya aplicado solo
cuando el plan virtual produce `changed_paths() == []`.

Consecuencias:

- operaciones ya satisfechas pueden ser no-op;
- un estado parcialmente aplicado puede completar las operaciones restantes;
- una precondición incompatible produce conflicto;
- `regex_replace` necesita aserciones o diseño adicional para ser idempotente;
- un segundo `check` con código cero no prueba por sí mismo el no-op: hay que inspeccionar el
  plan o usar `build_plan(...).context.changed_paths()`.

Fuentes: `repo_patcher/context.py::changed_paths`, `is_already_applied` y
`repo_patcher/engine.py::apply_plan`.

## 8. Errores esperados

Jerarquía pública:

```text
RepoPatcherError
├── ManifestError
├── CompatibilityError
├── PatchConflictError
├── CommandError
└── ApplyRollbackError
```

`CommandError` conserva nombre, argv, código, stdout y stderr. `ApplyRollbackError` conserva
el error primario y el informe de rollback.

Fuente: `repo_patcher/errors.py`.

## 9. Limitaciones relevantes

- No existe sandbox de plugins.
- Los campos desconocidos del manifiesto se ignoran.
- `required_files` no valida por sí mismo que la ruta carezca de `..`.
- `check` no ejecuta generadores ni validadores.
- Un plan sin cambios no ejecuta generadores ni validadores durante `apply`.
- El digest lógico de `package-info` no identifica los bytes exactos del ZIP.
- El runtime vendorizado no incluye una suite de tests dentro de
  `tooling/repo-patcher-runtime/`; las garantías deben apoyarse también en validaciones de
  integración y en el workflow.
- Los comandos externos pueden realizar acciones que no respeten el contrato; el rollback
  es defensivo, no un sandbox.

## 10. Validación CI de MUD

El workflow debe ejecutar sobre un checkout desechable del SHA exacto:

```text
package-info
explain [--trust-plugin]
check [--trust-plugin]
apply [--trust-plugin] --emit-diff ...
git diff --check
check [--trust-plugin]
prueba semántica de changed_paths() == []
```

Para paquetes con plugin, el consentimiento viaja como booleano `trust_plugin`. Si el plugin
está presente y el booleano es falso, el workflow debe abortar con un diagnóstico específico
antes de cargarlo. Si es verdadero, `--trust-plugin` debe añadirse a `explain`, `check` y
`apply`.

El artifact debe registrar al menos:

```text
plugin_present
plugin_authorized
target_sha
package_sha256
```

## 11. Lista de comprobación para generar paquetes

### Manifiesto

- [ ] `schema: 1`.
- [ ] `id` y `title` no vacíos en la raíz.
- [ ] `operations`, `plugin` o ambos.
- [ ] `repository.names` y `repository.remotes` cuando proceda.
- [ ] `compatibility.clean_worktree: true` salvo justificación explícita.
- [ ] SHA exacto o antepasado requerido deliberadamente.
- [ ] `required_files` esenciales.
- [ ] Ningún campo conceptual que el runtime ignore.

### Operaciones y plugins

- [ ] Cada operación contiene una sola clave.
- [ ] Reemplazos exactos con cardinalidad conocida.
- [ ] Precondiciones para detectar estados parciales.
- [ ] `regex_replace` diseñado explícitamente para idempotencia.
- [ ] Plugin con firma `(ctx, manifest)` y sin escrituras directas.
- [ ] Consentimiento explícito antes de validar un plugin.

### Pruebas

- [ ] `package-info`.
- [ ] `explain`.
- [ ] `check`.
- [ ] `apply --emit-diff` sobre copia limpia.
- [ ] Generadores y validadores realmente ejecutados.
- [ ] `git diff --check`.
- [ ] Revisión de `git status`, `git diff --stat` y diff completo.
- [ ] Segunda planificación con `changed_paths() == []`.
- [ ] Prueba de rollback con un fallo inyectado en una copia desechable.
- [ ] Validación remota cuando el workflow esté disponible.

## 12. Cambios principales respecto a la guía de 0.1.0

- La versión auditada es 0.2.0.
- El rollback usa `RepositoryTransaction`, no limpieza global mediante
  `git reset --hard` y `git clean -fd`.
- El rollback es diagnosticable y puede quedar parcialmente incompleto.
- Se conserva el índice Git.
- Se preservan archivos no rastreados no ignorados preexistentes.
- Se eliminan únicamente rutas nuevas atribuidas, de manera conservadora.
- `PatchContext` incorpora `original_bytes` para la transacción.
- Los comandos externos informan a la transacción de rutas nuevas.
- La guía deja de afirmar que el runtime vendorizado contiene los tests de 0.1.0.
- El consentimiento de plugins se documenta también para CI y debe cubrir `explain`, `check`
  y `apply`.
