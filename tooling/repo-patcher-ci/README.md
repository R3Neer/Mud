# repo-patcher CI relay v4

This directory contains the validation tooling used by
`.github/workflows/validate-repo-patcher.yml`.

Version 4 supports two transports:

1. `workflow_dispatch` with a temporary carrier branch, retained from v3;
2. GitHub Issues with Base64 chunks and an `issue_comment` trigger.

The Issues relay exists so an authorized assistant can submit and iterate
candidate packages without permission to create branches or dispatch workflows.
It never writes to `main`.

## Authorized relay actors

The workflow currently authorizes the GitHub logins:

```text
R3Neer
efferra
```

`efferra` is the actor observed when the connected GitHub integration creates
issues and comments. The parser requires the issue author, every accepted chunk author,
and the trigger author to be the same authorized actor. Unrelated comments from
other users are ignored so they cannot invalidate a request.

## Public transport warning

Issue bodies and comments in this repository are public. Never place secrets,
tokens, credentials, private keys, confidential files, or personal data in a
relay package.

## Protocol

One issue represents exactly one validation request.

The issue body contains one delimited JSON request block:

`````markdown
<!-- mud-repo-patcher-request:v1 -->
```json
{"protocol":"mud-repo-patcher-issue/v1","request_id":"...","repository":"R3Neer/Mud","target_sha":"...","package_sha256":"...","package_size":123,"encoding":"base64","chunk_count":2,"allow_python_plugin":false}
```
<!-- /mud-repo-patcher-request:v1 -->
````

Each package chunk is a separate comment:

`````markdown
<!-- mud-repo-patcher-chunk:v1 -->
```json
{"protocol":"mud-repo-patcher-chunk/v1","request_id":"...","index":1,"count":2,"payload":"..."}
```
<!-- /mud-repo-patcher-chunk:v1 -->
````

After every chunk exists, add exactly one trigger comment:

```text
/repo-patcher validate REQUEST_ID
```

A second trigger on the same issue is rejected. Create a new issue for a new
candidate.

## Encoding helper

The parser can produce issue and comment bodies without publishing them:

```powershell
python "$Repo\tooling\repo-patcher-ci\issue_transport.py" encode `
    --package "C:\Path\candidate.zip" `
    --repository R3Neer/Mud `
    --target-sha 0123456789012345678901234567890123456789 `
    --request-id candidate-001 `
    --output-directory "$env:TEMP\candidate-001"
```

Default limits:

```text
package bytes:       1,048,576
Base64 chunk chars:     28,000
chunk comments:              64
ZIP entries:               4,096
uncompressed bytes:   33,554,432
member bytes:          8,388,608
```

## Validation performed

For a reconstructed package, the Windows runner verifies:

```text
transport schema and actors
Base64 integrity
package size
SHA-256
ZIP paths and expansion limits
exact target SHA
clean target checkout
vendored repo-patcher runtime
package-info
explain
check before apply
apply and declared generators/validators
git diff --check
check after apply
explicit second-plan no-op proof
final status and complete binary diff
```

The workflow uploads logs and available evidence even when a step fails.

## Python plugins

Issue requests default to:

```json
"allow_python_plugin": false
```

A package containing a Python plugin is rejected before `explain` unless the
request explicitly authorizes it. Authorized plugins are passed
`--trust-plugin` to all commands that load the plugin.

## Local tests

```powershell
& "$Repo\tooling\repo-patcher-ci\Test-GitHubWorkflow.ps1" `
    -Workflow "$Repo\.github\workflows\validate-repo-patcher.yml"
```

This compiles the parser and tests, runs 24 transport tests and 12 workflow-contract tests, downloads the pinned actionlint
binary, verifies its SHA-256, and validates the workflow.

## Documentation discrepancy

The vendored runtime at the v4 base commit reports `repo-patcher 0.2.0`, while
`gobierno/USO-DE-REPO-PATCHER.md` still describes 0.1.0. The workflow executes
the vendored runtime from the exact target SHA. This README records the
mismatch but does not silently rewrite the authoritative government document.
