---
title: Operational metadata for the spell domain
tags:
  - mud/examples
  - mud/expressiveness
  - mud/metadata
status: analysis
---

# Operational metadata for the spell domain

This proposal selects three uses: activation features, feedback capabilities and
regression selection. Each has a named consumer and an observable effect. They
are recommendations for the example, not accepted language changes or metadata
already installed in its source files. No compiler, test runner or Unity adapter
is implemented by this document.

The proposed metadata uses existing owner, typing, header and reflection forms.
The asset catalogue change and regression-driver contract are explicit design
changes to the example/tooling, not new intrinsic metadata understood by Mud.

## Boundary between metadata and domain state

Use metadata for configuration of a canonical declaration, including a family
member. Use fields/associated data for the represented domain value, and ordinary
mutable fields for live world state. A consumer gives user metadata its meaning;
writing a tag alone does not alter activation, dispatch or effect semantics.

All three selected uses have immutable, closed-static metadata values. Although
D-087 permits live calculated metadata, these cases need no runtime reads in
metadata. Metadata remains available when its owner is inactive, is not inherited,
and does not change equality, alias construction or ordinary payload shape.

Every metadata query below has a closed set of possible owners. Each owner must
provide the queried entry with the same complete contract. Missing or incompatible
entries are configuration errors, not false, empty or a runtime fallback. Do not
widen a closed catalogue to Any or an arbitrary Declaration and assume its custom
properties remain available. These are source proposals, not typechecked compiler
output; the ordinary owner-availability and closed-static checks remain mandatory.

## 1. Activation features: replace repeated support lists

The current forty scenarios repeatedly list the same four schemas and seven
rules, alongside their distinct concrete fixtures. Replace that repeated support
list with one private, finite catalogue and a typed classification on its entries.
Keep the concrete fixtures explicit: preparing BoxA must not accidentally activate
BoxB, Turret or another feedback channel.

A shared configuration/activationFeature.mud would declare:

```mud
family ActivationFeature { Core, Feedback, LinkEffects }
```

Each listed support declaration receives exactly one stored entry:

```mud
rule PublishSpellEvents on magic: Magic [mut] {
    ~activationFeature: configuration.ActivationFeature = configuration.ActivationFeature.Core

    when magic.pending changes
    if exists event in magic.pending : true
    then {
        let events = magic.pending
        magic.pending = empty
        magic.published = events
    }
}
```

These are excerpts in the existing owning paths, not alternative declarations to
compile beside the originals. Preserve each file's current part-only header.
When every top-level declaration in a file has the same feature, use a file default.
For spells/state.mud, the order would be:

```mud
~activationFeature: configuration.ActivationFeature = configuration.ActivationFeature.Core

using world
using sympathy
```

In a private file, part only precedes even that default. A default applies to
compatible top-level declarations written in that file; it does not classify a
family's members, imported names, descendants or other files. Use direct owner
entries in mixed files such as sympathy/linkState.mud, where only the reactive
rule belongs in this activation catalogue.

| Feature | Complete catalogue membership |
| --- | --- |
| Core | world.Entity, world.Creature, spells.Spellcaster, spells.Magic, spells.CanSelect, spells.CanAttempt, spells.ConcentrationWithinLimit, sympathy.TargetUsable, sympathy.CanLink, sympathy.ExclusiveSympathy, spells.PublishSpellEvents |
| Feedback | feedback.FeedbackChannel, feedback.PlanSpellFeedback |
| LinkEffects | sympathy.PrepareLinkEffects |

A proposed private configuration/activationSelection.mud contains the single
registration list. Its alias stores requested features and derives a finite
collection of the actual original declaration values:

```mud
part only

using world
using spells
using sympathy
using feedback

alias ActivationSelection {
    let features: ActivationFeature [* unique] = empty
    let declarations := foreach declaration in [
        Entity, Creature, Spellcaster, Magic,
        CanSelect, CanAttempt, ConcentrationWithinLimit,
        TargetUsable, CanLink, ExclusiveSympathy, PublishSpellEvents,
        FeedbackChannel, PlanSpellFeedback, PrepareLinkEffects
    ] if (features | [ActivationFeature.Core]) has declaration~activationFeature --> declaration
}
```

Core is always included. A feature request adds support; it cannot silently remove
an invariant or allow inactive Boolean-call pruning to bypass admission. The
catalogue is part-only because it contains private rule identities. The shared
ActivationFeature type does not reveal those identities or grant activation rights.

A plain feature-to-declarations dictionary could also shorten these lists. The
reason to choose metadata here is to keep each support declaration's activation
classification beside that declaration, queryable independently of a particular
startup expression. The catalogue registers identities; the owner supplies their
classification. This costs two explicit checks when registering new support.
Metadata does not eliminate that registration cost or automatically discover code.

A selection scenario becomes:

```mud
start with {
    configuration.ActivationSelection().declarations,
    MagicWorld, Player
}
```

A feedback scenario explicitly opts into its consumer and concrete channel:

```mud
start with {
    configuration.ActivationSelection([configuration.ActivationFeature.Feedback]).declarations,
    MagicWorld, Player, PlayerFeedback
}
```

