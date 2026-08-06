[CmdletBinding()]
param(
    [Parameter(Mandatory, Position = 0)]
    [ValidateScript({
        if (-not (Test-Path -LiteralPath $_ -PathType Leaf)) {
            throw "Package file does not exist: $_"
        }
        $true
    })]
    [string] $Package,

    [string] $Repo = (Get-Location).Path,
    [string] $TargetRef = "HEAD",
    [string] $Workflow = "validate-repo-patcher.yml",
    [string] $ArtifactDirectory = (
        Join-Path $env:USERPROFILE "Downloads\repo-patcher-validation"
    ),
    [switch] $NoWait,
    [switch] $KeepBranch,
    [switch] $AllowPythonPlugin
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Native {
    param([string] $File, [string[]] $Arguments = @())
    & $File @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$File failed with exit code $LASTEXITCODE."
    }
}

function Get-NativeText {
    param([string] $File, [string[]] $Arguments = @())
    $lines = & $File @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "$File failed with exit code $LASTEXITCODE.`n$($lines -join [Environment]::NewLine)"
    }
    return (($lines -join [Environment]::NewLine).Trim())
}

function Get-StateRoot {
    if ($env:LOCALAPPDATA) {
        return Join-Path $env:LOCALAPPDATA "repo-patcher-ci"
    }
    return Join-Path $env:TEMP "repo-patcher-ci"
}

function Invoke-Dispatch {
    param(
        [string] $WorkflowName,
        [string] $Repository,
        [string] $WorkflowRef,
        [hashtable] $Inputs
    )

    $delays = @(0, 5, 10, 20, 40)

    for ($attempt = 0; $attempt -lt $delays.Count; $attempt++) {
        if ($delays[$attempt] -gt 0) {
            Write-Warning "GitHub returned a server error. Retrying in $($delays[$attempt]) seconds..."
            Start-Sleep -Seconds $delays[$attempt]
        }

        $output = & gh workflow run $WorkflowName `
            --repo $Repository `
            --ref $WorkflowRef `
            -f "request_id=$($Inputs.request_id)" `
            -f "package_ref=$($Inputs.package_ref)" `
            -f "package_path=$($Inputs.package_path)" `
            -f "target_sha=$($Inputs.target_sha)" `
            -f "package_sha256=$($Inputs.package_sha256)" `
            -f "allow_python_plugin=$($Inputs.allow_python_plugin)" 2>&1

        $exitCode = $LASTEXITCODE
        $text = ($output -join [Environment]::NewLine).Trim()

        if ($exitCode -eq 0) {
            if ($text) { Write-Host $text }
            return
        }

        if ($text -notmatch "HTTP 5\d\d") {
            throw "GitHub rejected the workflow dispatch.`n$text"
        }
    }

    throw "GitHub did not accept the workflow after five attempts."
}

foreach ($command in "git", "gh") {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "Required command is not available in PATH: $command"
    }
}

$Package = (Resolve-Path -LiteralPath $Package).Path
$Repo = (Resolve-Path -LiteralPath $Repo).Path
$Repo = (Resolve-Path -LiteralPath (Get-NativeText git @("-C", $Repo, "rev-parse", "--show-toplevel"))).Path

Invoke-Native gh @("auth", "status")

$origin = Get-NativeText git @("-C", $Repo, "remote", "get-url", "origin")
$slug = Get-NativeText gh @("repo", "view", $origin, "--json", "nameWithOwner", "--jq", ".nameWithOwner")
$defaultBranch = Get-NativeText gh @("repo", "view", $origin, "--json", "defaultBranchRef", "--jq", ".defaultBranchRef.name")
$targetSha = Get-NativeText git @("-C", $Repo, "rev-parse", $TargetRef)
Invoke-Native gh @("api", "repos/$slug/commits/$targetSha", "--silent")

$requestId = "{0}-{1}" -f (Get-Date -Format "yyyyMMdd-HHmmss"), ([Guid]::NewGuid().ToString("N").Substring(0, 8))
$branch = "repo-patcher-validation/$requestId"
$remotePackagePath = ".repo-patcher-candidates/package.zip"
$worktree = Join-Path $env:TEMP "repo-patcher-$requestId"
$artifactOutput = Join-Path $ArtifactDirectory $requestId
$packageHash = (Get-FileHash -LiteralPath $Package -Algorithm SHA256).Hash.ToLowerInvariant()
$safeSlug = $slug.Replace("/", "__")
$stateDirectory = Join-Path (Get-StateRoot) $safeSlug
$stateFile = Join-Path $stateDirectory "$requestId.json"

$worktreeCreated = $false
$branchPushed = $false
$dispatchAccepted = $false
$runId = $null

