$ErrorActionPreference = "Stop"

$wheel = Join-Path $PSScriptRoot "vendor/pyyaml-6.0.3-cp313-cp313-win_amd64.whl"
$expectedSha256 = "79005a0d97d5ddabfeeea4cf676af11e647e41d81c9a7722a193022accdb6b7c"

if (-not (Test-Path -LiteralPath $wheel -PathType Leaf)) {
    throw "Missing pinned dependency wheel: $wheel"
}

$actualSha256 = (Get-FileHash -LiteralPath $wheel -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualSha256 -ne $expectedSha256) {
    throw "Pinned PyYAML wheel failed SHA-256 verification."
}

python -m pip install --disable-pip-version-check --no-index --no-deps $wheel
if ($LASTEXITCODE -ne 0) {
    throw "Installing the pinned PyYAML wheel failed with exit code $LASTEXITCODE."
}
