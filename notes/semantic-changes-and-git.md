# Semantic changes and Git

This document describes the safety protocol for modifying the model. Authority for the workflow belongs to [[notes/decisions/ADR-012-validation-and-atomic-versioning-of-semantic-changes|D-012]], [[notes/decisions/ADR-053-semantic-operator-and-authoring-flow|D-053]] and [[governance/COMMITS-POLICY|the commit policy]]. This differs from running an action inside a world: here the `.mud` definition is changed outside the world.

## Two types of transaction

MUD contains two related but distinct atomicities:

1. **Runtime transaction**: one action converts an instance of the world or reverses.
2. **Authorship transaction**: a request transforms the files `.mud` and its derivatives, or reverses.

Both share the philosophy of not publishing partial statuses, but they have different participants, validations and diagnostics.

## Classification of a request

Before making any changes, the operator must decide whether the request is:

- Consulta.
- Creation, updating, removal or migration.
- Structural change, API change, causal, by domain or affiliation.
- Change to randomness, an invariant, admissibility or reachability.
- Ambiguous, incomplete, out of scope or an attempt to circumvent restrictions.

A request can be assigned several tags: an operation `UPDATE` It may also involve a change to the API and a change causal.

## Operations plan

AI should first produce a structured and verifiable artefact:

```yaml
intent: "Limitar el reclutamiento diario"
operations:
  - kind: UPDATE
    anchor: action::warfare.armies.Recruit
    change: add-precondition
reads:
  - thing::warfare.armies.Kingdom::lastRecruitmentDate
expected_impacts:
  - rule::warfare.armies.CanRecruit
open_questions: []
```

The exact format is open to discussion, but it must distinguish between human intent, operations, observed anchors and anticipated consequences.

## Atomic flux

1. Capture the state Git and the compiler version.
2. Classify the request.
3. Resolve names to anchors.
4. See direct and transitive dependencies.
5. Identify ambiguities and open-ended decisions.
6. Draw up the operational plan.
7. Prepare a point an isolated catering establishment.
8. Apply changes only to `.mud` and authorised metadata.
9. Format.
10. Compile and validate.
11. Rebuild graph and IR.
12. Regenerate the affected instancements.
13. Run tests.
14. Compare the predicted impact with the observed impact.
15. Check the differential.
16. Please confirm that no unauthorised changes have been included.
17. Create a atomic commit.

If any step prior to the commit fails, the exact state at the start of the transaction.

This flow, the classification and the operator’s inference limit are consolidated in [[notes/decisions/ADR-053-semantic-operator-and-authoring-flow|D-053]].

## Policy for repositories with previous changes

The operator must not assume that a ‘dirty’ worktree belongs to them. Safe options:

- Reject the mutation until changes are isolated.
- Use a worktree or index temporary.
- Restrict the patch to known files and hunks.

You must never perform a destructive reset of someone else’s work. The final commit should only include changes that form part of the semantic plan.

## Semantic commits

A commit should state:

- Which intention was addressed?
- What operations were carried out?
- Which anchors were changed?
- Whether there was a change to the API, causality or domain.
- Which validations were carried out.
- Which decisions or migrations are related?

Example message:

```text
UPDATE action::warfare.armies.Recruit recruitment limit

Operations:
- UPDATE action::warfare.armies.Recruit
- CREATE rule::warfare.armies.CanRecruitToday

Impact:
- API: unchanged
- Causality: precondition added
- Data migration: none
```

The general format of commits is governed by [[governance/COMMITS-POLICY|the policy commits]]. Before automating log parsers, you must also set a contract a standard for machine-readable semantic fields.

## Should `READ` create a commit?

No. One query It may appear in audit logs, but it does not alter the source semantics. D-012, D-053 and the policy Commits are reserved for CREATE, UPDATE, RETIRE, migrations or other persistent changes, not for an isolated read.

If you wish to version control knowledge acquired during a query —for example, closing a decision— that would be a `UPDATE` on metadata from specification, not a `READ`.

## Withdrawal versus deletion

`RETIRE` suggests a semantics more useful than deleting text:

- Check references.
- Prevent further dependencies.
- Enter the replacement or reason.
- Allow anchor migration.
- Only physically remove it when it is safe to do so.

The semantics Exacta remains open at [[notes/questions/Q-015-r-retirement|Q-015]]. Until it has been resolved, the operator must not automatically equate `RETIRE` by removing one declaration.

## Validation of the impact

The expected impact should be compared with:

- Anchors added, modified, removed or migrated.
- Changes to rules and actions.
- New readings and writings.
- Changes to domains and cardinalities.
- New cycles.
- Changes in stochasticity.
- Affected deployments and tests.

An unexpected discrepancy between the predicted and actual impact should halt the commit or trigger a request review.

## Reproducibilidad

The commit should allow the following to be reconstructed:

- Version of the specification.
- Compiler version and IR schema.
- Modelo `.mud`.
- Relevant derivatives.
- Results from validation.

Not all derivatives need to be versioned. The decision must be based on cost, auditability and ease of reconstruction, whilst bearing in mind that they are never authority semantics.

