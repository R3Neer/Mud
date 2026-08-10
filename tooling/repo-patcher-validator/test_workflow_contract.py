from __future__ import annotations

import os
import re
import unittest
from pathlib import Path


WORKFLOW = Path(
    os.environ.get(
        "MUD_REMOTE_WORKFLOW_PATH",
        Path(__file__).resolve().parents[2] / ".github/workflows/validate-repo-patcher-remote.yml",
    )
).resolve()
TEXT = WORKFLOW.read_text(encoding="utf-8")


def job_block(name: str) -> str:
    match = re.search(rf"(?ms)^  {re.escape(name)}:\n(.*?)(?=^  [a-zA-Z0-9_-]+:\n|\Z)", TEXT)
    if match is None:
        raise AssertionError(f"job not found: {name}")
    return match.group(1)


class RemoteWorkflowContractTests(unittest.TestCase):
    def test_v1_dispatch_has_no_carrier_or_issue_inputs(self) -> None:
        for name in (
            "protocol", "request_id", "target_sha", "package_sha256", "package_size",
            "trust_plugin", "transport_kind",
        ):
            self.assertIn(f"      {name}:\n", TEXT)
        for forbidden in ("package_url", "package_ref", "package_path", "issue_number"):
            self.assertNotIn(f"      {forbidden}:\n", TEXT)

    def test_control_and_target_are_distinct_exact_checkouts(self) -> None:
        block = job_block("validate")
        self.assertIn("ref: ${{ github.workflow_sha }}", block)
        self.assertIn("path: control", block)
        self.assertIn("fetch-depth: 1", block)
        self.assertIn("ref: ${{ inputs.target_sha }}", block)
        self.assertIn("path: target-source", block)
        self.assertIn("fetch-depth: 0", block)
        self.assertEqual(block.count("persist-credentials: false"), 2)

    def test_candidate_job_has_oidc_but_no_write_permissions(self) -> None:
        block = job_block("validate")
        self.assertIn("contents: read", block)
        self.assertIn("id-token: write", block)
        self.assertNotIn("contents: write", block)
        self.assertNotIn("issues: write", block)
        self.assertNotIn("actions: write", block)

    def test_download_uses_oidc_and_no_package_url(self) -> None:
        block = job_block("validate")
        self.assertIn("Download-Candidate.ps1", block)
        self.assertIn("REPO_PATCHER_WORKER_URL", block)
        self.assertNotIn("PACKAGE_URL", block)

    def test_credentials_are_removed_before_harness(self) -> None:
        block = job_block("validate")
        scrub = block.index("Remove candidate credentials")
        harness = block.index("Run deterministic validator")
        self.assertLess(scrub, harness)
        for name in (
            "ACTIONS_ID_TOKEN_REQUEST_URL", "ACTIONS_ID_TOKEN_REQUEST_TOKEN",
            "GITHUB_TOKEN", "GH_TOKEN",
        ):
            self.assertIn(name, block[scrub:harness])

    def test_evidence_is_always_uploaded_before_conclusion(self) -> None:
        block = job_block("validate")
        upload = block.index("Upload validation evidence")
        enforce = block.index("Enforce validation conclusion")
        self.assertLess(upload, enforce)
        self.assertIn("if: always()", block[upload:enforce])
        self.assertIn("actions/upload-artifact@v7", block[upload:enforce])

    def test_v6_workflow_is_not_referenced_or_modified(self) -> None:
        self.assertNotIn("repo-patcher-ci", TEXT)
        self.assertNotIn("schedule:", TEXT)
        self.assertNotIn("issues:", TEXT)


if __name__ == "__main__":
    unittest.main(verbosity=2)
