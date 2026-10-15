---
title: Operational metadata in the spell domain
tags:
  - mud/examples
  - mud/expressiveness
  - mud/metadata
status: analysis
---

# Operational metadata in the spell domain

Three user-defined metadata entries have concrete consumers in this example.
They classify canonical declarations; ordinary Mud expressions or the bounded
source planner consume them. They introduce no intrinsic metadata, implicit
permissions, startup order or runtime scheduling rule.

| Metadata | Owners | Consumer and effect |
| --- | --- | --- |
| activationFeature: ActivationFeature | The fourteen registered support declarations | ActivationSelection selects actual declarations for start with. Core support is always retained. |
| modalities: FeedbackModality [1..* unique] | Every FeedbackAsset family member | FeedbackChannel omits resources whose requirements its allowedModalities do not satisfy. |
| checks: TestConcern [1..* unique] | Every scenario declaration | spell_metadata.py selects roots and produces their independent activation plans, including directly called tests. |

All configured values here are closed-static and read-only. Metadata is available
before activation and while its owner is inactive. It is not inherited and does
not become ordinary alias payload or change value equality. Every owner that a
consumer can inspect must supply the expected complete contract. Missing metadata
is an error, not a false/empty default invented by the consumer.

## Activation features

configuration/activationSelection.mud is part-only because its registration list
contains private rule identities. It holds the only support catalogue:

| Feature | Members |
| --- | --- |
| Core | world.Entity, world.Creature, spells.Spellcaster, spells.Magic, spells.CanSelect, spells.CanAttempt, spells.ConcentrationWithinLimit, sympathy.TargetUsable, sympathy.CanLink, sympathy.ExclusiveSympathy, spells.PublishSpellEvents |
| Feedback | feedback.FeedbackChannel, feedback.PlanSpellFeedback |
| LinkEffects | sympathy.PrepareLinkEffects |

```mud
start with {
    configuration.ActivationSelection([configuration.ActivationFeature.Feedback]).declarations,
    fixtures.MagicWorld, fixtures.Player, fixtures.PlayerFeedback
}
```

The private alias stores requested features and derives a flat finite collection
from the catalogue by querying declaration~activationFeature. It always includes
Core, including for ActivationSelection(). Repeated features or declarations do
not change activation membership. Concrete fixtures remain explicit; requesting
Feedback does not activate every caster or channel.

File defaults classify homogeneous files such as spells/state.mud. They precede
using and follow part only where present. Direct owner metadata classifies the
schemas in world/entities.mud and PrepareLinkEffects in the mixed link-state file.
Defaults apply to compatible declarations written directly in a file, not to
imports, family members or descendants. Explicit owner values replace defaults.

The catalogue registers identities; metadata keeps classification adjacent to
its owner. A feature-to-declarations dictionary could also express the selection,
but this arrangement makes owner classification independently inspectable.
Registration remains explicit: all Thing is not discovery of inactive schemas
and rules. A new support declaration must be classified and registered once.

All reads in the start expression are static: alias construction, metadata and
the finite comprehension. No active population, mutable world field or native
call participates. This changes neither activation rights nor the ordinary
identity-deduplicated, unordered combination of start contributions.

## Feedback capabilities

feedback/contracts.mud defines a closed resource family. Each resource has a
stable descriptor and explicit nonempty modality requirements. An arbitrary alias
value would not supply a distinct anchored owner for per-resource metadata.

| Resource | Required modalities |
| --- | --- |
| AmbientGlow, SelectionFlash, SuccessFlash | Visual |
| CastChime, FailureChime, RejectionChime | Audio |
| LegacyPulse, CancelPulse | Haptic |
| SynchronizedBurst | Audio and Visual |

These are the example's authored resource identities, not discovered Unity
resources. SynchronizedBurst supplies the combined-capability counterexample;
it appears only in capability fixtures. Native bindings remain external.

FeedbackChannel.allowedModalities is ordinary per-channel configuration, defaulting
to all three modalities. Metadata describes resource requirements; the channel
field determines which requirements this receiver can satisfy. Live mute state,
if needed later, belongs in world state rather than writable metadata.

