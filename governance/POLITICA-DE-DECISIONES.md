---
title: Policy on MUD decisions
aliases:
  - Cycle decision-making
tags:
  - mud/governance
  - mud/decisiones
status: current
---

# Policy MUD decisions

## Purpose

An decision records an accepted choice that influences the language, its architecture, the product or the editorial process. It explains the context and rationale for the choice, but does not replace its integration into the existing normative frameworks that fall within its scope.

Where the canonical location of a rule does not yet exist as a developed surface of `specification/`, an ADR current may retain interim authority until that surface is drawn up. This situation does not authorise the retention of contradictions in existing documents, nor does it require the creation of a provisional chapter in an inappropriate location.

## Autoridad

Each decision has a stable archive:

```text
notes/decisions/ADR-NNN-titulo-breve.md
```

The file is the source of truth based on the identity, state, provenance and decision relationships. `notes/decisions/README.md` is a generated index: it can be reconstructed and is never edited manually.

The specification prevails as the linguistic norm within already formalised domains. An ADR preserves the rationale behind a rule and serves as an interim authority until its canonical normative status has been established.

The relation of a `specification/` document, together with the decisions on which it is based, is recorded via its frontmatter `decisions:`. The decision-making history is not retained in the body of the legislation, in accordance with MUD-EDIT-002.

## Identidad

- The identifier `D-NNN` is unique and is not reused.
- The corresponding file uses the same number as prefix and `ADR-`.
- The title can be clarified without changing the identifier.
- The omitted numbers are set out in `notes/decisions/identificadores-reservados.txt`.
- A new decision is assigned the following free identifier; it does not fill a historical gap.

## Mandatory metadata

Every ADR begins with:

```yaml
---
id: D-NNN
title: "Título"
status: proposed
date: YYYY-MM-DD
supersedes: []
superseded-by: []
questions: []
affects: []
---
```

Meaning:

- `id`: identity stable.
- `title`: title without prefix `ADR-NNN`.
- `status`: state of the ADR.
- `date`: date of adoption or commencement.
- `supersedes`: decisions wholly superseded by this one.
- `superseded-by`: decisions which completely supersede this one.
- `questions`: related identifiers `Q-NNN`.
- `affects`: documents, chapters, artefacts or domains that must incorporate or verify the decision where such surfaces exist.

`supersedes` is not used for mere extensions, clarifications or partial modifications. These relationships are explained in the ADR and, where appropriate, via reciprocal links.

### Effective date of the body

An ADR with `status: vigente` must be able to be read literally as a description of the current decision within its scope. When a subsequent decision amends only part of an ADR current, the same editorial change must remove or rewrite, within the previous ADR, any rules that are no longer applicable and retain a note from provenance referring to the modifying decision. The history of the previous draft belongs to Git and is not maintained as an affirmative semantics within an ADR current.

When a subsequent decision replaces the entire scope, the previous ADR is not rewritten as if it had always stated something else: `status: sustituida` is applied with the reciprocal `superseded-by`. `retirada` is reserved for scope, which ceases to apply without a replacement rule.

## States

Permitted states:

- `propuesta`: not yet accepted.
- `vigente`: selection accepted.
- `sustituida`: another decision replaces all of its scope.
- `retirada`: ceased to apply without being replaced by another rule.
- `rechazada`: alternative considered but not accepted.

An decision `sustituida` must declare `superseded-by`. An decision that declares `supersedes` must also be declared in `superseded-by` for each decision that is substituted.

Nuances such as ‘current at its core’ or ‘exact open schema’ are explained in the main text and through active questions; they do not create additional states.

## Contents

An ADR shall include, where applicable:

```markdown
## Contexto
## Decisión
## Alternativas
## Consecuencias
## Ejemplos
## Verificación
```

An decision semantics must be precise enough to identify what was chosen. Its final normative formulation belongs to the canonical surface of `specification/` where such a surface exists.

## Integration into the specification

The integration continues from MUD-EDIT-003 to [[specification/00-editorial-conventions]].

For each current decision:

1. The regulatory areas that have already been developed and for which responsibility is stated to cover their scope are identified.
2. These surfaces must literally represent the state resulting from the decision and must not retain the substituted formulation.
3. Integration is not achieved simply by adding a subsequent section explaining that an decision changes the preceding content.
4. If the canonical surface does not yet exist, the rule is classified as semantics ‘accepted pending formalisation’; it is not nested within another chapter for documentary convenience.
5. Whilst it is pending formalisation, no existing content may contradict it, and the headings or descriptions of future chapters must remain consistent with it.
6. When the canonical surface is finally created, the rule is promoted to it and the ADR retains context and provenance, rather than a second normative copy intended to compete with the specification.

Integration is based on the affected surface area, not a binary property of the complete decision: a single decision may be integrated into the grammar and AST whilst still awaiting formalisation in the dynamic semantics if the corresponding chapter does not yet exist.

## Opening and acceptance

Before creating an decision:

1. A check is carried out to ensure that there is no other one with the same scope.
2. The questions it answers are identified.
3. Relevant alternatives and consequences are described.
4. A new identifier is assigned.
5. The questions and areas already developed that are affected by the same change are updated.
6. It must be ensured that the indices or maps of future surfaces do not contradict decision.

A proposal is moved to `vigente` once the author accepts the choice. If there are still any unresolved issues, these are retained as open questions.

## Replacement and withdrawal

ADRs are not cancelled when they cease to be valid. Replacement:

1.  creates or accepts the new decision;
2.  updates `supersedes` and `superseded-by` reciprocally;
3.  replaces the previous state with `sustituida`;
4.  updates the net areas, queries and relevant indices.

The rollback uses `retirada`, explains the reason and retains the file as traceability.

## Index and mechanical checks

From root:

```powershell
python tooling/decisions/manage_decisions.py generate
python tooling/decisions/manage_decisions.py validate
```

`generate` reconstructs `notes/decisions/README.md`. `validate` checks:

- mandatory names, identifiers and metadata;
- statuses and dates;
-  uniqueness and gaps in numbering;
- the existence of linked questions and decisions;
- reciprocity of substitutions;
-  exact match for the generated index;
-  absence of the old manual register.

## Relation with publishing and Git

Integration into the standard follows [[CICLO-DOCUMENTAL]]. The creation, acceptance, replacement or withdrawal of an decision forms part of the same atomic commit as its questions and any affected, already developed surfaces, unless an independent audit uncovers a pre-existing inconsistency.

