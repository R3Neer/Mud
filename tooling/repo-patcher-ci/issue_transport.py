from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import re
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

PROTOCOL_REQUEST = "mud-repo-patcher-issue/v1"
PROTOCOL_CHUNK = "mud-repo-patcher-chunk/v1"
REQUEST_START = "<!-- mud-repo-patcher-request:v1 -->"
REQUEST_END = "<!-- /mud-repo-patcher-request:v1 -->"
CHUNK_START = "<!-- mud-repo-patcher-chunk:v1 -->"
CHUNK_END = "<!-- /mud-repo-patcher-chunk:v1 -->"
TRIGGER_RE = re.compile(r"^/repo-patcher validate ([A-Za-z0-9][A-Za-z0-9._-]{0,79})$")
REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
BASE64_RE = re.compile(r"^[A-Za-z0-9+/]*={0,2}$")
DEFAULT_CHUNK_CHARS = 28_000
DEFAULT_MAX_PACKAGE_BYTES = 1_048_576
DEFAULT_MAX_CHUNKS = 64
DEFAULT_MAX_ENTRIES = 4_096
DEFAULT_MAX_UNCOMPRESSED_BYTES = 33_554_432
DEFAULT_MAX_MEMBER_BYTES = 8_388_608

REQUEST_KEYS = {
    "protocol",
    "request_id",
    "repository",
    "target_sha",
    "package_sha256",
    "package_size",
    "encoding",
    "chunk_count",
    "allow_python_plugin",
}
CHUNK_KEYS = {"protocol", "request_id", "index", "count", "payload"}


class TransportError(ValueError):
    pass


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TransportError(f"{label} must be a JSON object.")
    return value


def _require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise TransportError(f"{label} is missing keys: {', '.join(missing)}.")
    if extra:
        raise TransportError(f"{label} contains unknown keys: {', '.join(extra)}.")


def _extract_json_block(text: Any, start: str, end: str, label: str) -> dict[str, Any]:
    if not isinstance(text, str):
        raise TransportError(f"{label} body must be text.")
    pattern = re.compile(
        re.escape(start) + r"\s*```json\s*(.*?)\s*```\s*" + re.escape(end),
        re.DOTALL,
    )
    matches = pattern.findall(text)
    if len(matches) != 1:
        raise TransportError(f"{label} must contain exactly one delimited JSON block.")
    try:
        parsed = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise TransportError(f"{label} contains invalid JSON: {exc.msg}.") from exc
    return _require_mapping(parsed, label)


def _login(document: dict[str, Any], label: str) -> str:
    user = document.get("user")
    if not isinstance(user, dict) or not isinstance(user.get("login"), str):
        raise TransportError(f"{label} has no valid user.login.")
    return user["login"]


def _comment_id(comment: dict[str, Any]) -> int:
    value = comment.get("id")
    if not isinstance(value, int) or isinstance(value, bool):
        raise TransportError("A comment has no valid integer id.")
    return value


def _validate_request(
    request: dict[str, Any],
    *,
    expected_repository: str,
    max_package_bytes: int,
    max_chunks: int,
) -> dict[str, Any]:
    _require_exact_keys(request, REQUEST_KEYS, "request")
    if request["protocol"] != PROTOCOL_REQUEST:
        raise TransportError(f"Unsupported request protocol: {request['protocol']!r}.")
    request_id = request["request_id"]
    if not isinstance(request_id, str) or not REQUEST_ID_RE.fullmatch(request_id):
        raise TransportError("request_id has an invalid format.")
    repository = request["repository"]
    if not isinstance(repository, str) or repository.casefold() != expected_repository.casefold():
        raise TransportError(
            f"Request repository mismatch. Expected {expected_repository!r}, got {repository!r}."
        )
    target_sha = request["target_sha"]
    if not isinstance(target_sha, str) or not SHA_RE.fullmatch(target_sha):
        raise TransportError("target_sha must be a complete 40-character Git SHA.")
    package_sha256 = request["package_sha256"]
    if not isinstance(package_sha256, str) or not SHA256_RE.fullmatch(package_sha256):
        raise TransportError("package_sha256 must be a 64-character hexadecimal SHA-256.")
    package_size = request["package_size"]
    if (
        not isinstance(package_size, int)
        or isinstance(package_size, bool)
        or package_size <= 0
        or package_size > max_package_bytes
    ):
        raise TransportError(
            f"package_size must be between 1 and {max_package_bytes} bytes."
        )
    if request["encoding"] != "base64":
        raise TransportError("Only base64 encoding is supported.")
    chunk_count = request["chunk_count"]
    if (
        not isinstance(chunk_count, int)
        or isinstance(chunk_count, bool)
        or chunk_count < 1
        or chunk_count > max_chunks
    ):
        raise TransportError(f"chunk_count must be between 1 and {max_chunks}.")
    if not isinstance(request["allow_python_plugin"], bool):
        raise TransportError("allow_python_plugin must be a JSON boolean.")
    normalized = dict(request)
    normalized["target_sha"] = target_sha.lower()
    normalized["package_sha256"] = package_sha256.lower()
    normalized["repository"] = expected_repository
    return normalized


