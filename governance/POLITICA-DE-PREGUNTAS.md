---
title: Policy MUD questions
aliases:
  - Cycle questions
tags:
  - mud/governance
  - mud/preguntas
status: current
---

# Policy MUD questions

Related decisions: [[POLITICA-DE-DECISIONES|Policy from MUD decisions ]].

## Purpose

A question identifies a specific uncertainty that may prevent the completion of an specification, an decision or an conformance test. It does not replace an decision nor does it keep a problem that has already been solved ‘open’ indefinitely.

## Autoridad

Questions are recorded in `notes/questions/`. They do not, in themselves, define semantics. An answer only becomes a MUD rule through an decision accepted in accordance with [[POLITICA-DE-DECISIONES]] and its incorporation into the relevant regulatory frameworks in accordance with [[CICLO-DOCUMENTAL]].

Each question has a stable file:

```text
notes/questions/Q-NNN-titulo-breve.md
```

The file is not moved when state is changed. Its fixed location prevents broken links and preserves traceability.

`notes/questions/README.md` lists only active questions.

## Identidad

- The identifier `Q-NNN` is unique and is not reused.
- The title may be clarified without changing the identifier when the investigation reveals genuine doubt.
- If a question contains independent uncertainties, it is split, and each new question links to its provenance.
- An decision can resolve several questions, and a single question may require several decisions.

## State from resolution

The field `resolved` is the only source of truth of the state in a question:

- `resolved: false` (`[ ]`): open; there is no sufficiently accepted answer.
- `resolved:` (`[-]`): partially resolved; the file lists exactly what is missing.
- `resolved: true` (`[x]`): closed; there is no uncertainty remaining within its scope.

Open and partially resolved questions are active. If a question is closed because it has been discarded, section `Resolución` explains the reason. If it has been superseded, `superseded-by` links to the questions that now cover its scope.

## Minimum content

Each file uses:

```yaml
---
id: Q-NNN
title:
priority: P0
opened: YYYY-MM-DD
resolved: false
closed:
decisions: []
affects: []
superseded-by: []
---
```

The priority is `P0`, `P1` or `P2` and determines the section of the active index; it is not part of the stable identity in the question.

`opened` contains, in `YYYY-MM-DD` format, the creation date of the question’s stable record and does not change throughout its cycle lifetime. For questions migrated from a previous database, `closed` may predate `opened` because it records the closure of the question, not the subsequent creation of its individual record.

`closed` remains blank whilst the query is active. When it changes to an inactive state, it contains the closing date in `YYYY-MM-DD` format. The `resolved` and `closed` fields must be updated in the same transaction.

And it contains, where applicable:

```markdown
# Q-NNN — Título

## Pregunta
## Contexto
## Ya decidido
## Pendiente
## Criterio de cierre
## Resolución
```

A partially resolved query does not list what has already been resolved as pending. Section `Pendiente` should make it possible to determine objectively when it can be closed.

### Closure criteria and evidence

The closure criteria used to mark a question as resolved have local identifiers `C1`, `C2`, … and describe verifiable conditions, not merely the existence of a linked decision. A question may retain additional explanatory text, but the set of identified criteria constitutes the list that must be met in order to close it.

A question `resolved: true` also contains `## Evidencia de cierre`. For each criterion, there is exactly one entry with the same identifier that cites the specific evidence: decisions, regulatory rules, mechanical devices, instances of conformance or an explicit rejection. The validator checks the structural correspondence between criteria and evidence; the human review semantics remains responsible for verifying that this evidence actually demonstrates the criterion.

Closed historical questions are migrated to this structure when this policy is adopted; evidence generated during the migration does not exempt one from reviewing its adequacy when the scope is revisited.

## References from specification

An active question may appear explicitly in the body of `specification/` when its existence is necessary to define which part of the current state has not yet been decided. This exception provides guidance on the scope current of the rule and does not grant semantics to the question.

Any reference to a part of the body in a question:

1.  must point to an active question;
2.  must state, in a local and precise manner, what remains open;
3.  must also appear in the frontmatter `questions:` of the document where the document has frontmatter;
4.  must not describe which decisions gave rise to, altered or left the question open;
5.  must be removed from the main text and the front matter once the question is closed or no longer relates to the document.

An active question that is only relevant for research, planning or a chapter that does not yet exist does not need to appear in an normative document other than its canonical location.

## Opening

Before creating a question, the following is checked:

1. The uncertainty has not already been resolved by specification or a current decision.
2. Please ensure this is not a duplicate of another question.
3. Ensure that your scope is small enough to elicit a verifiable response.
4. Identify the relevant sections, decisions or tests.
5. Identify viable alternatives where these are already known.

The new question is added to the active index and the frontmatter `questions` of each developed normative document whose current state is bounded by that uncertainty.

## Closure

A question is closed when:

1. All of its criteria `C1`, `C2`, … have identified evidence, and review semantics confirms that this evidence meets the criterion.
2. The set of criteria covers the entire scope of the question; a linked ADR on its own does not constitute closure.
3. The relevant regulatory and technical documents are updated.
4.  Withdrawn from `notes/questions/README.md`.
5. Remove from the frontmatter `questions` and from any open references or callouts in the specification.
6. This file contains the response, the closure date, the criteria, the evidence and the links from provenance.

Closing does not delete or recycle the file. Historical references may continue to link to it outside the regulatory framework current, but should not describe it as pending.

## Editorial checks

Before publishing an unit, the following is checked:

-  that every identifier included in `questions` corresponds to a active question;
- that any reference or regulatory warning regarding a pending issue should link to a active question;
- that every question cited in the body also appears in `questions:` where such frontmatter exists;
- that a closed question should not remain in the main text, the frontmatter or the index active section;
- that body references describe only the current uncertainty and not the decision-making history;
-  that `opened` contains a valid date and that `closed` is only empty for active questions, according to `resolved`;
- that decisions which introduce, answer or replace questions should maintain reciprocal links;
- that there are no partial states without an explicit listing of what remains to be done;
- that every closed question must meet criteria `C1`, `C2`, … and provide evidence that corresponds exactly to each criterion;
- that no piece of evidence should invoke a non-existent criterion;
-  that the concluding review should not be confused with a link to ADR being sufficient evidence in itself.

The active index is regenerated from the metadata and then validated against the root:

```powershell
python tooling/questions/validate_questions.py generate
python tooling/questions/validate_questions.py
```

## Relation with Git

The opening, splitting, replacement or closure of a query forms part of the same atomic commit as the decision or documentary change that gives rise to it, unless the query is identified during an independent audit.

