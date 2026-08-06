from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .engine import apply_plan, build_plan, package_digest
from .errors import RepoPatcherError
from .gitops import ensure_runtime, find_repo, head, origin_remote, status_porcelain
from .manifest import load_manifest
from .patch_source import open_patch_source
from .tutorial import TUTORIAL


class TutorialParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        print(f"\nERROR: {message}\n", file=sys.stderr)
        print("Ejecuta «repo-patcher tutorial» para ver una guía completa.", file=sys.stderr)
        raise SystemExit(2)


def _parser() -> argparse.ArgumentParser:
    parser = TutorialParser(
        prog="repo-patcher",
        description="Aplica paquetes de cambios de forma transaccional sobre repositorios Git.",
        epilog=(
            "PRIMER USO EN POWERSHELL\n"
            "  1. Entra en la repo:\n"
            "       Set-Location 'D:\\Ruta\\Repo'\n\n"
            "  2. Comprueba el paquete sin modificar archivos:\n"
            "       repo-patcher check 'C:\\Descargas\\patch.zip'\n\n"
            "  3. Aplícalo y deja que ejecute sus validadores:\n"
            "       repo-patcher apply 'C:\\Descargas\\patch.zip'\n\n"
            "  4. Revisa antes de crear un commit:\n"
            "       git status\n"
            "       git diff --stat\n"
            "       git diff\n\n"
            "Si no estás dentro de la repo, añade --repo 'D:\\Ruta\\Repo'.\n"
            "Si el paquete contiene un plugin Python, se pedirá confirmación antes de cargarlo.\n"
            "La herramienta no crea commits ni hace push.\n\n"
            "GUÍA COMPLETA\n"
            "  repo-patcher tutorial"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"repo-patcher {__version__}")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("tutorial", help="muestra una guía completa, especialmente para PowerShell")

    doctor = sub.add_parser("doctor", help="comprueba Python, Git y, opcionalmente, la repo")
    doctor.add_argument("--repo", type=Path, help="ruta de la repo; si se omite, se detecta desde el directorio actual")

    info = sub.add_parser("package-info", help="muestra identidad, compatibilidad y hash del paquete")
    info.add_argument("patch", type=Path, help="directorio o ZIP del paquete")

    for name, help_text in [
        ("explain", "explica qué pretende cambiar el paquete"),
        ("check", "comprueba el paquete sin modificar archivos"),
        ("apply", "aplica, valida y revierte automáticamente si falla"),
    ]:
        command = sub.add_parser(name, help=help_text)
        command.add_argument("patch", type=Path, help="directorio o ZIP del paquete")
        command.add_argument("--repo", type=Path, help="ruta de la repo; se autodetecta si se omite")
        command.add_argument(
            "--trust-plugin",
            action="store_true",
            help="autoriza un plugin Python sin pedir confirmación interactiva",
        )
        if name == "apply":
            command.add_argument("--emit-diff", type=Path, help="guarda también un diff Git tradicional")
    return parser


def _manifest_lines(manifest) -> list[str]:
    lines = [
        f"Patch: {manifest.patch_id}",
        f"Versión: {manifest.version}",
        f"Título: {manifest.title}",
    ]
    if manifest.description:
        lines.append(f"Descripción: {manifest.description}")
    if manifest.repository.names:
        lines.append(f"Repos admitidas: {', '.join(manifest.repository.names)}")
    if manifest.repository.remotes:
        lines.append(f"Remotes admitidos: {', '.join(manifest.repository.remotes)}")
    if manifest.compatibility.exact_heads:
        lines.append(f"HEAD exactos: {', '.join(manifest.compatibility.exact_heads)}")
    if manifest.compatibility.required_ancestor:
        lines.append(f"Antepasado requerido: {manifest.compatibility.required_ancestor}")
    lines.append(f"Plugin Python: {'sí' if manifest.plugin else 'no'}")
    lines.append(f"Operaciones declarativas: {len(manifest.operations)}")
    lines.append(f"Generadores: {len(manifest.generators)}")
    lines.append(f"Validadores: {len(manifest.validators)}")
    return lines


def _confirm_plugin() -> bool:
    print("\nADVERTENCIA DE SEGURIDAD")
    print("Este paquete contiene un plugin Python y puede ejecutar código con tus permisos.")
    print("Continúa únicamente si confías en quien preparó el paquete.")
    try:
        answer = input("Escribe SI para continuar: ").strip().upper()
    except EOFError:
        return False
    return answer == "SI"


def _print_plan(plan, repo: Path) -> None:
    print("\nREPO")
    print(f"  Ruta: {repo}")
    print(f"  HEAD: {head(repo)}")
    print(f"  Origin: {origin_remote(repo) or '(sin origin)'}")
    print("\nCAMBIOS PREVISTOS")
    paths = plan.context.changed_paths()
    if not paths:
        print("  Ninguno: el paquete parece estar ya aplicado.")
    else:
        for path in paths:
            relevant = [item for item in plan.context.changes if item.path == path]
            actions = ", ".join(dict.fromkeys(item.action for item in relevant)) or "modificar"
            print(f"  {actions}: {path}")
    if plan.context.notes:
        print("\nNOTAS DEL PAQUETE")
        for note in plan.context.notes:
            print(f"  - {note}")


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.command is None or args.command == "tutorial":
        print(TUTORIAL)
        return 0
    try:
        if args.command == "doctor":
            print("DIAGNÓSTICO")
            for line in ensure_runtime():
                print(f"  {line}")
            try:
                repo = find_repo(args.repo)
            except RepoPatcherError as exc:
                if args.repo is not None:
                    raise
                print(f"  Repo: no detectada ({exc})")
                return 0
            print(f"  Repo: {repo}")
            print(f"  HEAD: {head(repo)}")
            print(f"  Origin: {origin_remote(repo) or '(sin origin)'}")
            print(f"  Árbol limpio: {'sí' if not status_porcelain(repo).strip() else 'no'}")
            return 0

        with open_patch_source(args.patch) as patch_root:
            if args.command == "package-info":
                manifest = load_manifest(patch_root)
                print("INFORMACIÓN DEL PAQUETE")
                for line in _manifest_lines(manifest):
                    print(f"  {line}")
                print(f"  SHA-256 lógico: {package_digest(patch_root)}")
                return 0

            repo = find_repo(args.repo)
            preliminary_manifest = load_manifest(patch_root)
            if preliminary_manifest.plugin and not args.trust_plugin:
                if not sys.stdin.isatty() or not _confirm_plugin():
                    raise RepoPatcherError(
                        "Operación cancelada. El plugin no se ha cargado. "
                        "Para autorizarlo conscientemente usa --trust-plugin."
                    )
            require_clean = args.command == "apply"
            plan = build_plan(repo, patch_root, require_clean=require_clean)
            print("PAQUETE")
            for line in _manifest_lines(plan.manifest):
                print(f"  {line}")
            _print_plan(plan, repo)

            if args.command == "explain":
                print("\nEste comando no ha modificado ningún archivo.")
                return 0
            if args.command == "check":
                print("\nCOMPROBACIÓN CORRECTA")
                print("El paquete puede preparar sus cambios sobre esta repo sin escribir archivos.")
                print("Los generadores y validadores se ejecutarán durante apply.")
                return 0

            result = apply_plan(plan, repo, patch_root, emit_diff=args.emit_diff)
            if not result.changed_paths:
                print("\nSIN CAMBIOS")
                print("El paquete ya parece estar aplicado.")
                return 0
            print("\nPATCH APLICADO CORRECTAMENTE")
            print(f"  Archivos afectados: {len(result.changed_paths)}")
            print(f"  Generadores superados: {len(result.generators)}")
            print(f"  Validadores superados: {len(result.validators)}")
            if result.diff_path:
                print(f"  Diff guardado: {result.diff_path}")
            print("  Commit creado: no")
            print("\nSIGUIENTE PASO")
            print(f"  Set-Location {str(repo)!r}")
            print("  git status")
            print("  git diff --stat")
            print("  git diff")
            return 0
    except RepoPatcherError as exc:
        print(f"\nERROR\n{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
