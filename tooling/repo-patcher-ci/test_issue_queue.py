from __future__ import annotations

import base64
import hashlib
import io
import json
import unittest
import zipfile
from datetime import datetime, timedelta, timezone

import issue_queue as queue
import issue_transport as transport

REPOSITORY = "R3Neer/Mud"
ACTOR = "efferra"
STATE_ACTOR = "github-actions[bot]"
NOW = datetime(2026, 8, 7, 0, 0, tzinfo=timezone.utc)


def block(start: str, end: str, value: dict) -> str:
    return f"{start}\n```json\n{json.dumps(value, separators=(',', ':'))}\n```\n{end}\n"


def package_bytes() -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("patch.yaml", "schema: 1\nid: smoke\ntitle: Smoke\noperations:\n  - assert_contains:\n      path: AGENTS.md\n      text: MUD\n")
    return stream.getvalue()


def make_issue(number: int, created: str, *, actor: str = ACTOR, complete: bool = True):
    package = package_bytes()
    payload = base64.b64encode(package).decode("ascii")
    request_id = f"queue-{number}"
    request = {
        "protocol": transport.PROTOCOL_REQUEST,
        "request_id": request_id,
        "repository": REPOSITORY,
        "target_sha": "1" * 40,
        "package_sha256": hashlib.sha256(package).hexdigest(),
        "package_size": len(package),
        "encoding": "base64",
        "chunk_count": 1,
        "trust_plugin": False,
    }
    issue = {
        "number": number,
        "state": "open",
        "created_at": created,
        "body": block(transport.REQUEST_START, transport.REQUEST_END, request),
        "user": {"login": actor},
    }
    comments = []
    if complete:
        chunk = {
            "protocol": transport.PROTOCOL_CHUNK,
            "request_id": request_id,
            "index": 1,
            "count": 1,
            "payload": payload,
        }
        comments.append({
            "id": number * 10,
            "created_at": created,
            "body": block(transport.CHUNK_START, transport.CHUNK_END, chunk),
            "user": {"login": actor},
        })
    return issue, comments, request


def claim_comment(request_id: str, when: datetime, run_id: int = 1):
    value = {
        "protocol": queue.CLAIM_PROTOCOL,
        "request_id": request_id,
        "repository": REPOSITORY,
        "run_id": run_id,
    }
    return {
        "id": run_id,
        "created_at": when.isoformat().replace("+00:00", "Z"),
        "body": block(queue.CLAIM_START, queue.CLAIM_END, value),
        "user": {"login": STATE_ACTOR},
    }


def result_comment(request_id: str, when: datetime, run_id: int = 1):
    value = {
        "protocol": queue.RESULT_PROTOCOL,
        "request_id": request_id,
        "repository": REPOSITORY,
        "run_id": run_id,
        "conclusion": "success",
        "package_sha256": "2" * 64,
        "artifact_name": "artifact",
        "run_url": "https://example.invalid/run",
    }
    return {
        "id": run_id + 100,
        "created_at": when.isoformat().replace("+00:00", "Z"),
        "body": block(queue.RESULT_START, queue.RESULT_END, value),
        "user": {"login": STATE_ACTOR},
    }


class QueueTests(unittest.TestCase):
    def select(self, issues, comments):
        return queue.select_oldest_pending(
            issues,
            lambda number: comments[number],
            repository=REPOSITORY,
            allowed_actors=["R3Neer", ACTOR],
            state_actor=STATE_ACTOR,
            now=NOW,
        )

    def test_no_issues(self):
        self.assertIsNone(self.select([], {}))

    def test_complete_issue_is_selected(self):
        issue, comments, request = make_issue(3, "2026-08-06T20:00:00Z")
        selected = self.select([issue], {3: comments})
        self.assertEqual(selected["request"]["request_id"], request["request_id"])

    def test_oldest_complete_issue_wins(self):
        newer, newer_comments, _ = make_issue(5, "2026-08-06T21:00:00Z")
        older, older_comments, _ = make_issue(4, "2026-08-06T20:00:00Z")
        selected = self.select([newer, older], {4: older_comments, 5: newer_comments})
        self.assertEqual(selected["issue_number"], 4)

    def test_incomplete_issue_is_skipped(self):
        incomplete, incomplete_comments, _ = make_issue(3, "2026-08-06T20:00:00Z", complete=False)
        ready, ready_comments, _ = make_issue(4, "2026-08-06T21:00:00Z")
        selected = self.select([incomplete, ready], {3: incomplete_comments, 4: ready_comments})
        self.assertEqual(selected["issue_number"], 4)

    def test_unauthorized_issue_is_skipped(self):
        bad, bad_comments, _ = make_issue(3, "2026-08-06T20:00:00Z", actor="attacker")
        self.assertIsNone(self.select([bad], {3: bad_comments}))

    def test_pull_request_is_skipped(self):
        issue, comments, _ = make_issue(3, "2026-08-06T20:00:00Z")
        issue["pull_request"] = {"url": "x"}
        self.assertIsNone(self.select([issue], {3: comments}))

    def test_active_claim_is_skipped(self):
        issue, comments, request = make_issue(3, "2026-08-06T20:00:00Z")
        comments.append(claim_comment(request["request_id"], NOW - timedelta(minutes=30)))
        self.assertIsNone(self.select([issue], {3: comments}))

    def test_stale_claim_can_be_reclaimed(self):
        issue, comments, request = make_issue(3, "2026-08-06T20:00:00Z")
        comments.append(claim_comment(request["request_id"], NOW - timedelta(hours=3)))
        selected = self.select([issue], {3: comments})
        self.assertEqual(selected["issue_number"], 3)

    def test_result_is_never_reprocessed(self):
        issue, comments, request = make_issue(3, "2026-08-06T20:00:00Z")
        comments.append(result_comment(request["request_id"], NOW - timedelta(minutes=1)))
        self.assertIsNone(self.select([issue], {3: comments}))

    def test_fake_claim_from_untrusted_actor_is_ignored(self):
        issue, comments, request = make_issue(3, "2026-08-06T20:00:00Z")
        fake = claim_comment(request["request_id"], NOW - timedelta(minutes=1))
        fake["user"]["login"] = "attacker"
        comments.append(fake)
        selected = self.select([issue], {3: comments})
        self.assertEqual(selected["issue_number"], 3)

    def test_duplicate_complete_chunks_are_selected_then_rejected_by_transport(self):
        issue, comments, _ = make_issue(3, "2026-08-06T20:00:00Z")
        comments.append(dict(comments[0]))
        selected = self.select([issue], {3: comments})
        self.assertEqual(selected["issue_number"], 3)
        with self.assertRaises(transport.TransportError):
            transport.reconstruct_from_documents(
                issue,
                comments,
                expected_repository=REPOSITORY,
                allowed_actors=["R3Neer", ACTOR],
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
