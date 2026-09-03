---
title: MUD commit policy
aliases:
  - Git policy
tags:
  - mud/gobierno
  - mud/git
status: current
---

# MUD commit policy

## Aim

Git history must allow MUD's conceptual, normative and technical evolution to
be reconstructed. A commit represents a coherent unit that can be understood
and reverted independently.

## Responsibility

Codex is responsible for preparing and creating repository commits.

The author need not explicitly say "make a commit" after every task. When a
requested change:

1. Is complete within its scope.
2. Has been reviewed in proportion to its risk.
3. Contains no unrelated changes.
4. Leaves the repository in a coherent state.

Codex must create the corresponding commit before closing the task.

No commit is made when:

- The author explicitly asks to leave the work uncommitted.
- The work is incomplete or cannot be validated.
- A blocking question would substantially change the result.
- The diff includes unrelated work that cannot safely be isolated.

In those cases, Codex reports what remains uncommitted and why.

## Atomicity

Every commit must have one main reason to exist.

A commit may modify several files when they all form part of the same decision,
for example:

- A rule, example and conformance test for a feature.
- A decision and the chapters it affects.
- A policy and the persistent rules that implement it.

The following must not be mixed:

- Unrelated normative changes.
- Bulk reformatting with semantic changes.
- Author work unrelated to the task.
- Ordinary ephemeral files, builds, logs, caches, dumps or local Obsidian state.

An intentionally temporary document may remain versioned only under the
[[POLITICA-DE-ARCHIVOS-TEMPORALES|temporary-file policy]]. Its temporariness
does not exempt it from commit atomicity or make ephemeral residue suitable for
version control.

## Message format

First line:

```text
type(scope): imperative summary
```

Types:

| Type | Use |
| --- | --- |
| `spec` | Rules, grammar, semantics or conformance |
| `decision` | ADR or explicit change of direction |
| `docs` | Informative documentation without a normative change |
| `govern` | Editorial, Git or governance processes |
| `fix` | Correction of an error |
| `refactor` | Reorganisation without a change of meaning |
| `test` | Suite or conformance cases |
| `chore` | Infrastructure and maintenance |

Common scopes:

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

The summary:

- Is written in the imperative present tense.
- Does not end with a full stop.
- Describes the result, not generic activity.
- Avoids messages such as `changes`, `updates` or `work`.

## Commit body

Add one when the reason is not self-evident. Recommended structure:

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

For normative changes, include where applicable:

- Affected rules or anchors.
- Related decision.
- Compatibility.
- Questions closed or created.
- Conformance tests.

## Temporary-file gate

Before every commit, run:

```powershell
python gobierno/validate_temporaries.py
```

Review the complete printed inventory. If any document's
`temporary-delete-when` condition is already met, delete it before closing the
commit unless the change itself explicitly modifies its lifecycle. An expired
`temporary-delete-after` date mechanically blocks the commit.

## Preparation process

Before creating a commit, Codex must:

1. Read the applicable instructions.
2. Review `git status`.
3. Identify pre-existing or unrelated files.
4. Inspect the diff.
5. Run `python gobierno/validate_temporaries.py` and semantically review its complete inventory.
6. Run the other available validations.
7. Add only the files in the atomic unit.
8. Review the staged diff.
9. Create the commit.
10. Confirm that the resulting state is as expected.

## Main branch

The local main branch is named `main`.

While work is local and there is a single authorship stream, commits may be
created directly on `main`. When experimental changes, parallel implementation
or external collaboration appear, topic branches are adopted.

## History rewriting

Codex must not:

- Run `git reset --hard`.
- Force-push.
- Rewrite published commits.
- Run `commit --amend` on work that may belong to someone else.

An ordinary correction is recorded in a new commit. History clean-up before
publication occurs only at the author's explicit request and after checking the
exact boundaries.

## Remote publication

This policy authorises local commits, but not:

- Creating remote repositories.
- Pushing.
- Opening pull requests.
- Publishing releases.

Those actions require an explicit request.

## Relationship with future semantic changes

When the repository contains `.mud` models, commits that change semantics must
add operations such as these to their body:

```text
Operations:
- CREATE action::warfare.Recruit
- UPDATE rule::warfare.CanRecruit
- RETIRE construct::warfare.LegacyArmy
```

A pure `READ` query does not produce a commit.
