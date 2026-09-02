# Migración temporal español-inglés

Esta carpeta integra temporalmente
[`R3Translate`](https://github.com/R3Neer/R3Translate) en Mud. No es una nueva
autoridad normativa ni participará en la futura migración de nombres de rutas.

- `mud-es-en.toml` es la fuente ejecutable de términos, protecciones,
  frontmatter, inglés británico y hallazgos específicos de Mud.
- `render_glossary.py` genera la vista humana de
  `notas/glosario-de-traduccion-es-en.md` y `--check` impide divergencias.
- `check_migration.py` combina `r3translate check` con las barreras editoriales
  y de temporalidad existentes.

Ejemplo sobre el README representativo:

```powershell
python tooling/translation/render_glossary.py --check
python tooling/translation/check_migration.py
```

Para comparar un candidato con su fuente y detectar enlaces, identificadores o
protecciones alterados:

```powershell
python tooling/translation/check_migration.py ruta/candidato.md --source ruta/original.md
```

Si `r3translate` no está en `PATH`, se puede usar `--r3translate RUTA` o la
variable `R3TRANSLATE`. La clave de DeepL se proporciona exclusivamente como
`DEEPL_AUTH_KEY`; nunca se escribe en esta carpeta.

El perfil y el glosario se eliminarán juntos cuando se cumpla su condición
`temporary-delete-when`.
