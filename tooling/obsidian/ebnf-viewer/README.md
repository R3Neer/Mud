# MUD EBNF Viewer

Plugin local de Obsidian para abrir y editar archivos `.ebnf` sin salir de la
bóveda.

Incluye:

- resaltado básico de la metanotación EBNF;
- números de línea, ajuste de línea y resaltado de paréntesis;
- búsqueda mediante `Ctrl+F`;
- deshacer y rehacer;
- guardado automático y guardado inmediato mediante `Ctrl+S`.

## Instalación local

Desde este directorio:

```powershell
npm run install-local
```

El instalador copia el plugin a `.obsidian/plugins/mud-ebnf-viewer`, lo añade a
`.obsidian/community-plugins.json` y deja intactos los archivos `.ebnf`.

Después hay que recargar Obsidian una vez. Para actualizar el plugin tras un
cambio, se ejecuta el mismo comando y se vuelve a recargar Obsidian.

## Personalización de colores

Las paletas están al principio de `styles.css`, en los bloques
`.theme-dark .mud-ebnf-view` y `.theme-light .mud-ebnf-view`. Cada categoría
dispone de una variable `--mud-ebnf-*`, por lo que se puede cambiar un color sin
tocar las reglas del editor.

Los valores iniciales siguen las convenciones visuales de Visual Studio Code
Dark+ y Light+, adaptadas a las categorías de EBNF.
