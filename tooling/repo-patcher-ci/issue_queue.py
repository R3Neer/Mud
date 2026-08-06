from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

from issue_transport import (
    CHUNK_START,
    REQUEST_START,
    TransportError,
    _extract_json_block,
    _login,
    _require_mapping,
    _write_json,
    authorized_chunk_comments,
    parse_issue_request,
    reconstruct_from_documents,
)

CLAIM_PROTOCOL = "mud-repo-patcher-claim/v1"
RESULT_PROTOCOL = "mud-repo-patcher-result/v1"
CLAIM_START = "<!-- mud-repo-patcher-claim:v1 -->"
CLAIM_END = "<!-- /mud-repo-patcher-claim:v1 -->"
RESULT_START = "<!-- mud-repo-patcher-result:v1 -->"
RESULT_END = "<!-- /mud-repo-patcher-result:v1 -->"
CLAIM_KEYS = {"protocol", "request_id", "repository", "run_id"}
RESULT_KEYS = {
    "protocol",
    "request_id",
    "repository",
    "run_id",
    "conclusion",
    "package_sha256",
    "artifact_name",
    "run_url",
}
DEFAULT_STALE_CLAIM_SECONDS = 7_200


class QueueError(ValueError):
    pass


def _api_request_json(
    method: str,
    url: str,
    token: str,
    payload: dict[str, Any] | None = None,
) -> Any:
    data = None
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "mud-repo-patcher-issue-queue/1",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise QueueError(f"GitHub API returned HTTP {exc.code}: {detail[:500]}.") from exc
    except urllib.error.URLError as exc:
        raise QueueError(f"GitHub API request failed: {exc.reason}.") from exc


def _repo_base(repository: str) -> str:
    parts = repository.split("/", 1)
    if len(parts) != 2 or not all(parts):
        raise QueueError("repository must use owner/name form.")
    quoted = "/".join(urllib.parse.quote(part, safe="") for part in parts)
    return f"https://api.github.com/repos/{quoted}"


def list_open_issues(repository: str, token: str) -> list[dict[str, Any]]:
    base = _repo_base(repository)
    issues: list[dict[str, Any]] = []
    page = 1
    while True:
        payload = _api_request_json(
            "GET",
            f"{base}/issues?state=open&sort=created&direction=asc&per_page=100&page={page}",
            token,
        )
        if not isinstance(payload, list):
            raise QueueError("GitHub API issues response is not a list.")
        issues.extend(_require_mapping(item, "issue") for item in payload)
        if len(payload) < 100:
            break
        page += 1
        if page > 100:
            raise QueueError("Issue pagination exceeded 10,000 issues.")
    return issues


def fetch_issue_comments(repository: str, issue_number: int, token: str) -> list[dict[str, Any]]:
    base = _repo_base(repository)
    comments: list[dict[str, Any]] = []
    page = 1
    while True:
        payload = _api_request_json(
            "GET",
            f"{base}/issues/{issue_number}/comments?per_page=100&page={page}",
            token,
        )
        if not isinstance(payload, list):
            raise QueueError("GitHub API comments response is not a list.")
        comments.extend(_require_mapping(item, "comment") for item in payload)
        if len(payload) < 100:
            break
        page += 1
        if page > 100:
            raise QueueError("Issue comment pagination exceeded 10,000 comments.")
    return comments


def post_issue_comment(repository: str, issue_number: int, token: str, body: str) -> dict[str, Any]:
    value = _api_request_json(
        "POST",
        f"{_repo_base(repository)}/issues/{issue_number}/comments",
        token,
        {"body": body},
    )
    return _require_mapping(value, "created comment")


def close_issue(repository: str, issue_number: int, token: str) -> None:
    _api_request_json(
        "PATCH",
        f"{_repo_base(repository)}/issues/{issue_number}",
        token,
        {"state": "closed", "state_reason": "completed"},
    )


def _delimited_json(start: str, end: str, value: dict[str, Any]) -> str:
    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return f"{start}\n```json\n{encoded}\n```\n{end}\n"


def _parse_timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise QueueError("GitHub document has no valid created_at timestamp.")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise QueueError(f"Invalid GitHub timestamp: {value!r}.") from exc


