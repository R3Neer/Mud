---

## title: "Uso de repo-patcher"  
status: vigente  
scope: "Entrega de patches descargables"  
repo-patcher-min-version: "0.1.0"  
package-format: 1
---
# Guía técnica autoritativa de paquetes para `repo-patcher` 0.1.0

> Alcance: esta guía describe **la implementación real de `repo-patcher` 0.1.0** contenida en el wheel `repo_patcher-0.1.0-py3-none-any.whl`. No describe una API deseada ni una versión futura.
>
> Convención de citas: `archivo:Lx-Ly` se refiere a las líneas del código fuente distribuido con la versión 0.1.0.

## 1. Versión exacta analizada

La versión analizada es **`0.1.0`**:

- `pyproject.toml:L5-L13` declara el proyecto `repo-patcher`, versión `0.1.0`, Python `>=3.11` y dependencia `PyYAML>=6.0`.
- `src/repo_patcher/__init__.py:L1-L3` define `__version__ = "0.1.0"`.
- `pyproject.toml:L26-L27` registra el comando `repo-patcher = repo_patcher.cli:main`.

La API descrita aquí se verificó también por introspección directa del wheel instalado.

## 2. Modelo real de un paquete

Un paquete es:

- un **directorio** que contiene `patch.yaml` directamente; o
- un **ZIP** que contiene `patch.yaml` en su raíz, **o** exactamente dentro de un único directorio de primer nivel.

El cargador admite estas dos formas ZIP:

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
    ├── transform.py
    └── files/
```

En un directorio pasado directamente al programa, `patch.yaml` sí debe estar en la raíz de ese directorio. Para ZIP, `_manifest_root()` busca primero `patch.yaml` directo y, si no existe, exactamente un patrón `*/patch.yaml`. Cero candidatos o más de uno son error. El extractor rechaza rutas que escapen del directorio temporal. Fuentes: `src/repo_patcher/patch_source.py:L13-L33`, `src/repo_patcher/patch_source.py:L36-L54`.

No existe ningún significado especial para el nombre `files/`: es una convención. Cualquier archivo incluido dentro del paquete puede usarse como fuente si su ruta no escapa del paquete.

## 3. Esquema completo y real de `patch.yaml`

### 3.1. Nivel raíz

| Campo | Obligatorio | Tipo admitido | Valor por defecto | Uso real |
|---|---:|---|---|---|
| `schema` | No | valor igual a entero `1` | `1` | Cualquier otro valor produce error. |
| `id` | Sí | `str` no vacío tras `strip()` | — | Identificador del patch y parte del nombre interno del módulo plugin. |
| `version` | No | `str`, `int` o `float` | `"1"` | Se convierte a `str`. |
| `title` | Sí | `str` no vacío tras `strip()` | — | Título humano. |
| `description` | No | `str` | `""` | Descripción humana. |
| `repository` | No | mapa YAML | `{}` | Restricciones de nombre/remoto. |
| `compatibility` | No | mapa YAML | `{}` | Restricciones Git y de archivos. |
| `plugin` | No | mapa YAML o `null` | `null` | Plugin Python. |
| `operations` | Condicional | lista de mapas | `[]` | Debe haber `operations`, `plugin`, o ambos. |
| `generators` | No | lista de especificaciones de comando | `[]` | Se ejecutan tras escribir los cambios. |
| `validators` | No | lista de especificaciones de comando | `[]` | Se ejecutan después de los generadores. |

La validación y construcción del objeto `Manifest` están en `src/repo_patcher/manifest.py:L54-L132`. El requisito «plugin u operations» está en `manifest.py:L113-L117`.

**Campos raíz desconocidos:** la implementación no los rechaza; simplemente los ignora, porque solo consulta las claves anteriores. Esto no significa que deban usarse: un error tipográfico puede quedar silenciosamente ignorado. Fuente: `manifest.py:L62-L132`.

### 3.2. `repository`

```yaml
repository:
  names: [Mud, mud]
  remotes:
    - github.com/R3Neer/Mud
```

Campos admitidos:

| Campo | Alias | Tipo | Semántica |
|---|---|---|---|
| `names` | `name` | texto o lista de textos | El nombre de la carpeta raíz de la repo, comparado sin distinguir mayúsculas. |
| `remotes` | `remote` | texto o lista de textos | Valores admitidos para `origin`, normalizados. |

La elección se hace con `repo_raw.get("names") or repo_raw.get("name")`, y de modo equivalente para remotos. Una lista vacía en la forma plural puede hacer que se consulte el alias singular. Fuente: `src/repo_patcher/manifest.py:L81-L85`.

La comparación real está en `src/repo_patcher/gitops.py:L81-L94`. La normalización elimina `.git`, traduce `git@host:ruta` a `host/ruta`, elimina el esquema y pasa a minúsculas (`gitops.py:L66-L73`).

Válido:

```yaml
repository:
  name: Mud
  remote: https://github.com/R3Neer/Mud.git
