# Temporary Spanish-to-English migration

This directory temporarily integrates
[`R3Translate`](https://github.com/R3Neer/R3Translate) into Mud. It is not a new
normative authority and will not participate in the future migration of route
names. The minimum version is `v0.1.1`, which includes frontmatter lists and
multiline protections.

Mud's own CLIs first require `python -m pip install -r
tooling/requirements.txt`. R3Translate continues to be installed as an isolated
executable so that its dependency tree is not mixed with Mud's.

- `mud-es-en.toml` is the executable source for terms, protections, frontmatter,
  British English and Mud-specific findings.
- `render_glossary.py` generates the human-readable view of
  `notes/glosario-de-traduccion-es-en.md`, and `--check` prevents divergence.
- `check_migration.py` combines `r3translate check` with the existing editorial
  and temporality barriers.

Example using the representative README:

```powershell
python tooling/translation/render_glossary.py --check
python tooling/translation/check_migration.py
```

To compare a candidate with its source and detect altered links, identifiers or
protections:

```powershell
python tooling/translation/check_migration.py ruta/candidato.md --source ruta/original.md
```

If `r3translate` is not on `PATH`, use `--r3translate PATH` or the
`R3TRANSLATE` variable. The DeepL key is supplied exclusively as
`DEEPL_AUTH_KEY`; it is never written to this directory.

The profile and glossary will be removed together when their
`temporary-delete-when` condition is met.
