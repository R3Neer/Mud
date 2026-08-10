param(
    [string] $Workflow = ".github/workflows/validate-repo-patcher-remote.yml"
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$tooling = Join-Path $root "tooling\repo-patcher-validator"

python -m py_compile `
    (Join-Path $tooling "package_safety.py") `
    (Join-Path $tooling "runtime_probe.py") `
    (Join-Path $tooling "snapshot.py") `
    (Join-Path $tooling "validate_candidate.py") `
    (Join-Path $tooling "test_snapshot.py") `
    (Join-Path $tooling "test_validate_candidate.py") `
    (Join-Path $tooling "test_workflow_contract.py")
if ($LASTEXITCODE -ne 0) { throw "py_compile failed" }

python (Join-Path $tooling "test_snapshot.py")
if ($LASTEXITCODE -ne 0) { throw "snapshot tests failed" }
python (Join-Path $tooling "test_validate_candidate.py")
if ($LASTEXITCODE -ne 0) { throw "validator tests failed" }

$env:MUD_REMOTE_WORKFLOW_PATH = (Resolve-Path (Join-Path $root $Workflow)).Path
python (Join-Path $tooling "test_workflow_contract.py")
if ($LASTEXITCODE -ne 0) { throw "workflow contract tests failed" }
