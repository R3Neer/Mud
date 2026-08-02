# Python CLI Terminal

Plugin personal de Obsidian Desktop para abrir archivos Python en una vista contextual con compositor de comandos y terminal PowerShell real.

## Comportamiento

- Registra los archivos `.py` en una vista central.
- Reconoce paquetes con `__main__.py`, scripts ejecutables y entradas de `unittest`.
- Analiza `argparse` mediante `ast.parse`, sin importar el módulo.
- Usa sondas `--help` limitadas únicamente cuando detecta un framework compatible.
- Conserva una sesión ConPTY por raíz de proyecto.
- Ejecuta `node-pty` en un proceso Node.js auxiliar porque el renderer de
  Obsidian bloquea el `Worker` que necesita ConPTY.
- No ejecuta el comando preparado hasta que se pulsa **Ejecutar** o `Enter`.
- Los módulos auxiliares permanecen visibles, pero se marcan como «sin CLI detectado».

La configuración `tooling/python-cli-terminal.json` aporta datos específicos del proyecto que no forman parte de `argparse`, como los valores disponibles para `--profile`.

## Desarrollo e instalación

```powershell
npm install
npm run check
npm run install-local
```

`install-local` copia el bundle, los estilos, el analizador Python y `node-pty` a `.obsidian/plugins/mud-python-cli-terminal/`, y activa el plugin sin retirar los demás.

El identificador interno conserva el prefijo histórico para mantener compatible
la instalación existente; el nombre visible del plugin es `Python CLI Terminal`.

Requisitos:

- Windows 10 o posterior.
- Obsidian 1.7.2 o posterior.
- PowerShell 7 o Windows PowerShell.
- Node.js disponible mediante el ejecutable configurado.
- Python disponible mediante el ejecutable configurado.

## Seguridad

El análisis estático no ejecuta el archivo. Las sondas dinámicas usan un proceso con tiempo y salida limitados, pero no constituyen un sandbox: un módulo puede ejecutar código de nivel superior antes de mostrar su ayuda. `validate_grammar.py` está configurado para no recibir sondas porque no implementa `--help`.

No hay telemetría, IA ni tráfico externo del plugin.
