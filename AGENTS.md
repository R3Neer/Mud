# Operating instructions for the MUD repository

These instructions apply to the entire repository.

## Authority

- `specification/` will contain the MUD rules.
- `notes/` will contain analysis, planning, risks and decisions.
- `governance/` will contain editorial and version control processes.

## Normative snapshot

The normative documents and artefacts in `specification/` describe the current state for MUD within its scope. Before modifying them, MUD-EDIT-002 and MUD-EDIT-003 of `specification/00-convenciones-editoriales.md` must be applied in full.

In particular:

- The history of the introduction, amendment, replacement or withdrawal of a rule is not recorded within the body of the regulations; it is contained in ADR, Git and the metadata for traceability.
- Related decisions are recorded using `decisions:` and are not described as provenance within the body of `specification/`.
- An active question may be cited in the main text solely to highlight an uncertainty affecting the current state; it must also appear in `questions:`.
- A current decision must be integrated into any normative surface that has already been developed and whose remit covers its scope. If the canonical location does not yet exist, a temporary surface must not be created solely to accommodate it, but no existing surface may contradict it.
- If the change affects nominal resolution, MUD-EDIT-004 must also be applied and `specification/09-nombres-y-anclas.md` must be reviewed together with `specification/names/mud-nominal-hir.asdl`.

The mechanical barrier for MUD-EDIT-002 and question handling is executed using `python governance/validate_spec_editorial.py`. Any change affecting `specification/` or `notes/questions/` must pass this check before committing. If the barrier itself is modified, `python governance/test_validate_spec_editorial.py` is also executed.

## Temporary files

Documents that are intended to be temporary are governed by `governance/POLITICA-DE-ARCHIVOS-TEMPORALES.md`. Ordinary temporary files are not versioned.

Before creating any commit, you must run `python governance/validate_temporaries.py` and check the complete inventory of documents using `temporary: true`. If the `temporary-delete-when` condition for any document is already met, it must be removed before closing the commit, unless the change itself explicitly modifies its cycle lifespan.

Temporality is declared solely in the document’s frontmatter; `governance/temporales.base` is a derived view and not a separate record.

## Git

Before editing files, you must read and follow `governance/POLITICA-DE-COMMITS.md`.

After completing and validating a consistent working unit, Codex must:

1. Check the state and the diff.
2. Add only the files relating to the task.
3. Create an atomic commit in accordance with policy.
4. Check the resulting status.

You must not push or overwrite the history without an explicit request.

## Document publication

The publication and promotion of regulatory documents is governed by `governance/CICLO-DOCUMENTAL.md`.

Before marking a chapter as `vigente`, the publication process must be carried out and it must be checked that its content reflects only the current regulatory state within its scope.

## Remote changes via ChatGPT

When environment allows repository to be edited directly via GitHub, a branch, a pull request or a writable checkout, a standard Git workflow is preferred, involving an isolated candidate, validations, a thorough review of the diff, atomic commits and fast-forward publishing.

If a candidate fails at a specific layer, that layer must be corrected and the review must be repeated from the affected point. If `main` changes during the process, the reference is not forced: the new state is inspected and the candidate is reconstructed on the new basis.

## Questions

The opening, updating, splitting and closing of questions are governed by `governance/POLITICA-DE-PREGUNTAS.md`.

Closed questions must not remain in active indexes or in the frontmatter `questions` of specification. Their stable archive is retained as traceability and links to the decisions or evidence that resolved them.
