# Mud

> Add the rules. Let the world take shape.

Children invent games without designing an architecture first.

They say things like:

- “You cannot be caught while touching the wall.”
- “If you are tagged twice, you are out.”
- “The person holding the ball cannot move.”
- “When everyone reaches the other side, the round starts again.”

Each new rule is added directly to the game. It meets the rules that are already
there, changes what can happen and sometimes creates consequences nobody had to
design explicitly.

Mud begins with the idea that domain logic should work in much the same way.

## Start with the rules, not the architecture

Mud is an experimental declarative language for describing things, rules,
actions and consequences without first deciding how an application should be
structured.

In a conventional system, adding a new rule often begins with technical
questions: which class owns it, which service executes it, where its state is
stored, which event triggers it and how it fits the existing architecture.

Mud moves those questions out of the domain model. A person should be able to
introduce a thing or a rule because it belongs to the world being described.
Mud combines it with the rest of the model; compilers, runtimes and
materialisers turn that model into something a particular application can run.

The architecture adapts to the model. The model does not adapt to the
architecture.

## Why “Mud”?

The name is literal.

A Mud model is not intended to resemble a carefully arranged collection of
software components. Things, relationships, actions and rules are added as
they become necessary and mixed into a common semantic substance.

From those declarations, the behaviour of the world emerges.

That emergence is not intended to be mysterious or unpredictable. Given the
same model, state, inputs and random seed, a conforming implementation should
produce the same result and be able to explain how it was reached.

Developers should rarely need to inspect the internal arrangement of the whole
model. The model simply exists and can be queried, changed, validated and
materialised. But opacity must never be required: Mud source remains readable,
diagnosable and editable when a person needs to understand or change it.

## A language that grows with its user

Mud is designed especially for people who are not programmers when they begin.

The first interaction may happen entirely in natural language. An AI-assisted
semantic operator can identify relevant declarations and anchors, inspect
dependencies, expose ambiguity and impact, propose explicit semantic
operations, update the model atomically, validate it, rebuild derived artifacts
and record the change in Git.

Natural language is the interface, not the source of truth. Lasting meaning
must be represented in formal `.mud` source.

As a person becomes familiar with the model, they can move gradually from
natural-language intentions, through reviewable operations and concrete Mud
anchors, to direct source editing.

## Vocabulary from the world

Mud deliberately avoids framing every idea in conventional programming
terminology:

- `thing` introduces something that exists in the modelled world;
- `family` describes a closed family of related values;
- `action` describes something that may be attempted;
- `look` observes the world without changing it;
- `message` describes something that occurred;
- `when`, `if`, `then`, `after` and `otherwise` express rule structure;
- `always` states a condition every confirmed world must preserve;
- `given` introduces information supplied to an operation;
- `start with` describes what initially exists.

This vocabulary is intended to be approachable without making the language
informal. Mud is a formal language with explicit syntax and semantics.

## What Mud models

Mud describes domain meaning:

- things, values and identities;
- fields, relationships and collections;
- domains, intervals, magnitudes and units;
- pure queries and invariants;
- actions that may be accepted, rejected or fail;
- reactive rules and causal consequences;
- reproducible randomness;
- public observations through `look`;
- causal occurrences through `message`;
- isolated declarative tests.

Mud does not describe user interfaces, persistence technologies, networks,
authentication, deployment infrastructure, application frameworks or rendering
algorithms. Those belong to the systems that host or materialize a Mud model.

## A glimpse of Mud

```mud
action Recruit for kingdom: Kingdom [mut]
given
    amount: Nat in 1..100
{
    if kingdom.treasury >= amount * kingdom.recruitmentCost
    otherwise "The kingdom cannot afford {amount} recruits"
    then {
        kingdom.treasury -= amount * kingdom.recruitmentCost
        kingdom.soldiers += amount
    }
    after kingdom.soldiers >= old kingdom.soldiers
    otherwise "Recruitment did not increase the army"
}
```

This declares a domain operation rather than an application endpoint. Its
participants, input domain, precondition, effects, postcondition and
diagnostics belong to the model. It says nothing about buttons, HTTP requests,
database tables or game-engine objects.

## Rules meet inside the model

An external `action` begins a causal resolution. Its effects may activate
reactive rules, which may produce further consequences. The system evaluates
those consequences in causal waves until it reaches a stable tentative world.

