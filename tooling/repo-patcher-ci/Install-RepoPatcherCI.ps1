[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string] $Repo,

    [string] $RuntimeSource,

    [switch] $Force,

    [switch] $Commit,

    [switch] $Push
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$kitRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = (Resolve-Path -LiteralPath $Repo).Path

& git -C $Repo rev-parse --show-toplevel | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "The destination is not a Git repository: $Repo"
}

$workflowSource = Join-Path `
    $kitRoot `
    "templates\validate-repo-patcher.yml"

$submitSource = Join-Path `
    $kitRoot `
    "templates\Submit-RepoPatch.ps1"

$workflowDestination = Join-Path `
    $Repo `
    ".github\workflows\validate-repo-patcher.yml"

$ciDirectory = Join-Path `
    $Repo `
    "tooling\repo-patcher-ci"

$submitDestination = Join-Path `
    $ciDirectory `
    "Submit-RepoPatch.ps1"

$installerDestination = Join-Path `
    $ciDirectory `
    "Install-RepoPatcherCI.ps1"

$runtimeDestination = Join-Path `
    $Repo `
    "tooling\repo-patcher-runtime"

New-Item `
    -ItemType Directory `
    -Path (Split-Path -Parent $workflowDestination) `
    -Force | Out-Null

New-Item `
    -ItemType Directory `
    -Path $ciDirectory `
    -Force | Out-Null

Copy-Item `
    -LiteralPath $workflowSource `
    -Destination $workflowDestination `
    -Force:$Force

Copy-Item `
    -LiteralPath $submitSource `
    -Destination $submitDestination `
    -Force:$Force

Copy-Item `
    -LiteralPath $MyInvocation.MyCommand.Path `
    -Destination $installerDestination `
    -Force:$Force

if ($RuntimeSource) {
    $RuntimeSource = (Resolve-Path -LiteralPath $RuntimeSource).Path

    if (-not (Test-Path `
        -LiteralPath (Join-Path $RuntimeSource "repo_patcher\__init__.py") `
        -PathType Leaf
    )) {
        throw "RuntimeSource does not contain repo_patcher: $RuntimeSource"
    }

    $sameRuntime = $false
    if (Test-Path -LiteralPath $runtimeDestination) {
        $sameRuntime = (
            (Resolve-Path -LiteralPath $runtimeDestination).Path -eq
            $RuntimeSource
        )
    }

    if (-not $sameRuntime) {
        if (Test-Path -LiteralPath $runtimeDestination) {
            if (-not $Force) {
                throw @"
Runtime already exists:
  $runtimeDestination

Use -Force to replace it.
"@
            }

            Remove-Item `
                -LiteralPath $runtimeDestination `
                -Recurse `
                -Force
        }

        Copy-Item `
            -LiteralPath $RuntimeSource `
            -Destination $runtimeDestination `
            -Recurse `
            -Force
    }
}
elseif (-not (Test-Path `
    -LiteralPath (Join-Path $runtimeDestination "repo_patcher\__init__.py") `
    -PathType Leaf
)) {
    throw @"
No vendored repo-patcher runtime exists in the destination repository.

Pass:
  -RuntimeSource "PATH\TO\repo-patcher-runtime"
"@
}

$pathsToStage = @(
    ".github/workflows/validate-repo-patcher.yml",
    "tooling/repo-patcher-ci",
    "tooling/repo-patcher-runtime"
)

Write-Host ""
Write-Host "Installed:"
foreach ($path in $pathsToStage) {
    Write-Host "  $path"
}

if ($Commit) {
    & git -C $Repo add -- $pathsToStage
    if ($LASTEXITCODE -ne 0) {
        throw "git add failed."
    }

    & git -C $Repo diff --cached --quiet
    $hasNoStagedChanges = ($LASTEXITCODE -eq 0)

    if (-not $hasNoStagedChanges) {
        & git -C $Repo commit -m `
            "tooling(repo-patcher): add package validation workflow"

        if ($LASTEXITCODE -ne 0) {
            throw "git commit failed."
        }
    }
    else {
        Write-Host "No new CI changes needed a commit."
    }

    if ($Push) {
        & git -C $Repo push
        if ($LASTEXITCODE -ne 0) {
            throw "git push failed."
        }
    }
}
elseif ($Push) {
    throw "-Push requires -Commit."
}

Write-Host ""
Write-Host "Next:"
Write-Host "  git -C `"$Repo`" status --short"
Write-Host "  git -C `"$Repo`" add .github/workflows/validate-repo-patcher.yml tooling/repo-patcher-ci tooling/repo-patcher-runtime"
Write-Host "  git -C `"$Repo`" commit -m `"tooling(repo-patcher): add package validation workflow`""
Write-Host "  git -C `"$Repo`" push"