```

También válido:

```yaml
repository:
  names: Mud
  remotes: [github.com/R3Neer/Mud]
```

Inválido:

```yaml
repository:
  names: 42
```

Produce `ManifestError`: debe ser texto o lista de textos (`manifest.py:L20-L27`).

### 3.3. `compatibility`

```yaml
compatibility:
  clean_worktree: true
  exact_heads:
    - abcdef0123456789
  required_ancestor: 0123456789abcdef
  required_files:
    - AGENTS.md
```

| Campo | Alias | Tipo | Predeterminado | Semántica |
|---|---|---|---|---|
| `clean_worktree` | — | `bool` | `true` | Solo se exige cuando el comando llama a compatibilidad con `require_clean=True`; actualmente, solo `apply`. |
| `exact_heads` | `exact_head` | texto o lista de textos | vacío | El SHA devuelto por `git rev-parse HEAD` debe coincidir literalmente con uno. |
| `required_ancestor` | — | texto o `null` | `null` | Se comprueba con `git merge-base --is-ancestor SHA HEAD`. |
| `required_files` | — | texto o lista de textos | vacío | Cada ruta debe existir bajo la repo. No se impide `..` aquí. |

Fuentes: `src/repo_patcher/manifest.py:L87-L99`; comprobación: `src/repo_patcher/gitops.py:L96-L123`.

`exact_heads` y `required_ancestor` se comprueban ambos si se declaran ambos.

Importante: `explain` y `check` llaman a `build_plan(..., require_clean=False)`, por lo que **no exigen árbol limpio**, aunque `clean_worktree: true`. `apply` sí lo exige. Fuente: `src/repo_patcher/cli.py:L172-L173` y `gitops.py:L115-L123`.

Inválido:

```yaml
compatibility:
  clean_worktree: "true"
```

Debe ser booleano YAML real (`manifest.py:L87-L90`).

### 3.4. `plugin`

```yaml
plugin:
  file: transform.py
  entrypoint: apply
```

| Campo | Obligatorio | Tipo | Predeterminado |
|---|---:|---|---|
| `file` | Sí si existe `plugin` | `str` no vacío | — |
| `entrypoint` | No | `str` no vacío | `"apply"` |

Fuentes: `src/repo_patcher/manifest.py:L101-L111`.

La ruta debe resolver dentro del paquete y existir como archivo (`src/repo_patcher/plugin.py:L14-L24`).

### 3.5. `operations`

Debe ser una lista cuyos elementos sean mapas. Cada mapa debe contener **exactamente una** operación, y su payload debe ser otro mapa. Fuentes: `manifest.py:L113-L117`, `src/repo_patcher/operations.py:L10-L16`.

Operaciones admitidas, y solo estas:

#### `create`

Con contenido inline:

```yaml
- create:
    path: docs/nuevo.md
    content: "contenido\n"
```

Desde un archivo del paquete:

```yaml
- create:
    path: docs/nuevo.md
    source: files/nuevo.md
```

Campos:

- `path`: obligatorio, texto.
- Si existe la clave `source`, se usa `source` y se ignora `content` si también existe.
- Si no existe `source`, `content` es obligatorio y debe ser texto.

Fuente: `src/repo_patcher/operations.py:L30-L35`.

Solo crea texto UTF-8 mediante `create_from_patch()` o `create_text_file()`. Si el destino ya existe con el mismo contenido, es no-op; si existe con contenido diferente, conflicto. Fuentes: `src/repo_patcher/context.py:L80-L99`.

#### `delete`

```yaml
- delete:
    path: obsoleto.txt
```

`path` es obligatorio y texto. Si no existe, es no-op. Fuente: `operations.py:L36-L37`, `context.py:L101-L106`.

#### `replace`

```yaml
- replace:
    path: README.md
    old: "antes"
    new: "después"
    count: 1
```

- `path`, `old`, `new`: textos obligatorios.
- `count`: entero; predeterminado `1`.

Fuente: `operations.py:L38-L47`.

Semántica exacta:

- Cuenta todas las apariciones de `old`.
- Si hay cero y `new` no vacío ya aparece, lo considera ya aplicado.
- Si hay cero y no se cumple lo anterior, conflicto.
- Si `count >= 0`, el número total de apariciones debe ser exactamente `count`.
- `count < 0` desactiva esa comprobación y `str.replace(..., -1)` reemplaza todas.

Fuente: `context.py:L108-L124`.

#### `regex_replace`

```yaml
- regex_replace:
    path: archivo.md
    pattern: "(?m)^Viejo$"
    replacement: "Nuevo"
    count: 1
    flags: [MULTILINE]
