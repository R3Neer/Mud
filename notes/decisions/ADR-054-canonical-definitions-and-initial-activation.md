---
id: D-054
title: "Canonical definitions and initial activation"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-044"
  - "Q-045"
affects:
  - "[[notes/questions/README|Preguntas activas]], [[specification/04-mathematical-model]], futuros capítulos 06, 07, 08, 09, 11, 21 a 25 y 32"
---
# ADR-054 — Canonical definitions and initial activation

- Amended by: [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]]
- Amended by: [[notes/decisions/ADR-084-specialisation-de-aliases-inherited-members-and-derived-views|D-084]]
- Related to: [[notes/decisions/ADR-021-cycle-logical-lifespan-and-suspension-by-department|D-021]], [[notes/decisions/ADR-023-consolidation-of-concurrent-structural-effects|D-023]], [[notes/decisions/ADR-025-vocabulary-from-thing-headings-and-sections|D-025]], [[notes/decisions/ADR-035-organisation-names-using-and-anchors|D-035]], [[notes/decisions/ADR-046-algebra-and-conflicts-of-effects|D-046]], [[notes/decisions/ADR-055-declarative-and-diagnostic-tests-otherwise|D-055]]
- Amended by: [[notes/decisions/ADR-058-temporal-triggers-changes-and-reactive-old|D-058]]
- Amended by: [[notes/decisions/ADR-068-universal-thing-and-intrinsic-name|D-068]]
- Amended by: [[ADR-099-fresh-materialisations-after-destroy-and-create|D-099]]
- Close: [[notes/questions/Q-044-i-identity-and-references-to-future-thing-values|Q-044]], [[notes/questions/Q-045-c-declarative-content-of-create|Q-045]]
- Documents concerned: [[notes/questions/README|Active questions]], [[specification/04-mathematical-model]], future episodes 06, 07, 08, 09, 11, 21 to 25 and 32

## Context

The syntax must distinguish between three operations:

1. Define what a declaration.
2. Decide whether to take part in the world current and, for a `thing` specifically, if there is a materialisation runtime enabled.
3. Modify the structure of a materialisation active.

The model The approach adopted is that of a game featuring:

- A static catalogue of possible things and rules.
- A selection of statements to begin with.
- Runtime operations that remove and re-introduce the same canonical identifiers.
- Runtime instantiations of `thing` specific actions that could lead to `destroy` and reinvent itself in a fresh way through a `create` back.

## Decisión

### Canonical definition unique

Every `thing` declarable, and each rule has exactly one complete top-level definition throughout the programme. The root incorporated `Thing` it is the only one `thing` source not specified: his descriptor The canonical belongs to language; it is abstract and always effective. It cannot be redefined, nor can it be regarded as the object of `create` o `destroy`.

```mud
abstract thing Vegetation {}

thing Tree as Vegetation {
    age: Years
}

rule CanGrow on plant: Vegetation {
    ...
}
```

The standard definition:

- The category of the declaration.
- His identity y anchor.
- In a `thing`, whether it is abstract or concrete.
- In a `thing`, their direct predecessors.
- Its declarative body.

The direct predecessors of a `thing` do not change during execution. `destroy` y `create` adjust their behaviour and, for a `thing` specifically, they complete or build their materialisation runtime; they do not change their identity nor his descriptor canonical.

Two complete definitions with the same anchor are a error static, even if their bodies are the same. The order of files and statements does not resolve the duplication.

### `create` activate a canonical identity and carries it out when necessary

`create` is a runtime instruction directed at a canonical identity:

```mud
create Tree
create CanGrow
```

Its objective must be to solve a single problem statically canonical definition from `thing` or rule. It does not allow for a category, modifier, list of predecessors or body.

One activation following `destroy Tree` restore it to its original state identity `Tree`, with the same predecessors and the same descriptor. In accordance with D-099, if `Tree` is a `thing` specific one whose materialisation the previous one ended, `create Tree` build a materialisation fresh from the canonical definition; it does not restore the load or the structural modifications characteristic of the materialisation destroyed.

Several concurrent applications `create d` addressed to her declaration absent, they are idempotently consolidated. There are no longer any runtime declarative fragments, nor any merging of bodies caused by `create`.

One request `create d` does not change a declaration already active. The applicability of rules and actions that require activations that have already been completed remains subject to Q-046.

### Starting set `start with`

The definitions of `thing` and rules do not remain active simply because they appear. Each module can contribute a maximum of one `start with` unified:

```mud
start with {
    Vegetation,
    Tree,
    CanGrow
}
```

A direct contribution, or each expression in the block, contributes zero, one or several activatable statements `thing | rule`: a reference provides one, `empty` equals zero and one collection contributed by its members. To bring about a domain Explicit enumeration is used `all D`; a collection of collections is invalid. Duplicate identifiers are deduplicated and the order is not observable.

Expressions can only depend on information available before they exist world runtime. The contributions from all modules are combined, materialised and validated atomically, and stabilised before external actions are accepted. Each module can only trigger statements with cycle its lifespan module.

Actions, aliases and magnitudes are not executable statements. Each test declares his own contribution `start with`; for a test root the contributions from the static transitive closure of reachable tests are combined in accordance with D-096.

### Initialisation and rematerialisation

The defaults and initialisers for a `thing` These specific rules apply when building a materialisation since its canonical definition, both in the materialisation initial via `start with` o `create` as in a subsequent rematerialisation following `destroy`.

After a `destroy d` confirmed on a `thing` specifically, the own stored data and the runtime structural modifications to the materialisation Once destroyed, they are discarded. One `create d` back:

