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

$ciDirectory = Join-Path $Repo "tooling\repo-patcher-ci"
$workflowDestination = Join-Path $Repo ".github\workflows\validate-repo-patcher.yml"
$runtimeDestination = Join-Path $Repo "tooling\repo-patcher-runtime"

New-Item -ItemType Directory -Path (Split-Path -Parent $workflowDestination) -Force | Out-Null
New-Item -ItemType Directory -Path $ciDirectory -Force | Out-Null

$copies = @(
    @((Join-Path $kitRoot "templates\validate-repo-patcher.yml"), $workflowDestination),
    @((Join-Path $kitRoot "templates\Submit-RepoPatch.ps1"), (Join-Path $ciDirectory "Submit-RepoPatch.ps1")),
    @((Join-Path $kitRoot "templates\Collect-RepoPatchRun.ps1"), (Join-Path $ciDirectory "Collect-RepoPatchRun.ps1")),
    @((Join-Path $kitRoot "templates\Test-GitHubWorkflow.ps1"), (Join-Path $ciDirectory "Test-GitHubWorkflow.ps1")),
    @($MyInvocation.MyCommand.Path, (Join-Path $ciDirectory "Install-RepoPatcherCI.ps1"))
)

foreach ($copy in $copies) {
    Copy-Item -LiteralPath $copy[0] -Destination $copy[1] -Force:$Force
}

"3" | Set-Content -LiteralPath (Join-Path $ciDirectory "VERSION.txt") -Encoding ascii

if ($RuntimeSource) {
    $RuntimeSource = (Resolve-Path -LiteralPath $RuntimeSource).Path
    $runtimePackage = Join-Path $RuntimeSource "repo_patcher\__init__.py"

    if (-not (Test-Path -LiteralPath $runtimePackage -PathType Leaf)) {
        throw "RuntimeSource does not contain repo_patcher."
    }

    $sameRuntime = $false
    if (Test-Path -LiteralPath $runtimeDestination) {
        $sameRuntime = ((Resolve-Path -LiteralPath $runtimeDestination).Path -eq $RuntimeSource)
    }

    if (-not $sameRuntime) {
        if (Test-Path -LiteralPath $runtimeDestination) {
            if (-not $Force) {
                throw "Runtime exists. Use -Force to replace it."
            }
            Remove-Item -LiteralPath $runtimeDestination -Recurse -Force
        }

        Copy-Item -LiteralPath $RuntimeSource -Destination $runtimeDestination -Recurse -Force
    }
}
elseif (-not (Test-Path -LiteralPath (Join-Path $runtimeDestination "repo_patcher\__init__.py") -PathType Leaf)) {
    throw "No vendored repo-patcher runtime exists."
}

& (Join-Path $ciDirectory "Test-GitHubWorkflow.ps1") -Workflow $workflowDestination
if ($LASTEXITCODE -ne 0) {
    throw "Workflow validation failed."
}

$pathsToStage = @(
    ".github/workflows/validate-repo-patcher.yml",
    "tooling/repo-patcher-ci",
    "tooling/repo-patcher-runtime"
)

Write-Host ""
Write-Host "Installed CI kit version 3."

if ($Commit) {
    & git -C $Repo add -- $pathsToStage
    if ($LASTEXITCODE -ne 0) { throw "git add failed." }

    & git -C $Repo diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        & git -C $Repo commit -m "tooling(repo-patcher): update validation workflow to v3"
        if ($LASTEXITCODE -ne 0) { throw "git commit failed." }
    }

    if ($Push) {
        & git -C $Repo push
        if ($LASTEXITCODE -ne 0) { throw "git push failed." }
    }
}
elseif ($Push) {
    throw "-Push requires -Commit."
}

Write-Host "Version:"
Get-Content -LiteralPath (Join-Path $ciDirectory "VERSION.txt")
