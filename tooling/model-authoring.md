# Semantic model authoring

This guide describes planned tooling for changing .mud source. Its authority is
[[notes/decisions/ADR-012-validation-and-atomic-versioning-of-semantic-changes|D-012]],
[[notes/decisions/ADR-053-semantic-operator-and-authoring-flow|D-053]] and
[[governance/COMMITS-POLICY|the commit policy]]. It is not an implemented service,
compiler or runtime API.

## Transactions and requests

A runtime action operates on a world instance under the language's causal
transaction contract. An authoring transaction changes the source model and its
derivatives. Their participants, checks and diagnostics are distinct.

Before changing source, classify the request as a query, CREATE, UPDATE, RETIRE
or migration. Record applicable structural/API/causal/domain/type/randomness,
invariant, admissibility and reachability effects. Identify ambiguity, missing
choices and authorization boundaries. An operator may apply only inferences
already defined by Mud; it cannot invent domain behaviour.

A structured plan should distinguish intent, semantic operations, resolved
anchors, preconditions, reads and expected impacts. Its machine-readable encoding
is not specified. An illustrative fragment is:

```yaml
intent: "Limit daily recruitment"
operations:
  - kind: UPDATE
    anchor: action::warfare.armies.Recruit
    change: add-precondition
expected_impacts:
  - rule::warfare.armies.CanRecruit
```

## Atomic workflow

1. Capture repository state and relevant language/compiler versions.
2. Resolve intent, names, anchors, dependencies and affected current decisions.
3. Assess impact and resolve indispensable ambiguities.
4. Prepare the operation plan and an isolated candidate or known task-owned hunks.
5. Edit only authorized source and metadata; format and validate.
6. Rebuild affected representations and derivatives once the required consumers
   exist. Run the applicable tests and compare expected with observed impact.
7. Review the complete diff and stage only the consistent task-owned unit.
8. Commit under the repository policy. Remote publication requires authorization.

Failure before publication must not publish a partial candidate. Preserve other
worktree changes; do not use a destructive reset as an authoring rollback.
Compilation, semantic IR and generated-code steps describe the future workflow;
the repository's current specification validators do not implement them.

## Queries, retirement and compatibility

A pure READ does not create a commit. A resulting decision or documentation
amendment is an UPDATE and follows its own validated commit process.

RETIRE is not automatically equivalent to deleting a declaration. Reference
handling, replacement, withdrawal and anchor migration retain the unresolved
contract in [[notes/questions/Q-015-r-retirement|Q-015]].

Commits follow the current commit format. Semantic descriptions may record
intention, affected anchors, API/domain/causal implications, validations and
related decisions or migrations. No machine-readable semantic commit schema is
selected here.

Reproduction requires the relevant model, specification target, compiler version,
foreign dependencies and any specified derivative schema. Version only those
derivatives justified by their cost and role; they never become semantic authority.