try {
    Write-Host "[1/5] Preparing temporary carrier branch..."
    Invoke-Native git @("-C", $Repo, "worktree", "add", "-b", $branch, $worktree, $targetSha)
    $worktreeCreated = $true

    $remotePackageFile = Join-Path $worktree $remotePackagePath
    New-Item -ItemType Directory -Path (Split-Path -Parent $remotePackageFile) -Force | Out-Null
    Copy-Item -LiteralPath $Package -Destination $remotePackageFile -Force

    Invoke-Native git @("-C", $worktree, "config", "user.name", "repo-patcher CI uploader")
    Invoke-Native git @("-C", $worktree, "config", "user.email", "repo-patcher-ci@users.noreply.github.com")
    Invoke-Native git @("-C", $worktree, "add", "--", $remotePackagePath)
    Invoke-Native git @("-C", $worktree, "commit", "-m", "ci(repo-patcher): carry package $requestId")

    Write-Host "[2/5] Uploading package branch..."
    Invoke-Native git @("-C", $worktree, "push", "--set-upstream", "origin", $branch)
    $branchPushed = $true

    Write-Host "[3/5] Requesting GitHub Actions validation..."
    Invoke-Dispatch `
        -WorkflowName $Workflow `
        -Repository $slug `
        -WorkflowRef $defaultBranch `
        -Inputs @{
            request_id = $requestId
            package_ref = $branch
            package_path = $remotePackagePath
            target_sha = $targetSha
            package_sha256 = $packageHash
            allow_python_plugin = $AllowPythonPlugin.IsPresent.ToString().ToLowerInvariant()
        }
    $dispatchAccepted = $true

    Write-Host "[4/5] Waiting for GitHub to register the run..."
    $expectedTitle = "repo-patcher validation $requestId"
    $started = [DateTime]::UtcNow
    $deadline = $started.AddMinutes(2)
    $lastProgress = $started.AddSeconds(-10)

    while (-not $runId -and [DateTime]::UtcNow -lt $deadline) {
        if (([DateTime]::UtcNow - $lastProgress).TotalSeconds -ge 10) {
            $elapsed = [int](([DateTime]::UtcNow - $started).TotalSeconds)
            Write-Host "  Still waiting for run registration (${elapsed}s)..."
            $lastProgress = [DateTime]::UtcNow
        }

        Start-Sleep -Seconds 2
        $runsJson = Get-NativeText gh @(
            "run", "list", "--repo", $slug, "--workflow", $Workflow,
            "--event", "workflow_dispatch", "--limit", "50", "--json",
            "databaseId,displayTitle,status,conclusion,createdAt,url"
        )

        $runs = @($runsJson | ConvertFrom-Json)
        $run = $runs | Where-Object { $_.displayTitle -eq $expectedTitle } | Sort-Object createdAt -Descending | Select-Object -First 1

        if ($run) {
            $runId = [string] $run.databaseId
            Write-Host "GitHub Actions run: $($run.url)"
        }
    }

    if (-not $runId) {
        throw "GitHub accepted the dispatch but the run was not found."
    }

    New-Item -ItemType Directory -Path $stateDirectory -Force | Out-Null
    [ordered] @{
        schema = 1
        request_id = $requestId
        run_id = $runId
        slug = $slug
        branch = $branch
        repo = $Repo
        artifact_output = $artifactOutput
        workflow = $Workflow
        target_sha = $targetSha
        package_sha256 = $packageHash
        allow_python_plugin = $AllowPythonPlugin.IsPresent
        created_at_utc = [DateTime]::UtcNow.ToString("o")
    } | ConvertTo-Json | Set-Content -LiteralPath $stateFile -Encoding utf8

    Write-Host "[5/5] Carrier uploaded and run registered."

    if ($NoWait) {
        Write-Host ""
        Write-Host "Validation continues on GitHub."
        Write-Host "State file: $stateFile"
        Write-Host ""
        Write-Host "Collect later with:"
        Write-Host "& `"$Repo\tooling\repo-patcher-ci\Collect-RepoPatchRun.ps1`" -StateFile `"$stateFile`""
        exit 0
    }

    & "$Repo\tooling\repo-patcher-ci\Collect-RepoPatchRun.ps1" -StateFile $stateFile -KeepBranch:$KeepBranch
    exit $LASTEXITCODE
}
finally {
    if ($worktreeCreated -and (Test-Path -LiteralPath $worktree)) {
        & git -C $Repo worktree remove --force $worktree | Out-Null
    }

    & git -C $Repo branch -D $branch 2>$null | Out-Null

    if ($branchPushed -and -not $dispatchAccepted) {
        & git -C $Repo push origin --delete $branch | Out-Null
    }
}