def _state_documents(
    comments: Iterable[dict[str, Any]],
    *,
    state_actor: str,
    request_id: str,
) -> tuple[list[tuple[dict[str, Any], datetime]], list[tuple[dict[str, Any], datetime]]]:
    claims: list[tuple[dict[str, Any], datetime]] = []
    results: list[tuple[dict[str, Any], datetime]] = []
    for comment in comments:
        comment = _require_mapping(comment, "comment")
        try:
            author = _login(comment, "comment")
        except TransportError:
            continue
        if author.casefold() != state_actor.casefold():
            continue
        body = comment.get("body")
        if not isinstance(body, str):
            continue
        if CLAIM_START in body:
            value = _extract_json_block(body, CLAIM_START, CLAIM_END, "claim")
            if set(value) != CLAIM_KEYS or value.get("protocol") != CLAIM_PROTOCOL:
                raise QueueError("A trusted claim comment has an invalid schema.")
            if value.get("request_id") == request_id:
                claims.append((value, _parse_timestamp(comment.get("created_at"))))
        if RESULT_START in body:
            value = _extract_json_block(body, RESULT_START, RESULT_END, "result")
            if set(value) != RESULT_KEYS or value.get("protocol") != RESULT_PROTOCOL:
                raise QueueError("A trusted result comment has an invalid schema.")
            if value.get("request_id") == request_id:
                results.append((value, _parse_timestamp(comment.get("created_at"))))
    return claims, results


def candidate_state(
    issue: dict[str, Any],
    comments: Iterable[dict[str, Any]],
    *,
    repository: str,
    allowed_actors: Iterable[str],
    state_actor: str,
    now: datetime,
    stale_claim_seconds: int,
) -> dict[str, Any] | None:
    if issue.get("state") not in (None, "open"):
        return None
    if issue.get("pull_request") is not None:
        return None
    body = issue.get("body")
    if not isinstance(body, str) or REQUEST_START not in body:
        return None
    try:
        request, actor = parse_issue_request(
            issue,
            expected_repository=repository,
            allowed_actors=allowed_actors,
        )
    except TransportError:
        return None
    comments_list = [_require_mapping(item, "comment") for item in comments]
    claims, results = _state_documents(
        comments_list,
        state_actor=state_actor,
        request_id=request["request_id"],
    )
    if results:
        return None
    if claims:
        latest_claim = max(timestamp for _claim, timestamp in claims)
        age = (now - latest_claim.astimezone(timezone.utc)).total_seconds()
        if age < stale_claim_seconds:
            return None
    chunks = authorized_chunk_comments(comments_list, expected_actor=actor)
    if len(chunks) < request["chunk_count"]:
        return None
    number = issue.get("number")
    if not isinstance(number, int) or isinstance(number, bool):
        return None
    return {
        "issue": issue,
        "comments": comments_list,
        "issue_number": number,
        "request": request,
        "actor": actor,
    }


def select_oldest_pending(
    issues: Iterable[dict[str, Any]],
    comments_for_issue: Callable[[int], list[dict[str, Any]]],
    *,
    repository: str,
    allowed_actors: Iterable[str],
    state_actor: str,
    now: datetime,
    stale_claim_seconds: int = DEFAULT_STALE_CLAIM_SECONDS,
) -> dict[str, Any] | None:
    ordered = sorted(
        (_require_mapping(item, "issue") for item in issues),
        key=lambda item: (str(item.get("created_at", "")), int(item.get("number", 0) or 0)),
    )
    for issue in ordered:
        number = issue.get("number")
        if not isinstance(number, int) or isinstance(number, bool):
            continue
        candidate = candidate_state(
            issue,
            comments_for_issue(number),
            repository=repository,
            allowed_actors=allowed_actors,
            state_actor=state_actor,
            now=now,
            stale_claim_seconds=stale_claim_seconds,
        )
        if candidate is not None:
            return candidate
    return None


def _write_outputs(report: dict[str, Any]) -> None:
    output = os.environ.get("GITHUB_OUTPUT")
    if not output:
        return
    keys = (
        "found",
        "prepared",
        "source",
        "issue_number",
        "request_id",
        "target_sha",
        "package_sha256",
        "trust_plugin",
    )
    with Path(output).open("a", encoding="utf-8") as stream:
        for key in keys:
            value = report.get(key, "")
            if isinstance(value, bool):
                value = str(value).lower()
            stream.write(f"{key}={value}\n")


