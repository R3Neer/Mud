[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateScript({
        if (-not (Test-Path -LiteralPath $_ -PathType Leaf)) {
            throw "Workflow does not exist: $_"
        }
        $true
    })]
    [string] $Workflow,

    [string] $ActionlintVersion = "v1.7.12"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Workflow = (Resolve-Path -LiteralPath $Workflow).Path

$existing = Get-Command actionlint `
    -ErrorAction SilentlyContinue

if ($existing) {
    & $existing.Source $Workflow
    if ($LASTEXITCODE -ne 0) {
        throw "actionlint rejected the workflow."
    }

    Write-Host "Workflow accepted by actionlint: $Workflow"
    exit 0
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw @"
actionlint is not installed and GitHub CLI is unavailable.

Install gh or actionlint, then rerun this command.
"@
}

& gh auth status | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "GitHub CLI is not authenticated."
}

$versionNumber = $ActionlintVersion.TrimStart("v")
$asset = "actionlint_${versionNumber}_windows_amd64.zip"

$knownHashes = @{
    "v1.7.12" = @{
        Asset = "actionlint_1.7.12_windows_amd64.zip"
        Sha256 = "6e7241b51e6817ea6a047693d8e6fed13b31819c9a0dd6c5a726e1592d22f6e9"
    }
}

if (-not $knownHashes.ContainsKey($ActionlintVersion)) {
    throw @"
No pinned checksum is configured for actionlint $ActionlintVersion.

Update Test-GitHubWorkflow.ps1 before changing the version.
"@
}

$expectedAsset = $knownHashes[$ActionlintVersion].Asset
$expectedHash = $knownHashes[$ActionlintVersion].Sha256

if ($asset -ne $expectedAsset) {
    throw "Internal actionlint asset mismatch."
}

$temp = Join-Path `
    $env:TEMP `
    "repo-patcher-actionlint-$versionNumber"

$download = Join-Path $temp $asset
$expanded = Join-Path $temp "expanded"

Remove-Item `
    -LiteralPath $temp `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

New-Item `
    -ItemType Directory `
    -Path $temp `
    -Force | Out-Null

try {
    & gh release download $ActionlintVersion `
        --repo rhysd/actionlint `
        --pattern $asset `
        --dir $temp `
        --clobber

    if ($LASTEXITCODE -ne 0) {
        throw "Could not download actionlint $ActionlintVersion."
    }

    $actualHash = (
        Get-FileHash `
            -LiteralPath $download `
            -Algorithm SHA256
    ).Hash.ToLowerInvariant()

    if ($actualHash -ne $expectedHash) {
        throw @"
Downloaded actionlint archive has the wrong SHA-256.

Expected: $expectedHash
Actual:   $actualHash
"@
    }

    Expand-Archive `
        -LiteralPath $download `
        -DestinationPath $expanded `
        -Force

    $executable = Join-Path $expanded "actionlint.exe"

    if (-not (
        Test-Path `
            -LiteralPath $executable `
            -PathType Leaf
    )) {
        throw "actionlint.exe was not found after extraction."
    }

    & $executable $Workflow

    if ($LASTEXITCODE -ne 0) {
        throw "actionlint rejected the workflow."
    }

    Write-Host "Workflow accepted by actionlint: $Workflow"
}
finally {
    Remove-Item `
        -LiteralPath $temp `
        -Recurse `
        -Force `
        -ErrorAction SilentlyContinue
}