def _validate_chunk(chunk: dict[str, Any], *, request_id: str, chunk_count: int) -> dict[str, Any]:
    _require_exact_keys(chunk, CHUNK_KEYS, "chunk")
    if chunk["protocol"] != PROTOCOL_CHUNK:
        raise TransportError(f"Unsupported chunk protocol: {chunk['protocol']!r}.")
    if chunk["request_id"] != request_id:
        raise TransportError("A chunk belongs to a different request_id.")
    index = chunk["index"]
    count = chunk["count"]
    if not isinstance(index, int) or isinstance(index, bool) or not 1 <= index <= chunk_count:
        raise TransportError(f"Chunk index must be between 1 and {chunk_count}.")
    if count != chunk_count:
        raise TransportError("A chunk declares a count inconsistent with the request.")
    payload = chunk["payload"]
    if not isinstance(payload, str) or not payload or not BASE64_RE.fullmatch(payload):
        raise TransportError("A chunk contains invalid or whitespace-normalized Base64.")
    return chunk


def validate_zip_bytes(
    package: bytes,
    *,
    max_entries: int = DEFAULT_MAX_ENTRIES,
    max_uncompressed_bytes: int = DEFAULT_MAX_UNCOMPRESSED_BYTES,
    max_member_bytes: int = DEFAULT_MAX_MEMBER_BYTES,
) -> dict[str, int]:
    if not package:
        raise TransportError("The reconstructed package is empty.")
    if not zipfile.is_zipfile(io.BytesIO(package)):
        raise TransportError("The reconstructed package is not a valid ZIP archive.")
    total = 0
    names: set[str] = set()
    folded_names: set[str] = set()
    windows_reserved = {
        "con", "prn", "aux", "nul",
        *(f"com{index}" for index in range(1, 10)),
        *(f"lpt{index}" for index in range(1, 10)),
    }
    with zipfile.ZipFile(io.BytesIO(package), "r") as archive:
        infos = archive.infolist()
        if not infos:
            raise TransportError("The ZIP archive contains no entries.")
        if len(infos) > max_entries:
            raise TransportError(f"The ZIP archive exceeds {max_entries} entries.")
        for info in infos:
            raw_name = info.filename
            if "\x00" in raw_name:
                raise TransportError("The ZIP archive contains a NUL byte in an entry name.")
            normalized = raw_name.replace("\\", "/")
            path = PurePosixPath(normalized)
            if (
                normalized.startswith("/")
                or path.is_absolute()
                or not path.parts
                or any(part in {"", ".", ".."} for part in path.parts)
                or any(":" in part for part in path.parts)
                or any(part.endswith((" ", ".")) for part in path.parts)
            ):
                raise TransportError(f"Unsafe ZIP entry path: {raw_name!r}.")
            for part in path.parts:
                stem = part.split(".", 1)[0].casefold()
                if stem in windows_reserved:
                    raise TransportError(f"Windows-reserved ZIP entry path: {raw_name!r}.")
            canonical = path.as_posix()
            folded = canonical.casefold()
            if canonical in names or folded in folded_names:
                raise TransportError(f"Duplicate or case-colliding ZIP entry path: {canonical!r}.")
            names.add(canonical)
            folded_names.add(folded)
            if info.flag_bits & 0x1:
                raise TransportError(f"Encrypted ZIP entries are not allowed: {raw_name!r}.")
            unix_mode = (info.external_attr >> 16) & 0o170000
            if unix_mode and not (stat.S_ISREG(unix_mode) or stat.S_ISDIR(unix_mode)):
                raise TransportError(f"Special ZIP entry types are not allowed: {raw_name!r}.")
            if info.file_size > max_member_bytes:
                raise TransportError(
                    f"ZIP entry {raw_name!r} exceeds {max_member_bytes} uncompressed bytes."
                )
            total += info.file_size
            if total > max_uncompressed_bytes:
                raise TransportError(
                    f"The ZIP archive exceeds {max_uncompressed_bytes} uncompressed bytes."
                )
    return {"entry_count": len(names), "uncompressed_size": total}


