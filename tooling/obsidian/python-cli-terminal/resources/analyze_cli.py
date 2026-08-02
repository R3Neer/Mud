from __future__ import annotations

import ast
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Option:
    names: list[str]
    help: str = ""
    metavar: str | None = None
    nargs: str | int | None = None
    value_type: str = "text"
    choices: list[str] = field(default_factory=list)
    takes_value: bool = True
    group: str | None = None

    def as_json(self) -> dict[str, Any]:
        return {
            "names": self.names,
            "help": self.help,
            "metavar": self.metavar,
            "nargs": self.nargs,
            "valueType": self.value_type,
            "choices": self.choices,
            "takesValue": self.takes_value,
            "group": self.group,
        }


@dataclass
class ParserModel:
    name: str
    help: str = ""
    options: list[Option] = field(default_factory=list)
    commands: list["ParserModel"] = field(default_factory=list)

    def as_json(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "help": self.help,
            "options": [option.as_json() for option in self.options],
            "commands": [command.as_json() for command in self.commands],
        }


@dataclass
class ParserRef:
    parser: ParserModel


@dataclass
class SubparsersRef:
    parser: ParserModel


@dataclass
class GroupRef:
    parser: ParserModel
    group: str


def literal(node: ast.AST | None) -> Any:
    if node is None:
        return None
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError):
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{literal(node.value)}.{node.attr}"
        return None


def keywords(call: ast.Call) -> dict[str, Any]:
    return {item.arg: literal(item.value) for item in call.keywords if item.arg is not None}


