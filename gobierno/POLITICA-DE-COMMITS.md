---
title: Policy MUD commits
aliases:
  - Policy Git
tags:
  - mud/gobierno
  - mud/git
status: vigente
---

# Policy MUD commits

## Objective

The Git history should make it possible to trace the conceptual, regulatory and technical evolution of MUD. A commit represents a coherent unit that can be understood and reverted independently.

## Liability

Codex will be responsible for preparing and creating the commits for repository.

The author does not need to explicitly state “commit” after each task. When a change is requested:

1. This is complete within its scope.
2. It has been reviewed in line with its risk.
3. Do not include any unauthorised changes.
4. Keep the repository in a coherent state.

Codex must create the relevant commit before closing the task.

A commit will not be made when:

- The author has explicitly asked for this to remain unconfirmed.
- The work is incomplete or cannot be validated.
- There is a blocking issue that substantially alters the result.
- The diff includes work by others that cannot be reliably isolated.

In such cases, Codex will state what remains unconfirmed and why.

## Atomicity

Each commit must have a single main reason to exist.

A commit may modify several files when they are all part of the same decision, for example:

- Standard, example and conformance test of a characteristic.
- Decision and the relevant sections.
- Policy and persistent rules that implement it.

The following must not be mixed:

- Unrelated regulatory changes.
- Mass reformatting with semantic changes.
- Work by the author unrelated to the assignment.
-  Ordinary temporary files, builds, logs, caches, dumps or state Obsidian’s local data.

A document that is intentionally temporary may only be versioned under [[POLITICA-DE-ARCHIVOS-TEMPORALES| the policy of temporary files ]]. Its temporary nature does not exempt it from commit atomicity, nor does it convert ephemeral data into versionable material.

## Message format

First line:

```text
tipo(ámbito): resumen imperativo
```

Types:

| Type | Use |
| --- | --- |
| `spec` | Standard, grammar, semantics or conformance |
| `decision` | ADR or explicit change of address |
| `docs` | Informative documentation with no regulatory changes |
| `govern` | Editorial processes, Git or governance |
| `fix` | Correction of a error |
| `refactor` | Reorganisation without any change in meaning |
| `test` | Series or cases of conformance |
| `chore` | Infrastructure and maintenance |

Common areas:

```text
language
notation
lexicon
grammar
types
actions
waves
random
reachability
git
editorial
```

Examples:

```text
spec(types): define nominal equality for aliases
decision(language): require full MUD 1.0 specification first
govern(git): establish atomic commit policy
fix(waves): clarify binding lifetime after destruction
```

Summary:

- It is written in the present imperative.
- It does not end in point.
- Describes the result, not the generic activity.
- Avoid messages such as `changes`, `updates` or `work`.

## Commit body

This should be added when the reason is not obvious. Recommended structure:

```text
Context:
- ...

Changes:
- ...

Validation:
- ...

Open questions:
- ...
```

In the case of regulatory changes, the following shall be included, where applicable:

- Rules or anchors affected.
- Decision related.
- Compatibilidad.
- Closed or newly created questions.
- Tests for conformance.

## Temporary files gate

Before any commit, the following is executed:

```powershell
python gobierno/validate_temporaries.py
```

The printed inventory must be checked in full. If the `temporary-delete-when` condition for any document is already met, that document must be removed before the commit is finalised, unless the change itself explicitly modifies its cycle lifecycle. An expired `temporary-delete-after` date automatically blocks the commit.

## Preliminary process

Before creating a commit, Codex must:

1. Read the relevant instructions.
2. Check `git status`.
3. Identify previous or external files.
4. Check the diff.
5. Run `python gobierno/validate_temporaries.py` and carry out a semantic check of your entire inventory.
6. Run the other available validation checks.
7. Add only the files from the unit atomic file.
8. Review the staged diff.
9. Create the commit.
10. Confirm that the subsequent state is as expected.

## Branch main

The main local branch is called `main`.

As long as there is only local work and a single authoring workflow, commits can be made directly to `main`. When experimental changes, parallel implementation or external collaboration arise, thematic branches will be adopted.

## History rewrite

Codex must not:

- Execute `git reset --hard`.
- Force a push.
- Rewrite published commits.
- Create `commit --amend` for work that may belong to someone else.

A routine correction is recorded in a new commit. History clean-up prior to publication will only be carried out at the author’s explicit request and after the exact boundaries have been verified.

## Remote publication

This policy allows local commits, but not:

- Create remote repositories.
- Push.
- Open pull requests.
- Publish versions.

Such actions require an explicit request.

## Relation with future semantic changes

When repository contains `.mud` models, commits that modify semantics must include operations such as the following in the body:

```text
Operations:
- CREATE action::warfare.Recruit
- UPDATE rule::warfare.CanRecruit
- RETIRE construct::warfare.LegacyArmy
```

A pure query `READ` does not result in a commit.

