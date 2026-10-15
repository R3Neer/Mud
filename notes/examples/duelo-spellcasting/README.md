---
title: Duelo spell controller modelling exercise
status: analysis
tags:
  - mud/examples
  - mud/expressiveness
---

# Duelo spell controller

This is an informative Mud model of Duelo's spell controller, not a language
rule, a Unity port or an implemented adapter. It exercises selection,
concentration, unlock changes, cast outcomes and cancellation against the
existing C# contracts. Unity remains read-only. Electricity is excluded.

```mud
PlayerCaster.Select(Spell.SympathyLink)
PlayerCaster.CastSample(CastResult.Partial, Aim(r0, r0, r0, ["crate"]))
PlayerCaster.CastSample(CastResult.Success, Aim(r0, r0, r0, ["other-crate"]))
```

These are effect-call fragments for a `then`, after activating Caster,
IsResolvable, ConcentrationWithinLimit and PlayerCaster.
The first cast keeps targeting; the second finishes targeting while retaining
the concentration spell's activity. The provider outcomes are sample inputs,
not an implementation of Sympathy's target selection or physics.

## Contracts before representation

The reviewed source root is `D:/Unity/Projects/Duelo/Assets`. The model's
authority for game behaviour is the implementation, rather than design notes:

| Component | Responsibility and model boundary |
| --- | --- |
| `Scripts/Motors/SpellCasting/SpellCasterTag.cs` | Supplies capacity, initial unlocked count, concentration limit and definitions. The fixture declares a valid initial configuration directly. |
| `Scripts/Motors/SpellCasting/SpellCaster.cs` | Owns active flags, selected slot, concentration accounting, unlock adjustment, dispatch and event order. This is the modelled controller. |
| `Scripts/Motors/SpellCasting/ISpell.cs` | Defines slot identifiers, RequiresConcentration, Cast, Cancel and self-cancellation. Providers remain external; the model records their invocation boundaries. |
| `Scripts/Player/States/SpellCastingState.cs` | Uses selection/cast Boolean results to control targeting. Its movement, input and player-state transitions remain external. |
| `Scripts/Motors/SpellCasting/SpellFeedbackManager.cs` | Consumes selected, failed-selection, attempted-cast and cancelled events. Feedback composition and execution remain external. |
| `Scripts/Motors/SpellCasting/SpellBarManager.cs` | Consumes unlocked-count notifications. Drawing and fading remain external. |
| `Scripts/Motors/SpellCasting/PassiveMagicalCaster.cs` | Separately traverses configured definitions; it is not dispatch of the selected active spell and is outside this controller model. |

Four different notions must survive modelling:

1. A slot is **configured** when it has an installed provider.
2. It is **unlocked** by its numeric position relative to unlockedCount, even
   when it has no provider.
3. It is **active** after successful selection until explicit cancellation or
   successful non-concentration casting. Selecting another spell leaves it active.
4. Exactly one slot, or None, is **selected** for dispatch. Activity does not
   imply selection, and selection is not automatically repaired after relocking.

Concentration is reserved on selection, before the first cast. The count is the
number of active configured spells requiring concentration. The model derives
it instead of maintaining a second mutable counter. This is equivalent within
the fixed-definition assumptions below. A zero limit blocks concentration
spells but permits non-concentration spells.

Selecting an already active slot attempts cancellation and returns false without
a failed-selection notification. A successful selection of another slot never
cancels the old one. Locked, missing-provider and concentration-full selections
retain state and notify failed selection. ActivationFailed is unreachable for
the admitted fixed, valid configuration after those checks.

Only CastResult.Success completes an actual cast. None, Partial and Failed
retain both activity and selection and return false. Successful concentration
casting clears selection but retains activity; non-concentration success also
deactivates the spell without calling Cancel. No selection returns true without
calling a provider or notifying an attempted cast.

AdjustSpells clamps the unlocked count but does not cancel or deselect anything.
It notifies even when the clamped count is unchanged. Consequently, relocking
a selected spell makes GetSpellAt return null: casting returns true without an
attempt notification and leaves selection unchanged; cancellation becomes a
no-op. Selecting that still-active slot follows the active-first cancellation
path, also a no-op, returning false without a failed-selection notification.
Unlocking it again makes cancellation possible. The model preserves this behaviour.

Cancellation of an available provider calls Cancel and notifies cancellation
even if its active flag is already false. Background self-cancellation does not
clear a different selected slot. None or a non-resolvable provider is a no-op.

## Files and representation

- `controller.mud` contains the catalogue, pure selection policy, controller
  state, public operations and observation query.