class ArgparseAnalyzer:
    def __init__(self, tree: ast.Module) -> None:
        self.tree = tree
        self.functions = {
            node.name: node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        self.root: ParserModel | None = None
        self.group_counter = 0
        self.active_calls: set[str] = set()

    def analyze(self) -> ParserModel | None:
        entry = "make_parser" if "make_parser" in self.functions else None
        if entry is None:
            candidates = [
                name
                for name, node in self.functions.items()
                if any(
                    isinstance(item, ast.Call)
                    and isinstance(item.func, ast.Attribute)
                    and item.func.attr == "parse_args"
                    for item in ast.walk(node)
                )
            ]
            entry = candidates[0] if candidates else None
        if entry is not None:
            self.run_function(entry, [])
        if self.root is None:
            self.run_statements(self.tree.body, {})
        return self.root

    def run_function(self, name: str, arguments: list[Any]) -> None:
        if name in self.active_calls:
            return
        function = self.functions.get(name)
        if function is None:
            return
        self.active_calls.add(name)
        environment: dict[str, Any] = {}
        for parameter, value in zip(function.args.args, arguments, strict=False):
            environment[parameter.arg] = value
        self.run_statements(function.body, environment)
        self.active_calls.remove(name)

    def run_statements(self, statements: list[ast.stmt], environment: dict[str, Any]) -> None:
        for statement in statements:
            if isinstance(statement, (ast.Assign, ast.AnnAssign)):
                target = statement.targets[0] if isinstance(statement, ast.Assign) else statement.target
                value = statement.value
                if isinstance(target, ast.Name) and value is not None:
                    resolved = self.evaluate(value, environment)
                    if resolved is not None:
                        environment[target.id] = resolved
            elif isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
                self.evaluate(statement.value, environment)
            elif isinstance(statement, ast.If):
                self.run_statements(statement.body, environment)

    def resolve(self, node: ast.AST, environment: dict[str, Any]) -> Any:
        if isinstance(node, ast.Name):
            return environment.get(node.id)
        return None

    def evaluate(self, node: ast.AST, environment: dict[str, Any]) -> Any:
        if not isinstance(node, ast.Call):
            return None
        if isinstance(node.func, ast.Name) and node.func.id in self.functions:
            arguments = [self.resolve(argument, environment) for argument in node.args]
            self.run_function(node.func.id, arguments)
            return None
        if isinstance(node.func, ast.Attribute):
            receiver = self.resolve(node.func.value, environment)
            method = node.func.attr
            if method == "ArgumentParser" and isinstance(node.func.value, ast.Name):
                model = ParserModel(name=str(keywords(node).get("prog") or "python"))
                self.root = self.root or model
                return ParserRef(model)
            if method == "add_subparsers" and isinstance(receiver, ParserRef):
                return SubparsersRef(receiver.parser)
            if method == "add_parser" and isinstance(receiver, SubparsersRef):
                name = str(literal(node.args[0])) if node.args else ""
                command = ParserModel(name=name, help=str(keywords(node).get("help") or ""))
                receiver.parser.commands.append(command)
                return ParserRef(command)
            if method == "add_mutually_exclusive_group" and isinstance(receiver, ParserRef):
                self.group_counter += 1
                return GroupRef(receiver.parser, f"group-{self.group_counter}")
            if method == "add_argument" and isinstance(receiver, (ParserRef, GroupRef)):
                self.add_argument(receiver, node)
                return None
        return None

    def add_argument(self, receiver: ParserRef | GroupRef, call: ast.Call) -> None:
        values = keywords(call)
        names = [value for argument in call.args if isinstance((value := literal(argument)), str)]
        if not names:
            return
        action = str(values.get("action") or "")
        if action.endswith("BooleanOptionalAction"):
            expanded: list[str] = []
            for name in names:
                expanded.append(name)
                if name.startswith("--") and not name.startswith("--no-"):
                    expanded.append(f"--no-{name[2:]}")
            names = expanded
        takes_value = action not in {"store_true", "store_false", "count"} and not action.endswith(
            "BooleanOptionalAction"
        )
        type_name = str(values.get("type") or "")
        value_type = "integer" if type_name == "int" else "path" if type_name.endswith("Path") else "text"
        choices_value = values.get("choices")
        choices = [str(value) for value in choices_value] if isinstance(choices_value, (list, tuple)) else []
        nargs_value = values.get("nargs")
        nargs = nargs_value if isinstance(nargs_value, (str, int)) else None
        receiver.parser.options.append(
            Option(
                names=names,
                help=str(values.get("help") or ""),
                metavar=str(values["metavar"]) if values.get("metavar") is not None else None,
                nargs=nargs,
                value_type=value_type,
                choices=choices,
                takes_value=takes_value,
                group=receiver.group if isinstance(receiver, GroupRef) else None,
            )
        )


def has_main_guard(tree: ast.Module) -> bool:
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        test = node.test
        if (
            isinstance(test, ast.Compare)
            and isinstance(test.left, ast.Name)
            and test.left.id == "__name__"
            and any(isinstance(value, ast.Constant) and value.value == "__main__" for value in test.comparators)
        ):
            return True
    return False


def call_names(tree: ast.Module) -> set[str]:
    result: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        try:
            result.add(ast.unparse(node.func))
        except AttributeError:
            pass
    return result


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: analyze_cli.py FILE", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        source = path.read_text(encoding="utf-8-sig")
        tree = ast.parse(source, filename=str(path))
    except (OSError, SyntaxError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        return 1

    calls = call_names(tree)
    frameworks: list[str] = []
    if any(name.startswith("argparse.") or name.endswith(".parse_args") for name in calls):
        frameworks.append("argparse")
    if any(name.startswith("click.") for name in calls):
        frameworks.append("click")
    if any(name.startswith("typer.") or name == "Typer" for name in calls):
        frameworks.append("typer")
    unit_test = "unittest.main" in calls
    parser = ArgparseAnalyzer(tree).analyze() if "argparse" in frameworks else None
    print(
        json.dumps(
            {
                "frameworks": frameworks,
                "hasMainGuard": has_main_guard(tree),
                "unittest": unit_test,
                "spec": parser.as_json() if parser is not None else None,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
