[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string] $Workflow,

    [string] $ToolingDirectory,

    [string] $RuntimeDirectory
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$env:PYTHONDONTWRITEBYTECODE = "1"
$Workflow = (Resolve-Path -LiteralPath $Workflow).Path

if (-not $ToolingDirectory) {
    $ToolingDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
}
$ToolingDirectory = (Resolve-Path -LiteralPath $ToolingDirectory).Path

if (-not $RuntimeDirectory) {
    $RuntimeDirectory = Join-Path (Split-Path -Parent $ToolingDirectory) "repo-patcher-runtime"
}
$RuntimeDirectory = (Resolve-Path -LiteralPath $RuntimeDirectory).Path
if (-not (Test-Path -LiteralPath (Join-Path $RuntimeDirectory "repo_patcher\__init__.py") -PathType Leaf)) {
    throw "Vendored repo-patcher runtime is missing: $RuntimeDirectory"
}

foreach ($command in "python", "gh") {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "Required command is not available in PATH: $command"
    }
}

$transport = Join-Path $ToolingDirectory "issue_transport.py"
$queue = Join-Path $ToolingDirectory "issue_queue.py"
$packageChecks = Join-Path $ToolingDirectory "package_checks.py"
$transportTests = Join-Path $ToolingDirectory "test_issue_transport.py"
$queueTests = Join-Path $ToolingDirectory "test_issue_queue.py"
$packageTests = Join-Path $ToolingDirectory "test_package_checks.py"
$workflowTests = Join-Path $ToolingDirectory "test_workflow_contract.py"
$pluginConsent = Join-Path $ToolingDirectory "PluginConsent.ps1"
$pluginConsentTests = Join-Path $ToolingDirectory "Test-PluginConsent.ps1"
foreach ($path in $transport, $queue, $packageChecks, $transportTests, $queueTests, $packageTests, $workflowTests, $pluginConsent, $pluginConsentTests) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Required relay file is missing: $path"
    }
}

Write-Host "Compiling queue, transport and tests..."
& python -m py_compile $transport $queue $packageChecks $transportTests $queueTests $packageTests $workflowTests
if ($LASTEXITCODE -ne 0) {
    throw "Python compilation failed."
}

try {
    Write-Host "Running issue transport tests..."
    & python $transportTests
    if ($LASTEXITCODE -ne 0) {
        throw "Issue transport tests failed."
    }

    Write-Host "Running scheduled queue tests..."
    & python $queueTests
    if ($LASTEXITCODE -ne 0) {
        throw "Issue queue tests failed."
    }

    Write-Host "Running runtime-backed package inspection tests..."
    $previousPythonPath = $env:PYTHONPATH
    try {
        $env:PYTHONPATH = $RuntimeDirectory
        & python $packageTests
        if ($LASTEXITCODE -ne 0) {
            throw "Package inspection tests failed."
        }
    }
    finally {
        $env:PYTHONPATH = $previousPythonPath
    }

    Write-Host "Running plugin consent tests..."
    & $pluginConsentTests
    if ($LASTEXITCODE -ne 0) {
        throw "Plugin consent tests failed."
    }

    Write-Host "Running workflow contract tests..."
    $previousWorkflowPath = $env:MUD_WORKFLOW_PATH
    try {
        $env:MUD_WORKFLOW_PATH = $Workflow
        & python $workflowTests
        if ($LASTEXITCODE -ne 0) {
            throw "Workflow contract tests failed."
        }
    }
    finally {
        $env:MUD_WORKFLOW_PATH = $previousWorkflowPath
    }
}
finally {
    Remove-Item -LiteralPath (Join-Path $ToolingDirectory "__pycache__") -Recurse -Force -ErrorAction SilentlyContinue
}

$version = "v1.7.12"
$asset = "actionlint_1.7.12_windows_amd64.zip"
$expectedHash = "6e7241b51e6817ea6a047693d8e6fed13b31819c9a0dd6c5a726e1592d22f6e9"
$cacheBase = if ($env:LOCALAPPDATA) {
    Join-Path $env:LOCALAPPDATA "repo-patcher-ci\tools\actionlint-1.7.12"
}
else {
    Join-Path $env:TEMP "repo-patcher-ci-tools\actionlint-1.7.12"
}
$archive = Join-Path $cacheBase $asset
$expanded = Join-Path $cacheBase "expanded"
$executable = Join-Path $expanded "actionlint.exe"

New-Item -ItemType Directory -Path $cacheBase -Force | Out-Null

$download = $true
if (Test-Path -LiteralPath $archive -PathType Leaf) {
    $actualHash = (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualHash -eq $expectedHash) {
        $download = $false
    }
    else {
        Remove-Item -LiteralPath $archive -Force
    }
}

if ($download) {
    & gh release download $version `
        --repo rhysd/actionlint `
        --pattern $asset `
        --dir $cacheBase `
        --clobber
    if ($LASTEXITCODE -ne 0) {
        throw "Could not download actionlint."
    }
}

$actualHash = (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualHash -ne $expectedHash) {
    throw "actionlint SHA-256 mismatch. Expected $expectedHash, got $actualHash."
}

if (-not (Test-Path -LiteralPath $executable -PathType Leaf)) {
    Remove-Item -LiteralPath $expanded -Recurse -Force -ErrorAction SilentlyContinue
    Expand-Archive -LiteralPath $archive -DestinationPath $expanded -Force
}

& $executable $Workflow
if ($LASTEXITCODE -ne 0) {
    throw "actionlint rejected the workflow."
}

Write-Host "Workflow accepted by actionlint: $Workflow"
