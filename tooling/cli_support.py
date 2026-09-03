from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import NoReturn

try:
    from r3_cli import (
        CliError,
        CommandHelp,
        ConsoleUI,
        Diagnostic,
        HelpCatalogue,
        HelpItem,
        Level,
        add_output_arguments,
        resolve_help_request,
        validate_argparse_catalogue,
    )
except ImportError:
    print(
        "Mud tooling requires R3CLI 0.2.0. "
        "Install it with: python -m pip install -r tooling/requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(2) from None


@dataclass(frozen=True)
class ParsedCLI:
    arguments: argparse.Namespace | None
    ui: ConsoleUI
    exit_code: int | None = None


class MudArgumentParser(argparse.ArgumentParser):
    def __init__(
        self,
        *args: object,
        error_code: str = "Mud.Cli.InvalidArguments",
        **kwargs: object,
    ) -> None:
        kwargs.setdefault("add_help", False)
        super().__init__(*args, **kwargs)
        self.error_code = error_code

    def error(self, message: str) -> NoReturn:
        raise CliError(
            "The command-line arguments are invalid.",
            code=self.error_code,
            details=message,
            hint=f"{self.prog} --help",
        )


def add_presentation_arguments(parser: argparse.ArgumentParser) -> None:
    add_output_arguments(parser)


def _presentation(argv: Sequence[str]) -> tuple[str, bool]:
    colour = "auto"
    ascii_output = "--ascii" in argv
    for index, value in enumerate(argv):
        if value.startswith("--colour="):
            candidate = value.partition("=")[2]
            if candidate in {"auto", "always", "never"}:
                colour = candidate
        elif value == "--colour" and index + 1 < len(argv):
            candidate = argv[index + 1]
            if candidate in {"auto", "always", "never"}:
                colour = candidate
    if not ascii_output:
        encoding = sys.stdout.encoding or "utf-8"
        try:
            "═✓→•✗—".encode(encoding)
        except (LookupError, UnicodeEncodeError):
            ascii_output = True
    return colour, ascii_output


def parse_cli(
    parser: argparse.ArgumentParser,
    catalogue: HelpCatalogue,
    argv: Sequence[str] | None = None,
    *,
    executable_commands: Iterable[str] | None = None,
) -> ParsedCLI:
    values = tuple(sys.argv[1:] if argv is None else argv)
    colour, ascii_output = _presentation(values)
    ui = ConsoleUI(colour=colour, ascii=ascii_output)
    try:
        catalogue.validate(executable_commands)
        validate_argparse_catalogue(parser, catalogue)
        request = resolve_help_request(values, catalogue)
        if request is not None:
            ui.help(catalogue, request.command)
            return ParsedCLI(None, ui, 0)
        return ParsedCLI(parser.parse_args(values), ui)
    except CliError as exc:
        ui.error(exc)
        return ParsedCLI(None, ui, exc.exit_code)


def failure(
    ui: ConsoleUI,
    message: str,
    *,
    code: str,
    details: str | None = None,
    hint: str | None = None,
    exit_code: int = 1,
) -> int:
    ui.error(
        CliError(
            message,
            code=code,
            details=details,
            hint=hint,
            exit_code=exit_code,
        )
    )
    return exit_code


__all__ = [
    "CliError",
    "CommandHelp",
    "ConsoleUI",
    "Diagnostic",
    "HelpCatalogue",
    "HelpItem",
    "Level",
    "MudArgumentParser",
    "ParsedCLI",
    "add_presentation_arguments",
    "failure",
    "parse_cli",
]