- `scenarios.mud` contains declarative Mud tests with fresh fixture state.
- `reactive-presentation.mud` is an optional Mud-oriented consumer with reactive
  update examples; it does not replace the Unity callback trace.
- `mud.part` defines this example's part without dependencies.

The three installed fixture definitions are test configurations: SympathyLink
and SympathyMagnet require concentration; Fireball does not. Their names come
from the real enum, but the reserved spell implementations are not claimed to
exist. Capacity is 17, initially three slots are unlocked, and the concentration
limit is two. NoConcentrationCaster overrides that limit to zero.
ThreeConcentrationCaster additionally classifies its Fireball test provider as
requiring concentration, solely to exercise a third candidate at the limit;
this is not a claim about an implemented Fireball spell. The complete
enum is retained so an unlocked slot can lack a provider and a configured slot
can be locked. No global start with activates the library fixtures; each test
chooses its initial population, including abstract Caster and IsResolvable.
Ancestry does not implicitly activate Caster; its inherited-schema/type
dependencies must be available. Boolean rules have an activation lifecycle:
the driver must keep this predicate active, otherwise inactive-call pruning
would not enforce its test.

SelectionPlan is a pure priority policy: active-toggle takes precedence over
locked checks. Its optional singleton fields describe actual work. IsResolvable
is a Boolean rule. Cancellation and cast handling use domain subactions with
if admission guards. Pure optional policies return the resolvable spell or
empty; `[?]` extraction omits the dependent call when no spell is available.
The same extraction handles planned cancellation and rejection. The activation
iteration retains its multi-statement body over the planned spell. Optional
contracts use `[?]`, the abbreviation for `[0..1]`.

The completion dispatch infers its callable output contract, retaining receiver
capabilities, and selects the matching operation before calling it:
successful concentration, successful instant cast, or continued targeting.
None, Partial and Failed therefore complete normally with castFinished=false.
A genuinely false subaction guard would produce IfRefusal, not a skipped body;
ordinary bare calls preserve that refusal or any Error rather than ignoring it.
Decisions are captured before the mutations they govern.

The guards are part of the executable contracts: CancelAvailableSpell and
AttemptCast require a resolvable provider; CompleteConcentrationCast and
CompleteInstantCast require the corresponding successful outcome and spell
kind; KeepTargeting requires a non-success outcome. Membership comparisons bind
more tightly than `and`, so these conditions need no grouping parentheses.