```

- `path`, `pattern`, `replacement`: textos obligatorios.
- `count`: no tiene validación explícita de tipo en `operations.py`; se pasa a `re.subn`. El valor predeterminado es `1`.
- `flags`: lista de textos; predeterminado `[]`. Cada texto se resuelve con `getattr(re, nombre)` y se combina con OR binario. Un nombre inexistente produce `ManifestError`.

Fuente: `operations.py:L48-L65`.

La operación exige al menos una sustitución; cero produce `PatchConflictError`. No implementa detección «ya aplicado». Fuente: `context.py:L126-L139`.

#### `append_once`

```yaml
- append_once:
    path: README.md
    marker: "## Nueva sección"
    content: |
      ## Nueva sección

      Texto.
```

Todos los campos son textos obligatorios. Si `marker` ya aparece en el archivo, no cambia nada. En otro caso produce `text.rstrip() + "\n\n" + content.strip() + "\n"`. Fuentes: `operations.py:L66-L71`, `context.py:L141-L146`.

#### `assert_contains`

```yaml
- assert_contains:
    path: AGENTS.md
    text: "Regla obligatoria"
```

Ambos campos son textos obligatorios. No modifica; falla si el fragmento no existe. Fuentes: `operations.py:L72-L73`, `context.py:L148-L150`.

#### `assert_not_contains`

```yaml
- assert_not_contains:
    path: README.md
    text: "Sintaxis retirada"
```

Ambos campos son textos obligatorios. No modifica; falla si el fragmento existe. Fuentes: `operations.py:L74-L75`, `context.py:L152-L154`.

#### Operaciones inválidas

```yaml
operations:
  - copy:
      from: a
      to: b
```

Produce «Operación declarativa desconocida» (`operations.py:L76-L77`).

```yaml
operations:
  - create:
      path: a.txt
      content: a
    delete:
      path: b.txt
```

Produce error porque un elemento debe contener exactamente una operación (`operations.py:L10-L16`).

### 3.6. `generators` y `validators`

Ambos usan el mismo esquema, una lista:

```yaml
generators:
  - name: Regenerar índice
    command: ["{python}", tooling/generate.py]
    cwd: .
    env:
      MODE: generated
```

Por elemento:

| Campo | Obligatorio | Tipo | Predeterminado |
|---|---:|---|---|
| `command` | Sí | lista no vacía de textos | — |
| `name` | No | texto | unión de `command` con espacios |
| `cwd` | No | texto | `"."` |
| `env` | No | mapa texto→texto | `{}` |

Fuente: `src/repo_patcher/manifest.py:L30-L51`.

Sustituciones literales disponibles en cada argumento, en `cwd` y en valores de `env`:

- `{python}` → `sys.executable`;
- `{repo}` → raíz de la repo;
- `{patch}` → raíz física o temporal del paquete.

Fuente: `src/repo_patcher/commands.py:L13-L18`, `commands.py:L41-L52`.

No se usa shell: cada `command` es `argv` directo para `subprocess.run`. `cwd` siempre se interpreta como `repo / cwd` y debe permanecer dentro de la repo. En preflight solo se comprueba que el directorio y el ejecutable existan; el comando no se ejecuta hasta `apply`. Fuentes: `commands.py:L22-L38`, `commands.py:L41-L69`.

## 4. Firma exacta del entrypoint de plugins

El loader espera un callable y lo invoca así:

```python
entrypoint(ctx, manifest)
```

Por tanto, la firma compatible es:

```python
def apply(ctx: PatchContext, manifest: Manifest) -> None:
    ...
