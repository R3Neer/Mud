---

## title: "Uso de repo-patcher"  
status: vigente  
scope: "Entrega de patches descargables"  
repo-patcher-min-version: "0.1.0"  
package-format: 1
---

# Uso de `repo-patcher`

## Propósito

`repo-patcher` es la herramienta utilizada para entregar cambios descargables que otra persona aplicará sobre una copia local de este repositorio.

Su función es separar:

- el motor estable que aplica cambios de forma transaccional;
    
- el paquete concreto que describe una modificación del repositorio.
    

El motor `repo-patcher` no contiene decisiones específicas de MUD. Cada cambio se entrega como un paquete independiente con su manifiesto, operaciones, archivos y, cuando sea necesario, un plugin Python.

## Cuándo se aplica este documento

Este documento se aplica únicamente en alguno de estos casos:

1. El usuario solicita expresamente un patch descargable.
2. El entorno permite leer el repositorio, pero no modificarlo directamente.
3. El agente no puede crear una rama, realizar commits o abrir una pull request y debe entregar los cambios para que el usuario los aplique localmente.
4. El resultado solicitado es un paquete reproducible y revisable que pueda aplicarse posteriormente.

Este documento no se aplica cuando el agente puede trabajar directamente sobre el repositorio mediante:

- Codex;
- un checkout local con permisos de escritura;
- el conector de GitHub con capacidad de modificación;
- una rama de trabajo;
- commits;
- una pull request;
- cualquier otro flujo directo autorizado por el usuario.

Cuando sea posible modificar directamente el repositorio, debe emplearse el flujo normal indicado por `AGENTS.md` y por las políticas de gobierno correspondientes.

## Principio general

Cuando este documento sea aplicable, la entrega normal debe ser un paquete compatible con `repo-patcher`.

No debe entregarse un script Python monolítico que reproduzca por sí mismo toda la infraestructura de comprobación, escritura, validación y rollback, salvo que exista una limitación técnica concreta y documentada que impida utilizar `repo-patcher`.

El motor general no debe copiarse ni modificarse dentro de cada paquete. Los cambios específicos pertenecen al paquete del patch.

## Lecturas obligatorias antes de preparar un patch

Antes de diseñar el paquete, el agente debe:

1. Leer el `AGENTS.md` aplicable a la raíz y a cada subdirectorio afectado.
2. Leer las políticas y documentos enlazados desde `AGENTS.md`.
3. Inspeccionar el estado actual del repositorio.
4. Identificar la rama y revisión exactas utilizadas como base.
5. Revisar los generadores y validadores disponibles.
6. Localizar los archivos derivados que no deben editarse manualmente.
7. Determinar qué decisiones anteriores quedan modificadas, ampliadas o sustituidas.
8. Comprobar que el cambio solicitado está suficientemente definido.

No debe asumirse que el repositorio conserva el estado observado en una conversación anterior.

## Flujo de trabajo del agente

### 1. Inspección

El agente debe identificar:

- la raíz del repositorio;
- el remoto esperado;
- el commit base;
- los archivos afectados;
- los archivos generados;
- los validadores obligatorios;
- las dependencias necesarias;
- las posibles divergencias con el estado actual.

### 2. Diseño del cambio

El agente debe separar:

- cambios normativos;
- cambios editoriales;
- cambios mecánicos;
- artefactos generados;
- pruebas y casos de cobertura;
- operaciones de regeneración;
- validaciones posteriores.

Cuando el repositorio mantenga trazabilidad mediante ADR, índices, manifiestos o referencias recíprocas, el patch debe conservarla.

### 3. Construcción del paquete

El paquete debe contener como mínimo:

```text
patch-id/
├── patch.yaml
├── README.md
└── files/
```

Puede contener además:

```text
patch-id/
├── transform.py
├── operations.yaml
├── checks.yaml
└── files/
```

La estructura exacta depende de las necesidades del cambio, pero `patch.yaml` es obligatorio.

### 4. Comprobación previa

Antes de entregar el paquete deben ejecutarse, cuando el entorno lo permita:

```powershell
repo-patcher explain ".\patch.zip"
repo-patcher check ".\patch.zip" --repo "D:\Ruta\Al\Repositorio"
```

`check` no debe modificar archivos.

### 5. Aplicación de prueba

El paquete debe probarse sobre una copia limpia y compatible del repositorio:

