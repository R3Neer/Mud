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
        Join-Path `
            $env:USERPROFILE `
            "Downloads\repo-patcher-validation"
    ),

    [switch] $KeepBranch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Native {
    param(
        [Parameter(Mandatory)]
        [string] $File,

        [Parameter()]
        [string[]] $Arguments = @(),

        [switch] $AllowFailure
    )

    & $File @Arguments
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0 -and -not $AllowFailure) {
        throw "$File failed with exit code $exitCode."
    }

    return $exitCode
}

function Get-NativeText {
    param(
        [Parameter(Mandatory)]
        [string] $File,

        [Parameter()]
        [string[]] $Arguments = @()
    )

    $lines = & $File @Arguments 2>&1
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        throw @"
$File failed with exit code $exitCode.

$($lines -join [Environment]::NewLine)
"@
    }

    return (($lines -join [Environment]::NewLine).Trim())
}

foreach ($command in "git", "gh") {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "Required command is not available in PATH: $command"
    }
}

$Package = (Resolve-Path -LiteralPath $Package).Path
$Repo = (Resolve-Path -LiteralPath $Repo).Path

$repoRoot = Get-NativeText git @(
    "-C", $Repo,
    "rev-parse", "--show-toplevel"
)

$Repo = (Resolve-Path -LiteralPath $repoRoot).Path

Invoke-Native gh @("auth", "status") | Out-Null

$slug = Get-NativeText gh @(
    "repo", "view",
    "--json", "nameWithOwner",
    "--jq", ".nameWithOwner"
)

$targetSha = Get-NativeText git @(
    "-C", $Repo,
    "rev-parse", $TargetRef
)

# The target must already exist on GitHub so Actions can check it out.
Invoke-Native gh @(
    "api",
    "repos/$slug/commits/$targetSha",
    "--silent"
) | Out-Null

$requestId = "{0}-{1}" -f (
    Get-Date -Format "yyyyMMdd-HHmmss"
), (
    [Guid]::NewGuid().ToString("N").Substring(0, 8)
)

$branch = "repo-patcher-validation/$requestId"
$candidateDirectory = ".repo-patcher-candidates"
$remotePackagePath = "$candidateDirectory/package.zip"
$requestPath = "$candidateDirectory/request.json"
$worktree = Join-Path $env:TEMP "repo-patcher-$requestId"
$artifactOutput = Join-Path $ArtifactDirectory $requestId
$branchPushed = $false
$worktreeCreated = $false
$runId = $null
$runExitCode = 1

$packageHash = (
    Get-FileHash `
        -LiteralPath $Package `
        -Algorithm SHA256
).Hash.ToLowerInvariant()

try {
    New-Item `
        -ItemType Directory `
        -Path $ArtifactDirectory `
        -Force | Out-Null

    Invoke-Native git @(
        "-C", $Repo,
        "worktree", "add",
        "-b", $branch,
        $worktree,
        $targetSha
    ) | Out-Null

    $worktreeCreated = $true

    $candidatePath = Join-Path `
        $worktree `
        $candidateDirectory

    New-Item `
        -ItemType Directory `
        -Path $candidatePath `
        -Force | Out-Null

    Copy-Item `
        -LiteralPath $Package `
        -Destination (
            Join-Path $worktree $remotePackagePath
        ) `
        -Force

    [ordered] @{
        schema = 1
        request_id = $requestId
        target_sha = $targetSha
        package_sha256 = $packageHash
        package_name = [System.IO.Path]::GetFileName($Package)
        created_at_utc = [DateTime]::UtcNow.ToString("o")
    } |
        ConvertTo-Json |
        Set-Content `
            -LiteralPath (
                Join-Path $worktree $requestPath
            ) `
            -Encoding utf8

    Invoke-Native git @(
        "-C", $worktree,
        "config", "user.name",
        "repo-patcher CI uploader"
    ) | Out-Null

    Invoke-Native git @(
        "-C", $worktree,
        "config", "user.email",
        "repo-patcher-ci@users.noreply.github.com"
    ) | Out-Null

    Invoke-Native git @(
        "-C", $worktree,
        "add", "--",
        $remotePackagePath,
        $requestPath
    ) | Out-Null

    Invoke-Native git @(
        "-C", $worktree,
        "commit",
        "-m",
        "ci(repo-patcher): validate package $requestId"
    ) | Out-Null

    Invoke-Native git @(
        "-C", $worktree,
        "push",
        "--set-upstream",
        "origin",
        $branch
    ) | Out-Null

    $branchPushed = $true

    $deadline = [DateTime]::UtcNow.AddMinutes(5)

    while (-not $runId -and [DateTime]::UtcNow -lt $deadline) {
        Start-Sleep -Seconds 2

        $runsJson = Get-NativeText gh @(
            "run", "list",
            "--repo", $slug,
            "--workflow", $Workflow,
            "--branch", $branch,
            "--event", "push",
            "--limit", "20",
            "--json",
            "databaseId,headBranch,status,conclusion,createdAt,url"
        )

        $runs = @($runsJson | ConvertFrom-Json)

        $run = $runs |
            Where-Object { $_.headBranch -eq $branch } |
            Sort-Object createdAt -Descending |
            Select-Object -First 1

        if ($run) {
            $runId = [string] $run.databaseId
            Write-Host "GitHub Actions run: $($run.url)"
        }
    }

    if (-not $runId) {
        throw @"
No workflow run was found for branch:
  $branch

Confirm that the workflow is active and listens to:
  repo-patcher-validation/**
"@
    }

    & gh run watch $runId `
        --repo $slug `
        --exit-status

    $runExitCode = $LASTEXITCODE

    if (Test-Path -LiteralPath $artifactOutput) {
        Remove-Item `
            -LiteralPath $artifactOutput `
            -Recurse `
            -Force
    }

    New-Item `
        -ItemType Directory `
        -Path $artifactOutput `
        -Force | Out-Null

    & gh run download $runId `
        --repo $slug `
        -D $artifactOutput

    if ($LASTEXITCODE -ne 0) {
        Write-Warning "The validation artifact could not be downloaded."
    }
    else {
        Write-Host "Validation files: $artifactOutput"
    }

    if ($runExitCode -ne 0) {
        Write-Host ""
        Write-Host "Failed workflow log:"
        & gh run view $runId `
            --repo $slug `
            --log-failed
    }
}
finally {
    if ($worktreeCreated -and (Test-Path -LiteralPath $worktree)) {
        & git -C $Repo `
            worktree remove `
            --force `
            $worktree | Out-Null
    }

    if (-not $KeepBranch) {
        if ($branchPushed) {
            & git -C $Repo `
                push origin `
                --delete `
                $branch | Out-Null
        }

        & git -C $Repo `
            branch -D `
            $branch | Out-Null
    }
    else {
        Write-Host "Temporary branch retained: $branch"
    }
}

exit $runExitCode