```

El nombre `apply` es solo el predeterminado; puede configurarse otro mediante `plugin.entrypoint`. Fuentes: `src/repo_patcher/plugin.py:L14-L39`, `src/repo_patcher/engine.py:L48-L55`.

### Argumento 1: `ctx`

Tipo real: `repo_patcher.context.PatchContext`.

Contenido público relevante al entrar:

- `ctx.repo: pathlib.Path`: raíz absoluta resuelta de la repo.
- `ctx.patch_root: pathlib.Path`: raíz absoluta resuelta del paquete; en un ZIP apunta a un directorio temporal válido solo durante el comando.
- `ctx.changes: list[PlannedChange]`: registro acumulado de operaciones virtuales.
- `ctx.notes: list[str]`: notas que `explain`, `check` y `apply` muestran.

Se construye en `context.py:L26-L32` y se pasa en `engine.py:L46-L51`.

### Argumento 2: `manifest`

Tipo real: `repo_patcher.models.Manifest`, dataclass con:

```python
Manifest(
    source: Path,
    schema: int,
    patch_id: str,
    version: str,
    title: str,
    description: str,
    repository: RepositorySpec,
    compatibility: CompatibilitySpec,
    plugin: PluginSpec | None,
    operations: tuple[dict[str, Any], ...],
    generators: tuple[CommandSpec, ...],
    validators: tuple[CommandSpec, ...],
)
```

Fuente: `src/repo_patcher/models.py:L8-L49`.

### Valor de retorno

No se inspecciona ni se utiliza. El entrypoint **debe terminar normalmente**; por convención debe devolver `None`. Cualquier otro retorno se ignora. Una `RepoPatcherError` se propaga; cualquier otra excepción se envuelve como `RepoPatcherError("El plugin falló al preparar el patch: ...")`. Fuente: `engine.py:L48-L55`.

## 5. API pública completa de `PatchContext`

Todas las rutas de repo se reciben como `str`, aceptan `/` o `\`, se normalizan a POSIX y no pueden ser absolutas ni contener `..`. Salir de la repo produce `PatchConflictError`. Fuente: `context.py:L34-L44`.

### Constructor

```python
PatchContext(repo: Path, patch_root: Path)
```

Normalmente no lo crea el plugin; lo crea el motor. Fuente: `context.py:L26-L32`.

### `exists`

```python
def exists(self, relative: str) -> bool
```

Devuelve si el archivo virtual existe. Carga su estado original la primera vez. Puede lanzar `PatchConflictError` por ruta insegura; errores de I/O no se envuelven. Fuente: `context.py:L46-L56`.

```python
if ctx.exists("config.yaml"):
    ...
