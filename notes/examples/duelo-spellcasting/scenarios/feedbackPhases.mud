part only

using world
using spells
using sympathy
using fixtures
using feedback

# Phase planning contracts isolated with typed domain facts.

test FeedbackSelectedEffectsAreMerged {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Selected, caster = Player, spell = Spell.Fireball,
        aim = Aim(Point3(r1, r2, r3), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [FeedbackGroup(
            FeedbackStage.Selected,
            [FeedbackAsset("specific"), FeedbackAsset("shared"), FeedbackAsset("global")]
        )]
        forall request in PlayerFeedback.requests : request.aim.point == Point3(r1, r2, r3)
        MagicWorld.pending == empty
    }
}

test FeedbackSuccessfulAttemptHasTwoPhases {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Attempted, caster = Player, spell = Spell.Fireball,
        outcome = CastOutcome.Success, aim = Aim(Point3(r4, r5, r6), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [
            FeedbackGroup(FeedbackStage.Partial,
                [FeedbackAsset("shared"), FeedbackAsset("global")]),
            FeedbackGroup(FeedbackStage.Success,
                [FeedbackAsset("shared"), FeedbackAsset("global"), FeedbackAsset("success")])
        ]
    }
}

test FeedbackPartialAttemptHasNoSuccessPhase {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Attempted, caster = Player, spell = Spell.Fireball,
        outcome = CastOutcome.Partial, aim = Aim(Point3(r0, r0, r0), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [
            FeedbackGroup(FeedbackStage.Partial,
                [FeedbackAsset("shared"), FeedbackAsset("global")])
        ]
    }
}

test FeedbackFailedAttemptUsesFailureEffects {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Attempted, caster = Player, spell = Spell.Fireball,
        outcome = CastOutcome.Failed, aim = Aim(Point3(r0, r0, r0), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [
            FeedbackGroup(FeedbackStage.Failed, [FeedbackAsset("failure")])
        ]
    }
}

test FeedbackCancellationRetainsItsAim {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Cancelled, caster = Player, spell = Spell.Fireball,
        aim = Aim(Point3(r7, r8, r9), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [
            FeedbackGroup(FeedbackStage.Cancelled, [FeedbackAsset("cancel")])
        ]
        forall request in PlayerFeedback.requests : request.aim.point == Point3(r7, r8, r9)
    }
}
