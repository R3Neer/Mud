param(
    [Parameter(Mandatory = $true)][string] $WorkerBaseUrl,
    [Parameter(Mandatory = $true)][string] $RequestId,
    [Parameter(Mandatory = $true)][string] $TargetSha,
    [Parameter(Mandatory = $true)][string] $PackageSha256,
    [Parameter(Mandatory = $true)][long] $PackageSize,
    [Parameter(Mandatory = $true)][bool] $TrustPlugin,
    [Parameter(Mandatory = $true)][ValidateSet("zip_base64", "logical_files")][string] $TransportKind,
    [Parameter(Mandatory = $true)][string] $PackageFile,
    [Parameter(Mandatory = $true)][string] $RequestFile,
    [Parameter(Mandatory = $true)][string] $MetadataFile
)

$ErrorActionPreference = "Stop"
$audience = "mud-repo-patcher-worker"
$base = [Uri]$WorkerBaseUrl
if ($base.Scheme -ne "https") {
    throw "WorkerBaseUrl must use HTTPS."
}
if (-not $env:ACTIONS_ID_TOKEN_REQUEST_URL -or -not $env:ACTIONS_ID_TOKEN_REQUEST_TOKEN) {
    throw "GitHub OIDC environment is unavailable."
}

$separator = if ($env:ACTIONS_ID_TOKEN_REQUEST_URL.Contains("?")) { "&" } else { "?" }
$oidcUri = "$($env:ACTIONS_ID_TOKEN_REQUEST_URL)$separator" +
    "audience=$([Uri]::EscapeDataString($audience))"
$oidc = Invoke-RestMethod -Method Get -Uri $oidcUri -Headers @{
    Authorization = "bearer $($env:ACTIONS_ID_TOKEN_REQUEST_TOKEN)"
}
if (-not $oidc.value) {
    throw "GitHub did not return an OIDC token."
}

$encodedRequest = [Uri]::EscapeDataString($RequestId)
$candidateUri = [Uri]::new($base, "/internal/v1/candidates/$encodedRequest")
$delays = @(0, 1, 2, 4, 8, 15)
$started = [DateTimeOffset]::UtcNow
$attempts = 0
$bytes = $null

$client = [System.Net.Http.HttpClient]::new()
try {
    $client.DefaultRequestHeaders.Authorization =
        [System.Net.Http.Headers.AuthenticationHeaderValue]::new("Bearer", [string]$oidc.value)
    $client.DefaultRequestHeaders.Add("X-Mud-Protocol", "mud-repo-patcher-validation/v1")
    foreach ($delay in $delays) {
        if ($delay -gt 0) {
            Start-Sleep -Seconds $delay
        }
        $attempts += 1
        $response = $client.GetAsync($candidateUri).GetAwaiter().GetResult()
        $body = $response.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult()
        if ([int]$response.StatusCode -eq 200) {
            $bytes = $body
            break
        }
        if ([int]$response.StatusCode -eq 409) {
            $detail = [Text.Encoding]::UTF8.GetString($body) | ConvertFrom-Json
            if ($detail.code -eq "dispatch_not_committed_yet" -and $detail.retryable -eq $true) {
                continue
            }
        }
        $text = [Text.Encoding]::UTF8.GetString($body)
        throw "Candidate download failed with HTTP $([int]$response.StatusCode): $text"
    }
}
finally {
    $client.Dispose()
}

if ($null -eq $bytes) {
    throw "Candidate was not available after the dispatch/D1 retry window."
}

$packageDirectory = Split-Path -Parent $PackageFile
$requestDirectory = Split-Path -Parent $RequestFile
$metadataDirectory = Split-Path -Parent $MetadataFile
@($packageDirectory, $requestDirectory, $metadataDirectory) |
    Where-Object { $_ } |
    Sort-Object -Unique |
    ForEach-Object { New-Item -ItemType Directory -Path $_ -Force | Out-Null }
[IO.File]::WriteAllBytes($PackageFile, $bytes)

$actualSize = (Get-Item -LiteralPath $PackageFile).Length
$actualHash = (Get-FileHash -LiteralPath $PackageFile -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualSize -ne $PackageSize -or $actualHash -ne $PackageSha256.ToLowerInvariant()) {
    throw "Candidate identity differs from workflow inputs."
}

$request = [ordered]@{
    protocol = "mud-repo-patcher-validation/v1"
    request_id = $RequestId
    repository = $env:GITHUB_REPOSITORY
    target_sha = $TargetSha.ToLowerInvariant()
    package_sha256 = $actualHash
    package_size = $actualSize
    trust_plugin = $TrustPlugin
    transport_kind = $TransportKind
}
$request | ConvertTo-Json -Compress |
    Set-Content -LiteralPath $RequestFile -Encoding utf8NoBOM

$completed = [DateTimeOffset]::UtcNow
[ordered]@{
    protocol = "mud-repo-patcher-download/v1"
    request_id = $RequestId
    attempts = $attempts
    started_at = $started.ToString("O")
    completed_at = $completed.ToString("O")
    elapsed_ms = [long]($completed - $started).TotalMilliseconds
    package_sha256 = $actualHash
    package_size = $actualSize
} | ConvertTo-Json | Set-Content -LiteralPath $MetadataFile -Encoding utf8NoBOM
