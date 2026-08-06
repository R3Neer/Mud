[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string] $Workflow
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$Workflow = (Resolve-Path -LiteralPath $Workflow).Path

$version = "v1.7.12"
$asset = "actionlint_1.7.12_windows_amd64.zip"
$expectedHash = "6e7241b51e6817ea6a047693d8e6fed13b31819c9a0dd6c5a726e1592d22f6e9"
$temp = Join-Path $env:TEMP "repo-patcher-actionlint-1.7.12"
$archive = Join-Path $temp $asset
$expanded = Join-Path $temp "expanded"

Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $temp -Force | Out-Null

try {
    & gh release download $version `
        --repo rhysd/actionlint `
        --pattern $asset `
        --dir $temp `
        --clobber

    if ($LASTEXITCODE -ne 0) {
        throw "Could not download actionlint."
    }

    $actualHash = (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualHash -ne $expectedHash) {
        throw "actionlint SHA-256 mismatch."
    }

    Expand-Archive -LiteralPath $archive -DestinationPath $expanded -Force
    & (Join-Path $expanded "actionlint.exe") $Workflow

    if ($LASTEXITCODE -ne 0) {
        throw "actionlint rejected the workflow."
    }

    Write-Host "Workflow accepted by actionlint: $Workflow"
}
finally {
    Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
}