```

### `read_bytes`

```python
def read_bytes(self, relative: str) -> bytes
```

Lee el contenido virtual actual. Si no existe, `PatchConflictError`. Fuente: `context.py:L58-L62`.

```python
raw = ctx.read_bytes("logo.bin")
```

### `read_text`

```python
def read_text(self, relative: str, encoding: str = "utf-8") -> str
```

Decodifica `read_bytes`. Archivo ausente o ruta insegura: `PatchConflictError`; error de decodificación: `PatchConflictError`. Fuente: `context.py:L64-L68`.

```python
text = ctx.read_text("README.md")
```

### `write_bytes`

```python
def write_bytes(
    self,
    relative: str,
    content: bytes,
    *,
    action: str = "modificar",
    detail: str = "",
) -> None
```

Sustituye virtualmente el contenido binario. Si es idéntico, no registra cambio. `action` y `detail` solo alimentan el informe. Ruta insegura: `PatchConflictError`. Fuente: `context.py:L70-L75`.

```python
ctx.write_bytes("data.bin", b"\x00\x01", action="modificar", detail="cabecera")
```

### `write_text`

```python
def write_text(self, relative: str, content: str, encoding: str = "utf-8") -> None
```

Reemplazo completo virtual; registra acción `modificar`, detalle `reemplazo completo`. Fuente: `context.py:L77-L78`.

```python
ctx.write_text("README.md", "# Nuevo\n")
```

### `create_text_file`

```python
def create_text_file(
    self,
    relative: str,
    content: str,
    *,
    encoding: str = "utf-8",
) -> None
```

Crea virtualmente. Si ya existe idéntico, no-op; si existe diferente, `PatchConflictError`. Fuente: `context.py:L80-L89`.

```python
ctx.create_text_file("docs/nuevo.md", "# Nuevo\n")
```

### `create_from_patch`

```python
def create_from_patch(
    self,
    relative: str,
    source: str,
    *,
    encoding: str = "utf-8",
) -> None
```

Lee un archivo de texto incluido en el paquete y lo crea en la repo mediante `create_text_file`. `source` es relativo a `ctx.patch_root`, debe permanecer dentro del paquete y existir. Errores: `PatchConflictError` por escape, ausencia o conflicto del destino; errores de lectura/decodificación no se envuelven expresamente. Fuente: `context.py:L91-L99`.

```python
ctx.create_from_patch(
    "docs/GUIA.md",
    "files/GUIA.md",
)
```

Este es el mecanismo exacto pedido para tomar contenido de `files/`.

### `delete_file`

```python
def delete_file(self, relative: str) -> None
```

Marca el archivo virtual para eliminación. Ausente: no-op. Fuente: `context.py:L101-L106`.

```python
ctx.delete_file("docs/obsoleto.md")
```

### `replace_exact`

```python
def replace_exact(
    self,
    relative: str,
    old: str,
    new: str,
    *,
    count: int = 1,
) -> None
```

Semántica descrita en §3.5. Errores: archivo/ruta/UTF-8 y `PatchConflictError` por ausencia o cardinalidad inesperada. Fuente: `context.py:L108-L124`.

```python
ctx.replace_exact("README.md", "Estado: antiguo", "Estado: nuevo")
```

### `replace_regex`

```python
def replace_regex(
    self,
    relative: str,
    pattern: str,
    replacement: str,
    *,
    count: int = 1,
    flags: int = 0,
) -> None
```

Ejecuta `re.subn`. Cero sustituciones: `PatchConflictError`. Expresión inválida: `re.error` sin envolver. Fuente: `context.py:L126-L139`.

```python
import re
ctx.replace_regex("README.md", r"^Estado: .+$", "Estado: nuevo", flags=re.MULTILINE)
```

### `append_once`

```python
def append_once(self, relative: str, marker: str, content: str) -> None
```

No-op si `marker` aparece en cualquier posición. En otro caso añade dos saltos y contenido recortado. Fuente: `context.py:L141-L146`.

```python
ctx.append_once("README.md", "## Instalación", "## Instalación\n\nTexto.")
```

### `assert_contains`

```python
def assert_contains(self, relative: str, fragment: str) -> None
```

Falla con `PatchConflictError` si falta el fragmento. Fuente: `context.py:L148-L150`.

```python
ctx.assert_contains("AGENTS.md", "## Reglas")
```

### `assert_not_contains`

```python
def assert_not_contains(self, relative: str, fragment: str) -> None
```

Falla con `PatchConflictError` si aparece. Fuente: `context.py:L152-L154`.

```python
ctx.assert_not_contains("README.md", "texto retirado")
```

### `load_yaml`

```python
def load_yaml(self, relative: str) -> Any
```

Ejecuta `yaml.safe_load` sobre el texto virtual. YAML inválido: `PatchConflictError`; puede devolver cualquier tipo YAML, incluido `None`. Fuente: `context.py:L156-L160`.

```python
data = ctx.load_yaml("config.yaml")
```

### `save_yaml`

```python
def save_yaml(
    self,
    relative: str,
    value: Any,
    *,
    sort_keys: bool = False,
) -> None
```

Serializa con `yaml.safe_dump(..., allow_unicode=True, width=120)` y reemplaza el archivo virtual. Errores de serialización de PyYAML no se envuelven. Fuente: `context.py:L162-L164`.

```python
data = ctx.load_yaml("config.yaml")
data["enabled"] = True
ctx.save_yaml("config.yaml", data)
```

### `note`

```python
def note(self, text: str) -> None
```

Añade una nota al informe de plan. No comprueba el tipo en runtime. Fuente: `context.py:L166-L167`, presentación en `src/repo_patcher/cli.py:L125-L128`.

```python
ctx.note("Se regenerará el índice durante apply.")
```

### `changed_paths`

```python
def changed_paths(self) -> list[str]
```

Devuelve rutas ordenadas cuyo valor virtual difiere del original. Fuente: `context.py:L169-L170`.

```python
paths = ctx.changed_paths()
```

### `is_already_applied`

```python
def is_already_applied(self) -> bool
```

Es exactamente `not self.changed_paths()`. No consulta un registro de IDs o versiones. Fuente: `context.py:L172-L173`.

```python
if ctx.is_already_applied():
    ctx.note("No hay cambios virtuales.")
