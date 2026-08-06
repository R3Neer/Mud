from __future__ import annotations

import os
import re
import unittest
from pathlib import Path


WORKFLOW = Path(
    os.environ.get(
        "MUD_WORKFLOW_PATH",
        Path(__file__).with_name("validate-repo-patcher.yml"),
    )
).resolve()
TEXT = WORKFLOW.read_text(encoding="utf-8")


class WorkflowContractTests(unittest.TestCase):
    def test_dual_transport_triggers_exist(self) -> None:
        self.assertIn("  workflow_dispatch:\n", TEXT)
        self.assertIn("  issue_comment:\n    types: [created]", TEXT)

    def test_permissions_are_read_only_and_minimal(self) -> None:
        block = re.search(r"(?ms)^permissions:\n(.*?)(?=^[A-Za-z])", TEXT)
        self.assertIsNotNone(block)
        permissions = block.group(1)
        self.assertIn("contents: read", permissions)
        self.assertIn("issues: read", permissions)
        self.assertNotIn("write", permissions)

    def test_issue_relay_rejects_pull_requests_and_limits_actors(self) -> None:
        self.assertIn("github.event.issue.pull_request == null", TEXT)
        self.assertIn("startsWith(github.event.comment.body, '/repo-patcher validate ')", TEXT)
        self.assertIn("fromJSON('[\"R3Neer\",\"efferra\"]')", TEXT)

    def test_issue_transport_uses_event_identity(self) -> None:
        self.assertIn("EXPECTED_ACTOR: ${{ github.actor }}", TEXT)
        self.assertIn("TRIGGER_COMMENT_ID: ${{ github.event.comment.id }}", TEXT)
        self.assertIn('"--allowed-actor", "R3Neer"', TEXT)
        self.assertIn('"--allowed-actor", "efferra"', TEXT)

    def test_manual_dispatch_is_retained(self) -> None:
        for input_name in (
            "request_id",
            "package_ref",
            "package_path",
            "target_sha",
            "package_sha256",
            "trust_plugin",
        ):
            self.assertIn(f"      {input_name}:\n", TEXT)
        self.assertIn("Checkout manual package carrier", TEXT)

    def test_exact_target_and_package_identity_are_rechecked(self) -> None:
        self.assertIn("Checkout exact target commit", TEXT)
        self.assertIn("ref: ${{ steps.request.outputs.target_sha }}", TEXT)
        self.assertIn("Wrong target commit", TEXT)
        self.assertIn("Package identity changed after transport", TEXT)

    def test_vendored_runtime_is_used(self) -> None:
        self.assertIn(r"PYTHONPATH: ${{ github.workspace }}\tooling\repo-patcher-runtime", TEXT)
        self.assertIn('python -m repo_patcher --version', TEXT)
        self.assertNotIn("pip install repo-patcher", TEXT)

    def test_required_validation_sequence_is_present_and_ordered(self) -> None:
        markers = [
            'Invoke-Checked "package-info"',
            'Invoke-Checked "explain"',
            'Invoke-Checked "check before apply"',
            'Invoke-Checked "apply and declared validators"',
            'Invoke-Checked "explicit git diff --check"',
            'Invoke-Checked "check after apply"',
            'Invoke-Checked "prove second plan is a no-op"',
        ]
        positions = [TEXT.index(marker) for marker in markers]
        self.assertEqual(positions, sorted(positions))

    def test_idempotence_is_checked_semantically(self) -> None:
        self.assertIn("package_checks.py", TEXT)
        self.assertIn("idempotence --repo", TEXT)
        self.assertIn('Invoke-Checked "prove second plan is a no-op"', TEXT)

    def test_plugin_execution_requires_explicit_request_authorization(self) -> None:
        self.assertIn("trust_plugin", TEXT)
        self.assertIn("The package contains a Python plugin", TEXT)
        self.assertIn('$trustArguments = @("--trust-plugin")', TEXT)
        for command in ("explain", "check", "apply"):
            self.assertRegex(TEXT, rf"python -m repo_patcher {command}[^\n]*@trustArguments")
        self.assertIn("Plugin authorized:", TEXT)

    def test_artifact_is_uploaded_even_on_failure(self) -> None:
        self.assertIn("      - name: Upload logs and resulting diff", TEXT)
        self.assertIn("        if: always()", TEXT)
        self.assertIn("uses: actions/upload-artifact@v7", TEXT)
        self.assertIn("failure-summary.txt", TEXT)
        self.assertIn("transport-report.json", TEXT)
        self.assertIn('Join-Path $env:LOG_DIR "request.json"', TEXT)
        self.assertIn("validation-metadata.json", TEXT)

    def test_workflow_never_requests_write_permissions(self) -> None:
        forbidden = (
            "contents: write",
            "issues: write",
            "pull-requests: write",
            "actions: write",
            "id-token: write",
        )
        for item in forbidden:
            self.assertNotIn(item, TEXT)


if __name__ == "__main__":
    unittest.main(verbosity=2)