def claim_command(args: argparse.Namespace) -> int:
    token = os.environ.get(args.token_env)
    if not token:
        raise QueueError(f"Environment variable {args.token_env} is empty.")
    now = datetime.now(timezone.utc)
    issues = list_open_issues(args.repository, token)
    cache: dict[int, list[dict[str, Any]]] = {}

    def comments_for(number: int) -> list[dict[str, Any]]:
        if number not in cache:
            cache[number] = fetch_issue_comments(args.repository, number, token)
        return cache[number]

    candidate = select_oldest_pending(
        issues,
        comments_for,
        repository=args.repository,
        allowed_actors=args.allowed_actor,
        state_actor=args.state_actor,
        now=now,
        stale_claim_seconds=args.stale_claim_seconds,
    )
    queue_report_path = Path(args.output_queue_report)
    if candidate is None:
        report = {
            "found": False,
            "prepared": False,
            "source": "issue_queue",
            "issue_number": "",
            "request_id": "",
            "target_sha": "",
            "package_sha256": "",
            "trust_plugin": False,
            "error": "",
        }
        _write_json(queue_report_path, report)
        _write_outputs(report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    request = candidate["request"]
    issue_number = candidate["issue_number"]
    claim = {
        "protocol": CLAIM_PROTOCOL,
        "request_id": request["request_id"],
        "repository": args.repository,
        "run_id": args.run_id,
    }
    post_issue_comment(
        args.repository,
        issue_number,
        token,
        "RepoPatcher validation claimed by GitHub Actions.\n\n"
        + _delimited_json(CLAIM_START, CLAIM_END, claim),
    )

    report: dict[str, Any] = {
        "found": True,
        "prepared": False,
        "source": "issue_queue",
        "issue_number": issue_number,
        "request_id": request["request_id"],
        "target_sha": request["target_sha"],
        "package_sha256": request["package_sha256"],
        "trust_plugin": request["trust_plugin"],
        "actor": candidate["actor"],
        "run_id": args.run_id,
        "error": "",
    }
    try:
        package, normalized_request, transport_report = reconstruct_from_documents(
            candidate["issue"],
            candidate["comments"],
            expected_repository=args.repository,
            allowed_actors=args.allowed_actor,
        )
        Path(args.output_package).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output_package).write_bytes(package)
        _write_json(Path(args.output_request), normalized_request)
        _write_json(Path(args.output_transport_report), transport_report)
        report["prepared"] = True
    except (TransportError, OSError) as exc:
        report["error"] = str(exc)
    _write_json(queue_report_path, report)
    _write_outputs(report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def finalize_command(args: argparse.Namespace) -> int:
    token = os.environ.get(args.token_env)
    if not token:
        raise QueueError(f"Environment variable {args.token_env} is empty.")
    if args.conclusion not in {"success", "failure"}:
        raise QueueError("conclusion must be success or failure.")
    comments = fetch_issue_comments(args.repository, args.issue_number, token)
    _claims, results = _state_documents(
        comments,
        state_actor=args.state_actor,
        request_id=args.request_id,
    )
    duplicate = any(
        result.get("run_id") == args.run_id and result.get("conclusion") == args.conclusion
        for result, _timestamp in results
    )
    if not duplicate:
        result = {
            "protocol": RESULT_PROTOCOL,
            "request_id": args.request_id,
            "repository": args.repository,
            "run_id": args.run_id,
            "conclusion": args.conclusion,
            "package_sha256": args.package_sha256,
            "artifact_name": args.artifact_name,
            "run_url": args.run_url,
        }
        human = "passed" if args.conclusion == "success" else "failed"
        post_issue_comment(
            args.repository,
            args.issue_number,
            token,
            f"RepoPatcher validation {human}. See the linked run and artifact.\n\n"
            + _delimited_json(RESULT_START, RESULT_END, result),
        )
    close_issue(args.repository, args.issue_number, token)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scheduled MUD repo-patcher issue queue.")
    sub = parser.add_subparsers(dest="command", required=True)

    claim = sub.add_parser("claim", help="claim and reconstruct the oldest complete request")
    claim.add_argument("--repository", required=True)
    claim.add_argument("--allowed-actor", action="append", required=True)
    claim.add_argument("--state-actor", default="github-actions[bot]")
    claim.add_argument("--run-id", type=int, required=True)
    claim.add_argument("--token-env", default="GITHUB_TOKEN")
    claim.add_argument("--stale-claim-seconds", type=int, default=DEFAULT_STALE_CLAIM_SECONDS)
    claim.add_argument("--output-package", required=True)
    claim.add_argument("--output-request", required=True)
    claim.add_argument("--output-transport-report", required=True)
    claim.add_argument("--output-queue-report", required=True)
    claim.set_defaults(func=claim_command)

    finalize = sub.add_parser("finalize", help="publish a result and close its issue")
    finalize.add_argument("--repository", required=True)
    finalize.add_argument("--issue-number", type=int, required=True)
    finalize.add_argument("--request-id", required=True)
    finalize.add_argument("--run-id", type=int, required=True)
    finalize.add_argument("--conclusion", required=True)
    finalize.add_argument("--package-sha256", required=True)
    finalize.add_argument("--artifact-name", required=True)
    finalize.add_argument("--run-url", required=True)
    finalize.add_argument("--state-actor", default="github-actions[bot]")
    finalize.add_argument("--token-env", default="GITHUB_TOKEN")
    finalize.set_defaults(func=finalize_command)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        return args.func(args)
    except (QueueError, TransportError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
