from __future__ import annotations

import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from markdown_export.core import (
    VaultIndex,
    load_config,
    options_from_profile,
    select_paths,
)


class BundledProfileTests(unittest.TestCase):
    CONFIG = Path(__file__).resolve().parents[2] / "markdown-export.toml"

    def test_language_profile_grows_with_normative_directories(self) -> None:
        bundled = load_config(self.CONFIG)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            documents = {
                "specification/README.md",
                "specification/05-source-text.md",
                "specification/grammar/mud.ebnf",
                "specification/asdl/acciones.asdl",
                "specification/syntax/modelo.yaml",
                "notes/vision-and-scope.md",
                "notes/questions/README.md",
                "notes/questions/Q-001-g-grammar-and-line-breaks.md",
                "notes/questions/Q-002-m-exact-model-of-sequential-and-simultaneous-effects.md",
                "notes/decisions/README.md",
                "notes/decisions/ADR-054-lenguaje.md",
                "notes/decisions/ADR-055-nueva-decision.md",
                "notes/decisions/ADR-051-graph-future-semantics-and-reconstructable-information.md",
                "notes/decisions/ADR-052-pipelines-renderers-and-conformance.md",
                "notes/decisions/ADR-053-operador-semantico-and-flujo-de-autoria.md",
                "notes/risks-and-constraints.md",
                "tooling/README.md",
            }
            for relative in documents:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# {path.stem}\n", encoding="utf-8")

            config = replace(
                bundled,
                root=root,
                output_dir=root / "exports",
            )
            options = options_from_profile(config, "language")
            index = VaultIndex(root, options.excludes, options.source_languages)
            selected = {
                path.relative_to(root).as_posix()
                for path in select_paths(options, index)
            }

        self.assertIn("specification/05-source-text.md", selected)
        self.assertIn("specification/grammar/mud.ebnf", selected)
        self.assertIn("specification/asdl/acciones.asdl", selected)
        self.assertIn("specification/syntax/modelo.yaml", selected)
        self.assertIn("notes/vision-and-scope.md", selected)
        self.assertIn("notes/decisions/ADR-055-nueva-decision.md", selected)
        self.assertIn("notes/questions/README.md", selected)
        self.assertIn(
            "notes/questions/Q-002-m-exact-model-of-sequential-and-simultaneous-effects.md",
            selected,
        )
        self.assertNotIn(
            "notes/questions/Q-001-g-grammar-and-line-breaks.md",
            selected,
        )
        self.assertIn(
            "notes/decisions/ADR-051-graph-future-semantics-and-reconstructable-information.md",
            selected,
        )
        self.assertIn(
            "notes/decisions/ADR-052-pipelines-renderers-and-conformance.md",
            selected,
        )
        self.assertNotIn(
            "notes/decisions/ADR-053-operador-semantico-and-flujo-de-autoria.md",
            selected,
        )
        self.assertNotIn("notes/risks-and-constraints.md", selected)
        self.assertNotIn("tooling/README.md", selected)

    def test_decisions_profile_preserves_the_complete_question_history(self) -> None:
        bundled = load_config(self.CONFIG)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            documents = {
                "notes/decisions/README.md",
                "notes/decisions/ADR-062-lenguaje.md",
                "notes/questions/README.md",
                "notes/questions/Q-001-g-grammar-and-line-breaks.md",
                "notes/questions/Q-002-m-exact-model-of-sequential-and-simultaneous-effects.md",
                "specification/README.md",
            }
            for relative in documents:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# {path.stem}\n", encoding="utf-8")

            config = replace(bundled, root=root, output_dir=root / "exports")
            options = options_from_profile(config, "decisions")
            index = VaultIndex(root, options.excludes, options.source_languages)
            selected = {
                path.relative_to(root).as_posix()
                for path in select_paths(options, index)
            }

        self.assertIn("notes/questions/README.md", selected)
        self.assertIn(
            "notes/questions/Q-001-g-grammar-and-line-breaks.md",
            selected,
        )
        self.assertIn(
            "notes/questions/Q-002-m-exact-model-of-sequential-and-simultaneous-effects.md",
            selected,
        )
        self.assertNotIn("specification/README.md", selected)

    def test_current_profile_excludes_closed_questions(self) -> None:
        bundled = load_config(self.CONFIG)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            documents = {
                "notes/questions/README.md",
                "notes/questions/Q-001-g-grammar-and-line-breaks.md",
                "notes/questions/Q-002-m-exact-model-of-sequential-and-simultaneous-effects.md",
                "exports/current.md",
                "tooling/example/node_modules/dependency/README.md",
            }
            for relative in documents:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# {path.stem}\n", encoding="utf-8")

            config = replace(bundled, root=root, output_dir=root / "exports")
            options = options_from_profile(config, "current")
            index = VaultIndex(root, options.excludes, options.source_languages)
            selected = {
                path.relative_to(root).as_posix()
                for path in select_paths(options, index)
            }

        self.assertIn("notes/questions/README.md", selected)
        self.assertIn(
            "notes/questions/Q-002-m-exact-model-of-sequential-and-simultaneous-effects.md",
            selected,
        )
        self.assertNotIn(
            "notes/questions/Q-001-g-grammar-and-line-breaks.md",
            selected,
        )
        self.assertNotIn("exports/current.md", selected)
        self.assertNotIn(
            "tooling/example/node_modules/dependency/README.md",
            selected,
        )


if __name__ == "__main__":
    unittest.main()
