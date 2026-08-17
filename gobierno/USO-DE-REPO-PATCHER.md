---
title: "Uso de repo-patcher"
status: obsoleto
scope: "Entrega y validación de paquetes descargables"
repo-patcher-version: "0.2.0"
package-format: 1
audited-runtime-commit: "15a9c1f61cd154a5c8dfcfc6500f70f0e9e78c66"
---

# Guía técnica autoritativa de `repo-patcher` 0.2.0

## Estado actual

RepoPatcher se conserva como experimento técnico y como mecanismo opcional para paquetes descargables o aplicación local controlada. No es el método preferente para realizar cambios remotos desde ChatGPT cuando existe acceso escribible al repositorio mediante GitHub, una rama, una pull request o un checkout.

La experiencia práctica con cambios transversales de MUD ha mostrado que el flujo RepoPatcher añade fragilidad operacional desproporcionada —anclas textuales exactas, orden de transformaciones, empaquetado, plugins y transporte— sin aportar ventajas frente al flujo Git normal cuando ChatGPT ya puede escribir y revisar el repositorio directamente.

Este documento sigue siendo la referencia técnica para entender y usar la implementación 0.2.0 mientras el experimento permanezca en el repositorio. Su estado `obsoleto` indica que no gobierna el camino preferente de cambio remoto; no significa que el runtime haya sido eliminado ni que todas sus operaciones sean defectuosas.

Para cambios remotos desde ChatGPT se prefiere el procedimiento Git/GitHub descrito por las instrucciones de trabajo del repositorio: candidata aislada sobre un SHA exacto, validaciones, revisión exhaustiva del diff, commits atómicos, comprobación de concurrencia y publicación por fast-forward.

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
    - "0123456789abcdef0123456789abcdef01234567"
  required_ancestor: "89abcdef0123456789abcdef0123456789abcdef"
  required_files:
    - AGENTS.md
```

| Campo | Alias | Tipo | Predeterminado | Semántica |
| --- | --- | --- | --- | --- |
| `clean_worktree` | — | booleano | `true` | Se exige durante `apply`; `explain` y `check` no lo exigen. |
| `exact_heads` | `exact_head` | texto o lista | vacío | `HEAD` debe coincidir literalmente con uno de los SHA. |
| `required_ancestor` | — | texto o `null` | `null` | Se usa `git merge-base --is-ancestor`. |
| `required_files` | — | texto o lista | vacío | Cada ruta debe existir bajo la ruta construida desde la repo. |

Los SHA deben escribirse entre comillas. YAML puede interpretar como número una
cadena formada solo por dígitos —por ejemplo, cuarenta ceros— y el manifiesto
la rechazará antes de comprobar compatibilidad.

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
`repo_patcher/models.py::Manifest` y
`repo_patcher/plugin.py::load_plugin`.

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
directorio que contenga elementos no atribuidos o bloqueados por el sistema.

La restauración es best effort por fase: una fase fallida no impide intentar las restantes.
El informe de rollback distingue cada paso y muestra errores individuales.

## 7. Uso recomendado mientras siga disponible

RepoPatcher debe usarse solo cuando el usuario quiera deliberadamente un paquete portable o cuando el entorno no permita modificar el repositorio de forma directa. En esos casos:

1. fija un SHA exacto de base;
2. prefiere operaciones declarativas simples;
3. evita plugins salvo que sean imprescindibles;
4. ejecuta `package-info`, `explain`, `check` y `apply` sobre un checkout limpio;
5. ejecuta los generadores y validadores del repositorio;
6. inspecciona el diff resultante;
7. conserva el paquete como artefacto reproducible, no como sustituto de la revisión Git.

No debe introducirse nueva infraestructura remota específica para RepoPatcher salvo que el experimento se reactive explícitamente.
