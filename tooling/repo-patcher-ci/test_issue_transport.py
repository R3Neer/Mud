from __future__ import annotations

import base64
import hashlib
import io
import json
import tempfile
import unittest
import zipfile
from copy import deepcopy
from pathlib import Path

import issue_transport as transport

ACTOR = "efferra"
REPOSITORY = "R3Neer/Mud"
TARGET = "1" * 40
REQUEST_ID = "relay-test-001"
TRIGGER_ID = 999


def make_zip(entries: dict[str, bytes] | None = None) -> bytes:
    entries = entries or {"patch.yaml": b"schema: 1\nid: test\ntitle: Test\noperations:\n  - assert_contains:\n      path: AGENTS.md\n      text: MUD\n"}
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in entries.items():
            archive.writestr(name, content)
    return stream.getvalue()


def json_block(start: str, end: str, value: dict) -> str:
    return f"{start}\n```json\n{json.dumps(value, separators=(',', ':'))}\n```\n{end}\n"


def make_documents(package: bytes | None = None, chunk_chars: int = 24):
    package = package if package is not None else make_zip()
    encoded = base64.b64encode(package).decode("ascii")
    chunks = [encoded[i : i + chunk_chars] for i in range(0, len(encoded), chunk_chars)]
    request = {
        "protocol": transport.PROTOCOL_REQUEST,
        "request_id": REQUEST_ID,
        "repository": REPOSITORY,
        "target_sha": TARGET,
        "package_sha256": hashlib.sha256(package).hexdigest(),
        "package_size": len(package),
        "encoding": "base64",
        "chunk_count": len(chunks),
        "trust_plugin": False,
    }
    issue = {
        "number": 7,
        "body": json_block(transport.REQUEST_START, transport.REQUEST_END, request),
        "user": {"login": ACTOR},
    }
    comments = []
    for index, payload in enumerate(chunks, 1):
        chunk = {
            "protocol": transport.PROTOCOL_CHUNK,
            "request_id": REQUEST_ID,
            "index": index,
            "count": len(chunks),
            "payload": payload,
        }
        comments.append(
            {
                "id": index,
                "body": json_block(transport.CHUNK_START, transport.CHUNK_END, chunk),
                "user": {"login": ACTOR},
            }
        )
    comments.append(
        {
            "id": TRIGGER_ID,
            "body": f"/repo-patcher validate {REQUEST_ID}",
            "user": {"login": ACTOR},
        }
    )
    return package, request, issue, comments


def reconstruct(issue, comments, **overrides):
    options = {
        "expected_repository": REPOSITORY,
        "expected_actor": ACTOR,
        "allowed_actors": ["R3Neer", ACTOR],
        "trigger_comment_id": TRIGGER_ID,
    }
    options.update(overrides)
    return transport.reconstruct_from_documents(issue, comments, **options)