```

### `commit_to_disk`

```python
def commit_to_disk(self) -> None
```

Escribe/elimina todos los archivos virtualmente cambiados. Es API pública por nombre, pero un plugin **no debe llamarla**: el motor la llama en `apply_plan`. Fuente: `context.py:L175-L184`, `engine.py:L75-L77`.

### `restore_original`

```python
def restore_original(self) -> None
```

Restaura los archivos que el contexto llegó a cargar, incluidos archivos ignorados. También es infraestructura del motor, no una operación normal de plugin. Fuente: `context.py:L186-L195`, `engine.py:L91-L94`.

## 6. Qué hace el plugin en cada comando

### `package-info`

- Abre/descomprime el paquete.
- Carga `patch.yaml`.
- No busca repo.
- **No solicita confianza, no carga ni ejecuta el plugin.**
- Calcula un SHA-256 lógico del árbol del paquete.

Fuentes: `src/repo_patcher/cli.py:L155-L162`; digest: `engine.py:L33-L40`.

### `explain`

- Localiza la repo.
- Carga primero el manifiesto.
- Si hay plugin, exige confirmación o `--trust-plugin`.
- Construye el plan: comprueba compatibilidad, ejecuta operaciones declarativas **en memoria**, carga y ejecuta el plugin **en memoria**, y hace preflight de comandos.
- No escribe archivos ni ejecuta generadores/validadores.

Fuentes: `cli.py:L164-L181`, `engine.py:L43-L58`.

### `check`

Hace exactamente el mismo `build_plan` que `explain`, incluido ejecutar el plugin virtualmente. No escribe ni ejecuta generadores/validadores. No exige árbol limpio. Fuentes: `cli.py:L164-L186`.

### `apply`

Hace el mismo plan, pero exige árbol limpio si el manifiesto lo solicita. Si hay cambios virtuales:

1. escribe el plan;
2. ejecuta generadores;
3. comprueba que HEAD no cambió;
4. ejecuta validadores;
5. ejecuta siempre `git diff --check` adicional;
6. vuelve a comprobar HEAD;
7. opcionalmente emite diff.

Fuentes: `cli.py:L172-L205`, `engine.py:L61-L98`.

Si no hay cambios virtuales, devuelve inmediatamente y **no ejecuta generadores ni validadores** (`engine.py:L68-L71`).

## 7. Registro y ejecución de operaciones, generadores, validadores y rollback

### Operaciones

Las operaciones declarativas se ejecutan primero sobre `PatchContext`; luego el plugin, si existe, ve ya esos cambios virtuales. Fuente: `engine.py:L43-L51`.

Cada cambio que altera bytes añade `PlannedChange(path, action, detail)` a `ctx.changes`. Puede haber varias entradas para una ruta; el informe agrupa acciones por ruta. Fuentes: `context.py:L13-L17`, `context.py:L70-L75`, `cli.py:L111-L124`.

### Generadores y validadores

Se almacenan como tuplas de `CommandSpec`. `build_plan` solo hace preflight. `apply_plan` ejecuta todos los generadores en orden y luego todos los validadores en orden. Un código de salida distinto de cero lanza `CommandError` con stdout/stderr. Fuentes: `models.py:L8-L13`, `commands.py:L22-L69`, `engine.py:L75-L85`.

### Rollback

Cualquier excepción tras comenzar `apply_plan` provoca:

```python
plan.context.restore_original()
rollback_clean_repo(repo, initial_head)
```

Después, `rollback_clean_repo` ejecuta siempre:

```text
git reset --hard <HEAD-inicial>
git clean -fd
```

Fuentes: `engine.py:L91-L94`, `src/repo_patcher/gitops.py:L126-L132`.

**Advertencia autoritativa:** `git clean -fd` elimina archivos y directorios no rastreados de toda la repo, no solo los creados por el patch. Normalmente `apply` exige un árbol limpio, pero un manifiesto puede poner `clean_worktree: false`; en ese caso, un fallo podría borrar elementos no rastreados preexistentes. No use `clean_worktree: false` salvo que acepte esta consecuencia.

## 8. Detección de estados

### Aplicación previa

No hay base de datos, marca, ID aplicado ni comparación de versión. Se considera «ya aplicado» únicamente cuando todas las operaciones y el plugin producen un contexto sin diferencias: `ctx.changed_paths()` vacío. Fuentes: `context.py:L169-L173`, `engine.py:L68-L71`, `cli.py:L188-L192`.

### Aplicación parcial

No existe un estado específico «parcialmente aplicado» ni una detección global. Casos posibles:

- Si algunas operaciones son no-op por estar ya aplicadas y otras aún generan cambios, el plan se considera aplicable y aplicará las restantes.
- Si una operación encuentra un estado incompatible, lanza conflicto durante el plan y no escribe nada.
- Si todo queda sin cambios, se considera ya aplicado.

La distinción depende de las precondiciones, `assert_*`, reemplazos exactos y lógica del plugin; no existe una clasificación explícita.

### Incompatibilidad

Se detecta por:

- nombre de carpeta de repo;
- `origin` normalizado;
- HEAD exacto;
- antepasado Git;
- archivos requeridos;
- árbol sucio en `apply` si corresponde.

Fuente: `gitops.py:L81-L123`.

### Divergencia del repositorio

No existe análisis semántico general. Se manifiesta como:

- incompatibilidad Git/archivos;
- `PatchConflictError` porque un fragmento exacto, regex o aserción no coincide;
- excepción del plugin;
- fallo de generador o validador.

## 9. Paquete mínimo completo y probado

El ZIP adjunto `repo-patcher-authoritative-example.zip` fue probado contra `repo-patcher 0.1.0` ejecutando `package-info`, `explain`, `check` y `apply`.

Estructura:

```text
repo-patcher-authoritative-example.zip
├── patch.yaml
└── files/
    └── CREADO-DESDE-EL-PATCH.md
