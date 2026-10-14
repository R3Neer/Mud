# Risks and constraints

This note collects design and implementation risks. Language contracts belong to
specification and current decisions; mitigations below introduce no new semantics.

## Conceptual risks

- **Architecture independence confused with semantic neutrality.** Identity,
  atomicity, concurrency, errors, time and randomness require explicit language
  contracts even when Mud chooses no UI framework or database. Validate those
  contracts with contrasting conformance scenarios.
- **Regeneration with hidden domain logic.** Manual integrations and foreign
  fragments must retain their declared contracts and reproducible dependencies.
  Generated artefacts must preserve the source model's meaning.
- **Natural language as hidden authority.** An operator's inferred intention must
  not introduce behaviour absent from the model or accepted specification.
- **Premature implementation breadth.** Complete formalisation under
  [[notes/decisions/ADR-013-complete-formalisation-before-continuing-with-implementation|D-013]]
  before implementing the compiler/runtime. Later implementation can proceed
  through vertical conformance scenarios rather than many incomplete components.

## Semantic risks

- **Accidental nondeterminism.** Unspecified enumeration, match order, native
  behaviour or stochastic replay can alter observations. Preserve semantic order,
  the stated demand contracts and reproducibility inputs; physical hash/scheduler
  order cannot decide language behaviour.
- **Nontermination and oscillation.** Static source/body certification does not
  prove causal stabilization. Restricted reachability profiles and the still-pending
  operational cycle/resource policy retain separate obligations.
- **Invalid intermediate views.** Private temporary states, consolidated
  checkpoints and confirmed state have different validation/observation boundaries.
  Test those boundaries with traces rather than moving validation opportunistically.
- **Combinatorial growth.** Joint bindings, derived dependencies, imagine and
  eventually can require expensive exploration. Use cost models and measurements;
  unsupported proof obligations and technical interruption must retain their
  specified meanings.
- **Unstable identity.** Renaming paths can affect anchors, dependencies and
  persisted references. Anchor/data migrations need their own contracts before
  automatic refactoring promises compatibility.

## Tooling and implementation risks

- **Desynchronized derivatives.** Graphs, diagnostics and generated code must
  refer to the same model/version and remain reconstructible.
- **Unrelated changes in commits.** Isolate candidates or restrict edits/staging
  to known paths and hunks; never reset another author's work.
- **Incomplete authoring rollback.** Prepare and validate changes before publishing
  them, rather than relying on undoing partial external mutations.
- **Weak diagnostics.** Preserve error occurrence identity, source locations,
  dependencies and causal provenance. Do not confuse computing errors, refusal,
  unproved obligations and interrupted verification.
- **An accidental IR API.** Static contracts are specified, but semantic IR nodes,
  serialization and version migration remain undesigned. Consumers must not
  depend on placeholder encodings.
- **Premature syntax assumptions.** Respect the current grammar and chapter
  publication status. Test readability on real cases and route changes through
  the decision/conformance process rather than letting a parser choose semantics.
- **Silent semantic choices in implementation.** Report unspecified behaviour
  through its open question; passing a test does not authorize extending Mud.

## Boundaries to preserve

The model and declared foreign contracts remain the source of domain behaviour.
Boolean rules remain pure; external writes require the owning authority and
transaction/adapter contracts. Participants and given values retain their distinct
roles. Derivatives, prompts and maintenance logs add no language rules.

Tentative world state is not confirmed storage. Validated normal-message
notifications may be published provisionally with Waiting tickets; surviving
stable-root confirmation makes them Kept and scope disposal makes them Dropped.
This explicit protocol does not authorize leaking unchecked private state or
performing irreversible exterior writes before their confirmation/transaction
contract allows them.

Warning signs include relying on physical wave order, hiding a rule in a prompt,
turning an error into false for convenience, waiving a mandatory proof, guessing a
native purity contract or mixing unrelated changes into one commit.