def reconstruct_from_documents(
    issue: dict[str, Any],
    comments: Iterable[dict[str, Any]],
    *,
    expected_repository: str,
    expected_actor: str,
    allowed_actors: Iterable[str],
    trigger_comment_id: int,
    max_package_bytes: int = DEFAULT_MAX_PACKAGE_BYTES,
    max_chunks: int = DEFAULT_MAX_CHUNKS,
) -> tuple[bytes, dict[str, Any], dict[str, Any]]:
    issue = _require_mapping(issue, "issue")
    comments_list = [_require_mapping(item, "comment") for item in comments]
    allowed = {item.casefold() for item in allowed_actors}
    if expected_actor.casefold() not in allowed:
        raise TransportError(f"Actor {expected_actor!r} is not authorized for the relay.")
    issue_actor = _login(issue, "issue")
    if issue_actor.casefold() != expected_actor.casefold():
        raise TransportError("The issue author does not match the triggering actor.")
    request = _extract_json_block(issue.get("body"), REQUEST_START, REQUEST_END, "request")
    request = _validate_request(
        request,
        expected_repository=expected_repository,
        max_package_bytes=max_package_bytes,
        max_chunks=max_chunks,
    )
    request_id = request["request_id"]

    trigger_comments: list[dict[str, Any]] = []
    chunk_comments: list[dict[str, Any]] = []
    for comment in comments_list:
        body = comment.get("body")
        if not isinstance(body, str):
            continue
        try:
            author = _login(comment, "comment")
        except TransportError:
            continue
        if author.casefold() != expected_actor.casefold():
            # Public issues may contain unrelated or hostile comments. Only the
            # authorized request actor participates in the transport protocol.
            continue
        if TRIGGER_RE.fullmatch(body.strip()):
            trigger_comments.append(comment)
        if CHUNK_START in body:
            chunk_comments.append(comment)

    if len(trigger_comments) != 1:
        raise TransportError("The issue must contain exactly one relay validation trigger comment.")
    trigger = trigger_comments[0]
    if _comment_id(trigger) != trigger_comment_id:
        raise TransportError("The workflow event is not the unique trigger comment for this request.")
    if _login(trigger, "trigger comment").casefold() != expected_actor.casefold():
        raise TransportError("The trigger comment author does not match the authorized actor.")
    trigger_match = TRIGGER_RE.fullmatch(str(trigger.get("body", "")).strip())
    if trigger_match is None or trigger_match.group(1) != request_id:
        raise TransportError("The trigger comment request_id does not match the issue request.")

    if len(chunk_comments) != request["chunk_count"]:
        raise TransportError(
            f"Expected {request['chunk_count']} chunk comments, found {len(chunk_comments)}."
        )

    chunks: dict[int, str] = {}
    for comment in chunk_comments:
        if _login(comment, "chunk comment").casefold() != expected_actor.casefold():
            raise TransportError("A chunk comment author does not match the authorized actor.")
        chunk = _extract_json_block(comment.get("body"), CHUNK_START, CHUNK_END, "chunk")
        chunk = _validate_chunk(
            chunk,
            request_id=request_id,
            chunk_count=request["chunk_count"],
        )
        index = chunk["index"]
        if index in chunks:
            raise TransportError(f"Duplicate chunk index: {index}.")
        chunks[index] = chunk["payload"]

    expected_indexes = set(range(1, request["chunk_count"] + 1))
    if set(chunks) != expected_indexes:
        missing = sorted(expected_indexes - set(chunks))
        raise TransportError(f"Missing chunk indexes: {missing}.")

    encoded = "".join(chunks[index] for index in sorted(chunks))
    try:
        package = base64.b64decode(encoded, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise TransportError("The concatenated payload is not valid Base64.") from exc
    if len(package) != request["package_size"]:
        raise TransportError(
            f"Package size mismatch. Expected {request['package_size']}, got {len(package)}."
        )
    actual_hash = hashlib.sha256(package).hexdigest()
    if actual_hash != request["package_sha256"]:
        raise TransportError(
            f"Package SHA-256 mismatch. Expected {request['package_sha256']}, got {actual_hash}."
        )
    archive = validate_zip_bytes(package)
    report = {
        "protocol": request["protocol"],
        "request_id": request_id,
        "repository": expected_repository,
        "issue_number": issue.get("number"),
        "actor": expected_actor,
        "trigger_comment_id": trigger_comment_id,
        "target_sha": request["target_sha"],
        "package_sha256": actual_hash,
        "package_size": len(package),
        "chunk_count": request["chunk_count"],
        "allow_python_plugin": request["allow_python_plugin"],
        **archive,
    }
    return package, request, report


def _api_get_json(url: str, token: str) -> tuple[Any, dict[str, str]]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "mud-repo-patcher-issue-relay/1",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response), {key.lower(): value for key, value in response.headers.items()}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise TransportError(f"GitHub API returned HTTP {exc.code}: {detail[:500]}.") from exc
    except urllib.error.URLError as exc:
        raise TransportError(f"GitHub API request failed: {exc.reason}.") from exc