After the existing per-phase merge, deduplication and global-only exclusions:

```mud
let permitted := foreach asset in effects
    if forall modality in asset~modalities : allowedModalities has modality --> asset
```

Every required modality must be allowed. Audio-only output omits SynchronizedBurst;
it does not request half that resource. Separate resource members express independent
presentation. The same predicate filters selectionRejected using an ordered
comprehension, preserving permitted repetitions. Filtering never reorders phases,
merges resources across phases or changes captured aim/context. Empty work yields
no FeedbackRequest. An empty allowed set silences all resources.

An all-enabled channel preserves the existing merge/exclusion contract under the
resource identity migration. All prior feedback scenarios remain; seven additional
source scenarios cover visual-only output, both combined-capability cases, muted
output, rejection duplicates, rejection absence and repeated phase resources.
Filtering cannot affect spell acceptance, concentration or sympathy relations.
It is not a guarantee of successful native playback.

## Selecting scenario plans

Run from the repository root:

```console
python tooling/examples/spell_metadata.py
python tooling/examples/spell_metadata.py --concern Feedback --concern PairAdmission
python -m unittest tooling.tests.test_spell_metadata
```

The CLI follows the repository's R3CLI help/diagnostic conventions. Stdout is JSON:
kind is bounded-source-plan, executesMud is false, and worlds contains one entry
per selected test root. Each entry lists its canonical qualified root, reachable
test declarations and deduplicated activation identities. Different roots keep
separate worlds; the tool never combines all selected fixtures into one world.
The --root option permits checking another copy of this same example layout.

The closed concern family is Selection, PairAdmission, Contributions, Lifecycle
and Feedback. All 47 scenarios have nonempty checks, normally through file defaults.
Mixed scenarios override their complete value. In particular,
FeedbackModelsARealSympathyCast explicitly covers Feedback, Selection and PairAdmission.
An override replaces its file default; it does not append to it.

Without a concern filter, all roots are selected. Repeated --concern options use union selection
and identity deduplication. Unknown names and empty matched root sets are errors.
The selected root's complete supported test-call closure contributes to its world,
even when a called test's own concerns do not match. Filtering never removes that
child's activation support. Cyclic test calls are rejected.

### Bounded source-tool boundary

The planner is implemented for this example's single dependency-free part,
unique short declaration names and scenarios path. It inventories literal enum
metadata, the written ActivationSelection template, explicit fixture lists and
direct statically named test calls. It checks complete classifications, registered
support, resource requirements and every scenario setup before producing a plan.
It also rejects a parenthesised tuple passed to the known byStage dictionary
component. This narrow shape check catches a parseable but incompatible literal;
it does not validate arbitrary constructor types. Sublook/submessage declarations
are inventoried so private query helpers cannot hide test references.

It is not a Mud parser, name resolver, typechecker, runtime or test executor. It
cannot establish arbitrary closed-static evaluation, descriptor availability,
permission correctness, domain behavior or causal effects. Its accepted template
checks are authoring evidence, not a new language rule. Normal Mud front-end
checks remain required when a compiler exists.

Nested/foreign parts, indirect or helper-mediated test references, native test blocks and metadata
forms outside the supported literal subset are rejected rather than guessed.
A compiler-produced call graph is required to generalise this tool. A plan does
not expose private operations as host endpoints or grant cross-part uses rights.
The tests exercise these boundaries and closure behavior; they do not execute Mud.

## Design boundaries

Spell.slot and needsConcentration remain family data. grabbed, present, selected,
concentration and relation contributions remain world state or ordinary derivations.
No tag grants commutativity, cache safety, purity, execution priority or scheduling.
No persistence/replication annotations exist without a corresponding consumer.
There is no metadata on start with, arbitrary clauses, branches or alias instances.
Neither file provenance nor presentation labels select behavior.

The configuration path remains in the existing part. Private registries retain
part-only visibility; shared feature/modality types do not confer access to their
owners. The normative language specification and Unity remain unchanged.