```powershell
repo-patcher apply ".\patch.zip" `
    --repo "D:\Ruta\Al\Repositorio" `
    --emit-diff ".\resultado.patch"
```

### 6. Verificación

Deben comprobarse:

- el estado final del repositorio;
- los validadores propios del proyecto;
- `git diff --check`;
- el diff completo;
- los archivos nuevos;
- los archivos eliminados;
- los artefactos regenerados;
- la detección de una aplicación previa;
- la idempotencia cuando proceda;
- el rollback ante un fallo inyectado.

### 7. Entrega

La entrega debe indicar:

- el identificador y versión del patch;
- la revisión o condiciones de compatibilidad;
- el alcance;
- los archivos afectados;
- los validadores ejecutados;
- las limitaciones conocidas;
- los comandos PowerShell exactos para aplicarlo;
- cómo revisar el resultado;
- qué hacer si el preflight falla.

No debe afirmarse que una validación se ha ejecutado si el entorno no permitió realizarla.

## Manifiesto `patch.yaml`

El manifiesto identifica el patch y declara sus condiciones de aplicación.

Ejemplo orientativo:

```yaml
format_version: 1

patch:
  id: mud-d085
  version: 2
  title: Diccionarios decisionales y metadatos
  description: >
    Actualiza la especificación, gramática y modelos sintácticos para
    incorporar las decisiones de D-085.

repository:
  expected_name: Mud
  expected_remote: github.com/R3Neer/Mud

compatibility:
  required_ancestor: 82e79f5af90f4d19037d234d7fc96ed4ecd4bdd7
  require_clean_worktree: true

requirements:
  files:
    - AGENTS.md
    - especificacion/gramatica/mud.ebnf
    - tooling/decisions/manage_decisions.py

plugin:
  file: transform.py
  entrypoint: apply

generators:
  - command:
      - python
      - tooling/decisions/manage_decisions.py
      - generate

validators:
  - command:
      - python
      - tooling/decisions/manage_decisions.py
      - validate

  - command:
      - python
      - especificacion/gramatica/validate_grammar.py

  - command:
      - python
      - especificacion/sintaxis/validate_syntax_model.py

  - command:
      - git
      - diff
      - --check
```

El manifiesto real debe ajustarse al esquema admitido por la versión instalada de `repo-patcher`. Este ejemplo expresa el contrato conceptual y no autoriza a inventar campos no soportados.

## Compatibilidad

La compatibilidad no debe reducirse innecesariamente a un único `HEAD` exacto cuando el patch pueda comprobarse de forma más flexible.

Puede declararse mediante:

- commit base exacto;
- ancestro obligatorio;
- uno de varios commits compatibles;
- remoto esperado;
- archivos requeridos;
- hashes o fragmentos concretos;
- ausencia o presencia de determinadas construcciones;
- versión mínima de una herramienta;
- estado limpio del árbol de trabajo.

La estrategia debe ser conservadora.

Si el repositorio ha avanzado, pero todos los fragmentos y condiciones relevantes siguen siendo compatibles, el paquete puede permitir la aplicación sobre descendientes del commit base.

Si existe una divergencia significativa, debe adaptarse el patch al nuevo estado. No debe recomendarse `--force` como solución ordinaria.

## Operaciones declarativas

Las operaciones sencillas deberían declararse sin plugin cuando el formato lo permita.

Ejemplos conceptuales:

- crear un archivo
- sustituir un fragmento exacto;
- insertar una sección;
- eliminar un archivo;
- copiar un archivo incluido en el paquete;
- actualizar un valor YAML o JSON;
- ejecutar un generador;
- ejecutar un validador.

Los reemplazos exactos deben:

- exigir una coincidencia inequívoca;
- abortar si el contexto esperado no existe;
- detectar cuando el resultado ya está aplicado;
- no realizar sustituciones parciales silenciosas.

Las expresiones regulares deben emplearse solo cuando un reemplazo exacto o estructural no sea suficiente.

## Plugins Python

Un paquete puede incluir un plugin Python cuando el cambio requiera lógica que no pueda expresarse de manera razonable mediante operaciones declarativas.

Es apropiado para:

- transformaciones complejas de YAML;
- actualización coordinada de varios modelos;
- regeneración estructurada;
- análisis de gramáticas;
- migraciones dependientes del contenido;
- cambios que exijan calcular información derivada.