Public gameplay rejection remains normal completion where required by the C#
contract. Moving such cases into an action guard would turn them into Refusal
and could suppress the required trace entries. CompleteConcentrationCast and CompleteInstantCast declare `after` contracts
for their final castFinished/selection state; the instant case also guarantees
the spell is inactive. These are consequences of their existing bodies within
the fixed non-reentrant model boundary. General admission and postcondition
examples, including AfterRefusal rollback, are in
[[specification/26-public-boundary#Admission and completion examples]]. The
`after` clauses in scenarios.mud are test assertions, not action postconditions.

The mutable state includes two explicitly auxiliary fields: selectionAccepted
and castFinished preserve the corresponding C# Boolean results for inspection.
They are not ActionReply payloads. Ordinary gameplay rejection is a completed
model operation with selectionAccepted=false, not a Mud Refusal or Error.
Cancel and unlock operations do not redefine those last per-method results.
These compatibility projections are harness requirements, not evidence that
Mud actions need arbitrary result payloads. A Mud-oriented exterior would use
the action reply for admission/completion, looks for current state and messages
for occurrences; it need not preserve the C# Boolean-method interface.

## Provider and observation boundary

CastSample accepts the outcome of one hypothetical synchronous provider call.
The supplied outcome is ignored when no provider can be resolved. ISpell.Cast
returns a non-nullable enum: CastResult.None is an actual result, never a missing
provider sentinel. Aim carries an uninterpreted point and optional stable host
object token; the controller does not interpret geometry or object internals.
The token registry and native conversions are adapter responsibilities.

lastTrace is an ordered, per-operation data trace. Each entry captures the core
state at the indicated boundary. CallCast and CallCancel record intended native
invocations; they do not execute C#. CastAttempted is observed before success
cleanup. CallCancel and Canceled occur after deactivation and before clearing
the matching selection. This retains observable ordering for contract review.
StartSample records the initial count notification; the driver calls it once
after initialization, as Unity Start would. Unity enable/disable/destroy and
registration are not simulated. In particular, disable does not cancel spells.

These entries are not Mud messages and replaying them after completion is not
an equivalent implementation of synchronous C# callbacks. The Observation look
exposes the trace and final state for a modelling harness. A production bridge
could use contracted `from Csharp` calls or an action/look/message boundary;
this exercise does not define either adapter. D-109/D-121 require explicit
read/effect/conversion contracts. Native spelling, hosting and lifetime work
remain separate from the model's game rules.

## Deliberate limits

The equivalence claim is limited to initialized, serial, non-reentrant controller
operations with fixed providers and fixed RequiresConcentration values. Provider
Cast/Cancel and event subscribers must not synchronously mutate the controller
or raise self-cancellation during another operation. SelfCancelledSample models
a notification between operations. The real C# controller has no reentrancy
guard and re-reads selected state across callbacks. Real Sympathy cancellation
can re-enter through its session callback and produce repeated cancellation
notifications. Arbitrary callback nesting and those intermediate mutations are
not represented here; they cannot be replaced by atomic Mud operations without
an explicit bridge design.

Configuration assumptions are 0 <= initialUnlockedCount <= capacity <= 17,
nonnegative concentration limit, unique installed slots within capacity and
stable spell definitions. Null entries, duplicate registration/subscriptions,
absent SpellCasterTag, arbitrary numeric enum casts, native exceptions and
initial counts outside capacity are outside this exercise. The constructor
does not itself clamp initialUnlockedCount in C#. Unlock arithmetic here uses
exact Int and matches only C# additions that do not overflow Int32.

Controller diagnostics, UI timing, feedback selection, spell internals and
PassiveMagicalCaster are external components, not silently completed systems.
The fixture does not introduce a new Mud runtime rule or settle causal scheduling.

## Evidence and expressiveness questions

Existing Unity tests reviewed include SpellCasterSelectionTests,
SpellCasterConcentrationTests, SpellCasterCastFlowTests,
SpellCasterCancellationTests, SpellCasterUnlockingTests and lifecycle tests under
`Tests/Motors/SpellCasting/Core/PlayMode`. The relocking scenarios additionally
follow directly from SpellCaster.GetSpellAt and its callers.

The Mud scenarios are source-level contract examples, not executed tests: the
repository has no Mud compiler/runtime. Repository validators check the
surrounding specification artefacts; they do not typecheck or execute this model.
Neither Unity tests nor Unity were run for this exercise.

Evaluate whether the selection policy reads naturally, whether derived
concentration avoids unnecessary bookkeeping and whether the decomposition into
guarded domain operations stays readable. Distinguish shortcomings of this
representation from missing language capabilities. SelectionPlan could also be
represented by a union of nominal decision aliases using existing constructs.

The Boolean result projections and callback trace preserve a C# interface for
comparison. They do not measure the ceremony of a Mud-oriented architecture.
Native callback reentrancy belongs to the chosen bridge contract; an adapted
exterior need not retain arbitrary C# callback interleavings. Neither issue
justifies new source syntax on the evidence of this exercise alone.

## Invariants, postconditions and reactive consumers

ConcentrationWithinLimit is activated explicitly by every controller scenario.
Nat excludes a negative concentration but does not relate its derived count to
maxConcentration. The always rule protects this cross-field checkpoint contract;
it is not a repairing action. Valid serial controller operations already
preserve it. It also documents why independently admitted proposals cannot be
assumed jointly capacity-safe. The existing causal checkpoint interface applies;
this example supplies no scheduler or completion algorithm.

The completion subactions state their operation-specific final guarantees with
after. These conditions are not world invariants: ordinary targeting may retain
selection and active spells. No invariant requires selected spells to remain
unlocked, because the Unity contract permits relocking without deselection.
Unlocked capacity is enforced by the existing clamping policy; a redundant
second always check is not added merely to increase syntax coverage.

The optional presentation variant stores a consumer's visible targeting state
and updates it through a reactive rule after observed controller changes.
Its abstract schema deliberately leaves caster to the concrete presentation.
The two accompanying scenarios are declarative source contracts, not executed
tests. The variant assumes fresh fixtures and normal binding observation;
reactivation/resynchronization and a real Unity UI adapter are not specified.
If only a query is needed, a derived field is preferable to storing this state.

A changes trigger observes consolidated snapshots. It cannot reproduce every
synchronous notification, an unchanged-value notification, or transient states
inside one operation. The reactive variant therefore leaves the existing
lastTrace writes intact and makes no claim of callback/reentrancy equivalence.
An action is not a causal when source. Per-attempt notifications would require
an explicit message/adapter occurrence contract, not guessing from final state.