That world is confirmed only if the entire resolution is valid. An action can
finish as `accepted`, `rejected` or `failed`; every result other than
`accepted` rolls the complete resolution back.

This is how behaviour can emerge from independently declared rules without
giving up atomicity, determinism or explanation.

## Source of truth

Files ending in `.mud` are the only source of domain behaviour.

Syntax trees, indexes, graphs, generated code, generated documentation and
runtime representations are reconstructible projections. They may make the
model easier to execute or inspect, but they cannot add rules of their own.

## Project status

Mud is under active design and is not ready for production use.

The current target is a formally specified Mud 1.0. The project prioritizes
completing the formal language specification before continuing with a full
implementation, so that accidental choices in an early compiler or runtime do
not silently become language semantics.

Substantially developed areas include the lexical and concrete grammars, a
lossless concrete syntax tree, a normalized surface AST, stable names and
public anchors, nominal resolution, a nominal HIR contract, mechanically
synchronized syntax artifacts and reviewed semantic decisions.

Syntax highlighting, formatting and smart editing are implemented tooling. The
complete type system, elaboration, causal runtime, advanced analyses, semantic
representation, conformance profiles, conformance suite, compiler and runtime
remain in development.

## Repository guide

- [`especificacion/`](especificacion/) — the normative language specification
  and checked syntax artifacts;
- [`notas/vision-y-alcance.md`](notas/vision-y-alcance.md) — product thesis,
  intended users and boundaries;
- [`notas/arquitectura-del-sistema.md`](notas/arquitectura-del-sistema.md) —
  compiler, runtime, semantic operator and materialisation architecture;
- [`notas/decisiones/`](notas/decisiones/) — language and architecture decisions;
- [`notas/preguntas/`](notas/preguntas/) — open and partially decided questions;
- [`gobierno/`](gobierno/) — editorial and change-control processes;
- [`tooling/`](tooling/) — supporting and experimental tools.

Repository-specific export profiles live in
[`markdown-export.toml`](markdown-export.toml) and are consumed by the separate
[R3 Markdown Export](https://github.com/R3Neer/markdown-export) package.

The canonical specification and project records are currently written in
Spanish. Mud source vocabulary is English.

## An Obsidian-native project

This repository is designed to be explored as an
[Obsidian](https://obsidian.md/) vault. The specification, decisions,
questions and notes form a connected body of knowledge through Markdown,
frontmatter and internal links.

Editing is powered by
[Syntax Highlight](https://github.com/R3Neer/syntax-highlight), an independent
and reusable project whose Mud package is derived from snapshots of the
normative lexical and concrete grammars.

It provides highlighting for Mud code blocks and `.mud` files, semantic token
categories, source formatting, smart editing inside Obsidian and reusable
CodeMirror, HTML, command-line and MCP integrations.

Syntax highlighting is an editing aid. It does not replace parsing, name
resolution, type checking or semantic validation. Local `.obsidian`
configuration is intentionally not versioned.

## Design promises

Mud is being designed around these long-term promises:

- **Meaning preservation** — relevant domain logic belongs in `.mud`.
- **Incremental growth** — new declarations join the model without requiring
  a prior application architecture.
- **Atomicity** — half of a semantic change or causal resolution is never
  published.
- **Explainability** — dependencies, affected anchors and causal consequences
  can be identified.
- **Reproducibility** — the same model, inputs and seed produce the same result.
- **Reconstruction** — derived artifacts can be rebuilt from their source.
- **Traceability** — semantic changes retain their intention and history.
- **Replaceability** — a technical materialisation must not imprison the model.
- **Progressive accessibility** — people can move from natural language to
  direct source editing at their own pace.

These are design goals under active formalization, not claims about an already
complete implementation.

## Contributing

Mud is currently developed under the direction of its author.

Discussion, questions and feedback are welcome. Before contributing code,
language changes, documentation or derived implementations, please contact the
author so that authorship, licensing and the semantic change process can be
agreed explicitly.

## Licence and trademark

Mud is not currently an open-source project. The contents of this repository
are published with all rights reserved. See [`LICENSE`](LICENSE).

**Mud™** is the name of the language project. The name may be used to refer
accurately to Mud, but not to imply endorsement or identify a modified or
unrelated language. See [`TRADEMARKS.md`](TRADEMARKS.md).
