from __future__ import annotations

import argparse
from pathlib import Path

from .core import ExportError, build_export, load_config, options_from_profile, write_export
from tooling.cli_support import (
    CommandHelp,
    HelpCatalogue,
    HelpItem,
    MudArgumentParser,
    add_presentation_arguments,
    failure,
    parse_cli,
)


DEFAULT_CONFIG = Path(__file__).with_name("profiles.toml")


def _common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path, help="Vault root (overrides the TOML configuration).")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="TOML configuration file.")


def _export_arguments(parser: argparse.ArgumentParser) -> None:
    _common_arguments(parser)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--profile", help="Configured profile.")
    source.add_argument("--files", nargs="+", metavar="PATH", help="Relative files, folders or patterns.")
    parser.add_argument("--name", help="Base export name.")
    parser.add_argument("--output", type=Path, help="Output path relative to the vault root.")
    parser.add_argument("--follow-links", action=argparse.BooleanOptionalAction, default=None)
    frontmatter = parser.add_mutually_exclusive_group()
    frontmatter.add_argument("--strip-frontmatter", dest="strip_frontmatter", action="store_true")
    frontmatter.add_argument("--keep-frontmatter", dest="strip_frontmatter", action="store_false")
    parser.set_defaults(strip_frontmatter=None)
    parser.add_argument("--source-markers", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--strict-links", action="store_true", default=None)
    parser.add_argument("--max-chars", type=int)
    parser.add_argument("--timestamp", action="store_true")
    parser.add_argument(
        "--zip-tree",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Create a ZIP with each source at its original relative path.",
    )


def make_parser() -> argparse.ArgumentParser:
    parser = MudArgumentParser(
        prog="python -m tooling.markdown_export",
        error_code="Mud.MarkdownExport.InvalidArguments",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    profiles = commands.add_parser("list-profiles")
    _common_arguments(profiles)

    export = commands.add_parser("export")
    _export_arguments(export)

    serve = commands.add_parser("serve")
    _common_arguments(serve)
    serve.add_argument("--port", type=int, default=8765)
    serve.add_argument("--no-browser", action="store_true")
    serve.add_argument(
        "--ready-json",
        action="store_true",
        help="Emit exactly one JSON readiness message for integrations.",
    )
    add_presentation_arguments(parser)
    return parser


def help_catalogue() -> HelpCatalogue:
    invocation = "python -m tooling.markdown_export"
    common = (
        HelpItem("--root PATH", "Override the configured vault root."),
        HelpItem("--config PATH", "Use an alternative TOML configuration."),
    )
    return HelpCatalogue(
        product="MUD MARKDOWN EXPORT",
        version="",
        description="Combine Markdown from an Obsidian vault into portable documents.",
        invocation=invocation,
        groups=("EXPORT", "INTERFACE"),
        commands=(
            CommandHelp("list-profiles", "EXPORT", "List configured profiles", "List the export profiles available in the selected configuration.", (f"{invocation} list-profiles [options]",), items=common),
            CommandHelp("export", "EXPORT", "Create a portable Markdown export", "Export selected Markdown as one document, several parts or a path-preserving ZIP.", (f"{invocation} export [--profile NAME | --files PATH ...] [options]",), items=common + (
                HelpItem("--profile NAME", "Use a configured selection profile."),
                HelpItem("--files PATH ...", "Select relative files, folders or patterns."),
                HelpItem("--output PATH", "Choose the output path within the vault root."),
                HelpItem("--follow-links", "Discover linked documents."),
                HelpItem("--no-follow-links", "Do not discover linked documents."),
                HelpItem("--strip-frontmatter", "Remove frontmatter from combined output."),
                HelpItem("--keep-frontmatter", "Preserve frontmatter in combined output."),
                HelpItem("--source-markers", "Add source markers to combined output."),
                HelpItem("--no-source-markers", "Do not add source markers."),
                HelpItem("--strict-links", "Fail on unresolved or unsupported links."),
                HelpItem("--max-chars N", "Split output between documents at the requested size."),
                HelpItem("--timestamp", "Append a timestamp to the output name."),
                HelpItem("--zip-tree", "Create a path-preserving ZIP."),
                HelpItem("--no-zip-tree", "Disable path-preserving ZIP output."),
            ), examples=(f"{invocation} export --profile specification",)),
            CommandHelp("serve", "INTERFACE", "Open the local web interface", "Serve the local export interface on 127.0.0.1.", (f"{invocation} serve [options]",), items=common + (
                HelpItem("--port PORT", "Listen on this local port; use 0 for an automatic port."),
                HelpItem("--no-browser", "Do not open the browser automatically."),
                HelpItem("--ready-json", "Write one machine-readable readiness object to stdout."),
            ), notes=("The server is local-only and must not be exposed as a network service.",)),
        ),
        usage=(f"{invocation} <command> [arguments] [options]", f"{invocation} <command> --help"),
        notes=(f"Run {invocation} <command> --help for detailed help.",),
        show_help_on_empty=True,
    )


def _configuration(args: argparse.Namespace):
    return load_config(args.config, args.root)


def _run_export(args: argparse.Namespace, ui) -> int:
    config = _configuration(args)
    profile_name = args.profile
    if args.files is None and profile_name is None:
        profile_name = config.default_profile
    output = args.output
    if output is not None and not output.is_absolute():
        output = config.root / output
    options = options_from_profile(
        config,
        profile_name or "",
        includes=args.files,
        name=args.name,
        output=output,
        follow_links=args.follow_links,
        strip_frontmatter=args.strip_frontmatter,
        source_markers=args.source_markers,
        strict_links=args.strict_links,
        max_chars=args.max_chars,
        timestamp=args.timestamp,
        zip_tree=args.zip_tree,
    )
    result = build_export(options)
    targets = write_export(options, result)
    ui.success(f"Exported {len(result.explicit_documents) + len(result.dependency_documents)} document(s).")
    for target in targets:
        ui.key_value("Output", target)
    for diagnostic in result.diagnostics:
        location = f" [{diagnostic.source}]" if diagnostic.source else ""
        message = f"{diagnostic.message}{location} [{diagnostic.code}]"
        if diagnostic.level.casefold() in {"error", "warning"}:
            ui.warning(message)
        else:
            ui.info(message)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = make_parser()
    parsed = parse_cli(
        parser,
        help_catalogue(),
        argv,
        executable_commands=("list-profiles", "export", "serve"),
    )
    if parsed.exit_code is not None:
        return parsed.exit_code
    args = parsed.arguments
    assert args is not None
    try:
        if args.command == "list-profiles":
            config = _configuration(args)
            rows = []
            for name, profile in config.profiles.items():
                rows.append((name, "yes" if name == config.default_profile else "", profile.title))
            parsed.ui.table(("PROFILE", "DEFAULT", "TITLE"), rows)
            return 0
        if args.command == "export":
            return _run_export(args, parsed.ui)
        if args.command == "serve":
            from .web import serve

            config = _configuration(args)
            serve(
                config,
                port=args.port,
                open_browser=not args.no_browser,
                ready_json=args.ready_json,
                ui=parsed.ui,
            )
            return 0
    except (ExportError, OSError) as exc:
        return failure(
            parsed.ui,
            "The Markdown export command failed.",
            code="Mud.MarkdownExport.Failed",
            details=str(exc),
            hint=f"{parser.prog} --help",
            exit_code=2,
        )
    return failure(parsed.ui, "The command is unknown.", code="Mud.MarkdownExport.UnknownCommand", hint=f"{parser.prog} --help", exit_code=2)


if __name__ == "__main__":
    raise SystemExit(main())
