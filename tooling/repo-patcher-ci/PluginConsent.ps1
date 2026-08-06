Set-StrictMode -Version Latest

function Test-RepoPatcherCanPrompt {
    [CmdletBinding()]
    param()

    try {
        return [Environment]::UserInteractive -and -not [Console]::IsInputRedirected
    }
    catch {
        return $false
    }
}

function Resolve-RepoPatcherPluginConsent {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [bool] $HasPlugin,

        [switch] $TrustPlugin,

        [bool] $CanPrompt = (Test-RepoPatcherCanPrompt),

        [scriptblock] $Prompt = {
            Read-Host "Escribe SI para autorizar el plugin Python"
        }
    )

    if (-not $HasPlugin) {
        return $false
    }

    if ($TrustPlugin.IsPresent) {
        return $true
    }

    if (-not $CanPrompt) {
        throw @"
El paquete contiene un plugin Python, pero esta terminal no permite solicitar consentimiento.
No se ha ejecutado el plugin.
Vuelve a ejecutar el envío con -TrustPlugin después de revisar y autorizar conscientemente el código.
"@
    }

    Write-Warning @"
Este paquete contiene un plugin Python y puede ejecutar código con tus permisos.
La autorización se aplicará a explain, check y apply en GitHub Actions.
"@

    $answer = [string] (& $Prompt)
    if ($answer.Trim().ToUpperInvariant() -ne "SI") {
        throw "Operación cancelada. El plugin no se ha autorizado ni ejecutado."
    }

    return $true
}
