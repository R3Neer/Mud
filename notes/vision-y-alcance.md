# Vision and scope

## Product proposition

MUD proposes that the logic of a system should have its own explicit and stable representation, independent of the implementation that executes it. This representation is stored in files `.mud`; the generated code, the indexes and the graph are interchangeable projections.

Ordinary interaction does not have to resemble programming in a MUD. The user expresses an intention in natural language and the system:

1. Identify the affected anchors.
2. Query dependencies and previous decisions.
3. It highlights ambiguities and their impact.
4. Formulate semantic operations.
5. Edit the model atom by atom.
6. Validate the new one state.
7. Regenerates derivatives.
8. Commit the change to Git.

Language is, therefore, a stable internal interface between human intention and technical implementation.

## Problem it aims to solve

In a conventional system, the meaning of the domain is distributed across code, the database, tests, documentation, configuration and implicit decisions. Changing the architecture may require reconstructing that meaning based on its effects.

The MUD is trying to reverse that relation:

- The semantics from domain It is declared only once.
- Dependencies can be checked before making any changes.
- The history shows semantic changes, not just edited lines.
- An implementation can be regenerated without redefining the world.
- An AI can operate on elements with identity consistent rather than making ad hoc changes to the text.

## Users and initial cases

The initial use case is video games and simulations with many interrelated rules. It is a good learning curve because it requires:

- State changeable.
- Relationships and collections.
- Reactive rules.
- Invariants.
- Reprehensible actions.
- A chain reaction of consequences.
- Reproducible randomness.
- Hypothetical questions.

The first user experience is that of a designer of domain AI-assisted, not written by a person who writes every declaration manually. Even so, the language must be readable, diagnosable and editable by humans, because it is the source of truth and the final inspection area.

## Limits of the domain

MUD describes:

- What a variety of things and values there are.
- What properties and relationships do they have?
- Which terms and conditions can be viewed?
- What legal actions can be taken?
- What effects and reactions do they cause?
- Which restrictions should be retained?
- What result A stable result is obtained.

MUD does not describe:

- Graphical user interface.
- Perseverance.
- Network.
- Authentication.
- Infrastructure.
- Application architecture.
- Frameworks, engines or platforms.
- Algorithms for presentation or deployment.

One materialisation You can decide on all of the above, but you cannot add behaviour from domain absent from the model.

## Product layers

It is best to refer to four layers to avoid any confusion over objectives:

1. **Model**: files `.mud` and its regulatory rules.
2. **Semantic engine**: compilation, validation and implementation causal.
3. **Semantic operator**: tools that query and modify the model using anchors.
4. **Materialisation**: code or contracts relating to a specific technology.

The natural language interface sits on top of the semantic operator; it is not part of MUD grammar.

## Essential promises

If the project is successful, I should be able to promise:

- **Preservation of meaning**: the relevant logic is in `.mud`.
- **Atomicity**: half a change is never published.
- **Explainability**: You can list read, written and affected anchors.
- **Reproducibility**: the same model, tickets and seed produce the same result.
- **Reconstruction**: derivatives are regenerated from the source.
- **Traceability**: every valid change has an intention, operations and a commit.
- **Substitutability**: the materialisation does not imprison the model.

## Criteria for the success of a first version

The first version does not need to express all the specification. You do need to demonstrate, from start to finish, that:

1. A model A small one can be written and validated.
2. Its symbols and anchors are stable.
3. One action brings about a change causal deterministic or reverses.
4. The impact can be explained before editing.
5. A semantic change It can be applied, tested and turned into a standalone commit.
6. A simple derivative can be regenerated without being a source of behaviour.

## No early targets

- To be a general-purpose language.
- Replace all implementation languages.
- Create a complete application.
- Deal with it from the outset `eventually`, chance, calendars and multiple inheritance.
- To accept any ambiguous request without human intervention.
- To guarantee formal properties that have not yet been proven.