def fetch_issue_documents(repository: str, issue_number: int, token: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    quoted_repo = "/".join(urllib.parse.quote(part, safe="") for part in repository.split("/", 1))
    base = f"https://api.github.com/repos/{quoted_repo}/issues/{issue_number}"
    issue, _ = _api_get_json(base, token)
    issue = _require_mapping(issue, "issue")
    comments: list[dict[str, Any]] = []
    page = 1
    while True:
        payload, _ = _api_get_json(f"{base}/comments?per_page=100&page={page}", token)
        if not isinstance(payload, list):
            raise TransportError("GitHub API comments response is not a list.")
        comments.extend(_require_mapping(item, "comment") for item in payload)
        if len(payload) < 100:
            break
        page += 1
        if page > 100:
            raise TransportError("Issue comment pagination exceeded 10,000 comments.")
    return issue, comments


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_github_outputs(report: dict[str, Any]) -> None:
    output = os.environ.get("GITHUB_OUTPUT")
    if not output:
        return
    pairs = {
        "request_id": report["request_id"],
        "target_sha": report["target_sha"],
        "package_sha256": report["package_sha256"],
        "allow_python_plugin": str(report["allow_python_plugin"]).lower(),
        "actor": report["actor"],
        "issue_number": report["issue_number"],
    }
    with Path(output).open("a", encoding="utf-8") as stream:
        for key, value in pairs.items():
            stream.write(f"{key}={value}\n")


def reconstruct_command(args: argparse.Namespace) -> int:
    issue = json.loads(Path(args.issue_json).read_text(encoding="utf-8"))
    comments = json.loads(Path(args.comments_json).read_text(encoding="utf-8"))
    if not isinstance(comments, list):
        raise TransportError("comments-json must contain a JSON list.")
    package, request, report = reconstruct_from_documents(
        issue,
        comments,
        expected_repository=args.repository,
        expected_actor=args.expected_actor,
        allowed_actors=args.allowed_actor,
        trigger_comment_id=args.trigger_comment_id,
        max_package_bytes=args.max_package_bytes,
        max_chunks=args.max_chunks,
    )
    Path(args.output_package).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_package).write_bytes(package)
    _write_json(Path(args.output_request), request)
    _write_json(Path(args.output_report), report)
    _write_github_outputs(report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def fetch_command(args: argparse.Namespace) -> int:
    token = os.environ.get(args.token_env)
    if not token:
        raise TransportError(f"Environment variable {args.token_env} is empty.")
    issue, comments = fetch_issue_documents(args.repository, args.issue_number, token)
    package, request, report = reconstruct_from_documents(
        issue,
        comments,
        expected_repository=args.repository,
        expected_actor=args.expected_actor,
        allowed_actors=args.allowed_actor,
        trigger_comment_id=args.trigger_comment_id,
        max_package_bytes=args.max_package_bytes,
        max_chunks=args.max_chunks,
    )
    Path(args.output_package).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_package).write_bytes(package)
    _write_json(Path(args.output_request), request)
    _write_json(Path(args.output_report), report)
    _write_github_outputs(report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def _delimited_json(start: str, end: str, value: dict[str, Any]) -> str:
    return f"{start}\n```json\n{json.dumps(value, ensure_ascii=False, separators=(',', ':'))}\n```\n{end}\n"


def encode_command(args: argparse.Namespace) -> int:
    package_path = Path(args.package).expanduser().resolve()
    package = package_path.read_bytes()
    if len(package) > args.max_package_bytes:
        raise TransportError(
            f"Package has {len(package)} bytes; maximum is {args.max_package_bytes}."
        )
    validate_zip_bytes(package)
    if args.chunk_chars < 4 or args.chunk_chars % 4 != 0:
        raise TransportError("chunk-chars must be a positive multiple of four.")
    encoded = base64.b64encode(package).decode("ascii")
    chunks = [encoded[index : index + args.chunk_chars] for index in range(0, len(encoded), args.chunk_chars)]
    if not chunks:
        raise TransportError("Package produced no Base64 chunks.")
    if len(chunks) > args.max_chunks:
        raise TransportError(f"Package requires {len(chunks)} chunks; maximum is {args.max_chunks}.")
    request = {
        "protocol": PROTOCOL_REQUEST,
        "request_id": args.request_id,
        "repository": args.repository,
        "target_sha": args.target_sha.lower(),
        "package_sha256": hashlib.sha256(package).hexdigest(),
        "package_size": len(package),
        "encoding": "base64",
        "chunk_count": len(chunks),
        "allow_python_plugin": args.allow_python_plugin,
    }
    request = _validate_request(
        request,
        expected_repository=args.repository,
        max_package_bytes=args.max_package_bytes,
        max_chunks=args.max_chunks,
    )
    output = Path(args.output_directory).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / "issue-body.md").write_text(
        "Automated repo-patcher validation request. Public transport: do not include secrets.\n\n"
        + _delimited_json(REQUEST_START, REQUEST_END, request),
        encoding="utf-8",
    )
    for index, payload in enumerate(chunks, start=1):
        chunk = {
            "protocol": PROTOCOL_CHUNK,
            "request_id": args.request_id,
            "index": index,
            "count": len(chunks),
            "payload": payload,
        }
        (output / f"chunk-{index:03d}.md").write_text(
            _delimited_json(CHUNK_START, CHUNK_END, chunk), encoding="utf-8"
        )
    (output / "trigger-comment.md").write_text(
        f"/repo-patcher validate {args.request_id}\n", encoding="utf-8"
    )
    _write_json(output / "request.json", request)
    print(json.dumps({**request, "output_directory": str(output)}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MUD repo-patcher transport over GitHub Issues.")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_reconstruct_arguments(command: argparse.ArgumentParser) -> None:
        command.add_argument("--repository", required=True)
        command.add_argument("--expected-actor", required=True)
        command.add_argument("--allowed-actor", action="append", required=True)
        command.add_argument("--trigger-comment-id", type=int, required=True)
        command.add_argument("--output-package", required=True)
        command.add_argument("--output-request", required=True)
        command.add_argument("--output-report", required=True)
        command.add_argument("--max-package-bytes", type=int, default=DEFAULT_MAX_PACKAGE_BYTES)
        command.add_argument("--max-chunks", type=int, default=DEFAULT_MAX_CHUNKS)

    fetch = sub.add_parser("fetch", help="fetch an issue and reconstruct its package")
    add_reconstruct_arguments(fetch)
    fetch.add_argument("--issue-number", type=int, required=True)
    fetch.add_argument("--token-env", default="GITHUB_TOKEN")
    fetch.set_defaults(func=fetch_command)

    reconstruct = sub.add_parser("reconstruct", help="reconstruct from local issue/comment JSON")
    add_reconstruct_arguments(reconstruct)
    reconstruct.add_argument("--issue-json", required=True)
    reconstruct.add_argument("--comments-json", required=True)
    reconstruct.set_defaults(func=reconstruct_command)

    encode = sub.add_parser("encode", help="encode a package into issue and comment bodies")
    encode.add_argument("--package", required=True)
    encode.add_argument("--repository", required=True)
    encode.add_argument("--target-sha", required=True)
    encode.add_argument("--request-id", required=True)
    encode.add_argument("--output-directory", required=True)
    encode.add_argument("--chunk-chars", type=int, default=DEFAULT_CHUNK_CHARS)
    encode.add_argument("--max-package-bytes", type=int, default=DEFAULT_MAX_PACKAGE_BYTES)
    encode.add_argument("--max-chunks", type=int, default=DEFAULT_MAX_CHUNKS)
    encode.add_argument("--allow-python-plugin", action="store_true")
    encode.set_defaults(func=encode_command)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        return args.func(args)
    except (TransportError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