Sympathy scenarios additionally list their particular boxes. Link-effect scenarios
request LinkEffects. Combining both features activates their union. Initialisation
is still the ordinary unordered, identity-deduplicated start with contribution;
there is no new startup priority or action execution.

The consumer is the static start expression. Its alias construction, finite
comprehension and metadata reads must be closed-static; no action, live field,
active population query or native call participates. Filtering precedes initial
materialisation and returns a flat collection, not nested feature bundles.

This deliberately retains one registration site. all Thing enumerates effective
concrete things, not all inactive schemas and rules. There is no invented all
ActivatableDeclarations query. Auto-discovery would need a separate catalogue API;
it is unnecessary for this improvement. A new support declaration must be added
to the catalogue once and classified once, rather than repeated in every scenario.

Useful implementation consequence: an elaborator can precompute the selected
identity set for each static feature request. This is ordinary static evaluation,
not a user promise that changes runtime semantics.

**Required evidence before adoption:** default selection equals precisely the
current eleven core entries; Feedback adds precisely two; LinkEffects adds one;
combination adds three; duplicate features change no membership; a new explicit
fixture cannot pull in another fixture. Check every scenario against its previous
activation set, including reachable-test contribution closure.

## 2. Feedback capabilities: make receiver filtering real

A device without haptics, a muted output profile or a headless consumer should not
receive work it cannot perform. A declaration-level capability description is a
useful input to the existing feedback planner.

Current FeedbackAsset is an alias containing a Text name. Different constructed
values do not each have their own canonical metadata owner. Do not attach one
metadata body to FeedbackAsset and pretend that FeedbackAsset("shared") and
FeedbackAsset("success") thereby acquire different annotations.

For this statically authored example, replace that open textual identifier with a
closed, shared resource family. Its members are resource identities; they do not
load or play resources. The proposed example catalogue is:

```mud
family FeedbackModality { Visual, Audio, Haptic }

family FeedbackAsset {
    AmbientGlow {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Visual]
    },
    SelectionFlash {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Visual]
    },
    CastChime {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Audio]
    },
    LegacyPulse {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Haptic]
    },
    FailureChime {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Audio]
    },
    SuccessFlash {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Visual]
    },
    CancelPulse {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Haptic]
    },
    RejectionChime {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Audio]
    }
}
```

These resources define the proposed Mud-only example configuration; they are not
assertions about the Unity assets. Apply this complete one-to-one replacement to
all tables and equality-based scenario expectations:

| Current Text key | Proposed FeedbackAsset member | Required modality |
| --- | --- | --- |
| global | AmbientGlow | Visual |
| specific | SelectionFlash | Visual |
| shared | CastChime | Audio |
| excluded | LegacyPulse | Haptic |
| failure | FailureChime | Audio |
| success | SuccessFlash | Visual |
| cancel | CancelPulse | Haptic |
| rejected | RejectionChime | Audio |

This classification is a chosen presentation design, not an inference from the
opaque old keys. An all-enabled channel preserves every old association and
occurrence under this bijection. Repeated occurrences reference the same member.
Actual Unity resource bindings remain an adapter responsibility as before.

The metadata describes a resource declaration's technical delivery requirements.
It does not replace spell-domain associated data. An ordinary family data slot
could implement the same filter, but metadata also permits declaration/adapter
inspection through the existing reflective surface without adding an instance
payload or inventing a field on every resource handle. The planner explicitly
consumes it; the language assigns no special privilege to the modalities name.

FeedbackChannel gains ordinary configuration:

```mud
let allowedModalities: FeedbackModality [* unique] = [
    FeedbackModality.Visual, FeedbackModality.Audio, FeedbackModality.Haptic
]
```

This is a field, not metadata: each channel configures its allowed work. Its
static default admits all modalities. An immutable per-channel override selects
a receiver profile; live mute controls, if later required, belong in ordinary
mutable state and produce ordinary dependencies, never runtime metadata writes.

After the existing global/specific merge and global-only exclusions, filter the
resulting phase asset set:

```mud
let permitted := foreach asset in effects
    if forall modality in asset~modalities : allowedModalities has modality --> asset
```

The policy is **all required modalities**, not any supported modality. An atomic
Audio+Visual resource is omitted if audio is unavailable. For independent delivery,
model separate audio and visual resources; do not silently play half an asset.
The metadata cardinality excludes an unclassified empty requirements set.

Apply the identical predicate to selectionRejected with an ordinary ordered
comprehension. It retains every permitted occurrence, including duplicates.
Keep phase ordering, within-phase uniqueness, exclusion origin and captured aim
unchanged. The same asset in Partial and Success remains two phase requests.
If every asset is filtered out, requestFor produces empty and no feedback message
is created. An empty allowed set intentionally silences the channel.

Filtering cannot alter CastOutcome, reservations, relations or the spell's
acceptance. It prevents unavailable presentation work rather than adding another
spell admission condition. It also does not certify successful native delivery.