```

`patch.yaml`:

```yaml
schema: 1
id: authoritative-minimal-example
version: 1
title: Ejemplo mínimo autoritativo
description: Reemplaza un fragmento, crea un archivo desde files/, ejecuta un generador y un validador.
repository:
  names: [demo-repo]
compatibility:
  clean_worktree: true
  required_files:
    - README.md
    - tools/generate.py
    - tools/validate.py
operations:
  - replace:
      path: README.md
      old: "Estado: antiguo"
      new: "Estado: nuevo"
      count: 1
  - create:
      path: docs/CREADO-DESDE-EL-PATCH.md
      source: files/CREADO-DESDE-EL-PATCH.md
generators:
  - name: Generar marca
    command: ["{python}", tools/generate.py]
validators:
  - name: Validar resultado
    command: ["{python}", tools/validate.py]
```

El repositorio de prueba contenía:

```python
# tools/generate.py
from pathlib import Path
Path("GENERATED.txt").write_text("generado\n", encoding="utf-8")
```

```python
# tools/validate.py
from pathlib import Path
assert "Estado: nuevo" in Path("README.md").read_text(encoding="utf-8")
assert Path("docs/CREADO-DESDE-EL-PATCH.md").read_text(encoding="utf-8").startswith("# Creado")
assert Path("GENERATED.txt").read_text(encoding="utf-8") == "generado\n"
```

Resultado verificado:

- `README.md` modificado;
- archivo de `files/` creado;
- `GENERATED.txt` creado por el generador;
- validador superado;
- `git diff --check` superado;
- diff emitido.

## 10. Tests existentes que demuestran las interfaces

La distribución contiene únicamente tres tests de integración:

1. `test_declarative_apply_and_idempotent_plan`: prueba `append_once`, un validador, aplicación y detección posterior de contexto sin cambios. `tests/test_integration.py:L27-L66`.
2. `test_validator_failure_rolls_back_everything`: prueba creación, modificación, fallo de validador y rollback a repo limpia sin archivo nuevo. `tests/test_integration.py:L68-L102`.
3. `test_plugin_uses_virtual_context`: prueba plugin `apply(ctx, manifest)`, `load_yaml`, acceso `manifest.patch_id`, `save_yaml`, ausencia de escritura durante plan y aplicación posterior. `tests/test_integration.py:L104-L140`.

Los tres tests se ejecutaron sobre el código 0.1.0 y pasaron.

No existen tests distribuidos específicos para:

- ZIP y raíz alternativa;
- todas las operaciones declarativas;
- seguridad de rutas;
- remotos y compatibilidad;
- comandos `package-info`, `explain`, `check` y CLI;
- retorno del plugin;
- rollback con `clean_worktree: false`;
- campos desconocidos del manifiesto.

## 11. Diferencias entre la API real y `USO-DE-REPO-PATCHER.md`

La documentación anterior propuesta en esa conversación no era autoritativa y contiene diferencias importantes:

1. **`format_version` no existe.** El campo real es `schema` en la raíz. Un manifiesto con solo `format_version` usará `schema=1` por defecto, pero `format_version` será ignorado. Fuente: `manifest.py:L64-L66`.
2. **No existe un mapa raíz `patch:`.** `id`, `version`, `title` y `description` están directamente en la raíz. Un ejemplo con `patch.id` falla por faltar `id` raíz. Fuente: `manifest.py:L68-L79`.
3. **No existe `requires.repo_patcher`.** No se comprueba versión mínima del motor; cualquier campo `requires` es ignorado.
4. **No existen `repository.expected_name` ni `expected_remote`.** Los campos reales son `name`/`names` y `remote`/`remotes`. Los otros se ignoran y no protegen contra repo equivocada. Fuente: `manifest.py:L81-L85`.
5. **No existe `compatibility.require_clean_worktree`.** El campo real es `clean_worktree`. Fuente: `manifest.py:L87-L90`.
6. **No existe `requirements.files`.** Los archivos requeridos están en `compatibility.required_files`. Fuente: `manifest.py:L94-L99`.
7. **`operations.yaml` y `checks.yaml` no se cargan.** Todas las operaciones, generadores y validadores se leen de `patch.yaml`.
8. **`files/` no es una ubicación reservada ni automática.** Se usa mediante `source: files/x` o `ctx.create_from_patch(...)`.
9. **`create_text_file(..., source=...)` es inválido.** La firma real recibe contenido; para archivo incluido se usa `create_from_patch(relative, source)`. Fuente: `context.py:L80-L99`.
10. **No existen comandos CLI `status`, `diff` ni `undo`.** Los comandos reales son `tutorial`, `doctor`, `package-info`, `explain`, `check` y `apply`. Fuente: `cli.py:L48-L74`.
11. **`check` no ejecuta validadores.** Solo comprueba que sus ejecutables/cwd existan; los validadores se ejecutan durante `apply`. Fuente: `cli.py:L182-L186`, `commands.py:L22-L38`.
12. **`explain` y `check` sí ejecutan el plugin.** Lo hacen virtualmente y requieren confianza. Fuente: `cli.py:L164-L177`, `engine.py:L43-L55`.
13. **No hay sandbox de plugin.** Aunque se recomienda usar `PatchContext`, el plugin es Python arbitrario ejecutado en el proceso. Fuente: `plugin.py:L25-L34`.
14. **No hay detección explícita de aplicación parcial ni registro por ID/versión.** Solo se inspeccionan diferencias virtuales.
15. **El rollback no se limita a archivos registrados.** Además de `restore_original`, hace `git reset --hard` y `git clean -fd`. Fuente: `engine.py:L91-L94`, `gitops.py:L126-L132`.

## 12. Lista de comprobación para agentes que generen paquetes

### Antes de escribir el paquete

- [ ] Confirmar que el usuario usa `repo-patcher 0.1.0`.
- [ ] Leer el código o esta guía; no usar campos conceptuales de versiones futuras.
- [ ] Identificar nombre real de la carpeta repo y `origin` si se van a restringir.
- [ ] Elegir `exact_heads` o `required_ancestor` conscientemente.
- [ ] Mantener `compatibility.clean_worktree: true`.
- [ ] Enumerar en `required_files` los archivos esenciales.

### `patch.yaml`

- [ ] Usar `schema: 1`.
- [ ] Poner `id` y `title` no vacíos en la raíz.
- [ ] Poner `version` en la raíz.
- [ ] Declarar `operations`, `plugin` o ambos.
- [ ] No usar `format_version`, `patch:`, `requires:`, `requirements:` ni `expected_name`.
- [ ] Escribir comandos como listas de strings, no como comandos de shell.
- [ ] Usar `{python}`, `{repo}` y `{patch}` solo donde corresponda.

### Operaciones

- [ ] Cada elemento de `operations` contiene exactamente una clave.
- [ ] Para crear desde el ZIP, usar `create.source` o `ctx.create_from_patch`.
- [ ] Hacer reemplazos exactos con fragmentos suficientemente distintivos.
- [ ] Añadir `assert_contains`/`assert_not_contains` para detectar estados parciales cuando sea útil.
- [ ] No confiar en `regex_replace` como idempotente: añadir una aserción o lógica de plugin.

### Plugins

- [ ] Declarar `plugin.file` y opcionalmente `entrypoint`.
- [ ] Usar firma `def apply(ctx, manifest):`.
- [ ] Devolver `None` por convención.
- [ ] Usar `PatchContext`; no escribir directamente en disco ni lanzar subprocess desde el plugin.
- [ ] Recordar que `explain` y `check` ejecutarán el plugin.
- [ ] No conservar `ctx.patch_root` para usarlo después del comando: en ZIP es temporal.

### Pruebas mínimas

- [ ] `repo-patcher package-info patch.zip`.
- [ ] `repo-patcher explain patch.zip --repo RUTA`.
- [ ] `repo-patcher check patch.zip --repo RUTA`.
- [ ] `repo-patcher apply patch.zip --repo COPIA_LIMPIA --emit-diff resultado.patch`.
- [ ] Revisar `git status`, `git diff --stat`, `git diff`.
- [ ] Confirmar que generadores y validadores realmente se ejecutaron.
- [ ] Aplicar, confirmar el resultado en Git y ejecutar `check` de nuevo para comprobar no-op/idempotencia.
- [ ] Inyectar un validador fallido en una copia y comprobar rollback.
- [ ] No probar fallos en una repo con archivos no rastreados valiosos: el rollback ejecuta `git clean -fd`.

### Entrega

- [ ] ZIP con `patch.yaml` en raíz o en un único directorio de primer nivel.
- [ ] Incluir todos los archivos referenciados por `source` y `plugin.file`.
- [ ] Indicar si contiene plugin y exigir `--trust-plugin` en uso no interactivo.
- [ ] No afirmar que existe una interfaz que el código 0.1.0 no implementa.
