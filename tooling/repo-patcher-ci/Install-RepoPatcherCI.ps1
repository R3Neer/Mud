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
$env:PYTHONDONTWRITEBYTECODE = "1"

foreach ($command in "git", "gh", "python") {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "Required command is not available in PATH: $command"
    }
}

if ($Push -and -not $Commit) {
    throw "-Push requires -Commit."
}

$kitRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$templates = Join-Path $kitRoot "templates"
$Repo = (Resolve-Path -LiteralPath $Repo).Path

$topLevel = (& git -C $Repo rev-parse --show-toplevel 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0) {
    throw "The destination is not a Git repository: $Repo`n$topLevel"
}
if ((Resolve-Path -LiteralPath $topLevel).Path -ne $Repo) {
    throw "-Repo must point to the repository root. Resolved root: $topLevel"
}

$currentBranch = (& git -C $Repo branch --show-current 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $currentBranch -ne "main") {
    throw "Install v6 from the local main branch. Current branch: $currentBranch"
}

$stagedBefore = @(& git -C $Repo diff --cached --name-only)
if ($LASTEXITCODE -ne 0) {
    throw "Could not inspect staged changes."
}
if ($stagedBefore.Count -ne 0) {
    throw "The index already contains staged changes. Commit or unstage them before installing v6."
}

$managedPaths = @(
    ".github/workflows/validate-repo-patcher.yml",
    "tooling/repo-patcher-ci",
    "tooling/repo-patcher-runtime",
    "gobierno/USO-DE-REPO-PATCHER.md"
)
$managedDirty = @(& git -C $Repo status --porcelain=v1 --untracked-files=all -- $managedPaths)
if ($LASTEXITCODE -ne 0) {
    throw "Could not inspect managed paths."
}
if ($managedDirty.Count -ne 0) {
    throw "Managed repo-patcher CI paths already contain local changes:`n$($managedDirty -join [Environment]::NewLine)"
}

$requiredTemplates = @(
    "validate-repo-patcher.yml",
    "Submit-RepoPatch.ps1",
    "Collect-RepoPatchRun.ps1",
    "Test-GitHubWorkflow.ps1",
    "issue_transport.py",
    "issue_queue.py",
    "package_checks.py",
    "test_issue_transport.py",
    "test_issue_queue.py",
    "test_package_checks.py",
    "test_workflow_contract.py",
    "PluginConsent.ps1",
    "Test-PluginConsent.ps1",
    "USO-DE-REPO-PATCHER.md",
    "README.md"
)
foreach ($name in $requiredTemplates) {
    $source = Join-Path $templates $name
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
        throw "The kit is incomplete. Missing template: $source"
    }
}