El plugin debe contener únicamente la lógica específica del patch.

No debe reimplementar:

- detección de la raíz Git;
- comprobación del árbol de trabajo;
- backups;
- rollback;
- ejecución general de validadores;
- generación del diff;
- interfaz de línea de comandos;
- informes finales.

El plugin debe utilizar la API transaccional proporcionada por `repo-patcher`. No debe escribir fuera del repositorio ni ejecutar procesos arbitrarios salvo que el manifiesto y el motor lo permitan expresamente.

Ejemplo conceptual:

```python
def apply(ctx):
    ctx.replace_exact(
        "especificacion/gramatica/mud.ebnf",
        old="fragmento anterior",
        new="fragmento nuevo",
    )

    ctx.create_text_file(
        "notas/decisiones/ADR-085.md",
        source="files/ADR-085.md",
    )
```

Un plugin Python es código ejecutable. El paquete debe indicar claramente su existencia y `repo-patcher` debe exigir autorización antes de cargarlo.

## Seguridad

El motor debe impedir, salvo autorización expresa:

- escribir fuera de la raíz del repositorio;
- seguir rutas que escapen mediante `..`;
- modificar el propio motor;
- ejecutar plugins antes de su autorización;
- realizar commits;
- hacer `push`;
- cambiar remotos;
- borrar ramas;
- ejecutar comandos destructivos;
- continuar después de una precondición fallida.

Los plugins de procedencia desconocida no deben autorizarse.

Antes de aplicar un paquete con plugin, el usuario debe poder inspeccionar:

```powershell
repo-patcher package-info ".\patch.zip"
repo-patcher explain ".\patch.zip"
```

## Transacciones y rollback

La aplicación debe ser transaccional.

Antes de escribir, `repo-patcher` debe registrar el estado original de cada archivo que pueda verse afectado.

Si falla cualquier operación, generador o validador, debe restaurar:

- archivos modificados;
- archivos eliminados;
- archivos nuevos;
- archivos generados;
- índices regenerados;
- cualquier otro artefacto incluido en la transacción.

El informe de error debe indicar si el rollback terminó correctamente.

Un error no debe dejar el repositorio parcialmente migrado.

## Árbol de trabajo

Por defecto, el repositorio debe estar limpio antes de aplicar un patch:

```powershell
git status
```

Los cambios locales deben confirmarse, guardarse mediante `git stash` o descartarse antes de continuar.

Un commit local adicional no implica necesariamente incompatibilidad, pero debe evaluarse mediante las condiciones declaradas por el paquete. No debe forzarse una aplicación simplemente porque la divergencia parezca pequeña.

## Generadores

Los archivos derivados deben actualizarse mediante sus generadores oficiales.

Ejemplo:

```powershell
python tooling/decisions/manage_decisions.py generate
```

El patch debe distinguir entre:

- archivos fuente editados directamente;
- artefactos generados;
- índices regenerados;
- salidas temporales.

Cuando un generador modifique archivos adicionales, estos deben quedar incluidos en la transacción y en el informe final.

## Validadores

Cada paquete debe ejecutar los validadores relevantes del repositorio.

Para MUD pueden incluir, según el alcance:

```powershell
python tooling/decisions/manage_decisions.py validate
python especificacion/gramatica/validate_grammar.py
python especificacion/sintaxis/validate_syntax_model.py
git diff --check
```

Esta lista no es universal. El agente debe inspeccionar el repositorio y utilizar los comandos vigentes en el momento de preparar el patch.

Pasar los validadores existentes no demuestra automáticamente que toda decisión conceptual sea correcta. El agente también debe revisar la coherencia normativa y semántica que los validadores todavía no cubran.

## Idempotencia y estado de aplicación

Siempre que sea razonable, el paquete debe distinguir entre:

- aplicable;
- ya aplicado;
- parcialmente aplicado;
- incompatible;
- compatible con advertencias.

Una segunda ejecución no debe duplicar:

- secciones;
- referencias;
- entradas YAML;
- archivos;
- decisiones;
- índices;
- casos de prueba.

Cuando la operación no pueda ser idempotente, debe documentarse expresamente.

## Comandos para el usuario

### Ejecutar desde la raíz del repositorio

