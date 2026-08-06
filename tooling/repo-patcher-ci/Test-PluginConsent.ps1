[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "PluginConsent.ps1")

function Assert-Equal {
    param($Expected, $Actual, [string] $Label)
    if ($Expected -ne $Actual) {
        throw "$Label failed. Expected $Expected, got $Actual."
    }
}

function Assert-Throws {
    param([scriptblock] $Action, [string] $ExpectedFragment, [string] $Label)
    try {
        & $Action
    }
    catch {
        if ($_.Exception.Message -notlike "*$ExpectedFragment*") {
            throw "$Label returned the wrong diagnostic: $($_.Exception.Message)"
        }
        return
    }
    throw "$Label did not throw."
}

Assert-Equal $false (Resolve-RepoPatcherPluginConsent -HasPlugin:$false -CanPrompt:$false) "declarative package"
Assert-Equal $true (Resolve-RepoPatcherPluginConsent -HasPlugin:$true -TrustPlugin -CanPrompt:$false) "non-interactive switch"
Assert-Equal $true (Resolve-RepoPatcherPluginConsent -HasPlugin:$true -CanPrompt:$true -Prompt { "SI" }) "interactive authorization"
Assert-Throws { Resolve-RepoPatcherPluginConsent -HasPlugin:$true -CanPrompt:$true -Prompt { "no" } } "cancelada" "interactive rejection"
Assert-Throws { Resolve-RepoPatcherPluginConsent -HasPlugin:$true -CanPrompt:$false } "-TrustPlugin" "non-interactive rejection"

Write-Host "Plugin consent tests passed."