Write-Host "Validating the v6 kit before modifying the repository..."
& (Join-Path $templates "Test-GitHubWorkflow.ps1") `
    -Workflow (Join-Path $templates "validate-repo-patcher.yml") `
    -ToolingDirectory $templates `
    -RuntimeDirectory (Join-Path $Repo "tooling\repo-patcher-runtime")

$ciDirectory = Join-Path $Repo "tooling\repo-patcher-ci"
$workflowDestination = Join-Path $Repo ".github\workflows\validate-repo-patcher.yml"
$runtimeDestination = Join-Path $Repo "tooling\repo-patcher-runtime"
$documentationDestination = Join-Path $Repo "gobierno\USO-DE-REPO-PATCHER.md"

New-Item -ItemType Directory -Path (Split-Path -Parent $workflowDestination) -Force | Out-Null
New-Item -ItemType Directory -Path $ciDirectory -Force | Out-Null

$copies = @(
    @((Join-Path $templates "validate-repo-patcher.yml"), $workflowDestination),
    @((Join-Path $templates "Submit-RepoPatch.ps1"), (Join-Path $ciDirectory "Submit-RepoPatch.ps1")),
    @((Join-Path $templates "Collect-RepoPatchRun.ps1"), (Join-Path $ciDirectory "Collect-RepoPatchRun.ps1")),
    @((Join-Path $templates "Test-GitHubWorkflow.ps1"), (Join-Path $ciDirectory "Test-GitHubWorkflow.ps1")),
    @((Join-Path $templates "issue_transport.py"), (Join-Path $ciDirectory "issue_transport.py")),
    @((Join-Path $templates "issue_queue.py"), (Join-Path $ciDirectory "issue_queue.py")),
    @((Join-Path $templates "package_checks.py"), (Join-Path $ciDirectory "package_checks.py")),
    @((Join-Path $templates "test_issue_transport.py"), (Join-Path $ciDirectory "test_issue_transport.py")),
    @((Join-Path $templates "test_issue_queue.py"), (Join-Path $ciDirectory "test_issue_queue.py")),
    @((Join-Path $templates "test_package_checks.py"), (Join-Path $ciDirectory "test_package_checks.py")),
    @((Join-Path $templates "test_workflow_contract.py"), (Join-Path $ciDirectory "test_workflow_contract.py")),
    @((Join-Path $templates "PluginConsent.ps1"), (Join-Path $ciDirectory "PluginConsent.ps1")),
    @((Join-Path $templates "Test-PluginConsent.ps1"), (Join-Path $ciDirectory "Test-PluginConsent.ps1")),
    @((Join-Path $templates "README.md"), (Join-Path $ciDirectory "README.md")),
    @((Join-Path $templates "USO-DE-REPO-PATCHER.md"), $documentationDestination),
    @($MyInvocation.MyCommand.Path, (Join-Path $ciDirectory "Install-RepoPatcherCI.ps1"))
)

foreach ($copy in $copies) {
    Copy-Item -LiteralPath $copy[0] -Destination $copy[1] -Force:$Force
    $sourceHash = (Get-FileHash -LiteralPath $copy[0] -Algorithm SHA256).Hash
    $destinationHash = (Get-FileHash -LiteralPath $copy[1] -Algorithm SHA256).Hash
    if ($sourceHash -ne $destinationHash) {
        throw "Installed file hash mismatch: $($copy[1])"
    }
}
"6" | Set-Content -LiteralPath (Join-Path $ciDirectory "VERSION.txt") -Encoding ascii

if ($RuntimeSource) {
    $RuntimeSource = (Resolve-Path -LiteralPath $RuntimeSource).Path
    $runtimePackage = Join-Path $RuntimeSource "repo_patcher\__init__.py"
    if (-not (Test-Path -LiteralPath $runtimePackage -PathType Leaf)) {
        throw "RuntimeSource does not contain repo_patcher: $RuntimeSource"
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
    throw "No vendored repo-patcher runtime exists. Supply -RuntimeSource."
}

Write-Host "Validating the installed files..."
& (Join-Path $ciDirectory "Test-GitHubWorkflow.ps1") `
    -Workflow $workflowDestination `
    -ToolingDirectory $ciDirectory `
    -RuntimeDirectory $runtimeDestination

$previousPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $runtimeDestination
    $runtimeVersion = (& python -m repo_patcher --version 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "The vendored runtime could not be imported after installation."
    }
}
finally {
    $env:PYTHONPATH = $previousPythonPath
}
Write-Host "Vendored repo-patcher runtime: $runtimeVersion"

$status = @(& git -C $Repo status --short --untracked-files=all -- $managedPaths)
if ($LASTEXITCODE -ne 0) {
    throw "Could not inspect the installed diff."
}
if ($status.Count -eq 0) {
    throw "Installation produced no changes; v6 may already be installed."
}

Write-Host ""
Write-Host "Installed CI kit version 6."
Write-Host "Managed changes:"
$status | ForEach-Object { Write-Host "  $_" }

if ($Commit) {
    & git -C $Repo add -- $managedPaths
    if ($LASTEXITCODE -ne 0) {
        throw "git add failed."
    }

    & git -C $Repo diff --cached --check
    if ($LASTEXITCODE -ne 0) {
        throw "The staged diff failed git diff --check."
    }

    & git -C $Repo commit -m "chore(repo-patcher): poll issue validation queue"
    if ($LASTEXITCODE -ne 0) {
        throw "git commit failed."
    }

    $managedAfterCommit = @(& git -C $Repo status --porcelain=v1 --untracked-files=all -- $managedPaths)
    if ($LASTEXITCODE -ne 0 -or $managedAfterCommit.Count -ne 0) {
        throw "Managed paths are not clean after the v6 commit."
    }

    if ($Push) {
        & git -C $Repo push
        if ($LASTEXITCODE -ne 0) {
            throw "git push failed."
        }
    }
}

Write-Host "Version:"
Get-Content -LiteralPath (Join-Path $ciDirectory "VERSION.txt")
Write-Host ""
Write-Host "Next: after this commit is on main, let the scheduled queue process the existing smoke-test issues and inspect their runs and artifacts."