```powershell
Set-Location "D:\Ruta\Al\Repositorio"

repo-patcher explain "C:\Ruta\Al\patch.zip"
repo-patcher check "C:\Ruta\Al\patch.zip"
repo-patcher apply "C:\Ruta\Al\patch.zip"
```

### Indicar explícitamente la ruta

```powershell
repo-patcher check "C:\Ruta\Al\patch.zip" `
    --repo "D:\Ruta\Al\Repositorio"
```

### Generar un diff convencional

```powershell
repo-patcher apply "C:\Ruta\Al\patch.zip" `
    --repo "D:\Ruta\Al\Repositorio" `
    --emit-diff "C:\Ruta\Al\resultado.patch"
```

### Revisar el resultado

```powershell
Set-Location "D:\Ruta\Al\Repositorio"

git status
git diff --stat
git diff
```

`repo-patcher` no debe crear el commit. Después de revisar:

```powershell
git add .
git commit -m "descripción del cambio"
```

## Diagnósticos

Los errores deben explicar:

1. Qué condición falló.
2. Qué archivo o comando está implicado.
3. Si se escribió algún archivo.
4. Si el rollback se completó.
5. Qué comando puede ejecutar el usuario para inspeccionar el estado.
6. Cuál es la solución recomendada.
7. Qué acciones no debe realizar.

Ejemplo:

```text
No puede aplicarse el patch porque el archivo
especificacion/gramatica/mud.ebnf no contiene el fragmento esperado.

No se ha conservado ningún cambio parcial.
El rollback terminó correctamente.

Comprueba:

    git status
    git log -1 --oneline

No uses --force sin revisar primero la divergencia.
```

## Uso de `--force`

`--force` es una opción excepcional.

No debe recomendarse para:

- ignorar un commit base diferente;
- saltarse un árbol de trabajo sucio;
- resolver un fragmento que ya no coincide;
- evitar un validador fallido;
- aplicar un paquete preparado para otra revisión.

Solo puede utilizarse cuando una persona haya revisado expresamente la divergencia y comprenda qué comprobación está anulando.

Un agente debe preferir preparar una nueva versión compatible del paquete.

## Versionado de paquetes

Cada patch debe poseer:

- identificador estable;
- versión;
- versión del formato;
- versión mínima de `repo-patcher`;
- descripción de cambios respecto de versiones anteriores.

Ejemplo:

```yaml
format_version: 1

patch:
  id: mud-d085
  version: 2

requires:
  repo_patcher: ">=0.1.0"
```

Corregir un paquete fallido debe incrementar su versión. No debe reutilizarse silenciosamente el mismo archivo con contenido distinto.

Nombres recomendados:

```text
mud-d085-v1.zip
mud-d085-v2.zip
```

## Contenido del `README.md` del paquete

Cada paquete debe explicar:

- qué modifica;
- para qué revisión se preparó;
- qué condiciones de compatibilidad utiliza;
- si contiene un plugin;
- qué validadores ejecuta;
- cómo realizar `explain`, `check` y `apply`;
- cómo revisar el resultado;
- qué limitaciones tiene;
- qué versión sustituye, cuando proceda.

## Informe final del agente

La respuesta que acompaña al paquete debe indicar con precisión:

- qué se entrega;
- qué se ha probado;
- qué no se ha podido probar;
- la versión de `repo-patcher` requerida;
- los comandos PowerShell;
- si existe plugin Python;
- si el patch crea, elimina o regenera archivos;
- cómo reconocer una aplicación correcta;
- qué información debe devolver el usuario si falla.

No debe afirmarse que el repositorio quedó validado cuando solo se validó el paquete en una reconstrucción o entorno parcial.

## Instalación de `repo-patcher`

La herramienta debe instalarse de forma aislada, preferentemente mediante `pipx`, y quedar disponible en el `PATH`.

Comprobaciones:

```powershell
repo-patcher --version
repo-patcher doctor
pipx list
Get-Command repo-patcher
```

El ZIP o wheel usado para instalarla puede eliminarse después. La instalación administrada por `pipx` no depende de que el archivo permanezca en `Downloads`.

Desinstalación:

```powershell
pipx uninstall repo-patcher
```

## Regla de cierre

`repo-patcher` es el mecanismo preferente para entregar cambios descargables cuando no puede utilizarse el flujo directo del repositorio.

No sustituye a Codex, GitHub, ramas, commits ni pull requests cuando esos mecanismos están disponibles.