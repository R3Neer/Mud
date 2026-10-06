---
title: MUD iterative consistency review policy
aliases:
  - Iterative consistency reviews
tags:
  - mud/governance
status: current
---

# MUD iterative consistency review policy

## Scope and obligation

Every task that changes the vault must complete an iterative consistency review
before it is declared finished. This applies to specification, decisions,
questions, governance, indexes, examples and technical artefacts. Read-only
tasks introduce no change requiring this gate.

Review each coherent working unit and its dependencies before committing it.
After the task's changes and corrections, perform a repository-wide review.
Its depth follows the change's risk, but its scope must include existing
surfaces that could contradict the resulting state, not just the edited files.

This policy complements [[COMMITS-POLICY]], [[DOCUMENT-LIFECYCLE]],
[[DECISIONS-POLICY]], [[QUESTIONS-POLICY]] and the applicable editorial rules.
Passing mechanical validators does not replace semantic review.

## Iterative procedure

1. Review the resulting state for inconsistencies. Check applicable decisions,
   normative prose and formulas, grammar and other mechanical contracts,
   examples and conformance evidence, dependencies, indexes, links, metadata,
   open questions and document authority. Include implementation/tooling claims
   where the change affects them.
2. At the end of every major review, write a new temporary Markdown document
   outside the repository. Record the iteration, reviewed scope and complete
   list of inconsistencies found. Each item identifies the affected surfaces
   and explains their contradiction or missing required integration.
3. Correct the listed inconsistencies within the authorised scope. Apply the
   existing decision/question process if a correction requires a semantic
   choice; do not silently invent behaviour to make the list empty. Run the
   relevant validations and commit only coherent, validated working units.
4. Review the resulting state again and write the next temporary list. Verify
   the previous corrections and search afresh for inconsistencies and their
   dependencies; do not merely mark the previous items as done.
5. Repeat corrections and reviews until the final repository-wide review
   produces an empty inconsistency list. Record that empty list explicitly,
   for example as `[]`, in its own temporary Markdown document.
6. Verify the empty final list, remove all ordinary review temporaries and
   confirm the resulting Git state. Report the review outcome and any actual
   limitation when closing the task.

There is no preset iteration count. An empty list means that the review found
no remaining inconsistency within its stated scope; it is not a proof that the
entire language or implementation is complete.

An explicitly delimited active question is not itself an inconsistency. A
contradiction, missing integration or unmet requirement must not be hidden by
reclassifying it as out of scope or deleting it from the list. If an item cannot
be resolved without user input or another genuine blocker, retain it and report
the task as incomplete. Do not claim that the final list is empty.

## Temporary documents and traceability

Review lists are ordinary ephemeral working documents under
[[TEMPORARY-FILES-POLICY]]. They must be created outside the repository, never
staged or committed, and deleted when the review cycle finishes. Ignoring a
review list inside the repository does not satisfy this placement requirement.
The exception for intentionally versioned temporary documents does not apply
to these lists.

Corrections and lasting decisions remain traceable through the normal
documents and atomic commits. Commit descriptions or the final report may
summarise iterations and validation outcomes without incorporating the
temporary lists into Git history.

## Completion and publication gate

The task cannot be declared complete, and a document cannot be promoted to
`current`, until the applicable final consistency list is empty and review
temporaries have been removed. If another substantive correction is made after
that review, repeat the affected review and the final repository-wide check.

Atomic commits may record consistent intermediate units and review
corrections. They do not waive the final task/publication gate. Repository-wide
review does not authorise unrelated edits, remote publication or history
rewriting.
