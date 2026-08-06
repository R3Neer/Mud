[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string] $StateFile,

    [switch] $KeepBranch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$StateFile = (Resolve-Path -LiteralPath $StateFile).Path
$state = Get-Content -LiteralPath $StateFile -Raw | ConvertFrom-Json

foreach ($property in @(
    "request_id", "run_id", "slug", "branch", "repo", "artifact_output"
)) {
    if (-not $state.PSObject.Properties[$property]) {
        throw "State file is missing property: $property"
    }
}

$runExitCode = 1

try {
    Write-Host "Following GitHub Actions run $($state.run_id)..."
    & gh run watch $state.run_id --repo $state.slug --exit-status
    $runExitCode = $LASTEXITCODE

    if (Test-Path -LiteralPath $state.artifact_output) {
        Remove-Item -LiteralPath $state.artifact_output -Recurse -Force
    }

    New-Item -ItemType Directory -Path $state.artifact_output -Force | Out-Null

    Write-Host "Downloading validation artifact..."
    & gh run download $state.run_id `
        --repo $state.slug `
        -n "repo-patcher-validation-$($state.request_id)" `
        -D $state.artifact_output

    if ($LASTEXITCODE -ne 0) {
        Write-Warning "The validation artifact could not be downloaded."
    }
    else {
        Write-Host "Validation files: $($state.artifact_output)"
    }

    if ($runExitCode -ne 0) {
        Write-Host ""
        Write-Host "Failed workflow log:"
        & gh run view $state.run_id --repo $state.slug --log-failed
    }
}
finally {
    if (-not $KeepBranch) {
        Write-Host "Deleting temporary remote branch..."
        & git -C $state.repo push origin --delete $state.branch | Out-Null
        Remove-Item -LiteralPath $StateFile -Force -ErrorAction SilentlyContinue
    }
    else {
        Write-Host "Temporary branch retained: $($state.branch)"
        Write-Host "State retained: $StateFile"
    }
}

exit $runExitCode
