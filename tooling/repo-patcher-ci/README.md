# repo-patcher CI relay v5

This directory supports two transports for
`.github/workflows/validate-repo-patcher.yml`:

1. manual `workflow_dispatch` using a temporary carrier branch;
2. GitHub Issues using Base64 comments and an `issue_comment` trigger.

Neither transport writes to `main`.

## Authorized issue actors

```text
R3Neer
efferra
```

The issue author, accepted chunk authors and trigger author must be the same
authorized actor. Public issue bodies must never contain secrets or confidential
data.

## Issue protocol

Request body:

`````markdown
<!-- mud-repo-patcher-request:v1 -->
```json
{"protocol":"mud-repo-patcher-issue/v1","request_id":"...","repository":"R3Neer/Mud","target_sha":"...","package_sha256":"...","package_size":123,"encoding":"base64","chunk_count":2,"trust_plugin":false}
```
<!-- /mud-repo-patcher-request:v1 -->
````

Chunk comment:

`````markdown
<!-- mud-repo-patcher-chunk:v1 -->
```json
{"protocol":"mud-repo-patcher-chunk/v1","request_id":"...","index":1,"count":2,"payload":"..."}
```
<!-- /mud-repo-patcher-chunk:v1 -->
````

Final trigger:

```text
/repo-patcher validate REQUEST_ID
```

`trust_plugin` must be a JSON boolean. It records explicit consent; it is not a
claim that the package actually contains a plugin.

## Encoding helper

```powershell
python "$Repo\tooling\repo-patcher-ci\issue_transport.py" encode `
    --package "C:\Path\candidate.zip" `
    --repository R3Neer/Mud `
    --target-sha 0123456789012345678901234567890123456789 `
    --request-id candidate-001 `
    --output-directory "$env:TEMP\candidate-001"
```

For an explicitly authorized plugin, add:

```text
--trust-plugin
```

## Plugin rules

`package_checks.py plugin` loads only the manifest through the vendored runtime.
It does not import or execute the plugin.

For a package with a plugin:

- `trust_plugin: false` fails with a specific diagnostic before `explain`;
- `trust_plugin: true` adds `--trust-plugin` to `explain`, both `check` calls and
  `apply`;
- the artifact records `plugin_present` and `plugin_authorized` separately.

For a declarative package, no prompt or plugin warning is shown.

## Validation sequence

```text
transport and actor validation
Base64, size and SHA-256 validation
ZIP safety and expansion limits
exact target checkout
vendored repo-patcher version
package-info
explain
check before apply
apply and declared generators/validators
git diff --check
check after apply
semantic changed_paths() == [] proof
status, diff and artifact collection
```

## Local verification

```powershell
& "$Repo\tooling\repo-patcher-ci\Test-GitHubWorkflow.ps1" `
    -Workflow "$Repo\.github\workflows\validate-repo-patcher.yml"
```

The command runs:

- 25 issue-transport tests;
- 2 runtime-backed package-inspection tests;
- 5 PowerShell consent cases;
- 12 workflow-contract tests;
- pinned `actionlint` with SHA-256 verification.

The authoritative runtime guide is `gobierno/USO-DE-REPO-PATCHER.md`, audited
against the vendored `repo-patcher 0.2.0` implementation.
