from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tooling.cli_support import (  # noqa: E402
    HelpCatalogue,
    HelpItem,
    MudArgumentParser,
    add_presentation_arguments,
    failure,
    parse_cli,
)

PROFILE = Path(__file__).with_name("mud-es-en.toml")


def run(command: list[str], ui) -> int:
    ui.step(subprocess.list2cmdline(command))
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def run_translation(command: list[str], ui) -> int:
    ui.step(subprocess.list2cmdline(command))
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.stderr:
        sys.stderr.write(completed.stderr)
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return failure(
            ui,
            "R3Translate returned invalid JSON.",
            code="Mud.Translation.InvalidProviderOutput",
            details=str(exc),
            hint="check the installed R3Translate version",
            exit_code=completed.returncode or 2,
        )
    if not isinstance(payload, dict):
        return failure(ui, "R3Translate returned an invalid payload.", code="Mud.Translation.InvalidProviderOutput", hint="check the installed R3Translate version", exit_code=completed.returncode or 2)
    findings = payload.get("findings", [])
    if isinstance(findings, list):
        for item in findings:
            if not isinstance(item, dict):
                continue
            location = f"line {item['line']}: " if item.get("line") else ""
            code = item.get("code", "R3Translate.Finding")
            ui.warning(f"{location}{item.get('message', 'Translation finding.')} [{code}]")
    error = payload.get("error")
    if isinstance(error, dict):
        failure(
            ui,
            str(error.get("message", "R3Translate failed.")),
            code=str(error.get("code", "Mud.Translation.R3TranslateFailed")),
            details=str(error["details"]) if error.get("details") else None,
            hint=str(error["hint"]) if error.get("hint") else None,
            exit_code=completed.returncode or 2,
        )
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    invocation = "python tooling/translation/check_migration.py"
    catalogue = HelpCatalogue(
        product="MUD TRANSLATION CHECK",
        version="",
        description="Run Mud's temporary translation and editorial gates.",
        invocation=invocation,
        groups=(),
        commands=(),
        usage=(f"{invocation} [CANDIDATE] [--source PATH] [--r3translate PATH] [--colour MODE] [--ascii]",),
        global_items=(
            HelpItem("CANDIDATE", "Translated Markdown candidate to check. Default: README.md."),
            HelpItem("--source PATH", "Optional Spanish source paired with the translated candidate."),
            HelpItem("--r3translate PATH", "Explicit R3Translate executable. Otherwise use R3TRANSLATE or PATH."),
            HelpItem("--colour auto|always|never", "Control colour for human output. Default: auto; NO_COLOR disables it."),
            HelpItem("--ascii", "Use ASCII status symbols when Unicode is unsuitable."),
        ),
        notes=("The default candidate is README.md.", "R3Translate remains an isolated external executable."),
        show_help_on_empty=False,
    )
    parser = MudArgumentParser(prog=invocation, error_code="Mud.Translation.InvalidArguments")
    parser.add_argument("candidate", nargs="?", type=Path, default=Path("README.md"))
    parser.add_argument("--source", type=Path, help="Spanish source paired with the translated candidate.")
    parser.add_argument("--r3translate", help="Path to the r3translate executable.")
    add_presentation_arguments(parser)
    parsed = parse_cli(parser, catalogue, argv)
    if parsed.exit_code is not None:
        return parsed.exit_code
    arguments = parsed.arguments
    assert arguments is not None

    executable = arguments.r3translate or os.environ.get("R3TRANSLATE") or shutil.which("r3translate")
    if not executable:
        return failure(parsed.ui, "R3Translate was not found.", code="Mud.Translation.MissingR3Translate", hint=f"install R3Translate v0.1.1 or pass {invocation} --r3translate PATH", exit_code=2)

    candidate = arguments.candidate if arguments.candidate.is_absolute() else ROOT / arguments.candidate
    translation = [executable, "--format", "json", "check", str(candidate), "--profile", str(PROFILE)]
    if arguments.source:
        source = arguments.source if arguments.source.is_absolute() else ROOT / arguments.source
        translation.extend(["--source", str(source)])

    presentation = ["--colour", arguments.colour] + (["--ascii"] if arguments.ascii else [])
    commands = [
        [sys.executable, str(Path(__file__).with_name("render_glossary.py")), "--check", *presentation],
        [sys.executable, str(ROOT / "gobierno" / "validate_temporaries.py"), *presentation],
        [sys.executable, str(ROOT / "gobierno" / "validate_spec_editorial.py"), *presentation],
    ]
    result = run_translation(translation, parsed.ui)
    for command in commands:
        code = run(command, parsed.ui)
        if code and not result:
            result = code
    if result:
        return result
    parsed.ui.success("Profile, glossary, representative translation and editorial gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
