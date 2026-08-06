from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

WORKFLOW = Path(os.environ.get("MUD_WORKFLOW_PATH", Path(__file__).with_name("validate-repo-patcher.yml"))).resolve()
TEXT = WORKFLOW.read_text(encoding="utf-8")


def job_block(name: str) -> str:
    match = re.search(rf"(?ms)^  {re.escape(name)}:\n(.*?)(?=^  [a-zA-Z0-9_-]+:\n|\Z)", TEXT)
    if match is None:
        raise AssertionError(f"job not found: {name}")
    return match.group(1)


class WorkflowContractTests(unittest.TestCase):
    def test_pull_request_self_test_exists(self):
        self.assertIn("  pull_request:\n", TEXT)
        block = job_block("self_test")
        self.assertIn("github.event_name == 'pull_request'", block)
        self.assertIn("test_issue_queue.py", block)
        self.assertIn("actionlint_1.7.12_linux_amd64.tar.gz", block)
        self.assertIn("8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8", block)

    def test_schedule_and_manual_dispatch_exist(self):
        self.assertIn("  schedule:\n    - cron: \"*/5 * * * *\"", TEXT)
        self.assertIn("  workflow_dispatch:\n", TEXT)

    def test_issue_comment_trigger_is_removed(self):
        self.assertNotIn("issue_comment:", TEXT)
        self.assertNotIn("github.event.comment", TEXT)
        self.assertNotIn("/repo-patcher validate", TEXT)

    def test_queue_has_global_concurrency(self):
        self.assertIn("'repo-patcher-issue-queue'", TEXT)
        self.assertIn("cancel-in-progress: false", TEXT)

    def test_three_jobs_exist(self):
        for name in ("prepare", "validate", "finalize"):
            self.assertRegex(TEXT, rf"(?m)^  {name}:$")

    def test_prepare_has_issue_write_but_does_not_execute_repo_patcher(self):
        block = job_block("prepare")
        self.assertIn("issues: write", block)
        self.assertIn("contents: read", block)
        self.assertIn("issue_queue.py claim", block)
        self.assertNotIn("python -m repo_patcher apply", block)

    def test_validation_job_cannot_write_issues(self):
        block = job_block("validate")
        self.assertIn("contents: read", block)
        self.assertNotIn("issues: write", block)
        self.assertNotIn("GITHUB_TOKEN:", block)

    def test_finalize_has_issue_write_and_always_runs_for_found_request(self):
        block = job_block("finalize")
        self.assertIn("issues: write", block)
        self.assertIn("if: always() && needs.prepare.outputs.found == 'true'", block)
        self.assertIn("issue_queue.py finalize", block)

    def test_control_plane_is_separate_from_target_checkout(self):
        block = job_block("validate")
        self.assertIn("path: _control", block)
        self.assertIn("path: _target", block)
        self.assertIn("CONTROL_ROOT:", block)
        self.assertIn("TARGET_REPO:", block)

    def test_manual_dispatch_contract_is_retained(self):
        for input_name in ("request_id", "package_ref", "package_path", "target_sha", "package_sha256", "trust_plugin"):
            self.assertIn(f"      {input_name}:\n", TEXT)
        self.assertIn("Checkout manual package carrier", TEXT)

    def test_required_validation_sequence_is_ordered(self):
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

    def test_plugin_consent_reaches_all_loading_commands(self):
        block = job_block("validate")
        self.assertIn("The package contains a Python plugin", block)
        self.assertIn('$trustArguments = @("--trust-plugin")', block)
        for command in ("explain", "check", "apply"):
            self.assertRegex(block, rf"python -m repo_patcher {command}[^\n]*@trustArguments")

    def test_evidence_is_uploaded_on_validation_failure(self):
        block = job_block("validate")
        self.assertIn("if: always()", block)
        self.assertIn("actions/upload-artifact@v7", block)
        self.assertIn("failure-summary.txt", block)

    def test_workflow_level_permissions_are_empty(self):
        self.assertIn("permissions: {}", TEXT)
        validation = job_block("validate")
        self.assertNotIn("actions: write", validation)
        self.assertNotIn("contents: write", validation)
        self.assertNotIn("id-token: write", validation)


if __name__ == "__main__":
    unittest.main(verbosity=2)
