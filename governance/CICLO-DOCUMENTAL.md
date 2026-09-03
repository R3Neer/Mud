---
title: Document lifecycle by MUD
aliases:
  - Regulatory publication
tags:
  - mud/governance
  - mud/specification
status: current
---

# Document lifecycle by MUD

Management of outstanding issues: [[POLITICA-DE-PREGUNTAS|Policy regarding MUD queries ]].

## Purpose

MUD’s specification must maintain a strict separation between the current normative state, the provenance on decisions, and issues that are still open. This process defines how an normative document is prepared, reviewed and published without incorporating drafts, the decision-making history or provisional reasoning into the current standard.

The distinction between state current, decisions and outstanding issues is governed by MUD-EDIT-002 and MUD-EDIT-003 of [[specification/00-convenciones-editoriales]].

## Superficie normativa

Location: `specification/`.

May contain:

- Definitions.
- Identified regulatory rules.
- Formal notation.
- Informative examples and counterexamples.
- Clearly categorised theorems, lemmas, proofs and conjectures.
-  Explicit open questions when they define the current state.
- Metadata from traceability for decision-making and queries.
-  Criteria from conformance.

Must not contain:

- Conversation.
- Provisional reasoning presented as a rule.
- History of the introduction, amendment, replacement or withdrawal of rules as part of the regulatory process.
- Additive sections that amend a previous rule rather than overwriting its canonical form.
- Incomplete solutions presented as the standard.

##  States of a chapter

```text
esqueleto
→ borrador
→ propuesta
→ en-revisión
→ vigente
```

- **Skeleton**: structure without sufficient content.
- **Draft**: incomplete content that may change significantly.
- **Proposal**: semantics is a complete candidate for review.
- **In review**: the content is considered a candidate for publication and the publication process is carried out.
- **Current**: text accepted as the current standard.

An chapter `vigente` may contain open issues only if the affected feature is marked as outside the scope of MUD 1.0 or if the issue does not alter its meaning.

### Authority during the promotion

The location at `specification/` and `normative: true` indicates that a file belongs to normative surface, not that all of its content has already been approved. The authority of the chapter, as unit, appears upon reaching `status: vigente`.

Prior to `vigente`, an chapter may incorporate rules that already have authority through existing decisions and consistent regulatory mechanisms. That transcription does not grant the chapter the authority to change those rules, close questions or introduce an alternative semantics. If it diverges from an current decision, there is a documentary defect that blocks the promotion. If the text and the mechanical artefact diverge, the editorial rule MUD-EDIT-001 applies: the divergence must be explicitly resolved, and neither of the two interpretations is given tacit priority.

Therefore, promotion to `vigente` certifies the complete chapter; it is not the mechanism that gives retroactive effect to the decisions it had already documented.

### Integration of current decisions

The promotion of an decision does not require all future chapters of the specification to be created in advance. MUD-EDIT-003 applies:

1. The regulatory areas already developed, for which decision is responsible, are identified.
2. Either they are all updated in the same transaction, or a lock is explicitly set to prevent this from happening.
3. If the canonical location is still only a planned chapter, the ADR current retains interim authority over that part until it is formalised.
4. No existing document, including tables of contents and maps of future chapters, may contain a description that is inconsistent with current decision.
5. It is not considered sufficient to add an ‘update’ section at the end of a document: rule current must be incorporated into its canonical location.

## Publication workflow

The promotion of an chapter follows these steps:

1. The regulatory scope that chapter is intended to cover is identified.
2. A check is carried out to determine which current decisions and outstanding issues affect that scope.
3. Any issues preventing the expression of an unambiguous contract are resolved or recorded.
4.  The current state is drafted in a prescriptive style.
5. The notation is standardised with [[specification/03-notacion]].
6. Regulatory identifiers are added where applicable.
7. Examples, counterexamples and interactions are examined.
8.  Links, dependencies and metadata for traceability are being checked.
9. Any decision history or provenance that is not part of the state current is removed from the body.
10. Integration is checked across all the affected surfaces that have already been developed.
11. The publication run is being executed.
12.  The state is replaced and a atomic commit is created.

## Publication date

Before promoting an chapter to `vigente`, the following checks are carried out.

### Revisión semántica

- Correspondence between prose, formulas and examples.
- No undefined cases within the reported scope.
- Compatibility with current sections.
- Compatibility with applicable decisions currently in force.
- Distinction between a standard, a proposal and open question.
- Search for counterexamples.
- Check that no existing surface retains semantics as a replacement.

### Review formal

- Symbols defined before they are used.
- Well-formed judgements and rules.
- Explicit hypotheses.
- Quantifiers and unambiguous domains.
- Consistent names.

### Review editorial

- Application of MUD-EDIT-002: the body describes the state current and not the history of the decisions.
-  Absence of identifiers `D-NNN` or `ADR-NNN` used as provenance or justification in the text of the regulation.
-  Bodily questions limited to active questions, also recorded in `questions:`, and formulated as present-tense uncertainty.
- No additive update or removal sections.
- Apply MUD-EDIT-003 to all affected surfaces that have already been developed.
- Standardised drafting.
- Stable identifiers.
- Wiki links and references.
-  Correct frontmatter and state.
- Clearly marked illustrative examples.

### Review mechanical

- Resolvable links.
- Properly delimited Markdown and LaTeX.
- Grammar or verifiable outlines, where available.
-  A follow-up to conformance, updated where necessary.
- Mechanical barrier of MUD-EDIT-002 and the processing of queries via `python governance/validate_spec_editorial.py`; MUD-EDIT-003 also retains its review semantics in terms of affected surfaces.
- Application of MUD-EDIT-004 and consistency between chapter 09 and Nominal HIR where the change affects name resolution.