Useful implementation consequence: the resource family's static requirements may
be represented by bit masks or precomputed compatibility tables. Such choices must
preserve the predicate and cannot reorder phases or merge occurrences.

**Required evidence before adoption:** all-enabled preserves existing requests;
visual-only removes audio/haptic resources; empty allowed modalities produces no
request; a combined Audio+Visual resource requires both; rejection repetitions
survive filtering; phase repetitions survive filtering; exclusion/reintroduction
still works. Test the unchanged domain state as well as the filtered outputs.

The cost is deliberate: family membership is closed per linked model. If future
requirements demand externally supplied dynamic resource IDs, keep those IDs as
values and use an ordinary descriptor/configuration dictionary instead. Per-value
capabilities in that alternative are data, not invented instance metadata.

## 3. Regression concerns: select tests without weakening their worlds

Annotate test declarations with a closed concern vocabulary:

```mud
family TestConcern { Selection, PairAdmission, Contributions, Lifecycle, Feedback }
```

For scenarios/contributions.mud, use a file default after part only and before using:

```mud
~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Contributions]
```

The end-to-end feedback case should explicitly use all three concerns:

```mud
~checks: configuration.TestConcern [1..* unique] = [
    configuration.TestConcern.Feedback,
    configuration.TestConcern.Selection,
    configuration.TestConcern.PairAdmission
]
```

An explicit value replaces a file default; it does not append to it. Other
coherent scenario files use the corresponding default. Mixed provider scenarios
receive explicit per-test concerns where their actual contract differs. Every
one of the forty tests must have a nonempty effective checks value.

The consumer is a proposed static regression driver, not a new Mud instruction.
Given requested concerns R and the compiler's resolved test catalogue T in the
authorised test context, choose roots {t in T | t.checks intersects R}. No filter
means all tests. An empty matched root set is a configuration error rather than
a successful run of zero checks. Unknown concern names are errors. Multiple
concerns use union selection and canonical test identity deduplication.

For each selected root, retain the existing statically reachable test closure and
its combined start with contributions. A concern filter must never remove a
called test's fixtures or rules. It does not change test reachability, create
cross-part uses rights, expose private tests to the host or invoke tests as normal
operations. The compiler/test context may inspect its own part-only test catalogue.
No claim is made that a regression driver already exists.

Examples: changing pair admission selects provider pair tests and the end-to-end
feedback case; changing effect projection selects contributions tests; changing
cancellation selects lifecycle tests. Concern coverage is a manually maintained
regression contract, not inferred proof of every dependency. CI should still run
all forty tests when execution becomes available.

**Required evidence before adoption:** all forty tests are classified; each
concern selects at least one root; multi-concern selection deduplicates; the real
sympathy-to-feedback case is selected by all three listed concerns; called-test
closure remains intact even when a child's own tags do not match the request.

## Choices rejected for this example

| Candidate | Decision |
| --- | --- |
| Move Spell.slot or needsConcentration to metadata | Keep associated family data: these are already explicit spell-domain parameters consumed by admission and concentration. Moving them adds no capability. |
| Mark fields with save/replicate flags | Defer: no persistence or replication consumer/contract exists here. |
| priority, runBefore or debounce tags on reactive rules | Reject: they would introduce causal scheduling semantics beyond this example's scope. |
| commutative, cache or pure promises | Reject: user tags cannot manufacture overloads, proofs, permissions or safe reuse. |
| Tag grabbed, present, selected or concentration | Keep world state/derivations. Static declaration classification cannot replace per-entity live values. |
| Put tags on start with, when, branches or alias instances | Reject: these are not independent anchored metadata owners. Put classification on the relevant declaration or use ordinary data. |
| Filter by file provenance or presentation name | Reject: moving a file or renaming a label must not silently change activation or capability policy. |

## Adoption order and scope

Adopt activation classification first: it removes repeated setup while preserving
the current domain contract exactly. Next adopt the resource catalogue and explicit
capability filter as an intentional presentation-policy extension. Add test
concerns when their regression selector is implemented, so no annotations are
installed without a consumer.

These three mechanisms remain separate. ActivationFeature selects supporting
world declarations; TestConcern selects test roots; FeedbackModality filters
presentation resources. No generic string tag bag or new reserved metadata name
is required. configuration is a proposed ordinary path in the existing part;
part-only catalogues and direct using rules remain in force. No new part, uses
permission, compiler implementation, Unity change or runtime algorithm is proposed.

The current .mud model remains the reference until a follow-up applies the chosen
proposal and its corresponding evidence. This document settles the recommendation
and its consumer contracts; it does not record a language ADR or silently change
normative rules.

## Existing contracts used

- [Source headers, file defaults and parts](../../../specification/05-source-text.md).
- [Activation and metadata syntax](../../../specification/08-concrete-grammar.md).
- [Nominal visibility and metadata ownership](../../../specification/10-names-and-anchors.md).
- [Static checking and closed evaluation](../../../specification/11-type-system.md).
- [Family identity and associated data](../../../specification/14-closed-families.md).
- [Current metadata decision](../../decisions/ADR-087-reflective-metadata-stable-descriptors-and-external-visibility.md).