- retains the identity, the descriptor and the canonical predecessors of `d`;
- reconstructs the structure from the canonical definition;
- re-apply defaults and initialisers;
- does not retrieve values or structural changes from the materialisation completed.

One `thing` abstracta does not have a specific implementation of its own to reset. For rules, D-099 specifies that the runtime memory of a activation nor does the new one pass through the one that has been explicitly destroyed activation.

The suspension of a declaration because one hard dependency 'is inactive' does not mean `destroy`: that suspension can retain the load belonging to the declaration suspended.

### Reserved and contextual words

`with` is a reserved word.

`start` is a contextual word: the parser recognises it as the start of a modular contribution `start with` top-tier or the `start with` contained in a test.

`abstract` It is also context-dependent: the parser recognises it as a modifier only when it precedes `thing`. Outside that position, it can be used as an ordinary identifier.

`always` is contextual before `rule`. D-055 enter `test` y `otherwise` as reserved words.

Standard metadata such as `~name` y `~prefixes` they use Postfix General Grammar `~`; `name` y `prefixes` they are not special contextual tags because of that reason.

There is no token neither a single lexical category nor one termed ‘reserved expression’ for `start with`; it is a production grammatical, consisting of a contextual word and one reserved word.

## Sintaxis concreta

In brief:

```ebnf
thing-declaration
    ::= [ "abstract" ] "thing" nominal-name
        [ "as" nominal-name { "," nominal-name } ]
        [ body ]

create-instruction
    ::= "create" declaration-reference

start-with-declaration
    ::= "start" "with"
        ( expression
        | "{" [ expression { "," expression } [ "," ] ] "}"
        )
```

The text in quotation marks in this EBNF does not in itself imply that `start` o `abstract` are reserved words; their lexical classification is as set out in the previous section.

## Sintaxis abstracta

The AST must distinguish, as a minimum:

```text
ThingDecl(anchor, mode, directAncestors, body)
RuleDecl(anchor, variant, body)
InitialActivationSet(references)
CreateReference(anchor)
DestroyReference(anchor)
```

`CreateReference` does not contain a descriptor nor a new definition. `InitialActivationSet` preserves provenance textual data for diagnostic purposes, but its meaning is an unordered set.

## Consequences

- The programme determines a finite set of possible identities; the world determines which ones are active and which specific instances exist.
- `destroy` + `create` does not introduce a identity new, although it can end one materialisation and build another one just like it canonical identity.
- The graph The specialisation declaration is derived from static definitions, not from fragments accumulated during execution.
- A bypass of a ancestor The ‘inactive’ status remains temporary and restores the declared edges when reactivated.
- Conflicts over the merger of organisations are resolved `thing`.
- Dynamic modification of properties, where permitted, must be expressed using explicit operations such as `add` y `remove` and belongs to the materialisation the relevant asset.
- Creating an unlimited number of fresh individuals would require a different feature; `create` it does not introduce it implicitly.
- The LSP can be accessed from anywhere activation o materialisation up to just one canonical definition.
- The list of reserved words must distinguish between hard words and contextual words.

## Options ruled out

### Reusing a name for successive identities

This is ruled out because it forces a decision on whether the existing references follow the identity either remain as they were or are re-linked to the new holder of the name. The second option may invalidate stored domains and cardinalities; the first preserves hidden identities that no longer match the visible name.

### Put the own stored data after `destroy`

It is ruled out in accordance with D-099. Preserve the materialisation its own would mean that `destroy` would act simply as a deactivation and would prevent a new materialisation started from the state stated.

### Accumulate predecessors without allowing them to be removed

It is ruled out because a new creation appears to provide a complete definition, but would silently retain all previous predecessors. This does not come across as natural to readers without a technical background, nor does it align with the usual expectation of declarative inheritance.

### Preserve the fragmentary fusion of `thing`

It is ruled out because it makes the descriptor of a identity which rules they agree on and in which waves. Structural changes must use explicit operations.

### Modelling `start with` such as action o `then`

It is ruled out because it has no caller, participants, conditions or result operation. Its content is an initial set, not a sequence causal.

## Future verification

The suite must cover:

1. One canonical definition by `thing` and a ruler.
2. Rejection of two definitions with the same anchor.
3. Rejection of `create` by category, predecessors or body.
4. Activation and the destruction of a `thing`.
5. Rematerialisation of a `thing` specific, whilst maintaining the exact identity y descriptor, but load reconstruction from defaults and initialisers.
6. Activation concurrent idempotent of a identity absent.
7. At most one `start with` by module and a valid exemption from contribution in a module.
8. Order independence and deduplication within the unified set of contributions.
9. Support for direct input, unified block and optional trailing comma.
10. Rejection of non-activatable declarations, activation from another module and nested collections.
11. A project in which certain modules are omitted `start with`, equivalent to an empty initial contribution.
12. Materialisation the combined total of the contributions from all modules and stabilisation prior to external actions.
13. `Thing` always in force and cannot be activated.
14. Load reduction and in-house structural modifications following `destroy`, without removing a third party’s charge that has merely been suspended by reason of subordination.
15. Union of contributions `start with` of the static transitive closure of reachable tests.
16. Shooting during the stabilisation initial of a `when` whose condition is initially true.
17. LSP navigation from each activation to a single definition.

## Syntactic modification by D-084

The body of a `thing` It may be omitted when it contains no members. `thing A`, `thing A {}` y `thing A;` set it at the same level canonical definition; only their CST differs.

## Amendment current by D-096

The initial activation becomes modular. Each module You can contribute a maximum of one `start with`; all contributions are combined and brought together before the stabilisation. `start with` no longer separates `things` y `rules`, does not specify an order and can only trigger statements with cycle its lifespan module.
