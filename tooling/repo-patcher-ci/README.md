# repo-patcher CI queue v6

This directory validates RepoPatcher packages through two transports:

1. a scheduled GitHub Issues queue;
2. manual `workflow_dispatch` using a temporary carrier branch.

Neither transport writes package changes to `main`.

## Scheduled issue queue

A request is complete when an open issue contains one request block and all of
its Base64 chunk comments. No final command comment is required.

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

The workflow polls every five minutes, selects the oldest complete request,
posts a claim, reconstructs the exact ZIP, validates it and closes the issue
with a machine-readable result. A claim becomes reclaimable after two hours if
no result was published.

Authorized request actors:

```text
R3Neer
efferra
```

State comments are trusted only when authored by `github-actions[bot]`.
Untrusted users cannot block the queue by imitating claim or result markers.

## Security boundary

The workflow uses three jobs:

- `prepare` has `issues: write`, but never executes RepoPatcher or package code;
- `validate` executes plugins only with explicit consent and has no issue-write
  permission or `GITHUB_TOKEN` environment variable;
- `finalize` has `issues: write`, but never executes package code.

The control-plane checkout and target checkout are separate. Validation helpers
come from the workflow commit; the RepoPatcher runtime and repository contents
come from the exact requested target SHA.

## Encoding helper

```powershell
python "$Repo\tooling\repo-patcher-ci\issue_transport.py" encode `
    --package "C:\Path\candidate.zip" `
    --repository R3Neer/Mud `
    --target-sha 0123456789012345678901234567890123456789 `
    --request-id candidate-001 `
    --output-directory "$env:TEMP\candidate-001"
```

For an explicitly authorized plugin, add `--trust-plugin`.

The helper produces `issue-body.md`, one or more `chunk-*.md` files and
`request.json`. It deliberately does not produce a trigger comment.

## Validation sequence

```text
queue authorization and persistent claim
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
persistent result and issue closure
```

## Plugin rules

`package_checks.py plugin` loads only `patch.yaml`; it does not import or execute
the plugin.

- `trust_plugin: false` rejects a plugin before `explain`;
- `trust_plugin: true` adds `--trust-plugin` to `explain`, both `check` calls and
  `apply`;
- artifacts record plugin presence and authorization separately.

## Local verification

```powershell
& "$Repo\tooling\repo-patcher-ci\Test-GitHubWorkflow.ps1" `
    -Workflow "$Repo\.github\workflows\validate-repo-patcher.yml"
```

The command compiles the queue and transport, runs their unit tests, runs the
runtime-backed package and plugin-consent tests, checks the workflow contract
and validates the YAML with pinned `actionlint`.

The authoritative runtime guide is `gobierno/USO-DE-REPO-PATCHER.md`, audited
against the vendored RepoPatcher 0.2.0 implementation.
