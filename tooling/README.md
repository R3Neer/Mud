# Mud command-line tooling

Mud's repository tools share the visual and help language provided by
[R3CLI 0.4.1](https://github.com/R3Neer/R3CLI/releases/tag/v0.4.1).
Install the pinned tooling dependencies with Python 3.11 or later:

```console
python -m pip install -r tooling/requirements.txt
```

R3 Markdown Export is also an independent package. Mud pins it for validating
the repository-specific profiles in [`markdown-export.toml`](../markdown-export.toml).
R3Translate remains a separate executable because its lifecycle and dependency
set are independent from Mud's repository tooling.

## Interface

Every human-facing command supports `-h`, `--help`,
`--colour auto|always|never`, `--ascii` and `NO_COLOR`. Command suites provide
focused pages through `<command> --help`. Mud tooling deliberately has no
`--version` option until it acquires an independent versioning policy.

Every operational argument and option is documented in the rendered help:
single-action validators use `GLOBAL OPTIONS`, whilst command suites describe
command-specific inputs in dedicated pages.

Progress and diagnostics are written to stderr when stdout carries
machine-readable data.

## Entry points

```console
markdown-export --help
python tooling/decisions/manage_decisions.py --help
python tooling/questions/validate_questions.py --help
python governance/validate_temporaries.py --help
python governance/validate_spec_editorial.py --help
python specification/grammar/validate_grammar.py --help
python specification/syntax/validate_syntax_model.py --help
```

Text displayed to users is in British English. Source documents, generated
migration indexes and other temporary migration content retain their current
language until the corresponding repository migration phase changes them.

## Tests

```console
python -m unittest discover -s tooling/tests
python -m unittest discover -s governance -p "test_*.py"
```
