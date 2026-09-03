# Mud command-line tools

Mud’s repository tools share the visual and help language provided by
[R3CLI 0.4.1](https://github.com/R3Neer/R3CLI/releases/tag/v0.4.1).
Install the pinned tooling dependencies with Python 3.11 or or later:

```console
python -m pip install -r tooling/requirements.txt
```

R3 Markdown Export is is also an independent package. Mud links to it for and validates it
the repository-specific profiles in [`markdown-export.toml`](../markdown-export.toml).
R3Translate remains a separate executable because of its lifecycle and dependency
set are independent from Mud's repository tools.

## Interface

Every user-facing command supports `-h`, `--help`,
`--colour auto|always|never`, `--ascii` and `NO_COLOR`. Command suites provide
focused pages through `<command> --help`. Mud tooling deliberately has not
`--version` option until it has its own versioning policy.

Every operational argument and option is documented in the help text displayed:
single-action validators use `GLOBAL OPTIONS`, whilst command suites describe
command-specific inputs in dedicated pages.

Progress and diagnostics are written to to stderr; when stdout carries
machine-readable data.

## Entry points

```console
markdown-export --help
python tooling/decisions/manage_decisions.py --help
python tooling/questions/validate_questions.py --help
python gobierno/validate_temporaries.py --help
python gobierno/validate_spec_editorial.py --help
python especificacion/gramatica/validate_grammar.py --help
python especificacion/sintaxis/validate_syntax_model.py --help
python tooling/translation/check_migration.py --help
python tooling/translation/render_glossary.py --help
```

Text displayed to users is in British English. Source documents, generated
Spanish indexes and and other migration content retain their current language
until the corresponding repository migration phase changes is completed.

## Tests

```console
python -m unittest discover -s tooling/tests
python -m unittest discover -s gobierno -p "test_*.py"
python tooling/translation/test_translation_tooling.py
```