class TransportTests(unittest.TestCase):
    def test_valid_single_chunk(self):
        package, _, issue, comments = make_documents(chunk_chars=100_000)
        rebuilt, _, report = reconstruct(issue, comments)
        self.assertEqual(rebuilt, package)
        self.assertEqual(report["package_sha256"], hashlib.sha256(package).hexdigest())

    def test_valid_multiple_chunks(self):
        package, _, issue, comments = make_documents(chunk_chars=20)
        rebuilt, _, report = reconstruct(issue, comments)
        self.assertEqual(rebuilt, package)
        self.assertGreater(report["chunk_count"], 1)

    def test_missing_chunk(self):
        _, _, issue, comments = make_documents(chunk_chars=20)
        comments.pop(0)
        with self.assertRaisesRegex(transport.TransportError, "Expected"):
            reconstruct(issue, comments)

    def test_duplicate_chunk(self):
        _, _, issue, comments = make_documents(chunk_chars=20)
        comments.insert(1, deepcopy(comments[0]))
        issue_request = transport._extract_json_block(issue["body"], transport.REQUEST_START, transport.REQUEST_END, "request")
        issue_request["chunk_count"] += 1
        issue["body"] = json_block(transport.REQUEST_START, transport.REQUEST_END, issue_request)
        with self.assertRaisesRegex(transport.TransportError, "inconsistent|Duplicate"):
            reconstruct(issue, comments)

    def test_index_out_of_range(self):
        _, _, issue, comments = make_documents(chunk_chars=100_000)
        chunk = transport._extract_json_block(comments[0]["body"], transport.CHUNK_START, transport.CHUNK_END, "chunk")
        chunk["index"] = 2
        comments[0]["body"] = json_block(transport.CHUNK_START, transport.CHUNK_END, chunk)
        with self.assertRaisesRegex(transport.TransportError, "index"):
            reconstruct(issue, comments)

    def test_count_inconsistent(self):
        _, _, issue, comments = make_documents(chunk_chars=100_000)
        chunk = transport._extract_json_block(comments[0]["body"], transport.CHUNK_START, transport.CHUNK_END, "chunk")
        chunk["count"] = 2
        comments[0]["body"] = json_block(transport.CHUNK_START, transport.CHUNK_END, chunk)
        with self.assertRaisesRegex(transport.TransportError, "count inconsistent"):
            reconstruct(issue, comments)

    def test_invalid_base64(self):
        _, _, issue, comments = make_documents(chunk_chars=100_000)
        chunk = transport._extract_json_block(comments[0]["body"], transport.CHUNK_START, transport.CHUNK_END, "chunk")
        chunk["payload"] = "not base64!"
        comments[0]["body"] = json_block(transport.CHUNK_START, transport.CHUNK_END, chunk)
        with self.assertRaisesRegex(transport.TransportError, "Base64"):
            reconstruct(issue, comments)

    def test_hash_mismatch(self):
        _, _, issue, comments = make_documents(chunk_chars=100_000)
        request = transport._extract_json_block(issue["body"], transport.REQUEST_START, transport.REQUEST_END, "request")
        request["package_sha256"] = "0" * 64
        issue["body"] = json_block(transport.REQUEST_START, transport.REQUEST_END, request)
        with self.assertRaisesRegex(transport.TransportError, "SHA-256 mismatch"):
            reconstruct(issue, comments)

    def test_size_mismatch(self):
        _, _, issue, comments = make_documents(chunk_chars=100_000)
        request = transport._extract_json_block(issue["body"], transport.REQUEST_START, transport.REQUEST_END, "request")
        request["package_size"] += 1
        issue["body"] = json_block(transport.REQUEST_START, transport.REQUEST_END, request)
        with self.assertRaisesRegex(transport.TransportError, "size mismatch"):
            reconstruct(issue, comments)

    def test_unauthorized_actor(self):
        _, _, issue, comments = make_documents(chunk_chars=100_000)
        with self.assertRaisesRegex(transport.TransportError, "not authorized"):
            reconstruct(issue, comments, expected_actor="attacker", allowed_actors=[ACTOR])

    def test_issue_actor_mismatch(self):
        _, _, issue, comments = make_documents(chunk_chars=100_000)
        issue["user"]["login"] = "attacker"
        with self.assertRaisesRegex(transport.TransportError, "issue author"):
            reconstruct(issue, comments)

    def test_mixed_request_id(self):
        _, _, issue, comments = make_documents(chunk_chars=100_000)
        chunk = transport._extract_json_block(comments[0]["body"], transport.CHUNK_START, transport.CHUNK_END, "chunk")
        chunk["request_id"] = "other"
        comments[0]["body"] = json_block(transport.CHUNK_START, transport.CHUNK_END, chunk)
        with self.assertRaisesRegex(transport.TransportError, "different request_id"):
            reconstruct(issue, comments)

    def test_extra_chunk_comment(self):
        _, _, issue, comments = make_documents(chunk_chars=100_000)
        comments.insert(0, deepcopy(comments[0]))
        with self.assertRaisesRegex(transport.TransportError, "Expected"):
            reconstruct(issue, comments)

    def test_unauthorized_noise_is_ignored(self):
        package, _, issue, comments = make_documents(chunk_chars=100_000)
        comments.insert(
            0,
            {
                "id": 900,
                "body": f"/repo-patcher validate {REQUEST_ID}",
                "user": {"login": "attacker"},
            },
        )
        comments.insert(
            1,
            {
                "id": 901,
                "body": comments[2]["body"],
                "user": {"login": "attacker"},
            },
        )
        rebuilt, _, _ = reconstruct(issue, comments)
        self.assertEqual(rebuilt, package)

    def test_empty_zip_rejected(self):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w"):
            pass
        package, _, issue, comments = make_documents(stream.getvalue(), chunk_chars=100_000)
        with self.assertRaisesRegex(transport.TransportError, "no entries"):
            reconstruct(issue, comments)

    def test_corrupt_zip_rejected(self):
        package, _, issue, comments = make_documents(b"not a zip", chunk_chars=100_000)
        with self.assertRaisesRegex(transport.TransportError, "valid ZIP"):
            reconstruct(issue, comments)

    def test_traversal_rejected(self):
        package = make_zip({"../escape.txt": b"x"})
        _, _, issue, comments = make_documents(package, chunk_chars=100_000)
        with self.assertRaisesRegex(transport.TransportError, "Unsafe ZIP"):
            reconstruct(issue, comments)

    def test_windows_reserved_name_rejected(self):
        package = make_zip({"files/CON.txt": b"x"})
        _, _, issue, comments = make_documents(package, chunk_chars=100_000)
        with self.assertRaisesRegex(transport.TransportError, "Windows-reserved"):
            reconstruct(issue, comments)

    def test_case_colliding_names_rejected(self):
        package = make_zip({"files/Name.txt": b"a", "files/name.txt": b"b"})
        _, _, issue, comments = make_documents(package, chunk_chars=100_000)
        with self.assertRaisesRegex(transport.TransportError, "case-colliding"):
            reconstruct(issue, comments)

    def test_package_over_limit(self):
        package, _, issue, comments = make_documents(chunk_chars=100_000)
        with self.assertRaisesRegex(transport.TransportError, "package_size"):
            reconstruct(issue, comments, max_package_bytes=len(package) - 1)

    def test_duplicate_trigger_rejected(self):
        _, _, issue, comments = make_documents(chunk_chars=100_000)
        comments.append(
            {"id": 1000, "body": f"/repo-patcher validate {REQUEST_ID}", "user": {"login": ACTOR}}
        )
        with self.assertRaisesRegex(transport.TransportError, "exactly one"):
            reconstruct(issue, comments)

    def test_unknown_request_key_rejected(self):
        _, _, issue, comments = make_documents(chunk_chars=100_000)
        request = transport._extract_json_block(issue["body"], transport.REQUEST_START, transport.REQUEST_END, "request")
        request["typo"] = True
        issue["body"] = json_block(transport.REQUEST_START, transport.REQUEST_END, request)
        with self.assertRaisesRegex(transport.TransportError, "unknown keys"):
            reconstruct(issue, comments)

    def test_trust_plugin_must_be_a_json_boolean(self):
        _, _, issue, comments = make_documents(chunk_chars=100_000)
        request = transport._extract_json_block(issue["body"], transport.REQUEST_START, transport.REQUEST_END, "request")
        request["trust_plugin"] = "true"
        issue["body"] = json_block(transport.REQUEST_START, transport.REQUEST_END, request)
        with self.assertRaisesRegex(transport.TransportError, "JSON boolean"):
            reconstruct(issue, comments)

    def test_same_request_can_be_reconstructed_again(self):
        package, _, issue, comments = make_documents(chunk_chars=100_000)
        first, _, _ = reconstruct(issue, comments)
        second, _, _ = reconstruct(issue, comments)
        self.assertEqual(first, package)
        self.assertEqual(second, package)

    def test_encode_round_trip(self):
        package = make_zip()
        with tempfile.TemporaryDirectory() as temp:
            package_path = Path(temp) / "package.zip"
            output = Path(temp) / "encoded"
            package_path.write_bytes(package)
            args = transport.build_parser().parse_args(
                [
                    "encode",
                    "--package",
                    str(package_path),
                    "--repository",
                    REPOSITORY,
                    "--target-sha",
                    TARGET,
                    "--request-id",
                    REQUEST_ID,
                    "--output-directory",
                    str(output),
                    "--chunk-chars",
                    "20",
                    "--trust-plugin",
                ]
            )
            self.assertEqual(args.func(args), 0)
            issue = {"number": 1, "body": (output / "issue-body.md").read_text(), "user": {"login": ACTOR}}
            comments = []
            for index, path in enumerate(sorted(output.glob("chunk-*.md")), 1):
                comments.append({"id": index, "body": path.read_text(), "user": {"login": ACTOR}})
            comments.append({"id": TRIGGER_ID, "body": (output / "trigger-comment.md").read_text(), "user": {"login": ACTOR}})
            rebuilt, request, report = reconstruct(issue, comments)
            self.assertEqual(rebuilt, package)
            self.assertIs(request["trust_plugin"], True)
            self.assertIs(report["trust_plugin"], True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
